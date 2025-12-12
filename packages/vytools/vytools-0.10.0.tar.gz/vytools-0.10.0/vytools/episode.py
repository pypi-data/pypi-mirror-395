import vytools.utils
import vytools.object
import json, copy, io, itertools
import cerberus
PERMUTATION_DELIMITER = '@'
SCHEMA = vytools.utils.BASE_SCHEMA.copy()

SCHEMA.update({
  'thingtype':{'type':'string', 'allowed':['episode']},
  'objects':{'type': 'dict', 'required': False},
  'permutations':{'type': 'dict', 'required': False, 'schema': {
    'labels':{'type': 'dict', 'required': False},
    'groups':{'type': 'list', 'required': False, 'schema':{
      'type':'list', 'schema':{
        'type':'list', 'schema':{
          'type':'string','maxlength':128
        }
      }
    }}
  }},
  'results':{'type': 'dict', 'required': False}
})
VALIDATE = cerberus.Validator(SCHEMA)

def parse(name, pth, items):
  item = {'name':name, 'thingtype':'episode', 'path':pth, 'loaded':True}
  type_name = 'episode:' + name
  item['depends_on'] = []
  try:
    content = json.load(io.open(pth, 'r', encoding='utf-8-sig'))
    for sc in SCHEMA:
      if sc in content: # and sc not in ['repos']: TODO I want this sometimes so I took the filter out. Hopefully I don't have to put it back in
        item[sc] = content[sc]
    vytools.utils._check_self_dependency(type_name, item)
    # object_mods can come from:
    #  1. from the episode file "permutations" field
    #  2. from the modifications of the object in the episode file "objects" field
    # The order here is the priority. That is, "permutations" overrides anything in the "objects"
    objects = copy.deepcopy(item['objects']) if 'objects' in item else {}
    permutations = {}
    if 'permutations' in item and 'groups' in item['permutations'] and len(item['permutations']['groups']) > 0:
      for perma in item['permutations']['groups']:
        for permb in list(itertools.product(*perma)):
          suffx = ''
          objp = {}
          for labl in permb:
            suffx += PERMUTATION_DELIMITER+labl
            deepmerge(objp, item['permutations']['labels'][labl])
          permutations[suffx] = objp
    else:
      permutations[''] = objects

    added = vytools.utils._add_item(item, items, VALIDATE)
    item['__permutations'] = permutations
    return added
  except Exception as exc:
    print('Failed to parse episode "{n}" at "{p}": {e}'.format(n=name, p=pth, e=exc))
    return False

def deepmerge(a, b, path=None): # merge b into a (b prioritized over a)
    if path is None: path = []
    for key in b:
        if key in a and isinstance(a[key], dict) and isinstance(b[key], dict):
          deepmerge(a[key], b[key], path + [str(key)])
        else:
            a[key] = copy.deepcopy(b[key])

def find_all(items, contextpaths):
  return vytools.utils.search_all(r'(.+)\.episode\.json', parse, items, contextpaths)

def get_episode_permutations(episode_name, items=None):
  if items is None: items = vytools.utils.ITEMS
  if episode_name not in items:
    vytools.utils.missing_item(episode_name, items)
    return []
  ep = items[episode_name]
  return [ep['name']+s for s in ep['__permutations'].keys()]

def expand_episode_objects(episode_name, items=None):
  if items is None: items = vytools.utils.ITEMS
  ep = items[episode_name]
  objects_ = {}
  for k,v in ep.get('objects',{}).items():
    base = v.get('base',None)
    obj,dep = vytools.object.expand(base)
    definition = vytools.utils.ITEMS.get(base,{}).get('definition',None)
    if obj is not None and definition is not None:
      obj,dep = vytools.object.expand(obj, definition, object_mods=v.get('modifications',{}))
      objects_[k] = {'object':obj,'definition':definition}
  return objects_
  
def expand_permutation_objects(permutation, items=None, objects_=None):
  if items is None: items = vytools.utils.ITEMS
  splitt = permutation.split('@',1)
  episode_name = splitt[0]
  if episode_name not in items:
    vytools.utils.missing_item(episode_name, items)
    return {}
  if objects_ is None:
    objects_ = expand_episode_objects(episode_name, items)
  ep = items[episode_name]
  suffix = '' if len(splitt) <= 1 else '@'+splitt[1]
  obj = {}
  if suffix not in ep['__permutations'] not in perms:
    vytools.utils.missing_item(permutation, items)
  else:
    for k,v in ep['__permutations'][suffix].items():
      pobj = objects_.get(k,None)
      if pobj:
        obj[k] = copy.deepcopy(pobj['object'])
        obj[k],dep = vytools.object.expand(obj[k], pobj['definition'], object_mods=v)
  return obj

  # stamp = os.stat(filename).st_mtime
  # if stamp != _cached_stamp:
  #     _cached_stamp = stamp
  #     # File has changed, so do something...