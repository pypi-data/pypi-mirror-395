# Patrix

[![pipeline](https://github.com/martinberoiz/patrix/actions/workflows/test.yml/badge.svg)](https://github.com/martinberoiz/patrix/actions/workflows/test.yml)
[![docs](https://readthedocs.org/projects/patrix/badge/?version=latest)](https://patrix.readthedocs.io/)
[![python](https://img.shields.io/pypi/pyversions/patrix)](https://pypi.org/project/patrix/)
[![license](https://img.shields.io/pypi/l/patrix)](https://github.com/martinberoiz/patrix/blob/main/LICENSE.txt)

A python package that uses a radix tree (aka trie, compressed prefix tree, or compact prefix tree)
to store a dictionary of known words and provides suggestions to complete partial words.

It is used in autocomplete systems to provide suggestions to users based on the words they have typed.

## Trie example

```python
>>> from patrix import Trie
>>> t = Trie((("trie", 1), ("try", 2), ("tree", 3)))
>>> t.as_dict()
{'t': {'r': {'i': {'e': {}}, 'y': {}, 'e': {'e': {}}}}}
```

Search for a word in the trie:

```python
>>> t.search("tri")
<patrix.trie.TrieNode object at 0x7f952c171c10>
>>> t.search("tri").get_key()
'tri'
>>> t.search("trio") is None
True
```

Add a new word to the trie:

```python
>>> t.insert("trio", 4)
>>> t.as_dict()
{'t': {'r': {'e': {'e': {}}, 'i': {'e': {}, 'o': {}}, 'y': {}}}}
```

## Radix tree example

```python
>>> from patrix import RadixTree
>>> # Entries can be a list of strings or key-value tuples
>>> r = RadixTree(("computer", "compute", ("computing", 1)))
>>> r.as_dict()
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
