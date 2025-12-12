"""Location normalization and leveling for geo-aware searches."""

from __future__ import annotations

import re
from typing import Dict, Optional, Tuple

ALIASES = {
    "hcm": "Ho Chi Minh City",
    "hcmc": "Ho Chi Minh City",
    "sai gon": "Ho Chi Minh City",
    "saigon": "Ho Chi Minh City",
    "sg": "Ho Chi Minh City",
    "ho chi minh": "Ho Chi Minh City",
    "ho chi minh city": "Ho Chi Minh City",
    "hn": "Hanoi",
    "ha noi": "Hanoi",
    "ha noi city": "Hanoi",
    "hanoi": "Hanoi",
}

COUNTRIES = {"vietnam", "viet nam", "usa", "united states", "united states of america"}


def normalize_location(raw: Optional[str]) -> Optional[Dict[str, object]]:
    """Normalize a free-form location into components and a normalized string."""
    if not raw or not str(raw).strip():
        return None
    text = " ".join(str(raw).replace(",", " , ").split()).strip(" ,")
    lowered = text.lower()
    if lowered in ALIASES:
        text = ALIASES[lowered]
    parts = [p.strip(" ,") for p in text.split(",") if p.strip(" ,")]

    components: Dict[str, Optional[str]] = {
        "country": None,
        "region": None,
        "city": None,
        "district": None,
        "commune": None,
    }

    country = None
    for token in list(parts)[::-1]:
        if token.lower() in COUNTRIES:
            country = _title(token)
            parts.remove(token)
            break

    if len(parts) >= 3:
        components["commune"] = _clean_part(parts[0])
        components["district"] = _clean_part(parts[1])
        components["city"] = _clean_part(parts[2])
        level = "commune"
    elif len(parts) == 2:
        components["district"] = _clean_part(parts[0])
        components["city"] = _clean_part(parts[1])
        level = "district"
    elif len(parts) == 1:
        components["city"] = _clean_part(parts[0])
        level = "city"
    else:
        level = "unknown"

    if not country:
        # Default country guess if city hints at Vietnam
        if components["city"] and "ho chi minh" in components["city"].lower():
            country = "Vietnam"
        elif components["city"] and "hanoi" in components["city"].lower():
            country = "Vietnam"
    components["country"] = country
    normalized_parts = [
        p for p in [components["commune"], components["district"], components["city"], components["country"]] if p
    ]
    normalized = ", ".join(normalized_parts) if normalized_parts else text
    return {
        "raw": raw,
        "normalized": normalized,
        "level": level,
        "components": components,
        "coords": {"lat": None, "lng": None},
    }


def _clean_part(value: str) -> str:
    val = value.strip()
    val = re.sub(r"\b(district|quan|quận|huyen|huyện|ward|phường|commune|xa|xã|tp\.?|thành phố)\b", "", val, flags=re.I)
    return _title(val.strip(" ,.-"))


def _title(value: str) -> str:
    return " ".join(token.capitalize() if token else "" for token in value.split())
