#!/usr/bin/env python3
"""
OTM Validator - Validates Open Threat Model files against the official schema

This utility validates OTM (Open Threat Model) files to ensure they conform to
the official IriusRisk OTM JSON schema specification.

Usage:
    python otm_validator.py <otm_file_path>
    python otm_validator.py --validate-all  # Validates all .otm files in current directory
"""

import json
import argparse
import sys
import os
from pathlib import Path
from typing import List, Tuple
import jsonschema
from jsonschema import validate, ValidationError, SchemaError


def load_otm_schema() -> dict:
    """Load the OTM JSON schema from the local file."""
    schema_path = Path(__file__).parent / "otm_schema.json"
    
    if not schema_path.exists():
        raise FileNotFoundError(
            f"OTM schema file not found at {schema_path}. "
            "Please ensure otm_schema.json is in the project root."
        )
    
    try:
        with open(schema_path, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in schema file: {e}")


def load_otm_file(file_path: str) -> dict:
    """Load and parse an OTM file."""
    try:
        with open(file_path, 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        raise FileNotFoundError(f"OTM file not found: {file_path}")
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON in OTM file: {e}")


def validate_otm_file(otm_data: dict, schema: dict) -> Tuple[bool, str]:
    """
    Validate OTM data against the schema.
    
    Returns:
        Tuple[bool, str]: (is_valid, error_message)
    """
    try:
        validate(instance=otm_data, schema=schema)
        return True, "OTM file is valid! ✅"
    except ValidationError as e:
        error_msg = f"Validation failed ❌\n"
        error_msg += f"Error at: {' -> '.join(str(x) for x in e.absolute_path)}\n"
        error_msg += f"Message: {e.message}\n"
        if e.context:
            error_msg += f"Context: {'; '.join(err.message for err in e.context)}"
        return False, error_msg
    except SchemaError as e:
        return False, f"Schema error: {e.message}"


def get_otm_info(otm_data: dict) -> dict:
    """Extract key information from OTM data for display."""
    info = {
        'version': otm_data.get('otmVersion', 'Unknown'),
        'project_name': otm_data.get('project', {}).get('name', 'Unknown'),
        'project_id': otm_data.get('project', {}).get('id', 'Unknown'),
        'components_count': len(otm_data.get('components', [])),
        'threats_count': len(otm_data.get('threats', [])),
        'mitigations_count': len(otm_data.get('mitigations', [])),
        'trustzones_count': len(otm_data.get('trustZones', [])),
        'dataflows_count': len(otm_data.get('dataflows', []))
    }
    return info


def validate_single_file(file_path: str, schema: dict) -> bool:
    """Validate a single OTM file and print results."""
    print(f"\n📄 Validating: {file_path}")
    print("=" * 60)
    
    try:
        otm_data = load_otm_file(file_path)
        is_valid, message = validate_otm_file(otm_data, schema)
        
        # Show file info
        info = get_otm_info(otm_data)
        print(f"📋 Project: {info['project_name']} (ID: {info['project_id']})")
        print(f"📊 OTM Version: {info['version']}")
        print(f"🏗️  Components: {info['components_count']}")
        print(f"⚠️  Threats: {info['threats_count']}")
        print(f"🛡️  Mitigations: {info['mitigations_count']}")
        print(f"🏛️  Trust Zones: {info['trustzones_count']}")
        print(f"🔄 Data Flows: {info['dataflows_count']}")
        print()
        print(message)
        
        return is_valid
        
    except Exception as e:
        print(f"❌ Error processing file: {e}")
        return False


def find_otm_files(directory: str = ".") -> List[str]:
    """Find all .otm files in the specified directory."""
    otm_files = []
    for file_path in Path(directory).glob("*.otm"):
        otm_files.append(str(file_path))
    
    # Also check for .json files that might be OTM
    for file_path in Path(directory).glob("*.json"):
        if "otm" in file_path.name.lower() or "threat" in file_path.name.lower():
            otm_files.append(str(file_path))
    
    return sorted(otm_files)


def main():
    parser = argparse.ArgumentParser(description='Validate OTM files against the official schema')
    parser.add_argument('file_path', nargs='?', help='Path to the OTM file to validate')
    parser.add_argument('--validate-all', action='store_true', 
                       help='Validate all OTM files in current directory')
    parser.add_argument('--schema-info', action='store_true',
                       help='Show information about the OTM schema')
    
    args = parser.parse_args()
    
    # Load schema
    try:
        schema = load_otm_schema()
        print("🔧 Loaded OTM Schema successfully")
        
        if args.schema_info:
            print(f"📜 Schema ID: {schema.get('$id', 'Unknown')}")
            print(f"📜 Schema Title: {schema.get('title', 'Unknown')}")
            print(f"📜 Schema Version: {schema.get('$schema', 'Unknown')}")
            return
            
    except Exception as e:
        print(f"❌ Failed to load OTM schema: {e}")
        sys.exit(1)
    
    # Validation logic
    if args.validate_all:
        otm_files = find_otm_files()
        if not otm_files:
            print("❌ No OTM files found in current directory")
            sys.exit(1)
            
        print(f"🔍 Found {len(otm_files)} OTM file(s) to validate:")
        for f in otm_files:
            print(f"  - {f}")
        
        valid_count = 0
        for file_path in otm_files:
            if validate_single_file(file_path, schema):
                valid_count += 1
        
        print(f"\n📊 Summary: {valid_count}/{len(otm_files)} files are valid")
        
        if valid_count < len(otm_files):
            sys.exit(1)
            
    elif args.file_path:
        if not validate_single_file(args.file_path, schema):
            sys.exit(1)
    else:
        print("❌ Please specify a file path or use --validate-all")
        parser.print_help()
        sys.exit(1)
    
    print("\n🎉 Validation complete!")


if __name__ == "__main__":
    main() 