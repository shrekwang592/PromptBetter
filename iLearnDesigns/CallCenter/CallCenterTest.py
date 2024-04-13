import unittest

from Call import Call
from CallHandler import CallHandler

class CallCenterTest(unittest.TestCase):
    def setUp(self):
        # Initialize the call center before each test
        self.call_center = CallHandler()

    def simulate_calls(self, num_calls):
        # Helper function to simulate multiple calls
        for _ in range(num_calls):
            self.call_center.dispatch_call(Call())

    def test_initial_operator_dispatch(self):
        # Test that the initial calls are dispatched to operators
        self.simulate_calls(5)
        self.assertTrue(all(not operator.available for operator in self.call_center.operators))
        self.assertTrue(all(supervisor.available for supervisor in self.call_center.supervisors))
        self.assertTrue(all(director.available for director in self.call_center.directors))

    def test_supervisor_escalation(self):
        # Test that additional calls are escalated to supervisors
        self.simulate_calls(6)
        self.assertFalse(self.call_center.supervisors[0].available)
        self.assertTrue(all(supervisor.available for supervisor in self.call_center.supervisors[1:]))  # Assuming more than one supervisor

    def test_director_escalation(self):
        # Test that when supervisors are busy, calls are escalated to directors
        self.simulate_calls(7)
        self.assertTrue(self.call_center.directors[0].available)

    def test_queueing_when_all_busy(self):
        # Test that when all employees are busy, calls are queued
        self.simulate_calls(9)
        self.assertEqual(len(self.call_center.call_queue), 1)

    def test_call_finished_and_queue_processed(self):
        # Test that when operators become available, queued calls are dispatched
        self.simulate_calls(9)
        # Finish the call for the first operator
        self.call_center.call_finished(self.call_center.operators[0])
        # Queue should have been processed and first operator reassigned
        self.assertFalse(self.call_center.operators[0].available)
        self.assertEqual(len(self.call_center.call_queue), 0)

    def tearDown(self):
        # Clean up actions if necessary after each test
        pass

if __name__ == '__main__':
    unittest.main()