"""
Viator Automated Scraper - Full Automation Solution
Based on viator_request_test 1.py with MongoDB integration and cache management

Features:
- Automated cookie management via Playwright CDP
- Fetches inputs from MongoDB
- Checks cache before fetching (HTML + JSON)
- Saves all pages to current directory structure
- Session management with cooldowns
- Rate limiting to avoid blocking
"""

import json
import time
import random
import os
import subprocess
from datetime import datetime, timedelta
from playwright.sync_api import sync_playwright
from config_data import *

# ===================== CONFIG =====================
CHROME_PORT = 9222
CHROME_PROFILE = r"C:\chrome_viator_profile"

MAX_API_CALLS_PER_SESSION = 35
MAX_PRODUCTS_PER_SESSION = 10
API_SLEEP_RANGE = (6, 12)
SESSION_COOLDOWN = (300, 900)  # 5-15 minutes

ADULTS = 2

MARKET_CONFIG = {
    "US": {
        "currency": "USD",
        "currency_name": "US Dollar",
        "symbol": "$",
        "locale": "en-US",
    },

    "MX": {
        "currency": "MXN",
        "currency_name": "Mexican Peso",
        "symbol": "MX$",
        "locale": "es-MX",
    },

    "IN": {
        "currency": "INR",
        "currency_name": "Indian Rupee",
        "symbol": "₹",
        "locale": "en-IN",
    },

    "UK": {
        "currency": "GBP",
        "currency_name": "British Pound",
        "symbol": "£",
        "locale": "en-GB",
    },

    "AU": {
        "currency": "AUD",
        "currency_name": "Australian Dollar",
        "symbol": "A$",
        "locale": "en-AU",
    },

    "CA": {
        "currency": "CAD",
        "currency_name": "Canadian Dollar",
        "symbol": "CA$",
        "locale": "en-CA",
    },

    "ES": {
        "currency": "EUR",
        "currency_name": "Euro",
        "symbol": "€",
        "locale": "es-ES",
    },
}


# ===================== HELPERS =====================
def start_chrome():
    """Start Chrome with remote debugging enabled"""
    chrome = r"C:\Program Files\Google\Chrome\Application\chrome.exe"
    os.makedirs(CHROME_PROFILE, exist_ok=True)
    
    print(f"🌐 Starting Chrome with profile: {CHROME_PROFILE}")
    subprocess.Popen([
        chrome,
        f"--remote-debugging-port={CHROME_PORT}",
        f"--user-data-dir={CHROME_PROFILE}",
        "--no-first-run",
        "--disable-extensions",
    ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(3)


def block_unneeded(route):
    """Block unnecessary resources to speed up page loads"""
    if route.request.resource_type in ("image", "media", "font"):
        return route.abort()
    if any(x in route.request.url for x in [
        "google-analytics",
        "doubleclick",
        "hotjar",
        "facebook",
        "segment",
        "optimizely",
    ]):
        return route.abort()
    return route.continue_()


def wait_for_page_ready(page, timeout=30000):
    """Wait for page to be fully ready for interaction"""
    print("⏳ Waiting for page to be ready...")
    
    page.wait_for_load_state("domcontentloaded", timeout=timeout)
    print("  ✓ DOM loaded")
    
    page.wait_for_timeout(3000)
    
    # Check if currency button is present and clickable
    currency_btn = page.locator("//button[@data-automation='language_currency_button']")
    currency_btn.wait_for(state="attached", timeout=10000)
    print("  ✓ Currency button attached")
    
    currency_btn.wait_for(state="visible", timeout=10000)
    print("  ✓ Currency button visible")
    
    page.wait_for_timeout(2000)
    print("  ✓ Page ready!")
    
    return True


def change_currency(page, currency):
    """Change the currency on the page safely"""
    try:
        print(f"  🌍 Changing currency to {currency}...")

        # Open language/currency modal
        page.locator(
            "//button[@data-automation='language_currency_button']"
        ).click()

        # Open currency section
        page.locator(
            "//button[@data-automation='currency']"
        ).click()

        # Wait for navigation/reload triggered by currency switch
        with page.expect_navigation(wait_until="networkidle", timeout=60000):
            page.locator(
                f"//span[@data-automation='header-navigation-currency-menu-code' and text()='{currency}']/ancestor::button"
            ).click()

        # Extra stabilization
        page.wait_for_load_state("networkidle")

        # Ensure body exists
        page.locator("body").wait_for(state="visible", timeout=15000)

        print(f"  ✓ Currency changed to {currency}")

    except Exception as e:
        print(f"  ⚠ Currency change failed: {e}")


def cache_exists(hashid):
    """Check if both HTML and JSON cache files exist"""
    html_path = os.path.join(save_dir, f"{hashid}.html")
    json_path = os.path.join(save_dir, f"{hashid}.json")
    
    html_exists = os.path.exists(html_path)
    json_exists = os.path.exists(json_path)
    
    return html_exists and json_exists, html_exists, json_exists


def save_html_page(page, hashid):
    """Save the current page HTML safely"""

    html_path = os.path.join(save_dir, f"{hashid}.html")

    # Ensure page stabilized
    page.wait_for_load_state("domcontentloaded")
    page.wait_for_load_state("networkidle")

    # Small stabilization delay
    page.wait_for_timeout(2000)

    html_content = page.content()

    with open(html_path, 'w', encoding='utf-8') as f:
        f.write(html_content)

    print(f"  ✓ Saved HTML: {hashid}.html")

    return html_path


def fetch_json_via_browser(page, product_code, date_str):
    """Fetch JSON data using browser's fetch API"""
    try:
        result = page.evaluate("""
        async ({ productCode, dateStr }) => {
            async function fetchAndDecodeStream() {
                const response = await fetch(
                    "https://www.viator.com/orion/ajax/product-availability",
                    {
                        method: "POST",
                        mode: "cors",
                        credentials: "include",
                        headers: {
                            "accept": "application/json, text/plain, */*",
                            "accept-language": "en-GB,en-US;q=0.9,en;q=0.8",
                            "content-type": "application/json",
                            "x-requested-with": "XMLHttpRequest",
                            "x-frontend-date-validation": "true",
                            "x-xsrf-token": document.cookie
                                .split("; ")
                                .find(c => c.startsWith("XSRF-TOKEN="))
                                ?.split("=")[1]
                        },
                        referrer: window.location.href,
                        body: JSON.stringify({
                            productCode: productCode,
                            searchDate: dateStr,
                            ageBands: { ADULT: "2" }
                        })
                    }
                );

                if (!response.ok) {
                    return {
                        status: response.status,
                        error: true,
                        text: await response.text()
                    };
                }

                const reader = response.body.getReader();
                const decoder = new TextDecoder("utf-8");
                let resultString = "";

                while (true) {
                    const { done, value } = await reader.read();
                    if (done) break;
                    resultString += decoder.decode(value, { stream: true });
                }

                resultString += decoder.decode();

                return {
                    status: response.status,
                    error: false,
                    text: resultString
                };
            }

            return await fetchAndDecodeStream();
        }
        """, {
            "productCode": product_code,
            "dateStr": date_str,
        })
        
        if result.get('error'):
            print(f"  ❌ JSON fetch error: Status {result.get('status')}")
            return None
        
        return result.get('text')
        
    except Exception as e:
        print(f"  ❌ Error fetching JSON: {e}")
        return None


def save_json_response(json_text, hashid):
    """Save JSON response to file"""
    json_path = os.path.join(save_dir, f"{hashid}.json")
    
    with open(json_path, 'w', encoding='utf-8') as f:
        f.write(json_text)
    
    print(f"  ✓ Saved JSON: {hashid}.json")
    return json_path


def process_document(doc, page, current_country, api_calls_counter, products_counter):
    """Process a single document - fetch and save HTML + JSON"""
    
    # Extract document data
    referer_url = doc['URL']
    order_code = doc['Order Code']
    seasonality = str(doc['Seasonality'])
    competitor = doc['Competitor']
    sm = doc['SM']
    pax = int(doc['pax'])
    
    # Generate hash ID
    hashid = generate_hash_id(referer_url, order_code, seasonality, competitor, sm, pax)
    
    # Check cache
    both_exist, html_exists, json_exists = cache_exists(hashid)
    
    if both_exist:
        print(f"✓ Cache exists for {order_code} - Skipping")
        return current_country, api_calls_counter, products_counter, True
    
    print(f"\n{'='*80}")
    print(f"📦 Processing Order: {order_code}")
    print(f"   URL: {referer_url}")
    print(f"   Market: {sm} | Date: {seasonality}")
    print(f"   Cache Status: HTML={'✓' if html_exists else '✗'} JSON={'✓' if json_exists else '✗'}")
    
    try:
        # Navigate to page if HTML not cached
        if not html_exists:
            print(f"🌐 Loading page...")
            page.goto(referer_url, wait_until="domcontentloaded", timeout=60000)
            page.wait_for_timeout(2000)
            
            # Currency change if needed
            if current_country != sm:
                market = MARKET_CONFIG.get(sm, MARKET_CONFIG["US"])

                currency = market["currency"]
                currency_name = market["currency_name"]
                currency_symbol = market["symbol"]
                locale = market["locale"]
                change_currency(page, currency)
                current_country = sm
            
            # Save HTML
            save_html_page(page, hashid)
        else:
            print(f"  ✓ HTML already cached")
        
        # Fetch and save JSON if not cached
        if not json_exists:
            print(f"📊 Fetching JSON data...")
            
            # Extract product code from URL
            product_code = referer_url.split("/")[-1].split("-")[-1]
            
            # Get date in correct format
            season_date = convert_to_standard_date(seasonality)
            
            # Fetch JSON via browser
            json_text = fetch_json_via_browser(page, product_code, season_date)
            
            if json_text:
                # Check for errors
                if 'OUT_OF_AGE_RANGE' in json_text:
                    print(f"  ⚠ Product not available for this age range")
                    search_data.update_one({"_id": doc['_id']}, {"$set": {"Status": "Not Found"}})
                else:
                    save_json_response(json_text, hashid)
                    api_calls_counter[0] += 1
            else:
                print(f"  ❌ Failed to fetch JSON")
                return current_country, api_calls_counter, products_counter, False
        else:
            print(f"  ✓ JSON already cached")
        
        # Update status
        search_data.update_one({"_id": doc['_id']}, {"$set": {"Status": "HTML_Done"}})
        products_counter[0] += 1
        
        print(f"✅ Completed: {order_code}")
        
        # Random sleep between products
        sleep_time = random.uniform(*API_SLEEP_RANGE)
        print(f"💤 Sleeping {sleep_time:.1f}s before next product...")
        time.sleep(sleep_time)
        
        return current_country, api_calls_counter, products_counter, True
        
    except Exception as e:
        print(f"❌ Error processing {order_code}: {e}")
        return current_country, api_calls_counter, products_counter, False


def run_session(docs):
    """Run a single session with automatic cookie management"""
    api_calls = [0]  # Use list to allow modification in nested function
    products_done = [0]
    current_country = None
    
    print(f"\n{'#'*80}")
    print(f"🚀 Starting new session with {len(docs)} documents")
    print(f"{'#'*80}\n")
    
    start_chrome()
    
    with sync_playwright() as p:
        browser = p.chromium.connect_over_cdp(f"http://localhost:{CHROME_PORT}")
        context = browser.contexts[0]
        page = context.new_page()
        
        # Enable request blocking
        page.route("**/*", block_unneeded)
        
        for i, doc in enumerate(docs, 1):
            # Check session limits
            if products_done[0] >= MAX_PRODUCTS_PER_SESSION:
                print(f"\n⚠ Reached max products per session ({MAX_PRODUCTS_PER_SESSION})")
                break
            
            if api_calls[0] >= MAX_API_CALLS_PER_SESSION:
                print(f"\n⚠ Reached max API calls per session ({MAX_API_CALLS_PER_SESSION})")
                break
            
            print(f"\n[{i}/{len(docs)}] Progress: {products_done[0]} products, {api_calls[0]} API calls")
            
            # Process document
            current_country, api_calls, products_done, success = process_document(
                doc, page, current_country, api_calls, products_done
            )
        
        page.close()
        # Keep browser alive for next session
        print(f"\n✅ Session complete: {products_done[0]} products, {api_calls[0]} API calls")
    
    return products_done[0], api_calls[0]


# ===================== MAIN =====================
def main():
    """Main automation loop"""
    print(f"\n{'='*80}")
    print(f"🤖 VIATOR AUTOMATED SCRAPER")
    print(f"{'='*80}\n")
    print(f"📁 Save Directory: {save_dir}")
    print(f"🔧 Chrome Profile: {CHROME_PROFILE}")
    print(f"🌐 Chrome Port: {CHROME_PORT}\n")
    
    session_count = 0
    total_products = 0
    total_api_calls = 0
    
    while True:
        # Fetch pending documents from MongoDB
        docs = list(search_data.find({"Status": "Pending"}).limit(MAX_PRODUCTS_PER_SESSION * 3))
        
        if not docs:
            print("\n✅ All documents processed!")
            break
        
        print(f"\n📊 Found {len(docs)} pending documents")
        
        # Process batch
        session_count += 1
        print(f"\n{'='*80}")
        print(f"SESSION #{session_count}")
        print(f"{'='*80}")
        
        products, api_calls = run_session(docs)
        total_products += products
        total_api_calls += api_calls
        
        # Check if more documents to process
        remaining = search_data.count_documents({"Status": "Pending"})
        
        if remaining > 0:
            # Apply cooldown before next session
            cooldown = random.uniform(*SESSION_COOLDOWN)
            print(f"\n{'='*80}")
            print(f"⏸ COOLDOWN")
            print(f"{'='*80}")
            print(f"⏰ Cooling down for {cooldown/60:.1f} minutes before next session...")
            print(f"📊 Remaining documents: {remaining}")
            print(f"📈 Progress so far: {total_products} products, {total_api_calls} API calls\n")
            time.sleep(cooldown)
        else:
            break
    
    # Final summary
    print(f"\n{'='*80}")
    print(f"🎉 AUTOMATION COMPLETE")
    print(f"{'='*80}")
    print(f"✅ Total Sessions: {session_count}")
    print(f"✅ Total Products: {total_products}")
    print(f"✅ Total API Calls: {total_api_calls}")
    print(f"📁 Files saved to: {save_dir}\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n⚠ Interrupted by user")
    except Exception as e:
        print(f"\n\n❌ Fatal error: {e}")
        import traceback
        traceback.print_exc()
