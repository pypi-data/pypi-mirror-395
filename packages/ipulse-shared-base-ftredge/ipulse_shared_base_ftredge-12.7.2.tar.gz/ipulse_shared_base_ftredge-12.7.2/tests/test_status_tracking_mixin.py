import unittest
from ipulse_shared_base_ftredge import ProgressStatus, StatusTrackingMixin

class TestStatusTracker(StatusTrackingMixin):
    """Simple class for testing the mixin"""
    def __init__(self, name: str = "test"):
        super().__init__()
        self.name = name

class TestStatusTrackingMixin(unittest.TestCase):
    def setUp(self):
        self.tracker = TestStatusTracker()

    def test_initial_state(self):
        """Test initial state of mixin"""
        self.assertEqual(self.tracker.progress_status, ProgressStatus.NOT_STARTED)
        self.assertEqual(self.tracker.issues, [])
        self.assertEqual(self.tracker.warnings, [])
        self.assertEqual(self.tracker.notices, [])
        self.assertEqual(self.tracker.metadata, {})
        self.assertEqual(self.tracker.statuses_aggregated, 1)

    def test_progress_status_transitions(self):
        """Test status transitions"""
        # Test string status setting
        self.tracker.progress_status = "IN_PROGRESS"
        self.assertEqual(self.tracker.progress_status, ProgressStatus.IN_PROGRESS)

        # Test enum status setting
        self.tracker.progress_status = ProgressStatus.DONE
        self.assertEqual(self.tracker.progress_status, ProgressStatus.DONE)

    def test_add_issues_warnings_notices(self):
        """Test adding issues/warnings/notices"""
        self.tracker.add_issue("test issue")
        self.tracker.add_warning("test warning")
        self.tracker.add_notice("test notice")

        self.assertEqual(len(self.tracker.issues), 1)
        self.assertEqual(len(self.tracker.warnings), 1)
        self.assertEqual(len(self.tracker.notices), 1)
        self.assertEqual(len(self.tracker.execution_state), 3)  # One state entry per add

    def test_metadata_management(self):
        """Test metadata operations"""
        self.tracker.add_metadata(key1="value1")
        self.assertEqual(self.tracker.metadata["key1"], "value1")

        self.tracker.add_metadata_from_dict({"key2": "value2"})
        self.assertEqual(self.tracker.metadata["key2"], "value2")

    def test_statuses_aggregation(self):
        """Test status aggregation"""
        self.tracker.increment_statuses_aggregated(2)
        self.assertEqual(self.tracker.statuses_aggregated, 3)

        self.tracker.statuses_aggregated = 5
        self.assertEqual(self.tracker.statuses_aggregated, 5)

    def test_integrate_status_tracker(self):
        """Test integration of another status tracker"""
        other = TestStatusTracker("other")
        other.add_issue("other issue")
        other.add_warning("other warning")
        other.progress_status = ProgressStatus.FAILED
        other.add_metadata(other_key="other_value")

        self.tracker.integrate_status_tracker(
            next=other,
            skip_metadata=False,
            name="other_tracker"
        )

        # Check status was combined
        self.assertEqual(self.tracker.progress_status, ProgressStatus.FAILED)
        
        # Check issues/warnings were merged
        self.assertEqual(len(self.tracker.issues), 1)
        self.assertEqual(len(self.tracker.warnings), 1)
        print(self.tracker.metadata.keys())
        # Check metadata was merged
        self.assertEqual(self.tracker.metadata["other_tracker>other_key"], "other_value")
        
        # Check status count was incremented
        self.assertEqual(self.tracker.statuses_aggregated, 2)

    def test_status_checks(self):
        """Test status check properties"""
        self.tracker.progress_status = ProgressStatus.DONE
        self.assertTrue(self.tracker.is_success)
        self.assertTrue(self.tracker.is_closed)

        self.tracker.progress_status = ProgressStatus.FAILED
        self.assertFalse(self.tracker.is_success)
        self.assertTrue(self.tracker.is_closed)

        self.tracker.progress_status = ProgressStatus.IN_PROGRESS
        self.assertFalse(self.tracker.is_success)
        self.assertFalse(self.tracker.is_closed)

if __name__ == '__main__':
    unittest.main()
