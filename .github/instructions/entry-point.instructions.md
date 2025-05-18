---
applyTo: "acris/main.py"
---

Coding standards, domain knowledge, and preferences that AI should follow.

In the ACRIS project, you should use **main.py** as your main entry point, not a top-level **main.py**.

> ### Why?
>
> - **Monolithic Modular Structure:** All code—including the main entry point—must reside within the acris directory, as per your coding standards.
> - **Project Organization:** Placing main.py inside acris keeps the codebase modular, organized, and consistent with Python package conventions.
> - **Imports & Namespacing:** This structure allows for clean relative imports between modules (e.g., `from acris.dp import ...`), and avoids import errors or namespace pollution.
>
> ### Example Structure
>
> ```
> acris/
>   __init__.py
>   main.py        # ← Main entry point
>   dp/
>   upq/
>   qo/
>   ro/
>   ra/
>   common/
> ```
>
> ### Usage
>
> To run the application:
>
> ```sh
> python -m acris.main
> ```
>
> or, if using a script:
>
> ```sh
> uv run acris/main.py
> ```
>
> **Do not** create or use a top-level main.py outside the acris directory. Always use main.py for entry-point logic.
