
import unittest
from ipulse_shared_base_ftredge import ProgressStatus, StatusCounts, eval_statuses

class TestEvalStatus(unittest.TestCase):
    def test_empty_input(self):
        """Test evaluation of empty input"""
        self.assertEqual(eval_statuses([]), ProgressStatus.NOT_STARTED)
        self.assertEqual(eval_statuses(set()), ProgressStatus.NOT_STARTED)
        self.assertEqual(eval_statuses(StatusCounts()), ProgressStatus.NOT_STARTED)

    def test_all_skipped(self):
        """Test when all statuses are skipped"""
        skipped_statuses = [
            ProgressStatus.INTENTIONALLY_SKIPPED,
            ProgressStatus.DISABLED
        ]
        self.assertEqual(eval_statuses(skipped_statuses), ProgressStatus.INTENTIONALLY_SKIPPED)

    def test_all_disabled(self):
        """Test when all statuses are disabled"""
        disabled_statuses = [
            ProgressStatus.DISABLED,
            ProgressStatus.DISABLED
        ]
        self.assertEqual(eval_statuses(disabled_statuses), ProgressStatus.DISABLED)

    def test_all_pending(self):
        """Test when all statuses are pending"""
        pending_statuses = [
            ProgressStatus.NOT_STARTED,
            ProgressStatus.IN_PROGRESS,
            ProgressStatus.STARTED
        ]
        self.assertEqual(eval_statuses(pending_statuses), ProgressStatus.IN_PROGRESS)



    def test_issues_allowed_with_fail_if_pending(self):

        self.assertEqual(
            eval_statuses([ProgressStatus.FINISHED_WITH_ISSUES, ProgressStatus.INTENTIONALLY_SKIPPED], fail_or_unfinish_if_any_pending=True, issues_allowed=True),
            ProgressStatus.FINISHED_WITH_ISSUES
        )
        self.assertEqual(
            eval_statuses([ProgressStatus.DONE, ProgressStatus.INTENTIONALLY_SKIPPED], fail_or_unfinish_if_any_pending=True, issues_allowed=True),
            ProgressStatus.DONE
        )

        self.assertEqual(
            eval_statuses([ProgressStatus.DONE, ProgressStatus.UNFINISHED], fail_or_unfinish_if_any_pending=True, issues_allowed=True),
            ProgressStatus.UNFINISHED
        )

        self.assertEqual(
            eval_statuses([ProgressStatus.DONE, ProgressStatus.UNFINISHED], fail_or_unfinish_if_any_pending=True, issues_allowed=False),
            ProgressStatus.UNFINISHED
        )

        self.assertEqual(
            eval_statuses([ProgressStatus.DONE, ProgressStatus.UNFINISHED, ProgressStatus.BLOCKED_BY_UNRESOLVED_DEPENDENCY], fail_or_unfinish_if_any_pending=True, issues_allowed=True),
            ProgressStatus.UNFINISHED
        )

        self.assertEqual(
            eval_statuses([ProgressStatus.DONE, ProgressStatus.UNFINISHED, ProgressStatus.FAILED ], fail_or_unfinish_if_any_pending=True, issues_allowed=True),
            ProgressStatus.FAILED
        )
        self.assertEqual(
            eval_statuses([ProgressStatus.DONE, ProgressStatus.FAILED ], fail_or_unfinish_if_any_pending=True, issues_allowed=True),
            ProgressStatus.FINISHED_WITH_ISSUES
        )

        self.assertEqual(
            eval_statuses([ProgressStatus.FAILED, ProgressStatus.DONE], fail_or_unfinish_if_any_pending=True, issues_allowed=False),
            ProgressStatus.FAILED
        )

        self.assertEqual(
            eval_statuses([ProgressStatus.FINISHED_WITH_ISSUES, ProgressStatus.DONE], fail_or_unfinish_if_any_pending=True, issues_allowed=True),
            ProgressStatus.FINISHED_WITH_ISSUES
        )

        self.assertEqual(
            eval_statuses([ProgressStatus.FINISHED_WITH_ISSUES, ProgressStatus.DONE], fail_or_unfinish_if_any_pending=True, issues_allowed=False),
            ProgressStatus.FINISHED_WITH_ISSUES
        )

        self.assertEqual(
            eval_statuses([ProgressStatus.DONE, ProgressStatus.UNFINISHED, ProgressStatus.FINISHED_WITH_ISSUES ], fail_or_unfinish_if_any_pending=True, issues_allowed=True),
            ProgressStatus.FAILED
        )


        self.assertEqual(
            eval_statuses([ProgressStatus.FAILED, ProgressStatus.BLOCKED_BY_UNRESOLVED_DEPENDENCY], fail_or_unfinish_if_any_pending=True, issues_allowed=True),
            ProgressStatus.FAILED
        )

        self.assertEqual(
            eval_statuses([ProgressStatus.FAILED, ProgressStatus.BLOCKED_BY_UNRESOLVED_DEPENDENCY], fail_or_unfinish_if_any_pending=True, issues_allowed=False),
            ProgressStatus.FAILED
        )

        self.assertEqual(
            eval_statuses([ProgressStatus.FINISHED_WITH_ISSUES, ProgressStatus.BLOCKED_BY_UNRESOLVED_DEPENDENCY], fail_or_unfinish_if_any_pending=True, issues_allowed=True),
            ProgressStatus.FAILED
        )

        self.assertEqual(
            eval_statuses([ProgressStatus.FINISHED_WITH_ISSUES, ProgressStatus.BLOCKED_BY_UNRESOLVED_DEPENDENCY], fail_or_unfinish_if_any_pending=True, issues_allowed=False),
            ProgressStatus.FAILED
        )

      
        self.assertEqual(
            eval_statuses([ProgressStatus.FAILED, ProgressStatus.IN_PROGRESS], fail_or_unfinish_if_any_pending=True, issues_allowed=True),
            ProgressStatus.FAILED
        )

        self.assertEqual(
            eval_statuses([ProgressStatus.FAILED, ProgressStatus.IN_PROGRESS], fail_or_unfinish_if_any_pending=True, issues_allowed=False),
            ProgressStatus.FAILED
        )

        # Mixed Success with Warnings = DONE_WITH_WARNINGS
        self.assertEqual(
            eval_statuses([ProgressStatus.DONE, ProgressStatus.DONE_WITH_WARNINGS], fail_or_unfinish_if_any_pending=True, issues_allowed=True),
            ProgressStatus.DONE_WITH_WARNINGS
        )

        self.assertEqual(
            eval_statuses([ProgressStatus.DONE, ProgressStatus.DONE_WITH_WARNINGS], fail_or_unfinish_if_any_pending=True, issues_allowed=False),
            ProgressStatus.DONE_WITH_WARNINGS
        )
        


        self.assertEqual(
            eval_statuses([ProgressStatus.DONE, ProgressStatus.IN_PROGRESS_WITH_ISSUES], fail_or_unfinish_if_any_pending=True, issues_allowed=True),
            ProgressStatus.FAILED # fail_or_unfinish_if_any_pending is evaluated first and all not finished fail_or_unfinish_if_any_pendings are considered as FAILED
        )

        self.assertEqual(
            eval_statuses([ProgressStatus.DONE, ProgressStatus.IN_PROGRESS_WITH_ISSUES], fail_or_unfinish_if_any_pending=True, issues_allowed=False),
            ProgressStatus.FAILED
        )

        self.assertEqual(
            eval_statuses([ProgressStatus.DONE, ProgressStatus.IN_PROGRESS_WITH_WARNINGS], fail_or_unfinish_if_any_pending=True, issues_allowed=True),
            ProgressStatus.UNFINISHED
        )

        self.assertEqual(
            eval_statuses([ProgressStatus.DONE, ProgressStatus.IN_PROGRESS_WITH_WARNINGS], fail_or_unfinish_if_any_pending=True, issues_allowed=False),
            ProgressStatus.UNFINISHED
        )
############################################################################################################

    def test_issues_allowed_non_fail_or_unfinish_if_any_pending(self):
        """Test final status calculation scenarios"""

        self.assertEqual(
            eval_statuses([ProgressStatus.FINISHED_WITH_ISSUES, ProgressStatus.INTENTIONALLY_SKIPPED], fail_or_unfinish_if_any_pending=False, issues_allowed=True),
            ProgressStatus.FINISHED_WITH_ISSUES
        )

        self.assertEqual(
            eval_statuses([ProgressStatus.DONE, ProgressStatus.UNFINISHED], fail_or_unfinish_if_any_pending=False, issues_allowed=True),
            ProgressStatus.UNFINISHED
        )

        self.assertEqual(
            eval_statuses([ProgressStatus.DONE, ProgressStatus.UNFINISHED, ProgressStatus.FAILED ], fail_or_unfinish_if_any_pending=False, issues_allowed=True),
            ProgressStatus.FAILED
        )

        self.assertEqual(
            eval_statuses([ProgressStatus.DONE, ProgressStatus.UNFINISHED, ProgressStatus.FINISHED_WITH_ISSUES ], fail_or_unfinish_if_any_pending=False, issues_allowed=True),
            ProgressStatus.FAILED
        )

        self.assertEqual(
            eval_statuses([ProgressStatus.DONE, ProgressStatus.INTENTIONALLY_SKIPPED], fail_or_unfinish_if_any_pending=False, issues_allowed=True),
            ProgressStatus.DONE
        )

        self.assertEqual(
            eval_statuses([ProgressStatus.FINISHED_WITH_ISSUES, ProgressStatus.DONE], fail_or_unfinish_if_any_pending=False, issues_allowed=True),
            ProgressStatus.FINISHED_WITH_ISSUES
        )

        self.assertEqual(
            eval_statuses([ProgressStatus.FINISHED_WITH_ISSUES, ProgressStatus.DONE], fail_or_unfinish_if_any_pending=False, issues_allowed=False),
            ProgressStatus.FINISHED_WITH_ISSUES
        )

        self.assertEqual(
            eval_statuses([ProgressStatus.FAILED, ProgressStatus.DONE], fail_or_unfinish_if_any_pending=False, issues_allowed=True),
            ProgressStatus.FINISHED_WITH_ISSUES
        )
        self.assertEqual(
            eval_statuses([ProgressStatus.FAILED, ProgressStatus.DONE], fail_or_unfinish_if_any_pending=False, issues_allowed=False),
            ProgressStatus.FAILED
        )

        self.assertEqual(
            eval_statuses([ProgressStatus.DONE, ProgressStatus.IN_PROGRESS_WITH_ISSUES], fail_or_unfinish_if_any_pending=False, issues_allowed=True),
            ProgressStatus.IN_PROGRESS_WITH_ISSUES # fail_or_unfinish_if_any_pending is evaluated first and all not finished fail_or_unfinish_if_any_pendings are considered as FAILED
        )

        self.assertEqual(
            eval_statuses([ProgressStatus.DONE, ProgressStatus.IN_PROGRESS_WITH_ISSUES], fail_or_unfinish_if_any_pending=False, issues_allowed=False),
            ProgressStatus.FAILED
        )

        self.assertEqual(
            eval_statuses([ProgressStatus.FAILED, ProgressStatus.BLOCKED_BY_UNRESOLVED_DEPENDENCY], fail_or_unfinish_if_any_pending=False, issues_allowed=True),
            ProgressStatus.FAILED
        )

        self.assertEqual(
            eval_statuses([ProgressStatus.FAILED, ProgressStatus.BLOCKED_BY_UNRESOLVED_DEPENDENCY], fail_or_unfinish_if_any_pending=False, issues_allowed=False),
            ProgressStatus.FAILED
        )

        self.assertEqual(
            eval_statuses([ProgressStatus.FINISHED_WITH_ISSUES, ProgressStatus.BLOCKED_BY_UNRESOLVED_DEPENDENCY], fail_or_unfinish_if_any_pending=False, issues_allowed=True),
            ProgressStatus.FAILED
        )

        self.assertEqual(
            eval_statuses([ProgressStatus.FINISHED_WITH_ISSUES, ProgressStatus.BLOCKED_BY_UNRESOLVED_DEPENDENCY], fail_or_unfinish_if_any_pending=False, issues_allowed=False),
            ProgressStatus.FAILED
        )

        self.assertEqual(
            eval_statuses([ProgressStatus.FAILED, ProgressStatus.IN_PROGRESS], fail_or_unfinish_if_any_pending=False, issues_allowed=True),
            ProgressStatus.IN_PROGRESS_WITH_ISSUES
        )

        self.assertEqual(
            eval_statuses([ProgressStatus.FAILED, ProgressStatus.IN_PROGRESS], fail_or_unfinish_if_any_pending=False, issues_allowed=False),
            ProgressStatus.FAILED
        )

        # Mixed Success with Warnings = DONE_WITH_WARNINGS
        self.assertEqual(
            eval_statuses([ProgressStatus.DONE, ProgressStatus.DONE_WITH_WARNINGS], fail_or_unfinish_if_any_pending=False, issues_allowed=True),
            ProgressStatus.DONE_WITH_WARNINGS
        )

        self.assertEqual(
            eval_statuses([ProgressStatus.DONE, ProgressStatus.DONE_WITH_WARNINGS], fail_or_unfinish_if_any_pending=False, issues_allowed=False),
            ProgressStatus.DONE_WITH_WARNINGS
        )



        self.assertEqual(
            eval_statuses([ProgressStatus.DONE, ProgressStatus.IN_PROGRESS_WITH_WARNINGS], fail_or_unfinish_if_any_pending=False, issues_allowed=True),
            ProgressStatus.IN_PROGRESS_WITH_WARNINGS
        )

        self.assertEqual(
            eval_statuses([ProgressStatus.DONE, ProgressStatus.IN_PROGRESS_WITH_WARNINGS], fail_or_unfinish_if_any_pending=False, issues_allowed=True),
            ProgressStatus.IN_PROGRESS_WITH_WARNINGS
        )

        

    def test_non_fail_or_unfinish_if_any_pending_status_calculation(self):
        """Test non-final status calculation scenarios"""
        # Test in-progress with issues
        self.assertEqual(
            eval_statuses([ProgressStatus.IN_PROGRESS, ProgressStatus.FINISHED_WITH_ISSUES]),
            ProgressStatus.IN_PROGRESS_WITH_ISSUES
        )

        # Test in-progress with warnings
        self.assertEqual(
            eval_statuses([ProgressStatus.IN_PROGRESS, ProgressStatus.DONE_WITH_WARNINGS]),
            ProgressStatus.IN_PROGRESS_WITH_WARNINGS
        )

        # Test all not started
        self.assertEqual(
            eval_statuses([ProgressStatus.NOT_STARTED]),
            ProgressStatus.NOT_STARTED
        )

        self.assertEqual(
            eval_statuses([ProgressStatus.IN_PROGRESS, ProgressStatus.IN_PROGRESS_WITH_NOTICES]),
            ProgressStatus.IN_PROGRESS_WITH_NOTICES
        )

        self.assertEqual(
            eval_statuses([ProgressStatus.IN_PROGRESS, ProgressStatus.IN_PROGRESS_WITH_ISSUES]),
            ProgressStatus.IN_PROGRESS_WITH_ISSUES)
        
        self.assertEqual(
            eval_statuses([ProgressStatus.IN_PROGRESS, ProgressStatus.FAILED, ProgressStatus.IN_PROGRESS_WITH_ISSUES]),
            ProgressStatus.IN_PROGRESS_WITH_ISSUES)
        

    def test_status_counts_input(self):
        """Test evaluation with StatusCounts input"""
        counts = StatusCounts()
        counts.add_status(ProgressStatus.IN_PROGRESS)
        counts.add_status(ProgressStatus.DONE_WITH_WARNINGS)
        
        self.assertEqual(
            eval_statuses(counts),
            ProgressStatus.IN_PROGRESS_WITH_WARNINGS
        )

    def test_issues_allowed_parameter(self):
        """Test issues_allowed parameter behavior"""
        statuses = [ProgressStatus.IN_PROGRESS, ProgressStatus.FINISHED_WITH_ISSUES]
        
        # With issues allowed
        self.assertEqual(
            eval_statuses(statuses, issues_allowed=True),
            ProgressStatus.IN_PROGRESS_WITH_ISSUES
        )
        
        # Without issues allowed
        self.assertEqual(
            eval_statuses(statuses, issues_allowed=False),
            ProgressStatus.FAILED
        )

    def test_edge_cases(self):
        """Test edge cases and complex combinations"""
        # Mix of everything
        complex_statuses = [
            ProgressStatus.DONE,
            ProgressStatus.IN_PROGRESS,
            ProgressStatus.FAILED,
            ProgressStatus.INTENTIONALLY_SKIPPED,
            ProgressStatus.DONE_WITH_WARNINGS
        ]
        
        # Non-final should show in-progress with issues
        self.assertEqual(
            eval_statuses(complex_statuses, fail_or_unfinish_if_any_pending=False),
            ProgressStatus.IN_PROGRESS_WITH_ISSUES
        )
        
        # Final should show failed
        self.assertEqual(
            eval_statuses(complex_statuses, fail_or_unfinish_if_any_pending=True),
            ProgressStatus.FAILED
        )

if __name__ == '__main__':
    unittest.main()
