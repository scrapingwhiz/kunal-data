# from concurrent.futures import ThreadPoolExecutor
#
# import requests
# from config import *
# def main_doc(doc):
#
#     headers = {
#         'sec-ch-ua-platform': '"Windows"',
#         'Referer': 'https://www.jet2holidays.com/beach/greece/crete-heraklion-area?airport=7&date=07-04-2026&duration=7&occupancy=r2c&sortorder=5&page=1',
#         'x-dtpc': '4$298946710_646h2vTMFJQPCMOJAFFRWBKWQGSPJPPWCAAOMV-0e0',
#         'pageTemplateId': '{767511FF-5F3E-430D-B4A7-8CA6EDAE82C0}',
#         'sec-ch-ua': '"Not:A-Brand";v="99", "Google Chrome";v="145", "Chromium";v="145"',
#         'sec-ch-ua-mobile': '?0',
#         'X-Requested-With': 'XMLHttpRequest',
#         'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36',
#         'Accept': 'application/json, text/javascript, */*; q=0.01',
#         'Content-Type': 'url-encoded',
#     }
#
#     response = requests.get('https://www.jet2holidays.com/api/jet2/searchresources/get', headers=headers)
#     print(response.status_code)
#     if response.status_code == 200:
#         selector = response.json()
#
#         # get airport code from MongoDB
#         dep_air = doc.get("Departure_Airport", "").strip()
#         airports = selector.get("airports", {})
#
#         if dep_air in airports:
#             airport_id = airports[dep_air]["id"]
#
#             search_data.update_one(
#                 {"_id": doc["_id"]},
#                 {"$set": {"dep_id_airport": airport_id}}
#             )
#
#             print(f"{dep_air} -> {airport_id} updated")
#
#
# if __name__ == "__main__":
#     with ThreadPoolExecutor(max_workers=10) as executor:
#         docs = list(search_data.find({"Status": "Pending"}))
#         executor.map(main_doc, docs)

import requests

cookies = {
    'mvt-460': '1',
    'akacd_prhpw': '1772866869~rv=41~id=6c388dfbc90a9626acf31ac0f9cc466b',
    'OptanonAlertBoxClosed': '2026-02-05T07:01:57.895Z',
    '_ga': 'GA1.1.1948792135.1770274917',
    '_gcl_au': '1.1.118792154.1770274918',
    'optimizelyEndUserId': 'oeu1770274917993r0.05985084604264501',
    '_fbp': 'fb.1.1770274918350.81170110985698888',
    '__qca': 'P1-ed9ab00c-8cd4-4b5d-b0bf-cfb39b285f29',
    'QuantumMetricUserID': 'efb7efb73885dd6be8b37c1029375a08',
    'kndctr_081C1EAC64EE1E270A495FF9_AdobeOrg_consent': 'general%3Din',
    '_tt_enable_cookie': '1',
    '_ttp': '01KGPA2QPBQ6RQHQ3E8H2B191Z_.tt.1',
    'J2HPOI': 'TRUE',
    'MDT': '3',
    'shell#lang': 'en',
    'ASP.NET_SessionId': 'eqdpmzt5z5pv2214b2bdsg0f',
    '__RequestVerificationToken': 'QrRnndHcgNVdYuBKh2dTNFNZO4zQ9D-0opckudAbE6WNSL6tnFQzEW-ADq1msiJIex2r_bVPyulq-LrILiBQzzaOX9lc9BwD8V8M-GoRR681',
    'J2_ST': '20',
    'dtCookie': 'v_4_srv_4_sn_E1B331E94167C3986892EF30F491A3E2_perc_100000_ol_0_mul_1_app-3A9bacd72748859223_0',
    'BIGSC': '2',
    'bf203_flexi_search': 'true',
    'optimizelySession': '0',
    'kndctr_081C1EAC64EE1E270A495FF9_AdobeOrg_identity': 'CiYzNzg0Nzk4MzE2MzQzMjgwMTgyMjY1NDA5NjIxODk5ODgzODM0OVITCPWy7uTCMxABGAEqBElORDEwAPABwfq65ssz',
    'PIM-SESSION-ID': 'yG7aZk5UrOFidy9w',
    'QuantumMetricSessionID': '212fef2996be49477dfe7173c8fce2a3',
    'J2H_SC': '{"Flexibility":null,"HolidayType":0,"AirportIds":[7],"DealFinderAirportIds":null,"AreaId":95,"AreaIds":null,"ResortId":0,"DepartureDate":"2026-04-07T00:00:00","DepartureMonth":"0001-01-01T00:00:00","DealFinderDepartureDate":"0001-01-01T00:00:00","Duration":7,"HolidayCalenderDuration":null,"FcpDuration":0,"SearchReferrer":0,"Occupancy":[{"Adults":2,"Children":[]}],"DepartureIds":[7],"DestinationIds":[95],"IsFamily":false,"Flexi":null}',
    'kndctr_081C1EAC64EE1E270A495FF9_AdobeOrg_cluster': 'ind1',
    'mp_d7f79c10b89f9fa3026f2fb08d3cf36d_mixpanel': '%7B%22distinct_id%22%3A%20%22%24device%3A19c2c9ad25fed-01b3efc30f77d8-26061d51-144000-19c2c9ad25fed%22%2C%22%24device_id%22%3A%20%2219c2c9ad25fed-01b3efc30f77d8-26061d51-144000-19c2c9ad25fed%22%2C%22%24initial_referrer%22%3A%20%22%24direct%22%2C%22%24initial_referring_domain%22%3A%20%22%24direct%22%7D',
    '__rtbh.uid': '%7B%22eventType%22%3A%22uid%22%2C%22id%22%3A%22GA1.1.1948792135.1770274917%22%2C%22expiryDate%22%3A%222027-03-05T10%3A09%3A35.726Z%22%7D',
    '__rtbh.lid': '%7B%22eventType%22%3A%22lid%22%2C%22id%22%3A%22Hd4LsA5Jiz1Vlq4ALJlL%22%2C%22expiryDate%22%3A%222027-03-05T10%3A09%3A35.727Z%22%7D',
    '_uetsid': '5f2769f0186111f18f09937652c675a9|1fje90u|2|g43|0|2255',
    'ttcsid': '1772705371325::TUIDglPuiNfM1__Vx48N.4.1772705376496.0::1.-2135.0::0.0.0.0::0.0.0',
    'ttcsid_CTKIM1JC77U1LI1DBSA0': '1772705371339::TvS3l0K8HsvnXFBzlRqh.4.1772705376496.1',
    '_uetvid': '905d0060026011f1b98b65f6785c7ec1|139wqet|1772705376915|4|1|bat.bing.com/p/insights/c/i',
    'ak_bmsc': 'A98043B9551DF4BF63DD181D660B99DC~000000000000000000000000000000~YAAQDhzFF65zl7KcAQAAZ3R5vR+zQI2htQp49WA7aekHWlPbAt2sp+QUKyCLL4WP1RoDe7mNYm37kRhRehObdnX2TRCIKSQB7gEmZ8S5lwuMfvWWZ08unEdmJ1N0PuDROjZgsBV4sEqUf4S0Y/hWLIhTZxIOAwQRnmum598QsVQiLU+XsaKOjTj8Eudw+5wGvLpO6H8OH4ylr9JuLstmxvh0PXdpdE1v40/p/6N1LZZTvS8OL6wdtdOs2jD7IxFSx5gwGE3twVydRqKdDBSafy37WQBgorv5PYLg1iM4tV3Q6aY2YrjZ0ABi0N9mOzv4ArNRO2GdEZ7wf9aC3/pwA0acBKJBx+hq06QGbAFXeusv4Rw8cftKyr8tJMoVdxubVe2vvOoxx7U5k+4PCr4FYn5wGcyP9aqAaYYGcctlEu0/+SvLtbjkULx0ZTvKR8iJh/oH39kcqLfCrdXN1w==',
    'cto_bundle': 'PQw5vF9LT1JVcEhCT3drWW40NkNQelFVZ0lQSjFnT3lTY0pONE85cjl0Z3g5UzlZQyUyRlNqNVNYN1h6T3lxeEowVFFEaUdzU0VoNURsVnhYWXBkWnN3S2RJSCUyQlklMkZ1MFkzeUVHMEVhczYlMkJmM2ZTVUJPdUMxdmZuWmdiM1dCUlZjclIyWDVyb2VZOGZDcU1ZRVElMkJ4cU95djBOZEVRJTNEJTNE',
    'SC_ANALYTICS_GLOBAL_COOKIE': '95e53f1a345e4d4aa9c3a584900e50b8|True',
    'bm_mi': '508209D98984C9B8BF87CED481E12F18~YAAQDhzFF8C0l7KcAQAAXrt5vR+DkkbR52gFq+TPdLFP1y6rtvePeVEJ8QBjMl7I5s7NWLZRO85U7oEyFRBcu7I23zYGUpB2x2pZqUoTNXfrKvRA89ZpZVXsNbBKQXaT97NrUDL/yUiLvLoWKq/8OqYIP6UFO6mDDRjkOlVgu/GN5tabTjHcAI0mQ2PN0ryEBV311sxX230gf/0xOs5CafICdTcfuG+5AbEwQG4T5tiM0yC5N2uOiUMkHfed8pxapqkZG3t0SeLahIj3K9r/PWp9LmJmqdQWWzI/UXMSyeePYK6kT0ZX4TPi0cKbzwFUJjXAVOx+lqYlEYQQISJgZYENwXizTKK8B3qNGn7buMdXHujT~1',
    'bm_sz': 'CC3061925023A17A8A0E6598A87E2439~YAAQDhzFF8O0l7KcAQAAXrt5vR/3g/t6r+6obvxdVKBdZxGc99V9brqmKxu4aTwkwn2fSjURh+Hg3nYbFE0PSJ2yx6wxiITPkoCm6WvDCrjQmdylQMoc/a+cJ7uLbfbWE5iSSWGnkumhPCJewJAGDQL0uTvspx9ZcIaB1D809dl1itbc64nnr4fM1RhHwsUqpEk7hYJQQFaH6c9p8xJJ05h781mEoefv8jLly8+exw98Dis0GlYNItBJuUL+MFDnS8fSBnjux4JYAnm4y/Ao0qyo0w+pGtJ/dUDqnhenyvejkNcRGN2PjQjo0Up/l+QFoxe+PNnGKQHryWAlFUsTE3wPFyOqpwsHXAWV4286GLw6icMo5yKAgRIBDj0oiAmjBYl8sCdEy25qhUP/4bVMV6dUUCOZQDuEkCVB3SFuB9cPfQO4dbA89J1I79colLbwvy0/qotnrBthr6NsIoozsCIvGC6Kqh0QRnLwF1vV/e7g7wx3WyDBl8dLK3uvPKPqrjiDZ9y0BVHkJ9xTiczQ4WXtdNO5Mbj85Sw=~3228993~3291462',
    '_ga_SERVERSIDE': 'GS2.1.s1772705373$o5$g1$t1772705397$j36$l0$h1869914066',
    '_abck': 'E33BB3D5BF8054CD87C327EBBA93723B~0~YAAQDhzFF7O1l7KcAQAAdLx5vQ/8l0f3WRipmM/G1SJ9llzS+mq4byDyb/NfXaCfsasi3bTT+xWk3uR5jtQl4dcLOcCrVqU4kFBj/7QwiDN8vGPY2rEmLk70voqK6tdxcDW7H2veiElAjyjqv8MPo8Xx3PbQx79KVJnSIJUOWHhbL+3Bui3t9j7rk3TC5QHxxtLLceqbffr/Q0tBNJRmsYSZdxNKAQr7hQah2zKehaqI6zPh85wWoka0EsA/YgHbHHTqfQ70jRUxwLi2AwkwhCCFBE5DfVJouwbEGI+saAtmQ1s8WVuW7rQZAyMttbDr/0zrOqJwbFNTID+VIizwZMpvLwSevTI6u8km1OwkPl/Fs8FiSo9Tq6EUXxaxUBwbVObDCPCTKr3kwd/Lb78Fj8BYWSf38UO2/r96e5lZ1HWKmHbcIsnlGB85fstAGBu7g30KLzDseXm51TIaKavHQWA6+bw+j9ALE2GDNAVzgWKVK01inEkpYFEW2ACV36KUuR5yIpoOrwUcrMsui8L16ekiURl4gLQiAmNUY+Y+O1WOCeJppVRqPpo2RfoxosMc6/ZNiojNEjRVzJGfdiJqvUdZen+8zESPcFPxppDzmC3sQrEwG3vLacwPuiMUapIn+iqNQeywIJnq1LW/xVi6mZvVFYsu2K+SPXbAOi1nwiVF6Y9wPNg8vFc8wr1rdmKNncwis70SNVX+QFuHDlwzrCsVsSLzsBly/GSM/VsuFXYKksDL7oC/syiS05yhtF876t484Oybd5ZoGZXglp/dRPrrHGiUwlZnPS5g4krbNUTfoffCzvar+C2bJbZ4PsnDrPAhTPWG1fd8lmwB2EgJAtui3Zh4tGztgXehMH9q5vrq5jchtLmzzqSo92CiFHAW5QQthxO8WTFRYnafQKRkTa/DN+XLCEbznAg0l7pqZ/FM4jDkc3I=~-1~-1~-1~AAQAAAAF%2f%2f%2f%2f%2f57oa0w9V9XdGrwVKp4ZPIkxdGqe2cLIMk6bVuZGbXdVX5MFoEfGrrX2YAHc5S2YBlPWKo6TMsSFJyUIgnQR+TavjQ9z7FxIXXy4SifrwaTCef9EaP0XipAV7ceLMmi00JtonYKGeLrC5vSHle6cw%2fU6Y5EYXBqI+REMEdtKJsKZGNu59n80NSu4jAuLs%2fOZFGUE5JowUKumrn0s%2fJvYrP0DkgfjUar25Z7ZFgxwwIE6PUI%3d~-1',
    'RT': '"sl=0&ss=1772705371399&tt=0&obo=0&sh=&dm=jet2holidays.com&si=undefined"',
    '_ga_QBB92EKVS3': 'GS2.1.s1772705373$o4$g1$t1772705397$j36$l0$h0',
    'OptanonConsent': 'isGpcEnabled=0&datestamp=Thu+Mar+05+2026+15%3A39%3A58+GMT%2B0530+(India+Standard+Time)&version=202510.2.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=2ee8a4ac-ab2b-4dc9-8c30-e3a2d64e224d&interactionCount=1&isAnonUser=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1%2CC0004%3A1%2CC0007%3A1&intType=1&geolocation=IN%3BGJ&AwaitingReconsent=false',
    'bm_sv': 'ECDF52D24B5A499FC6E1FF4F22C8003E~YAAQDhzFFxG5l7KcAQAArsB5vR9iqJ4Uamocdic2/Wd4zbrT+kwKroCTNjiRIsZvdUAkFg/6hZbU06Cz80oQYuzZWisVhAvQgWa+RRcGv97U+aLI9lJsmaVpVNdlCFt5QDDi4lrLX3lcRwcAV9f2lZI/NMU2t8RVGb1f2bP7kUb4mBT9ZSP2XzGKYm7kWSQlwMBp6I0NpYhL6NyJ8ERLZD0uK1TZlOmzxQ0iR/KFZRRVU1n0KPP9h7nvvpHRTqgWxw3IstipsQ==~1',
}

headers = {
    'accept': 'application/json, text/javascript, */*; q=0.01',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8,hi;q=0.7',
    'content-type': 'url-encoded',
    'pagetemplateid': '{767511FF-5F3E-430D-B4A7-8CA6EDAE82C0}',
    'priority': 'u=1, i',
    'referer': 'https://www.jet2holidays.com/beach/greece/crete-heraklion-area?airport=7&date=07-04-2026&duration=7&occupancy=r2c&sortorder=5&page=1',
    'sec-ch-ua': '"Not:A-Brand";v="99", "Google Chrome";v="145", "Chromium";v="145"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36',
    'x-dtpc': '4$305397200_340h3vOLCLQRMCRKUEDKHHHLHAFHVKUCDQDLCK-0e0',
    'x-requested-with': 'XMLHttpRequest',
    # 'cookie': 'mvt-460=1; akacd_prhpw=1772866869~rv=41~id=6c388dfbc90a9626acf31ac0f9cc466b; OptanonAlertBoxClosed=2026-02-05T07:01:57.895Z; _ga=GA1.1.1948792135.1770274917; _gcl_au=1.1.118792154.1770274918; optimizelyEndUserId=oeu1770274917993r0.05985084604264501; _fbp=fb.1.1770274918350.81170110985698888; __qca=P1-ed9ab00c-8cd4-4b5d-b0bf-cfb39b285f29; QuantumMetricUserID=efb7efb73885dd6be8b37c1029375a08; kndctr_081C1EAC64EE1E270A495FF9_AdobeOrg_consent=general%3Din; _tt_enable_cookie=1; _ttp=01KGPA2QPBQ6RQHQ3E8H2B191Z_.tt.1; J2HPOI=TRUE; MDT=3; shell#lang=en; ASP.NET_SessionId=eqdpmzt5z5pv2214b2bdsg0f; __RequestVerificationToken=QrRnndHcgNVdYuBKh2dTNFNZO4zQ9D-0opckudAbE6WNSL6tnFQzEW-ADq1msiJIex2r_bVPyulq-LrILiBQzzaOX9lc9BwD8V8M-GoRR681; J2_ST=20; dtCookie=v_4_srv_4_sn_E1B331E94167C3986892EF30F491A3E2_perc_100000_ol_0_mul_1_app-3A9bacd72748859223_0; BIGSC=2; bf203_flexi_search=true; optimizelySession=0; kndctr_081C1EAC64EE1E270A495FF9_AdobeOrg_identity=CiYzNzg0Nzk4MzE2MzQzMjgwMTgyMjY1NDA5NjIxODk5ODgzODM0OVITCPWy7uTCMxABGAEqBElORDEwAPABwfq65ssz; PIM-SESSION-ID=yG7aZk5UrOFidy9w; QuantumMetricSessionID=212fef2996be49477dfe7173c8fce2a3; J2H_SC={"Flexibility":null,"HolidayType":0,"AirportIds":[7],"DealFinderAirportIds":null,"AreaId":95,"AreaIds":null,"ResortId":0,"DepartureDate":"2026-04-07T00:00:00","DepartureMonth":"0001-01-01T00:00:00","DealFinderDepartureDate":"0001-01-01T00:00:00","Duration":7,"HolidayCalenderDuration":null,"FcpDuration":0,"SearchReferrer":0,"Occupancy":[{"Adults":2,"Children":[]}],"DepartureIds":[7],"DestinationIds":[95],"IsFamily":false,"Flexi":null}; kndctr_081C1EAC64EE1E270A495FF9_AdobeOrg_cluster=ind1; mp_d7f79c10b89f9fa3026f2fb08d3cf36d_mixpanel=%7B%22distinct_id%22%3A%20%22%24device%3A19c2c9ad25fed-01b3efc30f77d8-26061d51-144000-19c2c9ad25fed%22%2C%22%24device_id%22%3A%20%2219c2c9ad25fed-01b3efc30f77d8-26061d51-144000-19c2c9ad25fed%22%2C%22%24initial_referrer%22%3A%20%22%24direct%22%2C%22%24initial_referring_domain%22%3A%20%22%24direct%22%7D; __rtbh.uid=%7B%22eventType%22%3A%22uid%22%2C%22id%22%3A%22GA1.1.1948792135.1770274917%22%2C%22expiryDate%22%3A%222027-03-05T10%3A09%3A35.726Z%22%7D; __rtbh.lid=%7B%22eventType%22%3A%22lid%22%2C%22id%22%3A%22Hd4LsA5Jiz1Vlq4ALJlL%22%2C%22expiryDate%22%3A%222027-03-05T10%3A09%3A35.727Z%22%7D; _uetsid=5f2769f0186111f18f09937652c675a9|1fje90u|2|g43|0|2255; ttcsid=1772705371325::TUIDglPuiNfM1__Vx48N.4.1772705376496.0::1.-2135.0::0.0.0.0::0.0.0; ttcsid_CTKIM1JC77U1LI1DBSA0=1772705371339::TvS3l0K8HsvnXFBzlRqh.4.1772705376496.1; _uetvid=905d0060026011f1b98b65f6785c7ec1|139wqet|1772705376915|4|1|bat.bing.com/p/insights/c/i; ak_bmsc=A98043B9551DF4BF63DD181D660B99DC~000000000000000000000000000000~YAAQDhzFF65zl7KcAQAAZ3R5vR+zQI2htQp49WA7aekHWlPbAt2sp+QUKyCLL4WP1RoDe7mNYm37kRhRehObdnX2TRCIKSQB7gEmZ8S5lwuMfvWWZ08unEdmJ1N0PuDROjZgsBV4sEqUf4S0Y/hWLIhTZxIOAwQRnmum598QsVQiLU+XsaKOjTj8Eudw+5wGvLpO6H8OH4ylr9JuLstmxvh0PXdpdE1v40/p/6N1LZZTvS8OL6wdtdOs2jD7IxFSx5gwGE3twVydRqKdDBSafy37WQBgorv5PYLg1iM4tV3Q6aY2YrjZ0ABi0N9mOzv4ArNRO2GdEZ7wf9aC3/pwA0acBKJBx+hq06QGbAFXeusv4Rw8cftKyr8tJMoVdxubVe2vvOoxx7U5k+4PCr4FYn5wGcyP9aqAaYYGcctlEu0/+SvLtbjkULx0ZTvKR8iJh/oH39kcqLfCrdXN1w==; cto_bundle=PQw5vF9LT1JVcEhCT3drWW40NkNQelFVZ0lQSjFnT3lTY0pONE85cjl0Z3g5UzlZQyUyRlNqNVNYN1h6T3lxeEowVFFEaUdzU0VoNURsVnhYWXBkWnN3S2RJSCUyQlklMkZ1MFkzeUVHMEVhczYlMkJmM2ZTVUJPdUMxdmZuWmdiM1dCUlZjclIyWDVyb2VZOGZDcU1ZRVElMkJ4cU95djBOZEVRJTNEJTNE; SC_ANALYTICS_GLOBAL_COOKIE=95e53f1a345e4d4aa9c3a584900e50b8|True; bm_mi=508209D98984C9B8BF87CED481E12F18~YAAQDhzFF8C0l7KcAQAAXrt5vR+DkkbR52gFq+TPdLFP1y6rtvePeVEJ8QBjMl7I5s7NWLZRO85U7oEyFRBcu7I23zYGUpB2x2pZqUoTNXfrKvRA89ZpZVXsNbBKQXaT97NrUDL/yUiLvLoWKq/8OqYIP6UFO6mDDRjkOlVgu/GN5tabTjHcAI0mQ2PN0ryEBV311sxX230gf/0xOs5CafICdTcfuG+5AbEwQG4T5tiM0yC5N2uOiUMkHfed8pxapqkZG3t0SeLahIj3K9r/PWp9LmJmqdQWWzI/UXMSyeePYK6kT0ZX4TPi0cKbzwFUJjXAVOx+lqYlEYQQISJgZYENwXizTKK8B3qNGn7buMdXHujT~1; bm_sz=CC3061925023A17A8A0E6598A87E2439~YAAQDhzFF8O0l7KcAQAAXrt5vR/3g/t6r+6obvxdVKBdZxGc99V9brqmKxu4aTwkwn2fSjURh+Hg3nYbFE0PSJ2yx6wxiITPkoCm6WvDCrjQmdylQMoc/a+cJ7uLbfbWE5iSSWGnkumhPCJewJAGDQL0uTvspx9ZcIaB1D809dl1itbc64nnr4fM1RhHwsUqpEk7hYJQQFaH6c9p8xJJ05h781mEoefv8jLly8+exw98Dis0GlYNItBJuUL+MFDnS8fSBnjux4JYAnm4y/Ao0qyo0w+pGtJ/dUDqnhenyvejkNcRGN2PjQjo0Up/l+QFoxe+PNnGKQHryWAlFUsTE3wPFyOqpwsHXAWV4286GLw6icMo5yKAgRIBDj0oiAmjBYl8sCdEy25qhUP/4bVMV6dUUCOZQDuEkCVB3SFuB9cPfQO4dbA89J1I79colLbwvy0/qotnrBthr6NsIoozsCIvGC6Kqh0QRnLwF1vV/e7g7wx3WyDBl8dLK3uvPKPqrjiDZ9y0BVHkJ9xTiczQ4WXtdNO5Mbj85Sw=~3228993~3291462; _ga_SERVERSIDE=GS2.1.s1772705373$o5$g1$t1772705397$j36$l0$h1869914066; _abck=E33BB3D5BF8054CD87C327EBBA93723B~0~YAAQDhzFF7O1l7KcAQAAdLx5vQ/8l0f3WRipmM/G1SJ9llzS+mq4byDyb/NfXaCfsasi3bTT+xWk3uR5jtQl4dcLOcCrVqU4kFBj/7QwiDN8vGPY2rEmLk70voqK6tdxcDW7H2veiElAjyjqv8MPo8Xx3PbQx79KVJnSIJUOWHhbL+3Bui3t9j7rk3TC5QHxxtLLceqbffr/Q0tBNJRmsYSZdxNKAQr7hQah2zKehaqI6zPh85wWoka0EsA/YgHbHHTqfQ70jRUxwLi2AwkwhCCFBE5DfVJouwbEGI+saAtmQ1s8WVuW7rQZAyMttbDr/0zrOqJwbFNTID+VIizwZMpvLwSevTI6u8km1OwkPl/Fs8FiSo9Tq6EUXxaxUBwbVObDCPCTKr3kwd/Lb78Fj8BYWSf38UO2/r96e5lZ1HWKmHbcIsnlGB85fstAGBu7g30KLzDseXm51TIaKavHQWA6+bw+j9ALE2GDNAVzgWKVK01inEkpYFEW2ACV36KUuR5yIpoOrwUcrMsui8L16ekiURl4gLQiAmNUY+Y+O1WOCeJppVRqPpo2RfoxosMc6/ZNiojNEjRVzJGfdiJqvUdZen+8zESPcFPxppDzmC3sQrEwG3vLacwPuiMUapIn+iqNQeywIJnq1LW/xVi6mZvVFYsu2K+SPXbAOi1nwiVF6Y9wPNg8vFc8wr1rdmKNncwis70SNVX+QFuHDlwzrCsVsSLzsBly/GSM/VsuFXYKksDL7oC/syiS05yhtF876t484Oybd5ZoGZXglp/dRPrrHGiUwlZnPS5g4krbNUTfoffCzvar+C2bJbZ4PsnDrPAhTPWG1fd8lmwB2EgJAtui3Zh4tGztgXehMH9q5vrq5jchtLmzzqSo92CiFHAW5QQthxO8WTFRYnafQKRkTa/DN+XLCEbznAg0l7pqZ/FM4jDkc3I=~-1~-1~-1~AAQAAAAF%2f%2f%2f%2f%2f57oa0w9V9XdGrwVKp4ZPIkxdGqe2cLIMk6bVuZGbXdVX5MFoEfGrrX2YAHc5S2YBlPWKo6TMsSFJyUIgnQR+TavjQ9z7FxIXXy4SifrwaTCef9EaP0XipAV7ceLMmi00JtonYKGeLrC5vSHle6cw%2fU6Y5EYXBqI+REMEdtKJsKZGNu59n80NSu4jAuLs%2fOZFGUE5JowUKumrn0s%2fJvYrP0DkgfjUar25Z7ZFgxwwIE6PUI%3d~-1; RT="sl=0&ss=1772705371399&tt=0&obo=0&sh=&dm=jet2holidays.com&si=undefined"; _ga_QBB92EKVS3=GS2.1.s1772705373$o4$g1$t1772705397$j36$l0$h0; OptanonConsent=isGpcEnabled=0&datestamp=Thu+Mar+05+2026+15%3A39%3A58+GMT%2B0530+(India+Standard+Time)&version=202510.2.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=2ee8a4ac-ab2b-4dc9-8c30-e3a2d64e224d&interactionCount=1&isAnonUser=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A1%2CC0003%3A1%2CC0004%3A1%2CC0007%3A1&intType=1&geolocation=IN%3BGJ&AwaitingReconsent=false; bm_sv=ECDF52D24B5A499FC6E1FF4F22C8003E~YAAQDhzFFxG5l7KcAQAArsB5vR9iqJ4Uamocdic2/Wd4zbrT+kwKroCTNjiRIsZvdUAkFg/6hZbU06Cz80oQYuzZWisVhAvQgWa+RRcGv97U+aLI9lJsmaVpVNdlCFt5QDDi4lrLX3lcRwcAV9f2lZI/NMU2t8RVGb1f2bP7kUb4mBT9ZSP2XzGKYm7kWSQlwMBp6I0NpYhL6NyJ8ERLZD0uK1TZlOmzxQ0iR/KFZRRVU1n0KPP9h7nvvpHRTqgWxw3IstipsQ==~1',
}

params = {
    'departureAirportIds': '7',
    'destinationAreaIds': '95',
    'departureDate': '2026-04-07',
    'durations': '7',
    'occupancies': '2',
    'pageNumber': '1',
    'pageSize': '24',
    'sortOrder': '5',
    'filters': '',
    'holidayTypeId': '1',
    'flexibility': '0',
    'minPrice': '',
    'includePriceBreakDown': 'false',
    'brandId': '',
    'inboundFlightId': '0',
    'outboundFlightId': '0',
    'gtmSearchType': 'Beach Search Results',
    'searchId': '',
    'applyDiscount': 'false',
    'occupancyOpen': 'false',
    'useMultiSearch': 'false',
    'defaultSearchParametersUsed': 'false',
    'inboundFlightTimes': '',
    'outboundFlightTimes': '',
    'flexi': '',
}

response = requests.get('https://www.jet2holidays.com/api/jet2/search/search', params=params, cookies=cookies, headers=headers)

print(response.status_code)
print(response.json())