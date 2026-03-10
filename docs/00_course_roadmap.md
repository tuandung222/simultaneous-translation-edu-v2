# Course Roadmap

## Why This Topic Matters

Simultaneous translation sits at the intersection of sequence modeling, decision making, and systems constraints.

Offline translation asks:

- given the full source sentence, what is the best target sentence?

Simultaneous translation asks:

- while the source is still arriving, when is it safe enough to start speaking?
- how much future context should we wait for?
- what quality loss is acceptable for lower latency?

This makes the problem excellent for teaching because it forces students to think beyond pure model accuracy.

## The Teaching Arc

This repo uses a deliberate progression:

1. Formalize the task.
2. Learn the latency metrics.
3. Study several policies.
4. Implement a compact model.
5. Run end-to-end experiments.
6. Discuss where real research systems go further.

## What Students Will Build

By the end of the series, students will have:

- a working PyTorch implementation of a small text-to-text model
- a simultaneous decoding runner
- multiple READ/WRITE policies
- a metric pipeline for quality and latency
- a concrete base for future research extensions

## Why The Repo Uses Synthetic Data

Real simultaneous translation systems are complex. They usually involve:

- large corpora
- subword tokenization
- transformer variants
- prefix training objectives
- sophisticated latency-aware search

That is too much for a first educational repository.

Instead, this repo uses a synthetic bilingual grammar where:

- source and target share enough regularity to learn quickly
- some target words depend on future source context
- reordering exists, so low-latency policies can fail in visible ways

This means the educational signal remains high even though the benchmark is small.

## Suggested Teaching Rhythm

For each lecture:

1. start from one sentence-level example
2. abstract to notation
3. map notation to code
4. run a small experiment
5. ask students to interpret the result

The key habit to reinforce is this:

Do not ask only "is the translation correct?"

Also ask:

- when was each token emitted?
- what source evidence existed at that moment?
- could a better policy have delayed less or committed later?

## Course Output

The repo can support:

- a self-study reading sequence
- a lab-based mini-course
- lecture slides and live coding sessions
- a capstone where students add new policies
