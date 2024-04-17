class InMemoryDatabaseLevel1:
    def __init__(self):
        # For Level 1
        self.records = {}
         # For Level 3
        self.expiry_times = {}  # Maps record IDs to their expiry times
        # For Level 4
        self.history = {} 
    def set_value(self, timestamp, key, field, value):
        # Implement Level 4: Store history of value updates
        if key not in self.history:
            self.history[key] = []

        if key not in self.records:
            self.records[key] = {}

        self.records[key][field] = value
        self.history[key].append((timestamp, self.records[key].copy()))
        
        return ""

    def compare_and_set(self, timestamp, key, field, expected_value, new_value):
        if key in self.records and field in self.records[key] and self.records[key][field] == expected_value:
            self.records[key][field] = new_value
            return "true"
        return "false"

    def compare_and_delete(self, timestamp, key, field, expected_value):
        if key in self.records and field in self.records[key] and self.records[key][field] == expected_value:
            del self.records[key][field]
            if not self.records[key]:  # Check if record is empty after deletion and remove it if so
                del self.records[key]
            return "true"
        return "false"

    def get_value(self, timestamp, key, field):
        if key in self.records and field in self.records[key]:
            return str(self.records[key][field])
        return ""
    
    def purge_expired_records(self):
        # Implement Level 3: Purge expired records
        current_time = time.time()
        for key, expiry_time in self.expiry_times.items():
            if current_time >= expiry_time:
                del self.records[key]
                del self.history[key]  # Also delete the history when record is expired
        self.expiry_times = {k: v for k, v in self.expiry_times.items() if k in self.records}

    def set_value_with_ttl(self, timestamp, key, field, value, ttl):
        # For Level 3: Records with Time-to-Live
        self.set_value(timestamp, key, field, value)  # Set the value normally
        self.expiry_times[key] = time.time() + ttl  # Set the expiry time

    def get_value_at_timestamp(self, timestamp, key, field):
        # For Level 4: Getting historical value
        if key in self.history:
            for time_key, past_record in reversed(self.history[key]):
                if time_key <= timestamp:
                    return past_record.get(field, "")
        return ""
# Test function would need to be expanded to account for time-based actions (e.g. waiting for TTL expiry).
# Given operations now require timestamps, we'll need a way to generate them for Level 3+ tests.
# In Level 4, our testing would involve looking at the history state at different points in time.

# These tests would be more complicated due to the asynchronous nature of TTL expiry and the need to query past states.
# For a realistic test, you might have functions to simulate the passing of time and the purging of records.

# The updated `process_queries` function is expected to handle Level 3 and 4 capabilities.

# Helper function to process the queries.
def process_queries(queries):
    db = InMemoryDatabaseLevel1()
    results = []

    for query in queries:
        operation = query[0]
        timestamp = query[1]
        key = query[2]
        field = query[3]

        if operation == "SET":
            value = query[4]
            result = db.set_value(timestamp, key, field, value)
        elif operation == "COMPARE_AND_SET":
            expected_value, new_value = query[4], query[5]
            result = db.compare_and_set(timestamp, key, field, expected_value, new_value)
        elif operation == "COMPARE_AND_DELETE":
            expected_value = query[4]
            result = db.compare_and_delete(timestamp, key, field, expected_value)
        elif operation == "GET":
            result = db.get_value(timestamp, key, field)

        results.append(result)

    return results

# Example usage:
queries = [
    ["SET", "0", "A", "B", 4],
    ["SET", "1", "A", "C", 6],
    ["COMPARE_AND_SET", "2", "A", "B", 4, 9],
    ["COMPARE_AND_SET", "3", "A", "C", 4, 9],
    ["COMPARE_AND_DELETE", "4", "A", "C", 6]
]

# Process the queries and print the results
process_results = process_queries(queries)
print(process_results)  # Output: ['', '', 'true', 'false', 'true']