from typing import Tuple
from pycardano import (Network, PaymentVerificationKey, PaymentSigningKey, UTxO)
from chain import ChainQuery, SubmitTx, filter_utxos_by_reference


class OwnerScript(SubmitTx):
    def __init__(self,
                 network: Network,
                 context: ChainQuery,
                 signing_key: PaymentSigningKey,
                 verification_key: PaymentVerificationKey,
                 ) -> None:
        super().__init__(network, context, signing_key, verification_key)

    def get_utxo_ref(self) -> Tuple[str, int]:
        utxo = self.context.find_collateral(self.address)
        ref = utxo.input
        tx_id = ref.transaction_id
        tx_index = ref.index

        return (tx_id.payload.hex(), tx_index)

    def find_utxo(self, utxo_ref: Tuple[str, int]) -> UTxO:
        utxos = self.context.utxos(self.address)
        [utxo] = filter_utxos_by_reference(utxos, utxo_ref)
        return utxo

    def print_start_params(self):
        """Print mixer start params to compile mixer plutus script with"""

        mixer_creator = self.pub_key_hash
        print(f"Mixer Creator: {mixer_creator.payload.hex()}")

        tx_id, tx_index = self.get_utxo_ref()
        print(f"Mixer NFT UTxO reference has id: {tx_id} index: {tx_index}")
