from dotenv import load_dotenv
from typing import List
import os
import cbor2
from pycardano import (
    Network,
    PaymentVerificationKey,
    PaymentSigningKey,
    Address,
    TransactionBuilder,
    TransactionOutput,
    PlutusV2Script,
)
from chain import ChainQuery
from mixer.user import User

load_dotenv()

network = Network.TESTNET
context = ChainQuery(
    os.environ["BLOCKFROST_PROJECT_ID"],
    network,
    base_url=os.environ["BLOCKFROST_BASE_URL"],
)

owner_verification_key = PaymentVerificationKey.load("owner.vkey")
owner_signing_key = PaymentSigningKey.load("owner.skey")

with open("./forty_two.cbor", "r") as f:
    script_hex = f.read()
    plutus_script = PlutusV2Script(cbor2.loads(bytes.fromhex(script_hex)))

user = User(network, context, owner_signing_key, owner_verification_key, plutus_script)
tx = user.make_unlock_42_tx()

with open("./tx.payload", "w") as f:
    tx_hex = tx.to_cbor().hex()
    f.write(tx_hex)
