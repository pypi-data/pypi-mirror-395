from typing import List, Optional
from pydantic import BaseModel, Field, ValidationError
import requests
from concurrent.futures import ThreadPoolExecutor
import logging

logger = logging.getLogger(__name__)


class RawDataRecord(BaseModel):
    prompt: str
    response: str
    modelname: str
    usecase_name: str
    usecase_group: Optional[str] = Field(default="default")
    response_time: Optional[float] = None
    inference_error: Optional[str] = None
    is_from_optune_model: bool = False
    logprobs: Optional[List[float]] = None
    raw_logits: Optional[List[float]] = None
    
    def to_dict(self):
        return self.model_dump()

    @classmethod
    def from_dict(cls, data: dict):
        try:
            # Parse the data using pydantic's parsing and validation
            return cls(**data)
        except ValidationError as e:
            raise ValueError(f"Error creating DataRecords from dict: {e}")



class Tracing:
    """Handles background data collection."""

    def __init__(self, base_url: str):
        self.base_url = base_url
        self.executor = ThreadPoolExecutor(
            max_workers=1, thread_name_prefix="optune_tracing"
        )

    def _send_data(self, data: RawDataRecord) -> bool:
        """Send collected data to Optune."""
        try:
            logger.info("Starting data collection...")
            response = requests.post(
                f"{self.base_url}/public/api/collect_raw_data",
                json=data.to_dict(),
                timeout=10,
            )
            response.raise_for_status()
            logger.info("Data collection completed successfully")
            return True
        except Exception as e:
            logger.exception(f"Error collecting data: {str(e)}")
            return False

    def collect(
        self,
        modelname: str,
        prompt: str,
        response: str,
        usecase_name: str,
        usecase_group: str,
        response_time: float = 0,
        is_from_optune_model: bool = False,
        inference_error: Optional[str] = None,
        logprobs: Optional[List[float]] = None,
        raw_logits: Optional[List[float]] = None,
    ) -> None:
        """Queue data collection in background."""

        data = RawDataRecord(
            modelname=modelname,
            prompt=prompt,
            response=response,
            usecase_name=usecase_name,
            usecase_group=usecase_group,
            response_time=response_time,
            is_from_optune_model=is_from_optune_model,
            inference_error=inference_error,
            logprobs=logprobs,
            raw_logits=raw_logits,
        )
        self.executor.submit(self._send_data, data)

    def shutdown(self):
        """Shutdown the executor."""
        self.executor.shutdown(wait=False)
        