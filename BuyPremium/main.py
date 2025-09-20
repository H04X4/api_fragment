import asyncio
import logging
from .client import FragmentClient
from .transaction import TonTransaction
logging.basicConfig(level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s")

async def main(QUANTITY, QUERY, mountity):
    client = FragmentClient()
    recipient = await client.fetch_recipient(QUANTITY, mountity)
    if recipient:
        req_id = await client.fetch_req_id(recipient, mountity)  
        if req_id:
            recipient, amount_nano, la = await client.fetch_buy_link(recipient, req_id, mountity)  
            if recipient and amount_nano and la:
                amount_decimal = float(amount_nano) / 1_000_000_000
                logging.info(f"Сумма для отправки: {amount_decimal:.4f} TON")
                transaction = TonTransaction()
                await transaction.send_ton_transaction(recipient, amount_decimal, la, QUERY)
if __name__ == "__main__":
    QUANTITY = 1  
    QUERY = "@tgusername"  
    mountity = 3
    asyncio.run(main(QUERY, QUANTITY, mountity))
