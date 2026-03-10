from __future__ import annotations

from simulst_edu.data import generate_examples
from simulst_edu.decoding import run_simultaneous_decoding
from simulst_edu.metrics import average_lagging, average_proportion, token_f1
from simulst_edu.policies import (
    ConfidencePolicy,
    FixedChunkPolicy,
    LocalAgreementPolicy,
    WaitKPolicy,
)
from simulst_edu.train import TrainingConfig, train_model


def main() -> None:
    train_examples = generate_examples(800, seed=7)
    valid_examples = generate_examples(120, seed=8)
    test_examples = generate_examples(4, seed=9)

    model, source_vocab, target_vocab = train_model(
        train_examples,
        valid_examples,
        TrainingConfig(epochs=6, batch_size=32, learning_rate=3e-3),
    )

    policies = [
        WaitKPolicy(k=2),
        FixedChunkPolicy(chunk_size=2),
        LocalAgreementPolicy(),
        ConfidencePolicy(threshold=0.82),
    ]

    for example in test_examples:
        print("=" * 80)
        print("SRC:", " ".join(example.source_tokens))
        print("REF:", " ".join(example.target_tokens))
        for policy in policies:
            result = run_simultaneous_decoding(
                model,
                source_vocab,
                target_vocab,
                list(example.source_tokens),
                list(example.target_tokens),
                policy,
            )
            ap = average_proportion(result.read_positions, len(result.source_tokens))
            al = average_lagging(result.read_positions, len(result.source_tokens))
            f1 = token_f1(result.reference_tokens, result.predicted_tokens)
            print(
                f"{policy.name:>16} | pred={' '.join(result.predicted_tokens):<32} "
                f"| AP={ap:.3f} AL={al:.3f} F1={f1:.3f}"
            )
            print(f"{'':>16} | read_positions={result.read_positions}")
            print(f"{'':>16} | actions={' '.join(result.action_trace)}")


if __name__ == "__main__":
    main()
