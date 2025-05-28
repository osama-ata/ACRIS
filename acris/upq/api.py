# This file will contain the API for the User & Project Query (UPQ) module.
# It also defines data classes intended to be mapped to database tables using an ORM like SQLAlchemy.
# This version implements basic SQLite database interaction.
from dataclasses import dataclass, field
from typing import Optional, List, Dict, Any # Added Dict, Any
import logging
import uuid
import datetime
import sqlite3 # Added for SQLite
import json # Added for JSON serialization of results_preview

logger = logging.getLogger(__name__)

DB_FILE = "acris_upq.db"

def _get_db_connection() -> sqlite3.Connection:
    """Establishes and returns a connection to the SQLite database."""
    conn = sqlite3.connect(DB_FILE)
    conn.row_factory = sqlite3.Row # Access columns by name
    return conn

def init_db():
    """Initializes the database and creates tables if they don't exist."""
    with _get_db_connection() as conn:
        cursor = conn.cursor()

        # Users table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS users (
            user_id TEXT PRIMARY KEY,
            username TEXT UNIQUE NOT NULL,
            email TEXT UNIQUE NOT NULL,
            hashed_password TEXT NOT NULL,
            created_at TIMESTAMP NOT NULL,
            updated_at TIMESTAMP NOT NULL
        )
        """)

        # Projects table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS projects (
            project_id TEXT PRIMARY KEY,
            project_name TEXT NOT NULL,
            user_id TEXT NOT NULL,
            description TEXT,
            created_at TIMESTAMP NOT NULL,
            updated_at TIMESTAMP NOT NULL,
            FOREIGN KEY (user_id) REFERENCES users (user_id)
        )
        """)

        # Query Logs table
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS query_logs (
            log_id TEXT PRIMARY KEY,
            user_id TEXT NOT NULL,
            project_id TEXT NOT NULL,
            query_text TEXT NOT NULL,
            timestamp TIMESTAMP NOT NULL,
            results_preview TEXT,
            FOREIGN KEY (user_id) REFERENCES users (user_id),
            FOREIGN KEY (project_id) REFERENCES projects (project_id)
        )
        """)
        conn.commit()
    logger.info(f"Database initialized: {DB_FILE}")

@dataclass
class User:
    """
    Represents a user in the system.
    Maps to the 'users' database table.
    """
    user_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    username: str
    email: str
    hashed_password: str
    roles: List[str] = field(default_factory=lambda: ["user"]) # Not persisted in SQLite for this iteration
    created_at: datetime.datetime = field(default_factory=datetime.datetime.now)
    updated_at: datetime.datetime = field(default_factory=datetime.datetime.now)

@dataclass
class Project:
    """
    Represents a project created by a user.
    Maps to the 'projects' database table.
    """
    project_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    project_name: str
    user_id: str # Foreign Key
    description: str
    created_at: datetime.datetime = field(default_factory=datetime.datetime.now)
    updated_at: datetime.datetime = field(default_factory=datetime.datetime.now)

@dataclass
class QueryLog:
    """
    Represents a log of a user's query.
    Maps to the 'query_logs' database table.
    """
    log_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str # Foreign Key
    project_id: str # Foreign Key
    query_text: str
    timestamp: datetime.datetime = field(default_factory=datetime.datetime.now)
    results_preview: Optional[List[str]] = field(default_factory=list)


def _parse_datetime(iso_str: Optional[str]) -> Optional[datetime.datetime]:
    """Helper to parse ISO format string to datetime object."""
    if iso_str is None:
        return None
    return datetime.datetime.fromisoformat(iso_str)

def create_user(username: str, email: str, password: str) -> User:
    logger.info(f"Attempting to create user: {username} with email: {email}")
    hashed_password_placeholder = password + "_hashed" # Placeholder for actual hashing
    
    now = datetime.datetime.now()
    user = User(
        username=username,
        email=email,
        hashed_password=hashed_password_placeholder,
        created_at=now,
        updated_at=now
        # user_id and roles use default_factory
    )

    try:
        with _get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                INSERT INTO users (user_id, username, email, hashed_password, created_at, updated_at)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (user.user_id, user.username, user.email, user.hashed_password, 
                  user.created_at.isoformat(), user.updated_at.isoformat()))
            conn.commit()
        logger.info(f"User {user.username} (ID: {user.user_id}) created successfully in DB.")
        return user
    except sqlite3.IntegrityError as e:
        logger.error(f"User creation failed for {username}: {e}")
        if "UNIQUE constraint failed: users.username" in str(e):
            raise ValueError(f"Username '{username}' already exists.")
        elif "UNIQUE constraint failed: users.email" in str(e):
            raise ValueError(f"Email '{email}' already exists.")
        else:
            raise ValueError(f"Could not create user due to integrity error: {e}")


def get_user(user_id: str) -> Optional[User]:
    logger.debug(f"Attempting to retrieve user: {user_id}")
    with _get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
        row = cursor.fetchone()

    if row:
        user = User(
            user_id=row["user_id"],
            username=row["username"],
            email=row["email"],
            hashed_password=row["hashed_password"],
            created_at=_parse_datetime(row["created_at"]),
            updated_at=_parse_datetime(row["updated_at"])
            # roles will use default_factory
        )
        logger.debug(f"Retrieved user: {user_id}")
        return user
    else:
        logger.debug(f"User with ID {user_id} not found in DB.")
        return None

def create_project(project_name: str, user_id: str, description: str) -> Project:
    logger.info(f"Attempting to create project: {project_name} for user {user_id}")
    if not get_user(user_id): # Check if user exists
        logger.error(f"Project creation failed: User with ID '{user_id}' not found.")
        raise ValueError(f"User with ID '{user_id}' not found.")

    now = datetime.datetime.now()
    project = Project(
        project_name=project_name,
        user_id=user_id,
        description=description,
        created_at=now,
        updated_at=now
        # project_id uses default_factory
    )

    with _get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO projects (project_id, project_name, user_id, description, created_at, updated_at)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (project.project_id, project.project_name, project.user_id, project.description,
              project.created_at.isoformat(), project.updated_at.isoformat()))
        conn.commit()
    logger.info(f"Project {project.project_name} (ID: {project.project_id}) created successfully in DB for user {user_id}.")
    return project

def get_project(project_id: str) -> Optional[Project]:
    logger.debug(f"Attempting to retrieve project: {project_id}")
    with _get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM projects WHERE project_id = ?", (project_id,))
        row = cursor.fetchone()

    if row:
        project = Project(
            project_id=row["project_id"],
            project_name=row["project_name"],
            user_id=row["user_id"],
            description=row["description"],
            created_at=_parse_datetime(row["created_at"]),
            updated_at=_parse_datetime(row["updated_at"])
        )
        logger.debug(f"Retrieved project: {project_id}")
        return project
    else:
        logger.debug(f"Project with ID {project_id} not found in DB.")
        return None

def log_user_query(user_id: str, project_id: str, query_text: str, results_preview: Optional[List[str]] = None) -> QueryLog:
    logger.info(f"Attempting to log query for user {user_id}, project {project_id}: {query_text[:100]}...")
    
    if not get_user(user_id):
        logger.error(f"Query logging failed: User with ID '{user_id}' not found.")
        raise ValueError(f"User with ID '{user_id}' not found for query logging.")
    if not get_project(project_id): # Check if project exists
        logger.error(f"Query logging failed: Project with ID '{project_id}' not found.")
        raise ValueError(f"Project with ID '{project_id}' not found for query logging.")

    now = datetime.datetime.now()
    results_preview_json = json.dumps(results_preview) if results_preview is not None else None
    
    query_log_entry = QueryLog(
        user_id=user_id,
        project_id=project_id,
        query_text=query_text,
        timestamp=now, # Explicitly set for consistency, though default_factory would work
        results_preview=results_preview if results_preview is not None else []
        # log_id uses default_factory
    )
    
    with _get_db_connection() as conn:
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO query_logs (log_id, user_id, project_id, query_text, timestamp, results_preview)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (query_log_entry.log_id, query_log_entry.user_id, query_log_entry.project_id,
              query_log_entry.query_text, query_log_entry.timestamp.isoformat(), results_preview_json))
        conn.commit()
    logger.info(f"Query log entry {query_log_entry.log_id} created successfully in DB.")
    return query_log_entry

# Initialize the database and tables when the module is imported
init_db()

# Comments on database interaction (as per previous step, slightly adjusted for SQLite context):
# - This implementation uses SQLite, a file-based database. For larger applications,
#   a server-based RDBMS (e.g., PostgreSQL, MySQL) with an ORM like SQLAlchemy is recommended.
# - Error handling for DB operations is basic; more sophisticated retry mechanisms or
#   transaction management might be needed in a production environment.
# - Timestamps are stored as ISO format strings. SQLite's `TIMESTAMP` type is flexible.
# - The `roles` field in the `User` dataclass is not persisted to the DB in this iteration.
# - Password hashing is a placeholder; use libraries like passlib or bcrypt.
# - Foreign key constraints are defined in table creation but are only enforced by SQLite
#   if `PRAGMA foreign_keys = ON;` is executed per connection. For simplicity, this
#   is not explicitly done in `_get_db_connection()`, relying on application-level checks for now.
#   (In a production system, ensure FK enforcement is active).
# - Concurrency: SQLite supports concurrent reads, but writes are serialized. For high
#   write loads, a different DB might be better.
# - The `init_db()` call at module level is convenient for development but for production,
#   DB initialization/migration should be a more controlled process (e.g., via a CLI command).
