from typing import List, Tuple
from pycardano import (Network, Address, Redeemer, PlutusV1Script, PaymentVerificationKey, PaymentSigningKey, ScriptHash,
                       TransactionOutput, TransactionBuilder, Value, datum_hash, MultiAsset, PlutusV2Script, plutus_script_hash)
from pycardano.serialization import IndefiniteList
from chain import ChainQuery, SubmitTx
from .datums import DepositTree, Vault, WithdrawDatum, Unit
from .owner_script import OwnerScript


class MixerStart(SubmitTx):
    """Start mixer by submitting a reference script and minting its NFT"""

    def __init__(self,
                 network: Network,
                 context: ChainQuery,
                 signing_key: PaymentSigningKey,
                 verification_key: PaymentVerificationKey,

                 ) -> None:
        super().__init__(network, context, signing_key, verification_key)

    def start_mixer(self, owner_utxo_ref: Tuple[str, int], plutus_minting_script: PlutusV1Script,
                    deposit_script_hash: ScriptHash, withdraw_script_hash: ScriptHash, deposit_tree_datum):
        # Create a script that mints mixer NFT
        owner = OwnerScript(self.network, self.context,
                            self.signing_key, self.verification_key)
        utxo = owner.find_utxo(owner_utxo_ref)
        policy = plutus_minting_script
        policy_id = plutus_script_hash(policy)
        print(f"Protocol token Policy id: {policy_id.payload.hex()}")

        # Create a transaction builder
        builder = TransactionBuilder(self.context)

        # Add our own address as the input address
        builder.add_input(utxo)
        builder.add_input_address(self.address)

        ############ Mixer NFT minting: ############
        deposit_tree_token = MultiAsset.from_primitive(
            {
                policy_id.payload: {
                    b"Deposit Tree Token": 1,
                }
            }
        )
        vault_token = MultiAsset.from_primitive(
            {
                policy_id.payload: {
                    b"Vault Token": 1,
                }
            }
        )
        nullifier_store_token = MultiAsset.from_primitive(
            {
                policy_id.payload: {
                    b"Nullifier Store Token": 1,
                }
            }
        )
        mixer_nfts = deposit_tree_token + vault_token + nullifier_store_token

        # Set nft we want to mint
        builder.mint = mixer_nfts

        # Set plutus mint script
        builder.add_minting_script(
            script=plutus_minting_script, redeemer=Redeemer(data=Unit()))

        ############ Mixer first outputs creation: ############
        deposit_script_address = Address(
            payment_part=deposit_script_hash, network=self.network)
        print(
            f"Deposit script hash: {deposit_script_hash} \nDeposit script address: {deposit_script_address}")

        withdraw_script_address = Address(
            payment_part=withdraw_script_hash, network=self.network)
        print(
            f"Withdraw script hash: {withdraw_script_hash} \nWithdraw script address: {withdraw_script_address}")

        # Deposit Tree
        print(f"Deposit Tree datum hash: {datum_hash(deposit_tree_datum)}")
        deposit_tree_output = TransactionOutput(datum=deposit_tree_datum,
                                                address=deposit_script_address, amount=Value(2000000, deposit_tree_token))
        builder.add_output(deposit_tree_output)

        # Vault
        vault_datum = Vault()
        print(f"Vault datum hash: {datum_hash(vault_datum)}")
        vault_output = TransactionOutput(datum=vault_datum,
                                         address=deposit_script_address, amount=Value(2000000, vault_token))
        builder.add_output(vault_output)

        # Nullifier Store
        nullifier_store_datum = WithdrawDatum(
            nullifierHashes=IndefiniteList([]))
        print(
            f"Nullifier Store datum hash: {datum_hash(nullifier_store_datum)}")
        nullifier_store_output = TransactionOutput(datum=nullifier_store_datum,
                                                   address=withdraw_script_address, amount=Value(2000000, nullifier_store_token))
        builder.add_output(nullifier_store_output)

        builder.required_signers = [self.pub_key_hash]
        self.submit_tx_builder(builder)

    def deploy_deposit_script(self, deposit_script: PlutusV2Script):
        ############ Reference script creation: ############
        deposit_script_hash = plutus_script_hash(deposit_script)
        deposit_script_address = Address(
            payment_part=deposit_script_hash, network=self.network)
        print(
            f"Deposit script hash: {deposit_script_hash} \nDeposit script address: {deposit_script_address}")

        # Create a transaction builder
        builder = TransactionBuilder(self.context)

        # Add our own address as the input address
        builder.add_input_address(self.address)

        # Reference script output
        reference_script_utxo = TransactionOutput(
            address=deposit_script_address,
            amount=25000000,
            script=deposit_script
        )

        # Add reference script
        builder.add_output(reference_script_utxo)

        builder.required_signers = [self.pub_key_hash]
        self.submit_tx_builder(builder)

    def deploy_withdraw_script(self, withdraw_script: PlutusV2Script):
        ############ Reference script creation: ############
        withdraw_script_hash = plutus_script_hash(withdraw_script)
        withdraw_script_address = Address(
            payment_part=withdraw_script_hash, network=self.network)
        print(
            f"Withdraw script hash: {withdraw_script_hash} \nWithdraw script address: {withdraw_script_address}")

        # Create a transaction builder
        builder = TransactionBuilder(self.context)

        # Add our own address as the input address
        builder.add_input_address(self.address)

        # Reference script output
        reference_script_utxo = TransactionOutput(
            address=withdraw_script_address,
            amount=25000000,
            script=withdraw_script
        )

        # Add reference script
        builder.add_output(reference_script_utxo)

        builder.required_signers = [self.pub_key_hash]
        self.submit_tx_builder(builder)
