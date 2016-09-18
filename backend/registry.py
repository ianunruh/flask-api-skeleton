import six


class Registry(object):
    def __init__(self):
        self._plugins = {}

    def get(self, key):
        return self._plugins.get(key)

    def register(self, *args):
        for plugin_cls in args:
            self._plugins[plugin_cls.key] = plugin_cls

    def __iter__(self):
        return six.itervalues(self._plugins)

    def __len__(self):
        return len(self._plugins)
