import cbor2
from pycardano import plutus_script_hash, PlutusV1Script

with open("./mintingPolicy.plutus", "r") as f:
    script_hex = f.read()
    minting_script = PlutusV1Script(cbor2.loads(bytes.fromhex(script_hex)))

policy_id = plutus_script_hash(minting_script)

# Minting policy id: 2bd66802eef8424e78091f67b7d82c54f3c7f4bcb6b0b5452df5023f
print(f'Minting policy id: {policy_id}')
