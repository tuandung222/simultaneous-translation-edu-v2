from __future__ import annotations

from dataclasses import dataclass
from random import Random


@dataclass(frozen=True)
class Example:
    source_tokens: tuple[str, ...]
    target_tokens: tuple[str, ...]


SUBJECTS = {
    "i": "mi",
    "you": "tu",
    "we": "nos",
    "they": "tes",
}

VERBS = {
    "eat": "essen",
    "see": "sehen",
    "buy": "kaufen",
    "carry": "tragen",
    "like": "mogen",
}

OBJECTS = {
    "apple": "apfel",
    "bread": "brot",
    "book": "buch",
    "flowers": "blumen",
    "music": "musik",
}

ADJECTIVES = {
    "red": "rot",
    "fresh": "frisch",
    "small": "klein",
    "heavy": "schwer",
}

TIME_WORDS = {
    "today": "heute",
    "now": "jetzt",
    "nightly": "nachts",
}


def _negated(verb: str, negated: bool) -> str:
    return f"neg_{verb}" if negated else verb


def generate_examples(num_examples: int, seed: int = 0) -> list[Example]:
    rng = Random(seed)
    subjects = list(SUBJECTS.items())
    verbs = list(VERBS.items())
    objects = list(OBJECTS.items())
    adjectives = list(ADJECTIVES.items())
    times = list(TIME_WORDS.items())

    examples: list[Example] = []
    for _ in range(num_examples):
        src_subject, tgt_subject = rng.choice(subjects)
        src_verb, tgt_verb = rng.choice(verbs)
        src_object, tgt_object = rng.choice(objects)

        use_adjective = rng.random() < 0.55
        use_time = rng.random() < 0.45
        negated = rng.random() < 0.3

        source = [src_subject]
        if negated:
            source.append("not")
        source.append(src_verb)

        target = [tgt_subject, tgt_object]

        if use_adjective:
            src_adj, tgt_adj = rng.choice(adjectives)
            source.append(src_adj)
            target.append(tgt_adj)

        source.append(src_object)

        if use_time:
            src_time, tgt_time = rng.choice(times)
            source.append(src_time)
            target.append(tgt_time)

        target.append(_negated(tgt_verb, negated))
        examples.append(Example(tuple(source), tuple(target)))

    return examples
