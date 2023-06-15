"""offchain code containing mint class"""
from typing import Tuple
from pycardano import (Network, PaymentVerificationKey, PaymentSigningKey,
                       TransactionOutput, TransactionBuilder, Value, Redeemer,
                       MultiAsset, PlutusV1Script, plutus_script_hash)
from chain import ChainQuery, SubmitTx
from mixer import Unit
from .owner_script import OwnerScript


class Mint(SubmitTx):
    """\
        This class allows minting an NFT with simple script.
        See https://github.com/input-output-hk/plutus-apps/blob/v1.1.0/plutus-use-cases/src/Plutus/Contracts/Currency.hs"""

    def __init__(self,
                 network: Network,
                 context: ChainQuery,
                 signing_key: PaymentSigningKey,
                 verification_key: PaymentVerificationKey,
                 utxo_ref: Tuple[str, int],
                 plutus_minting_script: PlutusV1Script
                 ) -> None:
        super().__init__(network, context, signing_key, verification_key)
        self.utxo_ref = utxo_ref
        self.plutus_minting_script = plutus_minting_script

    def mint_nft_with_script(self):
        owner = OwnerScript(self.network, self.context,
                            self.signing_key, self.verification_key)
        utxo = owner.find_utxo(self.utxo_ref)

        policy = self.plutus_minting_script

        policy_id = plutus_script_hash(policy)

        mixer_nfts = MultiAsset.from_primitive(
            {
                policy_id.payload: {
                    # Name of our token  # Quantity of this token
                    b"Deposit Tree Token": 1,
                    b"Vault Token": 1,
                    b"Nullifier Store Token": 1,
                }
            }
        )

        print(f"Policy id: {policy_id.payload.hex()}")

        # Create a transaction builder
        builder = TransactionBuilder(self.context)

        # Add our own address as the input address
        builder.add_input(utxo)
        builder.add_input_address(self.address)

        # Set nft we want to mint
        builder.mint = mixer_nfts

        # Set plutus script
        builder.add_minting_script(
            script=self.plutus_minting_script, redeemer=Redeemer(data=Unit()))

        # Send the NFT to our own address
        nft_output = TransactionOutput(
            self.address, Value(3000000, mixer_nfts))
        builder.add_output(nft_output)

        builder.required_signers = [self.pub_key_hash]

        self.submit_tx_builder(builder)
