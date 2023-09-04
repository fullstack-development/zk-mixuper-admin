"""offchain code for tx handling"""
from pycardano import (
    Network,
    Address,
    PaymentVerificationKey,
    PaymentSigningKey,
    TransactionBuilder,
    Transaction,
    VerificationKeyWitness,
)
from .query import ChainQuery


class SubmitTx:
    def __init__(
        self,
        network: Network,
        context: ChainQuery,
        signing_key: PaymentSigningKey,
        verification_key: PaymentVerificationKey,
    ) -> None:
        self.network = network
        self.context = context
        self.signing_key = signing_key
        self.verification_key = verification_key
        self.pub_key_hash = self.verification_key.hash()
        self.address = Address(payment_part=self.pub_key_hash, network=self.network)

    def submit_tx_builder(self, builder: TransactionBuilder):
        """adds collateral and signers to tx , sign and submit tx."""
        collateral_utxo = self.context.find_collateral(self.address)

        builder.collaterals.append(collateral_utxo)
        builder.required_signers = [self.pub_key_hash]

        signed_tx = builder.build_and_sign(
            [self.signing_key],
            change_address=self.address,
            collateral_change_address=self.address,
        )
        self.context.submit_tx_with_print(signed_tx)

    def build_tx(self, builder: TransactionBuilder) -> Transaction:
        collateral_utxo = self.context.find_collateral(self.address)

        builder.collaterals.append(collateral_utxo)

        tx_body = builder.build(
            change_address=self.address, collateral_change_address=self.address
        )
        witness_set = builder.build_witness_set()
        witness_set.vkey_witnesses = []

        return Transaction(tx_body, witness_set, auxiliary_data=builder.auxiliary_data)

    def sign_tx(self, tx: Transaction):
        signature = self.signing_key.sign(tx.transaction_body.hash())
        tx.transaction_witness_set.vkey_witnesses.append(
            VerificationKeyWitness(self.verification_key, signature)
        )

    def sign_and_submit_tx(self, tx: Transaction):
        self.sign_tx(tx)
        self.context.submit_tx_with_print(tx)
