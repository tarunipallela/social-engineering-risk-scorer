from functools import lru_cache

import spacy

from app.nlp.patterns import (
    EMAIL_REGEX,
    FAMILY_KEYWORDS,
    JOB_KEYWORDS,
    PHONE_REGEX,
    ROUTINE_WORDS,
    TIME_REGEX,
    TRAVEL_KEYWORDS,
)


@lru_cache(maxsize=1)
def _get_nlp():
    return spacy.load("en_core_web_sm")


def _contains_any(text: str, keywords: set[str]) -> bool:
    lower_text = text.lower()
    return any(keyword in lower_text for keyword in keywords)


def _count_family_hits(text: str) -> int:
    lower_text = text.lower()
    return sum(1 for keyword in FAMILY_KEYWORDS if keyword in lower_text)


def extract_risk_signals(text: str) -> dict[str, float]:
    nlp = _get_nlp()
    doc = nlp(text)

    org_count = sum(1 for ent in doc.ents if ent.label_ == "ORG")
    gpe_count = sum(1 for ent in doc.ents if ent.label_ == "GPE")

    has_email = bool(EMAIL_REGEX.search(text))
    has_phone = bool(PHONE_REGEX.search(text))
    has_job_keyword = _contains_any(text, JOB_KEYWORDS)
    has_travel_keyword = _contains_any(text, TRAVEL_KEYWORDS)
    family_hits = _count_family_hits(text)
    has_time_pattern = bool(TIME_REGEX.search(text))
    has_routine_word = _contains_any(text, ROUTINE_WORDS)

    contact = 1.0 if (has_email or has_phone) else 0.0

    corporate = 0.0
    if org_count >= 1:
        corporate = 0.5
    if org_count >= 1 and has_job_keyword:
        corporate = 1.0

    location = 0.0
    if gpe_count >= 1:
        location = 0.5
    if gpe_count >= 1 and has_travel_keyword:
        location = 1.0

    family = min(family_hits * 0.5, 1.0)

    routine = 0.0
    if has_time_pattern:
        routine = 0.5
    if has_time_pattern and has_routine_word:
        routine = 1.0

    return {
        "contact": contact,
        "corporate": corporate,
        "location": location,
        "family": family,
        "routine": routine,
    }
