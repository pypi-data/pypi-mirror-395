from typing import Tuple

import pandas as pd
from langchain_core.runnables.config import RunnableConfig
from langchain_openai import OpenAI
from langchain_openai.chat_models.base import BaseChatOpenAI

from safety_eval.callbacks import BatchCallback
from safety_eval.configs import ModelConfig
from rich.console import Console


console = Console()

def split_flow_control_params(inference_params: dict)-> Tuple[dict, dict]:
    control_flow = ["concurrency", "retries"]
    control_flow_params: dict = {key: inference_params[key] for key in control_flow if key in inference_params}
    pure_inference_params = {key: inference_params[key] for key in inference_params if key not in control_flow}
    return control_flow_params, pure_inference_params


def run_inference(
        model_config: ModelConfig, 
        dataset_content: pd.DataFrame,
        output_file: str
    ) -> None:
    """Performs inference on the candidate model

    Args:
        batch_size: The batch size for inference
        model_config_file: The Eval Tool model config file
        dataset_name: The name of the dataset. This is used to identify the column containing 
        the text
        dataset_content: The Pandas dataframe
        inference_params: The inference params passed to `model.generate_text`
        output_file: The name of the output file
    """
    control_flow_params, inference_params = split_flow_control_params(model_config.inference_params)
    if model_config.type == "completions":
        Client = OpenAI
    elif model_config.type == "chat":
        Client = BaseChatOpenAI
    else:
        raise ValueError(f"Unrecognised model type {model_config.type}.")
    candidate_model = Client(base_url=model_config.base_url, api_key=model_config.api_key, model=model_config.llm_name, **inference_params)

    console.print(f"[bold red]Using inference params: {model_config.inference_params}\n")
    console.print(f"[bold red]Using model endpoint: {model_config.base_url}\n")

    data = dataset_content["prompt"].to_list()
    with BatchCallback(total=len(data), description="Running MUT inference") as cb:
        output = candidate_model.with_retry(stop_after_attempt=control_flow_params['retries']).batch(data, config=RunnableConfig(max_concurrency=control_flow_params['concurrency'], callbacks=[cb]))
        if isinstance(candidate_model, BaseChatOpenAI):
            output = [example.content for example in output]

    console.print("Model output generated", style="#0000d7")
    dataset_content['model_output'] = output
    dataset_content.to_csv(output_file, index=False)
