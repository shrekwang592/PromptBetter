import time

class InMemoryDatabase:
    def __init__(self):
        self.records = {}

    def create_record(self, record_id, initial_data):
        self.records[record_id] = initial_data

    def get_record(self, record_id):
        return self.records.get(record_id, None)

    def update_record(self, record_id, field, value):
        if record_id in self.records:
            self.records[record_id][field] = value

    def delete_record(self, record_id):
        if record_id in self.records:
            del self.records[record_id]

    def filter_records(self, field, expected_value):
        return {record_id: record for record_id, record in self.records.items() 
                if field in record and record[field] == expected_value}

    def create_record_with_ttl(self, record_id, initial_data, ttl):
        expiry_time = time.time() + ttl
        self.records[record_id] = {'data': initial_data, 'expiry': expiry_time}

    def purge_expired_records(self):
        current_time = time.time()
        self.records = {record_id: record for record_id, record in self.records.items() 
                        if current_time < record['expiry']}

class RecordHistory:
    def __init__(self):
        self.history = []

    def add_entry(self, timestamp, data):
        self.history.append((timestamp, data))

    def get_past_state(self, timestamp):
        for past_time, past_data in reversed(self.history):
            if past_time <= timestamp:
                return past_data
        return None
    
def test_level_1():
    db = InMemoryDatabase()
    # Create a record
    db.create_record('123', {'balance': 500})
    assert '123' in db.records, "Test failed: Record not created."
    # Read the record
    record_value = db.get_record('123')
    assert record_value == {'balance': 500}, "Test failed: Record value mismatch."
    # Update the record
    db.update_record('123', 'balance', 600)
    assert db.records['123']['balance'] == 600, "Test failed: Record not updated."
    # Delete the record
    db.delete_record('123')
    assert '123' not in db.records, "Test failed: Record not deleted."
    print("Level 1 tests passed.")
# Call the test function for level 1
test_level_1()

def test_level_2():
    db = InMemoryDatabase()
    db.create_record('123', {'balance': 500, 'account_type': 'checking'})
    db.create_record('456', {'balance': 1500, 'account_type': 'savings'})
    # Filter records
    filtered_records = db.filter_records('account_type', 'checking')
    assert '123' in filtered_records and '456' not in filtered_records, "Test failed: Filter not working correctly."
    print("Level 2 tests passed.")
# Call the test function for level 2
test_level_2()

def test_level_3():
    db = InMemoryDatabase()
    db.create_record_with_ttl('123', {'balance': 500, 'type': 'checking'}, ttl=1)  # 1 second TTL
    assert '123' in db.records, "Test failed: TTL record not created."
    # We need to wait for the TTL to expire
    time.sleep(1.1)  # Wait a little more than 1 second
    db.purge_expired_records()
    assert '123' not in db.records, "Test failed: TTL record not purged."
    print("Level 3 tests passed.")
# Call the test function for level 3
test_level_3()

def test_level_4():
    db = InMemoryDatabase()
    db.create_record('123', RecordHistory())
    # Add historical data
    past_time = time.time() - 60  # 1 minute in the past
    db.records['123'].add_entry(past_time, {'balance': 500})
    # Add more recent data
    more_recent_time = time.time() - 30  # 30 seconds in the past
    db.records['123'].add_entry(more_recent_time, {'balance': 600})
    # Look back at the state of the record at a past timestamp
    old_state = db.records['123'].get_past_state(past_time + 10)  # Looking at 50 seconds ago
    assert old_state == {'balance': 500}, "Test failed: Incorrect past state retrieval."
    # Ensure that querying for a time before any data was logged returns None
    very_old_state = db.records['123'].get_past_state(past_time - 10)
    assert very_old_state is None, "Test failed: Should not retrieve state from before any data was logged."
    print("Level 4 tests passed.")
# Call the test function for level 4
test_level_4()