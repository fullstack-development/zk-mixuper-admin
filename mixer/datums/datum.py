from dataclasses import dataclass
from pycardano import PlutusData
from pycardano.serialization import IndefiniteList


# data DepositDatum = DepositDatum
#   { merkleTreeState :: MerkleTreeState,
#     merkleTreeRoot :: Maybe Integer
#   }


class DepositDatum(PlutusData):
    CONSTR_ID = 0
    merkleTreeState: PlutusData  # :: MerkleTreeState
    merkleTreeRoot: PlutusData  # :: Maybe Integer


# data MixerDatum
#   = DepositTree DepositDatum
#   | Vault


@dataclass
class DepositTree(PlutusData):
    CONSTR_ID = 0
    depositDatum: DepositDatum


class Vault(PlutusData):
    CONSTR_ID = 1


# newtype PWithdrawDatum (s :: S)
#   = PWithdrawDatum (Term s (PDataRecord '["nullifierHashes" := PBuiltinList (PAsData PInteger)]))


@dataclass
class WithdrawDatum(PlutusData):
    CONSTR_ID = 0
    nullifierHashes: IndefiniteList  # :: [Integer]


# data DepositConfig = DepositConfig
#   { protocolCurrency :: CurrencySymbol,
#     depositTreeTokenName :: TokenName,
#     vaultTokenName :: TokenName,
#     nullifierStoreTokenName :: TokenName,
#     poolNominal :: Integer,
#     merkleTreeConfig :: MerkleTreeConfig
#   }


@dataclass
class DepositConfig(PlutusData):
    CONSTR_ID = 0
    protocolCurrency: bytes  # :: CurrencySymbol
    depositTreeTokenName: bytes  # :: TokenName
    vaultTokenName: bytes  # :: TokenName
    nullifierStoreTokenName: bytes  # :: TokenName
    poolNominal: int  # :: Integer
    merkleTreeConfig: PlutusData  # :: MerkleTreeConfig
