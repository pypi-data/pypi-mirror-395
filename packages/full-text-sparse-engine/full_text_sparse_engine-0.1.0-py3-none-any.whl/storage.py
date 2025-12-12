import lmdb, struct, pickle, os, atexit, xxhash

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

    def keys(self):
        for shard_db in self.shards.values():
            with shard_db.env.begin() as txn:
                cursor = txn.cursor()
                for key, _ in cursor:
                    yield key.decode('utf-8')

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
