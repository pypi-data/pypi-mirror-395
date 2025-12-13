"""
Schema Registry Item Validators

This module provides comprehensive schema validation and consistency checking
for data schemas across different storage systems (BigQuery, Firestore, etc.).

Key Features:
- Cross-format consistency validation
- Type compatibility checking
- Field coverage analysis
- Constraint validation
- Detailed reporting

Usage:
    from ipulse_shared_base_ftredge.validators.schema_registry_item_validators import validate_all_schemas
    
    # Validate all schemas in your registry
    is_valid = validate_all_schemas(TABLE_SCHEMAS)
    
    # Validate single schema with detailed report
    is_valid = validate_schema_consistency(schema_data, "my_schema")
"""

from typing import Dict, List, Optional
import re
from dataclasses import dataclass
from enum import Enum


class IssueType(Enum):
    """Types of schema consistency issues"""
    MISSING = "missing"
    TYPE_MISMATCH = "type_mismatch"
    CONSTRAINT_MISMATCH = "constraint_mismatch"
    EXTRA = "extra"


class StorageType(Enum):
    """Supported storage types"""
    BIGQUERY_TABLE = "bigquery_table"
    FIRESTORE_COLLECTION = "firestore_collection"
    UNKNOWN = "unknown"


@dataclass
class ConsistencyIssue:
    """Represents a schema consistency issue"""
    field_name: str
    issue_type: str  # 'missing', 'type_mismatch', 'constraint_mismatch', 'extra'
    format_1: str
    format_2: str
    details: str


class SchemaTypeMapper:
    """Handles type mapping between different schema formats"""
    
    def __init__(self):
        self.bigquery_type_mapping = {
            'string': ['STRING', 'DATE', 'TIMESTAMP', 'TIME'],
            'float': ['FLOAT64', 'NUMERIC'],
            'integer': ['INT64'], 
            'boolean': ['BOOL', 'BOOLEAN'],
            'date': ['DATE'],
            'datetime': ['TIMESTAMP'],
            'time': ['TIME'],
            'list': ['JSON'],
            'dict': ['JSON']
        }
        
        self.cerberus_special_mappings = {
            'standard_str_date': 'DATE',
            'iso_str_timestamp': 'TIMESTAMP',
            'standard_str_time': 'TIME'
        }
    
    def get_expected_bigquery_type(self, cerberus_def: Dict) -> str:
        """Get expected BigQuery type from Cerberus definition"""
        cerberus_type = cerberus_def.get('type')
        check_with = cerberus_def.get('check_with')
        
        # Handle list types in cerberus (e.g., ["string", "date"])
        if isinstance(cerberus_type, list):
            cerberus_type = cerberus_type[0]  # Take first type
        
        # Check for special validators first
        if check_with in self.cerberus_special_mappings:
            return self.cerberus_special_mappings[check_with]
        
        # Return the primary expected type
        if cerberus_type and cerberus_type in self.bigquery_type_mapping:
            expected_types = self.bigquery_type_mapping[cerberus_type]
            return expected_types[0]  # Return primary expected type
        
        return 'UNKNOWN'
    
    def is_type_compatible(self, cerberus_def: Dict, bigquery_type: str) -> bool:
        """Check if BigQuery type is compatible with Cerberus definition"""
        cerberus_type = cerberus_def.get('type')
        check_with = cerberus_def.get('check_with')
        
        # Handle list types
        if isinstance(cerberus_type, list):
            cerberus_type = cerberus_type[0]
        
        # Special validator mappings
        if check_with in self.cerberus_special_mappings:
            return bigquery_type == self.cerberus_special_mappings[check_with]
        
        # Check if BQ type is in allowed types for cerberus type
        if cerberus_type and cerberus_type in self.bigquery_type_mapping:
            allowed_types = self.bigquery_type_mapping[cerberus_type]
            return bigquery_type in allowed_types
        
        return False


class SchemaStorageDetector:
    """Detects storage type from schema data"""
    
    @staticmethod
    def detect_storage_type(schema_data: Dict) -> StorageType:
        """Detect storage type from schema configuration"""
        storage_resource = schema_data.get('storage_resource', '')
        storage_resource_str = str(storage_resource).lower()
        
        # BigQuery indicators
        bigquery_indicators = ['db_bigquery_table', 'bigquery']
        if any(indicator in storage_resource_str for indicator in bigquery_indicators):
            return StorageType.BIGQUERY_TABLE
        
        # Firestore indicators
        firestore_indicators = ['firestore', 'firestore_collection', 'db_firestore_collection']
        if any(indicator in storage_resource_str for indicator in firestore_indicators):
            return StorageType.FIRESTORE_COLLECTION
        
        return StorageType.UNKNOWN
    
    @staticmethod
    def is_bigquery_table(schema_data: Dict) -> bool:
        """Check if schema is for a BigQuery table"""
        return SchemaStorageDetector.detect_storage_type(schema_data) == StorageType.BIGQUERY_TABLE
    
    @staticmethod
    def is_firestore_collection(schema_data: Dict) -> bool:
        """Check if schema is for a Firestore collection"""
        return SchemaStorageDetector.detect_storage_type(schema_data) == StorageType.FIRESTORE_COLLECTION


class SchemaFieldExtractor:
    """Extracts field information from different schema formats"""
    
    @staticmethod
    def extract_firestore_fields(firestore_schema: Dict) -> set:
        """Extract field names from Firestore schema"""
        if not firestore_schema:
            return set()
        
        # Get fields from document_structure
        document_structure = firestore_schema.get('document_structure', {})
        return set(document_structure.keys())

    @staticmethod
    def extract_bigquery_fields(ddl: str) -> set:
        """Extract field names from BigQuery DDL"""
        if not ddl:
            return set()
        
        pattern = r'\s*(\w+)\s+(?:STRING(?:\(\d+\))?|FLOAT64|INT64|NUMERIC|BOOL|BOOLEAN|DATE|TIMESTAMP|TIME|JSON)'
        matches = re.findall(pattern, ddl, re.IGNORECASE)
        return set(matches)
    
    @staticmethod
    def extract_bigquery_field_type(ddl: str, field_name: str) -> str:
        """Extract the BigQuery type for a specific field with word boundaries"""
        if not ddl:
            return ""
        
        # More precise pattern that only matches the type immediately after the field name
        # This avoids matching types in the OPTIONS description
        type_pattern = rf'\b{field_name}\s+(STRING(?:\(\d+\))?|FLOAT64|INT64|NUMERIC|BOOL|BOOLEAN|DATE|TIMESTAMP|TIME|JSON)\b'
        match = re.search(type_pattern, ddl, re.IGNORECASE)
        return match.group(1).upper() if match else ""
    
    @staticmethod
    def extract_bigquery_field_definition(ddl: str, field_name: str) -> str:
        """Extract the complete field definition from BigQuery DDL with word boundaries"""
        if not ddl:
            return ""
        
        # More precise pattern that ensures we match field definitions at field start positions
        # and capture the complete definition including constraints
        pattern = rf'(?:^|,|\n)\s*{field_name}\s+[^,\n]+(?:OPTIONS\([^)]+\))?'
        match = re.search(pattern, ddl, re.IGNORECASE | re.MULTILINE)
        
        if match:
            # Clean up the match to remove leading comma/newline/whitespace
            result = match.group(0).strip()
            if result.startswith(','):
                result = result[1:].strip()
            return result
        return ""
    
    @staticmethod
    def extract_bigquery_string_length(ddl: str, field_name: str) -> Optional[int]:
        """Extract STRING length from BigQuery DDL for specific field"""
        field_def = SchemaFieldExtractor.extract_bigquery_field_definition(ddl, field_name)
        
        pattern = r'STRING\((\d+)\)'
        match = re.search(pattern, field_def, re.IGNORECASE)
        return int(match.group(1)) if match else None


class SchemaConsistencyChecker:
    """Check consistency across different schema representations"""
    
    def __init__(self):
        self.type_mapper = SchemaTypeMapper()
        self.storage_detector = SchemaStorageDetector()
        self.field_extractor = SchemaFieldExtractor()
    
    def check_schema_consistency(self, schema_data: Dict, debug: bool = False) -> Dict[str, List[ConsistencyIssue]]:
        """Main function to check consistency across all schema formats"""
        issues = {
            'field_coverage': [],
            'type_consistency': [],
            'constraint_consistency': [],
            'description_consistency': []
        }
        
        # Detect storage type
        storage_type = self.storage_detector.detect_storage_type(schema_data)
        is_bigquery_table = storage_type == StorageType.BIGQUERY_TABLE
        is_firestore_collection = storage_type == StorageType.FIRESTORE_COLLECTION
        
        if debug:
            print(f"🔍 DEBUG: storage_type = {storage_type}")
            print(f"🔍 DEBUG: is_bigquery_table = {is_bigquery_table}")
            print(f"🔍 DEBUG: is_firestore_collection = {is_firestore_collection}")
        
        # Extract field sets from each format
        descriptions_fields = set(schema_data.get('schema_fields_descriptions', {}).keys())
        
        # Choose validation schema based on storage resource
        if is_firestore_collection:
            firestore_schema = schema_data.get('schema_firestore_json', {})
            validation_fields = self.field_extractor.extract_firestore_fields(firestore_schema)
            validation_schema_name = 'schema_firestore_json'
        else:
            validation_fields = set(schema_data.get('schema_cerberus', {}).keys())
            validation_schema_name = 'schema_cerberus'
        
        # Extract BigQuery fields if it's a BigQuery table
        if is_bigquery_table:
            bigquery_fields = self.field_extractor.extract_bigquery_fields(
                schema_data.get('schema_bigquery_create_ddl', '')
            )
        else:
            bigquery_fields = set()
        
        if debug:
            print(f"🔍 DEBUG: descriptions_fields count = {len(descriptions_fields)}")
            print(f"🔍 DEBUG: validation_fields count = {len(validation_fields)}")
            print(f"🔍 DEBUG: bigquery_fields count = {len(bigquery_fields)}")
        
        # For Firestore collections, only check top-level keys from descriptions
        # to avoid false positives for nested field paths like assets.{asset_id}.field_name
        if is_firestore_collection:
            # Extract only top-level keys from descriptions (before first dot)
            top_level_descriptions_fields = {field.split('.')[0] for field in descriptions_fields}
            field_coverage_descriptions = top_level_descriptions_fields
        else:
            field_coverage_descriptions = descriptions_fields
        
        # Check field coverage
        issues['field_coverage'].extend(
            self._check_field_coverage(field_coverage_descriptions, validation_fields, 
                                     bigquery_fields, is_bigquery_table, validation_schema_name)
        )
        
        # Check type consistency (only for BigQuery tables)
        if is_bigquery_table:
            issues['type_consistency'].extend(
                self._check_type_consistency(schema_data)
            )
        
        # Check constraint consistency (only for BigQuery tables)
        if is_bigquery_table:
            issues['constraint_consistency'].extend(
                self._check_constraint_consistency(schema_data)
            )
        
        # Check description consistency
        issues['description_consistency'].extend(
            self._check_description_consistency(schema_data, validation_fields, validation_schema_name)
        )
        
        return issues
    
    def _check_field_coverage(self, descriptions_fields: set, validation_fields: set, 
                            bigquery_fields: set, is_bigquery_table: bool = True, 
                            validation_schema_name: str = 'schema_cerberus') -> List[ConsistencyIssue]:
        """Check if all formats have the same fields"""
        issues = []
        
        missing_in_validation = descriptions_fields - validation_fields
        
        for field in missing_in_validation:
            issues.append(ConsistencyIssue(
                field_name=field,
                issue_type=IssueType.MISSING.value,
                format_1='schema_fields_descriptions',
                format_2=validation_schema_name,
                details=f"Field '{field}' exists in descriptions but missing in {validation_schema_name}"
            ))
        
        # Only check BigQuery fields if it's a BigQuery table
        if is_bigquery_table:
            missing_in_bigquery = descriptions_fields - bigquery_fields
            for field in missing_in_bigquery:
                issues.append(ConsistencyIssue(
                    field_name=field,
                    issue_type=IssueType.MISSING.value,
                    format_1='schema_fields_descriptions',
                    format_2='schema_bigquery_create_ddl',
                    details=f"Field '{field}' exists in descriptions but missing in BigQuery DDL"
                ))
        
        # Extra fields in validation schema
        extra_in_validation = validation_fields - descriptions_fields
        for field in extra_in_validation:
            issues.append(ConsistencyIssue(
                field_name=field,
                issue_type=IssueType.EXTRA.value,
                format_1=validation_schema_name,
                format_2='schema_fields_descriptions',
                details=f"Field '{field}' exists in {validation_schema_name} but missing in descriptions"
            ))
        
        return issues
    
    def _check_type_consistency(self, schema_data: Dict) -> List[ConsistencyIssue]:
        """Check if field types are consistent across formats"""
        issues = []
        
        cerberus_schema = schema_data.get('schema_cerberus', {})
        bigquery_ddl = schema_data.get('schema_bigquery_create_ddl', '')
        
        for field_name, cerberus_def in cerberus_schema.items():
            # Get actual BigQuery type
            bigquery_type = self.field_extractor.extract_bigquery_field_type(bigquery_ddl, field_name)
            
            if bigquery_type:
                # Use compatibility check instead of exact mapping
                if not self.type_mapper.is_type_compatible(cerberus_def, bigquery_type):
                    expected_type = self.type_mapper.get_expected_bigquery_type(cerberus_def)
                    cerberus_type = cerberus_def.get('type')
                    check_with = cerberus_def.get('check_with', '')
                    
                    details = f"Type incompatible: Cerberus type='{cerberus_type}'"
                    if check_with:
                        details += f" with validator='{check_with}'"
                    details += f" -> expected BigQuery='{expected_type}' but found '{bigquery_type}'"
                    
                    issues.append(ConsistencyIssue(
                        field_name=field_name,
                        issue_type=IssueType.TYPE_MISMATCH.value,
                        format_1='schema_cerberus',
                        format_2='schema_bigquery_create_ddl',
                        details=details
                    ))
        
        return issues
    
    def _check_constraint_consistency(self, schema_data: Dict) -> List[ConsistencyIssue]:
        """Check if constraints are consistent (required fields, maxlength, etc.)"""
        issues = []
        
        cerberus_schema = schema_data.get('schema_cerberus', {})
        bigquery_ddl = schema_data.get('schema_bigquery_create_ddl', '')
        
        for field_name, cerberus_def in cerberus_schema.items():
            # Check required field consistency
            cerberus_required = cerberus_def.get('required', False)
            bigquery_field_def = self.field_extractor.extract_bigquery_field_definition(bigquery_ddl, field_name)
            bigquery_not_null = 'NOT NULL' in bigquery_field_def
            
            if cerberus_required and not bigquery_not_null:
                issues.append(ConsistencyIssue(
                    field_name=field_name,
                    issue_type=IssueType.CONSTRAINT_MISMATCH.value,
                    format_1='schema_cerberus',
                    format_2='schema_bigquery_create_ddl',
                    details="Field is required in Cerberus but not NOT NULL in BigQuery"
                ))
            
            # Check maxlength consistency
            cerberus_maxlength = cerberus_def.get('maxlength')
            bigquery_length = self.field_extractor.extract_bigquery_string_length(bigquery_ddl, field_name)
            
            if cerberus_maxlength and bigquery_length and cerberus_maxlength != bigquery_length:
                issues.append(ConsistencyIssue(
                    field_name=field_name,
                    issue_type=IssueType.CONSTRAINT_MISMATCH.value,
                    format_1='schema_cerberus',
                    format_2='schema_bigquery_create_ddl',
                    details=f"Maxlength mismatch: Cerberus={cerberus_maxlength}, BigQuery={bigquery_length}"
                ))
        
        return issues
    
    def _check_description_consistency(self, schema_data: Dict, validation_fields: Optional[set] = None, 
                                     validation_schema_name: str = 'schema_cerberus') -> List[ConsistencyIssue]:
        """Check if descriptions exist for all fields"""
        issues = []
        
        descriptions = schema_data.get('schema_fields_descriptions', {})
        
        # Use validation_fields if provided, otherwise fall back to cerberus
        if validation_fields is None:
            validation_fields = set(schema_data.get('schema_cerberus', {}).keys())
            validation_schema_name = 'schema_cerberus'
        
        # Check if all validation schema fields have descriptions
        for field_name in validation_fields:
            if field_name not in descriptions:
                issues.append(ConsistencyIssue(
                    field_name=field_name,
                    issue_type=IssueType.MISSING.value,
                    format_1=validation_schema_name,
                    format_2='schema_fields_descriptions',
                    details=f"Field '{field_name}' has schema definition but no description"
                ))
            elif not descriptions[field_name].get('description', '').strip():
                issues.append(ConsistencyIssue(
                    field_name=field_name,
                    issue_type=IssueType.MISSING.value,
                    format_1='schema_fields_descriptions',
                    format_2='description',
                    details=f"Field '{field_name}' has empty description"
                ))
        
        return issues
    
    def generate_consistency_report(self, issues: Dict[str, List[ConsistencyIssue]], schema_name: str) -> str:
        """Generate a human-readable consistency report"""
        report = [f"\n🔍 Schema Consistency Report: {schema_name}"]
        report.append("=" * 60)
        
        total_issues = sum(len(issue_list) for issue_list in issues.values())
        
        if total_issues == 0:
            report.append("✅ No consistency issues found!")
            return "\n".join(report)
        
        report.append(f"❌ Found {total_issues} consistency issues:\n")
        
        for category, issue_list in issues.items():
            if issue_list:
                report.append(f"📋 {category.replace('_', ' ').title()}:")
                for i, issue in enumerate(issue_list, 1):
                    report.append(f"  {i}. [{issue.field_name}] {issue.details}")
                report.append("")
        
        return "\n".join(report)


class SchemaValidationSummary:
    """Generates validation summaries and reports"""
    
    @staticmethod
    def generate_batch_validation_summary(valid_schemas: List[str], 
                                        invalid_schemas: List[str], 
                                        total_schemas: int) -> str:
        """Generate summary report for batch validation"""
        lines = [
            "\n" + "=" * 60,
            "📊 VALIDATION SUMMARY",
            "=" * 60
        ]
        
        if not invalid_schemas:
            lines.append(f"🎉 SUCCESS: All {total_schemas} schemas are consistent!")
        else:
            lines.extend([
                "⚠️  ISSUES FOUND:",
                f"   ✅ Valid schemas: {len(valid_schemas)}",
                f"   ❌ Invalid schemas: {len(invalid_schemas)}"
            ])
            
            if invalid_schemas:
                lines.extend([
                    "\n🔧 Schemas needing attention:",
                    *[f"   • {schema}" for schema in invalid_schemas]
                ])
        
        return "\n".join(lines)


# Public API Functions

def validate_schema_consistency(schema_data: Dict, schema_name: str, debug: bool = False) -> bool:
    """
    Validate schema consistency and print report
    
    Args:
        schema_data: Schema data dictionary
        schema_name: Name of the schema for reporting
        debug: Enable debug output
        
    Returns:
        bool: True if no issues found, False otherwise
    """
    checker = SchemaConsistencyChecker()
    issues = checker.check_schema_consistency(schema_data, debug=debug)
    report = checker.generate_consistency_report(issues, schema_name)
    
    print(report)
    
    # Return True if no issues found
    total_issues = sum(len(issue_list) for issue_list in issues.values())
    return total_issues == 0


def validate_schema_registry_formats_for_all_schemas(schemas_dict: Dict, stop_on_first_error: bool = False, debug: bool = False) -> bool:
    """
    Validate all schemas in your TABLE_SCHEMAS
    
    Args:
        schemas_dict: Dictionary of schema definitions
        stop_on_first_error: If True, stop validation on first schema with issues
        debug: Enable debug output
    
    Returns:
        bool: True if all schemas are valid, False otherwise
    """
    all_valid = True
    valid_schemas = []
    invalid_schemas = []
    
    print(f"🔍 Starting validation of {len(schemas_dict)} schemas...")
    print("=" * 60)
    
    for i, (schema_name, schema_data) in enumerate(schemas_dict.items(), 1):
        print(f"\n🔄 [{i}/{len(schemas_dict)}] Validating {schema_name}...")
        
        try:
            is_valid = validate_schema_consistency(schema_data, schema_name, debug=debug)
            
            if is_valid:
                valid_schemas.append(schema_name)
                print(f"✅ {schema_name} - PASSED")
            else:
                invalid_schemas.append(schema_name)
                all_valid = False
                print(f"❌ {schema_name} - FAILED")
                
                if stop_on_first_error:
                    print(f"\n⚠️ Stopping validation due to first error in {schema_name}")
                    break
                    
        except (ValueError, KeyError, AttributeError) as e:
            print(f"💥 ERROR validating {schema_name}: {str(e)}")
            invalid_schemas.append(schema_name)
            all_valid = False
            
            if stop_on_first_error:
                print(f"\n⚠️ Stopping validation due to error in {schema_name}")
                break
    
    # Generate and print summary
    summary = SchemaValidationSummary.generate_batch_validation_summary(
        valid_schemas, invalid_schemas, len(schemas_dict)
    )
    print(summary)
    
    return all_valid


# Convenience exports
__all__ = [
    'validate_schema_registry_formats_for_all_schemas',
    'validate_schema_consistency', 
    'SchemaConsistencyChecker',
    'ConsistencyIssue',
    'IssueType',
    'StorageType'
]
