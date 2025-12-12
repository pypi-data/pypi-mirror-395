"""
Trie (prefix tree) data structure implementation.

This module provides a Trie data structure that stores key-value pairs efficiently
for prefix-based lookups. Unlike a radix tree, a standard trie stores one character
per node, making it simpler but potentially more memory-intensive.
"""


class Trie:
    """
    A trie (prefix tree) data structure for efficient key-value storage.

    The Trie stores key-value pairs where each node represents a single character,
    allowing for fast prefix-based searches and insertions.

    Attributes
    ----------
    root : TrieNode
        The root node of the trie.
    """

    def __init__(self, key_value_pairs):
        """
        Initialize a Trie with a collection of key-value pairs.

        Parameters
        ----------
        key_value_pairs : iterable
            An iterable of (key, value) tuples to insert into the trie.
            Each key must be a non-empty string.

        Raises
        ------
        ValueError
            If any key is empty or not a string.
        """
        self.root = TrieNode()
        for key, value in key_value_pairs:
            self.insert(key, value)

    def insert(self, key, value):
        """
        Insert a key-value pair into the trie.

        If the key already exists, its value will be updated. Each character
        of the key is stored in a separate node.

        Parameters
        ----------
        key : str
            The key to insert. Must be a non-empty string.
        value
            The value to associate with the key.

        Raises
        ------
        ValueError
            If key is empty or not a string.
        """
        if key == "":
            raise ValueError("Key cannot be empty")
        if not isinstance(key, str):
            raise ValueError("Key must be a string")
        self.root.insert(key, value)

    def search(self, word):
        """
        Search for a node corresponding to the given word in the trie.

        Traverses the trie following the characters of the word and returns
        the node if found, or None if the word is not present in the trie.

        Parameters
        ----------
        word : str
            The word to search for. Must be a non-empty string.

        Returns
        -------
        TrieNode or None
            The node corresponding to the word if found, None otherwise.

        Raises
        ------
        ValueError
            If word is empty or not a string.
        """
        if word == "":
            raise ValueError("Word cannot be empty")
        if not isinstance(word, str):
            raise ValueError("Word must be a string")
        return self.root.search(word)

    def asdict(self):
        """
        Convert the trie to a nested dictionary representation.

        Returns
        -------
        dict
            A nested dictionary where each key is a character and the value
            is either another dictionary (for nodes with children) or None.
            Note: This representation does not preserve the values stored
            in leaf nodes, only the tree structure.
        """
        return self.root.asdict()


class TrieNode:
    """
    A node in the trie data structure.

    Each node stores a single character, an optional value, references to
    child nodes, and a reference to its parent node.

    Attributes
    ----------
    children : dict
        Dictionary mapping characters to child TrieNode instances.
    value
        The value stored at this node (None if this is not a leaf node).
    parent : TrieNode, optional
        Reference to the parent node (None for root).
    prefix : str
        The single character prefix associated with this node.
    """

    def __init__(self):
        """
        Initialize a TrieNode.

        Creates a new node with no children, no value, no parent, and
        an empty prefix.
        """
        self.children = {}
        self.value = None
        self.parent = None
        self.prefix = ""

    def insert(self, key, value):
        """
        Insert a key-value pair into the subtree rooted at this node.

        Recursively traverses or creates nodes for each character in the key,
        storing the value at the final node. If a path already exists for the
        key, the value is updated.

        Parameters
        ----------
        key : str
            The key to insert. If empty, stores the value at the current node.
        value
            The value to associate with the key.
        """
        if len(key) == 0:
            self.value = value
            return self
        prefix, suffix = key[0], key[1:]
        if prefix in self.children:
            child = self.children[prefix]
            child.insert(suffix, value)
            return

        # If there is no children with that key, create one
        child = TrieNode()
        self.children[prefix] = child
        child.parent = self
        child.prefix = prefix
        child.insert(suffix, value)

    def search(self, word):
        """
        Search for a node corresponding to the given word in the subtree.

        Recursively traverses the trie following the characters of the word,
        returning the node if found, or None if the word path does not exist.

        Parameters
        ----------
        word : str
            The word to search for. Must have at least one character.

        Returns
        -------
        TrieNode or None
            The node corresponding to the word if found, None otherwise.
        """
        if len(word) == 1:
            return self.children.get(word)
        char = word[0]
        if char not in self.children:
            return None
        return self.children[char].search(word[1:])

    def asdict(self):
        """
        Convert the subtree rooted at this node to a nested dictionary.

        Recursively converts all children and their subtrees into a nested
        dictionary structure that represents the tree topology.

        Returns
        -------
        dict
            A nested dictionary where keys are characters and values are
            dictionaries representing child subtrees. Leaf nodes return
            empty dictionaries.
        """
        return {k: v.asdict() for k, v in self.children.items()}

    def get_key(self):
        """
        Reconstruct the full key path from the root to this node.

        Recursively traverses up the parent chain, concatenating all prefix
        characters to form the complete key that leads to this node.

        Returns
        -------
        str
            The complete key string from the root to this node. Returns
            empty string if this is the root node.
        """
        if self.parent is None:
            return ""
        return self.parent.get_key() + self.prefix
