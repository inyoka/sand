import sys

def dump(obj, nested_level=0, output=sys.stdout):
    spacing = '   '
    if type(obj) == dict:
        print('%s{' % ((nested_level) * spacing), file=output)
        for k, v in list(obj.items()):
            if hasattr(v, '__iter__'):
                print('%s%s:' % ((nested_level + 1) * spacing, k), file=output)
                dump(v, nested_level + 1, output)
            else:
                print('%s%s: %s' % ((nested_level + 1) * spacing, k, v), file=output)
        print('%s}' % (nested_level * spacing), file=output)
    elif type(obj) == list:
        print('%s[' % ((nested_level) * spacing), file=output)
        for v in obj:
            if hasattr(v, '__iter__'):
                dump(v, nested_level + 1, output)
            else:
                print('%s%s' % ((nested_level + 1) * spacing, v), file=output)
        print('%s]' % ((nested_level) * spacing), file=output)
    else:
        print('%s%s' % (nested_level * spacing, obj), file=output)
