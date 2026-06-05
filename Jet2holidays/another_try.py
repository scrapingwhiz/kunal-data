import html
import json

import requests
from parsel import Selector

cookies = {
    'mvt-460': '1',
    'akacd_prhpw': '1771135323~rv=21~id=faeabf449a10059b1f0c4312c0d52a0b',
    'OptanonAlertBoxClosed': '2026-01-16T06:02:08.981Z',
    'kndctr_081C1EAC64EE1E270A495FF9_AdobeOrg_identity': 'CiYzODU5MTg4MTc4OTI2NjUxNTYxMDYxODM1MDQwODY0ODM0OTY2OVITCJeWofq9MxABGAEqBElORDEwAPABl5ah%2Dr0z',
    'kndctr_081C1EAC64EE1E270A495FF9_AdobeOrg_consent': 'general%3Dout',
    'J2HPOI': 'TRUE',
    'MDT': '3',
    'rxVisitor': '1769158604649PU07R6EM0TUV9OSENKT36972HHCT014Q',
    'dtSa': '-',
    'rxvt': '1769160403997|1769158604650',
    'dtPC': '-23548$358604644_772h2vCFWUATNCFBDDFJBOGHFMVHEHCCRGOEBN-0e0',
    'dtCookie': 'v_4_srv_4_sn_U16791KOO64KEBKIOV2P4VSEE5OCO39O_perc_100000_ol_0_mul_1_app-3A9bacd72748859223_0',
    'BIGSC': '1',
    'ASP.NET_SessionId': 'vlrdl2e1l1ifr30qig0f4pn3',
    'shell#lang': 'en',
    'J2_ST': '20',
    'SC_ANALYTICS_GLOBAL_COOKIE': '4b81ba62c43145b58aace5a9fee38e8d|True',
    'AKA_A2': 'A',
    '__RequestVerificationToken': '_zHHwVIZMrLhonDBC1PEzDaO9gfoUPjywidZgF7MlgndzBSvYXKtf-99gA_ozy_UiO1kx5L3LzZ_0fVlSz8elUN20HUDWpEquZJ8C7Z6PBs1',
    'PIM-SESSION-ID': 'ZsIzEk7516h6lFcj',
    '_abck': '4EE13BBED2730BAE212D522E13D6150B~0~YAAQzkvSF+ZhtdabAQAAglaE6g8EGMu1cC/NthekC3nkgoC6FUFxgREMW5zzT0VUdwSu8IqjV7Kb+yeavG1/QKI+QKR1A9eVQmRlnJEZIUmpHpAGriH4ZSlzJ9VFt7k1KJ8fgRy7sUewD0E4ppcnOEhwAJzmhxXl+JUvNMGtT47oiOxZhUSufsw5ULCKNyWe2JinjwXoCqoapQh4k/YMLb0IS8vMHx9uE8x5YLWIz7KAkhKRmCeELyKw036i7hsA2J5nkMNLIB640z89ZZb1XG/TUhWlp5cIrrwnEOVpj+acHD7LLuQlUav+bVOrJkSBSnwRbZBpW/79cAQEuofwq5q5PUzglGxcYI/tDqiNVQW7HLVkvwD7ID0vG8ZB7u7FlSruXwtJu899GV/S+gYMoN/KCDLQyvfkr29cWZ6YzXK+88UJd2N2GSzdl7FdCw5+dwPm5Ko0oq0lromdZSVvrZRM5vnbcpqyF/SGIy1fBxw5YOaDa08rh76uYSc/Q0Es4qgsxJlsszqrgp8dhYuSWHmyTeGxH4TvzXRY5VJJwq1rMhGg/IFtwwOhLAE1is11lC9JkVAcouz3aZba7gTehQ3yXhsb7f5QLdoAVaRP/7wdKT8ry3MjpRbTQNeN4AHQjlVzs9PNZbgJSqJb++fjClyPOB3OdvbKCI9S/LxBC1pV0tV3uuihHDPqOM+bpANNKEoAh6uUx2ky+MNNuEJW6ZWsJu6Djs+IrFxD9mNEVAqag0aZNX+OlkV7lcJnBxs6AlD/JAbHRlceNXd+FAhXpRU9QT4FfQNAhWg5n9iPce97ofgHI+l3BsYbQK0n2sYNg9W6fkd+vx+cw/+MNpFsSiDykUmIr+/fiE29qaKyOSjbxc+6L/ngDdsBTQV0luz0sUrB7RPDnBo0SL+GkAfKnKmZtCqVqQ2tVu/KPM4=~-1~-1~-1~AAQAAAAF%2f%2f%2f%2f%2f+yCMU59g81I+iOB951L1X7L1vyJiUPX3N8Jb1382WFBEL0nlHe593RxH6N+LTHQJTK1e7jrmmE%2fItC8oh70DKN5bFFBC+ijtVtMd3N6W1Zzh5k6j%2fqkb1bzI7kArQp5EVVjwzZ12Vz49PD+RCXk7mKx2Z8pzs%2fQUEZPq6ZlOXaW3LRLgL6AtZ8sFgg2LnEvM%2fCbYm4LSO8f~-1',
    'bm_mi': 'EDA72793E59C0E289C26890A7FE7E287~YAAQzkvSF+dhtdabAQAAglaE6h4U1M6ST73/X1tYKnlfxEfkltRFOQWIthhSh7yl4YoGYW7jF7WkjMADe/fsnrb3JPdzONXuNDeto8gQJvOt+54Pj9pNF0I5oW9EC0DX1ErUXIkwJ3rEAse98+Jfj/L/5HJaRWk7QCBbkxypdJg/QIF2Ev4hhIUIqqeBXzUyKbcPvuD10puHO1tuxSp5znrp+hApnYYBTRlDdNoWla8zT+BE47xVIGhW77svK6bsIeEgYCXMM8Y5I/gDJ7Gz5+SLPWR0QxiTjAjqxYK/vLRNAeMAXp/Bl2pF7VDemJgvJP88wYuPQZ80TXVRPJT9+0Dc3jqRT7QRmAiG+MCDQddvx9WVgCTi+RxYyc09bS79yQw4xddCr/oE/PxrlIZNvOs=~1',
    'bm_sz': 'C5C80B2B9CE5F1777570A6591C45B403~YAAQzkvSF+lhtdabAQAAglaE6h4B5/RwUf6epWnGv376B+WJJHoy7MxaNgAMm8dWC4PVl+J8OKSS7gII7X4Q+9OAObSdQJjVwoodCYayZz1o1rAraSyZPqs0tSwIkRvCJG4qbk3aoLCpvXrBJNzGqyQEWdEW9//vBQQFpD1a3AiM8A4hseTc1oOO72Fr2BauKBdVHwOGfyiranqSEkV4ye5aRKGuz0je3wc00BdYGKcupNMXYYaXh4ak0OM12KonjppH494OAwmWfmlgjmaY7feITM553q1ayCvQe/H34zyKmhhcKnelIdKNaIDvRgcKwleRofk2HkuUm7unlsxyAPUeQFMK1eD/uP6ZTFFQHsJefvMoYdlvdAybA61Ao1K9R0H/kavUVRLva+t+DJJNfWucxzcwVZEogVSinDqeq9/fOzzUSV/VBQgmKBGYDElcYM+2uZkw4dtmGWMv1aRY2gEZk4XY+a7ds5OFojQAt+1Ik00usNqY3oAoBMI24YVe/Zuoi5hnh5FF4GczcAS/pNizP/tc9oDd8maaYq/xytDI6kQH1sc=~3687473~3687987',
    'bm_sv': '4A9CF4AAABB0320903683D1D2A69354D~YAAQzkvSFxNitdabAQAAAVuE6h6VmWiaGbujNJsll7hdif1EFNvmU6bmfXg7idGEK5L6LfJdpM99Iy1b8XHyHdMUeqUe1gRTMvwlyASerQWS8JuEM79u3z+jC3yt/oBBgNsN3n8DlGVxL8q/wWL7VxV4bK6BNYeVcLbbQJGu3GxORPZu5dPXXvy+yvLpa4/QIbRmLUMNSC39ZRsXtkHTdsj3FIBwExpOpRVGT0pV9FLJ08b7QZdH9HMKLYJdXATEVALvpjz7~1',
    'mp_d7f79c10b89f9fa3026f2fb08d3cf36d_mixpanel': '%7B%22distinct_id%22%3A%20%22%24device%3A19bc5658ae96c2-0ca311ea597ff88-26061a51-144000-19bc5658ae96c2%22%2C%22%24device_id%22%3A%20%2219bc5658ae96c2-0ca311ea597ff88-26061a51-144000-19bc5658ae96c2%22%2C%22%24initial_referrer%22%3A%20%22%24direct%22%2C%22%24initial_referring_domain%22%3A%20%22%24direct%22%7D',
    'OptanonConsent': 'isGpcEnabled=0&datestamp=Fri+Jan+23+2026+16%3A31%3A41+GMT%2B0530+(India+Standard+Time)&version=202510.2.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=5e216a47-8cd5-4656-b132-f8c65b92cab5&interactionCount=1&isAnonUser=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A0%2CC0003%3A0%2CC0004%3A0%2CC0007%3A0&intType=2&geolocation=IN%3BMH&AwaitingReconsent=false',
    'ak_bmsc': 'CDB36BB46B1A9F2921534E7A2AAA81F2~000000000000000000000000000000~YAAQzkvSFytitdabAQAAZV2E6h4MDkbb/GX52OmGE4SKmEgUwerkMi2gs0YsbA9fKf1L0cYeLGIWhQWBQmbZwV11b5Tjbp+g77nBDwkbfYMmTrxSOHQJ/peOw0FsduTn5+QpcFufxPm6pY/jZDbqfPpZCRHCguT+HaKowuX5sdbpuMdN0yAPP8QbOu//N4sWiZBPwxhgVkkIv9e7iQDoJ1uh+js4/T5ZQ+VRSY3l1Y/dh3l3kFCv23IiYiybVqo8Df5tTWjabp8A58h1aW6XxsB1N+IkrTZzxfVvePbigkNLhAau/MlNkqLZyyecIOIA7dxY5cADD0i8JFtq9uSfTyueCU910wxCXTXLVtQatyaP2gqJ1rsnw5jip4ISQvu65B5NSDJJBFkJx4qrqA8PtvLiPitQhouvcUg5BxJmCWBMT6vd6MFok8SC8TDyVn/65KiFkKKyKX8ouXsOxg4NvcKEdPR8NBLCGYRrs2y8vwonhaUCNGyL5CMv0BMYHhEjEnf5bp/s15alx35n2otM6EedXU8CtJVPsBtStkNaj3LDvR1HDmWtbqGaWerV7r2JqW/v',
    'RT': '"sl=18&ss=1769158603899&tt=94100&obo=1&sh=1769166098432%3D18%3A1%3A94100%2C1769165801890%3D17%3A1%3A87470%2C1769165797423%3D16%3A0%3A87470%2C1769165322225%3D15%3A0%3A83441%2C1769165216342%3D14%3A0%3A77507&dm=jet2holidays.com&si=28c2b77d-f6e2-4a64-b12d-7e247f513b48&rl=1&ld=1769166098432&r=https%3A%2F%2Fwww.jet2holidays.com%2Fbeach%2Fgreece%2Fcorfu%2Fglyfada%2Fdomes-of-corfu-autograph-collection%3Ff43b5cec5b564db02bc0f1e737237f23&ul=1769166278586"',
}

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8,hi;q=0.7',
    'priority': 'u=0, i',
    'referer': 'https://www.jet2holidays.com/beach/greece/corfu/glyfada/domes-of-corfu-autograph-collection?holiday=34&duration=7&airport=7&date=06-04-2026&occupancy=r2c&board=2&iflight=1528016&oflight=1528013&rooms=81162&gtmsearchtype=Beach%20Search%20Results&smartsearchid=91898f4c-8f8a-4078-b0cb-16b5b69a8272',
    'sec-ch-ua': '"Google Chrome";v="143", "Chromium";v="143", "Not A(Brand";v="24"',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36',
    # 'cookie': 'mvt-460=1; akacd_prhpw=1771135323~rv=21~id=faeabf449a10059b1f0c4312c0d52a0b; OptanonAlertBoxClosed=2026-01-16T06:02:08.981Z; kndctr_081C1EAC64EE1E270A495FF9_AdobeOrg_identity=CiYzODU5MTg4MTc4OTI2NjUxNTYxMDYxODM1MDQwODY0ODM0OTY2OVITCJeWofq9MxABGAEqBElORDEwAPABl5ah%2Dr0z; kndctr_081C1EAC64EE1E270A495FF9_AdobeOrg_consent=general%3Dout; J2HPOI=TRUE; MDT=3; rxVisitor=1769158604649PU07R6EM0TUV9OSENKT36972HHCT014Q; dtSa=-; rxvt=1769160403997|1769158604650; dtPC=-23548$358604644_772h2vCFWUATNCFBDDFJBOGHFMVHEHCCRGOEBN-0e0; dtCookie=v_4_srv_4_sn_U16791KOO64KEBKIOV2P4VSEE5OCO39O_perc_100000_ol_0_mul_1_app-3A9bacd72748859223_0; BIGSC=1; ASP.NET_SessionId=vlrdl2e1l1ifr30qig0f4pn3; shell#lang=en; J2_ST=20; SC_ANALYTICS_GLOBAL_COOKIE=4b81ba62c43145b58aace5a9fee38e8d|True; AKA_A2=A; __RequestVerificationToken=_zHHwVIZMrLhonDBC1PEzDaO9gfoUPjywidZgF7MlgndzBSvYXKtf-99gA_ozy_UiO1kx5L3LzZ_0fVlSz8elUN20HUDWpEquZJ8C7Z6PBs1; PIM-SESSION-ID=ZsIzEk7516h6lFcj; _abck=4EE13BBED2730BAE212D522E13D6150B~0~YAAQzkvSF+ZhtdabAQAAglaE6g8EGMu1cC/NthekC3nkgoC6FUFxgREMW5zzT0VUdwSu8IqjV7Kb+yeavG1/QKI+QKR1A9eVQmRlnJEZIUmpHpAGriH4ZSlzJ9VFt7k1KJ8fgRy7sUewD0E4ppcnOEhwAJzmhxXl+JUvNMGtT47oiOxZhUSufsw5ULCKNyWe2JinjwXoCqoapQh4k/YMLb0IS8vMHx9uE8x5YLWIz7KAkhKRmCeELyKw036i7hsA2J5nkMNLIB640z89ZZb1XG/TUhWlp5cIrrwnEOVpj+acHD7LLuQlUav+bVOrJkSBSnwRbZBpW/79cAQEuofwq5q5PUzglGxcYI/tDqiNVQW7HLVkvwD7ID0vG8ZB7u7FlSruXwtJu899GV/S+gYMoN/KCDLQyvfkr29cWZ6YzXK+88UJd2N2GSzdl7FdCw5+dwPm5Ko0oq0lromdZSVvrZRM5vnbcpqyF/SGIy1fBxw5YOaDa08rh76uYSc/Q0Es4qgsxJlsszqrgp8dhYuSWHmyTeGxH4TvzXRY5VJJwq1rMhGg/IFtwwOhLAE1is11lC9JkVAcouz3aZba7gTehQ3yXhsb7f5QLdoAVaRP/7wdKT8ry3MjpRbTQNeN4AHQjlVzs9PNZbgJSqJb++fjClyPOB3OdvbKCI9S/LxBC1pV0tV3uuihHDPqOM+bpANNKEoAh6uUx2ky+MNNuEJW6ZWsJu6Djs+IrFxD9mNEVAqag0aZNX+OlkV7lcJnBxs6AlD/JAbHRlceNXd+FAhXpRU9QT4FfQNAhWg5n9iPce97ofgHI+l3BsYbQK0n2sYNg9W6fkd+vx+cw/+MNpFsSiDykUmIr+/fiE29qaKyOSjbxc+6L/ngDdsBTQV0luz0sUrB7RPDnBo0SL+GkAfKnKmZtCqVqQ2tVu/KPM4=~-1~-1~-1~AAQAAAAF%2f%2f%2f%2f%2f+yCMU59g81I+iOB951L1X7L1vyJiUPX3N8Jb1382WFBEL0nlHe593RxH6N+LTHQJTK1e7jrmmE%2fItC8oh70DKN5bFFBC+ijtVtMd3N6W1Zzh5k6j%2fqkb1bzI7kArQp5EVVjwzZ12Vz49PD+RCXk7mKx2Z8pzs%2fQUEZPq6ZlOXaW3LRLgL6AtZ8sFgg2LnEvM%2fCbYm4LSO8f~-1; bm_mi=EDA72793E59C0E289C26890A7FE7E287~YAAQzkvSF+dhtdabAQAAglaE6h4U1M6ST73/X1tYKnlfxEfkltRFOQWIthhSh7yl4YoGYW7jF7WkjMADe/fsnrb3JPdzONXuNDeto8gQJvOt+54Pj9pNF0I5oW9EC0DX1ErUXIkwJ3rEAse98+Jfj/L/5HJaRWk7QCBbkxypdJg/QIF2Ev4hhIUIqqeBXzUyKbcPvuD10puHO1tuxSp5znrp+hApnYYBTRlDdNoWla8zT+BE47xVIGhW77svK6bsIeEgYCXMM8Y5I/gDJ7Gz5+SLPWR0QxiTjAjqxYK/vLRNAeMAXp/Bl2pF7VDemJgvJP88wYuPQZ80TXVRPJT9+0Dc3jqRT7QRmAiG+MCDQddvx9WVgCTi+RxYyc09bS79yQw4xddCr/oE/PxrlIZNvOs=~1; bm_sz=C5C80B2B9CE5F1777570A6591C45B403~YAAQzkvSF+lhtdabAQAAglaE6h4B5/RwUf6epWnGv376B+WJJHoy7MxaNgAMm8dWC4PVl+J8OKSS7gII7X4Q+9OAObSdQJjVwoodCYayZz1o1rAraSyZPqs0tSwIkRvCJG4qbk3aoLCpvXrBJNzGqyQEWdEW9//vBQQFpD1a3AiM8A4hseTc1oOO72Fr2BauKBdVHwOGfyiranqSEkV4ye5aRKGuz0je3wc00BdYGKcupNMXYYaXh4ak0OM12KonjppH494OAwmWfmlgjmaY7feITM553q1ayCvQe/H34zyKmhhcKnelIdKNaIDvRgcKwleRofk2HkuUm7unlsxyAPUeQFMK1eD/uP6ZTFFQHsJefvMoYdlvdAybA61Ao1K9R0H/kavUVRLva+t+DJJNfWucxzcwVZEogVSinDqeq9/fOzzUSV/VBQgmKBGYDElcYM+2uZkw4dtmGWMv1aRY2gEZk4XY+a7ds5OFojQAt+1Ik00usNqY3oAoBMI24YVe/Zuoi5hnh5FF4GczcAS/pNizP/tc9oDd8maaYq/xytDI6kQH1sc=~3687473~3687987; bm_sv=4A9CF4AAABB0320903683D1D2A69354D~YAAQzkvSFxNitdabAQAAAVuE6h6VmWiaGbujNJsll7hdif1EFNvmU6bmfXg7idGEK5L6LfJdpM99Iy1b8XHyHdMUeqUe1gRTMvwlyASerQWS8JuEM79u3z+jC3yt/oBBgNsN3n8DlGVxL8q/wWL7VxV4bK6BNYeVcLbbQJGu3GxORPZu5dPXXvy+yvLpa4/QIbRmLUMNSC39ZRsXtkHTdsj3FIBwExpOpRVGT0pV9FLJ08b7QZdH9HMKLYJdXATEVALvpjz7~1; mp_d7f79c10b89f9fa3026f2fb08d3cf36d_mixpanel=%7B%22distinct_id%22%3A%20%22%24device%3A19bc5658ae96c2-0ca311ea597ff88-26061a51-144000-19bc5658ae96c2%22%2C%22%24device_id%22%3A%20%2219bc5658ae96c2-0ca311ea597ff88-26061a51-144000-19bc5658ae96c2%22%2C%22%24initial_referrer%22%3A%20%22%24direct%22%2C%22%24initial_referring_domain%22%3A%20%22%24direct%22%7D; OptanonConsent=isGpcEnabled=0&datestamp=Fri+Jan+23+2026+16%3A31%3A41+GMT%2B0530+(India+Standard+Time)&version=202510.2.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=5e216a47-8cd5-4656-b132-f8c65b92cab5&interactionCount=1&isAnonUser=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A0%2CC0003%3A0%2CC0004%3A0%2CC0007%3A0&intType=2&geolocation=IN%3BMH&AwaitingReconsent=false; ak_bmsc=CDB36BB46B1A9F2921534E7A2AAA81F2~000000000000000000000000000000~YAAQzkvSFytitdabAQAAZV2E6h4MDkbb/GX52OmGE4SKmEgUwerkMi2gs0YsbA9fKf1L0cYeLGIWhQWBQmbZwV11b5Tjbp+g77nBDwkbfYMmTrxSOHQJ/peOw0FsduTn5+QpcFufxPm6pY/jZDbqfPpZCRHCguT+HaKowuX5sdbpuMdN0yAPP8QbOu//N4sWiZBPwxhgVkkIv9e7iQDoJ1uh+js4/T5ZQ+VRSY3l1Y/dh3l3kFCv23IiYiybVqo8Df5tTWjabp8A58h1aW6XxsB1N+IkrTZzxfVvePbigkNLhAau/MlNkqLZyyecIOIA7dxY5cADD0i8JFtq9uSfTyueCU910wxCXTXLVtQatyaP2gqJ1rsnw5jip4ISQvu65B5NSDJJBFkJx4qrqA8PtvLiPitQhouvcUg5BxJmCWBMT6vd6MFok8SC8TDyVn/65KiFkKKyKX8ouXsOxg4NvcKEdPR8NBLCGYRrs2y8vwonhaUCNGyL5CMv0BMYHhEjEnf5bp/s15alx35n2otM6EedXU8CtJVPsBtStkNaj3LDvR1HDmWtbqGaWerV7r2JqW/v; RT="sl=18&ss=1769158603899&tt=94100&obo=1&sh=1769166098432%3D18%3A1%3A94100%2C1769165801890%3D17%3A1%3A87470%2C1769165797423%3D16%3A0%3A87470%2C1769165322225%3D15%3A0%3A83441%2C1769165216342%3D14%3A0%3A77507&dm=jet2holidays.com&si=28c2b77d-f6e2-4a64-b12d-7e247f513b48&rl=1&ld=1769166098432&r=https%3A%2F%2Fwww.jet2holidays.com%2Fbeach%2Fgreece%2Fcorfu%2Fglyfada%2Fdomes-of-corfu-autograph-collection%3Ff43b5cec5b564db02bc0f1e737237f23&ul=1769166278586"',
}
pdp_params = {
    'holiday': '34',
    'duration': '7',
    'airport': '7',
    'date': '06-04-2026',
    'occupancy': 'r2c',
    'iflight': '1528016',
    'oflight': '1528013',
    'gtmsearchtype': 'Beach Search Results',
    'smartsearchid': '91898f4c-8f8a-4078-b0cb-16b5b69a8272',
}

pdp_response = requests.get(
    'https://www.jet2holidays.com/beach/greece/corfu/glyfada/domes-of-corfu-autograph-collection',
    params=pdp_params,
    cookies=cookies,
    headers=headers,
)
if pdp_response.status_code == 200:
    main_selec = Selector(pdp_response.text)
    main_text = main_selec.xpath(
        '//div[@data-component="Search/HotelDetails/RoomTypeWrapper"]/@data-modeldata'
    ).get()

    if main_text:
        # Convert &quot; etc. into real characters
        main_text = html.unescape(main_text)

        # Load JSON
        room_data = json.loads(main_text)
        rooms = room_data.get("rooms", [])

        if rooms:
            rooming = rooms[0].get("roomOptions", [])
            for main_room in rooming:
                room_name = main_room.get("name")
                room_id = main_room.get("roomId")
                print(room_id)
                params = {
                    'duration': '7',
                    'airport': '7',
                    'date': '06-04-2026',
                    'occupancy': 'r2c',
                    'iflight': '1528016',
                    'oflight': '1528013',
                    'rooms': f'{room_id}',
                    'gtmsearchtype': 'Beach Search Results',
                }

                response = requests.get(
                    'https://www.jet2holidays.com/beach/greece/corfu/glyfada/domes-of-corfu-autograph-collection/options',
                    params=params,
                    cookies=cookies,
                    headers=headers,
                )
                if response.status_code == 200:
                    main_selec = Selector(response.text)
                    json_text = main_selec.xpath(
                        '//div[@data-component="Search/Options/HolidaysWrapper"]/@data-holiday-data'
                    ).get()

                    json_data = json.loads(html.unescape(json_text))
                    print(json_data)

                    boarding = json_data.get("boardBasisOptions", [])
                    for main_boarding in boarding:
                        board_name = main_boarding.get("name")
                        board_id = main_boarding.get("boardId")
                        print(board_id)
                        json_data = {
                            'airportId': 7,
                            'date': '2026-04-06T00:00:00.0000000Z',
                            'occupancy': 'r2c',
                            'boardId': board_id,
                            'inBoundFlightId': 1528016,
                            'outBoundFlightId': 1528013,
                            'rooms': [
                                room_id,
                            ],
                            'duration': 7,
                            'propertyId': 82495,
                            'earliestDepartureDate': '2026-04-01',
                            'latestDepartureDate': '2026-04-30',
                            'formatItemGuidString': 'e24701b9-b359-427b-b6d2-2bcc7609d536',
                            'settings': {
                                'updateUrlAfterChange': True,
                                'redirectAfterChange': False,
                                'spinnerType': 1,
                            },
                        }
                        main_headers = {
                            'accept': 'application/json, text/javascript, */*; q=0.01',
                            'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8,hi;q=0.7',
                            'content-type': 'application/json; charset=UTF-8',
                            'origin': 'https://www.jet2holidays.com',
                            'pagetemplateid': '{3C4592F6-E6F6-4F2A-A2EE-D6E8D64BF86D}',
                            'priority': 'u=1, i',
                            'referer': 'https://www.jet2holidays.com/beach/greece/corfu/glyfada/domes-of-corfu-autograph-collection/options?duration=7&airport=7&date=06-04-2026&occupancy=r2c&board=2&iflight=1528016&oflight=1528013&rooms=81162&gtmsearchtype=Beach%20Search%20Results',
                            'sec-ch-ua': '"Google Chrome";v="143", "Chromium";v="143", "Not A(Brand";v="24"',
                            'sec-ch-ua-mobile': '?0',
                            'sec-ch-ua-platform': '"Windows"',
                            'sec-fetch-dest': 'empty',
                            'sec-fetch-mode': 'cors',
                            'sec-fetch-site': 'same-origin',
                            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36',
                            'x-dtpc': '4$369336057_88h6vJUJOWPPFEKBDARUDQTLGGBDCRLHHBJAF-0e0',
                            'x-requested-with': 'XMLHttpRequest',
                            # 'cookie': 'mvt-460=1; akacd_prhpw=1771135323~rv=21~id=faeabf449a10059b1f0c4312c0d52a0b; OptanonAlertBoxClosed=2026-01-16T06:02:08.981Z; kndctr_081C1EAC64EE1E270A495FF9_AdobeOrg_identity=CiYzODU5MTg4MTc4OTI2NjUxNTYxMDYxODM1MDQwODY0ODM0OTY2OVITCJeWofq9MxABGAEqBElORDEwAPABl5ah%2Dr0z; kndctr_081C1EAC64EE1E270A495FF9_AdobeOrg_consent=general%3Dout; J2HPOI=TRUE; MDT=3; rxVisitor=1769158604649PU07R6EM0TUV9OSENKT36972HHCT014Q; dtSa=-; rxvt=1769160403997|1769158604650; dtPC=-23548$358604644_772h2vCFWUATNCFBDDFJBOGHFMVHEHCCRGOEBN-0e0; dtCookie=v_4_srv_4_sn_U16791KOO64KEBKIOV2P4VSEE5OCO39O_perc_100000_ol_0_mul_1_app-3A9bacd72748859223_0; BIGSC=1; ASP.NET_SessionId=vlrdl2e1l1ifr30qig0f4pn3; shell#lang=en; J2_ST=20; SC_ANALYTICS_GLOBAL_COOKIE=4b81ba62c43145b58aace5a9fee38e8d|True; __RequestVerificationToken=_zHHwVIZMrLhonDBC1PEzDaO9gfoUPjywidZgF7MlgndzBSvYXKtf-99gA_ozy_UiO1kx5L3LzZ_0fVlSz8elUN20HUDWpEquZJ8C7Z6PBs1; PIM-SESSION-ID=ZsIzEk7516h6lFcj; bm_mi=EDA72793E59C0E289C26890A7FE7E287~YAAQzkvSF+dhtdabAQAAglaE6h4U1M6ST73/X1tYKnlfxEfkltRFOQWIthhSh7yl4YoGYW7jF7WkjMADe/fsnrb3JPdzONXuNDeto8gQJvOt+54Pj9pNF0I5oW9EC0DX1ErUXIkwJ3rEAse98+Jfj/L/5HJaRWk7QCBbkxypdJg/QIF2Ev4hhIUIqqeBXzUyKbcPvuD10puHO1tuxSp5znrp+hApnYYBTRlDdNoWla8zT+BE47xVIGhW77svK6bsIeEgYCXMM8Y5I/gDJ7Gz5+SLPWR0QxiTjAjqxYK/vLRNAeMAXp/Bl2pF7VDemJgvJP88wYuPQZ80TXVRPJT9+0Dc3jqRT7QRmAiG+MCDQddvx9WVgCTi+RxYyc09bS79yQw4xddCr/oE/PxrlIZNvOs=~1; ak_bmsc=CDB36BB46B1A9F2921534E7A2AAA81F2~000000000000000000000000000000~YAAQzkvSFytitdabAQAAZV2E6h4MDkbb/GX52OmGE4SKmEgUwerkMi2gs0YsbA9fKf1L0cYeLGIWhQWBQmbZwV11b5Tjbp+g77nBDwkbfYMmTrxSOHQJ/peOw0FsduTn5+QpcFufxPm6pY/jZDbqfPpZCRHCguT+HaKowuX5sdbpuMdN0yAPP8QbOu//N4sWiZBPwxhgVkkIv9e7iQDoJ1uh+js4/T5ZQ+VRSY3l1Y/dh3l3kFCv23IiYiybVqo8Df5tTWjabp8A58h1aW6XxsB1N+IkrTZzxfVvePbigkNLhAau/MlNkqLZyyecIOIA7dxY5cADD0i8JFtq9uSfTyueCU910wxCXTXLVtQatyaP2gqJ1rsnw5jip4ISQvu65B5NSDJJBFkJx4qrqA8PtvLiPitQhouvcUg5BxJmCWBMT6vd6MFok8SC8TDyVn/65KiFkKKyKX8ouXsOxg4NvcKEdPR8NBLCGYRrs2y8vwonhaUCNGyL5CMv0BMYHhEjEnf5bp/s15alx35n2otM6EedXU8CtJVPsBtStkNaj3LDvR1HDmWtbqGaWerV7r2JqW/v; AKA_A2=A; _abck=4EE13BBED2730BAE212D522E13D6150B~0~YAAQ3VQ/F1F+JNmbAQAABG+16g9y7hKYKq6R0OxD60TwNSBrlLQj3dtD/KLvt/lZl38P6Zlqz5xxX6GBCXDd7BMi5y+E1fpxFSytEHwXbuX2C3HWmgIWr69URh6e4rTtFIMDQzaFfuEdpWD0rI83EWsOZR0I2QsgqBK5xsR8Uemfa57esUu/GPbj0z8rraSqPFXYjOHAm2Nm0SUrGHgWBGZ+zkPV6j8oAnyJT2dL56qShN71CIXBmWTaRJSm2Dn35NgZ6j9vOoeB3SAwJCy+Lol76b8AB5o0AD16NgaGJyuZmcIRDrUZE9DJNYKg8RG6/rmgCyX8JGblpVd+Y02B7fMZLbSGcQLJRrEHndrmzZN9KUVKDElENkrme8LZtdhf63Cx1IztEAMidol7ttaIthzNb73PPUuVlKTQVkd9TuMbg9M/6HUxv38/KVjl4v4GiaC1x5u8LSXlYjaUCPMVLaOOcGq9z5oXwfQ3aeN+yVeUQXY/63ecl37jiKb4Y73PaZ3D56rkebrEPknoz1p0FKnYFfeBTdt8ODBgPM0/AxP9CW9bETO8rXlpwPFGhwRVwRJ1K6Ml1fBzeS3XM7+yJbpTlLoS08WImMomWd4Qjsut308sugJg6S2/CeLlDWur4Vg3JxRk7uIlfsBhMmlZe3S9tKypK2Ja6DmDyRFFqXdBpad9xwZ4eriyKqptdNJYUpavqruoh4AwZpGSHETTiMfWlDx1QZj1sQPXJBQK7EHsdPr+plQVO5W1p2rXP2TYJs24iPa/pOpHB3kiASYJARkfkmdccZI4q1vKBay5g3Sx/fPGds9lsiRuricSmopM/w9ui2PMr9XRSGJNpUyaDb6tbsWyiR9982YQoqO+pRqOvzm9zWQei+1orsW2SOeJ8fhVVZXQlB1pi/TJwDK/ugb01APeYj2AkulgExnNa/EIZWlzl7V0QrrwAoe2NaEaCw3onGxWKJ05yWGlauTuBuZpidO8tSQGJuU=~-1~-1~-1~AAQAAAAF%2f%2f%2f%2f%2f5ROU%2fj81ia0bI44ndexfGu7yKgHzzwLZ4BS0APQ7hQQsHaXF+StlsiAG0gbYdhl7muzXU5uQc28LlvraEQPZOfzmfibc4m3FeRvXhK5vqUxTwnpSiz4tGXvbbOQqHjGiUPOeAjQfMg2EoP0klLlonl8Vu0s8he5qk00V74IGwCEbFs+iw8TjMXERQbHiRqAM0qPO2htBXLWdzctBqxpEZ%2fUS0DfjssXev8EUZtyexoNJ1Q%3d~-1; bm_sz=C5C80B2B9CE5F1777570A6591C45B403~YAAQ3VQ/FzyRJNmbAQAAYLa16h4eVxYnT46TQl0Vy6wy76Xv/pYfh3CRgxW9VOfiE/tuWKS2HXb4nk6/vUaro3nAd5tDn0JqlgNgm0GktFnUBRvodZOV70ihwgQlqCh5hh4H9j2ZqdIRZNIllqE/iQy5XAR7wmC+rNAxqAOPFLAdqG33O9PuU+eYmGShlXj2ewmacEYklSiWmuuJ+cHr19etWM7o9gOFjXKqkahTGApGT0hxa+WN4TYuRUjsYu1/vrPWbTHZCOhKB6R0qhTZKN13FeX0z+FB5aQPuSh0F2kOn1gwLj14qdXrPobk/nEyfTqVcayka75vU3i2/UA7Qwjt1LbxL7IzAil8WSBAsowdXpUIbVa9HGYTV6yrGGUcmjv8z+lzH1JU7P+ShOxL2CpbfmxF7srk/Y+ZGmp0Spt8jnfefVho+yT3LrWtw50Xfr30u5iTjoC791mx+3pYsf2T59YqmdlqxNy/fYFPGQ013YlgejtDMKew0KMxeRmgH/UiM0t15eZ41tTixG24GT2Lw74G4D0ILpHmC72goa+xGfkoA+ZWMA==~3687473~3687987; bm_sv=4A9CF4AAABB0320903683D1D2A69354D~YAAQ3VQ/F9qRJNmbAQAAHLm16h5BpliUicUzeI27+6wG8/d8enuU0YgyWE+r4wb+JSBuaaMG5rXdhZ++FsVekzWdpJTPWztAqjtTlahe1/U4eC7G1gW7on6T2+YW6lSW77M9Nt5KCz+mlTMONwuJsgMoCiNfgHC52b0Vl3/xx1a5x9thF7hX9HyCnrHf8BRM6NNN1lIZ3dzmgllDdRFiZy6v3V1ZKK8CedVuZIa3yesmxWu3+BIR8k5waranPTQWateIG+x21w==~1; OptanonConsent=isGpcEnabled=0&datestamp=Fri+Jan+23+2026+17%3A25%3A36+GMT%2B0530+(India+Standard+Time)&version=202510.2.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=5e216a47-8cd5-4656-b132-f8c65b92cab5&interactionCount=1&isAnonUser=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A0%2CC0003%3A0%2CC0004%3A0%2CC0007%3A0&intType=2&geolocation=IN%3BMH&AwaitingReconsent=false; mp_d7f79c10b89f9fa3026f2fb08d3cf36d_mixpanel=%7B%22distinct_id%22%3A%20%22%24device%3A19bc5658ae96c2-0ca311ea597ff88-26061a51-144000-19bc5658ae96c2%22%2C%22%24device_id%22%3A%20%2219bc5658ae96c2-0ca311ea597ff88-26061a51-144000-19bc5658ae96c2%22%2C%22%24initial_referrer%22%3A%20%22%24direct%22%2C%22%24initial_referring_domain%22%3A%20%22%24direct%22%7D; RT="sl=3&ss=1769169286763&tt=12229&obo=0&sh=1769169335031%3D3%3A0%3A12229%2C1769169315458%3D2%3A0%3A8685%2C1769169294101%3D1%3A0%3A2966&dm=jet2holidays.com&si=28c2b77d-f6e2-4a64-b12d-7e247f513b48&bcn=%2F%2F684d0d4a.akstat.io%2F&rl=1&ld=1769169335032"',
                        }

                        main_response = requests.post(
                            'https://www.jet2holidays.com/api/jet2/holidayswrapper/optionschanged',
                            cookies=cookies,
                            headers=main_headers,
                            json=json_data,
                        )
                        if main_response.status_code == 200:
                            main_price_data =  main_response.json()
                            holiday_price = main_price_data.get("holidayData").get("basketSummary")
                            if holiday_price:
                                per_person_price = holiday_price.get("perPersonPrice")
                                totalPrice = holiday_price.get("totalPrice")
                                print(per_person_price)
                                print(room_name)
                                print(board_name)
                                print(per_person_price)