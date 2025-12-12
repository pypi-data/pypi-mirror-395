import json
import os

from nemo_evaluator.api.api_dataclasses import EvaluationResult


def convert_to_standard_output(results_dict):
    num_conversations = results_dict.pop("num_conversations")

    metrics_dict = {}
    for k, v in  results_dict.items():
        metrics_dict[k] = {
            "scores": {
                k: {
                    'value': v,
                    'stats': {
                        'count': num_conversations,
                    },
                }
            }
        }

    standard_output = {
        'tasks': {
            'tooltalk': {
                'metrics': metrics_dict
            }
        },
    }

    return standard_output

def parse_output(output_dir: str) -> EvaluationResult:
    with open(os.path.join(output_dir, "metrics.json"), "r") as f:
        results_dict = json.load(f)

    converted_dict = convert_to_standard_output(results_dict)
    parsed_outputs = EvaluationResult(**converted_dict)

    return parsed_outputs
