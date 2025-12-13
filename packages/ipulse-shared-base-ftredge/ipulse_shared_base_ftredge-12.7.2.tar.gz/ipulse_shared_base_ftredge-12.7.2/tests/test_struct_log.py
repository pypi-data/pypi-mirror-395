import json
import unittest
import time
from typing import Dict
from ipulse_shared_base_ftredge import (StructLog, ReviewStatus, LogLevel, DataUnit,
                                        ProgressStatus, Alert, Action,
                                        DataResource)

class TestPipelineLog(unittest.TestCase):

    def setUp(self):
        # Only include valid parameters that match the StructLog constructor
        self.default_params = {
            "level": LogLevel.INFO,
            "action": Action.READ,
            "resource": DataResource.API,
            "progress_status": ProgressStatus.IN_PROGRESS,
            "alert": Alert.DATA_VALIDATION_ISSUES,
            "q": 40,
            "q_unit": DataUnit.DBROW,
            "log_review_status": ReviewStatus.OPEN,
            "collector_id": "collector_123",
            "trace_id": "task_456",
            "base_context": "base_context_example",
            "context": "context_example",
            "description": "This is a test description.",
            "note": "This is a test note.",
            "systems_impacted": ["system1", "system2"],
            "e": None,
            "e_type": None,
            "e_message": None,
            "e_traceback": None,
            "max_field_len": 6000
        }

    def create_log(self, **kwargs) -> StructLog:
        params = self.default_params.copy()
        params.update(kwargs)
        # Filter out any parameters that aren't valid for StructLog
        valid_params = {
            k: v for k, v in params.items() 
            if k in [
                "level", "action", "resource", "progress_status", "alert", 
                "q", "q_unit", "log_review_status", "collector_id", "trace_id", 
                "base_context", "context", "description", "note", "systems_impacted",
                "e", "e_type", "e_message", "e_traceback", "max_field_len"
            ]
        }
        return StructLog(**valid_params)

    def test_pipeline_log(self):
        test_cases = [
            {"description": "Short description", "note": "Short note"},
            {"description": "A" * 1000, "note": "B" * 1000},
            {"description": "A" * 5000, "note": "B" * 5000},
            {"description": "A" * 20000, "note": "B" * 20000, "systems_impacted": ["B"]*1000, "e": "C" * 10000, "base_context": "D" * 10000},
            {"description": "A" * 50000, "note": "B" * 10000},
            {"description": None, "note": None, "systems_impacted": None},
            {"description": "", "note": "", "systems_impacted": ["DB Bigquery"]},
            # Fix invalid enum values by using proper enum values
            {"alert": Alert.DATA_VALIDATION_ISSUES, "log_review_status": ReviewStatus.OPEN},
            {"action": Action.PERSIST_CREATE, "log_review_status": ReviewStatus.CLOSED},
            {"action": Action.PERSIST_CREATE, "log_review_status": ReviewStatus.CLOSED},
            {"level": LogLevel.CRITICAL, "log_review_status": ReviewStatus.CLOSED},
            {"level": LogLevel.CRITICAL, "log_review_status": ReviewStatus.CLOSED},
            {"e_traceback": "A" * 40000, "note": "B" * 40000, "context": "C" * 40000},
            {"e_traceback": "A" * 100000, "note": "B" * 100000, "context": "C" * 100000},
            {"description": "A" * 1000, "note": "B" * 1000, "max_field_len": 2000, "q": None, "q_unit": None},
            {"description": "Short description", "note": "Short note"},
        ]

        for i, case in enumerate(test_cases):
            with self.subTest(i=i):
                start_time = time.time()
                log = self.create_log(**case)
                log_dict = log.to_dict(byte_size_limit=1 * 1024)
                end_time = time.time()
                duration = end_time - start_time
                print(f"Test case {i + 1}: {duration:.6f} seconds")
                print("Size of log_dict: ", len(json.dumps(log_dict).encode('utf-8')))
                # print(f"Test case Dict {i + 1}: {log_dict}")
                print("Event with None: ", log.getEvent(exclude_none=False))
                print("Event without None: ", log.getEvent())
                self.assertIsInstance(log_dict, Dict)
                self.assertLessEqual(len(json.dumps(log_dict).encode('utf-8')), 256 * 1024 * 0.80)

    ############################################################################################################
    # Test to_dict() captures all fields
    ############################################################################################################
    def test_to_dict_field_count_no_truncation(self):
        """
        Verify the final dictionary has the expected number of fields 
        with typical (non-truncated) data.
        """
        log = self.create_log(description="Short desc", note="Short note")
        log_dict = log.to_dict()  # Large limit to avoid truncation
        # Check presence of expected keys
        expected_keys = {
            "level",
            "level_code",
            "base_context",
            "context",
            "action",
            "resource",
            "progress_status",
            "progress_status_code",
            "alert",
            "q",
            "q_unit",
            "collector_id",
            "trace_id",
            "description",
            "note",
            "systems_impacted",
            "log_review_status",
            "exception_type",
            "exception_message",
            "exception_traceback",
            "timestamp",
            "truncated"
        }
        self.assertTrue(expected_keys.issubset(set(log_dict.keys())), "All expected keys should be present.")
        self.assertGreaterEqual(len(log_dict.keys()), len(expected_keys), "No unexpected key removal.")


    def test_to_dict_field_count_truncated_data(self):
        """
        Verify that the final dictionary still has the right set of keys 
        even when truncation occurs.
        """
        log = self.create_log(
            description="A" * 100000, 
            note="B" * 50000, 
            max_field_len=500
        )
        log_dict = log.to_dict(byte_size_limit=700)  # Forcing truncation
        expected_keys = {
            "level",
            "level_code",
            "truncated",
            "action",
            "resource",
            "progress_status",
            "alert",
            "note",
            "description",
            "collector_id",
            "trace_id",
            "base_context",
            "context",
            "systems_impacted",
        }
        print(f"Log dict: {log_dict}")
        self.assertTrue(expected_keys.issubset(set(log_dict.keys())), "Even truncated, all required keys remain.")

    ############################################################################################################
    # Test field truncation and sizing
    ############################################################################################################

    def test_field_truncation_by_max_field_len(self):
        """
        Test that large fields get truncated if they exceed max_field_len.
        """
        test_cases = [
            {
                "description": "A" * 10000,
                "note": "B" * 8000,
                "max_field_len": 2000,
                "expected_desc_len": 2000, # Truncated to 2000 chars
                "expected_note_len": 2000, # Truncated to 2000 chars
            },
            {
                "description": "A" * 300,
                "note": "B" * 400,
                "max_field_len": 1000,
                "expected_desc_len": 300,  # No truncation
                "expected_note_len": 400,  # No truncation 
            },
        ]

        for i, case in enumerate(test_cases):
            with self.subTest(i=i):
                # Extract only the parameters that should be passed to StructLog
                valid_params = {
                    k: v for k, v in case.items() 
                    if k in ["description", "note", "max_field_len"]
                }
                log = self.create_log(**valid_params)
                
                log_dict = log.to_dict(byte_size_limit=1 * 1024)
                desc_len = len(log_dict["description"]) if "description" in log_dict else 0
                note_len = len(log_dict["note"]) if "note" in log_dict else 0
                
                self.assertLessEqual(
                    desc_len,
                    case["expected_desc_len"],
                    f"Description should be truncated to {case['expected_desc_len']} chars or less."
                )
                self.assertLessEqual(
                    note_len, 
                    case["expected_note_len"],
                    f"Note should be truncated to {case['expected_note_len']} chars or less."
                )

    def test_field_truncation_by_byte_size(self):
        """
        Test that large fields get truncated by the overall byte_size_limit
        if the maximum field length alone isn't enough.
        """
        # This small byte_size_limit ensures forced truncation.
        byte_size_limit = 600  # 600 bytes intentionally small
        log = self.create_log(
            description="X" * 5000,
            note="Y" * 5000,
            max_field_len=3000  # Enough to hold 3000 chars
        )
        log_dict = log.to_dict(byte_size_limit=byte_size_limit)
        # The resulting JSON must be <= 600 bytes.
        json_size = len(json.dumps(log_dict).encode('utf-8'))
        self.assertLessEqual(
            json_size,
            byte_size_limit,
            f"Total serialized JSON size must not exceed {byte_size_limit} bytes."
        )
        # Also verify fields did not exceed initial max_field_len
        self.assertLessEqual(
            len(log_dict.get("description", "")),
            3000,
            "Description should never exceed max_field_len=3000."
        )
        self.assertLessEqual(
            len(log_dict.get("note", "")),
            3000,
            "Note should never exceed max_field_len=3000."
        )

    ############################################################################################################
    # Test getEvent() method
    ############################################################################################################

    def test_get_event_dict_exclude_none_true(self):
        """
        Verify that getEvent() returns a dictionary without None fields 
        when exclude_none=True.
        """
        log = StructLog(
            level=LogLevel.INFO,
            action=Action.READ,
            resource=DataResource.DATA
        )
        event_dict = log.getEvent(exclude_none=True, as_dict=True)
        self.assertIsInstance(event_dict, dict, "Should return a dict.")
        self.assertIn("level", event_dict, "Field 'level' should be included.")
        self.assertIn("action", event_dict, "Field 'action' should be included.")
        self.assertIn("resource", event_dict, "Field 'resource' should be included.")
        self.assertNotIn("alert", event_dict, "Field 'alert' should not be included if it's None.")
        

    def test_get_event_dict_exclude_none_false(self):
        """
        Verify that getEvent() returns a dictionary with None fields 
        when exclude_none=False.
        """
        log = StructLog(
            level=LogLevel.WARNING,
            action=Action.PERSIST_APPEND,
            resource=None,
            alert=None
        )
        event_dict = log.getEvent(exclude_none=False, as_dict=True)
        self.assertIsInstance(event_dict, dict, "Should return a dict.")
        self.assertIn("resource", event_dict, "Resource should appear, even if None, when exclude_none=False.")
        self.assertIn("alert", event_dict, "Alert should appear, even if None, when exclude_none=False.")
        self.assertIsNone(event_dict["resource"], "Resource should be None.")
        self.assertIsNone(event_dict["alert"], "Alert should be None.")

    def test_get_event_as_tuple_exclude_none_true(self):
        """
        Verify getEvent(as_dict=False) omits None fields if exclude_none=True.
        """
        log = StructLog(
            level=LogLevel.ERROR,
            action=None,
            resource=DataResource.DATA,
            progress_status=ProgressStatus.DONE
        )
        event_tuple = log.getEvent(exclude_none=True, as_dict=False)
        self.assertTrue(isinstance(event_tuple, tuple), "Should return a tuple.")
        # Should contain only the non-None fields: level, resource, progress_status
        self.assertEqual(len(event_tuple), 3, "Tuple should have 3 items (level, resource, progress_status).")

    def test_get_event_as_tuple_exclude_none_false(self):
        """
        Verify getEvent() includes None fields if exclude_none=False.
        """
        log = StructLog(
            level=LogLevel.INFO,
            action=Action.READ,
            resource=None
        )
        event_tuple = log.getEvent(exclude_none=False)
        # Expect 7 total fields in the tuple (level, action, resource, progress_status, alert, q, q_unit)
        # resource is None, progress_status/alert/q/q_unit are also None
        self.assertEqual(len(event_tuple), 7, "Tuple should include all 7 possible fields even if some are None.")
        self.assertIn(None, event_tuple, "None fields should be present in the tuple when exclude_none=False.")

    def test_get_event_all_fields(self):
        """
        Confirm getEvent captures all relevant fields when they are set.
        """
        log = StructLog(
            level=LogLevel.DEBUG,
            action=Action.PERSIST_UPDATE,
            resource=DataResource.DB_BIGQUERY,
            progress_status=ProgressStatus.IN_PROGRESS,
            alert=Alert.DATA_VALIDATION_ISSUES
        )
        event_dict = log.getEvent(exclude_none=True, as_dict=True)
        self.assertEqual(len(event_dict), 5, "Should have 5 fields: level, action, resource, progress_status, alert.")
        self.assertEqual(event_dict["level"], "DEBUG", "Level should match.")
        self.assertEqual(event_dict["action"], "persist_update", "Action should match.")
        self.assertEqual(event_dict["resource"], "db_bigquery", "Resource should match.")
        self.assertEqual(str(event_dict["progress_status"]), "IN_PROGRESS", "Progress status should match.")
        self.assertEqual(event_dict["alert"], "data_validation_issues", "Alert should match.")

if __name__ == "__main__":
    unittest.main()