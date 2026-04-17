from redis import Redis
from rq import Queue

# 1. Establish the connection
redis_conn = Redis(host="localhost", port=6379)

# 2. Test the connection!
try:
    # This sends a RESP "PING" command to Valkey
    response = redis_conn.ping() 
    if response:
        print("✅ Successfully connected to Valkey!")
except Exception as e:
    print(f"❌ Connection failed: {e}")

# 3. Pass the verified connection to RQ
queue = Queue(connection=redis_conn)