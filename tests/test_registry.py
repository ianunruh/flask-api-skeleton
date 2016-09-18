import pytest

from backend.registry import Registry

class Example1Plugin(object):
    key = 'example1'

class Example2Plugin(object):
    key = 'example2'

def test_registry():
    registry = Registry()

    plugins = [Example1Plugin, Example2Plugin]

    registry.register(*plugins)

    assert registry.get('example1') == Example1Plugin
    assert registry.get('example3') == None
    assert len(registry) == 2

    assert set(registry) == set(plugins)
