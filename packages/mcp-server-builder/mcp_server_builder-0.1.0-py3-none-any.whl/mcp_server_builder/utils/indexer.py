"""BM25 search index with Porter stemming and n-gram support."""

from __future__ import annotations

import math
import re
from typing import Final, Self

from nltk.stem import PorterStemmer
from pydantic import BaseModel, ConfigDict, Field

from .stopwords import PRESERVE_TERMS, STOP_WORDS

# Python 3.13 type aliases (PEP 695)
type TokenList = list[str]
type SearchResult = tuple[float, Doc]
type SearchResults = list[SearchResult]

# Tokenization patterns
_TOKEN: Final[re.Pattern[str]] = re.compile(r"[A-Za-z0-9_]+(?:-[A-Za-z0-9_]+)*")
_CAMELCASE_SPLIT: Final[re.Pattern[str]] = re.compile(r"(?<!^)(?=[A-Z])")

# Markdown patterns
_MD_HEADER: Final[re.Pattern[str]] = re.compile(r"^#{1,6}\s+(.+)$", re.MULTILINE)
_MD_CODE_BLOCK: Final[re.Pattern[str]] = re.compile(r"```[\w]*\n([\s\S]*?)```")
_MD_INLINE_CODE: Final[re.Pattern[str]] = re.compile(r"`([^`]+)`")
_MD_LINK_TEXT: Final[re.Pattern[str]] = re.compile(r"\[([^\]]+)\]\([^)]+\)")

# Title boost constants
_TITLE_BOOST_EMPTY: Final[int] = 8  # boost for unfetched content
_TITLE_BOOST_SHORT: Final[int] = 5  # boost for short pages (<800 chars)
_TITLE_BOOST_LONG: Final[int] = 3  # boost for longer pages
_SHORT_PAGE_THRESHOLD: Final[int] = 800

# BM25 parameters
_K1: Final[float] = 1.5  # Term frequency saturation (1.2-2.0 typical)
_B: Final[float] = 0.75  # Document length normalization

# Initialize stemmer
_stemmer = PorterStemmer()


class Doc(BaseModel):
    """A single indexed document with display and search metadata."""

    uri: str = Field(description="Unique identifier/URL for the document")
    display_title: str = Field(description="Human-readable title shown to users")
    content: str = Field(description="Full text content (may be empty before fetching)")
    index_title: str = Field(description="Searchable title text including variants")

    model_config = ConfigDict(extra="allow")


def _generate_ngrams(tokens: TokenList, n: int) -> TokenList:
    """Generate n-grams from a list of tokens, joined with underscores."""
    return ["_".join(tokens[i : i + n]) for i in range(len(tokens) - n + 1)]


def _enhanced_tokenize(text: str) -> TokenList:
    """Enhanced tokenization with stemming and stopword removal.

    Handles:
    - Hyphenated terms (json-rpc)
    - CamelCase splitting (FastMCP -> fast, mcp)
    - Stop word removal
    - Porter stemming (with domain term preservation)
    """
    tokens: TokenList = []

    for token in _TOKEN.findall(text):
        token_lower = token.lower()

        # Skip stop words
        if token_lower in STOP_WORDS:
            continue

        # Preserve domain-specific terms without stemming
        if token_lower in PRESERVE_TERMS:
            tokens.append(token_lower)
            continue

        # Split CamelCase tokens (e.g., FastMCP -> Fast, MCP)
        if any(c.isupper() for c in token[1:]):
            camel_parts = _CAMELCASE_SPLIT.split(token)
            for part in camel_parts:
                part_lower = part.lower()
                if part_lower and part_lower not in STOP_WORDS:
                    if part_lower in PRESERVE_TERMS:
                        tokens.append(part_lower)
                    else:
                        stemmed = _stemmer.stem(part_lower)
                        if stemmed not in STOP_WORDS:
                            tokens.append(stemmed)
            # Also add stemmed original if meaningful
            stemmed_original = _stemmer.stem(token_lower)
            if stemmed_original not in STOP_WORDS and stemmed_original not in tokens:
                tokens.append(stemmed_original)
        else:
            stemmed = _stemmer.stem(token_lower)
            if stemmed not in STOP_WORDS:
                tokens.append(stemmed)

    return tokens


class IndexSearch:
    """BM25 inverted index with Markdown awareness and n-gram support."""

    def __init__(self) -> None:
        """Initialize an empty search index."""
        self.docs: list[Doc] = []
        self.doc_frequency: dict[str, int] = {}
        self.doc_indices: dict[str, list[int]] = {}
        self.doc_lengths: list[int] = []
        self.avg_doc_length: float = 0.0

    def add(self, doc: Doc) -> Self:
        """Add a document to the search index.

        Args:
            doc: Document to add to the index

        Returns:
            Self for method chaining
        """
        idx = len(self.docs)
        self.docs.append(doc)
        seen: set[str] = set()
        doc_tokens: TokenList = []

        # Extract content parts
        content = doc.content.lower()
        title_text = doc.index_title.lower()

        # Extract headers (high importance)
        headers = " ".join(_MD_HEADER.findall(doc.content))

        # Extract code content (medium importance)
        code_blocks = " ".join(_MD_CODE_BLOCK.findall(doc.content))
        inline_code = " ".join(_MD_INLINE_CODE.findall(doc.content))

        # Extract link text (medium importance)
        link_text = " ".join(_MD_LINK_TEXT.findall(doc.content))

        # Build weighted haystack
        haystack_parts = [
            title_text,
            headers.lower(),
            link_text.lower(),
            code_blocks.lower(),
            inline_code.lower(),
            content,
        ]
        haystack = " ".join(part for part in haystack_parts if part)

        # Tokenize and generate n-grams
        unigrams = _enhanced_tokenize(haystack)
        bigrams = _generate_ngrams(unigrams, 2)
        trigrams = _generate_ngrams(unigrams, 3)
        all_tokens = unigrams + bigrams + trigrams

        for tok in all_tokens:
            self.doc_indices.setdefault(tok, []).append(idx)
            if tok not in seen:
                self.doc_frequency[tok] = self.doc_frequency.get(tok, 0) + 1
                seen.add(tok)
            doc_tokens.append(tok)

        # Store document length for BM25
        self.doc_lengths.append(len(doc_tokens))

        # Update average document length
        if self.doc_lengths:
            self.avg_doc_length = sum(self.doc_lengths) / len(self.doc_lengths)

        return self

    def search(self, query: str, k: int = 8) -> SearchResults:
        """Search the index and return ranked results.

        Args:
            query: Search query string
            k: Maximum number of results to return

        Returns:
            List of (score, document) tuples sorted by relevance
        """
        if not self.docs:
            return []

        def _title_boost_for(doc: Doc) -> int:
            n = len(doc.content)
            if n == 0:
                return _TITLE_BOOST_EMPTY
            if n < _SHORT_PAGE_THRESHOLD:
                return _TITLE_BOOST_SHORT
            return _TITLE_BOOST_LONG

        def _calculate_bm25_score(doc: Doc, token: str, doc_idx: int) -> float:
            content_lower = doc.content.lower()
            title_lower = doc.index_title.lower()

            # Term frequencies
            content_tf = content_lower.count(token)
            title_tf = title_lower.count(token)

            # Header matches (4x weight)
            header_tf = sum(
                h.lower().count(token) for h in _MD_HEADER.findall(doc.content)
            )

            # Code matches (2x weight)
            code_tf = sum(
                c.lower().count(token) for c in _MD_CODE_BLOCK.findall(doc.content)
            )

            # Link text matches (2x weight)
            link_tf = sum(
                lnk.lower().count(token) for lnk in _MD_LINK_TEXT.findall(doc.content)
            )

            # Combined weighted TF
            weighted_tf = (
                content_tf
                + title_tf * _title_boost_for(doc)
                + header_tf * 4
                + code_tf * 2
                + link_tf * 2
            )

            # Document length
            doc_length = (
                self.doc_lengths[doc_idx] if doc_idx < len(self.doc_lengths) else 1
            )
            avg_len = max(self.avg_doc_length, 1.0)

            # BM25 IDF
            n_docs = max(len(self.docs), 1)
            df = self.doc_frequency.get(token, 0)
            idf = math.log((n_docs - df + 0.5) / (df + 0.5) + 1.0)

            # BM25 TF with length normalization
            tf_component = (weighted_tf * (_K1 + 1)) / (
                weighted_tf + _K1 * (1 - _B + _B * (doc_length / avg_len))
            )

            return idf * tf_component

        # Tokenize query
        q_unigrams = _enhanced_tokenize(query)
        q_bigrams = _generate_ngrams(q_unigrams, 2)
        q_trigrams = _generate_ngrams(q_unigrams, 3)
        q_tokens = q_unigrams + q_bigrams + q_trigrams

        scores: dict[int, float] = {}

        for qt in q_tokens:
            for idx in self.doc_indices.get(qt, []):
                d = self.docs[idx]
                score = _calculate_bm25_score(d, qt, idx)
                scores[idx] = scores.get(idx, 0.0) + score

        ranked = sorted(
            ((score, self.docs[i]) for i, score in scores.items()),
            key=lambda x: x[0],
            reverse=True,
        )

        return ranked[:k]
