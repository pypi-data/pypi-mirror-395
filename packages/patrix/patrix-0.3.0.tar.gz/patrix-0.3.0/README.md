# Patrix

[![pipeline](https://github.com/martinberoiz/patrix/actions/workflows/test.yml/badge.svg)](https://github.com/martinberoiz/patrix/actions/workflows/test.yml)
[![docs](https://readthedocs.org/projects/patrix/badge/?version=latest)](https://patrix.readthedocs.io/)
[![python](https://img.shields.io/pypi/pyversions/patrix)](https://pypi.org/project/patrix/)
[![license](https://img.shields.io/pypi/l/patrix)](https://github.com/martinberoiz/patrix/blob/main/LICENSE.txt)

Patrix provides a `RadixTree` class
(aka [trie](https://en.wikipedia.org/wiki/Trie), [compressed prefix tree](https://en.wikipedia.org/wiki/Radix_tree), or compact prefix tree)
that behaves like a python dictionary
([`abc.MutableMapping`](https://docs.python.org/3.10/library/collections.abc.html#collections-abstract-base-classes) subclass)
but provides quick and efficient completion suggestions for partial word entries.

This is useful for building autocomplete systems of long lists of known strings that share common prefixes.
This is typical for hierarchical naming systems
like file paths, IP addresses, or domain names, but it is not limited to those examples.

## Usage

### Autocomplete System

```python
from patrix import RadixTree

words = [
    "python",
    "programming",
    "program",
    "project",
    "package",
]
autocomplete = RadixTree(words)
```

Query for possible completions of a partial word:

```python
# Example usage
>>> autocomplete.completions()
{'p'}
>>> autocomplete.completions("p")
{'package', 'pro', 'python'}
>>> autocomplete.completions("pro")
{'program', 'project'}
>>> autocomplete.completions("program")
{'program', 'programming'}
>>> autocomplete.completions("programming")
set()
```

### Save and load a tree

```python
>>> from patrix import RadixTree
>>> # Entries can be a list of strings or key-value tuples
>>> r = RadixTree(("computer", "compute", ("computing", 1)))
>>> # Save to disk as JSON
>>> r.asdict()
{'comput': {'e': {'': {}, 'r': {}}, 'ing': {"__value__": 1}}}
>>> # Load using from_dict
>>> s = RadixTree.from_dict({'comput': {'e': {'': {}, 'r': {}}, 'ing': {"__value__": 1}}})
>>> s.asdict()
{'comput': {'e': {'': {}, 'r': {}}, 'ing': {"__value__": 1}}}
```

Compression rate for this tree:

```python
>>> r.total_chars
11
>>> len("computer" + "computing" + "compute")
24
>>> 1 - 11 / 24  # 54% compression rate
0.5416666666666667
>>> r.size  # nodes in the tree
6
```

### Use it like a regular dictionary

`RadixTree` behaves like a regular python dictionary,
but the insertion order is not preserved.

```python
>>> r = RadixTree()
>>> r["computer"] = 1
>>> r["compute"] = 2
>>> "computer" in r
True
>>> r["computer"]
1
>>> r.pop("compute")
2
>>> "compute" in r
False
>>> s = r | {"computing": 3}
>>> "computing" in s
True
>>> "computing" in r
False
>>> del s["computing"]
>>> r == s
True
```
