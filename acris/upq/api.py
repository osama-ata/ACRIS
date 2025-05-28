# This file will contain the API for the User & Project Query (UPQ) module.
from dataclasses import dataclass
from typing import Optional, List

# Placeholder for actual data storage or ORM integration
_users_db = {}
_projects_db = {}
_query_log = []

@dataclass
class User:
    """
    Represents a user in the system.

    Attributes:
        user_id: The unique identifier for the user.
        username: The username of the user.
        roles: A list of roles assigned to the user (e.g., "admin", "editor").
    """
    user_id: str
    username: str
    roles: List[str]

@dataclass
class Project:
    """
    Represents a project created by a user.

    Attributes:
        project_id: The unique identifier for the project.
        project_name: The name of the project.
        user_id: The ID of the user who owns the project.
        description: A brief description of the project.
    """
    project_id: str
    project_name: str
    user_id: str
    description: str

def get_user(user_id: str) -> Optional[User]:
    """
    Retrieves a user by their ID.

    Args:
        user_id: The ID of the user to retrieve.

    Returns:
        The User object if found, otherwise None.
    """
    return _users_db.get(user_id)

def create_user(username: str, password: str) -> User:
    """
    Creates a new user and stores them (placeholder).

    Args:
        username: The desired username for the new user.
        password: The user's password (in a real system, this would be hashed).

    Returns:
        The created User object.
    """
    # In a real system, generate a unique ID and hash the password.
    import uuid
    new_user_id = str(uuid.uuid4())
    # For simplicity, roles are not assigned by default here.
    user = User(user_id=new_user_id, username=username, roles=["user"])
    _users_db[new_user_id] = user
    print(f"User '{username}' created with ID '{new_user_id}'. Password handling is a placeholder.")
    return user

def get_project(project_id: str) -> Optional[Project]:
    """
    Retrieves a project by its ID.

    Args:
        project_id: The ID of the project to retrieve.

    Returns:
        The Project object if found, otherwise None.
    """
    return _projects_db.get(project_id)

def create_project(project_name: str, user_id: str, description: str) -> Project:
    """
    Creates a new project (placeholder).

    Args:
        project_name: The name of the new project.
        user_id: The ID of the user creating the project.
        description: A description for the project.

    Returns:
        The created Project object.
    """
    import uuid
    new_project_id = str(uuid.uuid4())
    project = Project(
        project_id=new_project_id,
        project_name=project_name,
        user_id=user_id,
        description=description
    )
    _projects_db[new_project_id] = project
    # Associate project with user (simplified)
    # In a real DB, this might be a foreign key relationship.
    print(f"Project '{project_name}' created with ID '{new_project_id}' for user '{user_id}'.")
    return project

def log_query(user_id: str, project_id: str, query_text: str, results: List[str]) -> bool:
    """
    Logs a user's query and the results they received (placeholder).

    Args:
        user_id: The ID of the user who made the query.
        project_id: The ID of the project context for the query.
        query_text: The actual query text.
        results: A list of identifiers or summaries of the results received.

    Returns:
        True if the query was logged successfully, False otherwise (placeholder always returns True).
    """
    import datetime
    log_entry = {
        "timestamp": datetime.datetime.now().isoformat(),
        "user_id": user_id,
        "project_id": project_id,
        "query_text": query_text,
        "results": results
    }
    _query_log.append(log_entry)
    print(f"Query logged for user '{user_id}' in project '{project_id}'.")
    return True
