from dotenv import load_dotenv
import os
import cbor2
from pycardano import Network, PaymentVerificationKey, PaymentSigningKey, PlutusV1Script
from mixer import Mint
from chain import ChainQuery

load_dotenv()

network = Network.TESTNET
context = ChainQuery(os.environ['BLOCKFROST_PROJECT_ID'],
                     network,
                     base_url=os.environ['BLOCKFROST_BASE_URL'])

owner_verification_key = PaymentVerificationKey.load("owner.vkey")
owner_signing_key = PaymentSigningKey.load("owner.skey")

utxo_ref = ('8f1efed2e61abd2ece188f7f98fcf0a89ccb5df1bcc7d1f6acb0f01bd2676070', 1)

with open("./mintingPolicy.plutus", "r") as f:
    script_hex = f.read()
    minting_script = PlutusV1Script(cbor2.loads(bytes.fromhex(script_hex)))

minter = Mint(
    network, context, owner_signing_key, owner_verification_key, utxo_ref, minting_script)
minter.mint_nft_with_script()
