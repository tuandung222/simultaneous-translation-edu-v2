# Problem Setup

## 1. Offline vs Simultaneous Translation

In offline machine translation, the model sees the complete source sentence before generating the target sentence.

If the source sentence is:

`x = (x_1, x_2, ..., x_n)`

then the model predicts:

`y = (y_1, y_2, ..., y_m)`

using the full source context.

Simultaneous translation changes the information pattern. The system does not always have access to the full source. Instead, it sees a source prefix:

`x_{\le i} = (x_1, x_2, ..., x_i)`

and must decide whether to:

- `READ`: wait for one more source token
- `WRITE`: commit the next target token

That decision is irreversible once the token is emitted.

## 2. Why This Is Hard

Three difficulties appear immediately.

### Delayed evidence

The source token needed to disambiguate a target token may arrive later.

### Reordering

The source language and target language may place corresponding information in different positions.

### Commitment risk

Once the system speaks a token, it cannot easily retract it.

This makes simultaneous translation both a prediction problem and a control problem.

## 3. Sequential Decision View

A simultaneous system can be viewed as interleaving two action types:

```text
READ, READ, WRITE, WRITE, READ, WRITE, ...
```

At any moment the state contains at least:

- how many source tokens have been consumed
- how many target tokens have already been committed
- the current model hypothesis under the available source prefix

The policy is the rule that maps this state to the next action.

The model and policy are not the same thing:

- the model scores or predicts tokens
- the policy decides when prediction is stable enough to emit

## 4. Prefix-to-Prefix Translation Intuition

In the idealized prefix-to-prefix view, target token `y_t` should be generated after consuming some source prefix length `g(t)`.

Here:

- `t` indexes target tokens
- `g(t)` is how many source tokens were read before emitting `y_t`

The function `g(t)` is central because it creates the latency trace.

If `g(t)` is large for every `t`, latency is high.

If `g(t)` is small, latency is low, but quality may collapse.

## 5. A Concrete Example

Suppose the source language order is:

`subject verb adjective object time`

but the target language order is:

`subject object adjective time verb`

Then the target object may need to be emitted very early relative to the target sequence, but it arrives late in the source sequence.

That is exactly the kind of mismatch that makes simultaneous translation nontrivial.

## 6. Taxonomy of Policies

There are many ways to define `g(t)` or decide actions:

- fixed policies: `wait-k`, chunked reading
- adaptive policies: confidence-based, local-agreement
- learned policies: train an agent to issue `READ` or `WRITE`

This repo focuses on hand-designed policies first, because they expose the structure of the problem clearly.

## 7. Questions Students Should Be Able to Answer

- What information is available when a token is emitted?
- What mistakes happen when the system writes too early?
- Which part of the system is responsible for timing?
- Why can two systems with similar final accuracy have very different user experience?
