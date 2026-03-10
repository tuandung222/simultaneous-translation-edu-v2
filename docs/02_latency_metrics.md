# Latency Metrics

## 1. Why We Need More Than Translation Accuracy

In simultaneous translation, a model that produces the right final sentence too late may still be unusable.

That means we need to evaluate at least two axes:

- quality of the emitted translation
- latency of the emission process

This repo uses a simple token-overlap quality score for the toy setting and two classic latency metrics:

- Average Proportion (AP)
- Average Lagging (AL)

## 2. The Trace `g(t)`

For target token position `t`, define `g(t)` as the number of source tokens consumed when token `y_t` was emitted.

Example:

```text
source length n = 5
target length m = 4
g(1) = 2
g(2) = 4
g(3) = 5
g(4) = 5
```

This says:

- the first target token was emitted after reading 2 source tokens
- the second after 4
- the third and fourth only after the full source arrived

## 3. Average Proportion

Average Proportion normalizes how much source was consumed, on average, before each target token.

Formula:

`AP = (1 / (n * m)) * sum_{t=1}^{m} g(t)`

Interpretation:

- lower AP means lower latency
- higher AP means the system tends to wait more

AP is easy to compute but can hide where the delay happened.

## 4. Average Lagging

Average Lagging compares the actual reading curve to an idealized policy that consumes source at a constant rate.

Let:

- `n` be source length
- `m` be target length
- `gamma = m / n`

Then one common form of AL is:

`AL = (1 / tau) * sum_{t=1}^{tau} (g(t) - (t - 1) / gamma)`

where `tau` is the first target step at which the source has been fully consumed, or `m` if that never happens earlier.

Interpretation:

- lower AL means the system tracks the ideal low-lag curve more closely
- higher AL means the system stays behind and waits more than necessary

## 5. Example

Assume:

- `n = 5`
- `m = 4`
- `g = [2, 4, 5, 5]`

Then:

`AP = (2 + 4 + 5 + 5) / (5 * 4) = 16 / 20 = 0.8`

Also:

- `gamma = 4 / 5 = 0.8`
- `(t - 1) / gamma` for `t = 1, 2, 3` gives `0, 1.25, 2.5`
- if `tau = 3`, then
- `AL = (1 / 3) * ((2 - 0) + (4 - 1.25) + (5 - 2.5)) = 2.4167`

The exact value is less important than the interpretation: this trace waits quite a lot.

## 6. Practical Caveats

Latency metrics are useful, but they are not the whole story.

### They ignore content severity

A late function word and a late content word count similarly in many formulas.

### They say nothing about revisions

Some systems support partial revision or display updates, but simple metrics assume committed tokens are final.

### They can hide bursty behavior

A system that waits silently and then outputs many tokens may have similar AP to a smoother system.

This is why qualitative trajectory inspection still matters in teaching.

## 7. What This Repo Measures

For each policy run, the example script records:

- predicted target tokens
- the source position used for each emitted token
- AP
- AL
- a simple token F1 against the reference

That is enough to compare the included policies on the same sentence.
