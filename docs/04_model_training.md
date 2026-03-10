# Model and Training Pipeline

## 1. Why This Repo Uses A Small Model

A teaching repository should maximize inspectability.

This project therefore uses:

- a small synthetic dataset
- separate source and target vocabularies
- a unidirectional GRU encoder
- additive attention
- a GRU-cell decoder

This is not because RNNs are state of the art. It is because the dataflow is easy to explain line by line.

## 2. Synthetic Data Design

The synthetic grammar deliberately introduces mild source-target reordering.

Source patterns look like:

- `subject verb object`
- `subject verb adjective object`
- `subject not verb object time`

Target patterns reorder them into a pseudo-language:

- `subject object verb`
- `subject object adjective verb`
- `subject object time NEG_verb`

This matters because simultaneous policies should visibly struggle if they emit before the object or modifier arrives.

## 3. Encoder

The encoder processes only the currently visible source prefix.

Key choice:

- the encoder is unidirectional, so the state remains conceptually compatible with streaming

Output:

- per-token encoder states for attention
- final hidden state for decoder initialization

## 4. Decoder

At each step the decoder:

1. embeds the previous target token
2. computes additive attention over encoder states
3. updates a GRU cell with the token embedding and context vector
4. projects to vocabulary logits

During training, the decoder uses teacher forcing.

During inference, it uses greedy decoding.

## 5. Prefix Decoding Mismatch

The most important conceptual limitation in this repo is this:

- training uses full source sentences
- simultaneous inference often decodes from incomplete source prefixes

That mismatch is educationally useful. It makes the role of the policy obvious.

It also motivates more advanced topics:

- prefix-to-prefix training
- latency-aware objectives
- monotonic or streaming attention

## 6. Training Loop

The training pipeline is intentionally standard:

1. generate examples
2. build vocabularies
3. numericalize and pad
4. train with cross-entropy
5. evaluate token accuracy on held-out examples

The goal is not benchmark performance. The goal is to get a model that is good enough for meaningful policy comparison.

## 7. What Students Should Inspect In Code

- how `Example` objects are generated
- how `<bos>` and `<eos>` are inserted
- how attention masks ignore padding
- how greedy decoding returns both tokens and token confidences
- how simultaneous decoding reuses the same model on progressively longer prefixes

## 8. Extension Path

Once students understand the baseline, they can replace the model with:

- a transformer encoder-decoder
- a prefix-LM style decoder
- a learned policy controller

The policy API can stay mostly unchanged.
