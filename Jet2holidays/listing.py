import html
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime
import requests
from config import *
def process_doc(doc):
    match_hotel_name = doc['Hotel_Name']
    destination = doc['Destination']
    country = doc['Country']
    dep_id_airport = doc['dep_id_airport']
    dep_air = doc['Departure_Airport']
    in_dates = doc['Check_In_Date']
    out_dates = doc['Check_Out_Date']
    nights = doc['Nights']
    Pax = doc['Pax']
    sorce_market = doc['Source_Market']
    date_obj = datetime.strptime(in_dates, "%m/%d/%Y")
    check_obj = datetime.strptime(out_dates, "%m/%d/%Y")

    # convert to required format
    formatted_date = date_obj.strftime("%Y-%m-%d")
    check_outs_date = check_obj.strftime("%Y-%m-%d")

    print(formatted_date)
    j2h_sc = {
        "Flexibility": None,
        "HolidayType": 0,
        "AirportIds": [dep_id_airport],
        "AreaId": 95,
        "ResortId": 0,
        "DepartureDate": f"{formatted_date}T00:00:00",
        "DepartureMonth": "0001-01-01T00:00:00",
        "Duration": nights,
        "SearchReferrer": 0,
        "Occupancy": [
            {
                "Adults": Pax,
                "Children": []
            }
        ],
        "DepartureIds": [dep_id_airport],
        "DestinationIds": [95],
        "IsFamily": False
    }


    j2h_sc_cookie = json.dumps(j2h_sc)
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
        'J2H_SC': j2h_sc_cookie,
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
        'referer': f'https://www.jet2holidays.com/beach/greece/crete-heraklion-area?airport={dep_id_airport}&date={formatted_date}&duration=7&occupancy=r2c&sortorder=5&page=1',
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
        'departureAirportIds': f'{dep_id_airport}',
        'destinationAreaIds': '94',
        'departureDate': f'{formatted_date}',
        'durations': f'{nights}',
        'occupancies': f'{Pax}',
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
    if response.status_code == 200:
        print(response.status_code)
        main_data = response.json()



        # main_data = response.json()
        results = main_data.get('results',{})
        filters = main_data.get('filters',{}).get('boardbasis',[])

        for data in results:
            hotel_url = data.get('url')
            path = hotel_url.split('?')[0]  # "/beach/greece/corfu/glyfada/domes-of-corfu-autograph-collection"

            # Split by '/'
            parts = path.split(
                '/')  # ['', 'beach', 'greece', 'corfu', 'glyfada', 'domes-of-corfu-autograph-collection']

            # Take the last two parts
            main_result = '/'.join(parts[-2:])
            main_hotel_url = f"https://www.jet2holidays.com{hotel_url}"
            night = data.get('duration')
            duration = data.get('duration')
            property_data = data.get('property',{})
            hotel_id = property_data.get('id')
            city = property_data.get('area')
            hotel_name = property_data.get('name')
            website_rating = property_data.get('rating')
            ReviewCount = property_data.get('tripAdvisorReviewCount')
            Rating = property_data.get('tripAdvisorRating')
            flights = main_data.get('flights', [])

            if flights:  # make sure list is not empty
                main_course = flights[0].get('outbound')
                inbound = flights[0].get('inbound')
                if inbound:
                    in_depart_time = inbound.get('departureDateTimeLocal')
                    in_flight_code = inbound.get('flightId')
                    in_arr_date = inbound.get('arrivalDateTimeLocal')
                if main_course:  # make sure outbound exists
                    departure_airport = main_course.get('departureAirportCode')
                    out_flight_code = main_course.get('flightId')
                    arrival_airport = main_course.get('arrivalAirportCode')
                    our_depart_date = main_course.get('departureDateTimeLocal')
                    our_arr_date = main_course.get('arrivalDateTimeLocal')

                    print("Departure:", our_depart_date)
                    print("Arrival:", our_arr_date)
            rooms = data.get('rooms', [])  # rooms is a list
            if rooms:  # make sure list is not empty
                room_name = rooms[0].get('description', '')  # first room
                room_id = rooms[0].get('roomId', '')  # first room
                print(room_name)
            accommodation_options = data.get('accommodationOptions', [])
            if accommodation_options:  # make sure list is not empty
                first_accommodation = accommodation_options[0]

                price_options = first_accommodation.get('priceOptions', [])
                if price_options:
                    first_price = price_options[0]

                    total_price = first_price.get('totalPrice')
                    per_p_price = first_price.get('pricePerPerson')
                    if not price_options:
                        continue

                    price_option = price_options[0]

                    included_items = price_option.get("includedItems", [])

                    # Initialize flags
                    transfer = "Excluded"
                    luggage = "Excluded"

                    for item in included_items:
                        item_type = item.get("type", "")
                        description = item.get("description", "").lower()

                        # Check transfer
                        if item_type in ("Transfers", "Car Hire"):
                            transfer = "Included"

                        # Check luggage / baggage
                        if item_type in ("HoldBaggage", "HandBaggage") or "baggage" in description:
                            luggage = "Included"

                    print("Transfer:", transfer, "| Luggage:", luggage)


                scraped_date = datetime.now().strftime("%d-%m-%y")
                date_obj = datetime.fromisoformat(in_arr_date)

                # Format as d/m/Y without leading zeros (works on all OS)
                formatted_date = f"{date_obj.day}/{date_obj.month}/{date_obj.year}"
                # filters.boardbasis[1].name
                print(formatted_date)
                params = {
                    'duration': f'{nights}',
                    'airport': '7',
                    'date': f'{formatted_date}',
                    'occupancy': 'r2c',
                    'iflight': '1528016',
                    'oflight': '1528013',
                    'rooms': f'{room_id}',
                    'gtmsearchtype': 'Beach Search Results',
                }
                cookies = {
                    'J2HPOI': 'TRUE',
                    'mvt-460': '0',
                    'MDT': '3',
                    'akacd_prhpw': '1772261386~rv=13~id=ff4e5169c101f4ab888f6da0109f4fd1',
                    'rxVisitor': '1769669386213VM1IQKG31TNM7I04DNMLTODOARS9SJMS',
                    'dtSa': '-',
                    'dtPC': '-26709$269386211_394h1vVHJKAEQDBOCJCAAIPURHUOAWCCVPECKB-0e0',
                    'dtCookie': 'v_4_srv_5_sn_21JIBMU6I33CMJI1QHBCN6A6REM43S24_perc_100000_ol_0_mul_1_app-3A9bacd72748859223_0',
                    'rxvt': '1769671185298|1769669386214',
                    'shell#lang': 'en',
                    'ASP.NET_SessionId': 'aqlcabne1u1pag0o415wufzh',
                    'J2_ST': '20',
                    'BIGSC': '2',
                    'ak_bmsc': 'BF813806136A686B51864580620F4298~000000000000000000000000000000~YAAQDxzFFyabmOebAQAAh+aDCB7ZhjS8zhZJjHSC1TY3cUX8FqygLwQM5asijz5GJtvCBaYTjf5Lwlfpx1HIH6FujFh90LIbfdWWRybf6NxUnCdsPl7cjS0dkvVfagxdFb2MHgPv6JE67zwnjUcdNtfy/OmoFdOmo+WVJwOWJ7y1sUekdcOWBEMUmMZT3JfoGUyKrZ5ujQ+DjcTPt9gHNh4NXEBznDmJ8wXlHmLIqlZBIY+T1ZvLJCKbdp9VK/9WWmVsssRqeUAmRSY49Qcs1jn8J4/060PJUG80AVyD6Ow2qTACZTBqcIcYayVEx/R9YgaRsr/ZbpsYCd4Lr/1E0ETurX5vbxDk78TJ6Adv6K9R2Rp2oidKT4/oHll19JColIcQ67Xzbq8in+hvz1pnNx1+a5xwlnV4Vr2F8iWLXjfAJ+cUk8Uk7fRfT+WgHJi4fbjtSooTQZ15tjGffSz/bQd3dESe',
                    'OptanonAlertBoxClosed': '2026-01-29T06:49:49.284Z',
                    'kndctr_081C1EAC64EE1E270A495FF9_AdobeOrg_identity': 'CiY3NjE2Mzk1NTYxMDA3NTk2NDAxMTc3NDg4NTI3MDkxNjQxODEzNVITCPTdj8TAMxABGAEqBElORDEwAPAB9N2PxMAz',
                    'kndctr_081C1EAC64EE1E270A495FF9_AdobeOrg_cluster': 'ind1',
                    'kndctr_081C1EAC64EE1E270A495FF9_AdobeOrg_consent': 'general%3Dout',
                    'SC_ANALYTICS_GLOBAL_COOKIE': '9fbefd76b88b4835b93a8bebfe0bee90|True',
                    'bm_sz': '04D27C0135EEABBF584D688150BA36EF~YAAQCxzFF7a5xwGcAQAAlHOMCB47uoqAkAhlPkNfn1ADOmN2aWu/hgBH70PVEW211EJJYQsY/ZjoJDKA1fsjvjLimEYwjzxlgzKMG3TKR7CgjoDGSMcJwT/Ujkhhm3N+UwV+IOJwLNcVfdBWBvDOPTdakS+JOexPL8fVV4azkIuN4SwF3eR5+yqxJNTSusEUVBnJxEiOEdlY51Mm4BsNCpBhbFj8IZ46LlqktR/RuCW2b7EZEJqKQhn0n+SkmMzdlbLVxZetZtFGgNlGa+WiVlR/jn6pJY2riHC8q0RDqa9+naU6Q9/k65pwGrd5pIL3PN24MCRIcUlvCawinq89KcHSU0G9peIoFk0RdoNDBjtXPOvz8DsBASkUVqGAjjeIHOAgnsare1915nJttARcLUD1kK0MlVDa07OJHL1y5nwEPfdR8ggRyZrnzbxoTd4vrqz+3b+JSWBIrMzB+A==~3552048~3617606',
                    '_abck': 'DDC3EF766C916643DD1CF57834504196~0~YAAQCxzFF9i5xwGcAQAALHSMCA9anYbJMlu8suGdOwJI5Nt8tKsAig2i3p+CZkPA82rB28qLut5js1fmasYvV0t8XGpFQCYNKLhA/Yf1/HXt/hiIsgTCQG1iHOqQggC7KUuz5Io30CGAb8f6Z+421cIjgXhYb3pGhVgS0fBw0BxBCYXpeHnmXDdtpJwQgwxPAXrMcCCDSXSL+S4/biTcKmrlqwRyrTs43COyItiPrB7wU7ezt832Mr5aaJDqgpNwsILzHpIeD6rhKp+zkGVikZEmSGkppwGymA2cXsGr8AkuxipyO2nOijQhHqfUDZlE3nm7U1Sjs5TtGYziXDEHYhREC7Ct5kgw5D0ddA5qTpza6uWm2aq8D+TAzh3401EI1bD4owwW+Rfeh+JOaRv75x5Nthtz36YoWH2D4FChAJJG/SxfzuHQmjnTJxwTq6AP4dEZgmDqcIw1pwfW0mEJtRJM6aij6Nb/Iu1cjGr7thr8XCyT+NSkH23s8QEySzfYxUDc6cNBRN/SBLRxpW/htS4XmD4Cz0mNl0++n7Rohi/K/ZxT9AfcOLIldwlQfwQB16Gk8Kq2QmASUoEa81tRDcrE77UKhJMWBDKg/mYg8+Azpr3tdeRNhNs2c2aceohCoTBegfzJztBIld45ujpkLYQBqPz84vV3QJr45SQhmSM120fEzcf+6z6boH7SjcbgpKd2gFWebuqZ+bg7UD27oslNLpIHh3OosUbQcwzXuR4LVYxyqrMl7L4QdPl20plu5aES0TFteuQph02mmN2EQUIJnOm2SMckonMANErmBy5gqdqhOrutNLhkB6n+3w/R7uOzhGHURcVhCL/ibiMoZskl6K25CYdkMDcoU0u0IZaKPXty6PJmHDEb4yr9vsuo20iVsQqBqll3aw==~-1~-1~-1~AAQAAAAF%2f%2f%2f%2f%2f3TONW8+VGBlbgAonU1dM23pwx4OXkpqQfgz9tlhaCEdomy4QUn4S6d9+UeYU%2fUZKianU9abDwQE7yyujE4i6rIppYg+7VHIVNO4tkXf8RrN9EdVL8EMGk8yVlwvJmrLc9E%2fXPg%3d~-1',
                    'OptanonConsent': 'isGpcEnabled=0&datestamp=Thu+Jan+29+2026+12%3A29%3A08+GMT%2B0530+(India+Standard+Time)&version=202510.2.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=3f86b333-267e-421a-bcc5-c118907ba734&interactionCount=1&isAnonUser=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A0%2CC0003%3A0%2CC0004%3A0%2CC0007%3A0&intType=2&geolocation=IN%3BGJ&AwaitingReconsent=false',
                    'bm_sv': '23DAC3BB62FB03DFA0E53042FA28A8EB~YAAQCxzFF33OxwGcAQAAcrOMCB52YZfzq9HJqgPucg0PWwzHhcmWCDk28p5+kVMO2LqW/G6cbWNHa4ed99H2TT0Iua+tRzyir//FJXKgRwnqZ/V5DCWhgmQ+xTWgPEZ8sEOobjGAa66CQj1fEoH1yqU3rWoOb2XZtFEJHOgE8sT+vCfzjywm1/MucZSanCK15MYMnH77U6c0qUDs466c/ExXah550cmKtDjFAgc8lYRVJM7dqQxcZAlzuYuYx6PlV4w5il2q3g==~1',
                    'RT': '"sl=6&ss=1769669385216&tt=30104&obo=0&sh=1769669946941%3D6%3A0%3A30104%2C1769669911708%3D5%3A0%3A26167%2C1769669899345%3D4%3A0%3A18327%2C1769669889600%3D3%3A0%3A14472%2C1769669745440%3D2%3A0%3A6243&dm=jet2holidays.com&si=82vmdkk4zj6&rl=1&ld=1769669946941&r=https%3A%2F%2Fwww.jet2holidays.com%2Fbeach%2Fgreece%2Fcorfu%2Fglyfada%2Fdomes-of-corfu-autograph-collection%2Foptions%3Fd66f8bc00412cf59e32972f7893f73a3&ul=1769670147236"',
                }

                headers = {
                    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
                    'accept-language': 'en-US,en;q=0.9,hi;q=0.8',
                    'cache-control': 'max-age=0',
                    'priority': 'u=0, i',
                    # 'referer': 'https://www.jet2holidays.com/beach/greece/corfu/glyfada/domes-of-corfu-autograph-collection?holiday=34&duration=7&airport=7&date=06-04-2026&occupancy=r2c&board=2&iflight=1528016&oflight=1528013&rooms=81162&gtmsearchtype=Beach%20Search%20Results&smartsearchid=48e74d42-f147-459d-ba39-cc6d41fbbc1a',
                    'sec-ch-ua': '"Not(A:Brand";v="8", "Chromium";v="144", "Google Chrome";v="144"',
                    'sec-ch-ua-mobile': '?0',
                    'sec-ch-ua-platform': '"Windows"',
                    'sec-fetch-dest': 'document',
                    'sec-fetch-mode': 'navigate',
                    'sec-fetch-site': 'same-origin',
                    'sec-fetch-user': '?1',
                    'upgrade-insecure-requests': '1',
                    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/144.0.0.0 Safari/537.36',
                    # 'cookie': 'J2HPOI=TRUE; mvt-460=0; MDT=3; akacd_prhpw=1772261386~rv=13~id=ff4e5169c101f4ab888f6da0109f4fd1; rxVisitor=1769669386213VM1IQKG31TNM7I04DNMLTODOARS9SJMS; dtSa=-; dtPC=-26709$269386211_394h1vVHJKAEQDBOCJCAAIPURHUOAWCCVPECKB-0e0; dtCookie=v_4_srv_5_sn_21JIBMU6I33CMJI1QHBCN6A6REM43S24_perc_100000_ol_0_mul_1_app-3A9bacd72748859223_0; rxvt=1769671185298|1769669386214; shell#lang=en; ASP.NET_SessionId=aqlcabne1u1pag0o415wufzh; J2_ST=20; BIGSC=2; ak_bmsc=BF813806136A686B51864580620F4298~000000000000000000000000000000~YAAQDxzFFyabmOebAQAAh+aDCB7ZhjS8zhZJjHSC1TY3cUX8FqygLwQM5asijz5GJtvCBaYTjf5Lwlfpx1HIH6FujFh90LIbfdWWRybf6NxUnCdsPl7cjS0dkvVfagxdFb2MHgPv6JE67zwnjUcdNtfy/OmoFdOmo+WVJwOWJ7y1sUekdcOWBEMUmMZT3JfoGUyKrZ5ujQ+DjcTPt9gHNh4NXEBznDmJ8wXlHmLIqlZBIY+T1ZvLJCKbdp9VK/9WWmVsssRqeUAmRSY49Qcs1jn8J4/060PJUG80AVyD6Ow2qTACZTBqcIcYayVEx/R9YgaRsr/ZbpsYCd4Lr/1E0ETurX5vbxDk78TJ6Adv6K9R2Rp2oidKT4/oHll19JColIcQ67Xzbq8in+hvz1pnNx1+a5xwlnV4Vr2F8iWLXjfAJ+cUk8Uk7fRfT+WgHJi4fbjtSooTQZ15tjGffSz/bQd3dESe; OptanonAlertBoxClosed=2026-01-29T06:49:49.284Z; kndctr_081C1EAC64EE1E270A495FF9_AdobeOrg_identity=CiY3NjE2Mzk1NTYxMDA3NTk2NDAxMTc3NDg4NTI3MDkxNjQxODEzNVITCPTdj8TAMxABGAEqBElORDEwAPAB9N2PxMAz; kndctr_081C1EAC64EE1E270A495FF9_AdobeOrg_cluster=ind1; kndctr_081C1EAC64EE1E270A495FF9_AdobeOrg_consent=general%3Dout; SC_ANALYTICS_GLOBAL_COOKIE=9fbefd76b88b4835b93a8bebfe0bee90|True; bm_sz=04D27C0135EEABBF584D688150BA36EF~YAAQCxzFF7a5xwGcAQAAlHOMCB47uoqAkAhlPkNfn1ADOmN2aWu/hgBH70PVEW211EJJYQsY/ZjoJDKA1fsjvjLimEYwjzxlgzKMG3TKR7CgjoDGSMcJwT/Ujkhhm3N+UwV+IOJwLNcVfdBWBvDOPTdakS+JOexPL8fVV4azkIuN4SwF3eR5+yqxJNTSusEUVBnJxEiOEdlY51Mm4BsNCpBhbFj8IZ46LlqktR/RuCW2b7EZEJqKQhn0n+SkmMzdlbLVxZetZtFGgNlGa+WiVlR/jn6pJY2riHC8q0RDqa9+naU6Q9/k65pwGrd5pIL3PN24MCRIcUlvCawinq89KcHSU0G9peIoFk0RdoNDBjtXPOvz8DsBASkUVqGAjjeIHOAgnsare1915nJttARcLUD1kK0MlVDa07OJHL1y5nwEPfdR8ggRyZrnzbxoTd4vrqz+3b+JSWBIrMzB+A==~3552048~3617606; _abck=DDC3EF766C916643DD1CF57834504196~0~YAAQCxzFF9i5xwGcAQAALHSMCA9anYbJMlu8suGdOwJI5Nt8tKsAig2i3p+CZkPA82rB28qLut5js1fmasYvV0t8XGpFQCYNKLhA/Yf1/HXt/hiIsgTCQG1iHOqQggC7KUuz5Io30CGAb8f6Z+421cIjgXhYb3pGhVgS0fBw0BxBCYXpeHnmXDdtpJwQgwxPAXrMcCCDSXSL+S4/biTcKmrlqwRyrTs43COyItiPrB7wU7ezt832Mr5aaJDqgpNwsILzHpIeD6rhKp+zkGVikZEmSGkppwGymA2cXsGr8AkuxipyO2nOijQhHqfUDZlE3nm7U1Sjs5TtGYziXDEHYhREC7Ct5kgw5D0ddA5qTpza6uWm2aq8D+TAzh3401EI1bD4owwW+Rfeh+JOaRv75x5Nthtz36YoWH2D4FChAJJG/SxfzuHQmjnTJxwTq6AP4dEZgmDqcIw1pwfW0mEJtRJM6aij6Nb/Iu1cjGr7thr8XCyT+NSkH23s8QEySzfYxUDc6cNBRN/SBLRxpW/htS4XmD4Cz0mNl0++n7Rohi/K/ZxT9AfcOLIldwlQfwQB16Gk8Kq2QmASUoEa81tRDcrE77UKhJMWBDKg/mYg8+Azpr3tdeRNhNs2c2aceohCoTBegfzJztBIld45ujpkLYQBqPz84vV3QJr45SQhmSM120fEzcf+6z6boH7SjcbgpKd2gFWebuqZ+bg7UD27oslNLpIHh3OosUbQcwzXuR4LVYxyqrMl7L4QdPl20plu5aES0TFteuQph02mmN2EQUIJnOm2SMckonMANErmBy5gqdqhOrutNLhkB6n+3w/R7uOzhGHURcVhCL/ibiMoZskl6K25CYdkMDcoU0u0IZaKPXty6PJmHDEb4yr9vsuo20iVsQqBqll3aw==~-1~-1~-1~AAQAAAAF%2f%2f%2f%2f%2f3TONW8+VGBlbgAonU1dM23pwx4OXkpqQfgz9tlhaCEdomy4QUn4S6d9+UeYU%2fUZKianU9abDwQE7yyujE4i6rIppYg+7VHIVNO4tkXf8RrN9EdVL8EMGk8yVlwvJmrLc9E%2fXPg%3d~-1; OptanonConsent=isGpcEnabled=0&datestamp=Thu+Jan+29+2026+12%3A29%3A08+GMT%2B0530+(India+Standard+Time)&version=202510.2.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=3f86b333-267e-421a-bcc5-c118907ba734&interactionCount=1&isAnonUser=1&landingPath=NotLandingPage&groups=C0001%3A1%2CC0002%3A0%2CC0003%3A0%2CC0004%3A0%2CC0007%3A0&intType=2&geolocation=IN%3BGJ&AwaitingReconsent=false; bm_sv=23DAC3BB62FB03DFA0E53042FA28A8EB~YAAQCxzFF33OxwGcAQAAcrOMCB52YZfzq9HJqgPucg0PWwzHhcmWCDk28p5+kVMO2LqW/G6cbWNHa4ed99H2TT0Iua+tRzyir//FJXKgRwnqZ/V5DCWhgmQ+xTWgPEZ8sEOobjGAa66CQj1fEoH1yqU3rWoOb2XZtFEJHOgE8sT+vCfzjywm1/MucZSanCK15MYMnH77U6c0qUDs466c/ExXah550cmKtDjFAgc8lYRVJM7dqQxcZAlzuYuYx6PlV4w5il2q3g==~1; RT="sl=6&ss=1769669385216&tt=30104&obo=0&sh=1769669946941%3D6%3A0%3A30104%2C1769669911708%3D5%3A0%3A26167%2C1769669899345%3D4%3A0%3A18327%2C1769669889600%3D3%3A0%3A14472%2C1769669745440%3D2%3A0%3A6243&dm=jet2holidays.com&si=82vmdkk4zj6&rl=1&ld=1769669946941&r=https%3A%2F%2Fwww.jet2holidays.com%2Fbeach%2Fgreece%2Fcorfu%2Fglyfada%2Fdomes-of-corfu-autograph-collection%2Foptions%3Fd66f8bc00412cf59e32972f7893f73a3&ul=1769670147236"',
                }

                booard_response = requests.get(
                    f'https://www.jet2holidays.com/beach/greece/corfu/{main_result}/options',
                    params=params,
                    cookies=cookies,
                    headers=headers,
                )
                if booard_response.status_code == 200:
                    main_selec = Selector(booard_response.text)

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
                            'date': f'{formatted_date}T00:00:00.0000000Z',
                            'occupancy': 'r2c',
                            'boardId': board_id,
                            'inBoundFlightId': in_flight_code,
                            'outBoundFlightId': out_flight_code,
                            'rooms': [
                                room_id,
                            ],
                            'duration': 7,
                            'propertyId': hotel_id,
                            'earliestDepartureDate': f'{formatted_date}',
                            'latestDepartureDate': f'{check_outs_date}',
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
                            'referer': f'https://www.jet2holidays.com/beach/{country}/{destination}/{main_result}/options?duration=7&airport=7&date=06-04-2026&occupancy=r2c&board=2&iflight={in_flight_code}&oflight={out_flight_code}&rooms={room_id}&gtmsearchtype=Beach%20Search%20Results',
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
                            main_price_data = main_response.json()

                            # Make filename Windows-safe



                            holiday_price = main_price_data.get("holidayData").get("basketSummary")
                            if holiday_price:
                                per_person_price = holiday_price.get("perPersonPrice")
                                main_t_price = holiday_price.get("basePrice")
                                print(per_person_price)
                                print(room_name)
                                print(board_name)
                                print(per_person_price)

                                base_main_list = {
                                    "Crawled Date": scraped_date,
                                    # "List page url":"https://www.jet2holidays.com/beach/greece/corfu?airport=7&date=06-04-2026&duration=7&occupancy=r2c&sortorder=5&page=1",
                                    # "Hotel url": f"https://www.jet2holidays.com{hotel_url}",
                                    "Website": "Jet2Holidays",
                                    "Check-In Date": in_dates,
                                    "Check-Out Date": out_dates,
                                    "Nights": night,
                                    "Pax": "2",
                                    "Destination type":"city",
                                    "Website Hotel Name": hotel_name,
                                    "Website Hotel ID": hotel_id,
                                    "Matched Hotel Name": "",
                                    "Matched Hotel ID": "",
                                    "Website Rating": website_rating,
                                    # "Tripadvisor Rating": Rating,
                                    # "Tripadvisor Reviews": ReviewCount,
                                    "City": city,
                                    "Country": country,
                                    "Source Market": sorce_market,
                                    "Room Name": room_name,
                                    "Board Type": board_name,
                                    # "Per Person Price": per_person_price,
                                    "Total Price": main_t_price,
                                    "Currency": "GBP",
                                    "Flight Status": "Direct",
                                    "Departure Airport": departure_airport,
                                    "Arrival Airport": arrival_airport,
                                    "Out Airline": "Jet2Airways",
                                    "Out Flight code": out_flight_code,
                                    "Out Depart Date": our_depart_date,
                                    "Out Arr Date": our_arr_date,
                                    "In Airline": "Jet2Airways",
                                    "In Flight code": in_flight_code,
                                    "In Depart Date": in_depart_time,
                                    "In Arr Date": in_arr_date,
                                    "Baggage": luggage,
                                    "Transfer": transfer,
                                }

                                print(hotel_name, "/////", match_hotel_name)
                                try:
                                    if match_hotel_name == hotel_name:
                                        json_file = os.path.join(base_path, f"{match_hotel_name}.json")
                                        try:
                                            if not os.path.exists(json_file):  # 🔒 prevent overwrite

                                                # Save JSON
                                                with open(json_file, "w", encoding="utf-8") as f:
                                                    json.dump(main_data, f, ensure_ascii=False, indent=4)
                                        except Exception as e:
                                            print(e)
                                        main_file = os.path.join(base_path, f"{match_hotel_name}_board.html")
                                        if not os.path.exists(main_file):  # 🔒 prevent overwrite

                                            # Save JSON
                                            with open(main_file, "w", encoding="utf-8") as f:
                                                f.write(booard_response.text)
                                        safe_name = re.sub(r'[<>:"/\\|?*]', '_', match_hotel_name)

                                        # ✅ File path = base_path + filename (ONLY ONCE)
                                        price_file = os.path.join(
                                            base_path,
                                            f"{safe_name}_price.json"
                                        )

                                        # Ensure base_path exists
                                        os.makedirs(base_path, exist_ok=True)

                                        if not os.path.exists(price_file):  # 🔒 prevent overwrite
                                            with open(price_file, "w", encoding="utf-8") as f:
                                                json.dump(main_price_data, f, ensure_ascii=False, indent=4)

                                            print("Price page saved once")
                                        # insert only if this board type for this hotel/room/checkin does not exist
                                        product_data.insert_one(base_main_list)

                                    else:
                                        print("Hotel name not matched, skipping")

                                except Exception as e:
                                    print(e)
if __name__ == "__main__":
    with ThreadPoolExecutor(max_workers=1) as executor:
        docs = list(search_data.find({"Status": "Pending"}))
        executor.map(process_doc, docs)

