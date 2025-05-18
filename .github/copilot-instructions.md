# GitHub Copilot Instructions for the ACRIS Project

## 1. Project Overview

- **Project Name:** ACRIS (Architecture for a Risk Information System)
- **Goal:** To develop a robust and intelligent system that allows users to effectively query, retrieve, and receive recommendations for relevant risk cases. The system aims to improve access to critical risk information through advanced data processing, query understanding, and recommendation techniques.
- **Primary Documents:**
  - `ACRIS System Development Plan`: Outlines the phased development approach, modules, technologies, and best practices.
  - `blueprint.md`: Describes the high-level architecture, components, and data flows. **Please refer to these documents for context.**

## 2. Architecture Summary

The ACRIS system is now organized as a **monolithic modular Python package** under the `acris/` directory. The main modules are:

- `dp/`: Data Processing
- `upq/`: User & Project Query
- `qo/`: Question Organization
- `ro/`: Risk Output
- `ra/`: Risk Analysis
- `common/`: Shared utilities, config, and data models

The main entry point is `acris/main.py`.

**Key Data Stores:**

- "Risk Case Database": Stores processed risk information (likely text-heavy, suitable for search engines like Elasticsearch).
- "Users, Projects, Queries Database": Stores user accounts, project information, and query logs (relational or NoSQL).

## 3. Key Technologies

- **Backend Development:** Primarily **Python**. Frameworks like **Flask, Django, or FastAPI** are preferred.
- **Databases:**
  - **SQL:** PostgreSQL, MySQL (for structured data like UPQ).
  - **NoSQL:** **Elasticsearch** (highly preferred for DP's "Risk Case Database" due to text search capabilities), MongoDB.
- **Natural Language Processing (NLP):** **NLTK, spaCy**.
- **Machine Learning / Recommendation:** **scikit-learn, Surprise** (for collaborative filtering), TensorFlow, PyTorch (for more advanced models if needed).
- **Frontend (UI/UX Module):** React, Angular, or Vue.js.
- **API Design:** RESTful principles. Use tools like Swagger/OpenAPI for documentation.
- **Containerization & Orchestration:** Docker, Kubernetes.
- **Version Control:** Git (using Gitflow branching model where appropriate).
- **Testing Frameworks:** `pytest` for Python.

## 4. Coding Standards & Best Practices

- **Monolithic Modular Structure:** All code should reside within the `acris/` directory, organized by module as described above. Avoid creating separate microservices or external packages unless explicitly required by the architecture.
- **Modularity:** Design components with clear responsibilities and well-defined APIs for loose coupling between modules.
- **Readability & Maintainability:**
  - Write clear, concise, and well-commented code.
  - Use meaningful variable and function names.
  - **Python:** Strictly adhere to **PEP 8** style guidelines. Include **type hints** for all function signatures and complex variables.
- **Documentation:**
  - Provide comprehensive docstrings for all modules, classes, and functions (e.g., Google-style Python docstrings).
  - Keep API documentation (Swagger/OpenAPI) up-to-date.
- **Configuration Management:** Externalize all configurations (database credentials, API keys, file paths, model parameters). Do not hardcode sensitive information. Use environment variables or configuration files.
- **Testing:**
  - Write comprehensive **unit tests** for all new logic. Aim for high test coverage.
  - Develop **integration tests** for interactions between modules.
  - System tests should cover main user workflows.
- **Security:**
  - Always validate and sanitize user inputs.
  - Use parameterized queries or ORMs (like SQLAlchemy with Flask/Django) to prevent SQL injection.
  - Implement secure authentication and authorization mechanisms for UPQ.
  - Be mindful of dependencies and scan for vulnerabilities.
- **Error Handling:** Implement robust error handling using try-except blocks. Provide meaningful error messages and appropriate HTTP status codes for APIs.
- **Logging:** Implement comprehensive logging throughout the application for debugging, monitoring, and auditing purposes. Use standard Python logging module.
- **Scalability:** Design modules, especially DP, RO, and RA, with scalability in mind. Consider asynchronous operations for long-running tasks.

## 5. Specific Instructions for GitHub Copilot

- **Adherence to Standards:** When generating code, strictly follow the coding standards, technology choices, and best practices outlined above (especially PEP 8 and type hints for Python).
- **Contextual Awareness:** Refer to the `blueprint.md` for architectural context and the `ACRIS System Development Plan` for module-specific objectives and tasks.
- **API Endpoints:** When suggesting code for API endpoints, follow RESTful conventions. Include request validation, proper response structures, and HTTP status codes.
- **Database Interactions:**
  - For SQL databases, prefer ORM usage (e.g., SQLAlchemy) or ensure all raw SQL queries are parameterized.
  - For Elasticsearch, utilize the official Python client and construct queries using its DSL.
- **NLP Tasks:** Leverage NLTK or spaCy functions effectively for tasks like tokenization, stemming, lemmatization, NER, and accessing WordNet.
- **Comments & Docstrings:** Automatically generate or suggest detailed docstrings for functions and classes, and provide explanatory comments for complex logic.
- **Test Generation:** Assist in writing test cases using `pytest`. Suggest tests for different scenarios, including edge cases.
- **Boilerplate Code:** Help generate boilerplate code for new modules, classes, or API endpoints based on the project structure and conventions.
- **Efficiency & Performance:** Suggest efficient algorithms and data structures. Highlight potential performance bottlenecks.
- **Security Prompts:** If generating code that handles user input or sensitive data, proactively suggest security best practices (e.g., sanitization, encryption if applicable).
- **Risk Domain Specifics:**
  - The system deals with "Risk Cases." Query expansion involves a "Predefined Lexicon" (domain-specific) and "WordNet."
  - Recommendations should be tailored to risk assessment and information retrieval.
  - When processing "Risk Case Data," be mindful that it could be sensitive. While the primary goal is content-based retrieval, avoid suggesting operations that might unnecessarily expose raw sensitive details without proper context or controls.

By following these instructions, GitHub Copilot can be a more effective assistant in developing the ACRIS project, ensuring consistency, quality, and adherence to architectural and design principles.
