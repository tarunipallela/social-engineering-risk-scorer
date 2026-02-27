import re

EMAIL_REGEX = re.compile(r"[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+")
PHONE_REGEX = re.compile(r"(?:\+?\d{1,2}[\s.-]?)?(?:\(?\d{3}\)?[\s.-]?)\d{3}[\s.-]?\d{4}")
TIME_REGEX = re.compile(r"\b\d{1,2}(am|pm)\b", re.IGNORECASE)

JOB_KEYWORDS = {
    "engineer",
    "manager",
    "director",
    "developer",
    "analyst",
    "intern",
    "ceo",
    "cto",
    "founder",
    "employee",
    "work",
    "job",
    "office",
}

TRAVEL_KEYWORDS = {
    "travel",
    "flying",
    "flight",
    "airport",
    "trip",
    "vacation",
    "heading to",
    "going to",
    "arriving",
    "departing",
}

FAMILY_KEYWORDS = {
    "mom",
    "dad",
    "sister",
    "brother",
    "wife",
    "husband",
    "parents",
    "kids",
}

ROUTINE_WORDS = {
    "daily",
    "every day",
    "morning routine",
    "nightly",
    "every morning",
}
