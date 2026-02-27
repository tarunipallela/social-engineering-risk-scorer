RECOMMENDATION_MAP = {
    "contact": "Remove public email/phone",
    "corporate": "Avoid workplace disclosure",
    "location": "Avoid real-time travel posts",
    "family": "Limit identifiable family sharing",
    "routine": "Avoid predictable daily patterns",
}

ORDER = ["contact", "corporate", "location", "family", "routine"]


def get_recommendations(raw_scores: dict[str, float]) -> list[str]:
    return [RECOMMENDATION_MAP[key] for key in ORDER if raw_scores.get(key, 0) > 0]
