import cbor2
from pycardano import plutus_script_hash, PlutusV1Script

with open("./mintingPolicy.plutus", "r") as f:
    script_hex = f.read()
    minting_script = PlutusV1Script(cbor2.loads(bytes.fromhex(script_hex)))

policy_id = plutus_script_hash(minting_script)

# Minting policy id: cd4ecd8b80466c7325e9d2f76fce6eb8a236667734eb1646bcfdcb51
print(f'Minting policy id: {policy_id}')
