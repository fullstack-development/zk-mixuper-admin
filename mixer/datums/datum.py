from dataclasses import dataclass
from pycardano import PlutusData
from pycardano.serialization import IndefiniteList

# newtype MixerDatum (s :: S)
#   = MixerDatum (Term s (PDataRecord '["nullifierHashes" := PBuiltinList (PAsData PInteger)]))


@dataclass
class MixerDatum(PlutusData):
    CONSTR_ID = 0
    nullifierHashes: IndefiniteList  # :: [Integer]


# data MixerConfig = MixerConfig
#   { protocolToken :: AssetClass
#   , poolNominal :: Integer
#   }


@dataclass
class MixerConfig(PlutusData):
    CONSTR_ID = 0
    protocolToken: tuple[bytes, bytes]  # :: AssetClass
    poolNominal: int  # :: Integer
