import cbor2
import json
from pycardano import (Network, Address, PaymentVerificationKey, PaymentSigningKey,
                       PlutusV2Script, PlutusV1Script, plutus_script_hash, RawPlutusData)

with open("./depositScript.plutus", "r") as f:
    deposit_script_hex = f.read()

deposit_script_conf = {
  'type': 'PlutusV2',
  'script': deposit_script_hex
}

with open("./withdrawScript.plutus", "r") as f:
    withdraw_script_hex = f.read()

withdraw_script_conf = {
  'type': 'PlutusV2',
  'script': withdraw_script_hex
}

with open("./mintingPolicy.plutus", "r") as f:
    script_hex = f.read()
    minting_script = PlutusV1Script(cbor2.loads(bytes.fromhex(script_hex)))
minting_script_hash = plutus_script_hash(minting_script)
policy_id = minting_script_hash.payload.hex()

# TokenUnit = policyId + encoded tokenName
vault_token_unit = policy_id + b'Vault Token'.hex()
deposit_tree_token_unit = policy_id + b'Deposit Tree Token'.hex()
nullifier_store_token_unit = policy_id + b'Nullifier Store Token'.hex()

zero_leaf = '6e045b8f5eaa4bdc8f8a44797255d03f4e2aac366e32859c5d07cd8de46c2ea3'

pool_config = {
  'zeroValue': zero_leaf,
  'depositScript': deposit_script_conf,
  'withdrawScript': withdraw_script_conf,
  'vaultTokenUnit': vault_token_unit,
  'depositTreeTokenUnit': deposit_tree_token_unit,
  'nullifierStoreTokenUnit': nullifier_store_token_unit,
}

pools = {
  100: pool_config
}

with open("./pools_config.json", "w") as f:
    json.dump(pools, f)
