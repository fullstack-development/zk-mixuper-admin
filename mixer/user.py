from copy import deepcopy
from pycardano import (UTxO, ScriptHash, Network, Address, PaymentVerificationKey, PaymentSigningKey,
                       TransactionBuilder, Redeemer, MultiAsset, plutus_script_hash, Value
                       )
from chain import ChainQuery, SubmitTx, filter_utxos_by_asset, filter_utxos_by_script_hash
from .datums import MixerDatum, Deposit, MixerConfig


class MixerUser(SubmitTx):

    def __init__(self,
                 network: Network,
                 context: ChainQuery,
                 signing_key: PaymentSigningKey,
                 verification_key: PaymentVerificationKey,
                 mixer_script_hash: ScriptHash,
                 reference_script_locking_script_hash: ScriptHash,
                 mixer_config: MixerConfig,
                 ) -> None:
        super().__init__(network, context, signing_key, verification_key)
        self.mixer_script_hash = mixer_script_hash
        self.mixer_address = Address(
            payment_part=self.mixer_script_hash, network=self.network)
        (curr_symbol, token_name) = mixer_config.protocolToken
        self.mixer_config = mixer_config
        self.mixer_nft_policy = ScriptHash(curr_symbol)
        self.mixer_nft = MultiAsset.from_primitive(
            {
                self.mixer_nft_policy.payload: {
                    token_name: 1,
                }
            }
        )
        self.reference_script_locking_script_hash = reference_script_locking_script_hash
        self.reference_script_address = Address(
            payment_part=self.reference_script_locking_script_hash, network=self.network)

    def deposit(self, commitment: bytes):
        mixer_utxos = self.context.utxos(str(self.mixer_address))
        correct_mixer_utxo: UTxO = filter_utxos_by_asset(
            mixer_utxos, self.mixer_nft)[0]

        print(f"Mixer output: {correct_mixer_utxo}")

        deposit_redeemer = Deposit(commitment)
        redeemer = Redeemer(deposit_redeemer)

        reference_script_outputs = self.context.utxos(
            str(self.reference_script_address))
        correct_ref_script_out = filter_utxos_by_script_hash(
            reference_script_outputs, self.mixer_script_hash)[0]

        print(
            f"Reference script hash: {plutus_script_hash(correct_ref_script_out.output.script)} \nScript hash: {self.mixer_script_hash}")

        initial_datum = MixerDatum.from_cbor(
            correct_mixer_utxo.output.datum.cbor)
        new_datum = deepcopy(initial_datum)

        print(f"New mixer datum: {new_datum}")

        builder = TransactionBuilder(self.context)
        builder.add_script_input(utxo=correct_mixer_utxo, redeemer=deepcopy(
            redeemer), script=correct_ref_script_out)

        new_mixer_out = deepcopy(correct_mixer_utxo.output)
        new_mixer_out.datum = new_datum
        new_mixer_out.amount += Value(self.mixer_config.poolNominal)
        builder.add_output(new_mixer_out)

        builder.add_input_address(self.address)

        builder.required_signers = [self.pub_key_hash]

        self.submit_tx_builder(builder)
