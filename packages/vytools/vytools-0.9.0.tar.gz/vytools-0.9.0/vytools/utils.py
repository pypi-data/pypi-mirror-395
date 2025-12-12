import os, re, json, copy, numbers

ITEMS = {}
BASE_DATA_TYPES = {
  'float32':{'validation':lambda x : isinstance(x,numbers.Real), 'default':0},
  'float64':{'validation':lambda x : isinstance(x,numbers.Real), 'default':0},
  'uint64':{'validation':lambda x : isinstance(x,numbers.Integral) and x >= 0, 'default':0},
  'int64':{'validation':lambda x : isinstance(x,numbers.Integral), 'default':0},
  'uint32':{'validation':lambda x : isinstance(x,numbers.Integral) and x < 4294967296 and x >= 0, 'default':0},
  'int32':{'validation':lambda x : isinstance(x,numbers.Integral) and x < 2147483648 and x >= -2147483648, 'default':0},
  'uint16':{'validation':lambda x : isinstance(x,numbers.Integral) and x < 65536 and x >= 0, 'default':0},
  'int16':{'validation':lambda x : isinstance(x,numbers.Integral) and x < 32768 and x >= -32768, 'default':0},
  'uint8':{'validation':lambda x : isinstance(x,numbers.Integral) and x < 256 and x >= 0, 'default':0},
  'int8':{'validation':lambda x : isinstance(x,numbers.Integral) and x < 128 and x >= -128, 'default':0},
  'string':{'validation':lambda x : isinstance(x,str), 'default':''},
  'bool':{'validation':lambda x : isinstance(x,bool), 'default':False},
  'blackbox':{'validation':lambda x : True, 'default':{}},
  'byte':{'validation':lambda x : True, 'default':0},
  'char':{'validation':lambda x : isinstance(x,str) and len(x) == 1, 'default':'-'}
}

BASE_SCHEMA = {
  'path': {'type':'string', 'maxlength': 1024,'required':True},
  'name': {'type':'string', 'maxlength': 64,'required':True},
  'depends_on':{'type':'list','schema': {'type': 'string', 'maxlength':256},'required':True},
  'loaded':{'type':'boolean','required':True}
}

def search_all(fname_regex, func, items, contextpaths):
  success = True
  exclude = set(['.vy','.git','.hg'])
  for cp in contextpaths:
    for root, dirs, files in os.walk(cp, topdown=True):
      dirs[:] = [d for d in dirs if d not in exclude]
      if fname_regex and func:
        for f in files:
          m = re.match(fname_regex,f,re.I)
          if m:
            success &= func(m.group(1), os.path.join(root, f), items)
  return success

def topological_sort(source):
    pending = [(name, set(deps)) for name, deps in source]        
    emitted = []
    while pending:
      next_pending = []
      next_emitted = []
      for entry in pending:
        name, deps = entry
        deps.difference_update(set((name,)), emitted)
        if deps:
          next_pending.append(entry)
        else:
          yield name
          emitted.append(name)
          next_emitted.append(name)
      if not next_emitted:
        raise ValueError("cyclic dependency detected {n}: pending={p}".format(n=name,p=pending))
      pending = next_pending
      emitted = next_emitted
    return emitted

def exists(lst, items, pad=''):
  success = True
  for l in lst:
    if l not in items:
      success = False
      print('"{n}" was not found {p}'.format(n=l,p=pad))
    else:
      success &= exists(items[l]['depends_on'],items,'(depended on by {})'.format(l))
  return success

def recursive_get_check(l,lst,items):
  if l not in lst and l in items:
    lst.append(l)
    for ll in items[l].get('depends_on',[]):
      recursive_get_check(ll,lst,items)

def sort(lst, items):
  all_in_list = []
  for l in lst:
    recursive_get_check(l, all_in_list, items)
  return [x for x in topological_sort([(k,set(items[k]['depends_on'])) for k in all_in_list]) if x in lst]

def ok_dependency_loading(action,type_name,items):
  if type_name not in items or not items[type_name]['loaded']:
    print('Cannot {} "{}" because it did not load properly'.format(action,type_name))
    return False
  for d in items[type_name]['depends_on']:
    if not ok_dependency_loading(action,d,items):
      return False
  return True

def _check_self_dependency(id,item):
  n = len(item['depends_on'])
  item['depends_on'][:] = [dep for dep in item['depends_on'] if dep != id]
  if n != len(item['depends_on']):
    item['loaded'] &= False
    print('Item "{n}" should not depend on itself'.format(n=id))

def _check_add(nme, typ, item, items, parent):
  if nme.startswith(typ+':') and nme in items:
    item['depends_on'].append(nme)
    return True
  print('Failed to find subitem "{n}" referenced by "{p}".\n  - "{n}" is not of type {t} or does not exist'.format(n=nme, t=typ, p=parent))
  return False

def _add_item(item, items, validate):
  typ = item['thingtype']
  name = item['name']
  pth = item['path']
  tname = typ+':'+name
  if tname in items:
    pthp = items[tname]['path']
    i1 = copy.deepcopy(items[tname])
    i2 = copy.deepcopy(item)
    del i1['path']
    del i2['path']
    try:
      same = json.dumps(i1,sort_keys=True) == json.dumps(i2,sort_keys=True)
    except Exception as exc:
      same = False
    if same:
      print('Identical objects "{t}" at:\n    "{p}" (loaded) and \n    "{p2}" (not loaded)'.format(t=tname, p=pth, p2=pthp))
    else:
      print('"{t}" at "{p}" was not loaded because a same name item was already loaded from {p2}'.format(t=tname, p=pth, p2=pthp))
    return False
  elif validate==True or validate.validate(item):
    items[tname] = item
    return True
  else:
    print('"{n}" at "{p}" failed validation {s}'.format(n=tname, p=pth, s=validate.errors))
    return False

def missing_item(type_name, items):
  if not items:
    print('No items are included. Do you have items defined? Have you scanned for them?')
  else:
    examples = []
    for k in items.keys():
      if not any([e.startswith(k.split(':')[0]+':') for e in examples]):
       examples.append(k)
    print('Item "{}" not found in vy items. Check the spelling and format.  Example items:\n  {}'.format(type_name,'\n  '.join(examples)))
