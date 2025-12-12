import argparse
import logging
import os

from safety_eval.aegis_v2.handler import handle_aegis_v2
from safety_eval.configs import LlamaNemoguardConfig, ModelConfig, WildguardConfig
from safety_eval.wildguard.handler import handle_wildguard

logger = logging.getLogger(__name__)
logging.basicConfig(
    format="%(asctime)s %(levelname)-8s %(message)s",
    level=logging.INFO,
)
logger.setLevel(logging.INFO)
import http.client as http_client
http_client.HTTPConnection.debuglevel = 0
import logging

# Only show warnings
logging.getLogger("urllib3").setLevel(logging.WARNING)

# Disable all child loggers of urllib3, e.g. urllib3.connectionpool
logging.getLogger("urllib3").propagate = False
import logging

logging.getLogger("requests").setLevel(logging.WARNING)
import urllib3
urllib3.disable_warnings()
class MisconfigurationError(Exception):
    pass

def comma_separated_to_dict(str_list: str, field_name: str) -> dict:
    if not str_list:
        return {}
    arg_list = str_list.split(",")
    arg_dict = {}
    for arg in arg_list:
        try:
            key, value = arg.split("=")
            try:
                value=int(value)
            except ValueError:
                try:
                    value=float(value)
                except:
                    pass
            arg_dict[key] = value
        except ValueError:
            raise MisconfigurationError(f"Incorrect parameters formatting for {field_name}")
    return arg_dict

def check_judge_inference_params(inference_params: dict):
    control_flow_params = ["concurrency", "retries"]
    if not set(inference_params.keys()).issubset(set(control_flow_params)):
        raise MisconfigurationError(f"For Judge model, only {control_flow_params} are allowed")

def build_arg_parser():
    parser = argparse.ArgumentParser(
        description="Run inference on LLama Guard finetuned models"
    )
    parser.add_argument(
        "--eval",
        choices=['aegis_v2',  'wildguard'],
        type=str,
        help="Evaluation to run",
        required=True,
    )

    parser.add_argument(
        "--model-url",
        type=str,
        help="Url to the model under test.",
        required=True,
    )


    parser.add_argument(
        "--model-name",
        type=str,
        help="Model name, as deployed.",
        required=True,
    )

    parser.add_argument(
        "--judge-model-name",
        type=str,
        help="Judge model name if it was deployed with a different name than default. Defaults are: llama-3.1-nemoguard-8b-content-safety for aegis_v2,  allenai/wildguard for wildguard",
        required=False,
    )

    parser.add_argument(
        "--model-type",
        type=str,
        help="Indicate if this is completions, or insturction-tuned model.",
        choices=['completions', 'chat'],
        required=True,
    )

    parser.add_argument(
        "--judge-url",
        type=str,
        help="Url to the judge.",
        required=True,
    )

    parser.add_argument(
        "--mut-inference-params",
        type=str,
        help="""Comma-separated inference parameters for Model Under Test endpoint. E.g \"temperature=0,top_p=0.6\". " \
                These parameters are passed directly to OpenAI client. You can also provide additional parameters: 
                concurrency and retires which control behaviour but are not passed as a part of a payload""",
        default="",
        required=False
    )

    parser.add_argument(
        "--judge-inference-params",
        type=str,
        help="""Comma-separated inference parameters for judge endpoint. You can ONLY provide additional parameters: 
                concurrency and retires which control behaviour but are not passed as a part of a payload. 
                The rest of inference params are set and should not be changed.""",
        default="",
        required=False
    )

    parser.add_argument(
        "--limit",
        "-l",
        type=int,
        default=0,
        help="Limit the number of prompts to evaluate",
        required=False,
    )
    parser.add_argument(
        "--results-dir", "-o", type=str, help="Results directory", required=True
    )
    parser.add_argument(
        "--evaluate-reasoning-traces", action='store_true'
    )

    parser.add_argument(
        "--dataset",
        type=str,
        default="",
        help="Dataset path or identifier",
        required=False,
    )

    return parser


def evaluate():
    logger.info("Started safety harness")
    parser = build_arg_parser()
    args = parser.parse_args()
    args.mut_inference_params = comma_separated_to_dict(args.mut_inference_params, "mut_inference_params")
    args.judge_inference_params = comma_separated_to_dict(args.judge_inference_params, "judge_inference_params")
    logger.info(f"Read MUT inference params from CLI: {args.mut_inference_params}")
    logger.info(f"Read Judge inference params from CLI: {args.judge_inference_params}")

    model_api_key = os.environ.get('API_KEY')
    if not model_api_key:
        logger.warning("Model api key \"API_KEY\" was empty. Changing to \"null\". If your model is not gated with API KEY, ignore this warning.")
        model_api_key = "null"


    judge_model_key = os.environ.get('JUDGE_API_KEY')
    if not judge_model_key:
        logger.warning("Judge model api key \"JUDGE_API_KEY\" was empty. Changing to \"null\". If your judge model is not gated with API KEY, ignore this warning.")
        judge_model_key = "null"
    
    # for OpenAI client, we need to have base URL
    model_url = args.model_url.rstrip("/chat/completions").rstrip("/completions")
    judge_url = args.judge_url.rstrip("/chat/completions").rstrip("/completions")

    os.makedirs(args.results_dir, exist_ok=True)
    output_file = f"{args.results_dir}/output.csv"
    
    model_config=ModelConfig(base_url=model_url, llm_name=args.model_name, type=args.model_type, api_key=model_api_key)
    model_config.inference_params.update(args.mut_inference_params)

    # TODO: make health-checks

    if args.eval.startswith("aegis_v2"):
        # load default inference configuration and update with CLI arguments
        judge_config=LlamaNemoguardConfig(base_url=judge_url, api_key=judge_model_key)
        lang = None
        judge_config.inference_params.update(args.judge_inference_params)
        if args.judge_model_name:
            judge_config.llm_name = args.judge_model_name
        handle_aegis_v2(model_config, judge_config, args.dataset, output_file, limit=args.limit, evaluate_reasoning_traces=args.evaluate_reasoning_traces)
    elif args.eval == "wildguard":
        judge_config=WildguardConfig(base_url=judge_url, api_key=judge_model_key)
        judge_config.inference_params.update(args.judge_inference_params)
        if args.judge_model_name:
            judge_config.llm_name = args.judge_model_name
        handle_wildguard(model_config, judge_config, args.results_dir, limit=args.limit)
    else:
        raise Exception("Unrecognized evaluation.")


if __name__ == "__main__":
    evaluate()