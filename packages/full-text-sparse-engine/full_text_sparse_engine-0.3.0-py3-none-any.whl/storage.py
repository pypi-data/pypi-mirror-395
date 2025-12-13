import lmdb, struct, pickle, os, atexit, xxhash, heapq

class LmdbStorage:
    def __init__(self, path, map_size=50*1024*1024*1024): # e.g. 50GB by default
        self.env = lmdb.open(path, map_size=map_size)
        atexit.register(self.close)

    def _int_to_bytes(self, x):
        """
        Converts an integer to 8-byte signed little-endian format.
        If x is outside the signed 64-bit range, wraps it safely.
        """
        MAX_UINT64 = 2**64
        MAX_INT64 = 2**63

        # Ensure x is within 0 to 2^64 - 1
        x = x % MAX_UINT64

        # Convert to signed range if necessary
        if x >= MAX_INT64:
            x -= MAX_UINT64

        return struct.pack('<q', x)

    def store_data(self, data, identifiers, batch_size=5000):
        total = len(data)
        with self.env.begin(write=True) as txn:
            for i in range(0, total, batch_size):
                batch_data = data[i:i+batch_size]
                batch_ids = identifiers[i:i+batch_size]
                with txn.cursor() as curs:
                    for vec, id in zip(batch_data, batch_ids):
                        curs.put(
                            self._int_to_bytes(id) if isinstance(id, int) else id.encode(),
                            pickle.dumps(vec)
                        )

    def get_data(self, identifiers):
        datas = []
        with self.env.begin() as txn:
            for id in identifiers:
                data = txn.get(self._int_to_bytes(id) if isinstance(id, int) else id.encode())
                if data:
                    datas.append(pickle.loads(data))
                else:
                    datas.append(None)
        return [ v for v in datas if v is not None ]
    
    def delete_data(self, identifiers):
        with self.env.begin(write=True) as txn:
            for id in identifiers:
                txn.delete(self._int_to_bytes(id) if isinstance(id, int) else id.encode())

    def get_data_count(self):
        with self.env.begin() as txn:
            return txn.stat()['entries']

    def sync(self):
        self.env.sync()

    def close(self):
        self.env.close()

    def keys_with_prefix(self, prefix):
        with self.env.begin() as txn:
            cursor = txn.cursor()
            if cursor.set_range(prefix.encode()):
                for key_bytes, _ in cursor:
                    key = key_bytes.decode()
                    if key.startswith(prefix):
                        yield key
                    else:
                        break

    def items_in_range(self, start_key, end_key, prefix):
        with self.env.begin() as txn:
            cursor = txn.cursor()
            # Start scanning from the first key that is >= start_key
            if cursor.set_range(start_key.encode()):
                for key_bytes, value_bytes in cursor:
                    key = key_bytes.decode()

                    # Ensure the key is still within the desired prefix
                    if not key.startswith(prefix):
                        break

                    # If the current key is at or after the end_key, we're done
                    if key >= end_key:
                        break

                    yield key, pickle.loads(value_bytes)

    def batch_atomic_update(self, updates, merge_func):
        """
        Performs updates for multiple keys in a single transaction.
        :param updates: Dictionary {key: new_data_partial}
        :param merge_func: Function (existing_value, new_data_partial) -> to_store_value
        """
        with self.env.begin(write=True) as txn:
            cursor = txn.cursor()
            for key, new_data in updates.items():
                key_bytes = key.encode('utf-8')
                current_val_bytes = cursor.get(key_bytes)
                current_val = pickle.loads(current_val_bytes) if current_val_bytes else None
                
                final_val = merge_func(current_val, new_data)
                
                cursor.put(key_bytes, pickle.dumps(final_val))

class ShardedLmdbStorage:
    """
    A sharded wrapper for LmdbStorage that splits data across multiple shards.
    Each shard is an instance of LmdbStorage stored in a subdirectory under a base path.
    """
    def __init__(self, base_path, num_shards=5, map_size=70*1024*1024*1024):
        """
        :param base_path: Base directory where shard subdirectories will be created.
        :param num_shards: Number of shards.
        :param map_size: Map size for each LMDB environment.
        """
        self.num_shards = num_shards
        self.shards = {}
        for shard_idx in range(num_shards):
            shard_path = os.path.join(base_path, f"shard_{shard_idx}")
            os.makedirs(shard_path, exist_ok=True)
            self.shards[shard_idx] = LmdbStorage(shard_path, map_size=map_size)

    def _get_shard_for_id(self, identifier):
        identifier_str = str(identifier).encode('utf-8')
        h = xxhash.xxh64(identifier_str).hexdigest()
        return int(h, 16) % self.num_shards

    def store_data(self, data, identifiers, batch_size=5000):
        """
        Stores data items by grouping them by shard.
        """
        # Group data and identifiers by shard index
        shard_data = {i: [] for i in range(self.num_shards)}
        shard_ids = {i: [] for i in range(self.num_shards)}
        for vec, identifier in zip(data, identifiers):
            shard = self._get_shard_for_id(identifier)
            shard_data[shard].append(vec)
            shard_ids[shard].append(identifier)
        # Call store_data on each shard that has items
        for shard, lmdb_storage in self.shards.items():
            if shard_data[shard]:
                lmdb_storage.store_data(shard_data[shard], shard_ids[shard], batch_size=batch_size)
    
    def get_data(self, identifiers):
        """
        Retrieves data items by grouping identifiers by shard.
        Returns a list of found data in the same order as identifiers.
        """
        id_to_data = {}
        shard_ids = {i: [] for i in range(self.num_shards)}
        for identifier in identifiers:
            shard = self._get_shard_for_id(identifier)
            shard_ids[shard].append(identifier)
        for shard, lmdb_storage in self.shards.items():
            if shard_ids[shard]:
                data_list = lmdb_storage.get_data(shard_ids[shard])
                for identifier, data in zip(shard_ids[shard], data_list):
                    id_to_data[identifier] = data
        return [id_to_data.get(identifier, None) for identifier in identifiers]

    def delete_data(self, identifiers):
        """
        Deletes data items by grouping identifiers by shard.
        """
        shard_ids = {i: [] for i in range(self.num_shards)}
        for identifier in identifiers:
            shard = self._get_shard_for_id(identifier)
            shard_ids[shard].append(identifier)
        for shard, lmdb_storage in self.shards.items():
            if shard_ids[shard]:
                lmdb_storage.delete_data(shard_ids[shard])

    def get_data_count(self):
        """
        Returns the total count of entries across all shards.
        """
        total = 0
        for lmdb_storage in self.shards.values():
            total += lmdb_storage.get_data_count()
        return total

    def atomic_update(self, key, update_function):
        shard_idx = self._get_shard_for_id(key)
        shard_db = self.shards[shard_idx]
        with shard_db.env.begin(write=True) as txn:
            current_value_bytes = txn.get(key.encode('utf-8'))
            current_value = pickle.loads(current_value_bytes) if current_value_bytes else None
            new_value = update_function(current_value)
            txn.put(key.encode('utf-8'), pickle.dumps(new_value))

    def batch_atomic_update(self, updates, merge_func):
        """
        Efficiently updates multiple keys across necessary shards.
        Grouping by shard ensures we only open one transaction per shard.
        """
        shard_updates = {i: {} for i in range(self.num_shards)}
        
        for key, val in updates.items():
            shard_idx = self._get_shard_for_id(key)
            shard_updates[shard_idx][key] = val
            
        for shard_idx, shard_data in shard_updates.items():
            if shard_data:
                self.shards[shard_idx].batch_atomic_update(shard_data, merge_func)

    def keys(self):
        for shard_db in self.shards.values():
            with shard_db.env.begin() as txn:
                cursor = txn.cursor()
                for key, _ in cursor:
                    yield key.decode('utf-8')

    def keys_with_prefix(self, prefix):
        for shard_db in self.shards.values():
            yield from shard_db.keys_with_prefix(prefix)

    def items_in_range(self, start_key, end_key, prefix):
        iterators = [shard_db.items_in_range(start_key, end_key, prefix) for shard_db in self.shards.values()]
        yield from heapq.merge(*iterators, key=lambda x: x[0])

    def sync(self):
        """
        Synchronizes all LMDB environments.
        """
        for lmdb_storage in self.shards.values():
            lmdb_storage.sync()

    def close(self):
        """
        Closes all LMDB environments.
        """
        for lmdb_storage in self.shards.values():
            lmdb_storage.close()