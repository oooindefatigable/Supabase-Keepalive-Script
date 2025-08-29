import os
from supabase import create_client
from datetime import datetime

def test_connection():
    """Test script to verify Supabase connection and table setup."""
    print("🔍 Testing Supabase connection...")
    
    try:
        # Create client
        url = "your_supabase_url"
        key = "your_supabase_service_role"
        
        supabase = create_client(url, key)
        print("✅ Supabase client created")
        
        # Test insert
        result = supabase.table('keepalive_pings').insert({
            'ping_time': datetime.now().isoformat()
        }).execute()
        
        if result.data:
            print("✅ Test ping successful!")
            print(f"📊 Inserted record: {result.data[0]}")
            
            # Test select
            recent_pings = supabase.table('keepalive_pings').select('*').limit(5).execute()
            print(f"📋 Recent pings count: {len(recent_pings.data)}")
            
            return True
        else:
            print("❌ Test ping failed")
            return False
            
    except Exception as e:
        print(f"💥 Error: {str(e)}")
        return False

if __name__ == "__main__":
    test_connection()
