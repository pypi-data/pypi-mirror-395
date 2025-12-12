import numpy as np
from collections import defaultdict
from scipy.sparse import csr_matrix
from sklearn.base import BaseEstimator, TransformerMixin
from sklearn.utils.validation import check_is_fitted
import unidecode, re


class IncrementalBM25(BaseEstimator, TransformerMixin):
    """
    BM25 Vectorizer that supports incremental fitting (partial_fit).

    Parameters
    ----------
    analyzer : {'word', 'char', 'char_wb'}, default='word'
        Whether the feature should be made of word or character n-grams.
        - 'word': standard word tokens.
        - 'char': character n-grams across the text.
        - 'char_wb': character n-grams only inside word boundaries (padded with space).
    ngram_range : tuple (min_n, max_n), default=(1, 1)
        The range of n-values for different n-grams to be extracted.
    k1 : float, default=1.5
        Term frequency saturation parameter.
    b : float, default=0.75
        Length normalization parameter.
    delta : float, default=0.0
        Smoothing term.
    token_pattern : str, default=r"(?u)\b\w\w+\b"
        Regex pattern to extract tokens (used for 'word' and 'char_wb').
    """

    def __init__(
        self,
        analyzer: str = "word",
        ngram_range: tuple = (1, 1),
        k1: float = 1.5,
        b: float = 0.75,
        delta: float = 0.0,
        token_pattern: str = r"(?u)\b\w\w+\b",
    ):
        self.analyzer = analyzer
        self.ngram_range = ngram_range
        self.k1 = k1
        self.b = b
        self.delta = delta
        self.token_pattern = token_pattern
        self._token_pattern_compiled = re.compile(token_pattern)

        if self.analyzer not in {"word", "char", "char_wb"}:
            raise ValueError("analyzer must be 'word', 'char', or 'char_wb'")

        # Incremental state
        self.vocabulary_ = {}
        self.feature_names_in_ = []
        self.df_ = defaultdict(int)
        self.n_samples_ = 0
        self.sum_doc_len_ = 0
        self.avg_doc_len_ = 0.0

    def _word_ngrams(self, tokens):
        """Turn tokens into word n-grams."""
        min_n, max_n = self.ngram_range
        if max_n == 1:
            return tokens

        n_original = len(tokens)
        ngrams = []
        if min_n == 1:
            ngrams.extend(tokens)

        for n in range(max(min_n, 2), max_n + 1):
            if n_original < n:
                continue
            for i in range(n_original - n + 1):
                ngrams.append(" ".join(tokens[i : i + n]))
        return ngrams

    def _char_ngrams(self, text):
        """Turn text into character n-grams."""
        min_n, max_n = self.ngram_range
        ngrams = []
        n_text = len(text)

        for n in range(min_n, max_n + 1):
            if n_text < n:
                continue
            for i in range(n_text - n + 1):
                ngrams.append(text[i : i + n])
        return ngrams

    def _char_wb_ngrams(self, text):
        """Turn text into character n-grams with word boundary padding."""
        min_n, max_n = self.ngram_range
        # Extract words first
        words = self._token_pattern_compiled.findall(text)
        ngrams = []

        for word in words:
            # Pad word with spaces for boundaries
            w_padded = f" {word} "
            n_len = len(w_padded)

            for n in range(min_n, max_n + 1):
                if n_len < n:
                    continue
                for i in range(n_len - n + 1):
                    ngrams.append(w_padded[i : i + n])
        return ngrams

    def _analyze(self, doc):
        """Analyze a single document and return a list of features."""
        doc = unidecode.unidecode(doc.lower())

        if self.analyzer == "word":
            tokens = self._token_pattern_compiled.findall(doc)
            return self._word_ngrams(tokens)

        elif self.analyzer == "char":
            # For char, we usually use the raw string, but standard vectorizers
            # often process the string directly.
            return self._char_ngrams(doc)

        elif self.analyzer == "char_wb":
            return self._char_wb_ngrams(doc)

        return []

    def partial_fit(self, X, y=None):
        if isinstance(X, str):
            X = [X]

        batch_n = 0
        batch_len = 0

        for doc in X:
            tokens = self._analyze(doc)
            n_tokens = len(tokens)

            batch_n += 1
            batch_len += n_tokens

            unique_tokens = set(tokens)
            for token in unique_tokens:
                if token not in self.vocabulary_:
                    idx = len(self.vocabulary_)
                    self.vocabulary_[token] = idx
                    self.feature_names_in_.append(token)

                self.df_[token] += 1

        self.n_samples_ += batch_n
        self.sum_doc_len_ += batch_len
        if self.n_samples_ > 0:
            self.avg_doc_len_ = self.sum_doc_len_ / self.n_samples_

        return self

    def fit(self, X, y=None):
        # Reset state
        self.vocabulary_ = {}
        self.feature_names_in_ = []
        self.df_ = defaultdict(int)
        self.n_samples_ = 0
        self.sum_doc_len_ = 0
        self.avg_doc_len_ = 0.0
        return self.partial_fit(X, y)

    def _calculate_idf(self):
        n_vocab = len(self.vocabulary_)
        idf_diag = np.zeros(n_vocab)
        for token, idx in self.vocabulary_.items():
            df = self.df_[token]
            idf = np.log((self.n_samples_ - df + 0.5) / (df + 0.5) + 1)
            idf_diag[idx] = idf
        self.idf_diag_ = idf_diag

    def partial_fit(self, X, y=None):
        if isinstance(X, str):
            X = [X]

        batch_n = 0
        batch_len = 0

        for doc in X:
            tokens = self._analyze(doc)
            n_tokens = len(tokens)

            batch_n += 1
            batch_len += n_tokens

            unique_tokens = set(tokens)
            for token in unique_tokens:
                if token not in self.vocabulary_:
                    idx = len(self.vocabulary_)
                    self.vocabulary_[token] = idx
                    self.feature_names_in_.append(token)

                self.df_[token] += 1

        self.n_samples_ += batch_n
        self.sum_doc_len_ += batch_len
        if self.n_samples_ > 0:
            self.avg_doc_len_ = self.sum_doc_len_ / self.n_samples_

        self._calculate_idf()

        return self

    def transform(self, X):
        check_is_fitted(self, attributes=["n_samples_", "vocabulary_"])

        if isinstance(X, str):
            X = [X]

        n_vocab = len(self.vocabulary_)
        indptr = [0]
        indices = []
        data = []

        for doc in X:
            tokens = self._analyze(doc)
            doc_len = len(tokens)

            tf_counter = defaultdict(int)
            for t in tokens:
                if t in self.vocabulary_:
                    tf_counter[self.vocabulary_[t]] += 1

            denom_part = self.k1 * (1 - self.b + self.b * (doc_len / self.avg_doc_len_)) if self.avg_doc_len_ > 0 else 0

            for idx, tf in tf_counter.items():
                numerator = tf * (self.k1 + 1)
                denominator = tf + denom_part
                score = self.idf_diag_[idx] * (numerator / denominator) + self.delta

                indices.append(idx)
                data.append(score)

            indptr.append(len(indices))

        return csr_matrix((data, indices, indptr), shape=(len(X), n_vocab), dtype=np.float32)

    def get_feature_names_out(self, input_features=None):
        check_is_fitted(self, attributes=["feature_names_in_"])
        return np.array(self.feature_names_in_, dtype=object)