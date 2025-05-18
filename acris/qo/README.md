# Query Operation Module

The Query Operation (QO) Module is a core component of the Automated Construction Risk Identification System (ACRIS). It is responsible for processing user queries and enabling effective retrieval of relevant risk cases from the system.

## Overview

The original QO module, as described in "ACRIS - REV02.01.pdf," processed user queries using a Sequence of Actions (SoA) similar to risk case preprocessing:

- Tokenization
- Lowercasing
- Lemmatization
- Stop word removal

A key feature was **query expansion**:

- Terms in the query are matched to a pre-defined risk-related lexicon.
- Unmatched terms are expanded using synonyms from WordNet.
- Terms not present in the risk case database are removed from both the original and expanded queries.

This approach aimed to address semantic similarity by including related terms, but had limitations in capturing deeper contextual meaning.

## Modernization and Enhancements

Recent advancements propose a shift to more sophisticated NLP techniques:

- **Transformer-based Query and Document Embeddings:**
  - Encode entire user queries and risk case documents into dense semantic vectors using pre-trained transformer models (e.g., BERT, RoBERTa, ELECTRA).
  - Compute similarity directly between these embeddings, enabling more nuanced semantic matching than keyword or lexicon-based methods.

- **Query Rewriting and Intent Recognition:**
  - Incorporate query rewriting based on historical query patterns and intent recognition to better understand user needs.
  - Reformulate queries for more effective retrieval (e.g., mapping "falls" to "falling from height").

These enhancements address challenges in semantic similarity and user intent, leading to more accurate and relevant risk information retrieval.

## Key Technologies

- **NLP Libraries:** spaCy, NLTK, HuggingFace Transformers
- **Deep Learning:** TensorFlow, PyTorch
- **Lexicon & WordNet:** For legacy and hybrid query expansion

## Directory Structure

- `expansion/` – Query expansion and synonym handling
- `embedding/` – Query/document embedding and similarity
- `intent/` – Intent recognition and query rewriting
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

- See `Docs/modules/query.md` for detailed design and rationale.
- Refer to the ACRIS System Development Plan and blueprint.md for architectural context.
