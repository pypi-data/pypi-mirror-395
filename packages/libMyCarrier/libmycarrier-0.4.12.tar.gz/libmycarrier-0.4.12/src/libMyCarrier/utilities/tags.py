import clickhouse_connect
from typing import Dict, List, Any

def pull_tags(CH_HOST: str, CH_USER: str, CH_PASS_SECRET: str, BRANCH: str, REPO: str) -> List[Dict[str, Any]]:
    """
    Pull the latest tags for services from ClickHouse buildinfo table.
    
    Args:
        CH_HOST: ClickHouse host address
        CH_USER: ClickHouse username
        CH_PASS_SECRET: ClickHouse password
        BRANCH: Branch to filter results (uses LIKE %branch%)
        REPO: Repository name to filter results (exact match)
        
    Returns:
        List of dictionaries containing Service, Component, and ImageTag
        
    Raises:
        Exception: If the ClickHouse query fails
    """
    try:
        clickhouse_client = clickhouse_connect.get_client(
            host=CH_HOST, 
            port=8443, 
            username=CH_USER, 
            password=CH_PASS_SECRET
        )
        
        tags = clickhouse_client.query(f'''
            SELECT Service, Component, ImageTag FROM (
                SELECT Service, Component, ImageTag, Timestamp, ROW_NUMBER() OVER (PARTITION BY Service, Component ORDER BY Timestamp DESC) as rn
                FROM ci.buildinfo 
                WHERE BuildBranch like '%{BRANCH}'
                AND BuildRepository = '{REPO}'
                AND BuildStatus = 'OK'
            ) WHERE rn = 1
        ''')
        return tags
    except Exception as e:
        raise Exception(f"Failed to pull tags from ClickHouse: {e}")