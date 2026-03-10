# Project Practicum

## 1. End-to-End Build Order

If you are teaching or self-studying from this repository, build in this order:

1. understand the synthetic grammar
2. train the offline model
3. decode full sentences greedily
4. add simultaneous decoding over prefixes
5. compare policies
6. inspect trajectories and metrics

This order matters because students often try to debug policies before they trust the underlying model.

## 2. Minimal Demo Workflow

Run the example script:

```bash
cd /Users/admin/TuanDung/repos/simultaneous-translation-edu
python examples/compare_policies.py
```

The script will:

- generate train, validation, and test splits
- train a small model
- pick a few held-out sentences
- run multiple simultaneous policies
- print the translation and latency metrics for each policy

## 3. Reading The Output

For each sentence, compare:

- reference translation
- predicted translation
- source positions used for each emitted token
- AP
- AL
- token F1

When a policy fails, ask:

- did it emit before the object arrived?
- did it wait until the source was complete?
- did the model become stable only after a critical token appeared?

## 4. Suggested Live-Coding Exercises

### Exercise A. Change wait-k

Run `wait-k` with different values and explain the tradeoff.

### Exercise B. Add a punctuation gate

Only allow writes when the latest source token belongs to a chosen set.

### Exercise C. Hybrid policy

Combine a minimum lag with a confidence threshold.

### Exercise D. Stress-test the dataset

Increase reordering frequency in the synthetic generator and inspect which policy degrades fastest.

## 5. Discussion Prompts

- Why can local agreement outperform confidence thresholding on unstable prefixes?
- Why might confidence be high for the wrong token?
- What part of the system would change first if we moved to speech input?
- Which policy is easiest to reason about analytically?

## 6. Practical Teaching Advice

Do not present the repo as a realistic benchmark winner.

Present it as:

- a controlled environment for thinking
- a bridge from sequence modeling to streaming decisions
- a scaffold for later research implementation

That framing keeps students focused on mechanism instead of leaderboard comparison.

## 7. Repository Exercise Checklist

- read all docs in order
- run the example script
- inspect one failed sentence deeply
- implement one new policy
- add one new metric or one new data pattern
- write a short note on the best latency-quality tradeoff you observed
