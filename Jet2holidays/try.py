# # import html
# # import json
# #
# # import requests
# # from parsel import Selector
# #
# #
# # cookies = {
# #     'mvt-460': '1',
# #     'akacd_prhpw': '1771135323~rv=21~id=faeabf449a10059b1f0c4312c0d52a0b',
# #     'OptanonAlertBoxClosed': '2026-01-16T06:02:08.981Z',
# #     'kndctr_081C1EAC64EE1E270A495FF9_AdobeOrg_identity': 'CiYzODU5MTg4MTc4OTI2NjUxNTYxMDYxODM1MDQwODY0ODM0OTY2OVITCJeWofq9MxABGAEqBElORDEwAPABl5ah%2Dr0z',
# #     'kndctr_081C1EAC64EE1E270A495FF9_AdobeOrg_consent': 'general%3Dout',
# #     'J2HPOI': 'TRUE',
# #     'MDT': '3',
# #     'rxVisitor': '1769158604649PU07R6EM0TUV9OSENKT36972HHCT014Q',
# #     'dtSa': '-',
# #     'rxvt': '1769160403997|1769158604650',
# #     'dtPC': '-23548$358604644_772h2vCFWUATNCFBDDFJBOGHFMVHEHCCRGOEBN-0e0',
# #     'dtCookie': 'v_4_srv_4_sn_U16791KOO64KEBKIOV2P4VSEE5OCO39O_perc_100000_ol_0_mul_1_app-3A9bacd72748859223_0',
# #     'BIGSC': '1',
# #     'ak_bmsc': 'ED8F00336FAC0E0A016421D8B8046882~000000000000000000000000000000~YAAQDhzFF9W639+bAQAAHv0R6h6JQEjgKDZjaML5AtI7OfttteXYtVKsN9wsQWYxhJErDhd9sJdXex96TS5SNYGPh5mQg5uFORVM0R8MZTC6ZmBHFjqOtBQ3bbPpkAjKFlrgFxU0Gf0FvIJE+OlMqedvG6bDJEJGRwDdkfCU7f4cdKgJmvG8D7KemazjXjmYiAWbK56vKPCigF1ymA/PXtIe3F9GupiiBqE+cCh9IiH5ZKCWrkZMQqnnAQh2bMO2v/xo3Zmi5XaLKHq6VxHS/nDLZE2FETsAu/HxZiGsgwVMyA2bIKrKiZTduvK5Mdup2sDMT5YLs2u6mGPuTKzbkM/WHksL/kaM5wGT0nW1AslJCwKvn1yfivZFpFWUWv4jAaPWZclXGUDCLyvvmSbHu84Rbgy5zNcql+1btKz4nNWMUvRTT2NwNq8i9wes9DSHa0bsCBWgX3m+c6sRgWLP9yo0SQ==',
# #     'ASP.NET_SessionId': 'vlrdl2e1l1ifr30qig0f4pn3',
# #     'shell#lang': 'en',
# #     'J2_ST': '20',
# #     'SC_ANALYTICS_GLOBAL_COOKIE': '4b81ba62c43145b58aace5a9fee38e8d|True',
# #     'AKA_A2': 'A',
# #     '__RequestVerificationToken': '_zHHwVIZMrLhonDBC1PEzDaO9gfoUPjywidZgF7MlgndzBSvYXKtf-99gA_ozy_UiO1kx5L3LzZ_0fVlSz8elUN20HUDWpEquZJ8C7Z6PBs1',
# #     'PIM-SESSION-ID': 'ZsIzEk7516h6lFcj',
# #     '_abck': '4EE13BBED2730BAE212D522E13D6150B~0~YAAQzkvSF4XEtNabAQAAt7V26g/V66Yov0L+7bpuJxRCremqXoX+X4VxHAK9x8Z0J7pg4K209t+46eE3Prt6llaauXuRRO3m313LqGuTMD35/ccdAsjUTMkUH4HNF7oBJD1m/z+s5DEEMCFQEKzdFLYS1bB/f66OVtuYeG8/YWTRCcbM2Z2OuuMa8r7LkEdfNdtvJZqfkTKjAMrTQjHpcClwX8i4Jbm22vh8Xsd9tR5TM6yvoyv80fnm4JTKYe7oFp4ADrWdphPfzep3I3WlHnIg3wsezSXG3s/GEDZb/vZP0hMhMy951Hp5yKD650olcLxzOoYFqAIJi2cGp5uoYyIFpKHQSSOyySd+0Ye87dTla2QQF4fcTpxiIUsf8N2nOEGGRhpZD3uXu6a4pJlVQOjY05b4zhsH4sIPjfLjiBPNipw+WG03uf5mC1Kw8LyMbWfBPyrgxLo4RPvRLPF0UdndYtdVwCoM05bxHygHOt8SXdp99gnAr9BshM7AEywYiaGIjJ1FdsLJ4LgIcdyPiwtcG3A2u+wJgub7iC28/hIEAMT0tQwjqWLby8Velm0F2CnDnOPAXhuy3OtE2dDxLu0qCk41+l+IEJKNKFm/eEidKuwSy1+hbwZtPYD62EA7Lk5/UIE/lKdSUO44tegiJa6TRZ4D9/Rs1ynBTuKmayT9FiPkuxbjGfZEE6PlLt+ojscjF7i1QuE0XXq43NUx8lANFbbRxGCYI+YBaFThKBhrjcbZgJbnTDYUqVmAwQQe+TvjklEu6CFK8Q+Lgm6AbBcj3+6Eave1J9X7p33x19+lYNf9vFhqVlnr9XmjzI8gi1nygEnyFOtGHO+jqmKP77kdJIbwOTQIxgyXpZrjEaNC4MRHpNCmXZmAqRjfXcq1VHQzYodZSQxc1M25KqkrvkBXJ0J4KRhFG3DEYLA=~-1~-1~-1~AAQAAAAF%2f%2f%2f%2f%2f+yCMU59g81I+iOB951L1X7L1vyJiUPX3N8Jb1382WFBEL0nlHe593RxH6N+LTHQJTK1e7jrmmE%2fItC8oh70DKN5bFFBC+ijtVtMd3N6W1Zzh5k6j%2fqkb1bzI7kArQp5EVVjwzZ12Vz49PD+RCXk7mKx2Z8pzs%2fQUEZPq6ZlOXaW3LRLgL6AtZ8sFgg2LnEvM%2fCbYm4LSO8f~-1',
# #     'bm_sz': 'C5C80B2B9CE5F1777570A6591C45B403~YAAQzkvSF4fEtNabAQAAt7V26h7t5LlAZUZzieZgPPlc5QgNpKsSAGeDEgNSvmGqInOvyvYP5UPcyJHBXuIRg3bIQvoEdUXfqm/Y/60B9K5kVs+NumqoGNWCgLemwtQvjCnn8V7JSkKtK3ZgDxxY5I+ny/9dgAL80nlxIcb7GvASK5K9iWFTjOAOI/BEpyB2dbgZaBF4fbQk3tFC6X9JgcuXvnCcaKVNAYNfcFBksVx9+Whd7BCe96FJV3/kTZRp5ZMTDM/MWevp5MWOULPZ7tIwonQUYsgGMl9v5M/spsw/9HcrTTT5Ikuxeep7HLIMu63bTCmFGnVG9hEXyCBBX8bteYADECyvZ4j8VED1LEJTBvu2NLx1LR2Ez28OgqnpYc2AGyUN1/u9KUGZaxhe65khjtzdZRmHRpXB53MnW9XRIF5/98Fy/u2/lMviTTB9g+stM891u2MqgsG+EvR0BOMI6U99madISwA9ueF/rawFI/mz8zR18jE9gI6lSKl+3IEZxSTVETerAhRa45JVqSppa5ma3+JhC8Bm9PqxHw==~3687473~3687987',
# #     'mp_d7f79c10b89f9fa3026f2fb08d3cf36d_mixpanel': '%7B%22distinct_id%22%3A%20%22%24device%3A19bc5658ae96c2-0ca311ea597ff88-26061a51-144000-19bc5658ae96c2%22%2C%22%24device_id%22%3A%20%2219bc5658ae96c2-0ca311ea597ff88-26061a51-144000-19bc5658ae96c2%22%2C%22%24initial_referrer%22%3A%20%22%24direct%22%2C%22%24initial_referring_domain%22%3A%20%22%24direct%22%7D',
# #     'OptanonConsent': 'isGpcEnabled=0&datestamp=Fri+Jan+23+2026+16%3A16%3A48+GMT%2B0530+(India+Standard+Time)&version=202510.2.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=5e216a47-8cd5-4656-b132-f8c65b92cab5&interactionCount=1&isAnonUser=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A0%2CC0003%3A0%2CC0004%3A0%2CC0007%3A0&intType=2&geolocation=IN%3BMH&AwaitingReconsent=false',
# #     'bm_sv': 'FA87FB0DFA6180EE9154A8FFA1FEAAC5~YAAQzkvSF/7EtNabAQAA08F26h5eQ7o+YXp54yo1iOkSBT8UB6e+4bE5DA6xNg306M4j0FGWEiQHexbbvUaRYBQTAfh4SCUgDGLcUfj+/T1OPuEfkpvD87vRoQKM5+Toy4jBIZ0Ni0J6ysri5E1mD0LrgwDUWD2D28fy8p+wO3yEkQyIqyD+m1Q3sN0mE1wKayvpKn/2zVUHGSw6ZKQ+ErWF7Cn6tTTafRytXd6B2e3al2Me4QT0/DMjzRE6UvsEezKBxvJHXQY=~1',
# #     'RT': '"sl=13&ss=1769158603899&tt=73123&obo=0&sh=1769165206257%3D13%3A0%3A73123%2C1769164523830%3D12%3A0%3A66448%2C1769164505912%3D11%3A0%3A62925%2C1769164493118%3D10%3A0%3A49537%2C1769164463958%3D9%3A0%3A31171&dm=jet2holidays.com&si=28c2b77d-f6e2-4a64-b12d-7e247f513b48&rl=1&ld=1769165206257&r=https%3A%2F%2Fwww.jet2holidays.com%2Fbeach%2Fgreece%2Fcorfu%2Fdassia%2Fikos-dassia%3F357aed888fbcd5b7f0238d9cd9b41a1a&ul=1769165211086"',
# # }
# #
# # headers = {
# #     'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
# #     'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8,hi;q=0.7',
# #     'cache-control': 'max-age=0',
# #     'priority': 'u=0, i',
# #     'referer': 'https://www.jet2holidays.com/beach/greece/corfu?airport=7&date=06-04-2026&duration=7&occupancy=r2c&sortorder=5&page=1&sr=true&property=75844',
# #     'sec-ch-ua': '"Google Chrome";v="143", "Chromium";v="143", "Not A(Brand";v="24"',
# #     'sec-ch-ua-mobile': '?0',
# #     'sec-ch-ua-platform': '"Windows"',
# #     'sec-fetch-dest': 'document',
# #     'sec-fetch-mode': 'navigate',
# #     'sec-fetch-site': 'same-origin',
# #     'sec-fetch-user': '?1',
# #     'upgrade-insecure-requests': '1',
# #     'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36',
# #     # 'cookie': 'mvt-460=1; akacd_prhpw=1771135323~rv=21~id=faeabf449a10059b1f0c4312c0d52a0b; OptanonAlertBoxClosed=2026-01-16T06:02:08.981Z; kndctr_081C1EAC64EE1E270A495FF9_AdobeOrg_identity=CiYzODU5MTg4MTc4OTI2NjUxNTYxMDYxODM1MDQwODY0ODM0OTY2OVITCJeWofq9MxABGAEqBElORDEwAPABl5ah%2Dr0z; kndctr_081C1EAC64EE1E270A495FF9_AdobeOrg_consent=general%3Dout; J2HPOI=TRUE; MDT=3; rxVisitor=1769158604649PU07R6EM0TUV9OSENKT36972HHCT014Q; dtSa=-; rxvt=1769160403997|1769158604650; dtPC=-23548$358604644_772h2vCFWUATNCFBDDFJBOGHFMVHEHCCRGOEBN-0e0; dtCookie=v_4_srv_4_sn_U16791KOO64KEBKIOV2P4VSEE5OCO39O_perc_100000_ol_0_mul_1_app-3A9bacd72748859223_0; BIGSC=1; ak_bmsc=ED8F00336FAC0E0A016421D8B8046882~000000000000000000000000000000~YAAQDhzFF9W639+bAQAAHv0R6h6JQEjgKDZjaML5AtI7OfttteXYtVKsN9wsQWYxhJErDhd9sJdXex96TS5SNYGPh5mQg5uFORVM0R8MZTC6ZmBHFjqOtBQ3bbPpkAjKFlrgFxU0Gf0FvIJE+OlMqedvG6bDJEJGRwDdkfCU7f4cdKgJmvG8D7KemazjXjmYiAWbK56vKPCigF1ymA/PXtIe3F9GupiiBqE+cCh9IiH5ZKCWrkZMQqnnAQh2bMO2v/xo3Zmi5XaLKHq6VxHS/nDLZE2FETsAu/HxZiGsgwVMyA2bIKrKiZTduvK5Mdup2sDMT5YLs2u6mGPuTKzbkM/WHksL/kaM5wGT0nW1AslJCwKvn1yfivZFpFWUWv4jAaPWZclXGUDCLyvvmSbHu84Rbgy5zNcql+1btKz4nNWMUvRTT2NwNq8i9wes9DSHa0bsCBWgX3m+c6sRgWLP9yo0SQ==; ASP.NET_SessionId=vlrdl2e1l1ifr30qig0f4pn3; shell#lang=en; J2_ST=20; SC_ANALYTICS_GLOBAL_COOKIE=4b81ba62c43145b58aace5a9fee38e8d|True; AKA_A2=A; __RequestVerificationToken=_zHHwVIZMrLhonDBC1PEzDaO9gfoUPjywidZgF7MlgndzBSvYXKtf-99gA_ozy_UiO1kx5L3LzZ_0fVlSz8elUN20HUDWpEquZJ8C7Z6PBs1; PIM-SESSION-ID=ZsIzEk7516h6lFcj; _abck=4EE13BBED2730BAE212D522E13D6150B~0~YAAQzkvSF4XEtNabAQAAt7V26g/V66Yov0L+7bpuJxRCremqXoX+X4VxHAK9x8Z0J7pg4K209t+46eE3Prt6llaauXuRRO3m313LqGuTMD35/ccdAsjUTMkUH4HNF7oBJD1m/z+s5DEEMCFQEKzdFLYS1bB/f66OVtuYeG8/YWTRCcbM2Z2OuuMa8r7LkEdfNdtvJZqfkTKjAMrTQjHpcClwX8i4Jbm22vh8Xsd9tR5TM6yvoyv80fnm4JTKYe7oFp4ADrWdphPfzep3I3WlHnIg3wsezSXG3s/GEDZb/vZP0hMhMy951Hp5yKD650olcLxzOoYFqAIJi2cGp5uoYyIFpKHQSSOyySd+0Ye87dTla2QQF4fcTpxiIUsf8N2nOEGGRhpZD3uXu6a4pJlVQOjY05b4zhsH4sIPjfLjiBPNipw+WG03uf5mC1Kw8LyMbWfBPyrgxLo4RPvRLPF0UdndYtdVwCoM05bxHygHOt8SXdp99gnAr9BshM7AEywYiaGIjJ1FdsLJ4LgIcdyPiwtcG3A2u+wJgub7iC28/hIEAMT0tQwjqWLby8Velm0F2CnDnOPAXhuy3OtE2dDxLu0qCk41+l+IEJKNKFm/eEidKuwSy1+hbwZtPYD62EA7Lk5/UIE/lKdSUO44tegiJa6TRZ4D9/Rs1ynBTuKmayT9FiPkuxbjGfZEE6PlLt+ojscjF7i1QuE0XXq43NUx8lANFbbRxGCYI+YBaFThKBhrjcbZgJbnTDYUqVmAwQQe+TvjklEu6CFK8Q+Lgm6AbBcj3+6Eave1J9X7p33x19+lYNf9vFhqVlnr9XmjzI8gi1nygEnyFOtGHO+jqmKP77kdJIbwOTQIxgyXpZrjEaNC4MRHpNCmXZmAqRjfXcq1VHQzYodZSQxc1M25KqkrvkBXJ0J4KRhFG3DEYLA=~-1~-1~-1~AAQAAAAF%2f%2f%2f%2f%2f+yCMU59g81I+iOB951L1X7L1vyJiUPX3N8Jb1382WFBEL0nlHe593RxH6N+LTHQJTK1e7jrmmE%2fItC8oh70DKN5bFFBC+ijtVtMd3N6W1Zzh5k6j%2fqkb1bzI7kArQp5EVVjwzZ12Vz49PD+RCXk7mKx2Z8pzs%2fQUEZPq6ZlOXaW3LRLgL6AtZ8sFgg2LnEvM%2fCbYm4LSO8f~-1; bm_sz=C5C80B2B9CE5F1777570A6591C45B403~YAAQzkvSF4fEtNabAQAAt7V26h7t5LlAZUZzieZgPPlc5QgNpKsSAGeDEgNSvmGqInOvyvYP5UPcyJHBXuIRg3bIQvoEdUXfqm/Y/60B9K5kVs+NumqoGNWCgLemwtQvjCnn8V7JSkKtK3ZgDxxY5I+ny/9dgAL80nlxIcb7GvASK5K9iWFTjOAOI/BEpyB2dbgZaBF4fbQk3tFC6X9JgcuXvnCcaKVNAYNfcFBksVx9+Whd7BCe96FJV3/kTZRp5ZMTDM/MWevp5MWOULPZ7tIwonQUYsgGMl9v5M/spsw/9HcrTTT5Ikuxeep7HLIMu63bTCmFGnVG9hEXyCBBX8bteYADECyvZ4j8VED1LEJTBvu2NLx1LR2Ez28OgqnpYc2AGyUN1/u9KUGZaxhe65khjtzdZRmHRpXB53MnW9XRIF5/98Fy/u2/lMviTTB9g+stM891u2MqgsG+EvR0BOMI6U99madISwA9ueF/rawFI/mz8zR18jE9gI6lSKl+3IEZxSTVETerAhRa45JVqSppa5ma3+JhC8Bm9PqxHw==~3687473~3687987; mp_d7f79c10b89f9fa3026f2fb08d3cf36d_mixpanel=%7B%22distinct_id%22%3A%20%22%24device%3A19bc5658ae96c2-0ca311ea597ff88-26061a51-144000-19bc5658ae96c2%22%2C%22%24device_id%22%3A%20%2219bc5658ae96c2-0ca311ea597ff88-26061a51-144000-19bc5658ae96c2%22%2C%22%24initial_referrer%22%3A%20%22%24direct%22%2C%22%24initial_referring_domain%22%3A%20%22%24direct%22%7D; OptanonConsent=isGpcEnabled=0&datestamp=Fri+Jan+23+2026+16%3A16%3A48+GMT%2B0530+(India+Standard+Time)&version=202510.2.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=5e216a47-8cd5-4656-b132-f8c65b92cab5&interactionCount=1&isAnonUser=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A0%2CC0003%3A0%2CC0004%3A0%2CC0007%3A0&intType=2&geolocation=IN%3BMH&AwaitingReconsent=false; bm_sv=FA87FB0DFA6180EE9154A8FFA1FEAAC5~YAAQzkvSF/7EtNabAQAA08F26h5eQ7o+YXp54yo1iOkSBT8UB6e+4bE5DA6xNg306M4j0FGWEiQHexbbvUaRYBQTAfh4SCUgDGLcUfj+/T1OPuEfkpvD87vRoQKM5+Toy4jBIZ0Ni0J6ysri5E1mD0LrgwDUWD2D28fy8p+wO3yEkQyIqyD+m1Q3sN0mE1wKayvpKn/2zVUHGSw6ZKQ+ErWF7Cn6tTTafRytXd6B2e3al2Me4QT0/DMjzRE6UvsEezKBxvJHXQY=~1; RT="sl=13&ss=1769158603899&tt=73123&obo=0&sh=1769165206257%3D13%3A0%3A73123%2C1769164523830%3D12%3A0%3A66448%2C1769164505912%3D11%3A0%3A62925%2C1769164493118%3D10%3A0%3A49537%2C1769164463958%3D9%3A0%3A31171&dm=jet2holidays.com&si=28c2b77d-f6e2-4a64-b12d-7e247f513b48&rl=1&ld=1769165206257&r=https%3A%2F%2Fwww.jet2holidays.com%2Fbeach%2Fgreece%2Fcorfu%2Fdassia%2Fikos-dassia%3F357aed888fbcd5b7f0238d9cd9b41a1a&ul=1769165211086"',
# # }
# #
# # params = {
# #     'holiday': '34',
# #     'duration': '7',
# #     'airport': '7',
# #     'date': '06-04-2026',
# #     'occupancy': 'r2c',
# #     'iflight': '1528016',
# #     'oflight': '1528013',
# #     'gtmsearchtype': 'Beach Search Results',
# #     'smartsearchid': '91898f4c-8f8a-4078-b0cb-16b5b69a8272',
# # }
# #
# # pdp_response = requests.get(
# #     'https://www.jet2holidays.com/beach/greece/corfu/glyfada/domes-of-corfu-autograph-collection',
# #     params=params,
# #     cookies=cookies,
# #     headers=headers,
# # )
# # if pdp_response.status_code == 200:
# #     main_selec = Selector(pdp_response.text)
# #     main_text = main_selec.xpath(
# #         '//div[@data-component="Search/HotelDetails/RoomTypeWrapper"]/@data-modeldata'
# #     ).get()
# #
# #     if main_text:
# #         # Convert &quot; etc. into real characters
# #         main_text = html.unescape(main_text)
# #
# #         # Load JSON
# #         room_data = json.loads(main_text)
# #         rooms = room_data.get("rooms", [])
# #
# #         if rooms:
# #             rooming = rooms[0].get("roomOptions", [])
# #             for main_room in rooming:
# #                 room_name = main_room.get("name")
# #                 room_id = main_room.get("roomId")
# #                 print(room_id)
# #
# #                 main_params = {
# #                     'duration': '7',
# #                     'airport': '7',
# #                     'date': '06-04-2026',
# #                     'occupancy': 'r2c',
# #                     'iflight': '1528016',
# #                     'oflight': '1528013',
# #                     'rooms': '81162',
# #                     'gtmsearchtype': 'Beach Search Results',
# #                 }
# #
# #                 response = requests.get(
# #                     'https://www.jet2holidays.com/beach/greece/corfu/glyfada/domes-of-corfu-autograph-collection/options',
# #                     params=main_params,
# #                     cookies=cookies,
# #                     headers=headers,
# #                 )
# #         # rooms[0].roomOptions[3].name
# #         # print(room_data)
# #
# #         # # Load JSON
# #         # room_data = json.loads(json_text)
# #         #
# #         # print(room_data)
#
#
#
# Crawled Date
# Website
# Check-In Date
# Check-Out Date
# Nights
# Pax
# Destination type
# Website Hotel Name
# Website Hotel ID
# Matched Hotel Name
# Matched Hotel ID
# Website Rating
# City
# Country
# Source Market
# Room Name
# Board Type
# Total Price
# Currency
# Flight Status
# Departure Airport
# Arrival Airport
# Out Airline
# Out Flight code
# Out Depart Date
# Out Arr Date
# In Airline
# In Flight code
# In Depart Date
# In Arr Date
# Baggage
# Transfer