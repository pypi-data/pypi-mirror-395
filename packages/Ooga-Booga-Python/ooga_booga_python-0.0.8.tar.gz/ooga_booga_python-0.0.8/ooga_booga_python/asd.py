from ooga_booga_python.client import OogaBoogaClient
from ooga_booga_python.models import TransactionReceipt
import asyncio
from dotenv import load_dotenv
import os

from ooga_booga_python.models import SwapParams

# Load environment variables from the .env file
load_dotenv()

def check_success(receipt: TransactionReceipt):
    if receipt.success:
        print(f"Transaction succeeded! Hash: {receipt.transactionHash}")
        print(f"Gas used: {receipt.gasUsed}")
    else:
        print(f"Transaction failed on-chain. Hash: {receipt.transactionHash}")


async def approve_allowance(client: OogaBoogaClient):
    token = "0xFCBD14DC51f0A4d49d5E53C2E0950e0bC26d0Dce"
    approval_response = await client.approve_allowance(token)
    print(f"Approval transaction: {approval_response}")


async def perform_swap(client: OogaBoogaClient):
    wallet = "0x98A79CF6288B27b2aBED90C73E2F3106DC234f43"
    honey = "0xFCBD14DC51f0A4d49d5E53C2E0950e0bC26d0Dce"
    allowance = await client.get_token_allowance(wallet, honey)
    print(f"Allowance: {allowance}")
    swap_params = SwapParams(
        tokenIn=honey,
        amount=1000000000000000000,  # 1 token in wei
        tokenOut="0x549943e04f40284185054145c6E4e9568C1D3241",
        to=wallet,
        slippage=0.02,
    )
    receipt = await client.swap(swap_params)
    check_success(receipt)

async def perform_swap_bera(client: OogaBoogaClient):
    wallet = "0x98A79CF6288B27b2aBED90C73E2F3106DC234f43"
    bera = "0x0000000000000000000000000000000000000000"
    allowance = await client.get_token_allowance(wallet, bera)
    print(f"Allowance: {allowance}")
    swap_params = SwapParams(
        tokenIn=bera,
        amount=110000000000000000,  # 1 token in wei
        tokenOut="0x549943e04f40284185054145c6E4e9568C1D3241",
        to=wallet,
        slippage=0.02,
    )
    receipt = await client.swap(swap_params)
    check_success(receipt)



async def perform_swap_insufficient_balance(client: OogaBoogaClient):
    swap_params = SwapParams(
        tokenIn="0xFCBD14DC51f0A4d49d5E53C2E0950e0bC26d0Dce",
        amount=10000000000000000000000000,  # 10000 token in wei
        tokenOut="0x549943e04f40284185054145c6E4e9568C1D3241",
        to="0x98A79CF6288B27b2aBED90C73E2F3106DC234f43",
        slippage=1,
    )
    receipt = await client.swap(swap_params)
    check_success(receipt)

async def perfom_circular_swap(client: OogaBoogaClient):
    swap_params = SwapParams(
        tokenIn="0xFCBD14DC51f0A4d49d5E53C2E0950e0bC26d0Dce",
        amount=10000000000000000000000000,  # 1 token in wei
        tokenOut="0xFCBD14DC51f0A4d49d5E53C2E0950e0bC26d0Dce",
        to="0x98A79CF6288B27b2aBED90C73E2F3106DC234f43",
        slippage=1,
    )
    receipt = await client.swap(swap_params)
    check_success(receipt)


async def perform_swap_slippage_too_high(client: OogaBoogaClient):
    swap_params = SwapParams(
        tokenIn="0xFCBD14DC51f0A4d49d5E53C2E0950e0bC26d0Dce",
        amount=10000000000000000000000000,  # 10000 token in wei
        tokenOut="0x549943e04f40284185054145c6E4e9568C1D3241",
        to="0x98A79CF6288B27b2aBED90C73E2F3106DC234f43",
        slippage=2,
    )
    receipt = await client.swap(swap_params)
    check_success(receipt)


async def approve_allowance_invalid_token_address(client: OogaBoogaClient):
    token = "0xFCBD14DC51f0A4d49dasdasdasd0950e0bC26d0Dce"
    amount = "1000000000000000000000"  # 1 token in wei

    approval_response = await client.approve_allowance(token, amount)
    print(f"Approval transaction: {approval_response}")

async def main():
    client = OogaBoogaClient(
        api_key=os.getenv("OOGA_BOOGA_API_KEY"),
        private_key=os.getenv("PRIVATE_KEY")
    )
    # Example: Fetch token list
    await perform_swap_bera(client)

asyncio.run(main())
