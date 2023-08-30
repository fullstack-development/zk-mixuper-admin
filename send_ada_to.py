from dotenv import load_dotenv
from typing import List
import os
from pycardano import (
    Network,
    PaymentVerificationKey,
    PaymentSigningKey,
    Address,
    TransactionBuilder,
    TransactionOutput,
)
from chain import ChainQuery

load_dotenv()

network = Network.TESTNET
context = ChainQuery(
    os.environ["BLOCKFROST_PROJECT_ID"],
    network,
    base_url=os.environ["BLOCKFROST_BASE_URL"],
)

owner_verification_key = PaymentVerificationKey.load("owner.vkey")
owner_signing_key = PaymentSigningKey.load("owner.skey")


def send_ada_to(addresses: List[str], amount: int):
    """Send ADA to a list of addresses."""
    sender_address = Address(owner_verification_key.hash(), network=network)
    topup_amount = amount * 1_000_000

    builder = TransactionBuilder(context)

    for address in addresses:
        builder.add_output(
            TransactionOutput(
                address=Address.from_primitive(address), amount=topup_amount
            )
        )

    builder.add_input_address(sender_address)
    signed_tx = builder.build_and_sign(
        signing_keys=[owner_signing_key],
        change_address=sender_address,
    )
    context.submit_tx_with_print(signed_tx)
    print(f"Sent {amount} ada to {len(addresses)} addresses")


if __name__ == "__main__":
    send_ada_to(
        [
            "addr_test1vr50zddqwp847fr2uy4935xvcck5m45vd2wa7c7jagn3pxq6skwcz",
            "addr_test1vq9226a3phrsgy4jawdxdwclrq6zn8d52gv43tfrdympjdqlg2cff",
        ],
        50,
    )
