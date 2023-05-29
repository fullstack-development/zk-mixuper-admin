"""Implementing Mixer checks and filters"""
from typing import List
from pycardano import UTxO, MultiAsset, ScriptHash, plutus_script_hash, PlutusV2Script
import cbor2
from copy import deepcopy


def filter_utxos_by_asset(utxos: List[UTxO], asset: MultiAsset):
    """filter list of UTxOs by given asset"""
    return list(filter(lambda x: x.output.amount.multi_asset >= asset, utxos))


def filter_utxos_by_script_hash(utxos: List[UTxO], script_hash: ScriptHash):
    """filter list of UTxOs by script hash"""
    filtered = list(filter(lambda x: plutus_script_hash(
        x.output.script) == script_hash, utxos))
    if filtered == []:
        return list(filter(lambda x: fix_reference_script(x, script_hash), deepcopy(utxos)))
    else:
        return filtered


def fix_reference_script(utxo: UTxO, script_hash: ScriptHash) -> bool:
    if utxo.output.script:
        plutus_script = PlutusV2Script(cbor2.dumps(utxo.output.script))
        utxo.output.script = plutus_script
    return plutus_script_hash(utxo.output.script) == script_hash
