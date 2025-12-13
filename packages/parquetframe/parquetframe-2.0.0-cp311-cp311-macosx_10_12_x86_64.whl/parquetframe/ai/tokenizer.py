"""
Simple BPE (Byte-Pair Encoding) tokenizer for text embeddings.

Provides a basic BPE implementation that can replace character-level
tokenization for better quality embeddings.
"""

import json
import logging
from collections import Counter
from pathlib import Path

logger = logging.getLogger(__name__)


class BPETokenizer:
    """Simple BPE tokenizer for embedding models."""

    def __init__(self, vocab_size: int = 10000):
        """
        Initialize BPE tokenizer.

        Args:
            vocab_size: Target vocabulary size
        """
        self.vocab_size = vocab_size
        self.vocab: dict[str, int] = {}
        self.merges: list[tuple[str, str]] = []
        self._initialized = False

        # Special tokens
        self.pad_token = "<PAD>"
        self.unk_token = "<UNK>"
        self.bos_token = "<BOS>"
        self.eos_token = "<EOS>"

        # Initialize with special tokens
        self.vocab = {
            self.pad_token: 0,
            self.unk_token: 1,
            self.bos_token: 2,
            self.eos_token: 3,
        }

    def train(self, texts: list[str], max_merges: int | None = None):
        """
        Train BPE tokenizer on corpus.

        Args:
            texts: Training corpus
            max_merges: Maximum number of merge operations (default: vocab_size - special tokens)
        """
        if max_merges is None:
            max_merges = self.vocab_size - len(self.vocab)

        # Initialize with character vocabulary
        word_freq: Counter = Counter()
        for text in texts:
            words = text.lower().split()
            for word in words:
                word_freq[" ".join(word) + " </w>"] += 1

        # Perform BPE merges
        for _i in range(max_merges):
            pairs = self._get_pair_frequencies(word_freq)
            if not pairs:
                break

            best_pair = max(pairs, key=pairs.get)
            word_freq = self._merge_vocab(best_pair, word_freq)
            self.merges.append(best_pair)

            # Add to vocabulary
            merged = "".join(best_pair)
            if merged not in self.vocab:
                self.vocab[merged] = len(self.vocab)

        self._initialized = True
        logger.info(
            f"Trained BPE with {len(self.vocab)} tokens and {len(self.merges)} merges"
        )

    def _get_pair_frequencies(self, word_freq: Counter) -> Counter:
        """Get frequencies of all adjacent pairs."""
        pairs: Counter = Counter()
        for word, freq in word_freq.items():
            symbols = word.split()
            for i in range(len(symbols) - 1):
                pairs[(symbols[i], symbols[i + 1])] += freq
        return pairs

    def _merge_vocab(self, pair: tuple[str, str], word_freq: Counter) -> Counter:
        """Merge a pair in the vocabulary."""
        new_word_freq: Counter = Counter()
        bigram = " ".join(pair)
        replacement = "".join(pair)

        for word, freq in word_freq.items():
            new_word = word.replace(bigram, replacement)
            new_word_freq[new_word] = freq

        return new_word_freq

    def encode(self, text: str, add_special_tokens: bool = True) -> list[int]:
        """
        Encode text to token IDs.

        Args:
            text: Input text
            add_special_tokens: Whether to add BOS/EOS tokens

        Returns:
            List of token IDs
        """
        if not self._initialized:
            # Fall back to simple character-level encoding
            return self._encode_chars(text)

        tokens = []
        if add_special_tokens:
            tokens.append(self.vocab[self.bos_token])

        words = text.lower().split()
        for word in words:
            word_tokens = self._encode_word(word)
            tokens.extend(word_tokens)

        if add_special_tokens:
            tokens.append(self.vocab[self.eos_token])

        return tokens

    def _encode_word(self, word: str) -> list[int]:
        """Encode single word using BPE."""
        word_chars = " ".join(word) + " </w>"

        # Apply merge operations
        for merge in self.merges:
            bigram = " ".join(merge)
            replacement = "".join(merge)
            word_chars = word_chars.replace(bigram, replacement)

        # Convert to token IDs
        tokens = []
        for symbol in word_chars.split():
            tokens.append(self.vocab.get(symbol, self.vocab[self.unk_token]))

        return tokens

    def _encode_chars(self, text: str) -> list[int]:
        """Fall back character-level encoding."""
        char_to_idx = {chr(i): i + len(self.vocab) for i in range(256)}
        return [char_to_idx.get(c, self.vocab[self.unk_token]) for c in text.lower()]

    def decode(self, token_ids: list[int]) -> str:
        """
        Decode token IDs to text.

        Args:
            token_ids: List of token IDs

        Returns:
            Decoded text
        """
        # Reverse vocab for decoding
        id_to_token = {v: k for k, v in self.vocab.items()}

        tokens = []
        for token_id in token_ids:
            if token_id in [
                self.vocab[self.pad_token],
                self.vocab[self.bos_token],
                self.vocab[self.eos_token],
            ]:
                continue
            tokens.append(id_to_token.get(token_id, self.unk_token))

        text = "".join(tokens)
        text = text.replace("</w>", " ")
        return text.strip()

    def save(self, path: Path):
        """Save tokenizer to file."""
        data = {
            "vocab": self.vocab,
            "merges": self.merges,
            "vocab_size": self.vocab_size,
        }
        with open(path, "w") as f:
            json.dump(data, f, indent=2)

    def load(self, path: Path):
        """Load tokenizer from file."""
        with open(path) as f:
            data = json.load(f)

        self.vocab = data["vocab"]
        self.merges = [tuple(m) for m in data["merges"]]
        self.vocab_size = data["vocab_size"]
        self._initialized = True


__all__ = ["BPETokenizer"]
