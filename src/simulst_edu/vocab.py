from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Vocab:
    stoi: dict[str, int]
    itos: list[str]

    pad_token: str = "<pad>"
    bos_token: str = "<bos>"
    eos_token: str = "<eos>"
    unk_token: str = "<unk>"

    @classmethod
    def from_token_sequences(cls, sequences: list[tuple[str, ...]]) -> "Vocab":
        specials = ["<pad>", "<bos>", "<eos>", "<unk>"]
        tokens = sorted({token for seq in sequences for token in seq})
        itos = specials + tokens
        stoi = {token: idx for idx, token in enumerate(itos)}
        return cls(stoi=stoi, itos=itos)

    @property
    def pad_id(self) -> int:
        return self.stoi[self.pad_token]

    @property
    def bos_id(self) -> int:
        return self.stoi[self.bos_token]

    @property
    def eos_id(self) -> int:
        return self.stoi[self.eos_token]

    @property
    def unk_id(self) -> int:
        return self.stoi[self.unk_token]

    def encode(
        self,
        tokens: tuple[str, ...] | list[str],
        *,
        add_bos: bool = False,
        add_eos: bool = False,
    ) -> list[int]:
        encoded: list[int] = []
        if add_bos:
            encoded.append(self.bos_id)
        encoded.extend(self.stoi.get(token, self.unk_id) for token in tokens)
        if add_eos:
            encoded.append(self.eos_id)
        return encoded

    def decode(self, ids: list[int], *, skip_specials: bool = True) -> list[str]:
        special_ids = {self.pad_id, self.bos_id}
        decoded: list[str] = []
        for idx in ids:
            if idx == self.eos_id:
                break
            if skip_specials and idx in special_ids:
                continue
            decoded.append(self.itos[idx])
        return decoded

    def __len__(self) -> int:
        return len(self.itos)
