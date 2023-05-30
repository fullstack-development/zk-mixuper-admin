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

with open("./mixerScript.plutus", "r") as f:
    script_hex = f.read()
    mixer_script = PlutusV2Script(cbor2.loads(bytes.fromhex(script_hex)))
script_start_slot = 29667384

start = MixerStart(network=network, context=context, signing_key=owner_signing_key,
                    verification_key=owner_verification_key, mixer_script=mixer_script, script_start_slot=script_start_slot)
start.start_mixer()
