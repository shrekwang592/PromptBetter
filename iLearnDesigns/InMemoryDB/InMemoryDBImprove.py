class InMemoryDatabaseLevel1:
    def __init__(self):
        self.records = {}
        self.expiry_times = {}  # Maps record IDs to their expiry times
        self.history = {} 
    def set_value(self, timestamp, key, field, value):
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
        current_time = time.time()
        for key, expiry_time in self.expiry_times.items():
            if current_time >= expiry_time:
                del self.records[key]
                del self.history[key]  # Also delete the history when record is expired
        self.expiry_times = {k: v for k, v in self.expiry_times.items() if k in self.records}

    def set_value_with_ttl(self, timestamp, key, field, value, ttl):
        self.set_value(timestamp, key, field, value)  # Set the value normally
        self.expiry_times[key] = time.time() + ttl  # Set the expiry time

    def get_value_at_timestamp(self, timestamp, key, field):
        if key in self.history:
            for time_key, past_record in reversed(self.history[key]):
                if time_key <= timestamp:
                    return past_record.get(field, "")
        return ""

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

# Process the queries and print the results
process_results = process_queries(queries)
print(process_results)  