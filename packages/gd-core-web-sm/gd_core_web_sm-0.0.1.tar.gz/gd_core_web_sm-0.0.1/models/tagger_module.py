# gd_core_web_sm/models/tagger_module.py
# -*- coding: utf-8 -*-

import csv
import pickle
from pathlib import Path
from typing import Dict, Union, List

import numpy as np
import torch
import torch.nn as nn
from torch.nn.utils.rnn import pack_padded_sequence, pad_packed_sequence

from spacy.language import Language


# ---------------------------------------------------------------------
# Paths & assets
# ---------------------------------------------------------------------
BASE_DIR = Path(__file__).resolve().parent

# vocab & tag maps
with open(BASE_DIR / "vocab.pkl", "rb") as f:
    word_to_idx: Dict[str, int] = pickle.load(f)

with open(BASE_DIR / "tag_map.pkl", "rb") as f:
    idx_to_tag: Union[Dict[int, str], List[str]] = pickle.load(f)

# embeddings (NumPy .npy)
embedding_matrix = np.load(BASE_DIR / "embedding_matrix.npy")

# fine→UD mapping (loaded once)
VALID_UD = {
    "NOUN", "PROPN", "VERB", "AUX", "ADJ", "ADV", "ADP", "DET", "PRON",
    "NUM", "PART", "SCONJ", "CCONJ", "INTJ", "PUNCT", "SYM", "X"
}

TAG2UD: Dict[str, str] = {}
csv_path = BASE_DIR / "Tags_Sheet.csv"
if csv_path.exists():
    with open(csv_path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            fine = (row.get("Tag") or "").strip()
            ud = (row.get("SimplifiedTags") or "").strip().upper()
            if not fine:
                continue
            base = fine.split("-")[0]
            TAG2UD[base] = ud if ud in VALID_UD else "X"
else:
    # If the CSV is missing, everything will gracefully fall back to "X"
    TAG2UD = {}

def map_fine_to_ud(fine_tag: str) -> str:
    """Map model's fine tag (e.g. 'Ncsmn', 'V-s') to UD POS (e.g. 'NOUN','VERB')."""
    base = (fine_tag or "").split("-")[0].strip()
    ud = TAG2UD.get(base, "X")
    return ud if ud in VALID_UD else "X"


# ---------------------------------------------------------------------
# Model
# ---------------------------------------------------------------------
class PosTagger(nn.Module):
    def __init__(self, vocab_size: int, tagset_size: int, embed_dim: int = 300,
                 hidden_dim: int = 256, dropout: float = 0.5):
        super().__init__()
        embedding_tensor = torch.tensor(embedding_matrix, dtype=torch.float32)
        pad_idx = word_to_idx.get("<pad>", 0)
        self.embedding = nn.Embedding.from_pretrained(
            embedding_tensor, freeze=False, padding_idx=pad_idx
        )
        self.lstm = nn.LSTM(embed_dim, hidden_dim, batch_first=True, bidirectional=True)
        self.dropout = nn.Dropout(dropout)
        self.fc = nn.Linear(hidden_dim * 2, tagset_size)

    def forward(self, token_ids: torch.Tensor, lengths: torch.Tensor) -> torch.Tensor:
        """
        token_ids: [B, T] (Long)
        lengths:   [B]    (Long), actual lengths before padding
        returns:   [B, T, tagset_size]
        """
        embedded = self.embedding(token_ids)                           # [B, T, E]
        packed = pack_padded_sequence(embedded, lengths.cpu(),
                                      batch_first=True, enforce_sorted=False)
        packed_output, _ = self.lstm(packed)
        lstm_output, _ = pad_packed_sequence(packed_output, batch_first=True)  # [B, T, 2H]
        dropped = self.dropout(lstm_output)
        tag_scores = self.fc(dropped)                                  # [B, T, C]
        return tag_scores


# Load trained weights
model = PosTagger(vocab_size=len(word_to_idx),
                  tagset_size=(len(idx_to_tag) if not isinstance(idx_to_tag, dict) else len(idx_to_tag)))
state = torch.load(BASE_DIR / "best_tagging_model.pt", map_location="cpu")
model.load_state_dict(state)
model.eval()


# ---------------------------------------------------------------------
# spaCy component
# ---------------------------------------------------------------------
class TaggerPipe:
    """
    A spaCy pipeline component that:
      1) Runs your PyTorch tagger to predict fine-grained tags.
      2) Sets token.tag_ to the fine tag.
      3) Maps the fine tag to UD and sets token.pos (ID) so .pos_ is valid.
    """

    def __init__(self, model: PosTagger,
                 word_to_idx: Dict[str, int],
                 idx_to_tag: Union[Dict[int, str], List[str]]):
        self.model = model
        self.word_to_idx = word_to_idx
        self.idx_to_tag = idx_to_tag
        self.unk_index = self.word_to_idx.get("<unk>", 0)

    def _idx_to_fine(self, idx: int) -> str:
        if isinstance(self.idx_to_tag, dict):
            return self.idx_to_tag.get(idx, "UNK")
        # list
        if 0 <= idx < len(self.idx_to_tag):
            return self.idx_to_tag[idx]
        return "UNK"

    def __call__(self, doc):
        if len(doc) == 0:
            return doc

        # 1) Convert tokens to ids
        tokens = [t.text.lower() for t in doc]
        ids = [self.word_to_idx.get(tok, self.unk_index) for tok in tokens]
        lengths = torch.tensor([len(ids)], dtype=torch.long)  # [1]
        tensor = torch.tensor([ids], dtype=torch.long)        # [1, T]

        # 2) Predict
        with torch.no_grad():
            scores = self.model(tensor, lengths)              # [1, T, C]
            pred = scores.argmax(dim=-1).squeeze(0).tolist()  # [T]

        # 3) Set fine tag and UD POS on each token
        for token, pred_idx in zip(doc, pred):
            fine = self._idx_to_fine(pred_idx)
            token.tag_ = fine  # fine-grained

            ud = map_fine_to_ud(fine)
            token.pos = doc.vocab.strings[ud]  # set by ID so token.pos_ is valid

        return doc


@Language.factory("pos_tagger_pipe")
def create_tagger_pipe(nlp, name):
    return TaggerPipe(model, word_to_idx, idx_to_tag)
