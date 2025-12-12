def get_metrics(total_metrics: dict):   
    return {
                "num_conversations": total_metrics["num_conversations"],
                "precision":  0 if not "predictions" in total_metrics else total_metrics["matches"] / total_metrics["predictions"],
                "recall":  0 if not "matches" in total_metrics else  total_metrics["matches"] / total_metrics["ground_truths"],
                "action_precision": 0 if not "actions" in  total_metrics else total_metrics["valid_actions"] / total_metrics["actions"],
                "bad_action_rate":  0 if not "bad_actions" in total_metrics else total_metrics["bad_actions"] / total_metrics["actions"],
                "success_rate": 0 if not "success" in total_metrics else total_metrics["success"] / total_metrics["num_conversations"]
            }