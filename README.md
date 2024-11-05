Start up each node in the cluster (different process or machine) python -m raft_consensus --config=config.json <node-name> where node-name is the name of a node defined in your config.


Start sending commands to the leader python -m raft_consensus --leader=localhost:12000 SET <bucket> <key> <value>

SET	<bucket>, <key>, <value>	Sets a key with value in the bucket. This command will implictly create the bucket. Returns OK on success.
SET fruits apples 3

GET	<bucket>, <key>	Gets the value for key stored in the bucket. Returns the stored value on success or None.
GET fruits apples

DEL	<bucket>, <key>	Deletes a key and associated value from the bucket. Returns OK on success or NO_KEY if the key doesn't exist.
DEL fruits apples

KEYS	<bucket>	Lists all the keys in the bucket.
KEYS fruits

DELBUCKET	<bucket>	Deletes a bucket and all key value pairs associated with it. Returns OK on success or NO_BUCKET if the bucket doesn't exist.
DELBUCKET fruits

BUCKETS		Lists all the buckets that exist.
BUCKETS