from dataclasses import dataclass
from pycardano import PlutusData
from pycardano.serialization import IndefiniteList

# newtype MixerDatum (s :: S)
#   = MixerDatum (Term s (PDataRecord '["nullifierHashes" := PBuiltinList (PAsData PInteger)]))
#   deriving stock (Generic)
#   deriving anyclass (PlutusType, PDataFields, PIsData, PEq)


@dataclass
class MixerDatum(PlutusData):
    CONSTR_ID = 0
    nullifierHashes: IndefiniteList  # :: [Integer]
