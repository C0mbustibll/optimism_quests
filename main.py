import random
from loguru import logger
import asyncio
import time
import os
from sys import stderr
import json
from web3 import Web3
from web3.eth import AsyncEth
import datetime

from optimism_quest import \
    work_pooltog, \
    work_pika, \
    work_beth, \
    work_perp, \
    work_polynomial, \
    work_velodrome, \
    work_synapse, \
    work_uniswap, \
    work_rubicon, \
    work_granary, \
    Galxe

from config import GWEI_MAX, RPC_ETH, RPC_OPTIMISM


def stat_quest(key, *ar):
    # print(ar)
    ADDRESS = web3.eth.account.from_key(key).address
    good = '✅'
    bad = '❌'

    st = [betho, perpet, granar, syna, rubico, velo, uni, pik, pool, poly] = [bad] * 10
    for v, arg in enumerate(range(len(st))):
        if ar[v]:
            st[v] = good

    logger.debug(f'\n{"*" * 10}{ADDRESS}{"*" * 10}\n'
                 f'1)BETHOVEN {st[0]}\n'
                 f'2)PERP {st[1]}\n'
                 f'3)GRANARY {st[2]}\n'
                 f'4)SYNCAPSE {st[3]}\n'
                 f'5)RUBICON {st[4]}\n'
                 f'6)VELODROME {st[5]}\n'
                 f'7)UNI {st[6]}\n'
                 f'8)PIKA {st[7]}\n'
                 f'9)POOLTOGETHER {st[8]}\n'
                 f'10)POLYNOMIAL {st[9]}\n'
                 f'{"*" * (len(ADDRESS) + 20)}')


def message(TASK, ADDRESS, STATUS=1):
    if STATUS == 0:
        return f'{TASK} | Success | {ADDRESS}'
    else:
        return f'{TASK} | False   | {ADDRESS}'


async def i_dont_know_what_to_call_it(key, FN, NAME: str, TASK_ID: str):
    ADDRESS = web3.eth.account.from_key(key).address

    if await gal.verify_task(TASK_ID, ADDRESS):
        logger.info(f'{NAME} | START | {ADDRESS}')
        if await FN(key):
            logger.success(message(NAME, ADDRESS, 0))
            return True
        else:
            logger.error(message(NAME, ADDRESS))
            return False
    else:
        logger.success(message(NAME, ADDRESS, 0))
        return True


async def i_dont_know_what_to_call_it_plus_rule(key, FN, USLO, NAME: str, TASK_ID: str):
    ADDRESS = web3.eth.account.from_key(key).address
    verif = await gal.verify_task(TASK_ID, ADDRESS)

    if int(TASK_ID) == 195285392787415040 and USLO:
        verif =False

    if verif or not USLO:
        logger.info(f'{NAME} | START | {ADDRESS}')
        if await FN(key):
            logger.success(message(NAME, ADDRESS, 0))
            return True
        else:
            logger.error(message(NAME, ADDRESS))
            return False
    else:
        logger.success(message(NAME, ADDRESS, 0))
        return True


async def beth(key):
    ADDRESS = web3.eth.account.from_key(key).address
    bal_beth=0
    if await balance_token(ADDRESS,'0x38f79beffc211c6c439b0a3d10a0a673ee63afb4') or await balance_token(ADDRESS,'0x4fd63966879300cafafbb35d157dc5229278ed23'):
        bal_beth = 1
    if bal_beth >0:
        bal_beth = False
    else:
        bal_beth = True
    stat = await i_dont_know_what_to_call_it_plus_rule(key, work_beth,bal_beth, 'BEETHOVEN', '193977443855015936')
    return stat


async def perp(key):
    stat = await i_dont_know_what_to_call_it(key, work_perp, 'PERP', '194475434890141696')
    return stat


async def granary(key):
    ADDRESS = web3.eth.account.from_key(key).address
    USLO = await balance_token(ADDRESS,'0x7a0fddba78ff45d353b1630b77f4d175a00df0c0') == 0
    stat = await i_dont_know_what_to_call_it_plus_rule(key, work_granary,USLO, 'GRANARY', '193030300969377792')
    return stat


async def synapse(key):
    stat = await i_dont_know_what_to_call_it(key, work_synapse, 'SYNAPSE', '196921351161421824')
    return stat


async def rubicon(key):
    stat = await i_dont_know_what_to_call_it(key, work_rubicon, 'RUBICON', '195455153575993344')
    return stat


async def velodrome(key):
    ADDRESS = web3.eth.account.from_key(key).address
    USLOVIE = await balance_token(ADDRESS, '0xe2cec8ab811b648ba7b1691ce08d5e800dd0a60a') == 0 and await balance_token(ADDRESS, '0x79c912FEF520be002c2B6e57EC4324e260f38E50') ==0
    stat = await i_dont_know_what_to_call_it_plus_rule(key, work_velodrome,USLOVIE, 'VELODROME', '193664347672322048')
    return stat


async def uniswap(key):
    stat = await i_dont_know_what_to_call_it(key, work_uniswap, 'UNISWAP', '193974798914330624')
    return stat


async def pika(key):
    stat = await i_dont_know_what_to_call_it(key, work_pika, 'PIKA', '193031912735547392')
    return stat


async def together(key):
    ADDRESS = web3.eth.account.from_key(key).address
    USDLOVIE = await balance_token(ADDRESS, '0x62bb4fc73094c83b5e952c2180b23fa7054954c4')
    if USDLOVIE > 0:
        USDLOVIE = True
    else:
        USDLOVIE = False
    stat = await i_dont_know_what_to_call_it_plus_rule(key, work_pooltog, USDLOVIE, 'TOGETHER', '195285392787415040')
    return stat


async def polynomial(key):
    stat = await i_dont_know_what_to_call_it(key, work_polynomial, 'POLYNOMIAL', '187906803892920320')
    return stat


async def balance_token(address, token):
    return await web3.eth.contract(address=web3.toChecksumAddress(token),
                                   abi=json.loads(
                                       '[{"inputs":[{"internalType":"address","name":"_troveManagerAddress","type":"address"},{"internalType":"address","name":"_stabilityPoolManagerAddress","type":"address"},{"internalType":"address","name":"_borrowerOperationsAddress","type":"address"}],"stateMutability":"nonpayable","type":"constructor"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"owner","type":"address"},{"indexed":true,"internalType":"address","name":"spender","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Approval","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"_newBorrowerOperationsAddress","type":"address"}],"name":"BorrowerOperationsAddressChanged","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"_asset","type":"address"},{"indexed":false,"internalType":"bool","name":"state","type":"bool"}],"name":"EmergencyStopMintingCollateral","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"previousOwner","type":"address"},{"indexed":true,"internalType":"address","name":"newOwner","type":"address"}],"name":"OwnershipTransferred","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"_newStabilityPoolAddress","type":"address"}],"name":"StabilityPoolAddressChanged","type":"event"},{"anonymous":false,"inputs":[{"indexed":true,"internalType":"address","name":"from","type":"address"},{"indexed":true,"internalType":"address","name":"to","type":"address"},{"indexed":false,"internalType":"uint256","name":"value","type":"uint256"}],"name":"Transfer","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"_troveManagerAddress","type":"address"}],"name":"TroveManagerAddressChanged","type":"event"},{"anonymous":false,"inputs":[{"indexed":false,"internalType":"address","name":"_user","type":"address"},{"indexed":false,"internalType":"uint256","name":"_amount","type":"uint256"}],"name":"VSTTokenBalanceUpdated","type":"event"},{"inputs":[],"name":"DOMAIN_SEPARATOR","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"PERMIT_TYPEHASH","outputs":[{"internalType":"bytes32","name":"","type":"bytes32"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"spender","type":"address"}],"name":"allowance","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"approve","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"account","type":"address"}],"name":"balanceOf","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"borrowerOperationsAddress","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"_account","type":"address"},{"internalType":"uint256","name":"_amount","type":"uint256"}],"name":"burn","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"chainId","outputs":[{"internalType":"uint256","name":"chainID","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"decimals","outputs":[{"internalType":"uint8","name":"","type":"uint8"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"subtractedValue","type":"uint256"}],"name":"decreaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_asset","type":"address"},{"internalType":"bool","name":"status","type":"bool"}],"name":"emergencyStopMinting","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"","type":"address"}],"name":"emergencyStopMintingCollateral","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"addedValue","type":"uint256"}],"name":"increaseAllowance","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_asset","type":"address"},{"internalType":"address","name":"_account","type":"address"},{"internalType":"uint256","name":"_amount","type":"uint256"}],"name":"mint","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"name","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"}],"name":"nonces","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"owner","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"owner","type":"address"},{"internalType":"address","name":"spender","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"},{"internalType":"uint256","name":"deadline","type":"uint256"},{"internalType":"uint8","name":"v","type":"uint8"},{"internalType":"bytes32","name":"r","type":"bytes32"},{"internalType":"bytes32","name":"s","type":"bytes32"}],"name":"permit","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"renounceOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_poolAddress","type":"address"},{"internalType":"address","name":"_receiver","type":"address"},{"internalType":"uint256","name":"_amount","type":"uint256"}],"name":"returnFromPool","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"_sender","type":"address"},{"internalType":"address","name":"_poolAddress","type":"address"},{"internalType":"uint256","name":"_amount","type":"uint256"}],"name":"sendToPool","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"stabilityPoolManager","outputs":[{"internalType":"contract IStabilityPoolManager","name":"","type":"address"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"symbol","outputs":[{"internalType":"string","name":"","type":"string"}],"stateMutability":"view","type":"function"},{"inputs":[],"name":"totalSupply","outputs":[{"internalType":"uint256","name":"","type":"uint256"}],"stateMutability":"view","type":"function"},{"inputs":[{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transfer","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"sender","type":"address"},{"internalType":"address","name":"recipient","type":"address"},{"internalType":"uint256","name":"amount","type":"uint256"}],"name":"transferFrom","outputs":[{"internalType":"bool","name":"","type":"bool"}],"stateMutability":"nonpayable","type":"function"},{"inputs":[{"internalType":"address","name":"newOwner","type":"address"}],"name":"transferOwnership","outputs":[],"stateMutability":"nonpayable","type":"function"},{"inputs":[],"name":"troveManagerAddress","outputs":[{"internalType":"address","name":"","type":"address"}],"stateMutability":"view","type":"function"}]')
                                   ).functions.balanceOf(address).call()


async def gas_eth(key):
    ADDRESS = web3eth.eth.account.from_key(key).address
    while True:
        GAS = await web3eth.eth.gas_price
        if GAS > GWEI_MAX * 10 ** 9:
            logger.info(f'{ADDRESS} | Await normal gas {"{:.2f}".format(GAS / 10 ** 9)}/{GWEI_MAX} GWEI')
            await asyncio.sleep(60)
        else:
            return True


async def work(key):
    st1, st2, st3, st4, st5, st6, st7, st8, st9, st10 = [False] * 10

    if await gas_eth(key):
        st1 = await beth(key)
        await asyncio.sleep(4)

    if await gas_eth(key):
        st2 = await perp(key)
        await asyncio.sleep(4)

    if await gas_eth(key):
        st3 = await granary(key)
        await asyncio.sleep(4)

    if await gas_eth(key):
        st4 = await synapse(key)
        await asyncio.sleep(4)

    if await gas_eth(key):
        st5 = await rubicon(key)
        await asyncio.sleep(4)

    if await gas_eth(key):
        st6 = await velodrome(key)
        await asyncio.sleep(4)

    if await gas_eth(key):
        st7 = await uniswap(key)
        await asyncio.sleep(4)

    if await gas_eth(key):
        st8 = await pika(key)
        await asyncio.sleep(4)

    if await gas_eth(key):
        st9 = await together(key)
        await asyncio.sleep(4)

    if await gas_eth(key):
        st10 = await polynomial(key)
        await asyncio.sleep(4)

    stat_quest(key, st1, st2, st3, st4, st5, st6, st7, st8, st9, st10)


logger.remove()
logger.add(stderr,
           format="<white>{time:HH:mm:ss}</white> | "
                  "<level>{level: <2}</level> | "
                  "<white>{function}</white> - "
                  "<white>{message}</white>")

date = datetime.datetime.now().utcnow().strftime("%H_%M_%S")
logger.add(f"./log/file_{date}.log")

gal = Galxe()



web3 = Web3(Web3.AsyncHTTPProvider(RPC_OPTIMISM),
            modules={'eth': (AsyncEth,)}, middlewares=[])

web3eth = Web3(Web3.AsyncHTTPProvider(RPC_ETH),
               modules={'eth': (AsyncEth,)}, middlewares=[])

key_path = os.path.abspath('data_file/key.txt')
with open(key_path, 'r') as f:
    key_list = [k for k in [i.strip() for i in f] if k != '']

async def run():
    await asyncio.gather(*[work(k) for k in key_list])
