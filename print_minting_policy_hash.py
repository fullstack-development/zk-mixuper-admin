import cbor2
from pycardano import plutus_script_hash, PlutusV1Script

with open("./mintingPolicy.plutus", "r") as f:
    script_hex = f.read()
    minting_script = PlutusV1Script(cbor2.loads(bytes.fromhex(script_hex)))

policy_id = plutus_script_hash(minting_script)

# Minting policy id: 9e2292858a865a6a4e8774e089c7186c20703de715dafd36c2f32d83
print(f'Minting policy id: {policy_id}')
