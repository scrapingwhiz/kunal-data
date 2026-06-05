from playwright.sync_api import sync_playwright
import requests
import json


def get_fresh_cookies():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        # Use a real browser context so DataDome doesn't fingerprint you
        context = browser.new_context(
            user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        )
        page = context.new_page()

        # Visit the actual product page to trigger cookie generation
        page.goto(
            "https://www.viator.com/tours/Las-Vegas/Grand-Canyon-Helicopter-Tour-from-Las-Vegas-with-Champagne-Picnic/d684-6613GRANDCELE")
        page.wait_for_load_state("networkidle")

        cookies = context.cookies()
        cookie_dict = {c["name"]: c["value"] for c in cookies}
        browser.close()
        return cookie_dict


def check_availability(cookies):
    # Extract only the minimum needed
    headers = {
        "Content-Type": "application/json",
        "X-Requested-With": "XMLHttpRequest",
        "X-XSRF-TOKEN": cookies.get("XSRF-TOKEN", ""),
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
        "Referer": "https://www.viator.com/tours/Las-Vegas/Grand-Canyon-Helicopter-Tour-from-Las-Vegas-with-Champagne-Picnic/d684-6613GRANDCELE",
    }

    cookie_str = "; ".join([
        f"datadome={cookies['datadome']}",
        f"XSRF-TOKEN={cookies['XSRF-TOKEN']}",
        f"ORION_SESSION={cookies['ORION_SESSION']}",
        f"x-viator-tapersistentcookie={cookies.get('x-viator-tapersistentcookie', '')}",
    ])
    headers["Cookie"] = cookie_str

    payload = {
        "productCode": "6613GRANDCELE",
        "searchDate": "2026-06-01",
        "ageBands": {"ADULT": "2"}
    }

    response = requests.post(
        "https://www.viator.com/orion/ajax/product-availability",
        headers=headers,
        json=payload
    )
    return response.json()


# Refresh cookies every ~4 minutes
import time

cookies = get_fresh_cookies()
while True:
    result = check_availability(cookies)
    print(result)
    time.sleep(240)  # 4 min
    cookies = get_fresh_cookies()  # re-acquire before expiry
