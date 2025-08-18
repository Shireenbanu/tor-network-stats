import os
import logging
from typing import Dict, Any
from src.domains.tor_net_fetcher.service import TorNetFetchService

logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event: Dict[str, Any], context) -> Dict[str, Any]:
    """
    AWS Lambda handler for fetching and storing Tor relay data
    """
    try:
        logger.info("Starting Tor relay data fetch")
        
        # # Initialize database session
        # db = next(get_db_session())
        
            # Business logic from your domain service
        count = TorNetFetchService.fetch_tor_and_net_stats_for_all_countries()
            
        logger.info(f"Successfully fetched tor and internet stats.")
        return {
                'statusCode': 200,
                'body': f"Updated {count} relays"
            }
            
            
    except Exception as e:
        logger.error(f"Lambda execution failed: {str(e)}")
        return {
            'statusCode': 500,
            'body': f"Error: {str(e)}"
        }