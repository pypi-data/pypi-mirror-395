import unittest
from ipulse_shared_base_ftredge import ProgressStatus, StatusCounts

class TestStatusCounts(unittest.TestCase):
    def setUp(self):
        self.status_counts = StatusCounts()

    def test_empty_status_counts(self):
        """Test initial state of StatusCounts"""
        self.assertEqual(self.status_counts.total_count, 0)
        self.assertEqual(len(self.status_counts.by_status_count), 0)
        self.assertEqual(len(self.status_counts.by_category_count), 0)
        self.assertEqual(self.status_counts.completion_rate, 0.0)
        self.assertEqual(self.status_counts.success_rate, 0.0)

    def test_add_single_status(self):
        """Test adding a single status"""
        self.status_counts.add_status(ProgressStatus.DONE)
        self.assertEqual(self.status_counts.total_count, 1)
        self.assertEqual(self.status_counts.by_status_count[ProgressStatus.DONE], 1)
        self.assertEqual(self.status_counts.get_category_count('success_statuses'), 1)

    def test_add_multiple_statuses(self):
        """Test adding multiple statuses"""
        statuses = [ProgressStatus.DONE, ProgressStatus.IN_PROGRESS, ProgressStatus.FAILED]
        self.status_counts.add_statuses(statuses)
        self.assertEqual(self.status_counts.total_count, 3)
        self.assertEqual(self.status_counts.get_category_count('success_statuses'), 1)
        self.assertEqual(self.status_counts.get_category_count('pending_statuses'), 1)
        self.assertEqual(self.status_counts.get_category_count('failure_statuses'), 1)

    def test_remove_status(self):
        """Test removing a status"""
        self.status_counts.add_status(ProgressStatus.DONE)
        self.status_counts.remove_status(ProgressStatus.DONE)
        self.assertEqual(self.status_counts.total_count, 0)
        self.assertEqual(self.status_counts.by_status_count[ProgressStatus.DONE], 0)
        self.assertEqual(self.status_counts.get_category_count('success_statuses'), 0)

    def test_category_counts(self):
        """Test category counting logic"""
        status_map = {
            ProgressStatus.IN_PROGRESS: 'pending_statuses',
            ProgressStatus.DONE: 'success_statuses',
            ProgressStatus.FAILED: 'failure_statuses',
            ProgressStatus.INTENTIONALLY_SKIPPED: 'skipped_statuses'
        }

        for status, category in status_map.items():
            self.status_counts.add_status(status)
            self.assertEqual(self.status_counts.get_category_count(category), 1)


    def test_has_properties(self):
        """Test boolean status properties"""
        # Test has_failures
        self.status_counts.add_status(ProgressStatus.FAILED)
        self.assertTrue(self.status_counts.has_failures)

        # Test has_issues
        self.status_counts.add_status(ProgressStatus.FINISHED_WITH_ISSUES)
        self.assertTrue(self.status_counts.has_issues)

        # Test has_warnings
        self.status_counts.add_status(ProgressStatus.DONE_WITH_WARNINGS)
        self.assertTrue(self.status_counts.has_warnings)

        # Test has_notices
        self.status_counts.add_status(ProgressStatus.DONE_WITH_NOTICES)
        self.assertTrue(self.status_counts.has_notices)

    def test_completion_and_success_rates(self):
        """Test completion and success rate calculations"""
        # Add mix of statuses
        self.status_counts.add_statuses([
            ProgressStatus.DONE,  # Success
            ProgressStatus.IN_PROGRESS,  # Pending
            ProgressStatus.FAILED,  # Closed
            ProgressStatus.INTENTIONALLY_SKIPPED  # Skipped
        ])

        # Expected rates
        expected_completion = (3 / 4) * 100  # DONE , FAILED  and INTENTIONALLY_SKIPPED are closed/skipped
        expected_success = (1 / 4) * 100  # Only DONE is success

        self.assertEqual(self.status_counts.completion_rate, expected_completion)
        self.assertEqual(self.status_counts.success_rate, expected_success)

    def test_to_status_set(self):
        """Test conversion to status set"""
        original_statuses = [
            ProgressStatus.DONE,
            ProgressStatus.DONE,  # Duplicate will be combined in set
            ProgressStatus.IN_PROGRESS
        ]
        for status in original_statuses:
            self.status_counts.add_status(status)

        status_set = self.status_counts.to_status_set()
        self.assertEqual(len(status_set), 2)  # Should be 2 unique statuses
        self.assertTrue(ProgressStatus.DONE in status_set)
        self.assertTrue(ProgressStatus.IN_PROGRESS in status_set)



if __name__ == '__main__':
    unittest.main()
