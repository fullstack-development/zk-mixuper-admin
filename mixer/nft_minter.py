"""offchain code containing mint class"""
from pycardano import (Network, PaymentVerificationKey, PaymentSigningKey,
                       TransactionOutput, TransactionBuilder, Value,
                       MultiAsset, ScriptPubkey,
                       InvalidHereAfter, ScriptAll)
from chain import ChainQuery, SubmitTx


class Mint(SubmitTx):
    """\
        This class allows minting an NFT with simple script.
        See https://github.com/input-output-hk/cardano-node/blob/master/doc/reference/simple-scripts.md
        Example taken from https://github.com/Python-Cardano/pycardano/blob/main/examples/native_token.py"""

    def __init__(self,
                 network: Network,
                 context: ChainQuery,
                 signing_key: PaymentSigningKey,
                 verification_key: PaymentVerificationKey,
                 ) -> None:
        super().__init__(network, context, signing_key, verification_key)

    def mint_nft_with_script(self):
        """mint tokens with native script"""
        # A policy that requires a signature from the public key
        pub_key_policy = ScriptPubkey(self.pub_key_hash)
        # A time policy that disallows token minting after 10000 seconds from last block
        # "type": "before" means that minting is valid before a slot
        # RequireTimeBefore means that minting tx must be submitted before a slot
        valid_before_slot = InvalidHereAfter(
            self.context.last_block_slot + 10000)
        # Combine two policies using ScriptAll policy
        policy = ScriptAll([pub_key_policy, valid_before_slot])

        policy_id = policy.hash()

        mixer_nft = MultiAsset.from_primitive(
            {
                policy_id.payload: {
                    b"Mixer Protocol Token #1": 1,  # Name of our token  # Quantity of this token
                }
            }
        )

        print(f"Policy id: {policy_id.payload.hex()}")

        # Create a transaction builder
        builder = TransactionBuilder(self.context)

        # Add our own address as the input address
        builder.add_input_address(self.address)

        # Since an InvalidHereAfter rule is included in the policy, we must specify time to live (ttl) for this transaction
        builder.ttl = valid_before_slot.after

        # Set nft we want to mint
        builder.mint = mixer_nft

        # Set native script
        builder.native_scripts = [policy]

        # Send the NFT to our own address
        nft_output = TransactionOutput(
            self.address, Value(2000000, mixer_nft))
        builder.add_output(nft_output)

        self.submit_tx_builder(builder)
