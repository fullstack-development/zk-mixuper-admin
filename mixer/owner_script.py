from typing import Tuple
from pycardano import (Network, PaymentVerificationKey, ScriptAll, ScriptPubkey, NativeScript,
                       InvalidBefore)
from chain import ChainQuery

class OwnerScript():
    def __init__(self,
                 network: Network,
                 context: ChainQuery,
                 owner_verification_key: PaymentVerificationKey,
                 ) -> None:
        self.network = network
        self.context = context
        self.owner_verification_key = owner_verification_key
        self.owner_pub_key_hash = self.owner_verification_key.hash()

    def create_owner_script(self) -> Tuple[int, NativeScript]:
        # requires later addition of
        # tx_builder.validity_start = script_start_slot
        script_start_slot: int = self.context.last_block_slot

        # remember to save that value for later script hash construction
        print(f"Script start slot: {script_start_slot}")

        owner_script = self.mk_owner_script(script_start_slot)

        return (script_start_slot, owner_script)

    def mk_owner_script(self, script_start_slot: int) -> NativeScript:
        # A policy that requires a signature from the public key
        pub_key_policy = ScriptPubkey(self.owner_pub_key_hash)

        # A time policy that validates before a certain slot:
        # this is to parametrize script and make a unique script hash (e.g. to make a NFT),
        # and it is done to ensure that owner could spend/burn later.
        # "type": "after" means that minting/spending is valid after a slot
        # RequireTimeAfter means that minting/spending tx must be submitted after a slot
        valid_after_slot = InvalidBefore(script_start_slot)

        # Combine two policies using ScriptAll policy
        policy = ScriptAll([pub_key_policy, valid_after_slot])

        return policy

    def print_start_params(self):
        """Print mixer start params to compile mixer plutus script with"""

        mixer_creator = self.owner_pub_key_hash
        print(f"Mixer Creator: {mixer_creator.payload.hex()}")

        _, nft_policy = self.create_owner_script()
        print(f"Mixer NFT currency symbol: {nft_policy.hash().payload.hex()}")
