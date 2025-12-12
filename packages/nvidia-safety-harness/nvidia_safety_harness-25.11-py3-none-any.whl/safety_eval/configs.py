from dataclasses import dataclass
from typing import Optional, ClassVar


@dataclass
class ModelConfig:
    base_url: str
    llm_name: str
    type: str
    inference_params: ClassVar[dict] = {
        "max_tokens": 1000,
        "concurrency": 1,
        "retries": 1
    }
    api_key: Optional[str] = None


@dataclass
class LlamaNemoguardConfig:
    base_url: str
    llm_name: str = "llama-3.1-nemoguard-8b-content-safety"
    inference_params: ClassVar[dict] = {
        "max_tokens": 200,
        "concurrency": 1,
        "retries": 1
    }
    api_key: Optional[str] = None

    
@dataclass
class WildguardConfig:
    base_url: str
    llm_name: str = "allenai/wildguard"
    inference_params: ClassVar[dict] = {
        "max_tokens": 100,
        "concurrency": 1,
        "retries": 1
    }
    api_key: Optional[str] = None
