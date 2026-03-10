# Lesson Plans

## Lecture 1. Problem Framing

### Teaching objective

Students should understand simultaneous translation as a control problem layered on top of sequence generation.

### Session flow

1. Warm-up: contrast subtitle generation with offline translation.
2. Define source stream `x_1, x_2, ..., x_n`.
3. Define target stream `y_1, y_2, ..., y_m`.
4. Introduce actions:
   - `READ`: wait for one more source token
   - `WRITE`: commit one target token
5. Show why premature commitment is irreversible.
6. Discuss two failure modes:
   - low latency but hallucinated output
   - high quality but unacceptable delay

### Board plan

- draw a timeline with source arrivals
- mark the exact source position used to emit each target token
- ask where a policy should wait in a reordering example

### In-class exercise

Give students a sentence where the object appears late in the source but early in the target. Ask them to manually simulate `wait-1`, `wait-3`, and offline decoding.

### Homework

Read [docs/01_problem_setup.md](/Users/admin/TuanDung/repos/simultaneous-translation-edu/docs/01_problem_setup.md) and summarize the role of `g(t)`.

## Lecture 2. Metrics and Tradeoffs

### Teaching objective

Students should compute latency numerically rather than reason only by intuition.

### Session flow

1. Review `g(t)`: how many source tokens were consumed when target token `t` was emitted.
2. Derive AP.
3. Derive AL and explain why it references an ideal policy with constant slope.
4. Show two traces with the same final translation but different latency.
5. Discuss metric blind spots.

### In-class exercise

Provide a small emission trace and ask students to compute AP and AL by hand.

### Homework

Read [docs/02_latency_metrics.md](/Users/admin/TuanDung/repos/simultaneous-translation-edu/docs/02_latency_metrics.md) and verify the formulas against the example trace.

## Lecture 3. Policy Design

### Teaching objective

Students should differentiate between model uncertainty and policy conservatism.

### Session flow

1. Fixed policies:
   - wait-k
   - chunked read
2. Adaptive policies:
   - local agreement
   - confidence thresholding
3. Compare information requirements:
   - source position only
   - source position plus hypothesis stability
   - source position plus token confidence
4. Show why local agreement can be conservative but robust.

### In-class demo

Run the same prefix sequence through several policies and display token commits.

### Homework

Read [docs/03_policy_design.md](/Users/admin/TuanDung/repos/simultaneous-translation-edu/docs/03_policy_design.md). Write one paragraph on when confidence thresholding can fail.

## Lecture 4. Model Design

### Teaching objective

Students should understand why the repo's model is intentionally small and inspectable.

### Session flow

1. Synthetic dataset with delayed target dependencies
2. Source and target vocabularies
3. Unidirectional encoder
4. Additive attention
5. Decoder with teacher forcing
6. Prefix decoding mismatch: train full sentence, test on partial source

### Whiteboard focus

- tensor shapes for encoder outputs
- attention score computation
- why partial-source decoding is inherently distribution-shifted

### Homework

Read [docs/04_model_training.md](/Users/admin/TuanDung/repos/simultaneous-translation-edu/docs/04_model_training.md) and annotate the training loop.

## Lecture 5. Implementation Practicum

### Teaching objective

Students should be able to extend the code without breaking the evaluation loop.

### Session flow

1. Walk through data generation
2. Build vocabularies
3. Train the model
4. Run simultaneous decoding
5. Log quality and latency metrics
6. Compare trajectories

### Lab task

Implement a new policy with one extra internal state variable and test it.

### Homework

Complete [docs/05_project_practicum.md](/Users/admin/TuanDung/repos/simultaneous-translation-edu/docs/05_project_practicum.md) exercises.

## Lecture 6. Beyond the Baseline

### Teaching objective

Students should understand where the toy project stops being enough.

### Session flow

1. Prefix-to-prefix training objectives
2. Learned agents versus hand-designed policies
3. Beam search in streaming settings
4. Real benchmark considerations
5. Relation to speech translation and online ASR

### Final assignment

Produce a short report comparing two policies, one model limitation, and one extension proposal.
