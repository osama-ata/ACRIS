import os
import logging
import sqlite3 # Though not directly used for table ops, good for context/potential direct checks
import sys
from typing import Optional, List # For type hints if needed in test functions

# Adjust path to import from acris.upq.api
# This assumes the script is run from the root of the 'acris' project or 'acris' is in PYTHONPATH
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from acris.upq.api import (
    create_user, get_user,
    create_project, get_project,
    log_user_query,
    User, Project, QueryLog, # Dataclasses
    init_db, DB_FILE # DB utility and filename
)

# Configure basic logging for the test script
logging.basicConfig(
    level=logging.DEBUG, # Set to DEBUG to see API's debug logs as well
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler() # Log to console
    ]
)
logger = logging.getLogger(__name__)

# --- Test Functions will be defined here ---

def test_user_creation_and_retrieval():
    logger.info("Starting test_user_creation_and_retrieval...")
    try:
        # 1. Create a new user
        user1 = create_user("testuser1", "test1@example.com", "password123")
        logger.info(f"User creation successful: {user1.user_id}, {user1.username}")

        # 2. Retrieve the created user
        retrieved_user = get_user(user1.user_id)
        if retrieved_user:
            logger.info(f"Successfully retrieved user: {retrieved_user.user_id}, {retrieved_user.username}")
            assert retrieved_user.username == "testuser1"
        else:
            logger.error(f"Failed to retrieve user: {user1.user_id}")

        # 3. Attempt to create a user with a duplicate username
        try:
            create_user("testuser1", "test1_dup_email@example.com", "password_dup")
            logger.error("Duplicate username test FAILED: ValueError was not raised for username 'testuser1'")
        except ValueError as e:
            logger.info(f"Duplicate username test PASSED: Expected error caught: {e}")
        
        # 4. Attempt to create a user with a duplicate email
        try:
            create_user("testuser1_dup_uname", "test1@example.com", "password_dup")
            logger.error("Duplicate email test FAILED: ValueError was not raised for email 'test1@example.com'")
        except ValueError as e:
            logger.info(f"Duplicate email test PASSED: Expected error caught: {e}")

    except Exception as e:
        logger.error(f"An unexpected error occurred in test_user_creation_and_retrieval: {e}", exc_info=True)
    logger.info("Finished test_user_creation_and_retrieval.")


def test_project_creation_and_retrieval():
    logger.info("Starting test_project_creation_and_retrieval...")
    try:
        # 1. Create a prerequisite user
        user_for_project = create_user("projectuser", "project@example.com", "projectpass")
        logger.info(f"Prerequisite user created: {user_for_project.user_id}")

        # 2. Create a new project for this user
        project1 = create_project("Test Project Alpha", user_for_project.user_id, "A test project.")
        logger.info(f"Project creation successful: {project1.project_id}, {project1.project_name}")

        # 3. Retrieve the project
        retrieved_project = get_project(project1.project_id)
        if retrieved_project:
            logger.info(f"Successfully retrieved project: {retrieved_project.project_id}, {retrieved_project.project_name}")
            assert retrieved_project.project_name == "Test Project Alpha"
            assert retrieved_project.user_id == user_for_project.user_id
        else:
            logger.error(f"Failed to retrieve project: {project1.project_id}")

        # 4. Attempt to create a project for a non-existent user
        non_existent_user_id = "non_existent_uuid"
        try:
            create_project("Orphan Project", non_existent_user_id, "This should fail.")
            logger.error(f"Project creation for non-existent user FAILED: ValueError was not raised for user_id '{non_existent_user_id}'")
        except ValueError as e:
            logger.info(f"Project creation for non-existent user PASSED: Expected error caught: {e}")

    except Exception as e:
        logger.error(f"An unexpected error occurred in test_project_creation_and_retrieval: {e}", exc_info=True)
    logger.info("Finished test_project_creation_and_retrieval.")


def test_query_logging():
    logger.info("Starting test_query_logging...")
    try:
        # 1. Create prerequisite user and project
        query_user = create_user("queryuser", "query@example.com", "querypass")
        logger.info(f"Prerequisite user for query logging created: {query_user.user_id}")
        
        query_project = create_project("Query Test Project", query_user.user_id, "Project for query logging test.")
        logger.info(f"Prerequisite project for query logging created: {query_project.project_id}")

        # 2. Log a sample query
        query_text = "Find all risks related to crane operations."
        results_preview = ["doc_id_123", "doc_id_456"]
        query_log_entry = log_user_query(query_user.user_id, query_project.project_id, query_text, results_preview)
        if query_log_entry:
            logger.info(f"Query logged successfully: Log ID {query_log_entry.log_id}, User {query_log_entry.user_id}, Query: {query_log_entry.query_text[:30]}...")
            assert query_log_entry.user_id == query_user.user_id
            assert query_log_entry.project_id == query_project.project_id
            assert query_log_entry.results_preview == results_preview
        else:
            logger.error("Failed to log query.")

        # 3. Attempt to log a query for a non-existent user
        non_existent_user_id = "non_existent_uuid_for_query"
        try:
            log_user_query(non_existent_user_id, query_project.project_id, "Test query non-existent user", [])
            logger.error(f"Query logging for non-existent user FAILED: ValueError was not raised for user_id '{non_existent_user_id}'")
        except ValueError as e:
            logger.info(f"Query logging for non-existent user PASSED: Expected error caught: {e}")

        # 4. Attempt to log a query for a non-existent project
        non_existent_project_id = "non_existent_uuid_for_query_project"
        try:
            log_user_query(query_user.user_id, non_existent_project_id, "Test query non-existent project", [])
            logger.error(f"Query logging for non-existent project FAILED: ValueError was not raised for project_id '{non_existent_project_id}'")
        except ValueError as e:
            logger.info(f"Query logging for non-existent project PASSED: Expected error caught: {e}")
            
    except Exception as e:
        logger.error(f"An unexpected error occurred in test_query_logging: {e}", exc_info=True)
    logger.info("Finished test_query_logging.")


if __name__ == "__main__":
    logger.info("Starting UPQ DB Integration Test Script...")

    # Define DB file path relative to this script's location (acris/upq/DB_FILE)
    # DB_FILE from api module is just the filename "acris_upq.db"
    # This script is in acris/upq/, so DB_FILE will be created in acris/upq/
    db_path = os.path.join(os.path.dirname(__file__), DB_FILE)

    # Delete the database file to ensure a fresh start for each test run
    if os.path.exists(db_path):
        try:
            os.remove(db_path)
            logger.info(f"Successfully deleted existing database: {db_path}")
        except OSError as e:
            logger.error(f"Error deleting database file {db_path}: {e}. Please check permissions.", exc_info=True)
            sys.exit(1) # Exit if we can't ensure a clean slate
    
    # Initialize the database (creates tables)
    # init_db() is defined in acris.upq.api and uses DB_FILE which should resolve correctly
    # as api.py is in the same directory where DB_FILE will be created.
    logger.info(f"Initializing database: {db_path}...")
    init_db() # This will create acris_upq.db in the acris/upq/ directory

    logger.info("--- Running User Creation and Retrieval Test ---")
    test_user_creation_and_retrieval()
    logger.info("--- Finished User Creation and Retrieval Test ---")

    logger.info("--- Running Project Creation and Retrieval Test ---")
    test_project_creation_and_retrieval()
    logger.info("--- Finished Project Creation and Retrieval Test ---")

    logger.info("--- Running Query Logging Test ---")
    test_query_logging()
    logger.info("--- Finished Query Logging Test ---")

    logger.info("UPQ DB Integration Test Script finished.")
