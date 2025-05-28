# Expose the public API of the acris.dp module
from .api import preprocess_text
from .api import get_text_embedding
from .api import extract_entities
from .api import load_data_source

__all__ = [
    "preprocess_text",
    "get_text_embedding",
    "extract_entities",
    "load_data_source",
]
