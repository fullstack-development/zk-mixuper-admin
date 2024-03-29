from pycardano import BlockFrostChainContext, Network, TransactionBuilder, TransactionOutput, Transaction
from blockfrost import ApiUrls, BlockFrostApi
from blockfrost.utils import request_wrapper
import os
import requests
from retry import retry


class BlockFrostDatumApi(BlockFrostApi):

    def __init__(self, project_id: str = None, base_url: str = None, api_version: str = None):
        super().__init__(
            project_id=project_id,
            base_url=base_url if base_url else os.environ.get(
                'BLOCKFROST_API_URL', default=ApiUrls.mainnet.value),
            api_version=api_version)

    @request_wrapper
    def script_datum_cbor(self, datum_hash: str, **kwargs):
        """
        Query cbor value of a datum by its hash.

        https://docs.blockfrost.io/#tag/Cardano-Scripts/paths/~1scripts~1datum~1{datum_hash}/get

        :param datum_hash: Hash of the datum.
        :type datum_hash: str
        :param return_type: Optional. "object", "json" or "pandas". Default: "object".
        :type return_type: str
        :returns object.
        :rtype: Namespace
        :raises ApiError: If API fails
        :raises Exception: If the API response is somehow malformed.
        """
        return requests.get(
            url=f"{self.url}/scripts/datum/{datum_hash}/cbor",
            headers=self.default_headers
        )


class ChainQuery(BlockFrostChainContext):
    def __init__(
        self, project_id: str, network: Network = Network.TESTNET, base_url: str = None
    ):
        super().__init__(
            project_id=project_id,
            network=network,
            base_url=base_url
        )
        self.api = BlockFrostDatumApi(
            project_id=self._project_id, base_url=self._base_url)

    def _get_datum(self, utxo):
        if utxo.output.datum_hash is not None:
            datum = self.api.script_datum_cbor(
                str(utxo.output.datum_hash)).cbor
            return datum
        return None

    def get_datums_for_utxo(self, utxos):
        """insert datum for UTxOs"""
        result = []
        if len(utxos) > 0:
            for utxo in utxos:
                datum = self._get_datum(utxo)
                result.append(datum)
        return result

    @retry(delay=10)
    def wait_for_tx(self, tx_id):
        self.api.transaction(tx_id)
        print(
            f"Transaction {tx_id} has been successfully included in the blockchain.")

    def submit_tx_with_print(self, tx: Transaction):
        print("############### Transaction created ###############")
        print(tx)
        print("############### Submitting transaction ###############")
        cbor = tx.to_cbor()
        print(cbor.hex())
        self.submit_tx(cbor)
        self.wait_for_tx(str(tx.id))

    def find_collateral(self, target_address):
        """return first output that contains no less that 5 ADA"""
        for utxo in self.utxos(str(target_address)):
            if utxo.output.amount.coin >= 10000000:
                return utxo
        return None

    def create_collateral(self, target_address, skey):
        collateral_builder = TransactionBuilder(self)

        collateral_builder.add_input_address(target_address)
        collateral_builder.add_output(
            TransactionOutput(target_address, 10000000))

        self.submit_tx_with_print(
            collateral_builder.build_and_sign([skey], target_address))
