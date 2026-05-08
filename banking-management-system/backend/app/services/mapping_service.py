from typing import List
from app.schemas.upload import FieldMappingItem

STANDARD_FIELDS = [
    "account_no", "date", "amount", "debit", "credit",
    "balance", "description", "transaction_id", "type",
    "branch", "currency", "reference_no",
]

ALIASES = {
    "account_no": ["acct", "account", "acc", "account_number", "acct_no", "account_no"],
    "date": ["date", "txn_date", "trans_date", "transaction_date", "value_date", "posting_date"],
    "amount": ["amount", "amt", "transaction_amount", "txn_amt"],
    "debit": ["debit", "dr", "debit_amt", "withdrawal", "debit_amount"],
    "credit": ["credit", "cr", "credit_amt", "deposit", "credit_amount"],
    "balance": ["balance", "bal", "closing_balance", "running_balance"],
    "description": ["description", "narration", "remarks", "particulars", "details", "memo"],
    "transaction_id": ["transaction_id", "txn_id", "trans_id", "ref_no", "reference"],
    "type": ["type", "txn_type", "transaction_type", "dr/cr", "dr_cr"],
    "branch": ["branch", "branch_name", "branch_code"],
    "currency": ["currency", "ccy", "curr"],
    "reference_no": ["reference_no", "ref_no", "cheque_no", "chq_no"],
}


class MappingService:

    @staticmethod
    def suggest_mappings(columns: List[str]) -> List[FieldMappingItem]:
        mappings = []
        for col in columns:
            matched = MappingService._match_column(col)
            mappings.append(FieldMappingItem(
                original_column=col,
                mapped_column=matched or col.lower().replace(" ", "_"),
            ))
        return mappings

    @staticmethod
    def _match_column(col: str) -> str:
        normalized = col.lower().strip().replace(" ", "_").replace("-", "_")
        for standard, aliases in ALIASES.items():
            if normalized in aliases:
                return standard
        return ""
