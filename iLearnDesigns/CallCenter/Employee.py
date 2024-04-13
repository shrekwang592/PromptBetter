class Employee:
    def __init__(self, name):
        self.name = name
        self.available = True

    def take_call(self, call):
        # Implementation of handling a call
        self.available = False

    def finish_call(self):
        # Free up the employee after finishing call
        self.available = True

    def escalate_call(self, call):
        # Implementation of escalating a call to the next level
        pass

class Operator(Employee):
    pass

class Supervisor(Employee):
    pass

class Director(Employee):
    pass

