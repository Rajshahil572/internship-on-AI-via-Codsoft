<<<<<<< HEAD
=======
"""Tiny user-based collaborative filtering demo."""

from __future__ import annotations

import math
from collections.abc import Mapping

Ratings = dict[str, dict[str, float]]


def cosine_similarity(a: Mapping[str, float], b: Mapping[str, float]) -> float:
    """Return cosine similarity using overlapping keys only."""
    common = set(a).intersection(b)
    if not common:
        return 0.0
    dot = sum(a[item] * b[item] for item in common)
    norm_a = math.sqrt(sum(a[item] ** 2 for item in common))
    norm_b = math.sqrt(sum(b[item] ** 2 for item in common))
    if not norm_a or not norm_b:
        return 0.0
    return dot / (norm_a * norm_b)


def recommend(user: str, ratings: Ratings, limit: int = 5) -> list[tuple[str, float]]:
    """Recommend unrated items to `user` based on similar users."""
    if user not in ratings:
        raise KeyError(f"Unknown user: {user}")

    totals: dict[str, float] = {}
    sim_sums: dict[str, float] = {}
    target_profile = ratings[user]

    for other, profile in ratings.items():
        if other == user:
            continue
        similarity = cosine_similarity(target_profile, profile)
        if similarity <= 0:
            continue
        for item, score in profile.items():
            if item in target_profile:
                continue
            totals[item] = totals.get(item, 0.0) + score * similarity
            sim_sums[item] = sim_sums.get(item, 0.0) + similarity

    scores = [
        (item, totals[item] / sim_sums[item])
        for item in totals
        if sim_sums[item]
    ]
    scores.sort(key=lambda pair: pair[1], reverse=True)
    return scores[:limit]


def main() -> None:
    sample_ratings: Ratings = {
        "Alice": {"Inception": 4.5, "Interstellar": 4.0, "The Martian": 4.5},
        "Bob": {"Inception": 5.0, "Arrival": 4.0, "Gravity": 3.5},
        "Cara": {"Interstellar": 4.0, "Arrival": 4.5, "The Martian": 4.0},
        "Dan": {"Inception": 4.0, "Gravity": 4.5, "Blade Runner": 4.0},
        "Eve": {"Arrival": 5.0, "Blade Runner": 4.5, "The Martian": 3.5},
    }

    user = "Alice"
    suggestions = recommend(user, sample_ratings, limit=3)
    print(f"Top picks for {user}:")
    if not suggestions:
        print("  No new items to recommend.")
    for item, score in suggestions:
        print(f"  {item} (predicted rating: {score:.2f})")


if __name__ == "__main__":
    main()
>>>>>>> 2d6b991 (Add collaborative filtering recommendation demo)

