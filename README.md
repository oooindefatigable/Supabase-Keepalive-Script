# Supabase Keepalive Script

A Python script designed to prevent Supabase databases from pausing due to inactivity by automatically writing timestamp records every 2 hours.

## Purpose

Supabase free tier databases automatically pause after a period of inactivity to conserve resources. This script prevents that by:

- Connecting to your Supabase database every 2 hours
- Writing a timestamp record to a dedicated `keepalive` table
- Automatically cleaning up old records (keeps only last 100 entries)
- Running continuously as a background service

## Features

- ✅ Automatic database keepalive every 2 hours
- ✅ Built-in error handling and retry logic
- ✅ Automatic cleanup of old records
- ✅ Comprehensive logging
- ✅ Easy setup with hardcoded credentials
- ✅ Systemd service support for Linux servers

## Files Included

- `supabase_keepalive.py` - Main keepalive script with hardcoded credentials
- `test_supabase_connection.py` - Connection test script
- `create_keepalive_table.sql` - SQL script to create the keepalive table
- `README.md` - This documentation

## Installation

1. **Install Python dependencies:**
   ```bash
   pip3 install supabase
   ```

2. **Create the keepalive table in your Supabase database:**
   - Run the SQL script `create_keepalive_table.sql` in your Supabase SQL editor
   - Or execute it using the v0 script runner

3. **Test the connection:**
   ```bash
   python3 test_supabase_connection.py
   ```

## Usage

### Manual Execution
```bash
python3 supabase_keepalive.py
```

The script will run continuously, pinging the database every 2 hours.

### As a Linux Service (Recommended)

1. **Create a systemd service file:**
   ```bash
   sudo nano /etc/systemd/system/supabase-keepalive.service
   ```

2. **Add the following content:**
   ```ini
   [Unit]
   Description=Supabase Keepalive Service
   After=network.target

   [Service]
   Type=simple
   User=your_username
   WorkingDirectory=/path/to/your/script/directory
   ExecStart=/usr/bin/python3 supabase_keepalive.py
   Restart=always
   RestartSec=30

   [Install]
   WantedBy=multi-user.target
   ```

3. **Enable and start the service:**
   ```bash
   sudo systemctl enable supabase-keepalive.service
   sudo systemctl start supabase-keepalive.service
   sudo systemctl status supabase-keepalive.service
   ```

## Configuration

The script needs to be configured with your Supabase credentials. Edit the script file and replace the placeholder values:

```python
SUPABASE_URL = "your_supabase_url"
SUPABASE_SERVICE_ROLE_KEY = "your_supabase_service_role"
```

Get these values from your Supabase dashboard:
- **SUPABASE_URL**: Settings → API → Project URL
- **SUPABASE_SERVICE_ROLE_KEY**: Settings → API → service_role (secret key)

## How It Works

1. **Connection:** Establishes connection to Supabase using the service role key
2. **Ping:** Every 2 hours, inserts a new record with current timestamp
3. **Cleanup:** Automatically removes old records, keeping only the latest 100
4. **Logging:** Provides detailed logs of all operations and any errors
5. **Recovery:** Automatically retries on connection failures

## Monitoring

The script provides comprehensive logging:
- ✅ Successful database pings
- ⚠️ Connection warnings
- ❌ Error details and retry attempts
- 📊 Cleanup operations

## Troubleshooting

**Script won't start:**
- Ensure `supabase` package is installed: `pip3 install supabase`
- Check that the keepalive table exists in your database
- Verify credentials are properly configured in the script

**Connection errors:**
- Verify your Supabase project is active
- Check that the service role key hasn't been regenerated
- Ensure the URL format is correct

**Service issues:**
- Check service status: `sudo systemctl status supabase-keepalive.service`
- View logs: `sudo journalctl -u supabase-keepalive.service -f`

## Security Note

⚠️ **Important:** To avoid credential leaks, always use placeholder values when sharing code:

```python
SUPABASE_URL = "your_supabase_url"
SUPABASE_SERVICE_ROLE_KEY = "your_supabase_service_role"
```

This script uses the service role key which has elevated permissions. Ensure:
- The script file has appropriate permissions (readable only by the service user)
- The server where this runs is secure
- Never commit actual credentials to version control
- Consider using environment variables in production environments

## Support

If this script helped you keep your Supabase database active, consider supporting the development:

☕ **[Buy me a coffee](https://buymeacoffee.com/oooindefatigable)**

## License

This script is provided as-is for keeping Supabase databases active. Use at your own discretion.
