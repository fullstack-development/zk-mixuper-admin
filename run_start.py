from dotenv import load_dotenv
import cbor2
from pycardano import (Network, Address, PaymentVerificationKey, PaymentSigningKey,
                       PlutusV2Script, PlutusV1Script, plutus_script_hash, RawPlutusData)
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

with open("./depositScript.plutus", "r") as f:
    script_hex = f.read()
    deposit_script = PlutusV2Script(cbor2.loads(bytes.fromhex(script_hex)))
deposit_script_hash = plutus_script_hash(deposit_script)

with open("./withdrawScript.plutus", "r") as f:
    script_hex = f.read()
    withdraw_script = PlutusV2Script(cbor2.loads(bytes.fromhex(script_hex)))
withdraw_script_hash = plutus_script_hash(withdraw_script)

with open("./mintingPolicy.plutus", "r") as f:
    script_hex = f.read()
    minting_script = PlutusV1Script(cbor2.loads(bytes.fromhex(script_hex)))
minting_script_hash = plutus_script_hash(minting_script)

with open("./depositTree.datum", "r") as f:
    datum_hex = f.read()
    deposit_tree_datum = RawPlutusData.from_cbor(bytes.fromhex(datum_hex))

start = MixerStart(network=network, context=context, signing_key=owner_signing_key,
                    verification_key=owner_verification_key)
start.start_mixer(minting_script_hash, deposit_script_hash, withdraw_script_hash, deposit_tree_datum)
