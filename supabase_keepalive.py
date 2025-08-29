import os
import time
from datetime import datetime
from supabase import create_client, Client
import logging
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

SUPABASE_URL = "your_supabase_url"
SUPABASE_SERVICE_ROLE_KEY = "your_supabase_service_role"

def create_supabase_client() -> Client:
    """Create and return a Supabase client using hardcoded credentials."""
    return create_client(SUPABASE_URL, SUPABASE_SERVICE_ROLE_KEY)

def ping_database(supabase: Client) -> bool:
    """Insert a keepalive ping into the database."""
    try:
        current_time = datetime.now().isoformat()
        
        # Insert a new ping record
        result = supabase.table('keepalive_pings').insert({
            'ping_time': current_time
        }).execute()
        
        if result.data:
            logger.info(f"✅ Keepalive ping successful at {current_time}")
            return True
        else:
            logger.error("❌ Failed to insert keepalive ping")
            return False
            
    except Exception as e:
        logger.error(f"❌ Error during keepalive ping: {str(e)}")
        return False

def cleanup_old_pings(supabase: Client, days_to_keep: int = 7):
    """Remove old ping records to prevent table from growing indefinitely."""
    try:
        # Delete pings older than specified days
        result = supabase.table('keepalive_pings').delete().lt(
            'created_at', 
            f"now() - interval '{days_to_keep} days'"
        ).execute()
        
        if result.data:
            logger.info(f"🧹 Cleaned up old ping records (keeping last {days_to_keep} days)")
        
    except Exception as e:
        logger.error(f"⚠️ Error during cleanup: {str(e)}")

def main():
    """Main function to run the keepalive script."""
    logger.info("🚀 Starting Supabase keepalive script...")
    logger.info("📅 Will ping database every 2 hours to prevent pause")
    
    try:
        # Create Supabase client
        supabase = create_supabase_client()
        logger.info("✅ Supabase client created successfully")
        
        # Test initial connection
        if not ping_database(supabase):
            logger.error("❌ Initial ping failed. Check your database connection and table setup.")
            return
        
        ping_count = 1
        
        # Main loop - ping every 2 hours (7200 seconds)
        while True:
            logger.info(f"😴 Sleeping for 2 hours... (Next ping will be #{ping_count + 1})")
            time.sleep(7200)  # 2 hours = 7200 seconds
            
            # Ping the database
            ping_database(supabase)
            ping_count += 1
            
            # Cleanup old records every 24 pings (approximately every 2 days)
            if ping_count % 24 == 0:
                cleanup_old_pings(supabase)
                
    except KeyboardInterrupt:
        logger.info("⏹️ Keepalive script stopped by user")
    except Exception as e:
        logger.error(f"💥 Unexpected error: {str(e)}")

if __name__ == "__main__":
    main()
