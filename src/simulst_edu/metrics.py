from __future__ import annotations

from collections import Counter


def average_proportion(read_positions: list[int], source_length: int) -> float:
    if not read_positions or source_length <= 0:
        return 0.0
    return sum(read_positions) / (source_length * len(read_positions))


def average_lagging(read_positions: list[int], source_length: int) -> float:
    if not read_positions or source_length <= 0:
        return 0.0
    target_length = len(read_positions)
    gamma = target_length / source_length
    tau = target_length
    for index, consumed in enumerate(read_positions, start=1):
        if consumed >= source_length:
            tau = index
            break
    numerator = 0.0
    for index, consumed in enumerate(read_positions[:tau], start=1):
        numerator += consumed - ((index - 1) / gamma)
    return numerator / tau


def token_f1(reference: list[str], hypothesis: list[str]) -> float:
    if not reference and not hypothesis:
        return 1.0
    ref_counts = Counter(reference)
    hyp_counts = Counter(hypothesis)
    overlap = sum((ref_counts & hyp_counts).values())
    if overlap == 0:
        return 0.0
    precision = overlap / max(1, len(hypothesis))
    recall = overlap / max(1, len(reference))
    return 2 * precision * recall / (precision + recall)
