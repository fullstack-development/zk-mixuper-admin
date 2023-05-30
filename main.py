from dotenv import load_dotenv
from pycardano import Network, PaymentVerificationKey, Address
import os
from chain import ChainQuery
from mixer import Deposit

load_dotenv()

network = Network.TESTNET
context = ChainQuery(os.environ['BLOCKFROST_PROJECT_ID'],
                     network,
                     base_url=os.environ['BLOCKFROST_BASE_URL'])

owner_verification_key = PaymentVerificationKey.load("owner.vkey")
owner_pub_key_hash = owner_verification_key.hash()
owner_address = Address(
    payment_part=owner_pub_key_hash, network=network)

deposit = Deposit(bytes())
print(deposit.to_cbor_hex())
