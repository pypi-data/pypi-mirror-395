"""Search strategies: query builders and source-specific routines."""

from __future__ import annotations

from typing import List

from .models import SearchRequest, StrategyStep
from .location_normalizer import normalize_location

def _segment_key(source: str, query: str, location: str | None, page: int) -> str:
    parts = [source]
    if location:
        parts.append(location)
    parts.append(query)
    parts.append(f"p{page}")
    return "|".join(parts)


def build_strategies(request: SearchRequest) -> List[StrategyStep]:
    """Dispatch to source-specific strategy builders."""
    steps: List[StrategyStep] = []
    for source in request.sources:
        if source.lower() in {"google_maps", "maps", "google-maps"}:
            steps.extend(build_google_maps_strategies(request))
    return steps


def build_google_maps_strategies(request: SearchRequest) -> List[StrategyStep]:
    """Create strategy steps for Google Maps search."""
    steps: List[StrategyStep] = []
    if not request.keywords:
        return steps

    locations = request.locations or [None]
    max_pages = max(1, request.pages_per_source)

    for kw in request.keywords:
        for loc in locations:
            geo = normalize_location(loc) if loc else None
            loc_norm = geo.get("normalized") if geo else loc
            query = kw if not loc_norm else f"{kw} {loc_norm}"
            for page in range(1, max_pages + 1):
                seg_key = _segment_key("google_maps", query, loc, page)
                steps.append(
                    StrategyStep(
                        source="google_maps",
                        query=query,
                        location=loc_norm or loc,
                        location_norm=loc_norm or loc,
                        geo_json=geo,
                        page=page,
                        max_pages=max_pages,
                        throttle_seconds=1.5,
                        parser_hint="maps_listing",
                        step_id=seg_key,
                    )
                )
    return steps
