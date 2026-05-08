BLOCKED_PATTERNS = [
    "password", "passwd", "secret", "pin", "otp",
    "ssn", "social security", "aadhar", "pan number",
    "hack", "exploit", "bypass", "inject", "drop table",
    "personal address", "phone number", "private",
    "salary of", "account of other", "other user",
]

SAFE_REFUSAL = (
    "I can only assist with your own transaction and banking data queries. "
    "I cannot access sensitive personal information, credentials, or other users' data."
)


def is_suspicious(query: str) -> bool:
    lowered = query.lower()
    return any(pattern in lowered for pattern in BLOCKED_PATTERNS)
