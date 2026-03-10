# Simultaneous Translation Text-to-Text Edu Repo

Educational repository for studying and implementing simultaneous text-to-text translation from scratch.

This repo is designed for three parallel goals:

- learn the problem formulation of simultaneous translation
- teach the latency-quality tradeoff with concrete policies
- build a small but complete PyTorch project that can be trained and inspected end to end

## Repo Structure

- `curriculum/syllabus.md`: learning roadmap for the full mini-course
- `curriculum/lesson_plans.md`: detailed teaching plans and classroom flow
- `docs/00_course_roadmap.md`: how to use the repo as a lecture series
- `docs/01_problem_setup.md`: formal problem definition and notation
- `docs/02_latency_metrics.md`: latency metrics such as AP and AL
- `docs/03_policy_design.md`: policy mechanisms for READ/WRITE control
- `docs/04_model_training.md`: from-scratch model and training pipeline
- `docs/05_project_practicum.md`: implementation walkthrough and extension ideas
- `src/simulst_edu/`: PyTorch code for toy simultaneous translation experiments
- `examples/compare_policies.py`: runnable script that trains a small model and compares policies
- `tests/`: sanity tests for metrics and policy behavior

## What This Project Is

This is an educational implementation, not a production simultaneous translation system.

It intentionally uses:

- a small synthetic dataset with controlled reordering
- a compact GRU + attention sequence-to-sequence model
- explicit policy objects for `READ` and `WRITE`

That keeps the code short enough to teach while still surfacing the real systems questions:

- when do we commit a target token?
- how much future source context do we need?
- what quality do we lose when we reduce latency?

## Learning Path

1. Read [docs/00_course_roadmap.md](/Users/admin/TuanDung/repos/simultaneous-translation-edu/docs/00_course_roadmap.md).
2. Work through [docs/01_problem_setup.md](/Users/admin/TuanDung/repos/simultaneous-translation-edu/docs/01_problem_setup.md) and [docs/02_latency_metrics.md](/Users/admin/TuanDung/repos/simultaneous-translation-edu/docs/02_latency_metrics.md).
3. Study [docs/03_policy_design.md](/Users/admin/TuanDung/repos/simultaneous-translation-edu/docs/03_policy_design.md).
4. Read the implementation note in [docs/04_model_training.md](/Users/admin/TuanDung/repos/simultaneous-translation-edu/docs/04_model_training.md).
5. Run the example script and compare policies on held-out samples.

## Included Policies

- `WaitKPolicy`: the classic fixed-lag baseline
- `FixedChunkPolicy`: read source in chunks, then flush a stable prefix
- `LocalAgreementPolicy`: only commit tokens that remain stable across successive prefixes
- `ConfidencePolicy`: commit only when the next-token probability exceeds a threshold

## Install

```bash
cd /Users/admin/TuanDung/repos/simultaneous-translation-edu
python3 -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
```

## Run

```bash
cd /Users/admin/TuanDung/repos/simultaneous-translation-edu
python examples/compare_policies.py
pytest
```

## Expected Outcomes

After working through the repo, you should be able to:

- explain simultaneous translation as a sequential decision problem
- distinguish policy-level control from model-level prediction
- reason about latency metrics instead of only offline accuracy
- implement and test new READ/WRITE policies on top of the same model

## Suggested Extensions

- replace the toy GRU with a transformer encoder-decoder
- train prefix-to-prefix rather than full-sentence only
- add differentiable or learned policies
- evaluate on a real monotonic translation benchmark
