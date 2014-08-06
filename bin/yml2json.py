#! /usr/bin/python

import sys
import yaml
import json
import collections

KEYS_NICE_ORDER = [
  '$schema',
  'title',
  'description',
  '$ref',
  'id',
  'definitions',
  'type',


  # Properties
  'properties',
  'required',
  'additionalProperties',
  'patternProperties',


  # Instead of defining it, use those options
  'anyOf',
  'allOf',
  'oneOf',
  'not',

  # Complex type use
  'enum',
  'items',
  'subtype',
  'on-ref-delete',

  # Some types use those
  'minItems',
  'uniqueItems',

  # Extended attributes
  "_ref", 
  "_type",
  "_count",
  "_add",
  "_remove",

  # main attributes
  'name',
  'aliases',
  'desc',
  'key',
  'attributes',
  'refpath',

  # Search properties
  "search", 
  "create",
  "update",
  "delete",
  "output-fields",

  # Specific to our definitions
  'stringSet',
  'stringOrSet', 
  'simpleValue',

  # Objects
  'objectTypes',
  'objectType',
  'objectAttributes',
  'objectAttribute',
  'objectAttributeSimple',
  'objectAttributeSet',
  'objectAttributeRef',
  "objectAttributeRefAlias",

  "identifiedObject",
  "identifiedObjects",
  "fullUpdateRequest",
  "createRequest",
  "updateRequest", 
  "deleteRequest",

  "searchRequest", 
  "searchFilter", 
  "searchFilterProperty",
  "outputFields", 

  "minimum",

  # Only appears alone anyway
  "_all", 
  "_any", 
]

#^[a-z0-9]+(-[a-z0-9]+)*$


unknown_keys = set()

def usage():
    """Display usage and exits"""
    sys.exit(u"Usage:\n\t{0} file.yml [...]\n".format(sys.argv[0]))


def load_yaml(filename):
    """Load yaml from a file"""
    return yaml.load(open(filename).read())


def dump_json(filename, data):
    """Dump to a file in JSON"""
    with open(filename, 'w') as fp:
        json.dump(data, fp, indent=4)

def key_pos(key):
    """ Position of the key in our keys_nice_order """
    try:
        return (KEYS_NICE_ORDER.index(key), key)
    except ValueError:
        global unknown_keys
        unknown_keys.add(key)
        return (len(KEYS_NICE_ORDER), key)

def friendly_sort(keys):
    """
    Friendly sort our keys
    """
    return sorted(keys, key=key_pos)

def transform(data):
    """ Transform our data to what we would like to present """
    if isinstance(data, list):
        return [ transform(val) for val in data ]
    if isinstance(data, dict):
        return collections.OrderedDict(
            [ (key, transform(data[key]))
                for key in friendly_sort(data.keys())
            ])
    return data


if len(sys.argv) < 2:
    usage()


for filename in sys.argv[1:]:
    if not filename.endswith('.yml'):
        sys.exit(u'{0}: unrecognized filename'.format(filename))


for filename in sys.argv[1:]:
    print filename
    data = load_yaml(filename)
    data = transform(data)
    dump_json(u'{0}.json'.format(filename[:-4]), data)

if unknown_keys:
    print "Unknown keys:"
    print json.dumps(list(unknown_keys), indent=2)
