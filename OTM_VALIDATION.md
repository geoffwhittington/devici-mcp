# OTM Schema Validation

This project now includes **automatic validation** of Open Threat Model (OTM) files against the official [IriusRisk OTM schema](https://github.com/iriusrisk/OpenThreatModel/blob/main/otm_schema.json).

## ✅ **What's Validated**

Every OTM file created or imported is automatically validated to ensure:

- **Proper structure** - All required fields are present
- **Correct data types** - Strings, numbers, arrays in the right places  
- **Valid relationships** - Components, threats, and mitigations link correctly
- **Schema compliance** - Follows OTM v0.2.0 specification exactly

## 🛠️ **Validation Tools**

### 1. **Standalone Validator** (`otm_validator.py`)

Validate any OTM file manually:

```bash
# Validate a single file
python otm_validator.py my-threat-model.otm

# Validate all OTM files in current directory
python otm_validator.py --validate-all

# Show schema information
python otm_validator.py --schema-info
```

### 2. **Integrated MCP Server Validation**

The MCP server automatically validates OTM files during:

- **`create_otm_from_description()`** - Before saving OTM files
- **`import_otm_to_devici()`** - Before uploading to Devici platform

## 📋 **Common Validation Errors**

Based on validation of existing files, here are the most common issues:

### **Missing 'risk' property in threats**
```json
// ❌ Invalid - missing risk object
{
  "id": "threat-1",
  "name": "SQL Injection",
  "description": "Attacker injects malicious SQL"
}

// ✅ Valid - includes required risk object
{
  "id": "threat-1", 
  "name": "SQL Injection",
  "description": "Attacker injects malicious SQL",
  "risk": {
    "likelihood": 50,
    "impact": 80,
    "likelihoodComment": "Common web vulnerability",
    "impactComment": "Could expose sensitive data"
  }
}
```

### **Incorrect assets format**
```json
// ❌ Invalid - assets should be object or null, not array
{
  "assets": []
}

// ✅ Valid - proper asset instance object
{
  "assets": {
    "processed": ["asset-id-1", "asset-id-2"], 
    "stored": ["asset-id-1"]
  }
}

// ✅ Also valid - null when no assets
{
  "assets": null
}
```

## 🔧 **Fixing Validation Errors**

1. **Run the validator** to see specific error locations
2. **Check the schema** - Reference `otm_schema.json` for exact requirements
3. **Fix the issues** - Update your OTM file structure
4. **Re-validate** to confirm fixes

## 📚 **Schema Reference**

- **Official Schema**: [otm_schema.json](https://github.com/iriusrisk/OpenThreatModel/blob/main/otm_schema.json)
- **Documentation**: [IriusRisk OTM Standard](https://www.iriusrisk.com/the-open-threat-model-standard)
- **Examples**: [OpenThreatModel Examples](https://github.com/iriusrisk/OpenThreatModel)

## 🚀 **Benefits**

- **Quality Assurance** - Only valid OTM files are created/imported
- **Better Compatibility** - Files work across all OTM-compatible tools
- **Early Error Detection** - Catch issues before they reach Devici
- **Professional Standards** - Ensures enterprise-grade threat model format

The validation runs automatically in the background, providing error messages when issues are found so you can create perfect OTM files every time! 🎯 