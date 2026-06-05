# import json
# import re
#
# from concurrent.futures import ThreadPoolExecutor
# from config_data import *
# import requests
# import datetime
# from parsel import Selector
# def process_document(doc):
#     try:
#         referer_url = doc['URL']
#         doc_id = doc['_id']
#         order_code = doc['Order Code']
#         seasonality = doc['Seasonality']
#         competitor = doc['Competitor']
#         sm = doc['SM']
#         pax = doc['pax']
#
#
#
#         headers = {
#             'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
#             'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8,hi;q=0.7',
#             'sec-fetch-user': '?1',
#             'upgrade-insecure-requests': '1',
#             'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36',
#             # 'cookie': 'x-viator-tapersistentcookie=517e4a51-f2c4-4cd5-a176-192a37fa610a; x-viator-tapersistentcookie-xs=517e4a51-f2c4-4cd5-a176-192a37fa610a; SEM_PARAMS=%7B%7D; SEM_MCID=42384; EXTERNAL_SESSION_ID=; LAST_TOUCH_SEM_MCID=42384; profilingBeaconSession=Bys%252Bn65YBPhGkotQzxI%252BDA%253D%253D%257ClJlsTjui2KpKu%252BxHMFXWMXe02qTWBOAVdMQbmLawVviBfu9mvI7KtGPDVh3tjcpvIRKcod1P0IA%253D%257CPDCYKN90d8w%253D%253AMAfABH3MGFMyU9hgmxuNcsJyjxCSU704klwH5PE78Gs%253D; OptanonAlertBoxClosed=2025-09-10T11:27:19.554Z; _gcl_au=1.1.1768072324.1757503640; rskxRunCookie=0; rCookie=10uilvjlqc4q60d6ckd6epmfdwafwk; _cc=AcRgRniBHe0VKSma4S0xWENM; _cid_cc=AcRgRniBHe0VKSma4S0xWENM; XSRF-TOKEN=48c56cf1-3d71-4e4e-8a1a-02f1d035e7d8; ORION_SESSION=X6D98iQfDjsJ%2FvYLD%2BZx1A%3D%3D%7C3gdbWr0rYMP%2FHiAyre064wG5IdqXMJ7Y1RIR2ds%2FherUm9lJ3QZz6RCeDbQ%2F40vWhgWKW4BP5aK%2B6a9LXYHzucaZqz3ZgL32rkce4pirIB26eI2zvJ3n5ZCMNZTzKiPG40OAZ33WKPfD4iUQTZh84%2F%2BhkADdGNTXbX%2F2hJJZwn2m7cCOjqnt54olDqH1yLIQRijHJEFioZ0oBVBsBvdf7BnBxuQckiwgavHT9MluqlDxPygNtV7r6dOZtVZLA91KonoMW1XDQ3zX2HM1ouv2%2BCYIAbQvF3qNk7T0Nni31x6efE7NwtE1W5DHDbw4cE8JJGrMZtDHVBr6gcASDdesTYjskHikbuqGucryI7NhkFB42KocBxmKe9Ujo%2FFGIxqWMGi%2B%2FSv1nDOw4ykMjgYvYyIw9hd%2BuWTShOy886VcSSyp49hLoCADGG23y7Q2eRCe%2BAYPtdxkMziutT3DCk%2BTF6U%2FCKQyWYyWFd4pakfx9b4C2Cv4B2b0KNHIqsJ9u2om1jKZ48dZXTp0M8nYby%2Fb8p0xFK3yx67e50eB%2BMYSyCU2vrAheoXIukEOmqRQT6RkXI7cLEDZQ4W%2BOBTQy41WEg7q6lmXelXjaMDknAcLGAgyBdeupRd50lkrrtynMgQPvMO5cEMP22wetB%2B%2FyWh6LkgYhnWvwSUk%2F4wIMEnY6H6YVnsOZ7oDTrL79qd2Qov5pqbWT5IJe9GwnRJbX1r22KIijaegjEyEmYcT9Cj5h4r28PJMygINEHDwioL0rScIxtFfNN4D5iGGCHd0YQHoCQXI4Z8te0CoHxUHF%2BfhkWrSzMgY%2Bt%2FsvM0NXjPO1Q5iP3QH5noC8J9aZlfna0eQubfz9TgTqXQiMIJupPYjMMZ%2BM2dJ7uaiiLjziIaD9md2SS7OVSV9vOT0CBRD6cr8lSZ5hKsROi%2FHc6fkAxFNsSugwJoXr8Y6EhFwnGIIu6TJrVpaGrT8PuBZpumZkpxU6aB4OwlwyBnCg9oWXY%2BPTbbiBJ6D%2Fi6AqwSDOGfJyWqdBUQ2999wR4IaAg4nRYYfjfFupMTiDdil2Pp%2FueT7tB%2FxIVb32SayNV%2FJAnGOU04my6A7OT9Ku4gXnpP9dtz%2FfSfMUq%2BnXky%2FQVvdLSrlQXuPUzkg9NFdKIfOvVC44YPgG91XOUKnnmhWWplwoYsUdUKWivIvt8qAbtMvstQtEQfMYj0S5OucS2GueWm0b7z17nP1mTkcmuexNIQxJJvYoCFYe3rbKMT9rJqKmh467A548HUveuOl4KWqERHUC4p4SGGmCEPVkT6FmoyxvAc%2FZZAl0OV2IMG%2FvDxwERkRtc2%2BM235h%2FVULPOlAiAtJj6Ink9CkT7N6qjZ0fKxO9uHCzgZ86FDWrGnOfgUEcIe%2BabMgrUzPuMsQSqxhirmlhXzZCYUOY5nOAKh1baI8hjhTCP7nPZkBrll3uZ6ym3UpCIuuB5uWWYsraAZuysvEQnBq3fqbBZd3Crgmh0eB29G4woysS%2B1GfgHLFncaMI%2F037xcqA6WJkqPcsPTN2yFfwMVcZD8O15pm56fT7vogq%2BTaOJixqyMZnu2hP%2FWjcna%2FDW0iAFSgfW7P3i7uEFvtm%2FdRhXy%2FKToMStWvRhn4HKN6yW0ZQFUOs3MyhBo1L7f59uZQ360Lx1RB8zWExvFUaOnFgOaB%2FaFX8MKw2FZ7uUdLeERpL4KoGd1bIEiJyXkcEht5hbCn89izzOJd4o76pVygByarDwXd9fg2n3QmZwV0rPzgcfUs7CJ4I6vbAISerydvEFR8Ou8RcKwYdouqUGgNYOUx2lt3JA9T5kaNE1ZMRS9QC66P2S0uNmuuurw0MR%2FjCubqDI8yUaTbH%2BSNjlitzoWR3grssGHoPKlSDpNlBoMWcacXUqV1Mz5lgxs6ng4LHXiwixtrhI1x6NH4VvFCcYlfp%2BbcC7QUuMTIbcHC4f4s1iNBZexdUcwTzwNXYtn1GeDkKBPzIA1KgtCSOVVLAkKKIMPVUNlVYur1%2FIB9C8RrbHEcpYu1C04wSK68T89%2B5CkxusmVyN%2BxO3ctwFAr319nQ0mQAj1buEDVU155sv3ahYu531WxFlJ4sowSEaaboCoeqvCob4yfoNujYURmQw1i4NOkJItvklSMHQuUSMvVoLudU55kErygCkFVrzTlWohMHRwRlu3j5HckgDaUl9svVKpweGagcrNh1nl7wI0Sx3tMes3b4RA3ok1lhrqrQO64vIQLsMihHVmDIXWUe6%2FRG88WjTPfaYM0kp37Z2T0iCpmhGy3wZ3Cu2TPHv9coavkd2azk%3D%7Cf3DDyJVNnV8%3D%3ACPZijq3WKnpnTmQMKd%2BmfM7blpHS3QxIuqZifdq7au4%3D; REFERER_PAGE_REQUEST_ID=A752A023:6E8D_0A280747:01BB_68C40B08_1449FD1:1970D9; mp_d7f79c10b89f9fa3026f2fb08d3cf36d_mixpanel=%7B%22distinct_id%22%3A%20%22%24device%3A199336142e2b44-009824152323978-26061951-144000-199336142e2b44%22%2C%22%24device_id%22%3A%20%22199336142e2b44-009824152323978-26061951-144000-199336142e2b44%22%2C%22%24initial_referrer%22%3A%20%22%24direct%22%2C%22%24initial_referring_domain%22%3A%20%22%24direct%22%7D; OptanonConsent=isGpcEnabled=0&datestamp=Fri+Sep+12+2025+17%3A30%3A19+GMT%2B0530+(India+Standard+Time)&version=202402.1.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=c60ca1d7-7736-4b5d-b53b-f179dc5b3791&interactionCount=2&isAnonUser=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0003%3A1%2CC0004%3A1%2CC0002%3A1&geolocation=SG%3B&AwaitingReconsent=false; lastRskxRun=1757678421262; ORION_SESSION_REQ=A752A02E%3A35C4_0A280907%3A01BB_68C40B57_160AFC6%3A220F68%7CA752A023%3A6E8D_0A280747%3A01BB_68C40B08_1449FD1%3A1970D9%7CA752A023%3A6E8D_0A280747%3A01BB_68C40B08_1449FD1%3A1970D9; profilingInAuthSession=JI%252FsjIlHgWLMac6Fc4tWMQ%253D%253D%257CTUbKoDx8Gfc3n0hz6OjgmaLBQnj5udigaekby6B0IYA2z62DxCB1G2%252FPFtr%252B3CMcydagDRnyEyWUHA%252FR9PAO9D0mYLFD7ZWtBEJdT0bKHiPPM4ZTcw%253D%253D%257CkkcIebFqolU%253D%253ARDRDaeZ3XWDmuodXJeMR9KCrLc17LP93Saz8WxuSyMM%253D; datadome=MkcpfINVmsH1_2tufRXsfqCvMYyoXRSpIe6PZXY1WqPdU_1vPuhr6qe~x54aN5_DU~10j3AU2CmIFG0NytZpE2F0itgHYuGFv~dr3T_vkeRRJ_FMmie6i~04w7nsEVBz',
#         }
#         region = "au"
#
#         zenrows_res_proxies = {
#             'http': f'http://3dbxcTLYpHGv:YF67LxHnCPRwc57_country-{region.lower()}@superproxy.zenrows.com:1337',
#             'https': f'http://3dbxcTLYpHGv:YF67LxHnCPRwc57_country-{region.lower()}@superproxy.zenrows.com:1337',
#         }
#
#         save_dir = r"D:\viator_page"
#         os.makedirs(save_dir, exist_ok=True)
#
#         file_name = f"{order_code}.html"
#         file_path = os.path.join(save_dir, file_name)
#
#         # check if file already exists
#         if os.path.exists(file_path):
#             print(f"Reading cached file for {order_code}")
#             with open(file_path, "r", encoding="utf-8") as f:
#                 html_content = f.read()
#         else:
#             print(f"No cache found. Fetching {order_code} from web...")
#             response = requests.get(
#                 referer_url,
#                 # cookies=cookies,
#                 proxies=zenrows_res_proxies,
#                 verify=False,
#                 headers=headers,
#             )
#
#             if response.status_code == 200:
#                 html_content = response.text
#                 with open(file_path, "w", encoding="utf-8") as f:
#                     f.write(html_content)
#                 print(f"Saved page for {order_code} -> {file_path}")
#             else:
#                 raise Exception(f"Failed to fetch {order_code}, status: {response.status_code}")
#             orion_sessions = {
#                 'IN': '73jGf16hJ7C2HYadGiRJ9w%3D%3D%7CBFbW9h4ry9tSn9VEIuIAUtGM3Ihhlckj8wJ%2BGqMwJpZIKQraff8NalC90L6MIirNIYKZwgITKDBkTKdIcG9obtLhWCBc4v7SHHV5XZNPQhZ95rbKKiFxWBXC0FF%2Fi3edMQ9u5GPjYCMnGUlatuYRckxdUQkQn9s6feKNE8z%2Bl9%2BjpmxhTai5kd3xd22MnBHJSzKxOR7xDN%2Fzh%2BYxCSAqy6X5nH5YfcJVcEhk0Kmms5sc7z3K0dhTjZh4o%2B6FXbY2b0SYgndcGmWg%2FZI8UIOpzGTa4%2BMsvHQRFspBkiiorPywXFg7tw7%2FuHmfGHXOr7VFhTPK06susq9xtSNGscduBRRuBTDi1sqKJjYYdVpY26Qfmt%2BWTq7Ji3RZWNBmANdnJwNxWwdLywhdYfV6rYIxyL5JAYPQiNo%2BBzKDWpbeYlIefwpQlguFZLrQ37Ru6OPCS0vxDtItHMPyd4byfp3ZMH5hUAzWw%2Bf1WEt7FhPknk3yfiTpvsnk6qBbSTPS4TVRjT8AsKfZmg77M1xw2evf6fKd6HnQ6Mwl7NvUEk23wTAqHaQfhmWYweQWoK2X7Bpk3rNM%2B1gFOMNRwS3H5qJPKVljj%2B%2BL%2FDHlwS4jZML6vGCsC8MK0vv%2FGBm5Xb2t2Qd5eL0CY2u%2B4Uovq0BPY2gly48rohsA8XbLdmEPTdfcBuCpce04vi%2BKA%2BDTadG%2F5JXxJbx0ladHzhEEHfBe%2FVEjLv4uaP4VktMbX%2BxtwL8NJ5aqUzmtYaoWOPq8Ttwx%2BNOF4zHfFkL1Ast3MZTQ60%2F9VXiv%2FHMSgEuTSTy1tnto6AqWiXazwXXIiOOVr6h80rvCODcmPqxPp5YGF%2BEqpv0nUG4kjNk4m3AslqYoPkJNYeehTrWqhNXw00VOSUXZvNUFFbb7PJ3sKIAYnmSOTaocQTQXgoOO22KH9h6OsGrN3DJ6e3G6HAN71MxCjZM3p84jPImcW4c9mpb%2BMDHfcvVnQyQJM5sSZMEUbEdVHqMndgQcNzvJ%2BYhaDO38Unz0%2Fig2CDl2PdRNOPjLHXIZpIwat6fThKy%2FpknTH1Tm8ib%2BhRSUFpHQPiOC0LcfXw%2BghccUg%2FA4TGjQdCsdcAxQ40AiRsN%2FhQPnxJ960tDI2%2FGbY1ru2YEsS5SmHefmU0ModywItNvi5boJPOKDpZHxTk9TwE7Vr%2Bf96D7XjL81u%2FPHkt6Dk%2BLi7d7n9EEL0xfbfvw0D0cb8EZCBUe1KrJw2jUpm%2BKPFtS0z9ckZBR6aHXn6Fr0%2BW0GjXdCoUnUl%2FtCPiT2C6LlRS6SjaMvgEr%2FIxe8dTjp3pSy1LGeNUmphRdr2b6DB8rT13suJ4TNyhnYwYaUJAO9fih%2BZLvSgcuUvz3cwwEn4OjmB96RUlYYs6N7FEGb0aJMeWfCwd5WfKH%2BGCio57utd09mFCgvZtV%2FRc0%2BRFshTj4LLiDnRnbcFioGxqZc0IK%2FC8MvLbpwsp5lnJK%2FyRhtzoX%2F6d756Q3ho%2B5ClJGb6AcHLbdRwxRF%2FJtVNnacoT3TxTinBCzePYHhTYH5FXH04kGmFNYkUqhed1uzj%2BJitoZZPtlMrG0hioa65vghaOSGWz0Y9K2jkIZHVz9sVUTEDMduCV4czQ4Se4NGDwfJtfsrr4y%2B7L18vwfpW97x7AlbGiEQWyFtscW59bpiFvqoLCXuKACNNaVmqlVOm0%2BWAwRjWlFDV87qwCREEEDTdU6aQj2etKz3Wo3y3gQHedF5K9S9WPkUuzloGFFReDePYpnfhcA1fUpIFWRVerAcNdbczzC9zHWWcb2lztWnWvUWaexG9%2FrZwdEjAqnmX9FQYg1XwApLn0v7egDbc23bwb3a%2FDSlc06PzIWGDSMBdVQqWO7dBuKnOIxACj2RhiqRFboxHyDJaPw2sOKny%2BZs9quw5R9gAL%2FGyu%2BfLG9LjrXCORWh0oWlSzDhxmKk9i8E00q2dt7wjWc%2FVJcu%2F6XDSqdjLeog5yp%2BNOyfIJOncdk9lKlQjWk0AdHKqBMufgb3H%2B5wxkjdLkVjIkz6JHcMNmgCbNeiAEmZtbYxzzBOA8DngRIP1bEF4fX%2BECzTUxT1y5aWac1zh9Fw%2FttzykTGzm9al9rKj75HVHF4Qv7O13NFleq8JFJO%2FUaZzX97%2BGhIdRR6rKoEZDmTG8xJTRliR9WLjzYmOI5TDYJaSIJl7p5JDl78cx1ZcbOfrNxjy0E3z7jasiLiJoGLm9vpqV4RHGrwZeEXrxqWrnyPXXuAgYO7o2e1WmAezqNxRgoeRG1Dg%2BjcdiDUHKnWxDRIFhDmXU251XMRw4MkuQC7RTZCL0LfbLvpdhAazWA8FgHGZxtL5RrMf3vma2VjWN3Psb92vNSOCGrgxB08WZODjVBxMpWB%7CWghAjFPPFiw%3D%3AvOv%2FLwkEQflQKEokzhv4JpnlbBKz9HIEmyD%2BOHcaKuE%3D',
#                 'MX': 'EOQFezi8ORTkRxKzWC1f0A%3D%3D%7C5X1aeCUvRlDk6FD0t80FWj163G9p3KQBbkIwS5w6O5Ft%2Bo8UBgEed0DRCHZBlDQCINckkY%2FLazEqWyA7ZXvliJi3mQ3tgGp6T4McJVvSD9EdxfLKXrQtK5UHrFlmtsajetxhs82jsFIKUCBD8K7sJ0JXYBjYE35H22o5f9FuFUZ%2FUtXKWc%2FEPremhGIXh2Bf9uftF2w49E7kFvk80fO5u0xAOwqbjzBONL2qOVIyMBNulZUT934Lpx2hnGA8ABnDyAP2aYgtMakj7H6dI52gwGGY%2BWoGmithxnJkTe%2BPj6w%2Fk2iUEhAlSj6zpgfiZ7uQjnp3iwmRdUO%2FcVV8v7LxH%2BXQdiQe22p0PRtbgDCjjIuE797DVID1CDK%2FNB9NMZwE6NdwFe1TUpomlcDWrcY2sdOq0Q9O%2BdMrXWWIH22CumAwNZODoHQtEO36FZ5aKFbZixfgoz8Wfe3eaWn%2FD9Hc6RyfEMGGeJA4dtHMr2D%2F4%2F%2FknIzv%2FJEjG1OnGVfHIW8bZ2sVes3R77CTW4vfLFSGnkqU%2BqpaQfv4T%2F9vlGk7QyRXTcxcoAJ8kmyGcFbPxapes9brGDfadLMO%2F0l4V3NlM5%2F5%2FEzYTHNGSta2Cvur4IckWMYYNE3sTwrjXjTDUD%2BH8HILmzoyhdPwCGyiBt0vy2aXyI5ptw7y43DSwreM0Ue2x%2BjwlKaNCIc%2F4z5P3u625kKaM56PW9cG3etjrcwt48DJxcWuSXMsdZdpMrpX%2BSHsUWG%2F7ta103zpF7c1VnUnXzrsYS1nRZMDmXycIkPHYHrgAUEivo3eTZbbJQan7PpUfbt27BxYGFwV2sVnShnQ4YkkZR4O9FV7KpDgBSVZ%2B%2B2wbhrcrmXiBR3V26h7SnE6WI7TGGlXqGsDuH8roMN60zS5MpU%2B1V%2FLppiYeaJ9TMfmLeifqFYQoFYmbLAey6cOIrUI34lm0HB9ZwDWc0AYrcGpDO8EeA1NbFOdd%2Fe46KwU0Lrj%2BfB8APRSeZ0jSznu5jfgRgrlVqyLeUoPrX8gYqp3XfIeDJ3KgEEOuO4Q29KwPGeBx7fVQ6HsEHhPQiFwTz6Y06oRkjIs2Z3TnWPYE4S67J8QDaObiBzj0tLZHUPi18hP7s8BeKxqG6n0OZQwkad2rUqyCAxqRU2sQDkZIthFCJSFInZDrK3jJiik6%2BSlAgPEsdNYwrQ%2FPXGKJIhhRyVk3oEMLhlbwGwN7DaK7RGnOq4OVHVYo7A4ZpdYfuADpj%2Bp7I%2BOzbPa9rUtBNFIMUuZthh7bcutif%2FO1v0tiVrfLi2XjRbPa6zb%2BXJj45Z7qjvgb3%2B2UTa2euLUCbIkdo3Wl0WjY%2BNw38IvQUwKWGGMrJD3iwWeaIjAP6%2BiNmtbW8uF%2FYz7GpavsEWbNbUpSjXHlImptBRQRIU%2B7haNHF%2BieMF4CMELOCqDGXPP8fKXRUWFpEpwz3iKJNMJuqbYKsvJwXJqFSHfluJ83%2BnZCddtAv46eLqCeHrBaKMvSeirzZ8lyE36WWZ9JeMnO5KXveu7J77GnkgsSiOnnIwCNe1YaRqKrQUlvKJjLqYfn%2BvEUJE9aU5l2J%2FjK5og4v0vQlAIQSloMdlqj6%2B3qjwc3%2FZ%2BKNhiwElZ%2FhJx1NjbWAcvdg7CRkX6fenwsF7uA6G3E1CwmzIgjKj9tBASeXQg2WTDruGX%2FOIWNp%2FF9mSkLRrEAyR5XAtFfa0dSQM6FoDbDMsggSsJ9wV85Ztv2Kix5PdVKSiTfBvwWRn0976%2BqLZhYmLIqnHlffZU75zlPysCmIJoFCgYP9BuvCirmHlVda1bVj92RSxZKSXh0KGwtbf2nPuadN4AtzvqTbHtbbPyEV0j6L4Wv4CLXI3Vru%2FNRRp3nwZeXrqjq3ivKBuVjRs75pgrCJfQ8dGfm2Lk6hxC%2BuZpgm598x7i0x4%2F3QjWh0G902nMVzmuiGhVjPNndAezVKYhmo2rZNprKIJXFfyt3%2Fdjb2PsDzY2UY53IW2yB2f7qO6nzbi4ijFRWXYREYw%2FWhYKPzmXDh0FVj6V77H1d3L8kX9yqgFR%2BD6m9vI5lbSmLyBVht7%2FnRN5cqo5rmvTyHPbUm5rmPe5%2BG3BX1yorSgq85qjzCFWtu0hoEDf4HXybgvcJTzPnrkBPr2iFLguwZF3rp9Yfohzjd25dhnoJ2lZL9ihLNkPkAwuast%2B6EGlk6NDG6xDqdv5Sfg3Nuwrz%2Bf0%2FoFhjFVTxjH3J2n7wYO%2F9Ez905M%2FItAwmq%2B%2BM2WaPXpmr9DBB1sOykaH1TW7%2B%2FMxXEyr1acCIrtILumbyr%2Fvbzu1m0iE6%2BuQzxsG0rehNisQBa1DEQad03e6oS%2FVFckEnCOIt7IuDIEBjlQQaoV7Hzj2%2FYrhVfM3u5XTrLzd%7CbCR3Y%2F%2FELF0%3D%3AOmD3DcVo364B1MUTdwxrpFPQhrX8AIOvLFmt5v%2BTn5E%3D',
#                 'AU': '%2BcNKf%2FzN1Io2TJtp3L5lXA%3D%3D%7CMjPUrKqBr0%2BSA%2FFLZ0HLZYjtBc1mwHAJv5%2FVtXAp7uRHcvjb%2BEOVwM%2F4CxHOZbFJPb02gNkMyf51eJX3jf6DMX1B0W9TCHTg5suvSc9i69H6sVqr76%2FOLIZiJ%2BtRQVgM4s6bAJHBNXqE0tNqFcE4EiHlkR2gitNadSDcCVGZYlsmiAGYsibwtCsxGx6KFiZNN8Nqn%2BG0k2CegIVxT%2BW4cAPXZyQilg1w4njByi5Lm4qhxvYilLvlxz9qyOWgnf3O3sq2s9FYRfgvSpElObxL4GyTPor6pwnGqMPljc%2B3tzs2awY60F5cPeCX02KBWUVfB%2FScJ00pJeEYubam8L47tP%2BVW7SJyaPsjJv7Dd1DfmEmo28OHR47NuqHSDMbCXk423eadEhmZCFlrkQKzclcYpExwT%2Bxrxggg%2FSzCKt9UgQd%2FYIVFPUggmsWtnIZUMMynqKwQZ6Ey5zqVhnyRP52aafSiIhfQnZlabGnVGccqIdRVoA6RwAaS65E9jziz8NKSxkne7%2FHi1XrySvzDPiVoaWnWY6D3Z4wAb2JNz4toOYeTvYHmYXDlqM0wp9oT7Nx%2FgxxcZBah8sDdycX7TuVGrBBCqE7d%2FXOxiXHdLutMBBaFg3BD0hkT69tuKEYk8F51abaJQKGZYB4D9BfeIN4k3m9PmOjwIRlS2zl9HEgAXy%2B8Pd8BU8jrkVT8SxNDN5DBm54pP9EWa6j3ZIiEaqTdtnFktFg6QYrdLOsvJ0QLyJGFkr9DQSr3gD122YFUhtsp23bsX75ihpfqsdJozzM6GLlbO%2FfxjjiXwjaERf7tx1ZJvkgOXATFocvkUNU9keYbcgbIAqQybDq7WW0rtltoRXJasz%2BrYRWIfNVIUkUjPOwijcP00dpJ9DbKWcpNpn5ACankaxX5w4EQQUo8Njpfo5U5ZRl1eqcZK84dNIkzaqaGQ3%2FBptri5qLepurEmJCkDBQl8xg%2B%2FrHYRlUVi0FoBPsaypD3PE2H2Gx87%2BTxurHajeHp1BMIxjhUIPENJRzIqNC98mh8bJkA43Vm%2FaxfpUBQtwlprUxUlDTNyW%2BDLQinHTbbZ2%2BEfaUAW03aqwG8%2FMa2jjt56cWvdQXYO6uhDzmKbFSvzlVZMxBlWZuPC%2FpoBD4FSM4hu5yJC2ivir7A7clEUWGddAKGC8DNzCMvsuXPSjaMqUkjsP2DAfR4IhXSdaf9Nck9%2BxJX98ClQojSU4hKRNNowuZOiEUsyU9fLcGSmNKUVFsGDlKksatbg7mmMoDqRtmCg4V0UpXIhzvX0A7O5ie3RQtk%2Fg0qh5x6N6u4qdTfnHle9TR12uRoBAlV%2Fb5M%2BPGtnVoBmNWb44762f7bKnbd8w6SRhnyH1hY1X2hNWLq%2BGmk49NcqZkmpwYf%2Fb1VUwl7WvCpRBZDSjDusL%2FMXqIVbuD%2FDt1A4aZlyB4QqMq1cMZ%2BaLMi4i%2FTgwc0a97C0urB%2FDn5XmVhb2TXR%2BhT9sBi7JldUBVub2YzEEN0skOoi1pfffSKBebnU61LnvdH7XWK5Bu067ymc5khu5%2BHyd9f0exqtLViKkGlWiL1epkBLhUu6QMTCn0XgfXezcb%2FSpHzdxNq7LQiAbchiUXbuQ6F1UG4n0LUuLhajQfvmppPyyD68psyX0MEP0EtVutV%2BxmFgyAWPLDmOV9bTsyPoynvZMaX3EnCemOq7C9jsxoMlw%2FwKsWK3%2BjKkltnP5dnggYH25kKPsqBTMcciL138%2B4oYSuCSp2K3288gvf1bAoyktq7x989bcF9mZeetFDR1mkPJuvu7yfhzgR%2F6ShwluNQ6eOMmpIV4Ho8FmYFmh47XfoNPb6rUALfyXYIuD4jgdzN%2FyWBu4bsixB6XFvnBO%2FJjVlK79LwkibLBbR%2B%2FFqnnuPKKOnjxaH6IReqTeTCN6qODiuqfvkgiIN7T2OY1XVxk0GI4K0ypqvpLT3qoahLh4eIW5J7v0BEf65XIWd6Geljt5eE99VCIsYG%2BuW4rUDOStZUkRXhQ%2BgypMkV8iUiprambOMP%2BCXWrm0H9btZnTq01Tbgfz5WYwGBtKLKlxzwu4sVmnk904hR7ui7BNvxzpTcGp9L1m8WGG4kELTFqOwa%2BTU6Nau43l9ofFZ7zmRFUfOpfvPFfk9B3XKMKyYSsDktfHJc2AapTdNaVcz%2F%2BOcnOGQf5vzrcwFbQVP5UCYK6GaVU2QE%2Bfpio%2FcSjd3y%2F%2Fj8AlE8tYWiqmRobSn3gHR78Zv2JVVN9yIx2DpTl8O8HBt1oJqNQPp%2FQ3Lg6aWix5OgCJpUoH9kcGhkCo0%2BJ%2FAgU%2BSciCNI0G98Jr%2BLk9vuj2xpkV71RU66mwmq8qDEfqkb%2F%2BCkHxlzhlat2ExnHlPZyngMzwlgqbKfp%2B2%7C1yyJ9lRBNbY%3D%3AgaRHTgWFr4waDm6zsydQ6pvRsZux29wSgSBgqwq66oA%3D',
#                 'CA': 'NjGLrA7cVWfiIQQcH93xGA%3D%3D%7CGlUXohRvZmHMtqW3lMpnRfLVgGNGMtUE9sK73PIDTw%2BAhtFLVLS8D2c6afQtkglBT5xv1xrP%2Bq%2FyicZqRYWUmBwASQNjkx6y2TOpuaUBhkjTm8mLw3tgnUSbrOjWXsoUzkPE34MLRBpH68JJTQPzMAYqnHdOcLoOlkB0HgtmI2Fe3QafhZ%2B4aK%2BNwXmV1E%2Bn2xNZ0w%2Fjb4Zu0JP8vj2k8%2FfCldAP%2FLfflhxKpoFiGPDRQH4NVki3MLn02gUaoOVvw80qpM7ui%2Fkq5A1dq7eFy01NF8jNAm06Nw9q8h2rHQuxj%2BfyRdUk1XgihSdjxTzi5R9nUX%2FrAqD6gteekfQ7wIaYt4ePfm%2BVJKFpN6XLp8N7L5tYWy4kCtPf6e1i2UDgvrpiOckerOXW8der8Q%2FzjrNI%2FFWvXLcFc2ugxluChpZnzrWUZzXZ6T%2BXtQlrBZfnZcdqPPZBi9ejNDlIPI8SmuB5bJzJW4KK0w86P4C9fJFzL9jqrxi175%2Bc1kn0VICIdWzA3Jf4gc5cPN7BRV1%2BPdd5hqn55uHFPzJurYxWHvTlNqbNBmavZ4Wg6ZLn1sIEG%2Fw4qGnJLTGYRXIKfp2Qbw2e8Ub1FxXqELrSWI%2BUlLhz%2FGFsrirSG2dMri%2FFa2AEoqU4LY8HylL8UFulNZz6aEnz33w9y1vY1FS7VQLnlP%2BP7Y8CNQPnCJ0sHr8Vj2QtQs8ibZjEi%2FXMoZyTxMb1zo8DVgKs61po3xoBDNb0uT1UnphmRN9m9TohMJvM7pDFyeg0TPfXIC5vbymR4PU14aOQqZwjMI3W5ESDSUI6YQOlEGO726aaR4RbxpN86S2GT8izWMF1KMuPxiVBfY4DyXFPT8u0DCBj5xJhKiC2AHJA9ma4wGNDNtv1%2FpkTOp0sxgg4%2FzWRi0gNfW2EPaPWxBKos%2B6j6G5EPDBXdcC2hduXVEdfz06hCAAbyb0NleAyQJAEgwTJQdH7DEcI4tu0ZAWC668q%2BzRI%2FoI5rCD6MypAPameHEv37vmeX78DgfKW1CCuDWhNmWlJbEbWI9YrVC37oQYNbSmqG2jOo%2FRyCGxxX9RC3G%2FFLQZ09W4NdUD2riUWFmLyu%2BxJsyQ9PG15NvS9C%2FMr1qWNRBWIUM%2FHihRDt80vLqP2y4y1bu76eOogncjoAJ2qmC%2BcBMC7%2F9NdNWFEAQoYUG%2BHYLKEruAaeYZnBKr2NxW9kVsPpv0QbJk4WsbnOCfNweeZH%2BAvIzUFx17VaSEvB4ehiWw94Wkemr0xlnLxQzYpTrsSdu1VCmab9STKur4vFAmfYyPsj5byRd5LGJOlBDK03L4fX5zqUwexKuFKmJld4SuxlHLiILARyMhSs5SIkXFmWnYWn71RXANy0HlqHxk7nEr3u7Q06s%2FPXReF9gTsxniruifyq5yKTehatkhX4NJcXkFsAtQbmXJTJ3YSb4X80jpjovkiTY2EXhqCFY0hMOXUEhBdAu25hcpkp%2F%2Fh7WqzKe5GXe1Ia3EAgFPwmjpZcJfHrYr%2BJ2Yu3hr5fML1NQPfzbuDveOW4spGzYILZi%2FhP4SkZQCaEFHLBeLBXtgJcAiRcKxqgKWvMo7fB1GegDDG9iJslJzHkEscOfSVvvFqziepOdtE%2FIHAD6Sy09pt9nk8Gq2xGxne3DZQPFwUjAQdSBXE4O4EWtcBE%2BPPzzHG2bWGRXZoxUQDs91SEVO0LZ9bWRp3c7TYpdS1o03xcuspM3NReiI0D%2FIkhouGHiUXceHbsNCM55WTIISbrEQAh4X%2FQmgn8FoGQ%2FMCkQFB8nVL%2Fk4%2FzraOOcksSM6tARs6NBxgFt3Z1lYXykxCvMnoQB4aifTZ7yvkZipgfpcv3eHcYFMngNX5vCRrn9p8yv%2FPOTCvJVy1TVhlt0w9ygAsZEJwl8ILQVD6fXyw23iFwbQuuODiUJDjedq0w7iDuwW%2Bqd%2FCVgnkBiNkWIVzUzmuvDYEJ3SN%2F7DS%2B1LXHJKPpetRYCqP%2Bk5X0QTj%2B5KKpJUCYA35x5h4idftmiyZVIrfIaWMyFHpXXyhedK0t2AE4SjZOZt49v01NbP3ohp8o%2Bt0RbIE%2BuTxEsl8w5VbvXasX5y3wgU1x6DDfWQ5uEYule1pKPj70dlS1eld3VTJNfBbCtR22fsRGy8pcuj4%2Ft77ETG%2BZqJHbb9ITXYD59McIS%2FVxXiYf69e%2FmHXnZETntad7V2n%2BX%2F6cI3E0ENYgdumOPyj4sAUaBFk%2Bs%2FUPqw3bwkFDRDVKEYOkl4U0IlUGrJ7xZm2Wp48MJo7RMfSsVbGv07NuPxGYBnBIjN4CzqYJ3uEA0P46DTWGsayPXgaUS3SoxGw4US5K%2FLDEMQfXlxfS1hEirpNd9GMTbUo9OdYZgiWgREcrU1rWlAf%7CT%2F7OKk8tjRw%3D%3AUoB0PiIMaCbS60pP8f0r89p8HmLfh6cHp%2BKpxjuUdio%3D',
#                 'ES': 'BHxMlhe5ljTYyg9UAzcPFA%3D%3D%7Cmo3hMuZyAewmjK9hQE7AGSDNmfWYKcB%2B%2Fc4lwkYGeyrPLefCTmf6VDgBm3QSxGzRRI9yfbK5zIuYpicJ1kXk%2FvUBizPyVSrC8B7rPzwsAan75UB4QGh9bwvl%2BTiaEWLRirfySzWrGYsZD8isCWNsFLYz5KA5%2BlOOyYJq6a9QioXmNFg5%2BtLiTR9M%2FIYytAUVKNyNTdUYKAVHFS%2FQwjxnbCxSLPXO%2Bvf91Lng180Pxdt7yMrX5S5stMgphIssQCWMOxn3jCgbZJlQjGT3Ase7SRaerKkucsdO1O7fUUdHdiTVNkzAFA68LxgtoqJIt6pHLGG1v1LfxpXA2JPegM7VlBSnhC1mdtZR7rwBdg1p9iZj1mOP4ch9gXEin%2FNfkeZRpds5JKwdD7znZ0akkUDxqQB9oGvhxQRzDZR5MAVAyR5ywdrtTnG%2BdjVDMsiY2gQ%2FAMNlRCrnqSbSMx6MKlheQQjEt%2FhY5p0jR1W1qQHjwn0ZrD%2BxsZQHQILlJLmjClVQuP72M1fhlY%2BnL8CoCP4vtrBE18x2KeMOnmsfy4ZRj5eOkw6TIBx0w57bYnsGiBoca5zts9BvRq%2B%2BMdGr%2BbUqQjpQA7KzhN2rondBOa7vtuglDqZsPa0Kigko4yLD9HxHOSyARy89gykJuKPj5yfOarDf%2F%2F%2BYsJHfns%2FmQUlfPogoVAN%2F9ZKsROfV3NevmzzJHrQjxPmf0YbbhCWLZiqRgNm%2BhKoYxEAvC4IWN1M39ZKH0kP69Bez1wFVvcbM%2Bdey1n3soG1ybhb%2BIdPj8lmzb%2Fo%2FXix1XQA74T%2BAncWzUYr%2BBaNwPEv3CJdKktupmJZ90vYywumVW3xRb%2Fe50drxrU3kGrEUYLwktv59iSW7qIRgypmO%2FuA6eX74SyJ6jzEfSy4g3l9NSzfnsyHSQPjLRAvCvLFGV%2BZjCVAl1hi%2B0nOXv3ShQEEwrMIKh%2FXYSB4vAlpt3TVAtq5LtsZdFMSvXJRbEf713Ho6TyytVKnRZ3AyMmbU95BtsSJUtTvQUDYNL593zGeAbxd%2FlMEv19%2B5eZPr9aKzcEyaPy9lVmZDR3RWcCT92zqJuyawuxEMUi6P8WPnnDC0yO9w7aGw51GYKBnQDmmDWoDQx%2Bx2pzPV8W3IHQBAjjAjYDLaZXgjstiFXKgabv2xtTLj6XyBFp%2Fpk4T%2FcdGNQf%2F2aS1mPehrpNUPbf4wvhv0%2FFBh497JgUDRPKyvJ68NJ%2BkcmqyLYDEV0jNcdz6JfxGTxRhkHPEmrWQSfAVWjrIqonMYvPDCGOSQ%2F1kJ4mEZAtynfQ1ai90TE5XeRdicW4kukMV0IzwfT15d%2BeOgm1TjoWc46m87zF59X2N%2BCwl6jKO2q60aaeMUmoAOsfekFdnx5JCNGepl7%2FQCHdLbqYcJm307VlbLMvol4ELDKpRI8P9xf3pKGfS6TDnCiVXU%2BEzHk1t6WFSK3k7hR27pNgYW1tcKLiNkiZfbB2cD3yrhCR6YxwGVN1Bjs9Sd%2BF2UOlYCkGZBJvfEGaskLZ3o5O9CTSZnGLM7RGaC48t%2FVuKR7aoPnD32iVdzts%2Bu55Z63cK3NocKD9CVXrOs6OamlrM6iMvCVyYsmrqdmwL1b88u6bGVX2tf9qfDLDIFAYWwSMdHK%2FNEEf5Oc6t17gMfdGjg4urJEjf%2FGsBl57jRK9SfUdiHOwZJyglQ5%2FL%2BG3nk7QQ1QeAPA2khXOaVSqDa9OqRhl4YjZEVeFQ5zsTHHjXfNd5dJPP2%2BhXYQZ%2FASW3i2AdzUHj2ksdNTblyDrI5%2FZ5bds9gUgUYxZRHDM%2B4jjlwZrj%2FuYpzoOCnF%2BDv7c1atmXVhRHM2mvOigEiIRkRu1vgykENt%2FcqJUmuXIOgRMuS2nnM%2FgR7RM7awvKxPY4WFWBkbqOeugdSd3yrqscD1pdAYGujzy3oigI8OKJlS91PiBOYqwWxQZ0FjA4T7VKU7%2F4PXIuItwfC1GGbBjNlCxoncBlX8uUFJidgdW6JpfqXpqS6Zys5gSJqeb6PWQqfuCmX7UkfIas1aHsdzlGFzUmn1Xcwr53xNT9%2B3%2FdpnEjC2aYv64ATwy4KrMi5ehiJhgqiYuzoxJO9GsklKOG3oct133teJcA2h5Kqe1CgVVkBzHn0pKniaeg%2B8iJCo4JnX9fZsFx%2Fr8j2cuOZXQf4DZPR36%2F4EgJD%2FHscBkyiles%2BN2O6cMVt2YGhj3IavOZG1nHuHhl20chY6bx3Q7j01OvjocK%2BIUuQKZVZDSuUuWcs%2BMOcdAEzRH9ua9NYFYne0sZU7M6gMXi23fbATNq%2Fh5MmQakXqES%2BX8tReFmJl58%2FzE50IIDY2OCTEGqgzcmCS8rqdiEwTyddz71Wdm15fc4BrpLnFfKzTFNLIQYX6Q%3D%3D%7CmtL2pzHLCL4%3D%3ABhsBCsUJhaR5Bkwf8s0BebSUgzGfk8wEIXfFUanydfU%3D',
#                 'US': '9GFWSsxPfs8Agogd9iBz7Q%3D%3D%7CThUK5D3fPdLmgUsxoUNjO8l1QnJgVE%2B993y95HqM94WHlNazt9KXtci7zo823bkSJuLsArEYhPBIDDGT6gJBoZpNyyhWgjm9u7j0G7qbGpUAZE6GwNWgwlldR0zgLNPIJwqGdZVv0GogEP0qPoN%2BiWzSmfU2Z5gdwjIP3sJUOWnqNpOatF%2FDgXWjdLDhcTCBZWR2KzDn%2Bme5GVLUFL%2BqPmpSB4%2FpcFJsTGwNg52356nHmtwcL%2BlOz%2F%2FjZzjeeaieeFZHoVbVOs11lpt5ML6JkX8DX9YAjs273D%2BMP5ho%2BmOKUXArPIN0ZAim3XWZSlBxhqcG%2FX4u2ozARDrcw8qQEi%2B63Y7QotxJhY01mJnBqomKW4WP5CNSPnKibtI8%2FSHXjIEgXJHuUI78kHt%2FVurlCuop8gOISsps4ow6YnbFzpom4%2Bu05eWwniGL0kA5DUP991fSCpjjcPCmAEh09zwT68A9k77MfSOKe7defSi%2BY0MMU1TwqNtL0y88Vk1e1Ei93zxPdPEmuNAC7HY5fS14%2FcOqYx1b8BaKo2KfiEhB8nT0upxbqJ8Em7DAUs8zJeup6TgqQFde2nhVU6GkD1lSBeM%2FDrXdmAAde4%2FL9BY5g0S2GoS%2B8arY83TMM9aZ0K%2FGZ705q5XIg7sbOV7rhvJGYbggMtjWQr6NE8Q567aR59VUXvAWK%2F8UIeMhezHLRdpoN29yIOpknFF7moo1oRrJZa3uzzTILs4%2BFnd%2FfiKSQ%2BcAsQYVNwuSQ8YT5EBcrP96poD89DDQbiUiqI8L4jNbL2zQLbhLmQszu7Sxazmw9Gnex9KEjRIAHBz1wf014GJ9S5NuoWV%2B4RyqqfzkTyLkZZYHgpVZw7ndqkEKIvu6W31AUKVCWWE9j2cCzi6VcqskI8kbeoPoI%2FsuGh77gqjHU0cyAiTTfr93hXin4dQAS6hBOCV7NK1SvVDuRF8FDWLOi1I5LWdSoAiscP5wzMcdTmSPFzYZjwJJZMs0mDSfmJJqPQAbCalwLcdCFGiTqNJ3bd95c%2Fi94tTxmS2N4IB2I5RxmUfvOiYAw2Rd1Da4JYTNlPUdDb%2BFN%2Bxv0NLAlDfvFn6PdQvCk3A1kNbV4Rs6FyPhuXzRJUKYoA8WnAsNgxFtDtoBLqmAze9C%2Fd7T3OnyQphdYmmD%2BRfMU%2F9Owmn0i1B7TO5dIAKmeAXut0tNwCFSR6dYmdmpQnLd1LLIqzE1EZR6d%2BpW%2BSk5YYDpzUBUvyCmn8AYYmA0yueX7C6PdV7xfJkcn0W6dunxvWTtHAK7A2uA6M7rs3dXauKX9XjKZat2Ji%2FXm%2BOQjx1HWFz3kfMJcJPda6VWCdxathXpXaYPTNHxV%2FjVvtri%2FqQKESljXLAGkqZaKg1ez4bkssFYZ9c%2FbVl2y3%2FixZeaseb%2BeOiaKP80RxqoM%2B4sec4dQnZRuI0mSUSwfmhSdWBkZXUISKo7H01tKURrK39UocxS8uSV23TZXLZp8C2l3yIcBzDF962hC0NdHKGxYLxI%2Fw%2FOnE4dXfUp4mPVZZVdZv17KT3GWtYvtLNiem2UCBvOTHoTPKF4alizMZ5Q4fL9L4AEshtbadELmiwN8YFKs00LaIOMrgcSxVo%2FJRU5r4SWCj10JBxFPmPq0y3VmvHYiGmjyBodh0447cEwLFt5s9s9cFfdoHmB0XJtTT8%2FHs7K6%2BI39Ryj9N%2B3%2FuCTp95Gt2%2B6P%2F5mj45vl2cAeGXPfVZIZkq8a%2FTw%2FXIlYcHWZV7sq8UEOQUqVXxWyHQfbFxtbycVtR3xoj%2FjCr%2FyxqoQ6xJueJTl%2FyNdYblQ95ug01%2B6qII5RfEuimps4c0LMqmNt2m3tKyDCQae%2FUi1otrq5cNofLNYfg5bwqMP6CYhJaiJzhKnNx%2BSO3lhnl24Cp424o1dhjIOrYDt%2FW%2F%2B2zSzKeP%2BrzA7e9dIw8HPM%2FMcHyaBGLYVT%2BU%2BJdSVoObFs3JJpFNRo1c0%2FSX%2FsXOd4n2cJlis6bjxPQwqC4oTU5tdoqTnuuunTSMSnSRWr8nf7lEfZBmO8fIILPNPDgW13He%2F2YQwEa4kJIoUzJYuH0YAQnb2ok5RYx6PIWaO8OsFVQYCLky8%2FsHTrZtmLifMa%2BTvNk4gnyO%2BLnEc9emkByjcxJednpOXnsEnNi4uQra0ZBW5NiHAKEHn4qKfFmXsRU56g%2Ba3wOl5PesYKUEocZ%2BcxGePFMlysOX%2BNTEfaDjeTMPztK4TlDZ7FmPMM39J3zHv7LqgIfZVpgtwftR8By0vvIhA%2BAeGkWdS5cU64PZUo3l1sJzwfexF%2FlMb8qoaVpvA5o%2B5PbRvmNuQNFSZvS7l7Zz%2B9GwoRBv317AaImCHV0vgsP8xyVPQ5y30F6Xbi2xSWR%2Bs%2F5D0Db%2B3%7ChboL1xAkV98%3D%3ArOU7vja5Ru0pJFyTnolC%2FhgoeNYNc62ko8e%2FRe9HnwA%3D',
#                 'UK': 'YET8ItNquHIvArVy9z%2Fegg%3D%3D%7C%2B03AuCQxCGgWAN7EDXJ8vQRNfB1C%2B37vZsGLvg0xXujp8cWCjBf9WNvSp%2BT2yYASqcDorvI2oZ2r1CAnfgc02E2qa6SXzzKgxIB31oN5Oo%2F%2BljmrizFiNJLj5soW6NgMkpyXTTVHVKlUNUtJ3pC0BIE7BenBgJZhA2teu%2Fppratecw4dwtnXWPjrTyyCoioiCKhI9SbPIGUsTIZrHOJy%2Fv1i5EsYRRyqA4gf9cRCt10mE5wadbEwDubCLH1ulNat524Gx4NG0lvtFOzwEni15OEFChrR7GXLhp3SH%2FOyPCzEkqJNtT32%2BN0nDPgmos0TjWICunUlQVg%2FEZrQ1vrw97irX0u85OdIauUC59bvSou6KlsFBL7hAjqIr0RC73%2F0sHNsGNnc2D%2BSSjPr5mTV7LSsmzTjnvdR8awCaohIn7Qz%2BfWENnKqgSbxLRoYMwsQiCmeEa1ZbWjbkaClQz%2BPAvPttJprqiqv5BKNSYaDsiGWGpz5wWHO1rX0gQ5yJU9P%2Fa7KjQUa676uHajmyFReAnNh2FbJJvF4PwbCu0Fs19t35MK6tSkd2qGMV509zNO6UlowoqP6QCa9rQRb8NFfFKlfKI%2Bhv8BnxPl7t8l4TXIdDaiELG92rboNvlMIrqUazzuvTBbsvbx4Zbo4QhGnx%2B%2FiHEgTEAAoVkL5i5VAPnbYjElJoXXbhlAWUBzpqo%2FxBmmrwbBO6Gzu0Qswxw%2Fft4bUEaGgkVZjsoZWhPhszh6UTaqFKxhG8WvHzjs62WU7mX928kQQuzdlIOxjRmpyk%2BWloFP4vriaZI96qlLpgKIIgwPhMiRPq5K6qCa5qhcEUsbgvDWyB1uk0aoNREAhKMvmDG3g%2FdPUeR1ulUGEG4UcAR6Y0iPYM7c9raO0ZyQ9CMkGCzwUYb3OGV5aqmCGrSdma81MJ6a84Cf%2F1%2FCqYGs8MIhYdUsf6VUsAMgKOM%2B6PexiDv4%2Bz%2BOpGzTXjvqD29Qy1o9Kro%2BH%2F80NsruRc9UHBv3f9e4KnW41orASxrndlQqmDHujnhdiYiPeIpIcgS4pPlWOP9waXUFMXBvhNobMDDycB5nlCS8ARqByXE6qinwzCjlIV%2B2CMnSKSr1%2FlXkVL9M1dIPoAiLCyVEhEd1tYU5WWS2AI7Up0iLAa9rqFTtIAT%2FdcGkEYkCjyYWTfhzEBB6%2Bs7%2BMIC8QO6n7XTxoFemcB%2FxuLusseX%2FdpUS1GbT%2FICA1yAuRs%2BqYLaq3tRjxtU%2BPQhB1a%2B9ji6gOpeEZVmzVHfiFmOCZwvdazZgwEchMqDuBveUMyf%2Bx5SybRdlR6n6AKZqND%2Bku%2Fs1aSjee6WlsI82%2FgOehGIn69VLGZ%2F4cPbw3SRgX7oo8o3QwpIPkT8tw9mYoIisjsus0nRrb%2FSk1vcQJeJTtkCYkzrWazJbLRExfMD5sd2cMTBEv7LE44Ww3MWc8Th2J6LVD0LnGa3FQrG2DvD7RaeZ7qHpF85u1ZtVPQ6ubys%2BdCVlPNIuIFIAeBvworlGuRRUe6hWLkPoHnvvAKHgdEIWnmH3cd0u1x4t%2FqcvRfVimiyk9KyEgW1M7ODrot%2Fdmc%2FAa3lqZdonpnsnhFq64OpW1vZ%2FZ3UAZ2BpKb74KtVZyXDcCPklDJ3ykIdrEYhbeeb%2F7ACu9v4wiYmmiCdruERECqUx3xY7QBLyKD1%2FW0dPry54eazJU%2BvmW7%2BGCCzWJES8H%2FzWwsifZDKelnjWivWcG5BHXjkpzkimXncefFj6%2B0XVkI03EMln%2FQ7RiTAunycT16J8G%2BDizIvYLF2KZ7fhvWDbALTsOqpIEjk7bB45gLJcLeg8KS1KfPQNbXtETEvs0rVZJyR5C%2BRmlTtrXceW9RkEgLgYdz8rgi8MdFqyNxPRgHN7u9%2BNTUP1rRphNXIKHQacP5TQG1AwaSisnYlPY5ovkLatMAjlSQxztS4X%2BhZEKa9Dli5%2BNv%2Fwwawm7mHry5S3rmlPYfe2EqQ64xgxZQ0ksVfaaSLG93yXi35DlW2d88y1dcHUSn%2FUJYJE6yuY%2B%2FVPxnyHzTt9XM6cwxBNBNr0WB6LBFBnF0BiEfxfFNn9VPpdDdu0M3e0QeZp2dV%2FsG5GmTeQ3DHpxt5mmlLUTMCfRFO5iOLLcfCQ1AUl79EuKvRpR7CqpHalvfiW7sCeXM%2FoDuBWaBsPCI0UGql1H0TDkzaPATcw6vkoOimBSgm5yPVZlVYmbHgGK5tot8gT7T70krGaVvzUHNSKjoJpYZO7Aw4k0SQCY8EP0ywT4%2BId9nusW%2F13XFcKcxsnx9pwHbqyZbo%2FRmHjkwExv1IMhDjsSuob3XofOP7foqzYtMHfKEL%2B%2F1j%2F6gV8%2BGssjfkR75ynM9%2F2Q9jgTCCGESG3murlrhjwmIA%3D%3D%7C5X1%2BL8aAgsE%3D%3AyCle3HXVIyH82zyWTRQs6yvj2M1X%2BL5K2bOKLONyesA%3D',
#             }
#             customer_market_reverse_dict = {
#                 "UK": "United Kingdom",
#                 "MX": "Mexico",
#                 "AU": "Australia",
#                 "ES": "Spain",
#                 "US": "United States",
#                 "IN": "India",
#                 "CA": "Canada"
#             }
#             custommer_market = customer_market_reverse_dict.get(sm)
#             if not custommer_market:
#                 raise ValueError(f"No ORION_SESSION defined for country code '{sm}'")
#
#
#             # --- Pick the ORION_SESSION based on sm ---
#             orion_session = orion_sessions.get(sm)
#             if not orion_session:
#                 raise ValueError(f"No ORION_SESSION defined for country code '{sm}'")
#             cookies1 = {
#                 'x-viator-tapersistentcookie': '517e4a51-f2c4-4cd5-a176-192a37fa610a',
#                 'x-viator-tapersistentcookie-xs': '517e4a51-f2c4-4cd5-a176-192a37fa610a',
#                 'OptanonAlertBoxClosed': '2025-09-10T11:27:19.554Z',
#                 '_gcl_au': '1.1.1768072324.1757503640',
#                 'rskxRunCookie': '0',
#                 'rCookie': '10uilvjlqc4q60d6ckd6epmfdwafwk',
#                 '_cc': 'AcRgRniBHe0VKSma4S0xWENM',
#                 '_cid_cc': 'AcRgRniBHe0VKSma4S0xWENM',
#                 'SEM_PARAMS': '%7B%7D',
#                 'SEM_MCID': '42861',
#                 'EXTERNAL_SESSION_ID': '',
#                 'LAST_TOUCH_SEM_MCID': '42861',
#                 'XSRF-TOKEN': 'cc187141-154d-43a5-9a5d-0b996cabbec2',
#                 'profilingBeaconSession': 'YpUE9iVk9adFZ%252Bd974P4%252BA%253D%253D%257Ct7ufcwEWW3z4WaLHTXeA%252BsYUSAwKzs3TDylRF7PBGQ9T5yJ%252F2YxRXWvJKccdxGrduG4GIYzceWk%253D%257Cim6nHOiuLxM%253D%253A%252F%252BtKSCTcldMC%252B89jvrdLSY3SSa0sRTPjMi6vLTtteRI%253D',
#                 'ORION_SESSION': orion_session,
#                 'REFERER_PAGE_REQUEST_ID': 'A7528725:518D_0A2809E5:01BB_68D54198_A732B64:319863',
#                 'mp_d7f79c10b89f9fa3026f2fb08d3cf36d_mixpanel': '%7B%22distinct_id%22%3A%20%22%24device%3A199336142e2b44-009824152323978-26061951-144000-199336142e2b44%22%2C%22%24device_id%22%3A%20%22199336142e2b44-009824152323978-26061951-144000-199336142e2b44%22%2C%22%24initial_referrer%22%3A%20%22%24direct%22%2C%22%24initial_referring_domain%22%3A%20%22%24direct%22%7D',
#                 'OptanonConsent': 'isGpcEnabled=0&datestamp=Thu+Sep+25+2025+18%3A50%3A42+GMT%2B0530+(India+Standard+Time)&version=202402.1.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=c60ca1d7-7736-4b5d-b53b-f179dc5b3791&interactionCount=2&isAnonUser=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0003%3A1%2CC0004%3A1%2CC0002%3A1&geolocation=SG%3B&AwaitingReconsent=false',
#                 'lastRskxRun': '1758806443614',
#                 'ORION_SESSION_REQ': 'A7528738%3ABFF4_0A280F01%3A01BB_68D541AB_A9BD248%3A31A7CE%7CA7528725%3A518D_0A2809E5%3A01BB_68D54198_A732B64%3A319863%7CA7528725%3A518D_0A2809E5%3A01BB_68D54198_A732B64%3A319863',
#                 'profilingInAuthSession': 'bK8LNaZVJgMnILnP255NUg%253D%253D%257Cfjs%252FfePY2ognaCBxjxJ7W5cgo7vIKOcsTtjft%252FvNW9AtxAxzGnlauYXKrIpzjv2DRtJMHCxBM6Si1Ec%252BIyRA1Zvy46%252FvdByzY6AxuEBZQ8e2JTJu8g%253D%253D%257CGS%252FcCGZsCZk%253D%253AKYILHwnRMHRg6O0A9fHzozGHbtCaivIkyhDEkwuCoq0%253D',
#                 'datadome': 'vS3prX8o5_fh4ak0eM74_GhktawnDHHnrfIieX3PzgVadzwfnIYF6RRPZ~1nw3YNUsA~T1OpqIuIZXzz8NLYaBTbA6bVA5aUOTnERZxn9wGgsCGFwWWOKRlWcib3mI~U',
#             }
#
#             headers1 = {
#                 'accept': 'application/json, text/plain, */*',
#                 'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8,hi;q=0.7',
#                 'content-type': 'application/json',
#                 'origin': 'https://www.viator.com',
#                 'priority': 'u=1, i',
#                 'referer': 'https://www.viator.com/tours/London/London-Pass/d737-3138LONDON',
#                 'sec-ch-device-memory': '8',
#                 'sec-ch-ua': '"Chromium";v="140", "Not=A?Brand";v="24", "Google Chrome";v="140"',
#                 'sec-ch-ua-arch': '"x86"',
#                 'sec-ch-ua-full-version-list': '"Chromium";v="140.0.7339.128", "Not=A?Brand";v="24.0.0.0", "Google Chrome";v="140.0.7339.128"',
#                 'sec-ch-ua-mobile': '?0',
#                 'sec-ch-ua-model': '""',
#                 'sec-ch-ua-platform': '"Windows"',
#                 'sec-fetch-dest': 'empty',
#                 'sec-fetch-mode': 'cors',
#                 'sec-fetch-site': 'same-origin',
#                 'traceparent': '00-0f81c2bb5f611ffc6fb7d541fd4c2b67-e0ac859506165aab-00',
#                 'tracestate': 'es=s:0.1',
#                 'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/140.0.0.0 Safari/537.36',
#                 'x-datadome-clientid': 'vS3prX8o5_fh4ak0eM74_GhktawnDHHnrfIieX3PzgVadzwfnIYF6RRPZ~1nw3YNUsA~T1OpqIuIZXzz8NLYaBTbA6bVA5aUOTnERZxn9wGgsCGFwWWOKRlWcib3mI~U',
#                 'x-frontend-date-validation': 'true',
#                 'x-requested-with': 'XMLHttpRequest',
#                 'x-xsrf-token': 'cc187141-154d-43a5-9a5d-0b996cabbec2',
#                 # 'cookie': 'x-viator-tapersistentcookie=517e4a51-f2c4-4cd5-a176-192a37fa610a; x-viator-tapersistentcookie-xs=517e4a51-f2c4-4cd5-a176-192a37fa610a; OptanonAlertBoxClosed=2025-09-10T11:27:19.554Z; _gcl_au=1.1.1768072324.1757503640; rskxRunCookie=0; rCookie=10uilvjlqc4q60d6ckd6epmfdwafwk; _cc=AcRgRniBHe0VKSma4S0xWENM; _cid_cc=AcRgRniBHe0VKSma4S0xWENM; SEM_PARAMS=%7B%7D; SEM_MCID=42861; EXTERNAL_SESSION_ID=; LAST_TOUCH_SEM_MCID=42861; XSRF-TOKEN=cc187141-154d-43a5-9a5d-0b996cabbec2; profilingBeaconSession=YpUE9iVk9adFZ%252Bd974P4%252BA%253D%253D%257Ct7ufcwEWW3z4WaLHTXeA%252BsYUSAwKzs3TDylRF7PBGQ9T5yJ%252F2YxRXWvJKccdxGrduG4GIYzceWk%253D%257Cim6nHOiuLxM%253D%253A%252F%252BtKSCTcldMC%252B89jvrdLSY3SSa0sRTPjMi6vLTtteRI%253D; ORION_SESSION=BHxMlhe5ljTYyg9UAzcPFA%3D%3D%7Cmo3hMuZyAewmjK9hQE7AGSDNmfWYKcB%2B%2Fc4lwkYGeyrPLefCTmf6VDgBm3QSxGzRRI9yfbK5zIuYpicJ1kXk%2FvUBizPyVSrC8B7rPzwsAan75UB4QGh9bwvl%2BTiaEWLRirfySzWrGYsZD8isCWNsFLYz5KA5%2BlOOyYJq6a9QioXmNFg5%2BtLiTR9M%2FIYytAUVKNyNTdUYKAVHFS%2FQwjxnbCxSLPXO%2Bvf91Lng180Pxdt7yMrX5S5stMgphIssQCWMOxn3jCgbZJlQjGT3Ase7SRaerKkucsdO1O7fUUdHdiTVNkzAFA68LxgtoqJIt6pHLGG1v1LfxpXA2JPegM7VlBSnhC1mdtZR7rwBdg1p9iZj1mOP4ch9gXEin%2FNfkeZRpds5JKwdD7znZ0akkUDxqQB9oGvhxQRzDZR5MAVAyR5ywdrtTnG%2BdjVDMsiY2gQ%2FAMNlRCrnqSbSMx6MKlheQQjEt%2FhY5p0jR1W1qQHjwn0ZrD%2BxsZQHQILlJLmjClVQuP72M1fhlY%2BnL8CoCP4vtrBE18x2KeMOnmsfy4ZRj5eOkw6TIBx0w57bYnsGiBoca5zts9BvRq%2B%2BMdGr%2BbUqQjpQA7KzhN2rondBOa7vtuglDqZsPa0Kigko4yLD9HxHOSyARy89gykJuKPj5yfOarDf%2F%2F%2BYsJHfns%2FmQUlfPogoVAN%2F9ZKsROfV3NevmzzJHrQjxPmf0YbbhCWLZiqRgNm%2BhKoYxEAvC4IWN1M39ZKH0kP69Bez1wFVvcbM%2Bdey1n3soG1ybhb%2BIdPj8lmzb%2Fo%2FXix1XQA74T%2BAncWzUYr%2BBaNwPEv3CJdKktupmJZ90vYywumVW3xRb%2Fe50drxrU3kGrEUYLwktv59iSW7qIRgypmO%2FuA6eX74SyJ6jzEfSy4g3l9NSzfnsyHSQPjLRAvCvLFGV%2BZjCVAl1hi%2B0nOXv3ShQEEwrMIKh%2FXYSB4vAlpt3TVAtq5LtsZdFMSvXJRbEf713Ho6TyytVKnRZ3AyMmbU95BtsSJUtTvQUDYNL593zGeAbxd%2FlMEv19%2B5eZPr9aKzcEyaPy9lVmZDR3RWcCT92zqJuyawuxEMUi6P8WPnnDC0yO9w7aGw51GYKBnQDmmDWoDQx%2Bx2pzPV8W3IHQBAjjAjYDLaZXgjstiFXKgabv2xtTLj6XyBFp%2Fpk4T%2FcdGNQf%2F2aS1mPehrpNUPbf4wvhv0%2FFBh497JgUDRPKyvJ68NJ%2BkcmqyLYDEV0jNcdz6JfxGTxRhkHPEmrWQSfAVWjrIqonMYvPDCGOSQ%2F1kJ4mEZAtynfQ1ai90TE5XeRdicW4kukMV0IzwfT15d%2BeOgm1TjoWc46m87zF59X2N%2BCwl6jKO2q60aaeMUmoAOsfekFdnx5JCNGepl7%2FQCHdLbqYcJm307VlbLMvol4ELDKpRI8P9xf3pKGfS6TDnCiVXU%2BEzHk1t6WFSK3k7hR27pNgYW1tcKLiNkiZfbB2cD3yrhCR6YxwGVN1Bjs9Sd%2BF2UOlYCkGZBJvfEGaskLZ3o5O9CTSZnGLM7RGaC48t%2FVuKR7aoPnD32iVdzts%2Bu55Z63cK3NocKD9CVXrOs6OamlrM6iMvCVyYsmrqdmwL1b88u6bGVX2tf9qfDLDIFAYWwSMdHK%2FNEEf5Oc6t17gMfdGjg4urJEjf%2FGsBl57jRK9SfUdiHOwZJyglQ5%2FL%2BG3nk7QQ1QeAPA2khXOaVSqDa9OqRhl4YjZEVeFQ5zsTHHjXfNd5dJPP2%2BhXYQZ%2FASW3i2AdzUHj2ksdNTblyDrI5%2FZ5bds9gUgUYxZRHDM%2B4jjlwZrj%2FuYpzoOCnF%2BDv7c1atmXVhRHM2mvOigEiIRkRu1vgykENt%2FcqJUmuXIOgRMuS2nnM%2FgR7RM7awvKxPY4WFWBkbqOeugdSd3yrqscD1pdAYGujzy3oigI8OKJlS91PiBOYqwWxQZ0FjA4T7VKU7%2F4PXIuItwfC1GGbBjNlCxoncBlX8uUFJidgdW6JpfqXpqS6Zys5gSJqeb6PWQqfuCmX7UkfIas1aHsdzlGFzUmn1Xcwr53xNT9%2B3%2FdpnEjC2aYv64ATwy4KrMi5ehiJhgqiYuzoxJO9GsklKOG3oct133teJcA2h5Kqe1CgVVkBzHn0pKniaeg%2B8iJCo4JnX9fZsFx%2Fr8j2cuOZXQf4DZPR36%2F4EgJD%2FHscBkyiles%2BN2O6cMVt2YGhj3IavOZG1nHuHhl20chY6bx3Q7j01OvjocK%2BIUuQKZVZDSuUuWcs%2BMOcdAEzRH9ua9NYFYne0sZU7M6gMXi23fbATNq%2Fh5MmQakXqES%2BX8tReFmJl58%2FzE50IIDY2OCTEGqgzcmCS8rqdiEwTyddz71Wdm15fc4BrpLnFfKzTFNLIQYX6Q%3D%3D%7CmtL2pzHLCL4%3D%3ABhsBCsUJhaR5Bkwf8s0BebSUgzGfk8wEIXfFUanydfU%3D; REFERER_PAGE_REQUEST_ID=A7528725:518D_0A2809E5:01BB_68D54198_A732B64:319863; mp_d7f79c10b89f9fa3026f2fb08d3cf36d_mixpanel=%7B%22distinct_id%22%3A%20%22%24device%3A199336142e2b44-009824152323978-26061951-144000-199336142e2b44%22%2C%22%24device_id%22%3A%20%22199336142e2b44-009824152323978-26061951-144000-199336142e2b44%22%2C%22%24initial_referrer%22%3A%20%22%24direct%22%2C%22%24initial_referring_domain%22%3A%20%22%24direct%22%7D; OptanonConsent=isGpcEnabled=0&datestamp=Thu+Sep+25+2025+18%3A50%3A42+GMT%2B0530+(India+Standard+Time)&version=202402.1.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=c60ca1d7-7736-4b5d-b53b-f179dc5b3791&interactionCount=2&isAnonUser=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0003%3A1%2CC0004%3A1%2CC0002%3A1&geolocation=SG%3B&AwaitingReconsent=false; lastRskxRun=1758806443614; ORION_SESSION_REQ=A7528738%3ABFF4_0A280F01%3A01BB_68D541AB_A9BD248%3A31A7CE%7CA7528725%3A518D_0A2809E5%3A01BB_68D54198_A732B64%3A319863%7CA7528725%3A518D_0A2809E5%3A01BB_68D54198_A732B64%3A319863; profilingInAuthSession=bK8LNaZVJgMnILnP255NUg%253D%253D%257Cfjs%252FfePY2ognaCBxjxJ7W5cgo7vIKOcsTtjft%252FvNW9AtxAxzGnlauYXKrIpzjv2DRtJMHCxBM6Si1Ec%252BIyRA1Zvy46%252FvdByzY6AxuEBZQ8e2JTJu8g%253D%253D%257CGS%252FcCGZsCZk%253D%253AKYILHwnRMHRg6O0A9fHzozGHbtCaivIkyhDEkwuCoq0%253D; datadome=vS3prX8o5_fh4ak0eM74_GhktawnDHHnrfIieX3PzgVadzwfnIYF6RRPZ~1nw3YNUsA~T1OpqIuIZXzz8NLYaBTbA6bVA5aUOTnERZxn9wGgsCGFwWWOKRlWcib3mI~U',
#             }
#
#             res = Selector(text=html_content)
#             service_name = res.xpath('//h1[@data-automation="product-title"]/text()').get()
#             service_code = res.xpath('//meta[@name="productCode"]/@content').get()
#             company = res.xpath('//meta[@property="og:site_name"]/@content').get()
#             duration = res.xpath('//span[@class="label__Tm23"]//text()').get()
#             # booking = res.xpath('//div[@class="bannerSubText__OOGX"]//text()').get()
#             cancellation = res.xpath('//div[@class="policyDescription__oAOW"]//text()').get()
#             Supplier_name = res.xpath('//button[@class="supplierDetailsLink__Yfk7"]/text()').get()
#             review_data = res.xpath('//div[@class="rating__jScz"]/text()').get()
#             mobile_data = res.xpath("//span[@class='label__Tm23' and normalize-space(text())='Mobile ticket']//text()").get()
#             review_text = res.xpath('//div[@class="reviewCount__Bmi3"]/text()').get()
#
#             review_number = ""
#             if review_text:  # make sure it's not None
#                 match = re.search(r'[\d,]+', review_text)
#                 if match:
#                     review_number = match.group()
#
#             print("Review number:", review_number)
#             print(referer_url)
#             script_text = res.xpath('//script[@id="globalState"]/text()').get()
#
#             if script_text:
#                 try:
#                     data = json.loads(script_text.strip())
#                     product_languages = (
#                         data.get("__PRELOADED_DATA__", {})
#                         .get("pageModel", {})
#                         .get("product", {})
#                         .get("productLanguages", {})
#                     )
#
#                     primary_language = product_languages.get("primaryLanguage", "")
#                     offered_languages = product_languages.get("offeredLanguages", [])
#
#                     # Join offered languages with commas
#                     offered_languages_str = ", ".join(offered_languages)
#
#                     print("Primary language:", primary_language)
#                     print("Offered languages:", offered_languages_str)
#
#                 except Exception as e:
#                     print("Error parsing globalState JSON:", e)
#
#                 print("Number of reviews:", review_number)
#             if not review_data:
#                 review_data = res.xpath('//span[@class="averageRatingValue__cWuj"]/text()').get()
#             review = f"{review_data} / 5" if review_data else ""
#             pick_up_innfo = ""
#             pick_info = "excluded"
#             picking = res.xpath("//span[@class='label__Tm23' and text()='Pickup offered']//text()").get()
#             if picking:
#                 try:
#                     pick_up_innfo = res.xpath(
#                         "//li[contains(@class,'feature__W54X')]//div/div[contains(text(),'Pickup')]//text()"
#                     ).get() or ""
#                 except Exception as e:
#                     print(e)
#                 pick_info = "included"
#             title_blocks = res.xpath('//div[@class="title__uQE0"]')
#
#             meal_keywords = ["meal", "meals", "food", "foods", "drink", "drinks", "lunch", "dinner", "breakfast"]
#
#             meal_info = "Excluded"  # default
#             guide_info = "Excluded"  # default
#
#             for block in title_blocks:
#                 # get the text of the child div
#                 text = block.xpath('./div/text()').get()
#                 if text:
#                     text_lower = text.lower()
#
#                     # --- check meals ---
#                     if any(k in text_lower for k in meal_keywords):
#                         meal_info = "Included"
#
#                     # --- check guide ---
#                     if "guide" in text_lower or "driver/guide" in text_lower:
#                         guide_info = "Included"
#
#                     # if we already found both, no need to continue
#                     if meal_info == "Included" and guide_info == "Included":
#                         break
#
#             print("Meal info:", meal_info)
#             print("Guide info:", guide_info)
#
#             guide_extrac = ""
#
#             if guide_info == "Included":
#                 guide_extrac = res.xpath(
#                     '//div[@class="title__uQE0"][contains(translate(.,"GUIDE","guide"), "guide")]//text()'
#                 ).get() or ""
#
#             print("Guide extracted:", guide_extrac)
#             transfer = res.xpath('//div[@class="title__uQE0"][contains(translate(.,"Transportation","Transportation"), "Transportation")]//text()').get()
#             if transfer:
#                 transoption = "Included"
#             else:
#                 transoption = "Excluded"
#
#
#             # --- Mobile ticket info ---
#             # data_information = res.xpath(
#             #     '//ul[@class="productAttributesList__RYf2"]//span[@class="label__Tm23"]/text()').getall()
#             # for d in data_information:
#             #     if "mobile" in d.strip().lower():
#             #         mdata = "Mobile ticket"
#             #         break
#
#             # --- Product code ---
#             product_code = res.xpath('//p[@data-automation="product-code"]/text()').get()
#             prod_code = product_code.split(":")[-1].replace(" ", "")
#             # api_key = "21ed11ef5c872bc7727680a52233027db4578a0e"
#             # zenrows_url = "https://api.zenrows.com/v1/"
#             # --- Call availability API ---
#
#             url = 'https://www.viator.com/orion/ajax/product-availability'
#             search_date = datetime.date.today() + datetime.timedelta(days=1)
#
#             for i in range(7):  # look ahead 7 days
#                 search_date_str = search_date.strftime("%Y-%m-%d")
#                 print(f"Trying date: {search_date_str}")
#
#                 resp = requests.post(
#                     url,
#                     headers=headers1,
#                     cookies=cookies1,
#                     json={
#                         'productCode': prod_code,
#                         'searchDate': search_date_str,
#                         'ageBands': {'ADULT': '2'},
#                     },
#                     proxies=zenrows_res_proxies,
#                     verify=False
#                 )
#
#                 print("Status:", resp.status_code)
#
#                 if resp.status_code == 200:
#                     # ✅ found availability
#                     availability_data = resp.json()
#
#                     # url = "https://www.viator.com/orion/ajax/product-availability"
#                     # avail_resp = requests.post(url, headers=headers1, data=payload).json()
#
#                     tourGrades_data = availability_data.get("productAvailability", {}).get("tourGrades", [])
#                     # for idx, model in enumerate(tourGrades_data):
#                     #     title_name_mode = model.get("title", "")
#                     #     print(f"[{idx}] Title: {title_name_mode}")
#                     # --- Extract JSON-LD for review/price ---
#                     # review = ""
#                     links = ""
#                     # currency = ""
#                     # price = ""
#
#                     # --- Extract JSON-LD for review/price ---
#                     json_loading = res.xpath('//script[@type="application/ld+json"]/text()').get()
#                     if json_loading:
#                         try:
#                             data = json.loads(json_loading)
#                             item = data[1]
#                             links = referer_url  # fall back to current page
#                         except Exception as e:
#                             print("JSON-LD parse error:", e)
#
#                     # --- Meals / Guide / Mobile Ticket ---
#                     data_for_meals = res.xpath('//script[@id="globalState"]/text()').get()
#                     if data_for_meals:
#                         try:
#                             parsed = json.loads(data_for_meals)
#
#                             including_data_mobile = (
#                                 parsed.get("pageModel", {})
#                                 .get("product", {})
#                                 .get("description", {})
#                                 .get("productAttributes", [])
#                             )
#                             for attr in including_data_mobile:
#                                 if attr.get("label") == "Mobile ticket":
#                                     mobile_ticket_info = "Mobile ticket"
#                                     break
#                         except Exception as e:
#                             print("Meals parse error:", e)  # stop after finding it
#
#                     # --- Insert one-by-one for each start time ---
#                     print("tourGrades_data:", tourGrades_data)
#                     for tg in tourGrades_data:
#                         title_name_mode = tg.get("title")
#
#                         modality_code = tg.get("tourGradeCode", "")
#                         print("modality_code:", modality_code)
#
#                         # Take only part before ~
#                         modality_code = modality_code.split("~")[0]
#
#                         print(modality_code)  # 👉 DEFAULT
#                         pickup_point = tg.get("title", "")
#                         date = tg.get("date", "")
#                         availability = tg.get("availability", "")
#
#                         start_times = tg.get("startTimes", [])
#
#                         # If no startTimes, still insert one record with defaults
#                         if not start_times:
#                             start_times = [{}]  # make a list with one empty dict
#
#                         for st in start_times:
#                             start_time = st.get("startTime") or st.get("startTime24H", "")
#                             cueency_code = (
#                                 st.get("price", {})
#                                 .get("retailPrice", {})
#                                 .get("currencyCode", "")
#                             )
#                             variant_price = (
#                                 st.get("price", {})
#                                 .get("discountedPrice", {})
#                                 .get("amount", "")
#
#                             )
#                             if not variant_price:
#                                 variant_price = (
#                                     st.get("price", {})
#                                 .get("retailPrice", {})
#                                 .get("amount", "")
#                                 )
#                             # booking_days = (date - today_date).days
#                             # booking = f"{booking_days} Days"
#
#                             today_date_str = today_date.strftime("%Y-%m-%d") if isinstance(today_date,
#                                                                                            datetime.date) else str(
#                                 today_date)
#
#                             list_main = {
#                                 "Modality Name": f"{title_name_mode}_{start_time}",
#                                 "Review": review_number,
#                                 "Region" : "",
#                                 "Destination Code":"",
#                                 "Destination": "",
#                                 "Supplier": Supplier_name,
#                                 "Service Name": service_name,
#                                 "Service code": service_code,
#                                 "Modality Order": "",
#                                 "Mobile Data Information": mobile_data,
#                                 "Cancelaciones ": cancellation,
#                                 "Currency": cueency_code,
#                                 "Pick up point- extracted info": pick_up_innfo,
#                                 "Meals : included/ excluded": meal_info,
#                                 "Duration": duration,
#                                 "Available Arrival date": "",
#                                 "Order": order_code,
#                                 "Calender Week": 38,
#                                 "opiniones": review,
#                                 "Links": links,
#                                 "Scope": "",
#                                 "Pick up point- options": pick_info,
#                                 "Booking in advance": "booking",
#                                 "Search date": today_date_str,
#                                 "Arrival date": date,
#                                 "Price": variant_price,
#                                 "Assistance/guided": guide_info,
#                                 "End Time": "",
#                                 "Segmentation-duration": "",
#                                 "Min pax": pax,
#                                 "Drop off -options": "",
#                                 "Drop off -extracted info": "",
#                                 "Transfers - options": transoption,
#                                 "Company": company,
#                                 "Assistance/guided-extracted info": guide_extrac,
#                                 "Language -extracted info": offered_languages_str,
#                                 "Promotion Description": "",
#                                 "Deliverable Date": today_date_str,
#                                 "Promotion": "",
#                                 "Modality Code": modality_code,
#                                 "Modality Availability": "",
#                                 "Tool Tip": "",
#                                 "Contractor": "",
#                                 "Product Line": "",
#                                 "Customer Market Key": sm,
#                                 "Meals - extracted info": "",
#                                 "Customer Market": custommer_market,
#                                 "Contract Info":"",
#                                 "Incomming Office Code": "",
#                                 "Transfers- extracted info": transfer,
#                                 "Start Time": start_time,
#                             }
#                             try:
#                                 product_data.insert_one(list_main)
#                                 print(f"Inserted variant: {pickup_point} | {start_time} | {variant_price}")
#                                 search_data.update_one({"_id": doc_id}, {"$set": {"Status": "Done"}})
#                                 return
#                             except Exception as e:
#                                 print(e)
#
#                 elif resp.status_code == 403:
#                     print(f"No availability for {search_date}, trying next day...")
#                 else:
#                     print(f"Unexpected status {resp.status_code}")
#
#
#     except Exception as e:
#         print(e)
#
#
#
#
#
# if __name__ == "__main__":
#     with ThreadPoolExecutor(max_workers=5) as executor:
#         docs = list(search_data.find({"Status": "Pending"}))
#         executor.map(process_document, docs)
#
