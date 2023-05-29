"""offchain code for tx handling"""
from pycardano import (Network, Address, PaymentVerificationKey, PaymentSigningKey,
                       TransactionBuilder)
from .query import ChainQuery


class SubmitTx():

    def __init__(self,
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
        self.address = Address(
            payment_part=self.pub_key_hash, network=self.network)

    def submit_tx_builder(self, builder: TransactionBuilder):
        """adds collateral and signers to tx , sign and submit tx."""
        collateral_utxo = self.context.find_collateral(self.address)

        builder.collaterals.append(collateral_utxo)
        builder.required_signers = [self.pub_key_hash]

        signed_tx = builder.build_and_sign(
            [self.signing_key], change_address=self.address, collateral_change_address=self.address)
        self.context.submit_tx_with_print(signed_tx)
