# ==========================================================
# Advanced Semantic + Context-Aware Detection Engine
# Returns normalized raw scores (0.0 – 1.0)
# ==========================================================

import re
import spacy
from typing import Dict

nlp = spacy.load("en_core_web_sm")


# ==========================================================
# Phrase Dictionaries
# ==========================================================

CONTACT_INTENT = [
    "call me",
    "reach me",
    "text me",
    "dm me",
    "contact me",
]

JOB_INTENT = [
    "work at",
    "employee at",
    "manager at",
    "intern at",
    "working in",
]

RESIDENCE_INTENT = [
    "live in",
    "based in",
    "from",
    "residing in",
    "staying at",
]

FAMILY_BASE_PATTERNS = [
    "my daughter",
    "my son",
    "my husband",
    "my wife",
    "my kids",
    "my parents",
]

FAMILY_VULNERABILITY_PATTERNS = [
    "family alone",
    "kids alone",
    "children alone",
    "home alone",
]

TIME_WORDS = [
    "today",
    "tomorrow",
    "tonight",
    "daily",
    "every day",
    "every week",
    "every month",
]

TRAVEL_VERBS = [
    "travel",
    "go",
    "leave",
    "visit",
    "fly",
    "commute",
    "relocate",
    "board",
]


# ==========================================================
# 1️⃣ CONTACT DETECTION
# ==========================================================

def detect_contact(text: str, doc) -> float:
    score = 0.0
    text_lower = text.lower()

    email_pattern = r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+"
    phone_pattern = r"\b(\+?\d{1,3}[- ]?)?\d{10}\b"

    email_found = bool(re.search(email_pattern, text))
    phone_found = bool(re.search(phone_pattern, text))
    intent_found = any(phrase in text_lower for phrase in CONTACT_INTENT)

    if email_found or phone_found:
        score += 0.6

    if intent_found:
        score += 0.4

    return min(score, 1.0)


# ==========================================================
# 2️⃣ CORPORATE DETECTION
# ==========================================================

def detect_corporate(text: str, doc) -> float:
    score = 0.0
    text_lower = text.lower()

    org_found = any(ent.label_ == "ORG" for ent in doc.ents)
    job_intent_found = any(phrase in text_lower for phrase in JOB_INTENT)

    if org_found:
        score += 0.5

    if job_intent_found:
        score += 0.5

    return min(score, 1.0)


# ==========================================================
# 3️⃣ LOCATION DETECTION
# ==========================================================

def detect_location(text: str, doc) -> float:
    score = 0.0
    text_lower = text.lower()

    location_found = any(ent.label_ in ["GPE", "LOC"] for ent in doc.ents)
    residence_intent_found = any(phrase in text_lower for phrase in RESIDENCE_INTENT)

    if location_found:
        score += 0.5

    if residence_intent_found:
        score += 0.5

    return min(score, 1.0)


# ==========================================================
# 4️⃣ FAMILY DETECTION (Upgraded)
# ==========================================================

def detect_family(text: str) -> float:
    text_lower = text.lower()

    if any(pattern in text_lower for pattern in FAMILY_VULNERABILITY_PATTERNS):
        return 1.0  # High vulnerability

    if any(pattern in text_lower for pattern in FAMILY_BASE_PATTERNS):
        return 0.7  # Normal family disclosure

    return 0.0


# ==========================================================
# 5️⃣ ROUTINE / PREDICTABILITY DETECTION (Upgraded)
# ==========================================================

def detect_routine(text: str, doc) -> float:
    score = 0.0
    text_lower = text.lower()

    lemmas = [token.lemma_.lower() for token in doc]

    travel_found = any(verb in lemmas for verb in TRAVEL_VERBS)
    location_found = any(ent.label_ in ["GPE", "LOC"] for ent in doc.ents)

    time_words_found = any(word in text_lower for word in TIME_WORDS)

    # Regex time detection (5AM, 7pm, 10:30am)
    time_regex = r"\b\d{1,2}(:\d{2})?\s?(am|pm)\b"
    time_pattern_found = bool(re.search(time_regex, text_lower))

    # Duration detection (10 days, 2 weeks, etc.)
    duration_regex = r"\b\d+\s?(day|days|week|weeks|month|months)\b"
    duration_found = bool(re.search(duration_regex, text_lower))

    # Leaving home detection
    leaving_home_found = "leave home" in text_lower or "leaving home" in text_lower

    if travel_found:
        score += 0.3

    if location_found:
        score += 0.2

    if time_words_found or time_pattern_found:
        score += 0.2

    if duration_found:
        score += 0.2

    if leaving_home_found:
        score += 0.2

    return min(score, 1.0)


# ==========================================================
# MASTER FUNCTION
# ==========================================================

def analyze_semantics(text: str) -> Dict[str, float]:

    if not text.strip():
        return {
            "contact": 0.0,
            "corporate": 0.0,
            "location": 0.0,
            "family": 0.0,
            "routine": 0.0,
        }

    doc = nlp(text)

    return {
        "contact": detect_contact(text, doc),
        "corporate": detect_corporate(text, doc),
        "location": detect_location(text, doc),
        "family": detect_family(text),
        "routine": detect_routine(text, doc),
    }