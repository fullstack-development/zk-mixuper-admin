from dotenv import load_dotenv
import os
from pycardano import (Network, PaymentVerificationKey)
from mixer import OwnerScript
from chain import ChainQuery

load_dotenv()

network = Network.TESTNET
context = ChainQuery(os.environ['BLOCKFROST_PROJECT_ID'],
                     network,
                     base_url=os.environ['BLOCKFROST_BASE_URL'])

owner_verification_key = PaymentVerificationKey.load("owner.vkey")
owner_pub_key_hash = owner_verification_key.hash()

mixer_owner = OwnerScript(network, context, owner_verification_key)
# Mixer Creator: d1ce83174feeb6ae11d95fd47cac403642cb616b244dbb32a2ca0bda
# Script start slot: 29667384
# Mixer NFT currency symbol: bbd65a4af3dd5bb07b11cfb66418cdffc6bd26817559e0c5a80f405d
mixer_owner.print_start_params()
