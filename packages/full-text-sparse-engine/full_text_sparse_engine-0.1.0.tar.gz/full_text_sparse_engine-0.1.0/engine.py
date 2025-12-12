import uuid, heapq, os
from lenlp import flash, sparse

from storage import ShardedLmdbStorage
from vectorizer import IncrementalBM25
from sparse_matrix import save_sparse_matrix, load_sparse_matrix


class SearchEngine:
    def __init__(self, storage_base_path, metadata_storage_base_path, metadata_index_storage_base_path, matrix_path, num_shards=8):
        self.storage = ShardedLmdbStorage(storage_base_path, num_shards=num_shards)
        self.metadata_storage = ShardedLmdbStorage(metadata_storage_base_path, num_shards=num_shards)
        self.metadata_index_storage = ShardedLmdbStorage(metadata_index_storage_base_path, num_shards=num_shards)
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

        # Use the fast, in-memory vectorizer to build the matrix
        self.vectorizer = sparse.BM25Vectorizer(ngram_range=(3, 5), analyzer="char_wb", normalize=True)
        self.indexed_matrix = self.vectorizer.fit_transform(valid_texts)

        # Save the matrix to disk
        save_sparse_matrix(self.matrix_path, self.indexed_matrix)

        # Load the matrix back as a memory-mapped object
        self.indexed_matrix = load_sparse_matrix(self.matrix_path)

    def store_data(self, text, metadata):
        doc_id = str(uuid.uuid4())
        self.storage.store_data([text], [doc_id])
        self.metadata_storage.store_data([metadata], [doc_id])

        for key, value in metadata.items():
            index_key = f"idx_{key}:{value}"

            def update_index(current_ids):
                if current_ids is None:
                    return {doc_id}
                else:
                    current_ids.add(doc_id)
                    return current_ids

            self.metadata_index_storage.atomic_update(index_key, update_index)
        return doc_id

    def store_data_batch(self, texts, metadatas):
        doc_ids = [str(uuid.uuid4()) for _ in texts]
        self.storage.store_data(texts, doc_ids)
        self.metadata_storage.store_data(metadatas, doc_ids)

        for doc_id, metadata in zip(doc_ids, metadatas):
            for key, value in metadata.items():
                index_key = f"idx_{key}:{value}"

                def update_index(current_ids):
                    if current_ids is None:
                        return {doc_id}
                    else:
                        current_ids.add(doc_id)
                        return current_ids

                self.metadata_index_storage.atomic_update(index_key, update_index)
        return doc_ids

    def _get_filtered_ids(self, metadata_query):
        if not metadata_query:
            return list(self.metadata_storage.keys())

        id_sets = []
        for key, value in metadata_query.items():
            index_key = f"idx_{key}:{value}"
            ids_data = self.metadata_index_storage.get_data([index_key])
            if ids_data and ids_data[0] is not None:
                id_sets.append(ids_data[0])
            else:
                return []

        if not id_sets:
            return []

        return list(set.intersection(*id_sets))

    def search(self, query, metadata_query, window_size=10000, k=5):
        filtered_ids = self._get_filtered_ids(metadata_query)
        if not filtered_ids:
            return []

        # If an index has been built, use the memory-mapped matrix for fast search.
        if self.indexed_matrix is not None:
            query_vec = self.vectorizer.transform([query])

            # Map filtered_ids to the rows in the matrix
            doc_id_to_row = {doc_id: i for i, doc_id in enumerate(self.indexed_ids)}
            matrix_rows = [doc_id_to_row[doc_id] for doc_id in filtered_ids if doc_id in doc_id_to_row]

            if not matrix_rows:
                return []

            sub_matrix = self.indexed_matrix[matrix_rows, :]
            scores = (sub_matrix * query_vec.T).toarray().flatten()

            num_results = min(k, len(scores))
            top_k_indices = scores.argsort()[-num_results:][::-1]

            top_doc_ids = [self.indexed_ids[matrix_rows[i]] for i in top_k_indices]

            top_docs = self.storage.get_data(top_doc_ids)
            metadatas = self.metadata_storage.get_data(top_doc_ids)
            return list(zip(top_doc_ids, top_docs, metadatas))

        # Fallback to FlashText and on-the-fly BM25 if no index is available.
        else:
            flash_text = flash.FlashText(normalize=True)
            flash_text.add(query.split())

            results = []
            for i in range(0, len(filtered_ids), window_size):
                batch_ids = filtered_ids[i:i+window_size]
                texts = self.storage.get_data(batch_ids)

                texts_with_ids = list(zip(batch_ids, texts))
                texts_to_process = [t for _, t in texts_with_ids if t is not None]
                ids_to_process = [doc_id for doc_id, t in texts_with_ids if t is not None]

                if not texts_to_process:
                    continue

                extracted = flash_text.extract(texts_to_process)
                for doc_idx, result in enumerate(extracted):
                    if result:
                        results.append((ids_to_process[doc_idx], texts_to_process[doc_idx]))

            if results:
                doc_ids = [r[0] for r in results]
                metadatas = self.metadata_storage.get_data(doc_ids)
                return list(zip(doc_ids, [r[1] for r in results], metadatas))

            if len(filtered_ids) > window_size:
                vectorizer = IncrementalBM25(ngram_range=(3, 5), analyzer="char_wb")

                for i in range(0, len(filtered_ids), window_size):
                    batch_ids = filtered_ids[i:i+window_size]
                    batch_texts = self.storage.get_data(batch_ids)
                    valid_texts = [text for text in batch_texts if text]
                    if valid_texts:
                        vectorizer.partial_fit(valid_texts)

                query_vec = vectorizer.transform([query])
                top_k = []

                for i in range(0, len(filtered_ids), window_size):
                    batch_ids = filtered_ids[i:i+window_size]
                    batch_texts = self.storage.get_data(batch_ids)

                    valid_texts_with_ids = [(doc_id, text) for doc_id, text in zip(batch_ids, batch_texts) if text]
                    if not valid_texts_with_ids:
                        continue

                    valid_ids = [doc_id for doc_id, _ in valid_texts_with_ids]
                    valid_texts = [text for _, text in valid_texts_with_ids]

                    matrix = vectorizer.transform(valid_texts)
                    scores = (matrix * query_vec.T).toarray().flatten()

                    for doc_id, score in zip(valid_ids, scores):
                        if len(top_k) < k:
                            heapq.heappush(top_k, (score, doc_id))
                        else:
                            heapq.heappushpop(top_k, (score, doc_id))

                top_k_ids_sorted = sorted(top_k, key=lambda x: x[0], reverse=True)
                doc_ids = [doc_id for score, doc_id in top_k_ids_sorted]
                top_docs = self.storage.get_data(doc_ids)
                metadatas = self.metadata_storage.get_data(doc_ids)
                return list(zip(doc_ids, top_docs, metadatas))
            else:
                all_texts = self.storage.get_data(filtered_ids)
                valid_texts_with_ids = [(doc_id, text) for doc_id, text in zip(filtered_ids, all_texts) if text]

                if not valid_texts_with_ids:
                    return []

                valid_ids = [doc_id for doc_id, _ in valid_texts_with_ids]
                valid_texts = [text for _, text in valid_texts_with_ids]

                vectorizer = sparse.BM25Vectorizer(ngram_range=(3, 5), analyzer="char_wb", normalize=True)
                matrix = vectorizer.fit_transform(valid_texts)
                query_vec = vectorizer.transform([query])

                scores = (matrix * query_vec.T).toarray().flatten()
                top_k_indices = scores.argsort()[-k:][::-1]

                result_ids = [valid_ids[i] for i in top_k_indices]
                result_texts = [valid_texts[i] for i in top_k_indices]
                metadatas = self.metadata_storage.get_data(result_ids)

                return list(zip(result_ids, result_texts, metadatas))
