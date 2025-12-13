import uuid, os, operator, datetime, decimal, re, unidecode
from collections import defaultdict
from lenlp import sparse

from lightning_disk_kv import LDKV
from vectorizer import IncrementalBM25
from sparse_matrix import save_sparse_matrix, load_sparse_matrix

class TextInvertedIndex:
    """
    Manages an inverted index (Token -> Set of DocIDs) using LMDB.
    Allows for exact match and prefix (tree-like) lookups.
    """
    def __init__(self, storage):
        self.storage = storage
        # Regex to extract words of 3+ chars
        self.token_pattern = re.compile(r"(?u)\b\w\w\w+\b")

    def tokenize(self, text):
        # Normalize and tokenize
        clean_text = unidecode.unidecode(text).lower()
        return set(self.token_pattern.findall(clean_text))

    def index_document(self, doc_id, text):
        tokens = self.tokenize(text)
        if not tokens:
            return
            
        updates = {f"term_{token}": {doc_id} for token in tokens}
        
        def merge_ids(existing, new_ids):
            if existing is None: return new_ids
            return existing | new_ids
            
        self.storage.batch_atomic_update(updates, merge_ids)

    def remove_document(self, doc_id, text):
        """
        Removes a document ID from the inverted index.
        """
        tokens = self.tokenize(text)
        if not tokens:
            return
            
        updates = {f"term_{token}": {doc_id} for token in tokens}
        
        def remove_ids(existing, ids_to_remove):
            if existing is None: return None
            return existing - ids_to_remove
            
        self.storage.batch_atomic_update(updates, remove_ids)

    def index_documents_batch(self, doc_ids, texts):
        """
        Optimized batch indexing. Aggregates all token->doc_id mappings in memory
        before writing to storage to minimize transactions.
        """
        token_to_new_ids = defaultdict(set)
        
        for doc_id, text in zip(doc_ids, texts):
            tokens = self.tokenize(text)
            for token in tokens:
                token_to_new_ids[f"term_{token}"].add(doc_id)
        
        if not token_to_new_ids:
            return

        def merge_ids(existing, new_ids):
            if existing is None: return new_ids
            return existing | new_ids
            
        self.storage.batch_atomic_update(token_to_new_ids, merge_ids)

    def get_ids_for_token(self, token):
        """
        Retrieves DocIDs using a smart bidirectional lookup:
        1. Forward (Prefix): Matches words in DB starting with token (exon -> exonera)
        2. Backward (Reduction): Matches words in DB that are roots of token (exonerações -> exonera)
        """
        token = unidecode.unidecode(token).lower()
        base_key = f"term_{token}"
        found_ids = set()

        # 1. Forward Scan: Find all keys in DB that start with this token
        start_key = base_key
        end_key = base_key + "{" 
        
        if len(token) >= 3:
            for _, ids in self.storage.items_in_range(start_key, end_key, base_key):
                if ids:
                    found_ids.update(ids)

        # 2. Backward Scan (Recursive Reduction)
        current_term = token
        min_len = 3
        
        for i in range(len(current_term) - 1, min_len - 1, -1):
            sub_token = current_term[:i]
            key = f"term_{sub_token}"
            
            data = self.storage.get_data([key])
            if data and data[0]:
                found_ids.update(data[0])
                break
        
        return found_ids

class SearchEngine:
    OP_MAP = {
        "$gt": operator.gt,
        "$gte": operator.ge,
        "$lt": operator.lt,
        "$lte": operator.le,
        "$ne": operator.ne
    }
    def __init__(self, storage_base_path, metadata_storage_base_path, metadata_index_storage_base_path, matrix_path, text_index_storage_base_path=None, num_shards=8):
        self.storage = LDKV(storage_base_path, num_shards=num_shards)
        self.metadata_storage = LDKV(metadata_storage_base_path, num_shards=num_shards)
        self.metadata_index_storage = LDKV(metadata_index_storage_base_path, num_shards=num_shards)
        
        if text_index_storage_base_path is None:
            text_index_storage_base_path = storage_base_path + "_text_index"
        
        self.text_index_storage = LDKV(text_index_storage_base_path, num_shards=num_shards)
        self.inverted_index = TextInvertedIndex(self.text_index_storage)

        self.matrix_path = matrix_path
        os.makedirs(self.matrix_path, exist_ok=True)
        self.vectorizer = None
        self.indexed_matrix = None
        self.indexed_ids = None

    def index(self, doc_ids=None, batch_size=1000):
        """
        Fits the vectorizer on the dataset in batches to learn the vocabulary
        and IDF scores without storing the entire matrix in memory.
        """
        if doc_ids is None:
            doc_ids = list(self.storage.keys())

        all_texts = self.storage.get_data(doc_ids)

        valid_texts_with_ids = [(doc_id, text) for doc_id, text in zip(doc_ids, all_texts) if text is not None]
        if not valid_texts_with_ids:
            return

        self.indexed_ids = [doc_id for doc_id, _ in valid_texts_with_ids]
        valid_texts = [text for _, text in valid_texts_with_ids]

        self.vectorizer = sparse.BM25Vectorizer(ngram_range=(3, 5), analyzer="char_wb", normalize=True)
        self.indexed_matrix = self.vectorizer.fit_transform(valid_texts)

        save_sparse_matrix(self.matrix_path, self.indexed_matrix)
        self.indexed_matrix = load_sparse_matrix(self.matrix_path)

    def _format_for_indexing(self, value):
        if isinstance(value, datetime.datetime):
            return value.isoformat()
        if isinstance(value, (int, float)):
            offset = decimal.Decimal(2**63)
            return f"{decimal.Decimal(value) + offset:064.8f}"
        return str(value)

    def _update_metadata_index(self, doc_id, metadata):
        updates = {}
        for key, value in metadata.items():
            formatted_value = self._format_for_indexing(value)
            index_key = f"idx_{key}:{formatted_value}"
            updates[index_key] = {doc_id}
        
        if updates:
            def merge_ids(existing, new_ids):
                if existing is None: return new_ids
                return existing | new_ids
            self.metadata_index_storage.batch_atomic_update(updates, merge_ids)
            
    def _prepare_metadata_index_batch(self, doc_ids, metadatas):
        updates = defaultdict(set)
        for doc_id, metadata in zip(doc_ids, metadatas):
            for key, value in metadata.items():
                formatted_value = self._format_for_indexing(value)
                index_key = f"idx_{key}:{formatted_value}"
                updates[index_key].add(doc_id)
        return updates

    def store_data(self, text, metadata, doc_id=None):
        """
        Stores a document.
        :param doc_id: Optional manually specified ID. If provided, acts as an Upsert (overwrites).
                       However, strict overwrite in index requires deleting old first. 
                       This implementation appends to index. For true update, use update_data or delete then store.
        """
        if doc_id is None:
            doc_id = str(uuid.uuid4())
            
        self.storage.store_data([text], [doc_id])
        self.metadata_storage.store_data([metadata], [doc_id])
        self._update_metadata_index(doc_id, metadata)
        
        self.inverted_index.index_document(doc_id, text)
        return doc_id

    def store_data_batch(self, texts, metadatas, doc_ids=None):
        if doc_ids is None:
            doc_ids = [str(uuid.uuid4()) for _ in texts]
            
        self.storage.store_data(texts, doc_ids)
        self.metadata_storage.store_data(metadatas, doc_ids)
        
        meta_updates = self._prepare_metadata_index_batch(doc_ids, metadatas)
        def merge_ids(existing, new_ids):
            if existing is None: return new_ids
            return existing | new_ids
        
        if meta_updates:
            self.metadata_index_storage.batch_atomic_update(meta_updates, merge_ids)

        self.inverted_index.index_documents_batch(doc_ids, texts)
        return doc_ids

    def delete(self, metadata_query):
        """
        Deletes documents matching the metadata query.
        Also cleans up inverted indexes (Text and Metadata).
        Returns number of deleted documents.
        """
        # 1. Identify IDs to delete
        ids_to_delete_set = self._get_filtered_ids(metadata_query)
        if not ids_to_delete_set:
            return 0
        
        ids_to_delete = list(ids_to_delete_set)
        
        # 2. Retrieve existing data to know what to clean from indexes
        # We need the original text to know which tokens to remove, 
        # and original metadata to know which metadata keys to remove.
        texts = self.storage.get_data(ids_to_delete)
        metadatas = self.metadata_storage.get_data(ids_to_delete)
        
        # 3. Clean Text Index
        # We can't batch efficiently across documents easily without reconstructing the logic, 
        # but we can reuse the inverted index helper.
        # Actually, let's build a large batch update for removal.
        text_index_removals = defaultdict(set)
        for doc_id, text in zip(ids_to_delete, texts):
            if text:
                tokens = self.inverted_index.tokenize(text)
                for token in tokens:
                    text_index_removals[f"term_{token}"].add(doc_id)
        
        # 4. Clean Metadata Index
        meta_index_removals = defaultdict(set)
        for doc_id, meta in zip(ids_to_delete, metadatas):
            if meta:
                for key, value in meta.items():
                    formatted_value = self._format_for_indexing(value)
                    index_key = f"idx_{key}:{formatted_value}"
                    meta_index_removals[index_key].add(doc_id)

        # Define removal merge function
        def remove_ids(existing, ids_to_remove):
            if existing is None: return None
            return existing - ids_to_remove

        # Execute Index Cleanups
        if text_index_removals:
            self.text_index_storage.batch_atomic_update(text_index_removals, remove_ids)
        
        if meta_index_removals:
            self.metadata_index_storage.batch_atomic_update(meta_index_removals, remove_ids)

        # 5. Delete Raw Data
        self.storage.delete_data(ids_to_delete)
        self.metadata_storage.delete_data(ids_to_delete)
        
        return len(ids_to_delete)

    def _convert_value(self, s, target_type):
        if target_type == datetime.datetime:
            try:
                return datetime.datetime.fromisoformat(s)
            except (ValueError, TypeError):
                return None
        try:
            return target_type(s)
        except (ValueError, TypeError):
            return None

    def _get_filtered_ids(self, metadata_query):
        if not metadata_query:
            return None

        id_sets = []
        for key, value_or_op in metadata_query.items():
            if isinstance(value_or_op, dict):
                op_str = next(iter(value_or_op))
                op_val = value_or_op[op_str]

                current_op_ids = set()
                if op_str == "$in":
                    for v in op_val:
                        formatted_v = self._format_for_indexing(v)
                        index_key = f"idx_{key}:{formatted_v}"
                        ids_data = self.metadata_index_storage.get_data([index_key])
                        if ids_data and ids_data[0]:
                            current_op_ids.update(ids_data[0])
                    id_sets.append(current_op_ids)
                else:
                    start_key, end_key = "", ""
                    prefix = f"idx_{key}:"

                    if op_str == "$gte":
                        start_key = prefix + self._format_for_indexing(op_val)
                        end_key = prefix + "~"
                    elif op_str == "$gt":
                        start_key = prefix + self._format_for_indexing(op_val) + "\0"
                        end_key = prefix + "~"
                    elif op_str == "$lte":
                        start_key = prefix
                        end_key = prefix + self._format_for_indexing(op_val) + "\0"
                    elif op_str == "$lt":
                        start_key = prefix
                        end_key = prefix + self._format_for_indexing(op_val)

                    for _, ids in self.metadata_index_storage.items_in_range(start_key, end_key, prefix):
                        if ids:
                            current_op_ids.update(ids)
                    id_sets.append(current_op_ids)
            else:
                index_key = f"idx_{key}:{self._format_for_indexing(value_or_op)}"
                ids_data = self.metadata_index_storage.get_data([index_key])
                if ids_data and ids_data[0]:
                    id_sets.append(ids_data[0])
                else:
                    return set()

        if not id_sets:
            return set()

        return set.intersection(*id_sets)

    def search(self, query, metadata_query, window_size=10000, k=5):
        # 1. Metadata Filter
        filtered_ids_set = self._get_filtered_ids(metadata_query)
        if filtered_ids_set is not None and len(filtered_ids_set) == 0:
             return []
        
        # 2. Text Inverted Index Filter
        query_tokens = self.inverted_index.tokenize(query)
        text_candidate_ids = None
        
        if query_tokens:
            token_id_sets = []
            for token in query_tokens:
                t_ids = self.inverted_index.get_ids_for_token(token)
                token_id_sets.append(t_ids)
            
            if token_id_sets:
                text_candidate_ids = set.intersection(*token_id_sets)
            else:
                text_candidate_ids = set()
        
        # 3. Intersect Metadata and Text candidates
        final_candidate_ids = set()
        
        if filtered_ids_set is None and text_candidate_ids is None:
            final_candidate_ids = set(self.storage.keys()) 
        elif filtered_ids_set is None:
            final_candidate_ids = text_candidate_ids
        elif text_candidate_ids is None:
            final_candidate_ids = filtered_ids_set
        else:
            final_candidate_ids = filtered_ids_set.intersection(text_candidate_ids)
                
        if not final_candidate_ids:
            return []

        final_candidate_ids_list = list(final_candidate_ids)

        if len(final_candidate_ids_list) > window_size:
            final_candidate_ids_list = final_candidate_ids_list[:window_size]

        docs_text = self.storage.get_data(final_candidate_ids_list)
        
        valid_docs = [(uid, txt) for uid, txt in zip(final_candidate_ids_list, docs_text) if txt]
        if not valid_docs:
            return []
            
        target_ids = [u for u, t in valid_docs]
        target_texts = [t for u, t in valid_docs]
        
        vectorizer = IncrementalBM25(ngram_range=(3, 5), analyzer="char_wb")
        vectorizer.partial_fit(target_texts)
        candidate_matrix = vectorizer.transform(target_texts)
        query_vec = vectorizer.transform([query])
        
        scores = (candidate_matrix * query_vec.T).toarray().flatten()
        
        scored_results = []
        for i, score in enumerate(scores):
            if score > 0:
                scored_results.append((score, target_ids[i], target_texts[i]))
        
        scored_results.sort(key=lambda x: x[0], reverse=True)
        top_k = scored_results[:k]
        
        top_ids = [r[1] for r in top_k]
        top_metas = self.metadata_storage.get_data(top_ids)
        
        return [(r[1], r[2], m) for r, m in zip(top_k, top_metas)]
