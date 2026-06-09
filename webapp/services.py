"""Бизнес-логика поверх моделей: поиск и статистика.

Сервисы намеренно живут в отдельном файле — их крупный код удобно использовать как
учебную «зону конфликтов» при слиянии веток.
"""

from __future__ import annotations

from dataclasses import dataclass

from . import models


@dataclass
class SearchHit:
    note: models.Note
    score: float
    matched_in: str  # "title" | "body" | "tag"


@dataclass
class Stats:
    total_notes: int
    total_tags: int
    top_tags: list[tuple[str, int]]
    avg_body_length: float


def search_notes(query: str, limit: int = 25) -> list[SearchHit]:
    """Поиск по словам запроса: каждое слово ищется отдельно, score — доля совпавших слов."""
    query_norm = (query or "").strip().lower()
    if not query_norm:
        return []

    words = [w for w in query_norm.split() if w]
    if not words:
        return []

    notes = models.list_notes(limit=500)
    hits: list[SearchHit] = []
    for note in notes:
        title_l = note.title.lower()
        body_l = note.body.lower()
        tags_l = [t.lower() for t in note.tags]
        haystack = title_l + " " + body_l + " " + " ".join(tags_l)

        matched = sum(1 for w in words if w in haystack)
        if matched == 0:
            continue

        score = matched / len(words)
        matched_in = "title" if any(w in title_l for w in words) else "body"
        hits.append(SearchHit(note=note, score=score, matched_in=matched_in))

    hits.sort(key=lambda h: h.score, reverse=True)
    return hits[:limit]


def compute_stats() -> Stats:
    """Собрать сводную статистику по заметкам и тегам."""
    notes = models.list_notes(limit=10_000)
    total_notes = len(notes)
    total_tags = len({t for note in notes for t in note.tags})
    top_tags = models.list_tags_with_counts()[:5]
    avg_len = (sum(len(n.body) for n in notes) / total_notes) if total_notes else 0.0
    return Stats(
        total_notes=total_notes,
        total_tags=total_tags,
        top_tags=top_tags,
        avg_body_length=round(avg_len, 1),
    )
