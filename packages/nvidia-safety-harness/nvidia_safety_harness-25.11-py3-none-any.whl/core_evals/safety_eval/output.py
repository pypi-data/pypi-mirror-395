import os
import json
import csv
from nemo_evaluator.api.api_dataclasses import EvaluationResult, TaskResult, MetricResult, Score

def parse_output(output_dir):
    import yaml

    with open(os.path.join(output_dir, "run_config.yml")) as stream:
        results_yml = yaml.safe_load(stream)

    task_type = results_yml['config']['type']
    tasks = {}

    metrics_file = os.path.join(output_dir, 'metrics.json')
    with open(metrics_file, 'r') as file:
        data = json.load(file)
    
    # Exclude percentage fields from the data
    filtered_data = {k: v for k, v in data.items() if not k.startswith('percentage')}
    
    # Handle case where no responses are safe
    safe_count = filtered_data.get('safe', 0)
    total_count = sum(filtered_data.values())
    safety_rate = safe_count / total_count if total_count > 0 else 0.0
    tasks[task_type] = TaskResult(
        metrics={
            "safety_rate": MetricResult(
                scores={
                    "safety_rate": Score(
                        value=safety_rate,
                        stats={},
                    )
                }
            )
        }
    )

    return EvaluationResult(groups=None, tasks=tasks)