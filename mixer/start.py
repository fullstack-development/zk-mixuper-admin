from typing import List
from pycardano import (Network, Address, PaymentVerificationKey, PaymentSigningKey,
                       TransactionOutput, TransactionBuilder, Value, datum_hash, MultiAsset, PlutusV2Script, plutus_script_hash)
from chain import ChainQuery, SubmitTx
from .datums import *
from .owner_script import OwnerScript


class MixerStart(SubmitTx):
    """Start mixer by submitting a reference script and minting its NFT"""

    def __init__(self,
                 network: Network,
                 context: ChainQuery,
                 signing_key: PaymentSigningKey,
                 verification_key: PaymentVerificationKey,
                 mixer_script: PlutusV2Script,
                 script_start_slot: int,
                 ) -> None:
        super().__init__(network, context, signing_key, verification_key)
        self.mixer_script = mixer_script
        self.mixer_script_hash = plutus_script_hash(self.mixer_script)
        self.mixer_address = Address(
            payment_part=self.mixer_script_hash, network=self.network)
        self.script_start_slot = script_start_slot
        self.mixer_datum = MixerDatum(nullifierHashes=IndefiniteList([]))

    def start_mixer(self):
        # Create a locking script that hold mixer script and also mints mixer NFT
        mixer_owner = OwnerScript(
            self.network, self.context, self.verification_key)
        owner_script = mixer_owner.mk_owner_script(self.script_start_slot)
        owner_script_hash = owner_script.hash()

        # Create a transaction builder
        builder = TransactionBuilder(self.context)

        # Add our own address as the input address
        builder.add_input_address(self.address)

        # Required since owner script is InvalidBefore type
        builder.validity_start = self.script_start_slot

        ############ Reference script creation: ############
        owner_script_addr = Address(
            payment_part=owner_script_hash, network=self.network)

        print(f"Locking script address: {owner_script_addr}")

        # Reference script output
        reference_script_utxo = TransactionOutput(
            address=owner_script_addr,
            amount=25000000,
            script=self.mixer_script
        )

        # Add reference script
        builder.add_output(reference_script_utxo)

        ############ Mixer NFT minting: ############
        mixer_nft = MultiAsset.from_primitive(
            {
                owner_script_hash.payload: {
                    b"Mixer Protocol Token": 1,  # Name of our token  # Quantity of this token
                }
            }
        )

        print(
            f"Protocol token currency / Policy id: {owner_script_hash.payload.hex()}")

        # Set nft we want to mint
        builder.mint = mixer_nft

        # Set native script
        builder.native_scripts = [owner_script]

        ############ Mixer first output creation: ############
        print(
            f"Mixer script hash: {self.mixer_script_hash} \nMixer script address: {self.mixer_address}")

        print(f"Mixer datum hash: {datum_hash(self.mixer_datum)}")

        output_with_inline_datum = TransactionOutput(datum=self.mixer_datum,
                                                     address=self.mixer_address, amount=Value(2000000, mixer_nft))
        builder.add_output(output_with_inline_datum)

        self.submit_tx_builder(builder)
