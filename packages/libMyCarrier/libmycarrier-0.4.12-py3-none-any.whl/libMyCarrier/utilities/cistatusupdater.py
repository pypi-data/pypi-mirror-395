#! /usr/bin/env python3
import os
import sys
import logging
import clickhouse_connect
from typing import List, Dict, Any, Tuple, Optional
from datetime import datetime, timezone

# Set up logger
logger = logging.getLogger(__name__)

# Try to import dotenv, but make it optional
try:
    from dotenv import load_dotenv
    has_dotenv = True
except ImportError:
    has_dotenv = False
    logger.debug("python-dotenv not installed; .env file loading disabled")

def setup_logging(level=logging.INFO):
    """Configure logging for the module"""
    logging.basicConfig(
        level=level,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )

def clickhouse_insert(ch_host: str, ch_user: str, ch_pass_secret: str, ch_table: str, ch_data: List[List[Any]]) -> None:
    """
    Insert data into ClickHouse table.
    
    Args:
        ch_host: ClickHouse host address
        ch_user: ClickHouse username
        ch_pass_secret: ClickHouse password
        ch_table: ClickHouse table name
        ch_data: List of data rows to insert
        
    Raises:
        Exception: If the insertion fails
    """
    try:
        clickhouse_client = clickhouse_connect.get_client(
            host=ch_host, 
            port=8443, 
            username=ch_user, 
            password=ch_pass_secret
        )
        clickhouse_client.insert(ch_table, ch_data, column_names='*')
        logger.info(f"Successfully inserted {len(ch_data)} rows into {ch_table}")
    except Exception as e:
        raise Exception("Failed to insert data into ClickHouse") from e

def ci_build_info(tag: str, version: str, branch: str, repo: str, job_status: str) -> List[List[Any]]:
    """
    Generate CI build info data for ClickHouse insertion.
    
    Args:
        tag: Image tag
        version: Version number
        branch: Git branch name
        repo: Git repository URL
        job_status: Status of the CI job
        
    Returns:
        List containing the formatted build information
    """
    ch_data = []
    
    # Parse service and component from tag
    if 'src/MC' in tag:
        image_repository = tag.replace('src/MC.', 'appstack/').lower().replace('.', '/')
        component = ''.join(tag.split('.')[2:]).lower()
        service = tag.split('.')[1].lower()
    else:
        image_repository = tag.lower().replace('.', '/')
        component = ''.join(tag.lower().split('/')[1:])
        service = ''.join(tag.lower().split('/')[0])
    
    # Generate image tag from version
    image_tag = f"{version}"
    
    # Clean up repository URL
    build_repository = f"{repo}".replace('.git', '').replace('https://', '')
    
    # Set branch name
    build_branch = f"{branch}"
    
    # Get current timestamp in UTC
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    
    # Normalize job status
    normalized_status = job_status
    if job_status != 'OK' and job_status != 'IN_PROGRESS':
        normalized_status = 'ERROR'
    
    # Create data row
    ch_data.append([
        timestamp, 
        service, 
        component, 
        build_repository, 
        build_branch, 
        image_repository, 
        image_tag, 
        normalized_status
    ])

    logger.debug(f"Generated build info: {ch_data}")
    return ch_data

def ci_deploy_info(environment: str, repository: str, branch: str, sha: str, 
                  job_status: str, render_status: str, deploy_status: str, 
                  gitops_commit: Optional[str]) -> List[List[Any]]:
    """
    Generate CI deployment info data for ClickHouse insertion.
    
    Args:
        environment: Deployment environment (prod, dev, etc.)
        repository: Git repository URL
        branch: Git branch name
        sha: Git commit SHA
        job_status: Status of the CI job
        render_status: Status of the render step
        deploy_status: Status of the deploy step
        gitops_commit: GitOps commit hash or message
        
    Returns:
        List containing the formatted deployment information
    """
    ch_data = []
    
    # Normalize environment name
    environment = environment.lower()
    
    # Extract repository name from URL
    repository = repository.split('/')[-1].replace('.git', '').lower()
    
    # Clean up branch name
    branch = branch.replace('refs/heads/', '').lower()
    
    # Get current timestamp in UTC
    timestamp = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%S.%fZ")
    
    # Determine GitOps repository based on environment
    gitops_repository = 'GitOps-prod' if environment == 'prod' else 'GitOps-dev'
    
    # Handle special case for gitops_commit
    if gitops_commit == 'Nothing to commit':
        gitops_commit = None
    
    # Determine overall status
    if job_status == 'IN_PROGRESS':
        status = 'IN_PROGRESS'
        gitops_commit = None
    else:
        if render_status != 'OK' or deploy_status != 'OK':
            status = 'ERROR'
        else:
            status = 'OK'
    
    # Create data row
    ch_data.append([
        timestamp, 
        environment, 
        repository, 
        branch, 
        sha, 
        status, 
        gitops_repository, 
        gitops_commit
    ])
    
    logger.debug(f"Generated deploy info: {ch_data}")
    return ch_data

def get_env_var(name: str, required: bool = True) -> Optional[str]:
    """
    Get environment variable with error handling.
    
    Args:
        name: Name of the environment variable
        required: Whether the variable is required
        
    Returns:
        Value of the environment variable or None if not required and not found
        
    Raises:
        ValueError: If a required environment variable is missing
    """
    value = os.getenv(name)
    if required and not value:
        raise ValueError(f"Required environment variable '{name}' is not set")
    return value

def main():
    """
    Main entry point for CI status updater.
    
    Reads environment variables to determine job type and updates
    the appropriate ClickHouse table with status information.
    
    Returns:
        Exit code (0 for success, non-zero for errors)
    """
    # Setup logging
    setup_logging()
    
    try:
        # Load .env file if exists and dotenv is installed (for local development)
        if has_dotenv:
            load_dotenv()
        
        # Required ClickHouse variables
        CH_HOST = get_env_var('CH_HOST')
        CH_USER = get_env_var('CH_USER')
        CH_PASS_SECRET = get_env_var('CH_PASS_SECRET')
        
        # Common required variables
        JOB_TYPE = get_env_var('JOB_TYPE')
        JOB_STATUS = get_env_var('JOB_STATUS')
        BRANCH = get_env_var('BRANCH')
        CLONE_URL = get_env_var('CLONE_URL')
        
        if JOB_TYPE == 'build':
            # Build-specific variables
            TAG = get_env_var('TAG')
            VERSION = get_env_var('VERSION')
            
            # Generate and insert build data
            data = ci_build_info(TAG, VERSION, BRANCH, CLONE_URL, JOB_STATUS)
            clickhouse_insert(CH_HOST, CH_USER, CH_PASS_SECRET, 'ci.buildinfo', data)
            logger.info(f"Successfully updated build info for {TAG} version {VERSION}")
            
        elif JOB_TYPE == 'render':
            # Render-specific variables
            RENDER_STATUS = get_env_var('RENDER_STATUS')
            DEPLOY_STATUS = get_env_var('DEPLOY_STATUS')
            SHA = get_env_var('SHA')
            ENVIRONMENT = get_env_var('ENVIRONMENT')
            GITOPS_COMMIT = get_env_var('GITOPS_COMMIT', required=False)
            
            # Generate and insert deployment data
            data = ci_deploy_info(
                ENVIRONMENT, CLONE_URL, BRANCH, SHA,
                JOB_STATUS, RENDER_STATUS, DEPLOY_STATUS, GITOPS_COMMIT
            )
            clickhouse_insert(CH_HOST, CH_USER, CH_PASS_SECRET, 'ci.deployinfo', data)
            logger.info(f"Successfully updated deployment info for {ENVIRONMENT} from {BRANCH}")
            
        else:
            logger.error(f"Invalid JOB_TYPE: {JOB_TYPE}")
            return 1
            
        return 0
        
    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        return 1
    except Exception as e:
        logger.error(f"Unexpected error: {e}")
        return 1

if __name__ == "__main__":
    sys.exit(main())
