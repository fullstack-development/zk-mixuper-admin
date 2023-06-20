import cbor2
from pycardano import plutus_script_hash, PlutusV1Script

with open("./mintingPolicy.plutus", "r") as f:
    script_hex = f.read()
    minting_script = PlutusV1Script(cbor2.loads(bytes.fromhex(script_hex)))

policy_id = plutus_script_hash(minting_script)

# Minting policy id: 0586c5ef51fad9b82c91dc2a7eaca200056f19fa25041fb16bb6e735
print(f'Minting policy id: {policy_id}')
