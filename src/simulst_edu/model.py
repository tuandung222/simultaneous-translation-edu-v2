from __future__ import annotations

from dataclasses import dataclass

import torch
from torch import Tensor, nn


@dataclass(frozen=True)
class Seq2SeqConfig:
    src_vocab_size: int
    tgt_vocab_size: int
    embedding_dim: int = 64
    hidden_dim: int = 96
    dropout: float = 0.1


class AdditiveAttention(nn.Module):
    def __init__(self, hidden_dim: int) -> None:
        super().__init__()
        self.encoder_proj = nn.Linear(hidden_dim, hidden_dim, bias=False)
        self.decoder_proj = nn.Linear(hidden_dim, hidden_dim, bias=False)
        self.score = nn.Linear(hidden_dim, 1, bias=False)

    def forward(
        self,
        encoder_outputs: Tensor,
        decoder_hidden: Tensor,
        source_mask: Tensor,
    ) -> tuple[Tensor, Tensor]:
        decoder_features = self.decoder_proj(decoder_hidden).unsqueeze(1)
        scores = self.score(
            torch.tanh(self.encoder_proj(encoder_outputs) + decoder_features)
        ).squeeze(-1)
        scores = scores.masked_fill(~source_mask, float("-inf"))
        weights = torch.softmax(scores, dim=-1)
        context = torch.bmm(weights.unsqueeze(1), encoder_outputs).squeeze(1)
        return context, weights


class Seq2SeqModel(nn.Module):
    def __init__(self, config: Seq2SeqConfig) -> None:
        super().__init__()
        self.config = config
        self.src_embedding = nn.Embedding(
            config.src_vocab_size, config.embedding_dim, padding_idx=0
        )
        self.tgt_embedding = nn.Embedding(
            config.tgt_vocab_size, config.embedding_dim, padding_idx=0
        )
        self.encoder = nn.GRU(
            input_size=config.embedding_dim,
            hidden_size=config.hidden_dim,
            batch_first=True,
        )
        self.attention = AdditiveAttention(config.hidden_dim)
        self.decoder_cell = nn.GRUCell(
            input_size=config.embedding_dim + config.hidden_dim,
            hidden_size=config.hidden_dim,
        )
        self.output_proj = nn.Linear(
            config.embedding_dim + (2 * config.hidden_dim), config.tgt_vocab_size
        )
        self.dropout = nn.Dropout(config.dropout)

    def encode(self, source_tokens: Tensor) -> tuple[Tensor, Tensor, Tensor]:
        source_mask = source_tokens != 0
        embeddings = self.dropout(self.src_embedding(source_tokens))
        encoder_outputs, hidden = self.encoder(embeddings)
        return encoder_outputs, hidden.squeeze(0), source_mask

    def decode_step(
        self,
        prev_tokens: Tensor,
        hidden: Tensor,
        encoder_outputs: Tensor,
        source_mask: Tensor,
    ) -> tuple[Tensor, Tensor, Tensor]:
        token_emb = self.dropout(self.tgt_embedding(prev_tokens))
        context, weights = self.attention(encoder_outputs, hidden, source_mask)
        hidden = self.decoder_cell(torch.cat([token_emb, context], dim=-1), hidden)
        logits = self.output_proj(torch.cat([token_emb, hidden, context], dim=-1))
        return logits, hidden, weights

    def forward(self, source_tokens: Tensor, decoder_inputs: Tensor) -> Tensor:
        encoder_outputs, hidden, source_mask = self.encode(source_tokens)
        logits_steps: list[Tensor] = []
        for step in range(decoder_inputs.size(1)):
            step_logits, hidden, _ = self.decode_step(
                decoder_inputs[:, step], hidden, encoder_outputs, source_mask
            )
            logits_steps.append(step_logits.unsqueeze(1))
        return torch.cat(logits_steps, dim=1)

    @torch.no_grad()
    def greedy_decode(
        self,
        source_tokens: Tensor,
        *,
        bos_id: int,
        eos_id: int,
        max_len: int = 24,
    ) -> tuple[list[int], list[float]]:
        self.eval()
        encoder_outputs, hidden, source_mask = self.encode(source_tokens)
        prev = torch.tensor([bos_id], device=source_tokens.device)
        generated: list[int] = []
        confidences: list[float] = []
        for _ in range(max_len):
            logits, hidden, _ = self.decode_step(prev, hidden, encoder_outputs, source_mask)
            probs = torch.softmax(logits, dim=-1)
            next_token = int(torch.argmax(probs, dim=-1).item())
            confidence = float(probs[0, next_token].item())
            generated.append(next_token)
            confidences.append(confidence)
            prev = torch.tensor([next_token], device=source_tokens.device)
            if next_token == eos_id:
                break
        return generated, confidences
