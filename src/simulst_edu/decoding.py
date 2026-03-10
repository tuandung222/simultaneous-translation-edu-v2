from __future__ import annotations

from dataclasses import dataclass

import torch

from .policies import PolicyContext, SimultaneousPolicy
from .vocab import Vocab


@dataclass
class SimultaneousResult:
    source_tokens: list[str]
    reference_tokens: list[str]
    predicted_tokens: list[str]
    read_positions: list[int]
    action_trace: list[str]


def run_simultaneous_decoding(
    model,
    source_vocab: Vocab,
    target_vocab: Vocab,
    source_tokens: list[str] | tuple[str, ...],
    reference_tokens: list[str] | tuple[str, ...],
    policy: SimultaneousPolicy,
    *,
    device: str = "cpu",
    max_target_len: int = 24,
) -> SimultaneousResult:
    policy.reset()
    source_tokens = list(source_tokens)
    reference_tokens = list(reference_tokens)

    consumed_source = 0
    committed_target: list[int] = []
    read_positions: list[int] = []
    action_trace: list[str] = []
    max_steps = (len(source_tokens) + max_target_len) * 4
    observed_prefix = -1

    for _ in range(max_steps):
        source_finished = consumed_source >= len(source_tokens)
        if consumed_source == 0:
            action_trace.append("READ")
            consumed_source += 1
            continue

        visible_source = source_tokens[:consumed_source]
        source_ids = source_vocab.encode(visible_source, add_eos=source_finished)
        source_tensor = torch.tensor([source_ids], dtype=torch.long, device=device)
        hypothesis, confidences = model.greedy_decode(
            source_tensor,
            bos_id=target_vocab.bos_id,
            eos_id=target_vocab.eos_id,
            max_len=max_target_len,
        )

        context = PolicyContext(
            source_length=len(source_tokens),
            consumed_source=consumed_source,
            committed_target=committed_target,
            hypothesis=hypothesis,
            confidences=confidences,
            source_finished=source_finished,
            eos_id=target_vocab.eos_id,
        )

        if consumed_source != observed_prefix:
            policy.observe(context)
            observed_prefix = consumed_source

        next_action = policy.decide(context)
        next_index = len(committed_target)

        if next_action == "WRITE" and next_index < len(hypothesis):
            next_token = hypothesis[next_index]
            if next_token == target_vocab.eos_id and not source_finished:
                next_action = "READ"
            else:
                committed_target.append(next_token)
                action_trace.append("WRITE")
                if next_token != target_vocab.eos_id:
                    read_positions.append(consumed_source)
                else:
                    break
                continue

        if source_finished:
            if next_index < len(hypothesis):
                next_token = hypothesis[next_index]
                committed_target.append(next_token)
                action_trace.append("WRITE")
                if next_token != target_vocab.eos_id:
                    read_positions.append(consumed_source)
                    continue
                break
            break

        action_trace.append("READ")
        consumed_source += 1

    predicted_tokens = target_vocab.decode(committed_target, skip_specials=True)
    return SimultaneousResult(
        source_tokens=source_tokens,
        reference_tokens=reference_tokens,
        predicted_tokens=predicted_tokens,
        read_positions=read_positions,
        action_trace=action_trace,
    )
