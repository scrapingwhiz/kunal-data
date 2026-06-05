import requests

cookies = {
    'x-viator-tapersistentcookie': '7b10bcc7-13c9-4565-89f6-c901e4950144',
    'SEM_PARAMS': '%7B%7D',
    'SEM_MCID': '42861',
    'EXTERNAL_SESSION_ID': '',
    'LAST_TOUCH_SEM_MCID': '42861',
    'XSRF-TOKEN': '99586cb1-59ec-4f1f-a831-44eb9cd22e42',
    'orion_first_touch_logged_in': 'false',
    'profilingBeaconSession': 'uTrJv7kQWGEq8poSDQMdCw%253D%253D%257CThceVsu2%252B4vuwz3N51pP7AV9JJHUFsA2E7ilPcTFB37YrgsxtHSeR2eSHhWm2UBPsRIGxew1lIk%253D%257CPcOOcWmO%252FnE%253D%253AO9%252Bwd7qdxyjLMmFt2RZoYO%252FbUxKzSW4Tdc4PAoxojX0%253D',
    '_bcnctkn': 'ae8d45970e2c8adbc57713476fc7b8e9edc5',
    'OptanonAlertBoxClosed': '2026-05-22T07:04:52.423Z',
    'ORION_SESSION': 'MgTChTzRVwWfHMjnT%2FLPFA%3D%3D%7Cju9xxBfdUdrRHXS9Laa%2FOVD2rNlstqybyvbhEzX%2B79paGdQNf9pKKdB%2BBg6QZs0E2bMwT%2F78as4nn3fl58%2BIC9N7QfNqOT%2Bn77oVACQqJquh%2Bpd0MBuyhj3CfghgkigsgaVjmy1HLuq2qZ5JsP5PV4TpLMgycRlwGptuRpnS%2BB6ISaFR7ohDuZfkPeHVmSGTKdvKpu2Tp0OZvvq4xb0kje8HZV%2Fxn2cwQflRtZznwfg31QHVRbr9ZJHQdzy1AFmQpNM6WNbD0DKmEb6czdLgD%2FeqAO3bXBP881snurhtiLczOiXlggZqZSslKC9oe%2B8%2B%2B5g8a6HVGBpykvIqZVFmrTZmOJykxeBy0tvPp2hbH3VMMKCDrvRY%2F%2BwkOaoKsGmpBksrBwCkDsz61KIGMEvY2I28rdlUtDwIZ3DzNZuXW%2BhGCrllDr3sjS0x7K0Mz5LN2nTLbjBEBO3VB3wjucfCT4DrsTgEV948YTP%2F1pbuvydjpmQSgIPywT2rbvgKWWwWqs7oe7m7dRgpmfAL4DGOyY0EtCuGM5w68XDjKGpOp1zW8iZXtoSQVv4J1slUQh1ISsOS9BRgXHtYzehqQCaH9x4wSC2cMRmCcy%2FRtqLE8HXG%2B9XplmszthGDSX%2F4aZzDcMRYoOiPVq%2BAMBXzKvg8EB%2BTbNTUTgUs%2BoDtr4VmfAFH6cDIFZMqTL2RhoIMPkdOSh%2BE%2B4krumyS96k4CO7EvRVcPEJATOhwJ49rfACyoDga9LhQPrRhhqTlZE9NaDRhhLaWKvYGBKqP4cUFG0L1Daxb%2FPjJEHB8s6q5ORSApLcr6r4x%2Bh3l6nnhs9nm6ySsi2ggsMaJD5XgsGL7gSizqMwAG75ulbCQS9VW%2BXeX2NRftlg6OtXK99DgZO7BZ7V58p7u2Um60rIQraYe1hDJP487TxpL5bp3RO5jmpOidU%2BzCfheCDJeDa2J1PBAQ1qfTAWf%2BgAoX5iGgepgLq%2F8vz8Jb1Fp2FhFqZ12KK%2FnjnQDW5MLecAv7YB3phtdH38QnnB%2Br%2Fm3eYDDjxTjXYj%2Ftbtow3ECEimq83J2ClTgJ3nx8Z7dqUQ2emy649S4xZ2CxvBpJ3YI3YL8ftZ6OLikcfUcV8CLWilGlZsFHGfTXjCmICJ4cKzaWKhM%2BkqbDxIeVTMKxFhkTnYUtI9E%2FfFMsSIVSNd%2BdFX7eSNjLk4Qpf%2B0L7MH49JIXNq526gv2e4Sc7RA2MVEzPBGqC0bMIlLe61ieC37WEaU78uE0vLr0R0K2f%2BUZhF%2B8OXf%2BfgHgAijq3edjob1IFrVFzsXgNqEbLemZ%2BRw0n0XA1AGVlfj9cy%2B2R8DXkdg4qyshu8jAZ9RUqTC5EugljAhcS2xPBiP6HL5klayHaTWQ9szGt6xKXhHd3wkqlyJ%2FS6tlxyWW1ulySR0Tr%2FkaoAYtVl%2FYOQTzlrf%2Ft1OpimyTLLBME%2BiDslg08JbluX8cE75fmLE%2F1HMxEA2z7oet9or3K2%2FxSg5N2g0Fc7LOfZsXf8%2FTR%2FPXjAFuK%2FD6C7L7NQ4qeWIa6SLoBOPURDPzy9hQI67WcFGoyWEOTrcIfOj%2BWRg58U6dDyIRYnQD63OBt7MQXyVUXV%2BfC3pwD7Ai0k73lLi4ynPEhtXNUxxlv3T60BRx6i6GOgXvXEXsYcSPtoWpEfBVa5A7%2FRZeClfGpt2V7K7TjsKx6JPxuKWv%2FER5l%2FDWP1RBF0GWMecZCl0qIRXbYazx74Dz3Dtkt0d21%2Bp5PtqU7STZfGjK16C6hkKeGZfMjdeCAZYXlhEuqMIe9B4vByNAFEWFJ%2Fq4IA6E%2FKRbvN9JkX%2Foh1RxBr6F%2FvhDmLU7bskT2fSP5jYbjdb5zf0x5MO2HCsqgWNsogX8Dd4aCgk9KB5%2BjRUyYgC%2BFgYC7Cy4%2Bs6c1Jr%2FG2%2FU64z%2FmoCnSLgSQDQWpm9tR1ceKYxa%2BYId3lRSLhan4TVJMhIVpE5LbJwUx3jUPzlPGJl%2FrxizocuhTCdvuwl5pMg4YA%2BueDC0o4JHfV6lP4SjAT0GC3GWqzLpes0K%2BSSOamdKgIpc833YioiJzjptx9xUWIRI62Tb3mIVs1P5%2BcgcqCUaodo%2BuHZphvvXqr%2FRLwEJ2iCy9IpqPxg7xmac5EdvSt5y0vzc0epmtquI%2F%2FALI9H55pFt9MsEtHZ6b%2F1V8pBMmml%2FhjtUsmI2MbJM6hCRrYvupGqx%2B%2BxJz%2BKygxFKRxByZhEwfn8s6HAPhMrDl73bCIzEbAXQHN%2F9nBLZvLe6mQkcdg6UTyLNRH857cAvbN3uJv4LOF6zpcksfEQ9c8n6%2BV8ApjgJwriu3NFPVLOTJvg4g9TlrfUz%2BwQ8hAy6oSd5B%2FK%7ChcMMVs6pqTA%3D%3APsJr1PbNt2XsLzm7Hz5iTIYwTh0WDrRpKz3Z14dr%2F%2Bc%3D',
    'REFERER_PAGE_REQUEST_ID': 'A752EB1D:9DA6_0A280F01:01BB_6A100011_40DF6C1:824CF',
    'g_state': '{"i_l":0,"i_ll":1779433494540,"i_b":"im4cbwfQPlSpPRcYBfg+AfBzgoD8hw7b+IdJJ4Q14bU","i_e":{"enable_itp_optimization":0},"i_et":1779392812535}',
    'OptanonConsent': 'isGpcEnabled=0&datestamp=Fri+May+22+2026+12%3A34%3A54+GMT%2B0530+(India+Standard+Time)&version=202601.2.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=cdc4fbf4-d6e3-457b-9d0d-a6c3d2e128b7&interactionCount=1&isAnonUser=1&prevHadToken=0&landingPath=NotLandingPage&groups=C0001%3A1%2CC0003%3A1%2CC0004%3A1%2CC0002%3A1&AwaitingReconsent=false&intType=1&geolocation=%3B',
    'ORION_SESSION_REQ': 'A752EB1D%3AC60C_0A2809E5%3A01BB_6A100017_404F11F%3A73CDF%7CA752EB1D%3A9DA6_0A280F01%3A01BB_6A100011_40DF6C1%3A824CF%7CA752EB1D%3A9DA6_0A280F01%3A01BB_6A100011_40DF6C1%3A824CF',
    'profilingInAuthSession': 'TLqnw00Swy3Fb%252BGH92DC7g%253D%253D%257CMZFC%252FLHjm3Tlqd4%252FFv21TU27lav6MbRjbUywCNGQ5xmRBnCSF5cVyAcHU4x%252BieHopceERl45nMigllZdYSYPahe9Px5N0UxyIu3V%252Fjy6lJpFcA%253D%253D%257CjpOMimeMybM%253D%253AiYgm%252Bxbls27ziI7NZ%252BfyU78CL3WazmEtTJmZ8n9HyLw%253D',
    'datadome': 'cp2X9zJ0FD4kKa~7nIEEH5QpIftrG9vRQR65kyXCNrfdqgRUzDH6Q1ytLZSXhwVs3E5L89KqnHxIDokS1jMcIwYt55hcA6wMApI_paeyk97PN7PmGWmJ1Mj2eydRhx~l',
}

headers = {
    'accept': 'application/json, text/plain, */*',
    'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8,hi;q=0.7',
    'content-type': 'application/json',
    'origin': 'https://www.viator.com',
    'priority': 'u=1, i',
    'referer': 'https://www.viator.com/tours/Reykjavik/Northern-Lights-Tour-from-Reykjavik/d905-24308P13?dd_referrer=',
    'sec-ch-ua': '"Chromium";v="148", "Google Chrome";v="148", "Not/A)Brand";v="99"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-ch-ua-platform-version': '"15.0.0"',
    'sec-ch-viewport-width': '1920',
    'sec-fetch-dest': 'empty',
    'sec-fetch-mode': 'cors',
    'sec-fetch-site': 'same-origin',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/148.0.0.0 Safari/537.36',
    'x-requested-with': 'XMLHttpRequest',
    'x-xsrf-token': '99586cb1-59ec-4f1f-a831-44eb9cd22e42',
    # 'cookie': 'x-viator-tapersistentcookie=7b10bcc7-13c9-4565-89f6-c901e4950144; SEM_PARAMS=%7B%7D; SEM_MCID=42861; EXTERNAL_SESSION_ID=; LAST_TOUCH_SEM_MCID=42861; XSRF-TOKEN=99586cb1-59ec-4f1f-a831-44eb9cd22e42; orion_first_touch_logged_in=false; profilingBeaconSession=uTrJv7kQWGEq8poSDQMdCw%253D%253D%257CThceVsu2%252B4vuwz3N51pP7AV9JJHUFsA2E7ilPcTFB37YrgsxtHSeR2eSHhWm2UBPsRIGxew1lIk%253D%257CPcOOcWmO%252FnE%253D%253AO9%252Bwd7qdxyjLMmFt2RZoYO%252FbUxKzSW4Tdc4PAoxojX0%253D; _bcnctkn=ae8d45970e2c8adbc57713476fc7b8e9edc5; OptanonAlertBoxClosed=2026-05-22T07:04:52.423Z; ORION_SESSION=MgTChTzRVwWfHMjnT%2FLPFA%3D%3D%7Cju9xxBfdUdrRHXS9Laa%2FOVD2rNlstqybyvbhEzX%2B79paGdQNf9pKKdB%2BBg6QZs0E2bMwT%2F78as4nn3fl58%2BIC9N7QfNqOT%2Bn77oVACQqJquh%2Bpd0MBuyhj3CfghgkigsgaVjmy1HLuq2qZ5JsP5PV4TpLMgycRlwGptuRpnS%2BB6ISaFR7ohDuZfkPeHVmSGTKdvKpu2Tp0OZvvq4xb0kje8HZV%2Fxn2cwQflRtZznwfg31QHVRbr9ZJHQdzy1AFmQpNM6WNbD0DKmEb6czdLgD%2FeqAO3bXBP881snurhtiLczOiXlggZqZSslKC9oe%2B8%2B%2B5g8a6HVGBpykvIqZVFmrTZmOJykxeBy0tvPp2hbH3VMMKCDrvRY%2F%2BwkOaoKsGmpBksrBwCkDsz61KIGMEvY2I28rdlUtDwIZ3DzNZuXW%2BhGCrllDr3sjS0x7K0Mz5LN2nTLbjBEBO3VB3wjucfCT4DrsTgEV948YTP%2F1pbuvydjpmQSgIPywT2rbvgKWWwWqs7oe7m7dRgpmfAL4DGOyY0EtCuGM5w68XDjKGpOp1zW8iZXtoSQVv4J1slUQh1ISsOS9BRgXHtYzehqQCaH9x4wSC2cMRmCcy%2FRtqLE8HXG%2B9XplmszthGDSX%2F4aZzDcMRYoOiPVq%2BAMBXzKvg8EB%2BTbNTUTgUs%2BoDtr4VmfAFH6cDIFZMqTL2RhoIMPkdOSh%2BE%2B4krumyS96k4CO7EvRVcPEJATOhwJ49rfACyoDga9LhQPrRhhqTlZE9NaDRhhLaWKvYGBKqP4cUFG0L1Daxb%2FPjJEHB8s6q5ORSApLcr6r4x%2Bh3l6nnhs9nm6ySsi2ggsMaJD5XgsGL7gSizqMwAG75ulbCQS9VW%2BXeX2NRftlg6OtXK99DgZO7BZ7V58p7u2Um60rIQraYe1hDJP487TxpL5bp3RO5jmpOidU%2BzCfheCDJeDa2J1PBAQ1qfTAWf%2BgAoX5iGgepgLq%2F8vz8Jb1Fp2FhFqZ12KK%2FnjnQDW5MLecAv7YB3phtdH38QnnB%2Br%2Fm3eYDDjxTjXYj%2Ftbtow3ECEimq83J2ClTgJ3nx8Z7dqUQ2emy649S4xZ2CxvBpJ3YI3YL8ftZ6OLikcfUcV8CLWilGlZsFHGfTXjCmICJ4cKzaWKhM%2BkqbDxIeVTMKxFhkTnYUtI9E%2FfFMsSIVSNd%2BdFX7eSNjLk4Qpf%2B0L7MH49JIXNq526gv2e4Sc7RA2MVEzPBGqC0bMIlLe61ieC37WEaU78uE0vLr0R0K2f%2BUZhF%2B8OXf%2BfgHgAijq3edjob1IFrVFzsXgNqEbLemZ%2BRw0n0XA1AGVlfj9cy%2B2R8DXkdg4qyshu8jAZ9RUqTC5EugljAhcS2xPBiP6HL5klayHaTWQ9szGt6xKXhHd3wkqlyJ%2FS6tlxyWW1ulySR0Tr%2FkaoAYtVl%2FYOQTzlrf%2Ft1OpimyTLLBME%2BiDslg08JbluX8cE75fmLE%2F1HMxEA2z7oet9or3K2%2FxSg5N2g0Fc7LOfZsXf8%2FTR%2FPXjAFuK%2FD6C7L7NQ4qeWIa6SLoBOPURDPzy9hQI67WcFGoyWEOTrcIfOj%2BWRg58U6dDyIRYnQD63OBt7MQXyVUXV%2BfC3pwD7Ai0k73lLi4ynPEhtXNUxxlv3T60BRx6i6GOgXvXEXsYcSPtoWpEfBVa5A7%2FRZeClfGpt2V7K7TjsKx6JPxuKWv%2FER5l%2FDWP1RBF0GWMecZCl0qIRXbYazx74Dz3Dtkt0d21%2Bp5PtqU7STZfGjK16C6hkKeGZfMjdeCAZYXlhEuqMIe9B4vByNAFEWFJ%2Fq4IA6E%2FKRbvN9JkX%2Foh1RxBr6F%2FvhDmLU7bskT2fSP5jYbjdb5zf0x5MO2HCsqgWNsogX8Dd4aCgk9KB5%2BjRUyYgC%2BFgYC7Cy4%2Bs6c1Jr%2FG2%2FU64z%2FmoCnSLgSQDQWpm9tR1ceKYxa%2BYId3lRSLhan4TVJMhIVpE5LbJwUx3jUPzlPGJl%2FrxizocuhTCdvuwl5pMg4YA%2BueDC0o4JHfV6lP4SjAT0GC3GWqzLpes0K%2BSSOamdKgIpc833YioiJzjptx9xUWIRI62Tb3mIVs1P5%2BcgcqCUaodo%2BuHZphvvXqr%2FRLwEJ2iCy9IpqPxg7xmac5EdvSt5y0vzc0epmtquI%2F%2FALI9H55pFt9MsEtHZ6b%2F1V8pBMmml%2FhjtUsmI2MbJM6hCRrYvupGqx%2B%2BxJz%2BKygxFKRxByZhEwfn8s6HAPhMrDl73bCIzEbAXQHN%2F9nBLZvLe6mQkcdg6UTyLNRH857cAvbN3uJv4LOF6zpcksfEQ9c8n6%2BV8ApjgJwriu3NFPVLOTJvg4g9TlrfUz%2BwQ8hAy6oSd5B%2FK%7ChcMMVs6pqTA%3D%3APsJr1PbNt2XsLzm7Hz5iTIYwTh0WDrRpKz3Z14dr%2F%2Bc%3D; REFERER_PAGE_REQUEST_ID=A752EB1D:9DA6_0A280F01:01BB_6A100011_40DF6C1:824CF; g_state={"i_l":0,"i_ll":1779433494540,"i_b":"im4cbwfQPlSpPRcYBfg+AfBzgoD8hw7b+IdJJ4Q14bU","i_e":{"enable_itp_optimization":0},"i_et":1779392812535}; OptanonConsent=isGpcEnabled=0&datestamp=Fri+May+22+2026+12%3A34%3A54+GMT%2B0530+(India+Standard+Time)&version=202601.2.0&browserGpcFlag=0&isIABGlobal=false&hosts=&consentId=cdc4fbf4-d6e3-457b-9d0d-a6c3d2e128b7&interactionCount=1&isAnonUser=1&prevHadToken=0&landingPath=NotLandingPage&groups=C0001%3A1%2CC0003%3A1%2CC0004%3A1%2CC0002%3A1&AwaitingReconsent=false&intType=1&geolocation=%3B; ORION_SESSION_REQ=A752EB1D%3AC60C_0A2809E5%3A01BB_6A100017_404F11F%3A73CDF%7CA752EB1D%3A9DA6_0A280F01%3A01BB_6A100011_40DF6C1%3A824CF%7CA752EB1D%3A9DA6_0A280F01%3A01BB_6A100011_40DF6C1%3A824CF; profilingInAuthSession=TLqnw00Swy3Fb%252BGH92DC7g%253D%253D%257CMZFC%252FLHjm3Tlqd4%252FFv21TU27lav6MbRjbUywCNGQ5xmRBnCSF5cVyAcHU4x%252BieHopceERl45nMigllZdYSYPahe9Px5N0UxyIu3V%252Fjy6lJpFcA%253D%253D%257CjpOMimeMybM%253D%253AiYgm%252Bxbls27ziI7NZ%252BfyU78CL3WazmEtTJmZ8n9HyLw%253D; datadome=cp2X9zJ0FD4kKa~7nIEEH5QpIftrG9vRQR65kyXCNrfdqgRUzDH6Q1ytLZSXhwVs3E5L89KqnHxIDokS1jMcIwYt55hcA6wMApI_paeyk97PN7PmGWmJ1Mj2eydRhx~l',
}

json_data = {
    'productCode': '24308P13',
    'searchDate': '2026-09-18',
    'ageBands': {
        'ADULT': '2',
    },
}
proxies = {
    "http": "http://103.152.112.145:80",
    "https": "http://103.152.112.145:80",
}
response = requests.post(
    'https://www.viator.com/orion/ajax/product-availability',
    cookies=cookies,
    headers=headers,
    json=json_data,
    # proxies=proxies
)

print(response.status_code)