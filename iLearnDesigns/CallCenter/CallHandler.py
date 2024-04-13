from Employee import Director, Operator, Supervisor

class CallHandler:
    def __init__(self):
        self.operators = [Operator('Operator_' + str(i)) for i in range(5)]
        self.supervisors = [Supervisor('Supervisor_' + str(i)) for i in range(2)]
        self.directors = [Director('Director_' + str(i)) for i in range(1)]
        self.call_queue = []

    def dispatch_call(self, call):
        # Try to handle the call with an available operator
        for operator in self.operators:
            if operator.available:
                operator.take_call(call)
                return True
        
        # If no operator is available, escalate to supervisor
        for supervisor in self.supervisors:
            if supervisor.available:
                supervisor.take_call(call)
                return True
        
        # If no supervisor is available, escalate to director
        for director in self.directors:
            if director.available:
                director.take_call(call)
                return True
        
        # If no one is available, add to queue
        self.call_queue.append(call)
        return False

    def queue_next_call(self):
        # Dispatch next call in the queue if possible
        if self.call_queue:
            next_call = self.call_queue.pop(0)
            self.dispatch_call(next_call)

    def call_finished(self, employee):
        # An employee finished a call. They become available.
        employee.finish_call()
        # Check if there is a call in the queue
        self.queue_next_call()
