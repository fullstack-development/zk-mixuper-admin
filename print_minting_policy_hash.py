import cbor2
from pycardano import plutus_script_hash, PlutusV1Script

with open("./mintingPolicy.plutus", "r") as f:
    script_hex = f.read()
    minting_script = PlutusV1Script(cbor2.loads(bytes.fromhex(script_hex)))

policy_id = plutus_script_hash(minting_script)

# Minting policy id: 2f7a19338244358e8b9d6cc91d8a45d442aae654c8adfa599638eccd
print(f'Minting policy id: {policy_id}')
