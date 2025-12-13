import unittest
from datetime import datetime, timezone
from ipulse_shared_base_ftredge import ProgressStatus
from ipulse_shared_data_eng_ftredge import FunctionResult

class TestFunctionResult(unittest.TestCase):
    def setUp(self):
        self.result = FunctionResult(name="test_function")

    def test_initial_state(self):
        """Test initial state of FunctionResult"""
        self.assertEqual(self.result.name, "test_function")
        self.assertEqual(self.result.progress_status, ProgressStatus.IN_PROGRESS)  # Different from mixin default
        self.assertIsNone(self.result.data)
        self.assertEqual(self.result.duration_s, 0.0)

        self.assertIsInstance(self.result.start_time, datetime)
        self.assertEqual(len(self.result.issues), 0)
        self.assertEqual(self.result.statuses_aggregated, 1)


    def test_data_handling(self):
        """Test data operations"""
        # Test direct data setting
        self.result.data = {"key": "value"}
        self.assertEqual(self.result.data["key"], "value")

        # Test adding data
        self.result.add_data("new_value", "new_key")
        self.assertEqual(self.result.data["new_key"], "new_value")

        # Test invalid data addition
        self.result.data = "string"
        with self.assertRaises(ValueError):
            self.result.add_data("value", "key")

    def test_integrate_result(self):
        """Test integration of another FunctionResult"""
        child = FunctionResult(name="child_function")
        child.data = {"child_key": "child_value"}
        child.add_issue("child issue")
        child.progress_status = ProgressStatus.FAILED
        child.add_metadata(child_meta="child_value")

        # Test integration with all flags
        self.result.integrate_result(
            child_result=child, 
            combine_status=True,
            issues_allowed=True,
            skip_data=False,
            skip_metadata=False
        )


        # Check status was combined
        self.assertEqual(self.result.progress_status, ProgressStatus.IN_PROGRESS_WITH_ISSUES)
        self.assertEqual(self.result.statuses_aggregated, 2)
        # Check data was merged
        
        self.assertEqual(self.result.data["child_key"], "child_value")
        
        # Check issues were merged (from StatusTrackingMixin)
        self.assertEqual(len(self.result.issues), 1)
        
        # Check metadata was merged (from StatusTrackingMixin)
        print(self.result.metadata.keys())
        self.assertEqual(self.result.metadata["child>child_function>child_meta"], "child_value")

    def test_final_status(self):
        """Test final status calculation"""
        # Test explicit status
        self.result.final(force_status=ProgressStatus.DONE)
        self.assertEqual(self.result.progress_status, ProgressStatus.DONE)

        # Test status based on issues
        result2 = FunctionResult()
        result2.add_issue("test issue")
        result2.final(issues_allowed=True)
        self.assertEqual(result2.progress_status, ProgressStatus.FINISHED_WITH_ISSUES)

        result2b = FunctionResult()
        result2b.add_issue("test issue")
        result2b.final(issues_allowed=False)
        self.assertEqual(result2b.progress_status, ProgressStatus.FAILED)

        # Test status based on warnings
        result3 = FunctionResult()
        result3.add_warning("test warning")
        result3.final()
        self.assertEqual(result3.progress_status, ProgressStatus.DONE_WITH_WARNINGS)

        

    def test_duration_calculation(self):
        """Test duration calculation"""
        self.result.calculate_duration()
        self.assertGreater(self.result.duration_s, 0)

if __name__ == '__main__':
    unittest.main()