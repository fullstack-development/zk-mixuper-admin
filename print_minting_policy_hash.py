import cbor2
from pycardano import plutus_script_hash, PlutusV1Script

with open("./mintingPolicy.plutus", "r") as f:
    script_hex = f.read()
    minting_script = PlutusV1Script(cbor2.loads(bytes.fromhex(script_hex)))

policy_id = plutus_script_hash(minting_script)

# Minting policy id: 75a07ecddfcd14b0b5ac5b3ca3d03ee8337145166bc522a5ec1529c0
print(f'Minting policy id: {policy_id}')
