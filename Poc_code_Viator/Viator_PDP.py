import json
import os.path
import re
import time
import urllib.parse
from base64 import b64decode
from concurrent.futures import ThreadPoolExecutor
from config_data import *
from datetime import datetime, timedelta
from parsel import Selector
import requests
import json
import urllib.parse


def parse_curl_file(file_path):
    headers = {}
    cookies = {}

    with open(file_path, "r", encoding="utf-8") as f:
        curl_text = f.read()

    # -----------------------------
    # Parse headers (-H)
    # -----------------------------
    header_matches = re.findall(r"-H\s+'([^:]+):\s*(.*?)'", curl_text)

    for key, value in header_matches:
        if key.lower() == "cookie":
            for pair in value.split(";"):
                if "=" in pair:
                    k, v = pair.strip().split("=", 1)
                    cookies[k] = v
        else:
            headers[key] = value

    # -----------------------------
    # Parse cookies from -b
    # -----------------------------
    cookie_match = re.search(r"-b\s+'([^']+)'", curl_text)
    if cookie_match:
        raw_cookie = cookie_match.group(1)
        for pair in raw_cookie.split(";"):
            if "=" in pair:
                k, v = pair.strip().split("=", 1)
                cookies[k] = v

    return headers, cookies

def api_request(josn_file_path, orion_session, zenrows_res_proxies, doc_id, season_date, prod_code, pax, sm):
    try:
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

        # Usage
        headers, cookies = parse_curl_file("cookie_profile.txt")

        # cookies['datadome']= region_cookies[sm]['datadome']
        # cookies['x-viator-tapersistentcookie']= region_cookies[sm]['x-viator-tapersistentcookie']
        # cookies['XSRF-TOKEN']= region_cookies[sm]['XSRF-TOKEN']
        # cookies['ORION_SESSION']= region_cookies[sm]['ORION_SESSION']


        username = "td-customer-fkYxy1pw8m4m"
        password = "us0im0rm9b"
        proxy_server = "pl707oea.pr.thordata.net:9999"

        tproxies = {"http": f"http://{username}:{password}@{proxy_server}"}
        main_res_proxies = {
            'http': 'http://68C24RCjsFq3:YF67LxHnCPRwc57@superproxy.zenrows.com:1337',
            'https': 'http://68C24RCjsFq3:YF67LxHnCPRwc57@superproxy.zenrows.com:1337',
        }
        oxyy_prox = {
            "http": "http://Kunal_kk_7JUxy:+m5x_zg=73H~@unblock.oxylabs.io:60000",
            "https": "http://Kunal_kk_7JUxy:+m5x_zg=73H~@unblock.oxylabs.io:60000",
        }
#orion_session

        cookies = {
            'profilingInAuthSession': '85Jq8He6Etyzx%2FOT7Rx6tg%3D%3D%7CzkUpfprvWp7Sv%2BAjmgWQ0%2FswLek75qHhQ4igtSc84LKO9f2yvr%2FDfeZLP1GCxQ%2BXc%2BJ%2FApirUdNJYOas%2BrAK%2FfOPVJowdpHpMaSGmaqn%2B2HpRQ%3D%3D%7C%2FQqcSi0jJ%2Bc%3D%3Ay1a0COe2jQ5Uymw%2Bpzf5qCg2avat%2FEBc%2Ffl%2FTjMbwX8%3D',
            'x-viator-tapersistentcookie': '77e80f3a-7802-4bac-b10f-ed38621dd6d3',
            'SEM_PARAMS': '%7B%7D',
            'SEM_MCID': '42861',
            'EXTERNAL_SESSION_ID': '',
            'LAST_TOUCH_SEM_MCID': '42861',
            'XSRF-TOKEN': '132bd55d-c112-4f93-bf65-988b89414cc8',
            'orion_first_touch_logged_in': 'false',
            'profilingBeaconSession': '1Lf2eU3zIJe%2B1QOrTY1jjg%3D%3D%7Coe71uQpIzduHfRYy3qtHcrKb4YbUgt%2Ff4jXEnT%2B5T72%2FU1rQXoKl8a8mDK7Jy7sQ2nbVycNcN2o%3D%7CNSBI0T5eqik%3D%3AYOF6fXr3Ai6qbNQQb0zwaBclDZTZ%2BODMIP%2FBeW4mJoE%3D',
            'OptanonAlertBoxClosed': '2026-05-25T18:45:52.918Z',
            'ORION_SESSION': 'oMSTj1WLilzQLvWclUwKkg%3D%3D%7CFih%2B9B4QjQAxx6YuhG2TT0dZMEMoG3S1ToL5X%2FL0su6lz5HUAWdynKYJFjn2dwY9LOHdNZFqkI3vE67WNnSK4Wsjj3AQRUHj5qeLcrHrK%2By1iNvKWrprt4ybhSWA5gBfTolP3U9IKX9%2FgCXT5it1z%2FZR3ugNm1XTh4mBOtBPwdqKsZuUv1B9yfA74zUkky1pya5Xp8T2jKrpFr3lCLd%2BW41iVDd%2Fi94EY9d40lAU8LLFDJ0NE6oeg%2F0BZgGlzUwoMoncCt5QdvnY9ZNTYsM39KPiXnGvCuqIkS6Cl7TsMTNFwVCJvKkiS9%2FiYfHwpah3pyzeh2ySwn1fYEAgRBuBGOrE8XZygPPj%2BkEM2kd3LECeS0%2BUQ761Z8Rh8G0koXf61qBD%2BUPazcTH87TTacic%2B4ZC9moaTeYyzYIrpMGNOu16sgkfWrtp%2F2gy713DZ66JGEOYyZmHS%2BTDbciFWe3I%2FY07ljHqbRWoGAFHtMyrPVPaVuBxyQb%2FBWc1YsW%2FhWPSi64YyAWwgvl08rRaq4WzNK7voWhY%2FJpefRvla%2F4%2F9bAwX9mRWs4E%2F%2Bw9lZBxK4qW2X95b7AESirXaPqB2aSn1QIkDUKFTAoIVC5qArGIAjJpBT047OZSH3HjVPO632rdSQ%2FNZ4pwEM8K3JkURFey%2FVyjUrORLDaEcZQBq3%2FjHhsOo8OhluBq0qK3iQuYLRTQqD9hwi%2F6gkwDUJc%2FNZYrh3zO41bf9jQ%2FjWZM7PcT1bWphDBoEMEUhG5OAmyFCZb3%2B9mgJMp15f555%2FY%2BKBfxDI0xBcLGOiCtBzSUWuIob7A3PxjQ5XTRBlT39yjSSVTS6me9U8a%2FwXf9UsF%2B%2Bz3TzD0qLGVpO%2FL8NfHSzpHlwyq4l45uHc0wpbLZTno8ZUBcJdGU2uyu3wSdllH6A9jWLv5uRqx3yQjCHCK3gV59TeyLDxy3wE5soUR2iu6Xdwm2%2B14qCl6sgXFbf1X%2BZeLb9uaLXXUaC%2BLah6WqwdvGymiSKfgKDLhathvs%2Fk3AexPAUNQ8wBDf5rPn%2FCCrD84GuqqnhL%2FAFBuhbF6i4bB1z19MlmuTqr8u2q7PA7qyeFTC8EucBFnGCUGU%2F91Pq1wShKqjlJ2To37iWnF0BFvwmU0REGGvesrl67IavNIV42Q0MSnfNQ%2BE6RoOJ8HbjN521FwDT7jvRmo21FLDTOJDL73EsNxBp9Zr6dR36JIgqTE9ZmMw8Wt32HJ%2FjCRoDcYiNDhDS8lBJ5NmuVHEtxwRdOO5715tBdunIp08J%2Ft2IGco%2F7zm6LsAV6NLr8%2FG%2FYXfINZJWKrJujw3BOeZg2gxdSNzr4coM4ypPf2P9G5tI0gTuHtE3lUqnCCjmezEE0MqjPG3id3OLREmSurIYAF40s%2BA5QTt%2BH3%2FsOFmtiV8hVMXeY5t2fz1jEbYx1rpgPtv%2Fo6%2BbuyE0XHj0N6T4cmDVIzX2oVIGx4RgDYvvLiTQgq89cEU%2FN2Ev7J8bDcFUowdsGfoLfiwzfmftBSwnvd5t4g486Xiqa%2Fzg7lwmNz4bFQGW9gEnN4C1L98U%2BdW2dbjlwgl5vXwuDkP0ww%2F8qOu4oEp9MhLITjTlikN3vs5pQNREPV4AChJCyFkzRfgUhzTANrqm8c66owuGAy9Xwlid%2BcZXYl1FMSNW1DtiallUMaNJ1goHT%2F8h4be9fILA%2B2AHG4NJLPjq3mRDdw1Q%2FXNA1A08blbd%2BMbzKpc4XKMB1yDZXGmttkpL82RBnf81o0Pfkprs1zkExJWG9oRx7rPaBrz8On03Ap%2BO2POwgzYnxShBCbA0axXXPToGvI5b9r8dVZG6oZHWEs0HetQhVM3IwnJdEFdXtgLTd9k1ov03ToOWzTntEbq7H8AWzte9PL5yWY2lnsuTDgROIGYPTFwC6%2FyxJCDEewdvwQeK3bVDtjTp27D7DVCdxOvPRiL%2F8VqoFmV2qBM7craGvRHKFSmB5A%2BA8Ti8BMIqPqlrTMmR%2BD31ioTdZ1lhsXkQ0MZSrR78chbPVazBibnTnmBpLGBehyYzQymAISlB%2FTklzfdBqsVHZbrd70Vghqn1Wwg1itmz1DnWdGk2gsPITcrtDNCefKvfE7Tr2fEcwlr8vk9sHGUykQ9PNkeM%2F0tnCNwXrKsSOozAODiAoW0cXezJxxyt7R93%2F54u8GrZHHp2y3jPJScJl0M1mV%2BWlnhDg11fVrVxW0D4LzsmSZpLn0XiHJWSpzUIxt0im86CaTF1j27OfjyF6hnjKqvKuRx%2BV%2FAuy2lHRZbIcMJXIZMC5wo9QVcDuBticpvfnwgFhAYC%2BwvpQd1I3D%2FEJmvrXMmDuU%3D%7CZ8D6OgGvkps%3D%3AY2p0D%2Bgwbzwmxw%2BUGG47hbaOpMlSBaITE%2BkCxKVwdtU%3D',
            'REFERER_PAGE_REQUEST_ID': 'A7528726:F722_0A280F01:01BB_6A1498DF_5CE84D:13AE47',
            'OptanonConsent': 'isGpcEnabled=0&datestamp=Tue+May+26+2026+00%3A15%3A55+GMT%2B0530+(India+Standard+Time)&version=202601.2.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=60bdce4a-7040-4af4-b1f1-e23ca6ff37b1&interactionCount=2&isAnonUser=1&prevHadToken=0&landingPath=NotLandingPage&groups=C0001%3A1%2CC0003%3A1%2CC0004%3A1%2CC0002%3A1&intType=1&geolocation=%3B&AwaitingReconsent=false',
            'ORION_SESSION_REQ': 'A7528726%3A79A0_0A2806EB%3A01BB_6A1498DF_5B233A%3A2B1A3F%7CA7528726%3AF722_0A280F01%3A01BB_6A1498DF_5CE84D%3A13AE47%7CA7528726%3AF722_0A280F01%3A01BB_6A1498DF_5CE84D%3A13AE47',
            'datadome': 's_qF8_Xw5bnJ2YU9QswhT7eC7tm5EfXkOb1zD4y5uH6dpt68yl50sU7yDhJNZWfj8dKBYOO8wKfB4vZOXWUqHfMEieXGWQvNp0bPNN1aIr2dUpni4XKfrq361zk4e_WK',
            'g_state': '{"i_l":0,"i_ll":1779734756830,"i_b":"wxzftKnBuy1Nt84kUb1knF0OBrME5H4mwFuRDMDZWgA","i_e":{"enable_itp_optimization":0},"i_et":1779734709423}',
        }

        headers = {
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'en-GB,en;q=0.9',
            'content-type': 'application/json',
            'origin': 'https://www.viator.com',
            'priority': 'u=1, i',
            'referer': 'https://www.viator.com/tours/Bangkok/Great-Ayutthaya-Adventure/d343-6356GAA?dd_referrer=',
            'sec-ch-ua': '"Chromium";v="148", "Google Chrome";v="148", "Not/A)Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-ch-ua-platform-version': '"15.0.0"',
            'sec-ch-viewport-width': '1920',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'traceparent': '00-48c1e0da2f4e3254027eb3d8532c79c4-3c17b1d2bdfd8daa-00',
            'tracestate': 'es=s:0.1',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36',
            'x-requested-with': 'XMLHttpRequest',
            'x-xsrf-token': '132bd55d-c112-4f93-bf65-988b89414cc8',
            # 'cookie': 'profilingInAuthSession=85Jq8He6Etyzx%2FOT7Rx6tg%3D%3D%7CzkUpfprvWp7Sv%2BAjmgWQ0%2FswLek75qHhQ4igtSc84LKO9f2yvr%2FDfeZLP1GCxQ%2BXc%2BJ%2FApirUdNJYOas%2BrAK%2FfOPVJowdpHpMaSGmaqn%2B2HpRQ%3D%3D%7C%2FQqcSi0jJ%2Bc%3D%3Ay1a0COe2jQ5Uymw%2Bpzf5qCg2avat%2FEBc%2Ffl%2FTjMbwX8%3D; x-viator-tapersistentcookie=77e80f3a-7802-4bac-b10f-ed38621dd6d3; SEM_PARAMS=%7B%7D; SEM_MCID=42861; EXTERNAL_SESSION_ID=; LAST_TOUCH_SEM_MCID=42861; XSRF-TOKEN=132bd55d-c112-4f93-bf65-988b89414cc8; orion_first_touch_logged_in=false; profilingBeaconSession=1Lf2eU3zIJe%2B1QOrTY1jjg%3D%3D%7Coe71uQpIzduHfRYy3qtHcrKb4YbUgt%2Ff4jXEnT%2B5T72%2FU1rQXoKl8a8mDK7Jy7sQ2nbVycNcN2o%3D%7CNSBI0T5eqik%3D%3AYOF6fXr3Ai6qbNQQb0zwaBclDZTZ%2BODMIP%2FBeW4mJoE%3D; OptanonAlertBoxClosed=2026-05-25T18:45:52.918Z; ORION_SESSION=oMSTj1WLilzQLvWclUwKkg%3D%3D%7CFih%2B9B4QjQAxx6YuhG2TT0dZMEMoG3S1ToL5X%2FL0su6lz5HUAWdynKYJFjn2dwY9LOHdNZFqkI3vE67WNnSK4Wsjj3AQRUHj5qeLcrHrK%2By1iNvKWrprt4ybhSWA5gBfTolP3U9IKX9%2FgCXT5it1z%2FZR3ugNm1XTh4mBOtBPwdqKsZuUv1B9yfA74zUkky1pya5Xp8T2jKrpFr3lCLd%2BW41iVDd%2Fi94EY9d40lAU8LLFDJ0NE6oeg%2F0BZgGlzUwoMoncCt5QdvnY9ZNTYsM39KPiXnGvCuqIkS6Cl7TsMTNFwVCJvKkiS9%2FiYfHwpah3pyzeh2ySwn1fYEAgRBuBGOrE8XZygPPj%2BkEM2kd3LECeS0%2BUQ761Z8Rh8G0koXf61qBD%2BUPazcTH87TTacic%2B4ZC9moaTeYyzYIrpMGNOu16sgkfWrtp%2F2gy713DZ66JGEOYyZmHS%2BTDbciFWe3I%2FY07ljHqbRWoGAFHtMyrPVPaVuBxyQb%2FBWc1YsW%2FhWPSi64YyAWwgvl08rRaq4WzNK7voWhY%2FJpefRvla%2F4%2F9bAwX9mRWs4E%2F%2Bw9lZBxK4qW2X95b7AESirXaPqB2aSn1QIkDUKFTAoIVC5qArGIAjJpBT047OZSH3HjVPO632rdSQ%2FNZ4pwEM8K3JkURFey%2FVyjUrORLDaEcZQBq3%2FjHhsOo8OhluBq0qK3iQuYLRTQqD9hwi%2F6gkwDUJc%2FNZYrh3zO41bf9jQ%2FjWZM7PcT1bWphDBoEMEUhG5OAmyFCZb3%2B9mgJMp15f555%2FY%2BKBfxDI0xBcLGOiCtBzSUWuIob7A3PxjQ5XTRBlT39yjSSVTS6me9U8a%2FwXf9UsF%2B%2Bz3TzD0qLGVpO%2FL8NfHSzpHlwyq4l45uHc0wpbLZTno8ZUBcJdGU2uyu3wSdllH6A9jWLv5uRqx3yQjCHCK3gV59TeyLDxy3wE5soUR2iu6Xdwm2%2B14qCl6sgXFbf1X%2BZeLb9uaLXXUaC%2BLah6WqwdvGymiSKfgKDLhathvs%2Fk3AexPAUNQ8wBDf5rPn%2FCCrD84GuqqnhL%2FAFBuhbF6i4bB1z19MlmuTqr8u2q7PA7qyeFTC8EucBFnGCUGU%2F91Pq1wShKqjlJ2To37iWnF0BFvwmU0REGGvesrl67IavNIV42Q0MSnfNQ%2BE6RoOJ8HbjN521FwDT7jvRmo21FLDTOJDL73EsNxBp9Zr6dR36JIgqTE9ZmMw8Wt32HJ%2FjCRoDcYiNDhDS8lBJ5NmuVHEtxwRdOO5715tBdunIp08J%2Ft2IGco%2F7zm6LsAV6NLr8%2FG%2FYXfINZJWKrJujw3BOeZg2gxdSNzr4coM4ypPf2P9G5tI0gTuHtE3lUqnCCjmezEE0MqjPG3id3OLREmSurIYAF40s%2BA5QTt%2BH3%2FsOFmtiV8hVMXeY5t2fz1jEbYx1rpgPtv%2Fo6%2BbuyE0XHj0N6T4cmDVIzX2oVIGx4RgDYvvLiTQgq89cEU%2FN2Ev7J8bDcFUowdsGfoLfiwzfmftBSwnvd5t4g486Xiqa%2Fzg7lwmNz4bFQGW9gEnN4C1L98U%2BdW2dbjlwgl5vXwuDkP0ww%2F8qOu4oEp9MhLITjTlikN3vs5pQNREPV4AChJCyFkzRfgUhzTANrqm8c66owuGAy9Xwlid%2BcZXYl1FMSNW1DtiallUMaNJ1goHT%2F8h4be9fILA%2B2AHG4NJLPjq3mRDdw1Q%2FXNA1A08blbd%2BMbzKpc4XKMB1yDZXGmttkpL82RBnf81o0Pfkprs1zkExJWG9oRx7rPaBrz8On03Ap%2BO2POwgzYnxShBCbA0axXXPToGvI5b9r8dVZG6oZHWEs0HetQhVM3IwnJdEFdXtgLTd9k1ov03ToOWzTntEbq7H8AWzte9PL5yWY2lnsuTDgROIGYPTFwC6%2FyxJCDEewdvwQeK3bVDtjTp27D7DVCdxOvPRiL%2F8VqoFmV2qBM7craGvRHKFSmB5A%2BA8Ti8BMIqPqlrTMmR%2BD31ioTdZ1lhsXkQ0MZSrR78chbPVazBibnTnmBpLGBehyYzQymAISlB%2FTklzfdBqsVHZbrd70Vghqn1Wwg1itmz1DnWdGk2gsPITcrtDNCefKvfE7Tr2fEcwlr8vk9sHGUykQ9PNkeM%2F0tnCNwXrKsSOozAODiAoW0cXezJxxyt7R93%2F54u8GrZHHp2y3jPJScJl0M1mV%2BWlnhDg11fVrVxW0D4LzsmSZpLn0XiHJWSpzUIxt0im86CaTF1j27OfjyF6hnjKqvKuRx%2BV%2FAuy2lHRZbIcMJXIZMC5wo9QVcDuBticpvfnwgFhAYC%2BwvpQd1I3D%2FEJmvrXMmDuU%3D%7CZ8D6OgGvkps%3D%3AY2p0D%2Bgwbzwmxw%2BUGG47hbaOpMlSBaITE%2BkCxKVwdtU%3D; REFERER_PAGE_REQUEST_ID=A7528726:F722_0A280F01:01BB_6A1498DF_5CE84D:13AE47; OptanonConsent=isGpcEnabled=0&datestamp=Tue+May+26+2026+00%3A15%3A55+GMT%2B0530+(India+Standard+Time)&version=202601.2.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=60bdce4a-7040-4af4-b1f1-e23ca6ff37b1&interactionCount=2&isAnonUser=1&prevHadToken=0&landingPath=NotLandingPage&groups=C0001%3A1%2CC0003%3A1%2CC0004%3A1%2CC0002%3A1&intType=1&geolocation=%3B&AwaitingReconsent=false; ORION_SESSION_REQ=A7528726%3A79A0_0A2806EB%3A01BB_6A1498DF_5B233A%3A2B1A3F%7CA7528726%3AF722_0A280F01%3A01BB_6A1498DF_5CE84D%3A13AE47%7CA7528726%3AF722_0A280F01%3A01BB_6A1498DF_5CE84D%3A13AE47; datadome=s_qF8_Xw5bnJ2YU9QswhT7eC7tm5EfXkOb1zD4y5uH6dpt68yl50sU7yDhJNZWfj8dKBYOO8wKfB4vZOXWUqHfMEieXGWQvNp0bPNN1aIr2dUpni4XKfrq361zk4e_WK; g_state={"i_l":0,"i_ll":1779734756830,"i_b":"wxzftKnBuy1Nt84kUb1knF0OBrME5H4mwFuRDMDZWgA","i_e":{"enable_itp_optimization":0},"i_et":1779734709423}',
        }

        for i in range(5):
            resp = requests.post(
                'https://www.viator.com/orion/ajax/product-availability',
                cookies=cookies,
                headers=headers,
                json=json_data,
                proxies=tproxies,
                verify=False

            )

            print("Json Response Code for:", resp.status_code)
            print(resp.status_code)

            if resp.status_code == 200:
                address_main_response_body = resp.text
                # address_main_response_body = b64decode(resp.json()["httpResponseBody"]).decode()
                # address_main_response_body = json.loads(address_main_response_body)["data"]
                print(resp.status_code)
                # # response_data = json.loads(address_main_response_body)
                print("success Response")

                if 'OUT_OF_AGE_RANGE' in address_main_response_body:
                    print("Not Found")
                    search_data.update_one({"_id": doc_id}, {"$set": {"Status": "Not Found"}})
                    return

                json_response = resp.text
                with open(josn_file_path, "w", encoding="utf-8") as f:
                    f.write(json_response)
                time.sleep(3)

                return json_response

            else:
                print(resp.status_code)
                time.sleep(2)

    except Exception as e:
        print("Error in API requesrtws:", e)

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
    print(hashid)

    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36',
        'cookie': 'x-viator-tapersistentcookie=df89af16-7c96-41ee-b4a1-42e82257f070; EXTERNAL_SESSION_ID=; orion_first_touch_logged_in=false; profilingBeaconSession=9WPNiaGLdGc0WjC70Lg95A%253D%253D%257CD7z9IobYHWujveX%252BTYQTuyYgpCYTHMRTcJfOdqiBUPgcAlkJyoSlm9Q7Qa9qVLBQn8fuqhf9gac%253D%257CCKx8xJZsxeQ%253D%253A3V%252FvUaWm%252Bx1IZG2QNF79jfPwrfE%252FLYTmW1Kq0k0rdHE%253D; _gcl_au=1.1.479477029.1776372828; rskxRunCookie=0; rCookie=vd1maq3jlrl769m8pztwmkmo1yinc4; _bcnctkn=74a0f649b9f9d81323b7446e6bc1f3292a23; _cc=AfY8ysFCWa%2Bi0rt7DQWWJQMn; OptanonAlertBoxClosed=2026-04-16T21:03:18.680Z; SEM_PARAMS=%7B%22gclid%22%3A%22CjwKCAjwhqfPBhBWEiwAZo196txJsnwfhkuqvbQkbVuYSW8Qmz0fZS64foXl2zRZre8d7pKk9UQ_YxoCsMAQAvD_BwE%22%2C%22supsc%22%3A%22aud-2226856787438%3Akwd-270303623%22%2C%22supca%22%3A%2212512866044%22%2C%22supti%22%3A%22aud-2226856787438%3Akwd-270303623%22%2C%22gbraid%22%3A%220AAAAAD-gbd6ypzB1OCRQdr1yAYMkSUAKP%22%2C%22suplp%22%3A%229199115%22%2C%22supdv%22%3A%22c%22%2C%22supai%22%3A%22504932285966%22%2C%22supag%22%3A%22122704388281%22%2C%22supnt%22%3A%22g%22%2C%22supci%22%3A%22aud-2226856787438%3Akwd-270303623%22%7D; SEM_MCID=28353; viator_mcid=28353; LAST_TOUCH_SEM_MCID=28353; XSRF-TOKEN=37154e5c-d8c9-49f4-9f15-1385f546f10f; _gcl_aw=GCL.1776935440.CjwKCAjwhqfPBhBWEiwAZo196txJsnwfhkuqvbQkbVuYSW8Qmz0fZS64foXl2zRZre8d7pKk9UQ_YxoCsMAQAvD_BwE; _gcl_dc=GCL.1776935440.CjwKCAjwhqfPBhBWEiwAZo196txJsnwfhkuqvbQkbVuYSW8Qmz0fZS64foXl2zRZre8d7pKk9UQ_YxoCsMAQAvD_BwE; _gcl_gs=2.1.k1$i1776935435$u154864063; lastRskxRun=1776935667552; REFERER_PAGE_REQUEST_ID=9D345C5E:7BA2_0A280D35:01BB_69EA8455_1316B7FB:3DC53A; ORION_SESSION=7VqbXb64Y7pvTubBLdQQsw%3D%3D%7CeF5%2BKgfxZ%2FoOGCUuZq2hzBVfCVQXWhaG1DOo%2FDxC7%2F%2FbYvDQnkEmBw3rmUyEuV8%2FZ3WMDMvxz9TD%2FSRF3E5FvsCKHwySCPzmagwofHSx0AYpYM1O8rCXnQqPP2JdJVdjARpveXNlJQQ7fo6%2BdtHkh2mf5szmJ7P99NOv3ItzQFSqJLXNtTU2wM4NYbtlOo8VWWSpGBr3ZRhmo7y9uI7juGrBPZ3vrkEg5JbfRC%2FNCsbcoxXO6jDP1e2YjmZNMZz3Pxzn72fa4dvv%2FZu%2FNXUCopoPvyhQppa%2B37dwYzBtz2TDkw%2FdUBiHuIEZdO6sSz6NOyUD5VsJUW%2FmnIwRCQs3bnBI1RMJHsll9CoCZxg6ghjziR5QF0zoJtUPw6XcJXhmSkVkAPaGY6oej%2F9Zka0iG7w6%2B0X3raKggXZKf3XbQcEtzxE5Wulrq0FWPkUc5EngX3s%2Bs359ZRQ6TBT0XBB7Aoh%2FYYLXnPzo%2BjMyNYV%2BxQ5yWq9W8TZfT9l5%2FNMHJRDSghkpipH1dlIod3%2Bd0tj03txi3E02dWR0fN8XKL2myDSBhd6ABWu4WF0x24KUgzOK1IaPBGCInzhQEWBxHY49Upqnk5AvhxH82JNLyexmrT2HfTDj%2FmntqJjNfLgEvD%2BjLP7MCzqWcH%2B%2B0F3scsxXszr8uQjaVS9eQknut3gDRgBL7KPAxP0RrWld2zQIfvlj8S1sdaSMmLEB4nQaA2lekQD3OIDx8rUaCxNYQmZu7gRFGbx5korvkk0ZD5Ox5h%2BPlZ70Reh707%2BP5aTN4jyIGTp6ncdVvpYASbGVf9u4snQK%2BhrImlHAea9RbPypd2Q%2FI5yHcKjTq7JWrEkSdpKyD8ra3%2B8x4UCbOYlEFh09VpYsQ6LFadeAnten0KkovWlklDdFkaq4tVdiAmZRJizTEHdxXz3N1%2Ff81VAVEI%2Bjkl9YnBFex0uVoMWPl0hUt2fJIT3%2FFXk2g1qnrhG%2FnHQxGn8uGP7eCitywF2NVTqulXU86g9%2F%2FgjOPZ6zt9g0cB5jeSr%2F%2ByXsLovt%2BqrFFWwL6wjmbwcM%2FhM9ToiMYyvVFSub8vCDIx8q5pYbb9fcqf33DRz7YuxkQMs%2B1hSHMweZI6wV7iLmGhk%2BZFgc%2Fp95bO583fCBT2%2F6lT4zmH7zwxrgUmyON0KvQNjlQ9keAxvgQ%2BJuW1H117qmUAguEF2FJ7b6FMWGzc07m%2F3zyYC2qEA1rFGexOhA0Nrx7CZEFHf5mvj7RyOaQ9z1wd3pa5gT3KLjC9ZhJG3x9zMCvxPl2u%2B5ohsU8z1GICBZhd3nbhFD87pMMuxnV%2BF0JnPS0TINAVWh4LM3krmSU4Z6yUjXsVnzcYhh7IWl54dRktQ5DStVYgio2rDchnBMrcuT8h2Wf9MigSc0YDWC7rYHPlEn4ss%2BVuFNMwjhen7g11lU4X%2BS6SPekb2V2g8h9y7d0voNwqXY3Zcb5ZPUGKfAHvOI8Mt8WIpZd6Pn4wE6OdZP3tFjLWRUTBKUBJ49n0Hhwwp3r0GAwg%2BcW%2BSoB5r3napJFmnW%2FnwCXgyFDRBI6Z0h9yMUVKkbY1FSAQxfY%2Fmoic2cxCYHWvmUc4ZQT2AHN%2BgEsvG%2FMHOMsEHCrOn2j6llIWQKiPpaQTPAkxS6Q%2FRSqdBaFCMGTtnGw57N8PLEkl1gznGtbnuf6WRXpY9Ozvn4NrMcTN5VgVbHDkQ230BNMq%2FEWNJIR4j4qIPv6Kisu2ybsKlPd7XgIyb4FKXawu4r4SwbqRndc6Ar64wIYw5z%2FANmnbB8121rLfJcjRniEYCLzkuDHi%2FBWEwXDwhXPG62VAYlyft2%2BF0Tpt%2BBpmcRpPXH5ZrjGdEWbDRp7%2BlgPxeXsJYSDlx2F4jkJqNMBEMhNTG08BNt0YW%2B3fy5IIcp2xIp4xPwgKuZRAxDbu9cGdw6NbQpD%2B53Dt8peemEkHW22577Q0rpqCaaYuB%2BdzCv4M%2BrS9sAkfEiR2NdfC4%2F4LyUegd9gSXsLIiTbKBReWXsLG3MHrSWrvxaDk4JJQKD5Y%2B9e3df%2FWqR3w0M%2Bo1t7xSsoElO8usEKpAD5yS3Uzl0%2FRhlbamwTYXH7nQkC6pIUmIjk0nbge2UsBKMGNEB2fUPM89VVWmE4nIOPoeWqwg7HKqyfownqCba2yQB2KrrRkrzU6rk7LAOjeFHDrxzn05nhiAEQ%2Fb8hDLto42bHXkPBDREdNsxux6kOp7Io7Xeqme3diNTQOMnQ9e9zwNDpsLEkAx4GACcNe%2BcYP3N1yJy%2FnJkzIbjL8wc3CTMirRDFaO4wrCkoStQGRasYMcD8Lf34Hn%2BNJEMpklvR6pEVe44MmutN0uaP5jBsJshyzfUtYlILjI2jfFGaSsVhz9fS6f%2Bfq71EaHU7TcN%2FlpcW%2BbU6069WHVuc0g3SfitwmOiGPIvxXn73w%3D%3D%7CNMzmFFmcFF8%3D%3As6T%2FJb%2BADqjJ%2BgkOevi0m1hh0CzeaZHG%2BCGh1zuHuks%3D; g_state={"i_l":0,"i_ll":1776977130464,"i_b":"iVnACHOvO6N4aeHZN0homng2zX6ry/6lyPJidgFqwuo","i_e":{"enable_itp_optimization":0},"i_et":1776372827735}; OptanonConsent=isGpcEnabled=0&datestamp=Fri+Apr+24+2026+02%3A15%3A32+GMT%2B0530+(India+Standard+Time)&version=202601.2.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=ff84a752-d728-42c2-b025-6d3abdf6ab17&interactionCount=2&isAnonUser=1&prevHadToken=0&landingPath=NotLandingPage&groups=C0001%3A1%2CC0003%3A1%2CC0004%3A1%2CC0002%3A1&crTime=1776373399356&intType=1&geolocation=IN%3BGJ&AwaitingReconsent=false; ORION_SESSION_REQ=9D345C1E%3AF718_0A280907%3A01BB_69EA8454_12D8D865%3A3E7993%7C9D345C5E%3A7BA2_0A280D35%3A01BB_69EA8455_1316B7FB%3A3DC53A%7C9D345C5E%3A7BA2_0A280D35%3A01BB_69EA8455_1316B7FB%3A3DC53A; profilingInAuthSession=%252FBm0oHSQ0kNl544FZRDbmg%253D%253D%257CNzAAacTIXn9ZBDoOj%252BmK8TccaxnFM6bRxFgNVkA0kXTlj%252F5IsBALGXttucqsao7EhviL10ON%252F4WOAinFwR9%252B%252F76rh0VzXojfidl222U%252F5KxYOw%253D%253D%257C7UItAgzzTeg%253D%253Asy8xY2z16bhBsEfdXdzh06xbwJ3sc7jj8ucy8neOx%252B0%253D; datadome=ez7zXV4GqhHW6Sxv_f9kOHKpzfOLPZHduU8RtyKSR2lb6nk4gH~Buv9uM5MENscpoaET9c1CGNtT60Zeornww70fPULEWzLdHPPJ9d~KYNfyZ4Sf3ybJnlQ7ZbFvXBU6',
    }
    region = "us"

    zenrows_res_proxies = {
        'http': f'http://68C24RCjsFq3:YF67LxHnCPRwc57_country-{region.lower()}@superproxy.zenrows.com:1337',
        'https': f'http://68C24RCjsFq3:YF67LxHnCPRwc57_country-{region.lower()}@superproxy.zenrows.com:1337',
    }

#http://68C24RCjsFq3:YF67LxHnCPRwc57@superproxy.zenrows.com:1337
    file_name = f"{hashid}.html"
    file_path = os.path.join(save_dir, file_name)
    if os.path.exists(file_path):
        # os.remove(file_path)
        # return
        with open(file_path, "r", encoding="utf-8") as f:
            html_content = f.read()
    else:
        username = "td-customer-fkYxy1pw8m4m"
        password = "us0im0rm9b"
        proxy_server = "pl707oea.pr.thordata.net:9999"

        tproxies = {"http": f"http://{username}:{password}@{proxy_server}"}
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

    res = Selector(text=html_content)
    service_name = res.xpath('//h1[@data-automation="product-title"]/text()').get()
    if not service_name:
        service_name = res.xpath('//h2[@data-automation="product-title"]/text()').get()


    if '>Sorry, this product is unavailable<' in html_content or '>404 Not Found | Viator<' in html_content:
        print(referer_url)
        print(file_path)
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
            offered_languages_str = ", ".join(
                lang["displayName"] for lang in offered_languages
            ) if offered_languages else ""

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
                                    pax, sm)
        if not json_response:
            print("Getting Wrong Response in API Requests,,,")
            return None

    try:availability_data = json.loads(json_response)
    except:
        os.remove(josn_file_path)
        return

    tourGrades_data = availability_data.get("productAvailability", {}).get("tourGrades", [])
    if not tourGrades_data:
        days_plus = 1
        max_retry_days = 5
        found = False

        # Convert season_date string to datetime object
        season_date_obj = datetime.strptime(season_date, "%Y-%m-%d")

        while days_plus <= max_retry_days:
            # Add days to season_date
            new_season_date = season_date_obj + timedelta(days=days_plus)
            season_date = new_season_date.strftime("%Y-%m-%d")

            print(f"Retrying with date: {season_date} (Day +{days_plus})")
            if not os.path.exists(josn_file_path):
                # Make new API request with updated date
                json_response = api_request(josn_file_path, orion_session, zenrows_res_proxies, doc_id, season_date, prod_code, pax, sm)

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
    # print("tourGrades_data:", tourGrades_data)
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
        if availability == "UNAVAILABLE":
            search_data.update_one({"_id": doc_id}, {"$set": {"Status": "Not Found"}})
            return

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

            MARKET_TO_CURRENCY = {
                "US": "USD",
                "UK": "GBP",
                "ES": "EUR",
                "IN": "INR",
                "PH": "PHP",
                "ZA": "ZAR",
                "AU": "AUD",
                "CA": "CAD",
                "MX": "MXN"
            }
            MARKET_CURRENCY = MARKET_TO_CURRENCY[sm]
            if cueency_code != MARKET_CURRENCY:
                print(f"      ❌ Getting Wrong Currency....{cueency_code} --> Expected Currency...{MARKET_CURRENCY}")
                os.remove(josn_file_path)
                return None


            hash_id = generate_hash_id(start_time, season_date, service_code, Supplier_name, modality_name, order_code, custommer_market, referer_url, variant_price)
            print(hash_id)
            try:
                list_main = {
                    "hash_id": hash_id,
                    "htmlpath": file_path,
                    "josn_file_path": josn_file_path,
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
                    "Contract Info":"",
                    "Incomming Office Code": "",
                    "Transfers- extracted info": transfer,
                    "Start Time": start_time,
                }
            except Exception as e:
                print(e)

            try:
                product_data.insert_one(list_main)
                print(f"Inserted variant: {pickup_point} | {start_time} | {variant_price}")
            except Exception as e:
                if 'duplicate key error collection' in str(e):
                    print(f"Duplicate Data: {pickup_point} | {start_time} | {variant_price}")
                else:
                    print(e)

    else:
        search_data.update_one({"_id": doc_id}, {"$set": {"Status": "Done"}})

def main():
    with ThreadPoolExecutor(max_workers=1) as executor:
        docs = list(search_data.find({"Status": "Pending"})) or list(search_data.find({"Status": "HTML_Done"}))
        executor.map(process_document, docs)

if __name__ == "__main__":
    Max_Retries = 100

    while Max_Retries > 0:
        Max_Retries -= 1
        total_pending = search_data.count_documents({"Status": "Pending"}) or search_data.count_documents({"Status": "HTML_Done"})
        print("Total Pending...", total_pending)
        if not total_pending:
            break
        main()


