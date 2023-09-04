from typing import List, Tuple
from pycardano import (
    Network,
    Address,
    Redeemer,
    Transaction,
    PaymentVerificationKey,
    PaymentSigningKey,
    ScriptHash,
    TransactionOutput,
    TransactionBuilder,
    Value,
    UTxO,
    datum_hash,
    PlutusV2Script,
    plutus_script_hash,
)
from pycardano.serialization import IndefiniteList
from chain import ChainQuery, SubmitTx
from mixer import Unit


class User(SubmitTx):
    def __init__(
        self,
        network: Network,
        context: ChainQuery,
        signing_key: PaymentSigningKey,
        verification_key: PaymentVerificationKey,
        plutus_v2_script: PlutusV2Script,
    ) -> None:
        super().__init__(network, context, signing_key, verification_key)
        self.plutus_v2_script = plutus_v2_script
        self.script_hash = plutus_script_hash(plutus_v2_script)
        self.script_address = Address(
            payment_part=self.script_hash, network=self.network
        )

    def lock_42(self) -> None:
        datum = Unit()

        # Create a transaction builder
        builder = TransactionBuilder(self.context)

        # Add our own address as the input address
        builder.add_input_address(self.address)

        # Add script output
        script_out = TransactionOutput(
            self.script_address, Value(15_000_000), datum_hash=datum_hash(datum)
        )
        builder.add_output(script_out)

        future_collateral = TransactionOutput(self.address, Value(10_000_000))
        builder.add_output(future_collateral)

        builder.required_signers = [self.pub_key_hash]

        self.submit_tx_builder(builder)

    def make_unlock_42_tx(self) -> Transaction:
        script_utxos = self.context.utxos(str(self.script_address))
        correct_script_utxo: UTxO = script_utxos[0]
        redeemer = Redeemer(42)

        # Create a transaction builder
        builder = TransactionBuilder(self.context)

        # Add our own address as the input address
        builder.add_input_address(self.address)

        # Set plutus script
        builder.add_script_input(
            utxo=correct_script_utxo,
            redeemer=redeemer,
            script=self.plutus_v2_script,
            datum=Unit(),
        )

        future_collateral = TransactionOutput(self.address, Value(10_000_000))
        builder.add_output(future_collateral)

        builder.required_signers = [self.pub_key_hash]

        self.build_tx(builder)
