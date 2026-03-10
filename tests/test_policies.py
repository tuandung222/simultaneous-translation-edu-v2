from simulst_edu.policies import (
    ConfidencePolicy,
    FixedChunkPolicy,
    LocalAgreementPolicy,
    PolicyContext,
    WaitKPolicy,
)


def make_context(
    *,
    source_length: int = 5,
    consumed_source: int = 2,
    committed_target: list[int] | None = None,
    hypothesis: list[int] | None = None,
    confidences: list[float] | None = None,
    source_finished: bool = False,
    eos_id: int = 2,
) -> PolicyContext:
    return PolicyContext(
        source_length=source_length,
        consumed_source=consumed_source,
        committed_target=committed_target or [],
        hypothesis=hypothesis or [10, 11, eos_id],
        confidences=confidences or [0.95, 0.92, 0.99],
        source_finished=source_finished,
        eos_id=eos_id,
    )


def test_wait_k_reads_until_required_source_is_available() -> None:
    policy = WaitKPolicy(k=3)
    assert policy.decide(make_context(consumed_source=2, committed_target=[])) == "READ"
    assert policy.decide(make_context(consumed_source=3, committed_target=[])) == "WRITE"


def test_fixed_chunk_unlocks_only_on_chunk_boundary() -> None:
    policy = FixedChunkPolicy(chunk_size=2)
    context = make_context(consumed_source=1, hypothesis=[10, 11, 2])
    policy.observe(context)
    assert policy.decide(context) == "READ"

    context = make_context(consumed_source=2, hypothesis=[10, 11, 2])
    policy.observe(context)
    assert policy.decide(context) == "WRITE"


def test_local_agreement_unlocks_common_prefix() -> None:
    policy = LocalAgreementPolicy()
    first = make_context(consumed_source=2, hypothesis=[10, 12, 2])
    second = make_context(consumed_source=3, hypothesis=[10, 13, 2])
    policy.observe(first)
    assert policy.decide(first) == "READ"
    policy.observe(second)
    assert policy.decide(second) == "WRITE"


def test_confidence_policy_blocks_low_confidence_tokens() -> None:
    policy = ConfidencePolicy(threshold=0.8)
    low_conf = make_context(confidences=[0.6, 0.95, 0.99])
    high_conf = make_context(confidences=[0.9, 0.95, 0.99])
    assert policy.decide(low_conf) == "READ"
    assert policy.decide(high_conf) == "WRITE"
