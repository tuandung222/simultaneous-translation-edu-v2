# Policy Design

## 1. The Separation of Concerns

The model answers:

- "Given this source prefix, what target tokens seem plausible?"

The policy answers:

- "Is the next token stable enough to emit now?"

This separation is crucial. A stronger model does not remove the need for a policy. It only changes what evidence the policy can use.

## 2. Wait-k

### Rule

Read `k` source tokens first. Then, for target step `t`, emit only after consuming:

`g(t) = min(k + t - 1, n)`

### Strengths

- simple
- easy to analyze
- strong baseline in research discussions

### Weaknesses

- cannot adapt to sentence difficulty
- may emit too early on reorder-heavy examples
- may wait too long on easy monotonic examples

## 3. Fixed Chunk Policy

### Rule

Read source in chunks of size `c`. After each chunk boundary, commit as much of the current hypothesis as is unlocked by that prefix.

### Strengths

- closer to mini-batch thinking in systems
- fewer control decisions
- easy to visualize

### Weaknesses

- emission becomes bursty
- chunk size is coarse and task dependent

## 4. Local Agreement

### Rule

After each new source token or chunk, decode the current prefix again. Commit only the longest prefix that matches the previous hypothesis.

### Intuition

If the first few target tokens remain unchanged even after more source arrives, they are likely stable enough to emit.

### Strengths

- robust to local hypothesis instability
- uses agreement rather than only position

### Weaknesses

- can be overly conservative
- requires repeated decoding of source prefixes

## 5. Confidence Thresholding

### Rule

Emit the next target token only if the model assigns it probability above a threshold `p`.

### Strengths

- adaptive to model uncertainty
- simple to combine with greedy decoding

### Weaknesses

- token probability can be miscalibrated
- high local confidence does not guarantee sequence-level stability
- may still fail badly under reordering

## 6. Policy Comparison Table

| Policy | Main signal | Main advantage | Main failure mode |
| --- | --- | --- | --- |
| Wait-k | source position | simple fixed lag | cannot adapt |
| Fixed chunk | chunk boundary | easy systems behavior | bursty commits |
| Local agreement | hypothesis stability | safer commits | can wait too long |
| Confidence | next-token probability | adaptive | calibration errors |

## 7. What The Repo Implements

The codebase implements all four of these policies through a shared interface:

- `observe(context)`: update internal state after a new source prefix is available
- `decide(context)`: return `READ` or `WRITE`

That makes it straightforward to plug a new policy into the same runner and compare it fairly.

## 8. Design Principle For Students

When inventing a new policy, state explicitly:

- what information it uses
- what internal state it stores
- when it becomes more aggressive
- when it becomes more conservative

If you cannot explain those four points cleanly, the policy design is probably still vague.
