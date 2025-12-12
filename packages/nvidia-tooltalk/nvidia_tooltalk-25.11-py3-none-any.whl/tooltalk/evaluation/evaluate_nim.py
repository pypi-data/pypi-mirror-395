import argparse
import json
import logging
import os
from collections import Counter
from enum import Enum
from typing import List
from pathlib import Path

import requests
from tqdm import tqdm
from importlib import resources

from tooltalk.utils.schemas import BaseGenerationKwargs, Hf2OpenAi
from tooltalk.apis import ALL_APIS, APIS_BY_NAME, SUITES_BY_NAME
from tooltalk.evaluation.metrics import get_metrics
from tooltalk.evaluation.tool_executor import BaseAPIPredictor, ToolExecutor
from tooltalk.utils.file_utils import get_names_and_paths

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_messages(conversation_history, metadata=None):
    system_prompt = "You are a helpful assistant. Here is some user data:" \
                    "\nlocation: {location}" \
                    "\ntimestamp: {timestamp}" \
                    "\nusername (if logged in): {username}"
    
    messages = []
    
    # Add system prompt if metadata is provided
    if metadata:
        formatted_system_prompt = system_prompt.format(
            location=metadata.get("location", "unknown"),
            timestamp=metadata.get("timestamp", "unknown"),
            username=metadata.get("username", "unknown")
        )
        messages.append({
            "role": "system",
            "content": formatted_system_prompt
        })
    
    tool_call_id = "123456789"
    for turn in conversation_history:
        if turn["role"] == "user" or turn["role"] == "assistant":
            messages.append({"role": turn["role"], "content": turn["text"]})
        elif turn["role"] == "api":
            messages.append(
                {
                    "role": "assistant",
                    "tool": turn["request"]["api_name"],
                    "parameters": json.dumps(turn["request"]["parameters"]),
                    "tool_call_id": tool_call_id,
                }
            )
            response_content = {
                "response": turn["response"],
                "exception": turn["exception"],
            }
            messages.append(
                {
                    "role": "tool",
                    "name": turn["request"]["api_name"],
                    "content": json.dumps(response_content),
                    "tool_call_id": tool_call_id,
                }
            )
            tool_call_id = str(int(tool_call_id) + 1)
    return messages


class NIMPredictor(BaseAPIPredictor):
    def __init__(
        self,
        url: str,
        model: str,
        apis_used: bool,
        disable_docs=False,
        generation_kwargs: BaseGenerationKwargs | None = None,
    ):
        self.url = url
        self.model = model
        self.generation_kwargs = (
            Hf2OpenAi.map(generation_kwargs) if generation_kwargs is not None else {}
        )
        self.tools = []
        for api in apis_used:
            doc = api.to_openai_doc(disable_docs)
            required = doc.pop("required")
            doc["parameters"]["required"] = required
            self.tools.append({"type": "function", "function": doc})

        API_KEY = os.environ.get("API_KEY", None)
        self.headers = {
            "content-type": "application/json",
        }
        if API_KEY is not None:
            self.headers["Authorization"] = f"Bearer {API_KEY}"

    def predict(self, metadata: dict, conversation_history: dict) -> dict:
        messages = create_messages(conversation_history, metadata)
        payload = {
            "messages": messages,
            "tools": self.tools,
            **self.generation_kwargs,
        }
        if self.model is not None:
            payload["model"] = self.model

        if logging.getLogger().isEnabledFor(logging.DEBUG):
            logging.debug(f"Request payload: {payload}")
        response = requests.post(
            self.url, headers=self.headers, json=payload, stream=True
        )
        try:
            response_json = response.json()
            openai_message = response_json["choices"][0]["message"]
        except (requests.exceptions.JSONDecodeError, KeyError):
            raise RuntimeError(
                f"Request failed!\n\nInput:\n{payload}\n\nResponse:\n{response.text}"
            )

        metadata = {
            "nim_request": {
                "model": self.model,
                "messages": messages,
                "functions": self.tools,
            },
            "nim_response": response_json,
        }

        if "tool_calls" in openai_message:
            try:
                function_call = openai_message["tool_calls"][0]["function"]
                api_name = function_call["name"]
            except Exception as e:
                logger.warning(f"No function call found: {e}")
                logger.info(f"Returning assistant message: {openai_message['content']}")
                return {
                    "role": "assistant",
                    "text": openai_message["content"],
                    # store metadata about call
                    "metadata": metadata,
                }
            try:
                parameters = json.loads(function_call["arguments"])
            except json.decoder.JSONDecodeError:
                # check termination reason
                logger.info(
                    f"Failed to decode arguments for {api_name}: {function_call['arguments']}"
                )
                parameters = None
            return {
                "role": "api",
                "request": {"api_name": api_name, "parameters": parameters},
                # store metadata about call
                "metadata": metadata,
            }
        else:
            return {
                "role": "assistant",
                "text": openai_message["content"],
                # store metadata about call
                "metadata": metadata,
            }


class EvalModes(str, Enum):
    PREDICT = "predict"
    EVALUATE = "evaluate"
    VALIDATE = "validate"


def get_arg_parser():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--url",
        type=str,
        default="https://integrate.api.nvidia.com/v1/chat/completions",
        help="NIM url",
    )
    parser.add_argument(
        "--dataset", type=str, help="Path to dataset for models to evaluate"
    )
    parser.add_argument(
        "--database", type=str, help="Path to database used in evaluation"
    )
    parser.add_argument(
        "--api_mode",
        type=str,
        choices=["exact", "suite", "all"],
        default="all",
        help="API mode to use for evaluation, determines which api docs to include",
    )
    parser.add_argument(
        "--model",
        type=str,
        required=False,
        help="Model to use for generation. Can be left empty if not required by the server.",
    )
    parser.add_argument(
        "--output_dir", type=str, help="Path to output model predictions"
    )
    parser.add_argument(
        "--reset",
        action="store_true",
        help="reset evaluation writing over any cached results",
    )
    parser.add_argument(
        "--disable_documentation",
        action="store_true",
        help="disable tool documentation sent to the model replacing with empty strings",
    )
    parser.add_argument(
        "--modes",
        choices=list(EvalModes),
        type=str,
        nargs="+",
        default=list(EvalModes),
        help="Evaluation modes",
    )
    parser.add_argument("--temperature", type=float, default=None, help="Temperature")
    parser.add_argument("--top_p", type=float, default=None, help="Top_p")
    parser.add_argument(
        "--max_new_tokens", type=int, default=1024, help="Max tokens to generate"
    )
    parser.add_argument(
        "--first_n", type=int, default=None, help="use only first n samples"
    )
    parser.add_argument("--debug", action="store_true", help="Enable debug mode")

    return parser

# In case the dir seems missing, check if we're calling inner package, eg. for data/easy
def check_internal_package_dir(dir: str):
    path_inside = os.path.join(Path(__file__).parent.parent.absolute().resolve(), dir)
    if os.path.isdir(dir):
        return dir
    elif os.path.isdir(path_inside):
        return path_inside
    else:
        raise FileNotFoundError(f"The requested directory {dir} was not found neither inside a package")

def main(flags: List[str] = None):

    parser = get_arg_parser()
    args = parser.parse_args(flags)

    generation_kwargs = {
        k: v
        for k, v in {
            "temperature": args.temperature,
            "top_p": args.top_p,
            "max_new_tokens": args.max_new_tokens,
        }.items()
        if v is not None
    }
    if EvalModes.PREDICT in args.modes:
        logger.info(
            f"Generation kwargs used: {generation_kwargs} | Default parameters will be used for: {[key for key in BaseGenerationKwargs.__annotations__.keys() if key not in generation_kwargs]}"
        )

    if args.debug:
        logging.getLogger().setLevel(logging.DEBUG)
        logging.basicConfig(level=logging.DEBUG)

    total_metrics = Counter()
    os.makedirs(args.output_dir, exist_ok=True)


    tool_executor = ToolExecutor(init_database_dir=check_internal_package_dir(args.database))
    dataset = check_internal_package_dir(args.dataset)
    if args.first_n is not None:
        file_names_and_paths = get_names_and_paths(dataset)[: args.first_n]
    else:
        file_names_and_paths = get_names_and_paths(dataset)
    for file_name, file_path in tqdm(file_names_and_paths):
        output_file_path = os.path.join(args.output_dir, file_name)
        if os.path.exists(output_file_path) and not args.reset:
            logger.info(f"Skipping {file_name} because it already exists")
            with open(output_file_path, "r", encoding="utf-8") as reader:
                conversation_with_metrics = json.load(reader)
            total_metrics += conversation_with_metrics["metrics"]
            total_metrics["num_conversations"] += 1
            continue

        logger.info(f"Running {file_name}")
        with open(file_path, "r", encoding="utf-8") as reader:
            conversation = json.load(reader)

        if EvalModes.PREDICT in args.modes:
            logger.info("Running prediction...")
            if args.api_mode == "exact":
                apis_used = [
                    APIS_BY_NAME[api_name] for api_name in conversation["apis_used"]
                ]
            elif args.api_mode == "suite":
                apis_used = [
                    api
                    for suite_name in conversation["suites_used"]
                    for api in SUITES_BY_NAME[suite_name].apis
                ]
            elif args.api_mode == "all":
                apis_used = ALL_APIS
            else:
                raise ValueError(f"Invalid api mode: {args.api_mode}")

            predictor_func = NIMPredictor(
                url=args.url,
                model=args.model,
                apis_used=apis_used,
                disable_docs=args.disable_documentation,
                generation_kwargs=generation_kwargs,
            )
            conversation = tool_executor.run_conversation(conversation, predictor_func)

        if EvalModes.EVALUATE in args.modes:
            logger.info("Running evaluation...")
            conversation = tool_executor.evaluate_predictions(conversation)
            logger.info(
                f"Conversation {file_name} pass: {conversation['metrics']['success']}"
            )
            total_metrics += conversation["metrics"]
            total_metrics["num_conversations"] += 1

            if EvalModes.VALIDATE in args.modes:
                logger.info("Validating evaluation...")
                for turn in conversation["conversation"]:
                    if "predictions" not in turn:
                        continue
                    for prediction in turn["predictions"]:
                        if prediction["role"] == "api":
                            assert "match" in prediction
                            assert "bad_action" in prediction

        with open(output_file_path, "w", encoding="utf-8") as writer:
            json.dump(conversation, writer, indent=4)

    logger.info("Finished processing conversations")
    if EvalModes.EVALUATE in args.modes:
        metrics = get_metrics(total_metrics)
        logger.info(f"Metrics: {json.dumps(metrics, indent=4)}")

        output_file = os.path.join(args.output_dir, "metrics.json")
        with open(output_file, "w") as f:
            json.dump(metrics, f, indent=4)

        logger.info(f"Metrics saved to {output_file}")


if __name__ == "__main__":
    main()
