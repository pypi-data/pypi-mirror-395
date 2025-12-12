from pydantic import BaseModel
from uuid import UUID
from datetime import datetime
from typing import Optional, Union
import requests
import base64
import logging


class BoundingBox(BaseModel):
    x0: Union[int, float]
    y0: Union[int, float]
    x1: Union[int, float]
    y1: Union[int, float]


class VisualComponent(BaseModel):
    id: UUID
    type: str
    document_id: UUID
    page_number: int
    label: str
    bbox: BoundingBox
    description: str
    content: Optional[str] = None
    created_at: datetime
    updated_at: datetime
    mask_url: Optional[str] = None
    metadata: Optional[dict] = None

    @property
    def mask(self) -> Optional[str]:
        """
        Fetch the mask image from S3 URL and return as a base64 encoded string.

        Returns:
            Optional[str]: Base64 encoded image string if mask_url exists and image is successfully loaded,
                          None otherwise.
        """
        if not self.mask_url:
            return None

        try:
            # Download the image from S3 URL
            response = requests.get(self.mask_url)
            response.raise_for_status()

            # Encode the image bytes as base64
            base64_string = base64.b64encode(response.content).decode("utf-8")

            return base64_string

        except Exception as e:
            # Log the error in a real application
            logging.error(f"Error loading mask from {self.mask_url}: {e}")
            return None


class DocumentComponent(BaseModel):
    id: UUID
    type: str
    document_id: UUID
    page_number: int
    label: str
    text: Optional[str] = None
    bbox: BoundingBox
    metadata: Optional[dict] = None
