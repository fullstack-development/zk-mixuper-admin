from dataclasses import dataclass
from pycardano import PlutusData


# data MixerRedeemer
#   = Deposit Commitment
#   | Topup
#   | Withdraw


@dataclass
class Deposit(PlutusData):
    CONSTR_ID = 0
    commitment: bytes  # :: ByteString


@dataclass
class Topup(PlutusData):
    CONSTR_ID = 1


@dataclass
class WithdrawVault(PlutusData):
    CONSTR_ID = 2


# -- | Just merkle tree root for now
# type PPublicInput = PInteger
# newtype PWithdrawRedeemer (s :: S)
#   = PWithdraw (Term s (PDataRecord '["publicInput" := PPublicInput]))


@dataclass
class Withdraw(PlutusData):
    CONSTR_ID = 0
    publicInput: int  # :: PInteger


@dataclass
class Unit(PlutusData):
    CONSTR_ID = 0  # :: ()
