class MetaData(object):
    '''Utility class for enriching data structures with meta data, e.g. qtype hint.'''
    def __init__(self, **kw):
        self.__dict__.update(kw)

    def __repr__(self):
        if not self.__dict__.items():
            return 'metadata()'

        s = ['metadata(']
        for k, v in self.__dict__.items():
            s.append('%s=%s' % (k, repr(v)))
            s.append(', ')
        s[-1] = ')'
        return ''.join(s)

    def __getattr__(self, attr):
        return None

    def __getitem__(self, key):
        return self.__dict__.get(key, None)

    def __setitem__(self, key, value):
        self.__dict__[key] = value

    def as_dict(self):
        return self.__dict__.copy()

    def union_dict(self, **kw):
        return dict(list(self.as_dict().items()) + list(kw.items()))


CONVERSION_OPTIONS = MetaData(raw = False,
                              numpy_temporals = False,
                              pandas = False,
                              single_char_strings = False
                             )