"""
Copyright (c) Microsoft Corporation.
Licensed under the MIT license.

Evaluate Tool LLM on API-Talk dataset.
"""
import os
import json
import logging
import argparse
import time
import requests
from enum import Enum
from typing import List
from collections import Counter
from pathlib import Path

from openai import OpenAI
from tqdm import tqdm

from tooltalk.apis import APIS_BY_NAME, ALL_APIS, SUITES_BY_NAME
from tooltalk.evaluation.tool_executor import ToolExecutor, BaseAPIPredictor
from tooltalk.utils.file_utils import get_names_and_paths
from tooltalk.utils.openai_utils import openai_chat_completion
from tooltalk.evaluation.metrics import get_metrics
from tooltalk.evaluation.evaluate_nim import check_internal_package_dir


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


class OpenAIPredictor(BaseAPIPredictor):
    system_prompt = "You are a helpful assistant. Here is some user data:" \
                    "\nlocation: {location}" \
                    "\ntimestamp: {timestamp}" \
                    "\nusername (if logged in): {username}"

    def __init__(self, model, apis_used, disable_docs=False, base_url=None, api_key=None, 
                 max_new_tokens=None, temperature=None, top_p=None):
        self.model = model
        self.api_docs = [api.to_openai_doc(disable_docs) for api in apis_used]
        self.base_url = base_url
        self.api_key = api_key
        self.max_new_tokens = max_new_tokens
        self.temperature = temperature
        self.top_p = top_p

    def predict(self, metadata: dict, conversation_history: dict) -> dict:
        system_prompt = self.system_prompt.format(
            location=metadata["location"],
            timestamp=metadata["timestamp"],
            username=metadata.get("username")
        )

        openai_history = [{
            "role": "system",
            "content": system_prompt
        }]
        for turn in conversation_history:
            if turn["role"] == "user" or turn["role"] == "assistant":
                openai_history.append({
                    "role": turn["role"],
                    "content": turn["text"]
                })
            elif turn["role"] == "api":
                openai_history.append({
                    "role": "assistant",
                    "content": None,
                    "function_call": {
                        "name": turn["request"]["api_name"],
                        "arguments": json.dumps(turn["request"]["parameters"])
                    }
                })
                response_content = {
                    "response": turn["response"],
                    "exception": turn["exception"]
                }
                openai_history.append({
                    "role": "function",
                    "name": turn["request"]["api_name"],
                    "content": json.dumps(response_content)
                })

        # Prepare API call parameters
        api_params = {
            "model": self.model,
            "messages": openai_history,
            "functions": self.api_docs,
            "base_url": self.base_url,
            "api_key": self.api_key
        }
        
        # Add optional parameters if they are set
        if self.max_new_tokens is not None:
            api_params["max_tokens"] = self.max_new_tokens
        if self.temperature is not None:
            api_params["temperature"] = self.temperature
        if self.top_p is not None:
            api_params["top_p"] = self.top_p

        try:
            openai_response = openai_chat_completion(**api_params)
        except Exception as e:
            logger.error(f"Error making API request: {str(e)}")
            logger.error(f"Request details: {json.dumps(api_params, indent=2)}")
            raise

        openai_message = openai_response.choices[0].message
        
        # Store only essential information
        metadata = {
            "model": self.model,
            "messages": openai_history,
            "functions": self.api_docs
        }
        
        if hasattr(openai_message, "function_call") and openai_message.function_call:
            function_call = openai_message.function_call
            api_name = function_call.name
            try:
                parameters = json.loads(function_call.arguments)
            except json.decoder.JSONDecodeError:
                # check termination reason
                logger.info(f"Failed to decode arguments for {api_name}: {function_call.arguments}")
                parameters = None
            return {
                "role": "api",
                "request": {
                    "api_name": api_name,
                    "parameters": parameters
                },
                "metadata": metadata
            }
        else:
            return {
                "role": "assistant",
                "text": openai_message.content,
                "metadata": metadata
            }


class EvalModes(str, Enum):
    PREDICT = "predict"
    EVALUATE = "evaluate"
    VALIDATE = "validate"


def get_arg_parser():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dataset", type=str, help="Path to dataset for models to evaluate")
    parser.add_argument("--database", type=str, help="Path to database used in evaluation")
    parser.add_argument("--api_key", type=str, default="openai.key", help="Path to OpenAI API key")
    parser.add_argument("--api_mode", type=str, choices=["exact", "suite", "all"], default="all",
                        help="API mode to use for evaluation, determines which api docs to include")
    parser.add_argument("--model", type=str, default="gpt-4", help="Model to use for generation")
    parser.add_argument("--output_dir", type=str, help="Path to output model predictions")
    parser.add_argument("--reset", action="store_true", help="reset evaluation writing over any cached results")
    parser.add_argument("--disable_documentation", action="store_true",
                        help="disabled documentation sent to GPT-4 replacing with empty strings")
    parser.add_argument("--modes", choices=list(EvalModes), type=str, nargs='+', default=list(EvalModes),
                        help="Evaluation modes")
    parser.add_argument("--url", type=str, help="URL for the API endpoint")
    parser.add_argument("--max_new_tokens", type=int, help="Maximum number of tokens to generate")
    parser.add_argument("--temperature", type=float, help="Sampling temperature")
    parser.add_argument("--top_p", type=float, help="Nucleus sampling parameter")
    parser.add_argument("--first_n", type=int, help="Limit number of samples to process")

    return parser


def main(flags: List[str] = None):
    parser = get_arg_parser()
    args = parser.parse_args(flags)
    logger.info(f"Arguments: {args}")

    # get api key
    openai_key = os.environ.get("API_KEY", None)
    if openai_key is None:
        with open(args.api_key, "r") as f:
            openai_key = f.read().strip()
    
    # Configure OpenAI
    client = OpenAI(
        api_key=openai_key,
        base_url=args.url if args.url else None
    )
    
    # Log configuration (without exposing the full key)
    logger.info(f"Using API base URL: {client.base_url}")
    logger.info(f"API key type: {type(openai_key)}")
    logger.info(f"API key length: {len(openai_key) if openai_key else 0}")
    logger.info(f"API key prefix: {openai_key[:10]}..." if openai_key else "No API key")

    # Test the configuration
    try:
        # Make a simple test call to verify authentication
        test_response = client.chat.completions.create(
            model=args.model,
            messages=[{"role": "user", "content": "test"}],
            max_tokens=5
        )
        logger.info("Successfully authenticated with OpenAI API")
    except Exception as e:
        logger.error(f"Failed to authenticate with OpenAI API: {str(e)}")
        raise

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
            with open(output_file_path, 'r', encoding='utf-8') as reader:
                conversation_with_metrics = json.load(reader)
            total_metrics += conversation_with_metrics["metrics"]
            total_metrics["num_conversations"] += 1
            continue

        logger.info(f"Running {file_name}")
        with open(file_path, 'r', encoding='utf-8') as reader:
            conversation = json.load(reader)

        if EvalModes.PREDICT in args.modes:
            logger.info("Running prediction...")
            if args.api_mode == "exact":
                apis_used = [APIS_BY_NAME[api_name] for api_name in conversation["apis_used"]]
            elif args.api_mode == "suite":
                apis_used = [
                    api for suite_name in conversation["suites_used"] for api in SUITES_BY_NAME[suite_name].apis
                ]
            elif args.api_mode == "all":
                apis_used = ALL_APIS
            else:
                raise ValueError(f"Invalid api mode: {args.api_mode}")

            predictor_func = OpenAIPredictor(
                model=args.model,
                apis_used=apis_used,
                disable_docs=args.disable_documentation,
                base_url=args.url,
                api_key=openai_key,
                max_new_tokens=args.max_new_tokens,
                temperature=args.temperature,
                top_p=args.top_p
            )
            conversation = tool_executor.run_conversation(conversation, predictor_func)

        if EvalModes.EVALUATE in args.modes:
            logger.info("Running evaluation...")
            conversation = tool_executor.evaluate_predictions(conversation)
            logger.info(f"Conversation {file_name} pass: {conversation['metrics']['success']}")
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

        with open(output_file_path, 'w', encoding='utf-8') as writer:
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
