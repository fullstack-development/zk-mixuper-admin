from dotenv import load_dotenv
import cbor2
from pycardano import (Network, Address, PaymentVerificationKey, PaymentSigningKey,
                       PlutusV2Script, plutus_script_hash)
import os
from mixer import MixerUser, OwnerScript, MixerConfig
from chain import ChainQuery

load_dotenv()

network = Network.TESTNET
context = ChainQuery(os.environ['BLOCKFROST_PROJECT_ID'],
                     network,
                     base_url=os.environ['BLOCKFROST_BASE_URL'])

user_signing_key = PaymentSigningKey.load("user.skey")
user_verification_key = PaymentVerificationKey.load("user.vkey")
owner_verification_key = PaymentVerificationKey.load("owner.vkey")
user_pub_key_hash = user_verification_key.hash()
user_address = Address(payment_part=user_pub_key_hash, network=network)

with open("./mixerScript.plutus", "r") as f:
    script_hex = f.read()
    mixer_script = PlutusV2Script(cbor2.loads(bytes.fromhex(script_hex)))

script_start_slot = 29667384
mixer_owner = OwnerScript(network, context, owner_verification_key)
owner_script = mixer_owner.mk_owner_script(script_start_slot)
owner_script_hash = owner_script.hash()

commitment = bytes()

mixer_config = MixerConfig(protocolToken=(
    owner_script_hash.payload, b'Mixer Protocol Token'), poolNominal=100_000_000)

user = MixerUser(network=network, context=context, signing_key=user_signing_key,
                 verification_key=user_verification_key, mixer_script_hash=plutus_script_hash(
                     mixer_script),
                 reference_script_locking_script_hash=owner_script_hash, mixer_config=mixer_config)
user.deposit(commitment)
