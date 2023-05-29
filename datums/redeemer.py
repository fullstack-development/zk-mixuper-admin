from dataclasses import dataclass
from pycardano import PlutusData

# data MixerRedeemer (s :: S)
#   = Deposit (Term s (PDataRecord '["commitment" := PCommitment]))
#   | Withdraw (Term s (PDataRecord '[]))


@dataclass
class Deposit(PlutusData):
    CONSTR_ID = 0
    commitment: bytes  # :: ByteString


@dataclass
class Withdraw(PlutusData):
    CONSTR_ID = 1
