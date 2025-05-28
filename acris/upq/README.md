# User & Project Query (UPQ) Module

The UPQ module manages user accounts, project information, and query logs within the ACRIS system. It supports authentication, authorization, and user/project-specific query management.

## Responsibilities

- User account management (registration, authentication, roles)
- Project creation and management
- Query logging and history
- Secure access control and permissions

## Key Technologies

- SQL/NoSQL databases (e.g., PostgreSQL, MongoDB)
- ORMs (e.g., SQLAlchemy)
- Security best practices (input validation, password hashing)

## Best Practices

- Follow PEP 8 and use type hints
- Write comprehensive docstrings and comments
- Use ruff for linting and formatting
- Write unit and integration tests with pytest

## References

- See `Docs/modules/users.md` and the ACRIS System Development Plan for details.

## API Contract

The `acris.upq` module exposes the following data classes and functions:

### Data Classes

#### 1. `User`
- **Purpose:** Represents a user in the system.
- **Attributes:**
    - `**user_id** \`(str)\`: The unique identifier for the user.
    - `**username** \`(str)\`: The username of the user.
    - `**roles** \`(List[str])\`: A list of roles assigned to the user (e.g., "admin", "editor").

#### 2. `Project`
- **Purpose:** Represents a project created by a user.
- **Attributes:**
    - `**project_id** \`(str)\`: The unique identifier for the project.
    - `**project_name** \`(str)\`: The name of the project.
    - `**user_id** \`(str)\`: The ID of the user who owns the project.
    - `**description** \`(str)\`: A brief description of the project.

### Functions

#### 1. `get_user(user_id: str) -> Optional[User]`
- **Description:** Retrieves a user by their ID.
- **Parameters:**
    - `**user_id** \`(str)\`: The ID of the user to retrieve.
- **Returns:**
    - `\`(Optional[User])\`: The `User` object if found, otherwise `None`.

#### 2. `create_user(username: str, password: str) -> User`
- **Description:** Creates a new user and stores them (placeholder implementation). In a real system, the password would be hashed.
- **Parameters:**
    - `**username** \`(str)\`: The desired username for the new user.
    - `**password** \`(str)\`: The user's password.
- **Returns:**
    - `\`(User)\`: The created `User` object.

#### 3. `get_project(project_id: str) -> Optional[Project]`
- **Description:** Retrieves a project by its ID.
- **Parameters:**
    - `**project_id** \`(str)\`: The ID of the project to retrieve.
- **Returns:**
    - `\`(Optional[Project])\`: The `Project` object if found, otherwise `None`.

#### 4. `create_project(project_name: str, user_id: str, description: str) -> Project`
- **Description:** Creates a new project (placeholder implementation).
- **Parameters:**
    - `**project_name** \`(str)\`: The name of the new project.
    - `**user_id** \`(str)\`: The ID of the user creating the project.
    - `**description** \`(str)\`: A description for the project.
- **Returns:**
    - `\`(Project)\`: The created `Project` object.

#### 5. `log_query(user_id: str, project_id: str, query_text: str, results: List[str]) -> bool`
- **Description:** Logs a user's query and the results they received (placeholder implementation).
- **Parameters:**
    - `**user_id** \`(str)\`: The ID of the user who made the query.
    - `**project_id** \`(str)\`: The ID of the project context for the query.
    - `**query_text** \`(str)\`: The actual query text.
    - `**results** \`(List[str])\`: A list of identifiers or summaries of the results received.
- **Returns:**
    - `\`(bool)\`: `True` if the query was logged successfully (placeholder always returns `True`), `False` otherwise.
