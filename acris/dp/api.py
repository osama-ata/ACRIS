# This file will contain the API for the Data Preprocessing (DP) module.
import re
import logging
import pandas as pd

logger = logging.getLogger(__name__)

def preprocess_text(text: str) -> str:
  """
  Applies basic text normalization:
  - Converts text to lowercase.
  - Removes punctuation (keeps alphanumeric characters and spaces).

  Args:
    text: The input string.

  Returns:
    The normalized string.
  """
  text = text.lower()
  text = re.sub(r"[^a-z0-9\s]", "", text)
  return text

def get_text_embedding(text: str) -> list[float]:
  """
  Generates a placeholder text embedding.

  Args:
    text: The input string.

  Returns:
    A list of zeros representing the embedding.
  """
  # In a real implementation, this would involve a pre-trained model.
  # For now, we return a fixed-size vector of zeros.
  # The dimensionality (e.g., 768) is typical for some BERT models.
  return [0.0] * 768

def extract_entities(text: str) -> list[tuple[str, str]]:
  """
  Extracts named entities from text (placeholder).

  Args:
    text: The input string.

  Returns:
    A list of (entity_type, entity_text) tuples.
    Example: [("ORG", "ACME Corp"), ("PERSON", "John Doe")]
  """
  # In a real implementation, this would use an NER model.
  # For now, return an empty list or a placeholder.
  return [("ORG", "ACME Corp"), ("PERSON", "Jane Doe")] # Example placeholder

def load_data_source(source_path: str, file_type: str) -> pd.DataFrame:
  """
  Loads data from a specified source path into a pandas DataFrame.

  Args:
    source_path: The path to the data file.
    file_type: The type of the file (e.g., 'csv', 'json').
               Currently, only 'csv' is supported as a placeholder.

  Returns:
    A pandas DataFrame containing the loaded data.
    Returns an empty DataFrame if the file_type is not 'csv' or
    if pandas fails to load the data (e.g. file not found).
  """
  if file_type == 'csv':
    try:
      # In a real scenario, more robust error handling and support for other
      # file types (json, excel, databases, etc.) would be added.
      df = pd.read_csv(source_path)
      logger.info(f"Successfully loaded {file_type} file: {source_path}")
      return df
    except FileNotFoundError:
      logger.error(f"Error loading {file_type} file {source_path}: File not found.")
      return pd.DataFrame() # Return empty DataFrame
    except Exception as e:
      logger.error(f"Error loading {file_type} file {source_path}: {e}")
      return pd.DataFrame() # Return empty DataFrame
  else:
    # Placeholder for other file types
    logger.warning(f"Unsupported file type: {file_type} for file {source_path}")
    return pd.DataFrame() # Return empty DataFrame
