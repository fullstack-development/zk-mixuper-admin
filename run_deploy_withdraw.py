from dotenv import load_dotenv
import cbor2
from pycardano import (Network, Address, PaymentVerificationKey, PaymentSigningKey,
                       PlutusV2Script)
import os
from mixer import MixerStart
from chain import ChainQuery

load_dotenv()

network = Network.TESTNET
context = ChainQuery(os.environ['BLOCKFROST_PROJECT_ID'],
                     network,
                     base_url=os.environ['BLOCKFROST_BASE_URL'])

owner_signing_key = PaymentSigningKey.load("owner.skey")
owner_verification_key = PaymentVerificationKey.load("owner.vkey")
owner_pub_key_hash = owner_verification_key.hash()
owner_address = Address(payment_part=owner_pub_key_hash, network=network)

with open("./withdrawScript.plutus", "r") as f:
    script_hex = f.read()
    withdraw_script = PlutusV2Script(cbor2.loads(bytes.fromhex(script_hex)))

start = MixerStart(network=network, context=context, signing_key=owner_signing_key,
                    verification_key=owner_verification_key)
start.deploy_withdraw_script(withdraw_script)
