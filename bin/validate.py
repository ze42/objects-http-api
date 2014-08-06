#! /usr/bin/python

import sys
import json
import yaml
import jsonschema

def load_file(filename):
    if filename.endswith('.json'):
        return json.load(open(filename))
    return yaml.load(open(filename).read())

def usage():
    print """Usage:
  {0} schema data

schema  file containing schema to validate against
data    file containing the data to validate

Input can be a .json file, or any file containing yaml valid data.
""".format(sys.argv[0])
    sys.exit(2)

if len(sys.argv) != 3:
    usage()

schema = load_file(sys.argv[1])
data = load_file(sys.argv[2])

jsonschema.Draft4Validator.check_schema(schema)
validator = jsonschema.Draft4Validator(schema)

#print(best_match(jsonschema.Draft4Validator(schema).iter_errors(data)).message)
#sys.exit(0)
try:
    validator.validate(data)
    print "Ok"
except jsonschema.SchemaError as err:
    print "Invalid schema"
    print err
    sys.exit(3)
except jsonschema.ValidationError as err:
    print "Invalid data"
    print err
    sys.exit(1)
