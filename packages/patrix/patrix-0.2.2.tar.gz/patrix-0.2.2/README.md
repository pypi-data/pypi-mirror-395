# Patrix

[![pipeline](https://github.com/martinberoiz/patrix/actions/workflows/test.yml/badge.svg)](https://github.com/martinberoiz/patrix/actions/workflows/test.yml)
[![docs](https://readthedocs.org/projects/patrix/badge/?version=latest)](https://patrix.readthedocs.io/)
[![python](https://img.shields.io/pypi/pyversions/patrix)](https://pypi.org/project/patrix/)
[![license](https://img.shields.io/pypi/l/patrix)](https://github.com/martinberoiz/patrix/blob/main/LICENSE.txt)

Patrix provides a radix tree class (aka trie, compressed prefix tree, or compact prefix tree)
that behaves mostly like a python dictionary
but provides quick and efficient completion suggestions for partial word entries.

This is useful for building autocomplete systems of long lists of known strings that share common prefixes.
This is typical for hierarchical naming systems
like file paths, IP addresses, or domain names, but it is not limited to those examples.

## Radix tree example

```python
>>> from patrix import RadixTree
>>> # Entries can be a list of strings or key-value tuples
>>> r = RadixTree(("computer", "compute", ("computing", 1)))
>>> r.asdict()
{'comput': {'e': {'': {}, 'r': {}}, 'ing': {}}}
>>> s = RadixTree.from_dict({'comput': {'e': {'': {}, 'r': {}}, 'ing': {}}})
>>> s.asdict()
{'comput': {'e': {'': {}, 'r': {}}, 'ing': {}}}
```

Display suggestions on how to continue a given query prefix

```python
>>> r.completions("c")
{'comput'}
>>> r.completions("comput")
{'compute', 'computing'}
>>> r.completions("compute") # The word 'compute' here is both a stem and a final word
{'compute', 'computer'}
>>> r.completions("p")
set()
```

`RadixTree` behaves like a python dictionary:

```python
>>> r["computer"] = 1
>>> r["compute"] = 2
>>> r["computing"] = 3
>>> r.pop("compute")
2
>>> "computing" in r
True
>>> r["computing"]
3
```

## Compression rate

```python
>>> r.total_chars
11
>>> len("computer" + "computing" + "compute")
24
>>> 1 - 11 / 24  # 54% compression rate
0.5416666666666667
>>> r.size  # nodes in the tree excluding the root
6
```
