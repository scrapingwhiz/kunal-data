import json
import os.path
import time
from concurrent.futures import ThreadPoolExecutor
from config_data import *
import requests
from parsel import Selector


def process_html_document(doc):
    """Process each document to fetch and save HTML content"""
    doc_id = doc['_id']
    referer_url = doc['URL']
    order_code = doc['Order Code']
    seasonality = str(doc['Seasonality'])
    competitor = doc['Competitor']
    sm = doc['SM']
    pax = int(doc['pax'])

    hashid = generate_hash_id(referer_url, order_code, seasonality, competitor, sm, pax)

    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36',
        # 'Cookie': 'x-viator-tapersistentcookie=ef446012-0a3b-417b-8ed2-6e3e4f942630; x-viator-tapersistentcookie-xs=ef446012-0a3b-417b-8ed2-6e3e4f942630; _gcl_au=1.1.388849303.1758025473; rskxRunCookie=0; rCookie=8zssai9remhcaw6ebaabiqmfmiz73c; _cc=AbPcIyRvk%2BFMm670ohTWVJOS; _cid_cc=AbPcIyRvk%2BFMm670ohTWVJOS; OptanonAlertBoxClosed=2025-09-16T12:24:53.026Z; lastRskxRun=1758105795337; SEM_PARAMS=%7B%7D; SEM_MCID=42384; EXTERNAL_SESSION_ID=; LAST_TOUCH_SEM_MCID=42384; XSRF-TOKEN=736e8b76-4c80-4368-acd7-bef847715de6; profilingBeaconSession=6V4HS8OI2kMeH5MoKvlYgA%253D%253D%257CDKWddXEV1DlE73Gms8iovGxQRDpAtj0jMceyYMUTdMpP7YMANn1c%252BA3S2p7EN2Ykd8hPEsWdMQ4%253D%257C5xDDAr50Gs8%253D%253AfiNwh1DhL2KiJXGn2n33sUc7B06Q7cBwhA4QRMxWEGI%253D; REFERER_PAGE_REQUEST_ID=9D345B1D:9342_0A2809E5:01BB_68DB6121_128BCC01:319863; ORION_SESSION=4QY4i%2Bl0CTnxbaiLd%2BgHAQ%3D%3D%7CpH95fnkvCCkuPQMa0tYAigHAIceoe5SaeNabzS6JtO%2FGkrpa9OjAfoUkhoWJkiDV8YEzPKYXUpM3T7lf3UNGghXV8K%2FdHNu6%2FtdvZU8Pt6gRiyaTPxzGgFTuTYTN2UQ5dqeXruCXTy8NjB%2B%2B2U5lMLIWFgXG2So4uUbWMLAFPULT9io6Ee%2FIeScv%2BGdbt1fOnjyDacLXuX5eS4gyg%2FPOzYsb6YvL6npSVvTgue%2BiwMY%2BtG2Vcg0Q7Bu73wFbe%2Bf1%2FAQMmJ4thMvYALRobxHOXmnpEoRnbnDk7zgiES68qXM8G%2BGz5vhCe7mts966M3VzAPjZd78ML5lLwwpV8HKiSpridcrjBantj0rZeLMnz2ZePuTEV7p%2Fcq9lZH%2Bh2CepTdgFxY7gLV%2B6lGGdth2DYXpmgiVTWMvyb%2F2eVjsJsUzJjQ0T50L6gdWlDG%2BWCfH%2FGUEG4nsQ0CBFG3bL9reTkcZ%2FxEdozxWrp5vdgkCxup38A5GJVXisF27RFXSnPj56wI1E64VC2yexSRxJZPtshyiKk1qyDCOa%2BDCb1qePc1goeVINNrOHUoDDz5mQqJJmVG6fzUSfdp6r%2F8axi%2FmnmQKphKQjTW9BA%2F0de3fRt8sTg7elAzHtW3qB%2BKk1k03xoKY0QSLGJiNMMHTrnreYm0v5vK4lCoFBOkz9PjATUnqEnvIRbfZxPvRDkj8TvYDoaCvcoq7%2FsRuEMTy3vYAEyYwRFK3jRH%2FXR6a2Vu8nDZJuB0bhea0q13nxyg89X09K%2BF8kX0rX%2Bn%2FqNOmyX3ds%2B1wR97KQeo%2F1V%2B1Rb3HY5uRUUyRj2CrO15rgOFJ5iPljgviCBE1LIhDAmKpg8nd%2BIoG9gvleDS8cMN17WVoqdbpfSKhXq9P1EHznps1hKiAh%2FgrpX6A6aoubisIxpiw9i1BdjX%2Bcvh%2BE83%2Fm299ImTTuyA6hRXqL7iheh89ogps9T207sBVfxLkxQhbSBzsLHpQ82uJVIbvN%2FLekKLYbdSRqqkDHHxyycObG7HtV5fOPpm%2FIct4KnFzNStgdH4%2BSJ8thegGRlMndpFU7vuJjbSVrQ5zZHgNPQ%2BDurFuv9YfdlLUbeBIRX1C5KUCkV9esXQSaMrikeDYzIEGfGd22zv2VMpz51YLaisBtQVtWS3X23TXvQGUB9m9tNFvDcuEWJP53gRGVtT2d35ioDT9rWKjTczxUmsHWsgDixp5%2FNFhzK2BEl9WShS6AMQkUtjiRGEu5rjaSBN%2FGp8%2FLBgEBs3IpXIdwNEJeh4OEw1P8lm0CEiYBCREYDWgyf9zBXHHKs3899eRd4y1rEezpccRyArdZvpqQ2CFVzhhI3NHcBaHWIxnxC0f8mJnDvJlC9esKSKm1lkUCxBuFLu6cq6U8eSedX1lNIrbZjHJPBouHdc5upiL0Kg9i0Fd0%2FXRtNJahnes%2BP53Qnx%2BYZ29jORDiNdxGnZftAtBl4k8SDg%2F6TBI7E8SS59Qgk7HKIDDX5lu0tuyVniUA5FD5s4rLkR7yPqBkOLghkVlbHbreFHcm%2BBan7UgiVA%2F%2FEBRrex74sBQNPnjfcooU51VsL70WwaDvaPCEkjLIvO%2FFUKPbxvTFw63Vw2XkVaGQJG1f47aEPFzty3BZdcHeNCwtYJrxnQAASvUi0Q1RJGzdoGAuGM5idx0%2FEK3d3LwtFhS9YOZho92Q9MLZ532T7cqtx6tbqdjA1fD0US%2BrxGLMqOyrhvW%2F9jJu%2FxvvS7%2FzdZp8CIhxGV%2By38hRtJfDTO00uxlj0XyyeY8KuXn0Rj7z5uWS%2B7xhzsCbAK3hvLSxAE6IZddDOvvRrqdklqA4C4BtIY9CPSZ6V5sY%2Bors1mOBpNXi%2BmExcGnNUw7n%2FuSjp%2Ft61ZqoBYepgKwHlz1KI2uZ5Y2zr%2Fbq8IP7%2BouvttC4ibq7sVT7N1ho6mijVS%2B5qH8TVhxaPXZJirL7irHG9FsiNCbalvF%2FRDcVN6eewp8nidZTCdv3lTmBXHLcF5Csfm1HxJRJT05VV%2BMYnrGZNKxqOM6dfL9jTCHunpgdNjrO2lU51e%2F49y16LUtwop8LD6oVc9fhAjHYXBgX5FyJ4FY0QJTMsRzLXZpjE4g%2FTTPbzD6JkFpStZHnL9rVZbEjUl4pnXl%2FhxKEO%2BMZRDaxgv%2FRnr0u9CffVxBQPnyyvZuLlLmcdOMbH9NR7kzrI8LeW9rYk8JSeJOXlXn5KyUROpkY9g8sGtiS6kJJIUGM28jaYMZLKrPMuadys2azvI5pTKPryuZZpMrTXlZwZB%2BQ82exvfpThh9g8cf0sJyt6%2F4hKLgUmGPcjSmpDdhU3w%2Fy8uiFxPKfz6ZS91KvKP59xJn%2FUjTAXsFm%7CR6SKR%2Fk6gEI%3D%3AedF6ys%2FD3ZidkiPw2PvfKhu7trYdtjANZGoMcHG5m1c%3D; OptanonConsent=isGpcEnabled=0&datestamp=Tue+Sep+30+2025+10%3A18%3A40+GMT%2B0530+(India+Standard+Time)&version=202402.1.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=40e49110-a00b-4267-a4cf-a4407571abd5&interactionCount=2&isAnonUser=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0003%3A0%2CC0004%3A0%2CC0002%3A0&geolocation=IN%3BGJ&AwaitingReconsent=false; ORION_SESSION_REQ=9D345B1B%3ACE45_0A2806EB%3A01BB_68DB6129_128D4B7B%3A33C7BF%7C9D345B1D%3A9342_0A2809E5%3A01BB_68DB6121_128BCC01%3A319863%7C9D345B1D%3A9342_0A2809E5%3A01BB_68DB6121_128BCC01%3A319863; profilingInAuthSession=jgpm4llu7Qau5r4KWWnb6w%253D%253D%257CwRwOP9Ny63U6pwNlc6F9C4MNUPyLZ0cDfFxmDSn68O%252B01Z2c2X8xYUn1kVyWLEml6gYvnIFYk%252Ft5TZC45mgFMugs6sNq4Z7TPLUkUXwKrINOWNXDgA%253D%253D%257CvV88TsZGBgc%253D%253Ay78t1g1rVoMq6CONtiLjQ5ZtADRnOBR40KczUYXXqck%253D; datadome=KONv3AggbsDZNmHP08vvHj7gitU3ENNrFfBYuNoZmkrIiOPWxanD0gTIlCXiKbQuG80Yx5pSR9J0vNDF8eoUKi~C3CjTIjwzZrA2VEEg2orDfAM2_2gBxpOzE0is4hmQ; datadome=1B1cN__yXy1jA9DSlBubFpVt9H91VvQF3FWeIi~gE6i7p1vbU~RovgRPs0HeAuEUgE6XKKxcxkyTqip_WxLZrUlqsOniGf5lkVkI98nHobKo7_R2qIXE~aST3MlaD9hU; LAST_TOUCH_SEM_MCID=42384; ORION_SESSION=OrRAxkaNAccuR9rqxXNXng%3D%3D%7CksWnjl4VGw1Eve%2Fa9rwVVi6DwU9UJuztYAHLCIvLKgUWt84qi46aabTlaorDDdCOFePR8MF88d3%2FGbcnFJRaP39UaKKS9Qx0LotSfKo9X9tKaF0NUlbjb%2FjdplSKD%2FD02YLRJmtaDxtlSNfcQohbFuBcGlNhAba%2FdxQtZoNwS7vfL9xWwLlGz1VzWmBueWZjeYIuBvn8HJMUEvgVgne%2BSjcP1oZShD0ICXGW1hgxM5%2FFwCsp1mmMEyg9GPMoVCXVJqjHewzSyV3GFxgUrDa%2Fm0QPZHpZ2BQ%2BvavsTnq1kqip6EHWeT0ukAE8Gx2Cp9t7jWNVbgKh%2BpmrNQYmeE2gCJK9EPpAqwTcpDF39xU%2BBly4cu04gSvX0uMLcI7gkjbF%2FQTsN9nkRcSsDBUZw3AImWj2iVuQrCahS4jcY2HbLDaXtzVS2CgTgAeESgvFvwd8CSqT7yYBT3ICj5ElMoDGhvVXRv5RvujIRRXPmW6m%2FfsGhDQkC6lXz3uRgzZm3a1wUbT175OC%2B%2FYtEnnpEJAkiWJ6iVUhs7aspHg5lRqIwNDQgeopb6Eemwd0YMbXnL%2FVLPpL3k2lmd8u%2FCkzjU7%2BwSaxJieAhbM8vAqU6QnQrSxpiA6CF5n1fkyrRQRvYzYLfxHxWdQEEkFCqIfBwbBpsV%2B6wK2%2FlsyqWyxbf%2Bmc8gRmTlOgUMuyBnSWFL77jUp2hwzUPHfT%2Bh9GydNjqisGN5HzK0FApPH6jfIW14WPyoC2Kal94kqSmCa%2BYLQQRNJfZEXQE8aMrNnv7OYqsPWldXUL3bQQhKVtjfppbWcjzcIBmCxStr0UulPjRszsfNhI8jzTRwhjVP9g%2FNFXYMTyk1ftU22LML%2FTM%2BO831gY5uuhd1w2eqUanPRHzpT1nkzwmTRQTwuAF9Ua2u1H8uhwGc7UFkwrhGkGLnsWywtCrkUGQkiCdwjlVQYftiJPw8SMNjWcUvYrbtocgYeNJe9%2B0jVZvXpdGTd4P%2BwE9Ap%2FVgVEe15pwyIiLcLaXfdiXOp7%2BeV1TR%2BgbzxtyohoucjMG%2FIo%2FXNdBnQlV%2FUeS1ABXHkdoDMA6n5VDbs4J9dNZQKjKbQUBq%2FBrsPEruI%2FnpLd8cBQqaVt1liuq%2FZbPgNW%2B71YcEpE2cuNtUHyEXeuLO1ePHEJs3VVqmEYA%2BCcNRUfsReC%2BulTnLwHpTB6xNhoqmdeUZ6CkkC0Ip1Tc%2BclN41yvlahZSGul9VxgxStFc3BXOYjoafClg4q4LuBSvq2V9GfgkqbDYQQWLvGZh2GCOIGzybNUGrsf89U3eRVYdLO5TuOIBMoR3X1sRYrSohpgCutNpHPFjTON4RMjLPnZkKGpsYTpYGztJcjblCCaydrvGBIStzz%2B7lYzt4lgoLDb6Td4%2FBELbbDAudr5ucFOP4N47EVzT5TyMjMcX7MUcuZpe5OFMSeQdLW4Nronzz8lcbP7PofybvMmxtk3u0ig5CWT0k%2F6Mp9rrs7HhXkK3muHyTaD6N7BlxDSYwOCD6mhMeORIrMEUS7u0NlrPpJZ4hkRTubtHuUDfF67ZQGbh%2BBvo8JpkGcBCrG0lmwNvgPizVOmJp2NFhtC6nk57fU%2BdidU516QLmWPzNIOZsc9kHO112bcmpV5NLdSv%2Blz019M5uv15dqOkjiMl0yiSHWneQ4HDUNZ1zRK%2B8H2sS48FC2%2BWifAy3VqEqcTAkcZgQqBRQl0hXGDLfLv8OpyTQoWBgrSRN58HK1ejbrF9yLAzjxQXS9IfkB0ocyQTh5y6cml%2FacaqVQbnakpTduwSsE2ltx%2BNf5sB%2FHiWwoqt2RREQAjrFd68rFjAgm%2ByJdhhp5KJJD0CqYaq568EL9QBUXLTQdT7JWqxE9mxqhw%2FA74qS9XVdDDtCSmt4O8Yik4nmRm%2FRsoiHckcmFBIq6Ke%2FBkFiKuZvY7eg6qhVVjJnJISWyof7vpz%2FC%2BRglR0PmTzZLB8LXhZwW0sLpXV2x45Qh8BGmPzUBQm81e%2Fvmoqfn8%2B2UjSC5O7zN6t0EG5U1m%2BV4Jx6MYrSeKqfWXCNKx9RwUKemPdvg5BqpOAqJeFu42vt9D9XbCe8WDCryrmlSr4bkjZdLtzhMY84H24vGTA1FksQjXBD7emIB7W6LnNxlRdrBWhW2jkYKNCZ1YvCk0zrKuQbxYtgA%2FyZveNBrryQzDy1%2FSJOr8cNvpa7PiKlsH6CP4MJhXgtd1oiOrSl7Je8z5RdMxLhIljtQ0wQEXNxpXV3xaqrzYQP5A5esmgAU6vMo1gQppbKZEN9H6CmRVIUzAdqrxkSwLsOutdCuwY2kXESnInAWrTG7mos42zof%2BSW3UQN0VYAa%2BZ%2BbKje1iJjtNg%3D%3D%7C%2BpUjq4eRwdQ%3D%3AuSyDJflinQNr6KDFIjStq35LE%2Bf5TuWzcQ26Aq6sBAM%3D; ORION_SESSION_REQ=9D345B1D%3AB1A1_0A2809E5%3A01BB_68DB619F_128C4F16%3A319863%7C9D345B1D%3A9342_0A2809E5%3A01BB_68DB6121_128BCC01%3A319863%7C9D345B1D%3AB1A1_0A2809E5%3A01BB_68DB619F_128C4F16%3A319863; x-viator-tapersistentcookie=ef446012-0a3b-417b-8ed2-6e3e4f942630'
    }

    region = "us"
    zenrows_res_proxies = {
        'http': f'http://3dbxcTLYpHGv:YF67LxHnCPRwc57_country-{region.lower()}@superproxy.zenrows.com:1337',
        'https': f'http://3dbxcTLYpHGv:YF67LxHnCPRwc57_country-{region.lower()}@superproxy.zenrows.com:1337',
    }

    file_name = f"{hashid}.html"
    file_path = os.path.join(save_dir, file_name)

    # Check if HTML file already exists
    if os.path.exists(file_path):
        print(f"HTML file already exists: {file_path}")
        search_data.update_one({"_id": doc_id}, {"$set": {"Status": "Pending"}})
        return

    # Fetch HTML content
    for attempt in range(5):
        try:
            response = requests.get(
                referer_url,
                proxies=proxies,
                verify=False,
                headers=headers,
                # cookies=cookies,
                # timeout=30
            )

            print(f"HTML Response Status: {response.status_code} for {referer_url}")

            if response.status_code == 200 or response.status_code == 404:
                html_content = response.text

                # Save HTML file
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(html_content)
                print(f"Saved HTML for {order_code} -> {file_path}")

                # Check if page is unavailable or not found
                res = Selector(text=html_content)
                service_name = res.xpath('//h1[@data-automation="product-title"]/text()').get()
                if not service_name:
                    service_name = res.xpath('//h2[@data-automation="product-title"]/text()').get()

                if '>Sorry, this product is unavailable<' in html_content or '>404 Not Found | Viator<' in html_content:
                    print(f"Product unavailable or not found: {referer_url}")
                    search_data.update_one({"_id": doc_id}, {"$set": {"Status": "Pending"}})
                else:
                    search_data.update_one({"_id": doc_id}, {"$set": {"Status": "Pending"}})

                break
            else:
                print(f"Attempt {attempt + 1}/5 failed with status {response.status_code}")
                time.sleep(3)

        except Exception as e:
            print(f"Error fetching HTML for {referer_url}: {e}")
            time.sleep(3)
    else:
        print(f"Failed to fetch HTML after 5 attempts: {referer_url}")
        search_data.update_one({"_id": doc_id}, {"$set": {"Status": "Pending"}})


def main_html():
    """Main function to process all pending HTML requests"""
    with ThreadPoolExecutor(max_workers=50) as executor:
        docs = list(search_data.find({"Status": "Pending"}))
        executor.map(process_html_document, docs)


if __name__ == "__main__":
    Max_Retries = 100

    while Max_Retries > 0:
        Max_Retries -= 1
        total_pending = search_data.count_documents({"Status": "Pending"})
        total_failed = search_data.count_documents({"Status": "Pending"})
        print(search_data)

        print(f"Total Pending HTML: {total_pending}")
        print(f"Total Failed HTML: {total_failed}")

        if not total_pending and not total_failed:
            print("All HTML requests completed!")
            break

        # Retry failed requests
        if total_failed > 0:
            search_data.update_many({"Status": "Pending"}, {"$set": {"Status": "Pending"}})

        main_html()
        break
        time.sleep(2)

    print("HTML scraping process completed!")