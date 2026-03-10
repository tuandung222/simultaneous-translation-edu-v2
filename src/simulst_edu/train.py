from __future__ import annotations

from dataclasses import dataclass

import torch
from torch import nn
from torch.nn.utils.rnn import pad_sequence
from torch.utils.data import DataLoader

from .data import Example
from .model import Seq2SeqConfig, Seq2SeqModel
from .vocab import Vocab


@dataclass(frozen=True)
class TrainingConfig:
    epochs: int = 8
    batch_size: int = 32
    learning_rate: float = 3e-3
    embedding_dim: int = 64
    hidden_dim: int = 96
    device: str = "cpu"
    log_every: int = 1


def build_vocabs(examples: list[Example]) -> tuple[Vocab, Vocab]:
    source_vocab = Vocab.from_token_sequences([example.source_tokens for example in examples])
    target_vocab = Vocab.from_token_sequences([example.target_tokens for example in examples])
    return source_vocab, target_vocab


def _collate_batch(
    batch: list[Example],
    source_vocab: Vocab,
    target_vocab: Vocab,
) -> tuple[torch.Tensor, torch.Tensor]:
    source_tensors = [
        torch.tensor(source_vocab.encode(example.source_tokens, add_eos=True), dtype=torch.long)
        for example in batch
    ]
    target_tensors = [
        torch.tensor(
            target_vocab.encode(example.target_tokens, add_bos=True, add_eos=True),
            dtype=torch.long,
        )
        for example in batch
    ]
    source_batch = pad_sequence(source_tensors, batch_first=True, padding_value=source_vocab.pad_id)
    target_batch = pad_sequence(target_tensors, batch_first=True, padding_value=target_vocab.pad_id)
    return source_batch, target_batch


def _sequence_token_accuracy(
    model: Seq2SeqModel,
    examples: list[Example],
    source_vocab: Vocab,
    target_vocab: Vocab,
    device: str,
) -> float:
    if not examples:
        return 0.0
    model.eval()
    correct = 0
    total = 0
    with torch.no_grad():
        for example in examples:
            source_ids = source_vocab.encode(example.source_tokens, add_eos=True)
            source_tensor = torch.tensor([source_ids], dtype=torch.long, device=device)
            predicted, _ = model.greedy_decode(
                source_tensor,
                bos_id=target_vocab.bos_id,
                eos_id=target_vocab.eos_id,
                max_len=len(example.target_tokens) + 4,
            )
            predicted_tokens = target_vocab.decode(predicted, skip_specials=True)
            total += len(example.target_tokens)
            correct += sum(
                1 for left, right in zip(predicted_tokens, example.target_tokens) if left == right
            )
    return correct / max(1, total)


def train_model(
    train_examples: list[Example],
    valid_examples: list[Example],
    config: TrainingConfig,
) -> tuple[Seq2SeqModel, Vocab, Vocab]:
    source_vocab, target_vocab = build_vocabs(train_examples + valid_examples)
    model = Seq2SeqModel(
        Seq2SeqConfig(
            src_vocab_size=len(source_vocab),
            tgt_vocab_size=len(target_vocab),
            embedding_dim=config.embedding_dim,
            hidden_dim=config.hidden_dim,
        )
    ).to(config.device)

    optimizer = torch.optim.Adam(model.parameters(), lr=config.learning_rate)
    criterion = nn.CrossEntropyLoss(ignore_index=target_vocab.pad_id)
    loader = DataLoader(
        train_examples,
        batch_size=config.batch_size,
        shuffle=True,
        collate_fn=lambda batch: _collate_batch(batch, source_vocab, target_vocab),
    )

    for epoch in range(1, config.epochs + 1):
        model.train()
        epoch_loss = 0.0
        for source_batch, target_batch in loader:
            source_batch = source_batch.to(config.device)
            target_batch = target_batch.to(config.device)
            decoder_inputs = target_batch[:, :-1]
            decoder_targets = target_batch[:, 1:]

            logits = model(source_batch, decoder_inputs)
            loss = criterion(logits.reshape(-1, logits.size(-1)), decoder_targets.reshape(-1))

            optimizer.zero_grad()
            loss.backward()
            optimizer.step()
            epoch_loss += float(loss.item())

        if config.log_every and epoch % config.log_every == 0:
            val_acc = _sequence_token_accuracy(
                model, valid_examples, source_vocab, target_vocab, config.device
            )
            avg_loss = epoch_loss / max(1, len(loader))
            print(
                f"epoch={epoch} train_loss={avg_loss:.4f} "
                f"valid_token_acc={val_acc:.4f}"
            )

    return model, source_vocab, target_vocab
