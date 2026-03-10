from __future__ import annotations

from dataclasses import dataclass, field


@dataclass
class PolicyContext:
    source_length: int
    consumed_source: int
    committed_target: list[int]
    hypothesis: list[int]
    confidences: list[float]
    source_finished: bool
    eos_id: int


def longest_common_prefix_length(left: list[int], right: list[int]) -> int:
    count = 0
    for left_item, right_item in zip(left, right):
        if left_item != right_item:
            break
        count += 1
    return count


@dataclass
class SimultaneousPolicy:
    name: str = "base"

    def reset(self) -> None:
        pass

    def observe(self, context: PolicyContext) -> None:
        pass

    def decide(self, context: PolicyContext) -> str:
        raise NotImplementedError


@dataclass
class WaitKPolicy(SimultaneousPolicy):
    k: int = 3
    name: str = field(init=False, default="wait-k")

    def decide(self, context: PolicyContext) -> str:
        next_target_index = len(context.committed_target) + 1
        required_source = min(context.source_length, self.k + next_target_index - 1)
        if context.consumed_source >= required_source:
            return "WRITE"
        return "READ"


@dataclass
class FixedChunkPolicy(SimultaneousPolicy):
    chunk_size: int = 2
    unlocked_prefix: int = 0
    last_observed_source: int = -1
    name: str = field(init=False, default="fixed-chunk")

    def reset(self) -> None:
        self.unlocked_prefix = 0
        self.last_observed_source = -1

    def observe(self, context: PolicyContext) -> None:
        if context.consumed_source == self.last_observed_source:
            return
        self.last_observed_source = context.consumed_source
        if (
            context.source_finished
            or context.consumed_source % self.chunk_size == 0
            or context.consumed_source == context.source_length
        ):
            self.unlocked_prefix = len(context.hypothesis)

    def decide(self, context: PolicyContext) -> str:
        if len(context.committed_target) < self.unlocked_prefix:
            return "WRITE"
        return "READ"


@dataclass
class LocalAgreementPolicy(SimultaneousPolicy):
    last_hypothesis: list[int] = field(default_factory=list)
    unlocked_prefix: int = 0
    last_observed_source: int = -1
    name: str = field(init=False, default="local-agreement")

    def reset(self) -> None:
        self.last_hypothesis = []
        self.unlocked_prefix = 0
        self.last_observed_source = -1

    def observe(self, context: PolicyContext) -> None:
        if context.consumed_source == self.last_observed_source:
            return
        self.last_observed_source = context.consumed_source
        if not self.last_hypothesis:
            self.last_hypothesis = list(context.hypothesis)
            if context.source_finished:
                self.unlocked_prefix = len(context.hypothesis)
            return
        agreed = longest_common_prefix_length(self.last_hypothesis, context.hypothesis)
        self.unlocked_prefix = max(self.unlocked_prefix, agreed)
        self.last_hypothesis = list(context.hypothesis)
        if context.source_finished:
            self.unlocked_prefix = len(context.hypothesis)

    def decide(self, context: PolicyContext) -> str:
        if len(context.committed_target) < self.unlocked_prefix:
            return "WRITE"
        return "READ"


@dataclass
class ConfidencePolicy(SimultaneousPolicy):
    threshold: float = 0.8
    name: str = field(init=False, default="confidence")

    def decide(self, context: PolicyContext) -> str:
        next_index = len(context.committed_target)
        if next_index >= len(context.hypothesis):
            return "READ"
        if context.source_finished:
            return "WRITE"
        next_token = context.hypothesis[next_index]
        next_confidence = context.confidences[next_index]
        if next_token == context.eos_id:
            return "READ"
        if next_confidence >= self.threshold:
            return "WRITE"
        return "READ"
