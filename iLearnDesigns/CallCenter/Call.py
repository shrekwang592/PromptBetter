class Call:
    id_counter = 0

    def __init__(self):
        self.id = Call.id_counter
        self.handled = False
        Call.id_counter += 1

    def __repr__(self):
        return f"Call(id={self.id})"