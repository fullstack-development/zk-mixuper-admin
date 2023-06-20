import cbor2
from pycardano import plutus_script_hash, PlutusV1Script

with open("./mintingPolicy.plutus", "r") as f:
    script_hex = f.read()
    minting_script = PlutusV1Script(cbor2.loads(bytes.fromhex(script_hex)))

policy_id = plutus_script_hash(minting_script)

# Minting policy id: 7e0e1e67a5d0c511f149f9aaba428ff94b5092956b1057e67b2d4967
print(f'Minting policy id: {policy_id}')
