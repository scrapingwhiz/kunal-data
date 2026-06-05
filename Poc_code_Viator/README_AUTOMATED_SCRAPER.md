# Viator Automated Scraper - Quick Start Guide

## 🚀 How to Run

### Prerequisites
1. Install Playwright:
   ```bash
   pip install playwright
   playwright install chromium
   ```

2. Make sure MongoDB is running and accessible at `192.168.1.52:27017`

3. Ensure your `config_data.py` has correct settings

### Running the Script

**Simple run:**
```bash
python "viator_request_test 1.py"
```

**Or the standalone version:**
```bash
python viator_automated_scraper.py
```

## 📋 What It Does

1. **Fetches from MongoDB**: Reads pending documents from your database
2. **Checks Cache**: Before fetching, checks if HTML and JSON already exist
3. **Saves Pages**: Downloads and saves both HTML and JSON to your current `save_dir`
4. **Auto Cookie Management**: Browser maintains live session, cookies auto-refresh
5. **Session Management**: Automatically applies cooldowns (5-15 mins) after each batch
6. **Rate Limiting**: Max 35 API calls per session, 10 products per batch

## 🎯 Key Features

### Cache-First Approach
- ✅ Checks if `{hashid}.html` exists
- ✅ Checks if `{hashid}.json` exists  
- ✅ Only fetches if missing
- ✅ Skips products with complete cache

### Automatic Cookie Refresh
- Uses Playwright CDP to connect to persistent Chrome browser
- Browser stays alive, cookies refresh naturally
- No manual DevTools copy/paste needed!

### Smart Session Management
- Processes 10 products per session
- Max 35 API calls per session
- 6-12 second delay between products
- 5-15 minute cooldown between sessions

## 📊 Status Updates

The script updates MongoDB `Status` field:
- `"Pending"` → Waiting to process
- `"HTML_Done"` → HTML and JSON saved successfully
- `"Not Found"` → Product unavailable or error

## 🔧 Configuration

Edit these variables in the script if needed:

```python
CHROME_PORT = 9222  # Remote debugging port
CHROME_PROFILE = r"C:\chrome_viator_profile"  # Persistent profile

MAX_API_CALLS_PER_SESSION = 35  # API call limit
MAX_PRODUCTS_PER_SESSION = 10   # Products per batch
API_SLEEP_RANGE = (6, 12)       # Seconds between requests
SESSION_COOLDOWN = (300, 900)    # 5-15 minutes cooldown
```

## 📁 File Outputs

All files saved to: `E:\Kamaram\Projects\Crawl_Data_Collection\Viator\Htmls\{today}`

```
2026_01_28/
├── {hashid}.html  # Product page HTML
├── {hashid}.json  # API availability data
└── ...
```

## 🛑 Stopping the Script

- Press `Ctrl+C` to gracefully stop
- Browser will close automatically
- Progress is saved to MongoDB

## 💡 Tips

1. **First Run**: Let it process a small batch (10-20 products) to verify everything works
2. **Overnight**: Just start the script and let it run overnight - fully automated!
3. **Monitoring**: Watch the console for progress updates and any errors
4. **Resume**: If stopped, just restart - it will skip cached files and continue

## ⚠️ Troubleshooting

**Chrome won't start?**
- Check if Chrome is installed at: `C:\Program Files\Google\Chrome\Application\chrome.exe`
- Kill any existing Chrome processes
- Delete profile directory and try again

**MongoDB connection error?**
- Verify MongoDB is running
- Check connection string in `config_data.py`

**No documents found?**
- Verify documents have `Status: "Pending"` in MongoDB
- Check collection name matches your day (e.g., `inputs_for_tuesday`)

## 📞 Support

If you encounter issues, check:
1. Console output for error messages
2. MongoDB for status updates
3. Save directory for created files

---

**Ready to automate! Just run the script and watch it work. 🎉**
