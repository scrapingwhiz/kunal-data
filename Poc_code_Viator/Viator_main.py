import json
import os.path
import re
import time
import urllib.parse
from base64 import b64decode
from concurrent.futures import ThreadPoolExecutor

from Export_File import Export_File
from config_data import *
import requests
from datetime import datetime
from parsel import Selector

def api_request(josn_file_path, orion_session, zenrows_res_proxies, doc_id, season_date, prod_code, pax):
    # json_data = {
    #     'productCode': '29537P33',
    #     'searchDate': '2025-10-15',
    #     'ageBands': {
    #         'ADULT': '2',
    #     },
    # }
    print(season_date)
    json_data = {
        'productCode': f'{prod_code}',
        'searchDate': f'{season_date}',
        'ageBands': {
            'ADULT': f'{pax}',
        },
    }
    cookies1 = {
        'x-viator-tapersistentcookie': 'ef446012-0a3b-417b-8ed2-6e3e4f942630',
        'x-viator-tapersistentcookie-xs': 'ef446012-0a3b-417b-8ed2-6e3e4f942630',
        '_gcl_au': '1.1.388849303.1758025473',
        'rskxRunCookie': '0',
        'rCookie': '8zssai9remhcaw6ebaabiqmfmiz73c',
        '_cc': 'AbPcIyRvk%2BFMm670ohTWVJOS',
        '_cid_cc': 'AbPcIyRvk%2BFMm670ohTWVJOS',
        'OptanonAlertBoxClosed': '2025-09-16T12:24:53.026Z',
        'SEM_PARAMS': '%7B%7D',
        'SEM_MCID': '42384',
        'EXTERNAL_SESSION_ID': '',
        'LAST_TOUCH_SEM_MCID': '42384',
        'XSRF-TOKEN': '736e8b76-4c80-4368-acd7-bef847715de6',
        'profilingBeaconSession': '6V4HS8OI2kMeH5MoKvlYgA%253D%253D%257CDKWddXEV1DlE73Gms8iovGxQRDpAtj0jMceyYMUTdMpP7YMANn1c%252BA3S2p7EN2Ykd8hPEsWdMQ4%253D%257C5xDDAr50Gs8%253D%253AfiNwh1DhL2KiJXGn2n33sUc7B06Q7cBwhA4QRMxWEGI%253D',
        'ORION_SESSION': orion_session,
        'REFERER_PAGE_REQUEST_ID': '9D347B1D:2252_0A280747:01BB_68DB6612_12B1CB7D:2B6E9A',
        'OptanonConsent': 'isGpcEnabled=0&datestamp=Tue+Sep+30+2025+10%3A40%3A39+GMT%2B0530+(India+Standard+Time)&version=202402.1.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=40e49110-a00b-4267-a4cf-a4407571abd5&interactionCount=2&isAnonUser=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0003%3A0%2CC0004%3A0%2CC0002%3A0&geolocation=IN%3BGJ&AwaitingReconsent=false',
        'lastRskxRun': '1759209041480',
        'ORION_SESSION_REQ': '9D347B2C%3A33D0_0A280747%3A01BB_68DB664F_12B1D33F%3A2B6E9A%7C9D347B1D%3A2252_0A280747%3A01BB_68DB6612_12B1CB7D%3A2B6E9A%7C9D347B1D%3A2252_0A280747%3A01BB_68DB6612_12B1CB7D%3A2B6E9A',
        'profilingInAuthSession': 'V5rhUUrgSvOzl8DVDFuNIw%253D%253D%257CT4zm2buNOvY3c6s2vr5eDXgkCQ4NOC9HJZE7%252BpJxqEfAr%252FKJ%252FTON4NAY2tgH0rLWK1xsLKW0HIt2Ug5wU%252F35b37flytwYY3u3p3jO2SX%252B0RlbfVAMA%253D%253D%257CKf1W4XesXMw%253D%253AjQNZbl8eWBWFY9iTZoAHalg238Lda1JJLrD1qqIFZF4%253D',
        'datadome': 'DRLaa9ZCILce70fF43rWZ4z~dtCRSxPratMPaO7MKYg5gxaKP2rAnQqGvjJgbc1FOW2x4pnEFGXOSFJNSusyE62lX1p7CzmIocquki4J503btmiphDVdtDtpodXc3p~J',
    }

    headers1 = {
        'accept': 'application/json, text/plain, */*',
        'accept-language': 'en-US,en;q=0.9',
        'content-type': 'application/json',
        'origin': 'https://www.viator.com',
        'priority': 'u=1, i',
        'referer': 'https://www.viator.com/tours/Playa-del-Carmen/Coba-Tulum-Ruins-Cenote-and-Tulum-Beach-from-Cancun/d5501-29537P33',
        'sec-ch-ua': '"Chromium";v="140", "Not=A?Brand";v="24", "Google Chrome";v="140"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'empty',
        'sec-fetch-mode': 'cors',
        'sec-fetch-site': 'same-origin',
        'traceparent': '00-b22691196cf6c56fae8a605d855af3a5-3da4bdfbbce24cab-01',
        'tracestate': 'es=s:0.1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36',
        'x-datadome-clientid': 'DRLaa9ZCILce70fF43rWZ4z~dtCRSxPratMPaO7MKYg5gxaKP2rAnQqGvjJgbc1FOW2x4pnEFGXOSFJNSusyE62lX1p7CzmIocquki4J503btmiphDVdtDtpodXc3p~J',
        'x-frontend-date-validation': 'true',
        'x-requested-with': 'XMLHttpRequest',
        'x-xsrf-token': '736e8b76-4c80-4368-acd7-bef847715de6',

    }

    for i in range(5):
        resp = requests.post(
            'https://www.viator.com/orion/ajax/product-availability',
            cookies=cookies1,
            headers=headers1,
            json=json_data,
            proxies=zenrows_res_proxies,
            verify=False
        )

        print("Json Response Code:", resp.status_code)
        print(resp.status_code)
        if resp.status_code == 200:
            address_main_response_body = resp.text
            # address_main_response_body = b64decode(resp.json()["httpResponseBody"]).decode()
            # address_main_response_body = json.loads(address_main_response_body)["data"]
            print(resp.status_code)
            # # response_data = json.loads(address_main_response_body)
            print("success Response")

            if 'OUT_OF_AGE_RANGE' in address_main_response_body:
                search_data.update_one({"_id": doc_id}, {"$set": {"Status": "Not Found"}})
                return

            json_response = resp.text
            with open(josn_file_path, "w", encoding="utf-8") as f:
                f.write(json_response)

            return json_response

        else:
            print(resp.status_code)
            time.sleep(2)

    return None



def process_document(doc):
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
    if os.path.exists(file_path):
        with open(file_path, "r", encoding="utf-8") as f:
            html_content = f.read()
    else:
        # check if file already exists
        for _ in range(5):
            response = requests.get(
                referer_url,
                # cookies=cookies,
                proxies=proxies,
                verify='zyte-ca.crt',
                headers=headers,
            )
            print("Html Response...",  response.status_code)
            print(referer_url)
            if response.status_code == 200 or response.status_code == 404:
                html_content = response.text
                with open(file_path, "w", encoding="utf-8") as f:
                    f.write(html_content)
                print(f"Saved page for {order_code} -> {file_path}")

                break
            else:
                time.sleep(3)

    if 'We can’t find that page.' in html_content:
        search_data.update_one({"_id": doc_id}, {"$set": {"Status": "Not Found"}})
        print("Updated as Not found....")
        return

    custommer_market = customer_market_reverse_dict.get(sm)
    if not custommer_market:
        raise ValueError(f"No ORION_SESSION defined for country code '{sm}'")


    # --- Pick the ORION_SESSION based on sm ---
    orion_session = orion_sessions[sm]
    if not orion_session:
        raise ValueError(f"No ORION_SESSION defined for country code '{sm}'")

    res = Selector(text=html_content)
    service_name = res.xpath('//h1[@data-automation="product-title"]/text()').get()
    service_code = res.xpath('//meta[@name="productCode"]/@content').get()
    company = res.xpath('//meta[@property="og:site_name"]/@content').get()
    duration = res.xpath('//span[@class="label__Tm23"]//text()').get()
    # booking = res.xpath('//div[@class="bannerSubText__OOGX"]//text()').get()
    cancellation = res.xpath('//div[@class="policyDescription__oAOW"]//text()').get()
    Supplier_name = res.xpath('//button[@class="supplierDetailsLink__Yfk7"]/text()').get()
    review_data = res.xpath('//div[@class="rating__jScz"]/text()').get()
    mobile_data = res.xpath("//span[@class='label__Tm23' and normalize-space(text())='Mobile ticket']//text()").get()
    review_text = res.xpath('//div[@class="reviewCount__Bmi3"]/text()').get()

    review_number = ""
    if review_text:  # make sure it's not None
        match = re.search(r'[\d,]+', review_text)
        if match:
            review_number = match.group()

    print("Review number:", review_number)
    print(referer_url)
    script_text = res.xpath('//script[@id="globalState"]/text()').get()

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

            # Join offered languages with commas
            offered_languages_str = ", ".join(offered_languages)

            print("Primary language:", primary_language)
            print("Offered languages:", offered_languages_str)

        except Exception as e:
            print("Error parsing globalState JSON:", e)

        print("Number of reviews:", review_number)
    if not review_data:
        review_data = res.xpath('//span[@class="averageRatingValue__cWuj"]/text()').get()
    review = f"{review_data} / 5" if review_data else ""
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
    title_blocks = res.xpath('//div[@class="title__uQE0"]')

    data_for_meals = res.xpath('//script[@id="globalState"]/text()').get()

    meal_keywords = ["meal", "meals", "food", "foods", "drink", "drinks", "lunch", "dinner", "breakfast"]

    meal_info = "Included"  # default

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
                exclusions_str = " ".join(exclusions).lower()  # combine all and lowercase
                # check if any keyword exists
                if any(word in exclusions_str for word in meal_keywords) or "food & drinks" in exclusions_str:
                    meal_info = "Excluded"

        except Exception as e:
            print("Meals parse error:", e)

    print("Meals : included/ excluded →", meal_info)  # default
    guide_info = "Excluded"  # default

    for block in title_blocks:
        # get the text of the child div
        text = block.xpath('./div/text()').get()
        if text:
            text_lower = text.lower()

            # --- check meals ---
            if any(k in text_lower for k in meal_keywords):
                meal_info = "Included"

            # --- check guide ---
            if "guide" in text_lower or "driver/guide" in text_lower:
                guide_info = "Included"

            # if we already found both, no need to continue
            if  guide_info == "Included":
                break

    print("Meal info:", meal_info)
    print("Guide info:", guide_info)

    guide_extrac = ""

    if guide_info == "Included":
        guide_extrac = res.xpath(
            '//div[@class="title__uQE0"][contains(translate(.,"GUIDE","guide"), "guide")]//text()'
        ).get() or ""

    print("Guide extracted:", guide_extrac)
    transfer = res.xpath('//div[@class="title__uQE0"][contains(translate(.,"Transportation","Transportation"), "Transportation")]//text()').get()
    if transfer:
        transoption = "Included"
    else:
        transoption = "Excluded"


    # --- Product code ---
    product_code = res.xpath('//p[@data-automation="product-code"]/text()').get()
    prod_code = product_code.split(":")[-1].replace(" ", "")
    # api_key = "21ed11ef5c872bc7727680a52233027db4578a0e"
    # zenrows_url = "https://api.zenrows.com/v1/"

    season_date = convert_to_standard_date(seasonality)
    josn_file_name = f"{hashid}.json"
    josn_file_path = os.path.join(save_dir, josn_file_name)

    if os.path.exists(josn_file_path):
        with open(josn_file_path, "r", encoding="utf-8") as f:
            json_response = f.read()
    else:
        json_response = api_request(josn_file_path, orion_session, zenrows_res_proxies, doc_id, season_date, prod_code,
                                    pax)
        if not json_response:
            print("Getting Wrong Response in API Requests,,,")
            return None

    availability_data = json.loads(json_response)

    tourGrades_data = availability_data.get("productAvailability", {}).get("tourGrades", [])
    if not tourGrades_data:
        days_plus = 1
        max_retry_days = 7
        found = False

        # Convert season_date string to datetime object
        season_date_obj = datetime.datetime.strptime(season_date, "%Y-%m-%d")

        while days_plus <= max_retry_days:
            # Add days to season_date
            new_season_date = season_date_obj + datetime.timedelta(days=days_plus)
            new_season_date_str = new_season_date.strftime("%Y-%m-%d")

            print(f"Retrying with date: {new_season_date_str} (Day +{days_plus})")

            # Make new API request with updated date
            json_response = api_request(josn_file_path, orion_session, zenrows_res_proxies, doc_id, new_season_date_str,
                                        prod_code, pax)

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
            return None

    # --- Extract JSON-LD for review/price ---
    json_loading = res.xpath('//script[@type="application/ld+json"]/text()').get()
    if json_loading:
        try:
            data = json.loads(json_loading)
            item = data[1]
        except Exception as e:
            print("JSON-LD parse error:", e)

    # --- Meals / Guide / Mobile Ticket ---
    data_for_meals = res.xpath('//script[@id="globalState"]/text()').get()
    if data_for_meals:
        try:
            parsed = json.loads(data_for_meals)

            including_data_mobile = (
                parsed.get("pageModel", {})
                .get("product", {})
                .get("description", {})
                .get("productAttributes", [])
            )
            for attr in including_data_mobile:
                if attr.get("label") == "Mobile ticket":
                    mobile_ticket_info = "Mobile ticket"
                    break
        except Exception as e:
            print("Meals parse error:", e)  # stop after finding it

    # --- Insert one-by-one for each start time ---
    print("tourGrades_data:", tourGrades_data)
    date_obj = today_date

    calendar_week = date_obj.isocalendar()[1] - 1  # [0]=year, [1]=week, [2]=weekday
    print("Calendar Week:", calendar_week)
    for tg in tourGrades_data:
        title_name_mode = tg.get("title")

        modality_code = tg.get("tourGradeCode", "")
        print("modality_code:", modality_code)

        # Take only part before ~
        modality_code = modality_code.split("~")[0]

        print(modality_code)  # 👉 DEFAULT
        pickup_point = tg.get("title", "")
        main_date = tg.get("date", "")
        availability = tg.get("availability", "")

        start_times = tg.get("startTimes", [])

        # If no startTimes, still insert one record with defaults
        if not start_times:
            start_times = [{}]  # make a list with one empty dict

        for st in start_times:
            # --- Start time ---
            start_time = st.get("startTime", "") or st.get("startTime24H", "")

            # --- Currency + Price ---
            cueency_code = ""
            variant_price = ""

            # 1. Try direct "price"
            variant_price = (
                    st.get("price", {}).get("retailPrice", {}).get("amount", "")
                    or st.get("price", {}).get("discountedPrice", {}).get("amount", "")
            )
            cueency_code = (
                    st.get("price", {}).get("retailPrice", {}).get("currencyCode", "")
                    or st.get("price", {}).get("discountedPrice", {}).get("currencyCode", "")
            )
            # search_date = today_date
            # search_date = datetime.strptime(today_date, "%Y-%m-%d")
            # Check type and convert accordingly
            if isinstance(today_date, str):
                search_date = datetime.strptime(today_date, "%Y-%m-%d")
            elif isinstance(today_date, date):
                search_date = datetime.combine(today_date, datetime.min.time())
            else:
                search_date = today_date  # Already a datetime
            # --- Normalize season_date (can be ISO with time or plain date) ---
            if "T" in season_date:  # if ISO format
                season_dt = datetime.fromisoformat(season_date.split("Z")[0].replace("+00:00", ""))
            else:  # plain YYYY-MM-DD
                season_dt = datetime.strptime(season_date, "%Y-%m-%d")

            # --- Calculate difference ---
            booking_days = (season_dt.date() - search_date.date()).days
            booking = f"{booking_days} Days"
            # 2. Try "totalPrice"
            if not variant_price:
                variant_price = (
                        st.get("totalPrice", {}).get("retailPrice", {}).get("amount", "")
                        or st.get("totalPrice", {}).get("discountedPrice", {}).get("amount", "")
                )
                cueency_code = (
                        st.get("totalPrice", {}).get("retailPrice", {}).get("currencyCode", "")
                        or st.get("totalPrice", {}).get("discountedPrice", {}).get("currencyCode", "")
                )
            if start_time:
                modality_name = f"{title_name_mode}_{start_time}"
            else:
                modality_name = title_name_mode

            # 3. Fallback to "priceBreakdown"
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
                    if variant_price:  # stop at the first valid one
                        break

            # --- Final check ---
            if not variant_price:
                print(f"⚠️ Skipping {start_time} - No price found")
                continue

            try:
                list_main = {
                    "Modality Name": modality_name,
                    "Review": review_number,
                    "Region" : "",
                    "Destination Code":"",
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
                    "Arrival date": main_date,
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
                    "Contract Info":"",
                    "Incomming Office Code": "",
                    "Transfers- extracted info": transfer,
                    "Start Time": start_time,
                }
            except Exception as e:
                print(e)

            try:
                product_data.insert_one(list_main)
            except Exception as e:
                search_data.update_one({"_id": doc_id}, {"$set": {"Status": "Not Found"}})
                print(e)
            print(f"Inserted variant: {pickup_point} | {start_time} | {variant_price}")
    else:
        search_data.update_one({"_id": doc_id}, {"$set": {"Status": "Done"}})

def main():
    with ThreadPoolExecutor(max_workers=1) as executor:
        docs = list(search_data.find({"Status": "Pending"}))
        executor.map(process_document, docs)

if __name__ == "__main__":
    Max_Retries = 1

    while Max_Retries > 0:
        Max_Retries -= 1
        total_pending = search_data.count_documents({"Status": "Pending"})
        print("Total Pending...", total_pending)
        if not total_pending:
            Export_File()
            break
        main()


