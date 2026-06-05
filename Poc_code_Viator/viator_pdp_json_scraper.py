import json
import os.path
import re
import time
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime, timedelta, date

from config_data import *
import requests
from parsel import Selector


def api_request(json_file_path, orion_session, zenrows_res_proxies, doc_id, season_date, prod_code, pax):
    """Make API request to fetch product availability data"""

    print(f"Making API request for date: {season_date}")

    json_data = {
        'productCode': f'{prod_code}',
        'searchDate': f'{season_date}',
        'ageBands': {
            'ADULT': f'{pax}',
        },
    }

    cookies = {
        'x-viator-tapersistentcookie': '12785ace-030c-4129-986b-62100de95416',
        'x-viator-tapersistentcookie-xs': '12785ace-030c-4129-986b-62100de95416',
        'rskxRunCookie': '0',
        'rCookie': 'rvt2h4lq5y9oi7o2ifr5lmfdrabfw',
        '_cc': 'AaMB9A4p%2F5B%2F9LEv0TnDdVup',
        '_cid_cc': 'AaMB9A4p%2F5B%2F9LEv0TnDdVup',
        '_gcl_au': '1.1.1842782717.1757495240',
        'OptanonAlertBoxClosed': '2025-09-10T09:07:52.203Z',
        'ORION_WISHLIST_INTERACTED': '',
        'SEM_PARAMS': '%7B%7D',
        'SEM_MCID': '42384',
        'EXTERNAL_SESSION_ID': '',
        'LAST_TOUCH_SEM_MCID': '42384',
        'XSRF-TOKEN': '108aab90-847a-4edb-9e8c-a867e319bbcd',
        'ORION_SESSION': orion_session,
    }

    headers = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9,hi;q=0.8',
        'content-type': 'application/json',
        'origin': 'https://www.viator.com',
        'priority': 'u=1, i',
        'referer': 'https://www.viator.com/',
        'sec-ch-device-memory': '8',
        'sec-ch-ua': '"Chromium";v="142", "Google Chrome";v="142", "Not_A Brand";v="99"',
        'sec-ch-ua-arch': '"x86"',
        'sec-ch-ua-full-version-list': '"Chromium";v="142.0.7444.134", "Google Chrome";v="142.0.7444.134", "Not_A Brand";v="99.0.0.0"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-model': '""',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/142.0.0.0 Safari/537.36',
        'x-frontend-date-validation': 'true',
        'x-requested-with': 'XMLHttpRequest',
        'x-xsrf-token': '108aab90-847a-4edb-9e8c-a867e319bbcd',
    }

    for attempt in range(5):
        try:
            resp = requests.post(
                'https://www.viator.com/orion/ajax/product-availability',
                cookies=cookies,
                headers=headers,
                json=json_data,
                proxies=zenrows_res_proxies,
                verify=False,
                timeout=30
            )

            print(f"API Response Status: {resp.status_code}")

            if resp.status_code == 200:
                address_main_response_body = resp.text

                if 'OUT_OF_AGE_RANGE' in address_main_response_body:
                    search_data.update_one({"_id": doc_id}, {"$set": {"Status": "Not Found"}})
                    return None

                # Save JSON response
                with open(json_file_path, "w", encoding="utf-8") as f:
                    f.write(address_main_response_body)

                print(f"API request successful, saved to {json_file_path}")
                return address_main_response_body
            else:
                print(f"Attempt {attempt + 1}/5 failed with status {resp.status_code}")
                time.sleep(2)

        except Exception as e:
            print(f"API request error: {e}")
            time.sleep(2)

    return None


def process_api_document(doc):
    """Process documents that have HTML downloaded to fetch API data"""
    doc_id = doc['_id']
    referer_url = doc['URL']
    order_code = doc['Order Code']
    seasonality = str(doc['Seasonality'])
    competitor = doc['Competitor']
    sm = doc['SM']
    pax = int(doc['pax'])

    hashid = generate_hash_id(referer_url, order_code, seasonality, competitor, sm, pax)

    file_name = f"{hashid}.html"
    file_path = os.path.join(save_dir, file_name)

    # Check if HTML file exists
    if not os.path.exists(file_path):
        print(f"HTML file not found: {file_path}")
        return

    # Read HTML content
    with open(file_path, "r", encoding="utf-8") as f:
        html_content = f.read()

    res = Selector(text=html_content)

    # Extract basic info
    service_name = res.xpath('//h1[@data-automation="product-title"]/text()').get()
    if not service_name:
        service_name = res.xpath('//h2[@data-automation="product-title"]/text()').get()

    service_code = res.xpath('//meta[@name="productCode"]/@content').get()
    company = res.xpath('//meta[@property="og:site_name"]/@content').get()
    duration = res.xpath('//span[@class="label__Tm23"]//text()').get()
    cancellation = res.xpath('//div[@class="policyDescription__oAOW"]//text()').get()
    Supplier_name = res.xpath('//button[@class="supplierDetailsLink__Yfk7"]/text()').get()
    review_data = res.xpath('//div[@class="rating__jScz"]/text()').get()
    mobile_data = res.xpath("//span[@class='label__Tm23' and normalize-space(text())='Mobile ticket']//text()").get()
    review_text = res.xpath('//div[@class="reviewCount__Bmi3"]/text()').get()

    # Extract review number
    review_number = ""
    if review_text:
        match = re.search(r'[\d,]+', review_text)
        if match:
            review_number = match.group()

    # Extract languages
    script_text = res.xpath('//script[@id="globalState"]/text()').get()
    primary_language = ""
    offered_languages_str = ""

    if script_text:
        try:
            data = json.loads(script_text.strip())
            product_languages = (
                data.get("__PRELOADED_DATA__", {})
                .get("pageModel", {})
                .get("product", {})
                .get("productLanguages", {})
            )
            primary_language = product_languages.get("primaryLanguage", "")
            offered_languages = product_languages.get("offeredLanguages", [])
            offered_languages_str = ", ".join(offered_languages)
        except Exception as e:
            print(f"Error parsing globalState JSON: {e}")

    if not review_data:
        review_data = res.xpath('//span[@class="averageRatingValue__cWuj"]/text()').get()

    review = f"{review_data} / 5" if review_data else ""

    # Pick up info
    pick_up_innfo = ""
    pick_info = "excluded"
    picking = res.xpath("//span[@class='label__Tm23' and text()='Pickup offered']//text()").get()
    if picking:
        try:
            pick_up_innfo = res.xpath(
                "//li[contains(@class,'feature__W54X')]//div/div[contains(text(),'Pickup')]//text()"
            ).get() or ""
        except Exception as e:
            print(e)
        pick_info = "included"

    # Meals info
    title_blocks = res.xpath('//div[@class="title__uQE0"]')
    data_for_meals = res.xpath('//script[@id="globalState"]/text()').get()
    meal_keywords = ["meal", "meals", "food", "foods", "drink", "drinks", "lunch", "dinner", "breakfast"]
    meal_info = "Included"

    if data_for_meals:
        try:
            parsed = json.loads(data_for_meals)
            exclusions = (
                parsed.get("__PRELOADED_DATA__", {})
                .get("pageModel", {})
                .get("product", {})
                .get("description", {})
                .get("exclusions", {})
                .get("features", [])
            )
            if exclusions:
                exclusions_str = " ".join(exclusions).lower()
                if any(word in exclusions_str for word in meal_keywords) or "food & drinks" in exclusions_str:
                    meal_info = "Excluded"
        except Exception as e:
            print(f"Meals parse error: {e}")

    # Guide info
    guide_info = "Excluded"
    for block in title_blocks:
        text = block.xpath('./div/text()').get()
        if text:
            text_lower = text.lower()
            if any(k in text_lower for k in meal_keywords):
                meal_info = "Included"
            if "guide" in text_lower or "driver/guide" in text_lower:
                guide_info = "Included"
            if guide_info == "Included":
                break

    guide_extrac = ""
    if guide_info == "Included":
        guide_extrac = res.xpath(
            '//div[@class="title__uQE0"][contains(translate(.,"GUIDE","guide"), "guide")]//text()'
        ).get() or ""

    # Transfer info
    transfer = res.xpath('//div[@class="title__uQE0"][contains(translate(.,"Transportation","Transportation"), "Transportation")]//text()').get()
    transoption = "Included" if transfer else "Excluded"

    # Product code
    product_code = res.xpath('//p[@data-automation="product-code"]/text()').get()
    prod_code = product_code.split(":")[-1].replace(" ", "") if product_code else service_code

    # Get customer market and ORION_SESSION
    custommer_market = customer_market_reverse_dict.get(sm)
    if not custommer_market:
        raise ValueError(f"No customer market defined for country code '{sm}'")

    orion_session = orion_sessions.get(sm)
    if not orion_session:
        raise ValueError(f"No ORION_SESSION defined for country code '{sm}'")

    # Prepare API request
    region = "us"
    zenrows_res_proxies = {
        'http': f'http://3dbxcTLYpHGv:YF67LxHnCPRwc57_country-{region.lower()}@superproxy.zenrows.com:1337',
        'https': f'http://3dbxcTLYpHGv:YF67LxHnCPRwc57_country-{region.lower()}@superproxy.zenrows.com:1337',
    }

    season_date = convert_to_standard_date(seasonality)
    json_file_name = f"{hashid}.json"
    json_file_path = os.path.join(save_dir, json_file_name)

    # Check if JSON already exists
    if os.path.exists(json_file_path):
        with open(json_file_path, "r", encoding="utf-8") as f:
            json_response = f.read()
    else:
        json_response = api_request(json_file_path, orion_session, zenrows_res_proxies, doc_id, season_date, prod_code, pax)
        if not json_response:
            print("Failed to get API response")
            search_data.update_one({"_id": doc_id}, {"$set": {"Status": "API_Failed"}})
            return

    # Parse availability data
    try:
        availability_data = json.loads(json_response)
    except Exception as e:
        print(f"Error parsing JSON: {e}")
        os.remove(json_file_path)
        search_data.update_one({"_id": doc_id}, {"$set": {"Status": "API_Failed"}})
        return

    tourGrades_data = availability_data.get("productAvailability", {}).get("tourGrades", [])

    # Retry with different dates if no data
    if not tourGrades_data:
        days_plus = 1
        max_retry_days = 7
        found = False
        season_date_obj = datetime.strptime(season_date, "%Y-%m-%d")

        while days_plus <= max_retry_days:
            new_season_date = season_date_obj + timedelta(days=days_plus)
            season_date = new_season_date.strftime("%Y-%m-%d")
            print(f"Retrying with date: {season_date} (Day +{days_plus})")

            json_response = api_request(json_file_path, orion_session, zenrows_res_proxies, doc_id, season_date, prod_code, pax)

            if not json_response:
                print(f"No response for day +{days_plus}")
                days_plus += 1
                continue

            availability_data = json.loads(json_response)
            tourGrades_data = availability_data.get("productAvailability", {}).get("tourGrades", [])

            if tourGrades_data:
                found = True
                print(f"Found tourGrades data on day +{days_plus}")
                break

            days_plus += 1

        if not found:
            print("tourGrades data not found even after 7 days retry")
            search_data.update_one({"_id": doc_id}, {"$set": {"Status": "Not Found"}})
            return

    # Calculate dates
    if isinstance(today_date, str):
        search_date = datetime.strptime(today_date, "%Y-%m-%d")
    elif isinstance(today_date, date):
        search_date = datetime.combine(today_date, datetime.min.time())
    else:
        search_date = today_date

    date_obj = search_date
    calendar_week = date_obj.isocalendar()[1] - 1

    # Process and insert data
    for tg in tourGrades_data:
        title_name_mode = tg.get("title")
        modality_code = tg.get("tourGradeCode", "").split("~")[0]
        pickup_point = tg.get("title", "")
        main_date = tg.get("date", "")
        availability = tg.get("availability", "")

        if availability == "UNAVAILABLE":
            search_data.update_one({"_id": doc_id}, {"$set": {"Status": "Not Found"}})
            return

        start_times = tg.get("startTimes", [])
        if not start_times:
            start_times = [{}]

        for st in start_times:
            start_time = st.get("startTime", "") or st.get("startTime24H", "")

            # Extract price
            variant_price = (
                    st.get("price", {}).get("retailPrice", {}).get("amount", "")
                    or st.get("price", {}).get("discountedPrice", {}).get("amount", "")
            )
            cueency_code = (
                    st.get("price", {}).get("retailPrice", {}).get("currencyCode", "")
                    or st.get("price", {}).get("discountedPrice", {}).get("currencyCode", "")
            )

            if not variant_price:
                variant_price = (
                        st.get("totalPrice", {}).get("retailPrice", {}).get("amount", "")
                        or st.get("totalPrice", {}).get("discountedPrice", {}).get("amount", "")
                )
                cueency_code = (
                        st.get("totalPrice", {}).get("retailPrice", {}).get("currencyCode", "")
                        or st.get("totalPrice", {}).get("discountedPrice", {}).get("currencyCode", "")
                )

            if not variant_price:
                for pb in tg.get("priceBreakdown", []):
                    variant_price = (
                            pb.get("totalPrice", {}).get("retailPrice", {}).get("amount", "")
                            or pb.get("price", {}).get("retailPrice", {}).get("amount", "")
                    )
                    cueency_code = (
                            pb.get("totalPrice", {}).get("retailPrice", {}).get("currencyCode", "")
                            or pb.get("price", {}).get("retailPrice", {}).get("currencyCode", "")
                    )
                    if variant_price:
                        break

            if not variant_price:
                print(f"⚠️ Skipping {start_time} - No price found")
                continue

            # Calculate booking days
            if "T" in season_date:
                season_dt = datetime.fromisoformat(season_date.split("Z")[0].replace("+00:00", ""))
            else:
                season_dt = datetime.strptime(season_date, "%Y-%m-%d")

            booking_days = (season_dt.date() - search_date.date()).days
            booking = f"{booking_days} Days"

            modality_name = f"{title_name_mode}_{start_time}" if start_time else title_name_mode

            hash_id = generate_hash_id(start_time, season_date, service_code, Supplier_name, modality_name, order_code, custommer_market, referer_url, variant_price)

            # Prepare data for insertion
            list_main = {
                "hash_id": hash_id,
                "htmlpath": file_path,
                "josn_file_path": json_file_path,
                "Modality Name": modality_name,
                "Review": review_number,
                "Region": "",
                "Destination Code": "",
                "Destination": "",
                "Supplier": Supplier_name,
                "Service Name": service_name,
                "Service code": service_code,
                "Modality Order": "",
                "Mobile Data Information": mobile_data,
                "Cancelaciones": cancellation,
                "Currency": cueency_code,
                "Pick up point- extracted info": pick_up_innfo,
                "Meals : included/ excluded": meal_info,
                "Duration": duration,
                "Available Arrival date": "",
                "Order": order_code,
                "Calender Week": calendar_week,
                "opiniones": review,
                "Links": referer_url,
                "Scope": "",
                "Pick up point- options": pick_info,
                "Booking in advance": booking,
                "Search date": search_date,
                "Arrival date": season_date,
                "Price": variant_price,
                "Assistance/guided": guide_info,
                "End Time": "",
                "Segmentation-duration": "",
                "Min pax": pax,
                "Drop off -options": "",
                "Drop off -extracted info": "",
                "Transfers - options": transoption,
                "Company": company,
                "Assistance/guided-extracted info": guide_extrac,
                "Language -extracted info": offered_languages_str,
                "Promotion Description": "",
                "Deliverable Date": search_date,
                "Promotion": "",
                "Modality Code": modality_code,
                "Modality Availability": "",
                "Tool Tip": "",
                "Contractor": "",
                "Product Line": "",
                "Customer Market Key": sm,
                "Meals - extracted info": "",
                "Customer Market": custommer_market,
                "Contract Info": "",
                "Incomming Office Code": "",
                "Transfers- extracted info": transfer,
                "Start Time": start_time,
            }

            try:
                product_data.insert_one(list_main)
                print(f"✓ Inserted: {pickup_point} | {start_time} | {variant_price}")
            except Exception as e:
                if 'duplicate key error collection' in str(e):
                    print(f"⚠ Duplicate: {pickup_point} | {start_time} | {variant_price}")
                else:
                    print(f"Error inserting data: {e}")

    # Mark as Done after successful processing
    search_data.update_one({"_id": doc_id}, {"$set": {"Status": "Done"}})
    print(f"✓ Completed processing for Order: {order_code}")


def main_api():
    """Main function to process all HTML_Done documents"""
    with ThreadPoolExecutor(max_workers=20) as executor:
        docs = list(search_data.find({"Status": "HTML_Done"}))
        executor.map(process_api_document, docs)


if __name__ == "__main__":
    Max_Retries = 100

    while Max_Retries > 0:
        Max_Retries -= 1
        total_html_done = search_data.count_documents({"Status": "HTML_Done"})
        total_api_failed = search_data.count_documents({"Status": "API_Failed"})

        print(f"Total HTML_Done: {total_html_done}")
        print(f"Total API_Failed: {total_api_failed}")

        if not total_html_done and not total_api_failed:
            print("All API requests completed!")
            break

        # Retry failed API requests
        if total_api_failed > 0:
            search_data.update_many({"Status": "API_Failed"}, {"$set": {"Status": "HTML_Done"}})

        main_api()
        time.sleep(2)

    print("API scraping process completed!")

    # Print final statistics
    total_done = search_data.count_documents({"Status": "Done"})
    total_not_found = search_data.count_documents({"Status": "Not Found"})
    print(f"\n=== Final Statistics ===")
    print(f"Successfully processed: {total_done}")
    print(f"Not found: {total_not_found}")