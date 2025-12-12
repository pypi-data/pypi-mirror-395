import json
from jsonschema.validators import Draft7Validator,Draft202012Validator
import os
from pathlib import Path
"""
Load JSON schemas for POPxf files. Match schema files to their validators.
"""

# map of filenames to loaded schema dicts
schemas = {}
# map of filenames to corresponding jsonschema Validator classes
validators = {}

# Map of known $schema URIs to their corresponding jsonschema Validator classes
known_validators = {
  "http://json-schema.org/draft-07/schema#": Draft7Validator,
  "https://json-schema.org/draft/2020-12/schema": Draft202012Validator
}

schema_dir = Path(__file__).parent / "schemas"
for schemafile in schema_dir.glob('popxf-*.json'):
    # Load schema and determine appropriate validator
    schema = json.load(open(schemafile))
    schema['$schema'] # schema of schema file

    # populate maps
    filename = os.path.basename(schemafile)
    schemas[filename] = schema
    validators[filename] = known_validators[schema['$schema']]
