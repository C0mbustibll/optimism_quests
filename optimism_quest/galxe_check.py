import aiohttp
from loguru import logger
import asyncio
import random

class Galxe():

    @staticmethod
    async def verify_task(ID_TASK,ADDRESS):

        headers = {
            'authority': 'graphigo.prd.galaxy.eco',
            'accept': '*/*',
            'accept-language': 'en-GB,en;q=0.9',
            'user-agent': 'Mozilla/5.0 (Windows NT 6.2; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/101.0.4951.54 Safari/537.36',
            'content-type': 'application/json',

        }

        json_data = {
            'operationName': 'VerifyCredential',
            'variables': {
                'input': {
                    'credId': ID_TASK,
                    'address': ADDRESS,
                },
            },
            'query': 'mutation VerifyCredential($input: VerifyCredentialInput) {\n  verifyCredential(input: $input)\n}\n',
        }

        rep = 0

        while True:
            try:
                async with aiohttp.ClientSession() as ses:
                    async with ses.post('https://graphigo.prd.galaxy.eco/query', headers=headers, json=json_data) as r:
                        data = await r.json()
                        if data.get('errors'):
                            return True
                        elif data['data']['verifyCredential']:
                            return False
                        else:
                            logger.error(f'{ADDRESS} {data}')
                            return False
            except Exception as e:
                rep+= 1
                if rep >=15:
                    logger.error(f'{ADDRESS} | {e}')
                    return
                await asyncio.sleep(random.randint(11,21))
'''
Error response 
 {'errors': [{'message': '1004:If you have fulfilled the requirement, please try 30 seconds later.', 
 'path': ['verifyCredential'], 'extensions': {'code': 'Unknown'}}], 'data': None}
 
Suc response 
{'data': {'verifyCredential': True}}
'''
