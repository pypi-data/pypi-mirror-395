import argparse
import json
import logging
import os
from collections import Counter
from enum import Enum
from typing import List

from bs4 import BeautifulSoup
from tqdm import tqdm
from transformers import AutoModelForCausalLM, AutoTokenizer

from tooltalk.utils.schemas import BaseGenerationKwargs
from tooltalk.apis import ALL_APIS, APIS_BY_NAME, SUITES_BY_NAME
from tooltalk.evaluation.metrics import get_metrics
from tooltalk.evaluation.tool_executor import BaseAPIPredictor, ToolExecutor
from tooltalk.utils.file_utils import get_names_and_paths

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def create_messages(conversation_history):
    messages = []
    for turn in conversation_history:
        if turn["role"] == "user" or turn["role"] == "assistant":
            messages.append({"role": turn["role"], "content": turn["text"]})
        elif turn["role"] == "api":
            messages.append(
                {
                    "role": "assistant",
                    "content": "",
                    "function_call": {
                        "name": turn["request"]["api_name"],
                        "arguments": json.dumps(turn["request"]["parameters"]),
                    },
                }
            )
            response_content = {
                "response": turn["response"],
                "exception": turn["exception"],
            }
            messages.append(
                {
                    "role": "function",
                    "name": turn["request"]["api_name"],
                    "content": json.dumps(response_content),
                }
            )
    return messages


def extract_dict_from_html_tag(text, html_tag="tool_call"):
    soup = BeautifulSoup(text, "html.parser")
    tool_call_tag = soup.find(html_tag)

    if tool_call_tag:
        tool_call_str = tool_call_tag.get_text(strip=True)
        try:
            # Convert the JSON string to a dictionary
            tool_call_dict = json.loads(tool_call_str)
            return tool_call_dict
        except json.JSONDecodeError as e:
            print(f"Failed to decode JSON: {e}")
            return None
    else:
        return None


class HFPredictor(BaseAPIPredictor):
    def __init__(
        self,
        model_name,
        model_kwargs,
        apis_used,
        disable_docs=False,
        generation_kwargs: BaseGenerationKwargs | None = None,
    ):
        self.model_name = model_name
        self.model = AutoModelForCausalLM.from_pretrained(
            model_name,
            device_map="auto",
            **model_kwargs,
        )
        self.tokenizer = AutoTokenizer.from_pretrained(model_name)

        self.tools = []
        for api in apis_used:
            doc = api.to_openai_doc(disable_docs)
            required = doc.pop("required")
            doc["parameters"]["required"] = required
            self.tools.append({"type": "function", "function": doc})
        self.generation_kwargs = (
            generation_kwargs if generation_kwargs is not None else {}
        )

    def predict(self, metadata: dict, conversation_history: dict) -> dict:
        messages = create_messages(conversation_history)

        inputs = self.tokenizer.apply_chat_template(
            messages,
            chat_template="tool_use",
            tools=self.tools,
            tokenize=True,
            add_generation_prompt=True,
            return_dict=True,
            return_tensors="pt",
        )
        inputs = {k: v.to(self.model.device) for k, v in inputs.items()}

        response = self.model.generate(**inputs, **self.generation_kwargs)
        decoded_response = self.tokenizer.decode(
            response[0][len(inputs["input_ids"][0]) :]
        )
        tool_call_response = extract_dict_from_html_tag(decoded_response)

        metadata = {
            "hf_request": {
                "model": self.model_name,
                "messages": messages,
                "functions": self.tools,
            },
            "hf_response": decoded_response,
        }

        if tool_call_response:
            try:
                api_name = tool_call_response["name"]
                parameters = tool_call_response["arguments"]
                return {
                    "role": "api",
                    "request": {"api_name": api_name, "parameters": parameters},
                    # store metadata about call
                    "metadata": metadata,
                }
            except:
                print(f"Failed to parse tool call response: {tool_call_response}.")
        else:
            return {
                "role": "assistant",
                "text": decoded_response,
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
    parser.add_argument(
        "--max_new_tokens",
        type=int,
        default=1024,
        help="[Hugging Face] The maximum numbers of tokens to generate, ignoring the number of tokens in the prompt.",
    )
    parser.add_argument(
        "--temperature", type=float, default=0.0, help="[Hugging Face] Temperature"
    )
    parser.add_argument("--top_p", type=float, default=None, help="[Hugging Face]Top_p")

    return parser


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

    total_metrics = Counter()
    os.makedirs(args.output_dir, exist_ok=True)
    tool_executor = ToolExecutor(init_database_dir=args.database)
    for file_name, file_path in tqdm(get_names_and_paths(args.dataset)):
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

            predictor_func = HFPredictor(
                model_name=args.model,
                model_kwargs={"precision": "auto"},
                apis_used=apis_used,
                generation_kwargs=generation_kwargs,
                disable_docs=args.disable_documentation,
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
