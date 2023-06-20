from dotenv import load_dotenv
import os
from pycardano import Network, PaymentVerificationKey, PaymentSigningKey
from mixer import OwnerScript
from chain import ChainQuery

load_dotenv()

network = Network.TESTNET
context = ChainQuery(os.environ['BLOCKFROST_PROJECT_ID'],
                     network,
                     base_url=os.environ['BLOCKFROST_BASE_URL'])

owner_verification_key = PaymentVerificationKey.load("owner.vkey")
owner_signing_key = PaymentSigningKey.load("owner.skey")

mixer_owner = OwnerScript(
    network, context, owner_signing_key, owner_verification_key)

# Mixer Creator: d1ce83174feeb6ae11d95fd47cac403642cb616b244dbb32a2ca0bda
# Mixer NFT UTxO reference has id: 542af902292561d7488715dbb0404b9ff29cee7042601edd827e9ea19b38ddc1 index: 1
mixer_owner.print_start_params()
