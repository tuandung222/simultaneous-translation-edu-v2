# Syllabus: Simultaneous Translation Text-to-Text

## Course Goal

Build enough conceptual and implementation depth to teach, discuss, and code a small simultaneous translation system from scratch.

## Audience

- learners who already know basic deep learning
- readers who know sequence-to-sequence models at a high level
- practitioners who want a compact path from theory to runnable code

## Prerequisites

- Python and basic PyTorch
- embeddings, RNNs, attention, and teacher forcing
- tokenization and padding
- basic evaluation mindset for sequence generation

## Course Format

Six lectures, each designed for 90 to 120 minutes.

## Lecture Sequence

### Lecture 1. Problem Framing

- What simultaneous translation is and why it is hard
- Difference between offline translation and online translation
- READ/WRITE action view
- Prefix-to-prefix intuition

Deliverable:

- learners can formalize the task and explain the latency-quality tradeoff

### Lecture 2. Metrics and Tradeoffs

- Why BLEU alone is insufficient
- Average Proportion (AP)
- Average Lagging (AL)
- Interpreting latency traces

Deliverable:

- learners can compute and interpret latency metrics from a token emission trace

### Lecture 3. Policy Design

- Fixed policies versus adaptive policies
- Wait-k
- Chunk-based policies
- Local agreement
- Confidence-based policies

Deliverable:

- learners can describe what information each policy uses and what it sacrifices

### Lecture 4. Model Design for the Repo

- Why the repo uses a toy but complete sequence-to-sequence model
- Synthetic data with controlled reorderings
- Encoder, decoder, attention
- Prefix decoding under partial source observation

Deliverable:

- learners can map theory to concrete PyTorch modules

### Lecture 5. Implementation Practicum

- Training loop
- Greedy decoding on prefixes
- Plugging policies into a shared runner
- Measuring quality and latency side by side

Deliverable:

- learners can run experiments and modify the code safely

### Lecture 6. Beyond the Baseline

- Prefix training versus full-sentence training
- Learned policies
- Simultaneous speech translation parallels
- Research directions and reading list

Deliverable:

- learners can position the toy project relative to real research systems

## Assessment Ideas

- coding exercise: implement one new policy
- analysis exercise: compare two policies on the same sentence and explain the trace
- essay exercise: argue when a latency reduction is worth the quality loss

## Repository-Based Milestones

1. Read all docs and reproduce the example run.
2. Change the synthetic grammar and inspect policy behavior.
3. Implement one additional adaptive policy.
4. Replace the GRU with a transformer baseline.
