from typing import Any, Optional
from uuid import UUID
from tqdm.auto import tqdm


from langchain_core.callbacks import BaseCallbackHandler

class BatchCallback(BaseCallbackHandler):
	def __init__(self, total: int, description: Optional[str] = None):
		super().__init__()
		self.count = 0
		self.progress_bar = tqdm(total=total)
		if description:
			self.progress_bar.set_description(description)

	def on_llm_end(self, response, *, run_id: UUID, parent_run_id: UUID | None = None, **kwargs: Any) -> Any:
		self.count += 1
		self.progress_bar.update(1)

	def __enter__(self):
		self.progress_bar.__enter__()
		return self
	
	def __exit__(self, exc_type, exc_value, exc_traceback):
		self.progress_bar.__exit__(exc_type, exc_value, exc_traceback)

	def __del__(self):
		self.progress_bar.__del__()
