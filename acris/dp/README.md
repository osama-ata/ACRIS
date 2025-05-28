# Data Preprocessing Module

The Data Preprocessing Module is a fundamental component of the Automated Construction Risk Identification System (ACRIS). It is responsible for transforming raw textual risk case data and user queries into structured, semantically rich representations suitable for downstream retrieval, analysis, and recommendation tasks.

## Overview

The initial version of the module, as described in "ACRIS - REV02.01.pdf," employed a Sequence of Actions (SoA) including:

- Tokenization
- Lowercasing
- Lemmatization
- Stop word removal

These steps normalize text for basic matching and similarity calculations.

## Modernization and Enhancements

Recent research and system enhancements propose the following state-of-the-art techniques:

- **Contextualized Word Embeddings:**
  - Leverage transformer models (e.g., BERT, RoBERTa, ELECTRA) to generate embeddings that capture word meaning in context, improving semantic similarity assessments.
- **Advanced Tokenization:**
  - Adopt subword tokenization (e.g., Byte-Pair Encoding) to handle out-of-vocabulary words and morphological variations, increasing robustness to new or rare terms.
- **Named Entity Recognition (NER) & Relationship Extraction:**
  - Integrate NER to identify key entities (e.g., project types, equipment, causes of accidents) and relationship extraction to understand connections between entities, enabling richer, more structured representations of risk cases.

These advancements address challenges in semantic similarity, efficient retrieval, and precise risk identification by providing a more nuanced, context-aware understanding of textual data.

## Key Technologies

- **NLP Libraries:** spaCy, NLTK
- **Deep Learning:** HuggingFace Transformers, TensorFlow, PyTorch
- **Data Storage:** Elasticsearch (for processed risk cases), SQL/NoSQL (for metadata)

## Directory Structure

- `cleaning/` – Basic text normalization utilities
- `ingestion/` – Data loading and ingestion scripts
- `processing/` – Advanced NLP, embedding, NER, and relationship extraction
- `data/` – Raw and processed data storage
- `utils/` – Shared utilities
- `tests/` – Unit and integration tests
- `config/` – Configuration files and parameters

## Best Practices

- Follow PEP 8 and use type hints
- Write comprehensive docstrings and comments
- Externalize all configuration and sensitive data
- Use ruff for linting and formatting
- Write unit and integration tests with pytest

## References

- See `Docs/modules/data-process.md` for detailed design and rationale.
- Refer to the ACRIS System Development Plan and blueprint.md for architectural context.

## API Contract

The `acris.dp` module exposes the following functions for data preprocessing:

### Functions

#### 1. `preprocess_text(text: str) -> str`

- **Description:** Applies basic text normalization to the input string. This includes converting the text to lowercase and removing punctuation, keeping only alphanumeric characters and spaces.
- **Parameters:**
    - `**text** \`(str)\`: The input string to preprocess.
- **Returns:**
    - `\`(str)\`: The normalized string.

#### 2. `get_text_embedding(text: str) -> List[float]`

- **Description:** Generates a placeholder text embedding for the input string. In a real implementation, this would involve a pre-trained model. For now, it returns a fixed-size vector of zeros (768 dimensions, typical for some BERT models).
- **Parameters:**
    - `**text** \`(str)\`: The input string for which to generate the embedding.
- **Returns:**
    - `\`(List[float])\`: A list of floating-point numbers representing the text embedding.

#### 3. `extract_entities(text: str) -> List[Tuple[str, str]]`

- **Description:** Extracts named entities from the input text. This is a placeholder implementation and currently returns a fixed list of example entities: `[("ORG", "ACME Corp"), ("PERSON", "Jane Doe")]`. A real implementation would use a Named Entity Recognition (NER) model.
- **Parameters:**
    - `**text** \`(str)\`: The input string from which to extract entities.
- **Returns:**
    - `\`(List[Tuple[str, str]])\`: A list of tuples, where each tuple contains the entity type (e.g., "ORG", "PERSON") and the extracted entity text.

#### 4. `load_data_source(source_path: str, file_type: str) -> pandas.DataFrame`

- **Description:** Loads data from a specified source path into a pandas DataFrame. Currently, it only supports 'csv' files as a placeholder. If the `file_type` is not 'csv', or if the file is not found or another error occurs during loading, it prints an error message and returns an empty DataFrame.
- **Parameters:**
    - `**source_path** \`(str)\`: The path to the data file.
    - `**file_type** \`(str)\`: The type of the file (e.g., 'csv', 'json').
- **Returns:**
    - `\`(pandas.DataFrame)\`: A pandas DataFrame containing the loaded data. Returns an empty DataFrame on failure or if the file type is unsupported.
