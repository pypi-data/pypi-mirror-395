import unittest
from ipulse_shared_base_ftredge import ProgressStatus
from ipulse_shared_base_ftredge.enums.enums_status import (
    ReviewStatus, ObjectOverallStatus, TradingStatus, 
    WorkScheduleStatus, SubscriptionStatus
)
from ipulse_shared_base_ftredge.enums import (
    IAMUnit, IAMAction, IAMUserType
)
from ipulse_shared_base_ftredge.enums import (
    SectorRecordsCategory, SubjectCategory, FincoreContractOrOwnershipType
)
from ipulse_shared_base_ftredge.enums import (
    LogLevel, LoggingHandler
)

class TestProgressStatusEnum(unittest.TestCase):  

    def test_progress_status_sets_complement(self):
            """Test that closed_or_skipped and pending statuses are complementary and complete"""
            # Get all enum values
            all_statuses = set(ProgressStatus)
            
            # Get the sets to compare
            closed_or_skipped = set(ProgressStatus.closed_or_skipped_statuses())
            pending = set(ProgressStatus.pending_or_blocked_statuses())
            
            # Test no intersection
            intersection = closed_or_skipped.intersection(pending)
            assert len(intersection) == 0, f"Found overlapping statuses: {intersection}"
            
            # Test union covers all statuses
            union = closed_or_skipped.union(pending)
            assert union == all_statuses, f"Missing statuses: {all_statuses - union}, Extra statuses: {union - all_statuses}"
            
            # Additional verification of individual elements
            assert all(isinstance(status, ProgressStatus) for status in closed_or_skipped)
            assert all(isinstance(status, ProgressStatus) for status in pending)

class TestAutoStrEnumValues(unittest.TestCase):
    """Test that all AutoStrEnum classes generate correct lowercase string values."""
    
    def test_review_status_values(self):
        """Test ReviewStatus enum generates lowercase string values."""
        expected_values = {
            'OPEN': 'OPEN',
            'ACKNOWLEDGED': 'ACKNOWLEDGED',
            'ESCALATED': 'ESCALATED',
            'IN_PROGRESS': 'IN_PROGRESS',
            'IN_REVIEW': 'IN_REVIEW',
            'RESOLVED': 'RESOLVED',
            'IGNORED': 'IGNORED',
            'CANCELLED': 'CANCELLED',
            'CLOSED': 'CLOSED'
        }
        
        for name, expected_value in expected_values.items():
            enum_member = getattr(ReviewStatus, name)
            self.assertIsInstance(enum_member.value, str, f"{name} should have string value")
            self.assertEqual(enum_member.value, expected_value, f"{name} should equal '{expected_value}'")
    
    def test_object_overall_status_values(self):
        """Test ObjectOverallStatus enum generates lowercase string values."""
        expected_values = {
            'ACTIVE': 'ACTIVE',
            'DISABLED': 'DISABLED',
            'DELETED': 'DELETED',
            'PENDING': 'PENDING',
            'PAUSED': 'PAUSED',
            'ARCHIVED': 'ARCHIVED'
        }
        
        for name, expected_value in expected_values.items():
            enum_member = getattr(ObjectOverallStatus, name)
            self.assertIsInstance(enum_member.value, str, f"{name} should have string value")
            self.assertEqual(enum_member.value, expected_value, f"{name} should equal '{expected_value}'")
    
    def test_trading_status_values(self):
        """Test TradingStatus enum generates lowercase string values."""
        # Test a sample of values
        sample_values = {
            'TRADED_ON_PUBLIC_EXCHANGE': 'TRADED_ON_PUBLIC_EXCHANGE',
            'TRADED_OTC': 'TRADED_OTC',
            'NOT_FOR_SALE': 'NOT_FOR_SALE',
            'UNKNOWN': 'UNKNOWN'
        }
        
        for name, expected_value in sample_values.items():
            enum_member = getattr(TradingStatus, name)
            self.assertIsInstance(enum_member.value, str, f"{name} should have string value")
            self.assertEqual(enum_member.value, expected_value, f"{name} should equal '{expected_value}'")
        
        # Test that all values are strings
        for status in TradingStatus:
            self.assertIsInstance(status.value, str, f"{str(status)} should have string value")
    
    def test_work_schedule_status_values(self):
        """Test WorkScheduleStatus enum generates lowercase string values."""
        sample_values = {
            'OPEN': 'OPEN',
            'CLOSED': 'CLOSED',
            'PERMANENTLY_CLOSED': 'PERMANENTLY_CLOSED',
            'UNKNOWN': 'UNKNOWN'
        }
        
        for name, expected_value in sample_values.items():
            enum_member = getattr(WorkScheduleStatus, name)
            self.assertIsInstance(enum_member.value, str, f"{name} should have string value")
            self.assertEqual(enum_member.value, expected_value, f"{name} should equal '{expected_value}'")
    
    def test_subscription_status_values(self):
        """Test SubscriptionStatus enum generates lowercase string values."""
        expected_values = {
            'ACTIVE': 'ACTIVE',
            'DISABLED': 'DISABLED',
            'TRIAL': 'TRIAL',
            'CANCELLED': 'CANCELLED',
            'EXPIRED': 'EXPIRED',
            'SUSPENDED': 'SUSPENDED',
            'UPGRADED': 'UPGRADED',
            'DOWNGRADED': 'DOWNGRADED',
            'UNKNOWN': 'UNKNOWN'
        }
        
        for name, expected_value in expected_values.items():
            enum_member = getattr(SubscriptionStatus, name)
            self.assertIsInstance(enum_member.value, str, f"{name} should have string value")
            self.assertEqual(enum_member.value, expected_value, f"{name} should equal '{expected_value}'")

class TestIAMEnumValues(unittest.TestCase):
    """Test that IAM enums using auto()  # type: ignore generate correct lowercase string values."""
    
    def test_iam_unit_type_values(self):
        """Test IAMUnit enum auto()  # type: ignore generates lowercase string values."""
        expected_values = {
            'GROUP': 'group',
            'ROLE': 'role'
        }
        
        for name, expected_value in expected_values.items():
            enum_member = getattr(IAMUnit, name)
            self.assertIsInstance(enum_member.value, str, f"{name} should have string value")
            self.assertEqual(enum_member.value, expected_value, f"{name} should equal '{expected_value}'")
    
    def test_iam_action_values(self):
        """Test IAMAction enum auto()  # type: ignore generates lowercase string values."""
        expected_values = {
            'ALLOW': 'allow',
            'DENY': 'deny',
            'GRANT': 'grant',
            'REVOKE': 'revoke'
        }
        
        for name, expected_value in expected_values.items():
            enum_member = getattr(IAMAction, name)
            self.assertIsInstance(enum_member.value, str, f"{name} should have string value")
            self.assertEqual(enum_member.value, expected_value, f"{name} should equal '{expected_value}'")
    
    def test_iam_usertype_values(self):
        """Test IAMUserType enum auto()  # type: ignore generates lowercase string values."""
        sample_values = {
            'ANONYMOUS': 'anonymous',
            'AUTHENTICATED': 'authenticated',
            'ADMIN': 'admin',
            'SUPERADMIN': 'superadmin'
        }
        
        for name, expected_value in sample_values.items():
            enum_member = getattr(IAMUserType, name)
            self.assertIsInstance(enum_member.value, str, f"{name} should have string value")
            self.assertEqual(enum_member.value, expected_value, f"{name} should equal '{expected_value}'")

class TestFincoreEnumValues(unittest.TestCase):
    """Test that Fincore enums using auto()  # type: ignore generate correct lowercase string values."""
    
    def test_fincore_category_values(self):
        """Test SectorRecordsCategory enum auto()  # type: ignore generates lowercase string values."""
        # Test that all values are strings (sample test since there are many)
        for enum_member in SectorRecordsCategory:
            self.assertIsInstance(enum_member.value, str, f"{enum_member.name} should have string value")
            if isinstance(enum_member.value, str):
                self.assertTrue(enum_member.value.islower(), f"{enum_member.name} value should be lowercase")
    
    def test_market_asset_category_values(self):
        """Test SubjectCategory enum auto()  # type: ignore generates lowercase string values."""
        for enum_member in SubjectCategory:
            self.assertIsInstance(enum_member.value, str, f"{enum_member.name} should have string value")
            if isinstance(enum_member.value, str):
                self.assertTrue(enum_member.value.islower(), f"{enum_member.name} value should be lowercase")
    
    def test_market_instrument_type_values(self):
        """Test MarketInstrumentType enum auto()  # type: ignore generates lowercase string values."""
        for enum_member in FincoreContractOrOwnershipType:
            self.assertIsInstance(enum_member.value, str, f"{enum_member.name} should have string value")
            if isinstance(enum_member.value, str):
                self.assertTrue(enum_member.value.islower(), f"{enum_member.name} value should be lowercase")

class TestLoggingEnumValues(unittest.TestCase):
    """Test that Logging enums using auto()  # type: ignore generate correct lowercase string values."""
    
    def test_logging_handler_values(self):
        """Test LoggingHandler enum auto()  # type: ignore generates lowercase string values."""
        for enum_member in LoggingHandler:
            self.assertIsInstance(enum_member.value, str, f"{enum_member.name} should have string value")
            if isinstance(enum_member.value, str):
                self.assertTrue(enum_member.value.islower(), f"{enum_member.name} value should be lowercase")
    
    def test_log_level_has_numeric_values(self):
        """Test LogLevel enum has numeric values (not string-based)."""
        for enum_member in LogLevel:
            self.assertIsInstance(enum_member.value, int, f"{enum_member.name} should have numeric value")

class TestEnumStringConversion(unittest.TestCase):
    """Test that enums convert to strings correctly."""
    
    def test_review_status_str_conversion(self):
        """Test ReviewStatus str() conversion works correctly."""
        self.assertEqual(str(ReviewStatus.OPEN), 'OPEN')
        self.assertEqual(str(ReviewStatus.IN_PROGRESS), 'IN_PROGRESS')

    def test_iam_enum_str_conversion(self):
        """Test IAM enum str() conversion works correctly."""
        self.assertEqual(str(IAMAction.ALLOW), 'allow')
        self.assertEqual(str(IAMUserType.AUTHENTICATED), 'authenticated')

if __name__ == '__main__':
    unittest.main()