"""
Radix tree (also known as a compressed trie or compact prefix tree) implementation.

This module provides a RadixTree data structure that stores key-value pairs efficiently
by compressing common prefixes. Unlike a standard trie, a radix tree compresses nodes
that have only one child, reducing memory usage while maintaining fast prefix-based
lookups and insertions.
"""

_sentinel = object()


class RadixTree:
    """
    A radix tree data structure for key-value pairs storage with compressed prefixes.

    The RadixTree compresses common prefixes among keys, making it more memory-efficient
    than a standard trie while maintaining fast insertion and lookup operations.
    The entries can be a list of strings or a list of (key, value) tuples.

    Attributes
    ----------
    root : RadixNode
        The root node of the radix tree.
    """

    def __init__(self, entries=()):
        """
        Initialize a RadixTree with a collection of strings or key-value pairs.

        Parameters
        ----------
        entries : iterable
            An iterable of strings or (key, value) tuples to insert into the tree.
            Each key must be a non-empty string.

        """
        self.root = RadixNode()
        self.root.is_root = True
        for entry in entries:
            if isinstance(entry, str):
                self.insert(entry)
            else:
                self.insert(*entry)

    def insert(self, key, value=None):
        """
        Insert a key-value pair into the radix tree.

        If the key already exists, its value will be updated. The tree structure
        is automatically compressed to share common prefixes among keys.

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

    def completions(self, key):
        """
        Return possible completions for the given key.

        Parameters
        ----------
        key : str
            The key to search for.

        Returns
        -------
        list
            A list of possible completions for the given key.
        """
        return self.root.completions(key)

    def asdict(self):
        """
        Convert the radix tree to a nested dictionary representation.

        Returns
        -------
        dict
            A nested dictionary where each key is a prefix and the value
            is either another dictionary (for nodes with children) or None.
            Note: This representation does not preserve the values stored
            in leaf nodes, only the tree structure.
        """
        return self.root.asdict()

    @classmethod
    def from_dict(cls, node_dict):
        """
        Create a radix tree from a nested dictionary.
        """
        instance = cls()
        root = instance.root
        # Create and attach all initially empty children nodes to root
        root.children = {k: RadixNode(k, parent=root) for k in node_dict}
        # push the children nodes and what they should contain to the stack
        stack = [(node, node_dict[prefix]) for prefix, node in root.children.items()]
        while stack:
            # 'node' will be expanded with subtree
            node, subtree = stack.pop()
            # Create and attach all initially empty children nodes to the node
            node.children = {k: RadixNode(k, parent=node) for k in subtree}
            # push the children nodes and what they should contain to the stack
            stack.extend([(v, subtree[k]) for k, v in node.children.items()])
        return instance

    @property
    def height(self):
        """
        Height of the radix tree.
        """
        # Subtract 1 to exclude the root node
        return self.root.height - 1

    @property
    def size(self):
        """
        Size of the radix tree.
        """
        return self.root.size

    @property
    def total_chars(self):
        """
        Total number of characters stored in all prefixes of the radix tree.

        This represents the compressed size of the tree. Compare this to the
        sum of len(key) for all keys to calculate the compression rate.
        """
        return self.root.total_chars

    def __getitem__(self, key):
        return self.root[key]

    def get(self, key, default=None):
        try:
            return self[key]
        except KeyError:
            return default

    def __contains__(self, key):
        return self.root._search_node(key) is not None

    def __setitem__(self, key, value):
        return self.insert(key, value)

    def pop(self, key, default=_sentinel):
        try:
            return self.root.pop(key)
        except KeyError:
            if default is not _sentinel:
                return default
            raise KeyError(key)


class RadixNode:
    """
    A node in the radix tree data structure.

    Each node stores a prefix (shared part of keys), an optional value,
    references to child nodes, and a reference to its parent node.

    Attributes
    ----------
    children : dict
        Dictionary mapping prefix strings to child RadixNode instances.
    value
        The value stored at this node (None if this is not a leaf node).
    parent : RadixNode, optional
        Reference to the parent node (None for root).
    prefix : str
        The prefix string associated with this node.
    """

    def __init__(self, prefix="", value=None, parent=None):
        """
        Initialize a RadixNode.

        Parameters
        ----------
        value : any, optional
            The value to store at this node. Defaults to None.
        prefix : str, optional
            The prefix string for this node. Defaults to empty string.
        parent : RadixNode, optional
            The parent node. Defaults to None.
        """
        self.children = {}
        self.prefix = prefix
        if value is not None:
            self.value = value
        self.parent = parent
        self.is_root = False

    def insert(self, key, value=None):
        """
        Insert a key-value pair into the subtree rooted at this node.

        This method handles the radix tree compression logic:
        - If no common prefix exists with existing children, creates a new child
        - If the key exactly matches an existing prefix, updates that child's value
        - If the key shares a prefix with an existing child, recursively inserts
        - If the key partially matches a child's prefix, splits the node to preserve
          the tree structure while maintaining compression

        Parameters
        ----------
        key : str
            The key to insert. Must be non-empty.
        value
            The value to associate with the key.
        """
        # Look for a node to insert the key into
        common_prefix, existing_prefix, existing_child = self._find_common_prefix_child(
            key
        )

        # Case 1: No common prefix found - create a new child node
        if existing_child is None:
            self.children[key] = RadixNode(key, value, parent=self)
            return

        # Case 2: Exact match - key matches an existing child's prefix exactly
        if common_prefix == existing_prefix == key:
            if value is not None:
                existing_child.value = value
            return

        # Case 3: Key extends beyond the common prefix - recursively insert given key
        if common_prefix == existing_prefix:
            # if this is a leaf node, preserve the prefix with an empty string
            if len(existing_child.children) == 0:
                existing_child.insert("")
            remaining_key = key[len(common_prefix) :]
            existing_child.insert(remaining_key, value)
            return

        # Case 4: Key and existing child share a prefix but diverge - split the node
        # Create an intermediate node to hold the common prefix
        intermediate_node = RadixNode(common_prefix, parent=self)
        self.children[common_prefix] = intermediate_node

        # Move the existing child under the intermediate node with its remaining prefix
        remaining_existing_prefix = existing_prefix[len(common_prefix) :]
        intermediate_node.children[remaining_existing_prefix] = existing_child
        existing_child.prefix = remaining_existing_prefix
        existing_child.parent = intermediate_node

        # Create a new child for the key under the intermediate node
        remaining_key = key[len(common_prefix) :]
        intermediate_node.children[remaining_key] = RadixNode(
            remaining_key, value, parent=intermediate_node
        )

        # Remove the old reference to the existing child under its original prefix
        del self.children[existing_prefix]

    def completions(self, key):
        """
        Return possible completions for the given key.

        Parameters
        ----------
        key : str
            The key to search for completions.

        Returns
        -------
        set
            A set of possible completions for the given key.
        """

        query = key
        common_prefix, existing_prefix, node = self._find_common_prefix_child(query)
        if node is None:
            return set()

        while node is not None:
            # Update search prefix to remove the common_prefix found
            query = query[len(common_prefix) :]
            # Save the last node that is not None
            last_node = node
            common_prefix, existing_prefix, node = node._find_common_prefix_child(query)
        # If the key is shorter than this node's key, complete until reaching
        # the node's key
        if len(key) < len(last_node.key):
            return {last_node.key}
        # When at exactly this node's key, complete with the children's keys
        return set(nd.key for nd in last_node.children.values())

    @property
    def value(self):
        """
        The value stored at this node, if any.
        """
        return getattr(self, "_value", None)

    @value.setter
    def value(self, value):
        """
        Set the value stored at this node.
        """
        self._value = value

    @property
    def siblings(self):
        """
        All the siblings, including the child.
        """
        return self.parent.children

    def _find_common_prefix_child(self, key):
        """
        Find the first child node that shares a common prefix with the given key.

        Iterates through all children to find the first one that has a non-empty
        common prefix with the input key.

        Parameters
        ----------
        key : str
            The key to search for a common prefix.

        Returns
        -------
        tuple
            A tuple (common_prefix, existing_prefix, child) where:
            - common_prefix (str): The longest common prefix between key
              and the first found child
            - existing_prefix (str): The prefix of the first found child
            - child (RadixNode): The child node, or None if no common prefix exists
            Returns ("", "", None) if no child shares a common prefix with key.
        """
        for existing_prefix, child in self.children.items():
            common_prefix = self._common_longest_prefix(key, existing_prefix)
            if len(common_prefix) > 0:
                return common_prefix, existing_prefix, child
        return "", "", None

    def _common_longest_prefix(self, key1, key2):
        """
        Find the longest common prefix between two strings.

        Compares the two strings character by character and returns the longest
        prefix that both strings share from the beginning.

        Parameters
        ----------
        key1 : str
            The first string.
        key2 : str
            The second string.

        Returns
        -------
        str
            The longest common prefix of key1 and key2. Returns empty string
            if no common prefix exists, or the shorter of the two strings if
            one is a prefix of the other.
        """
        min_length = min(len(key1), len(key2))
        for i in range(min_length):
            if key1[i] != key2[i]:
                return key1[:i]
        return key1[:min_length]

    def asdict(self):
        """
        Convert the subtree rooted at this node to a nested dictionary.

        Recursively converts all children and their subtrees into a nested
        dictionary structure that represents the tree topology.

        Returns
        -------
        dict
            A nested dictionary where keys are prefixes and values are
            dictionaries representing child subtrees. Leaf nodes return
            empty dictionaries.
        """
        return {k: v.asdict() for k, v in self.children.items()}

    @property
    def height(self):
        """
        Height of the subtree rooted at this node.
        """
        if self.children == {}:
            return 1
        return 1 + max(v.height for v in self.children.values())

    @property
    def key(self):
        """
        Full key string from the root to this node.
        """
        if self.parent is None:
            return self.prefix
        return self.parent.key + self.prefix

    @property
    def size(self):
        """
        Number of nodes in the subtree rooted at this node, including this node.
        """
        return 1 + sum(child.size for child in self.children.values())

    @property
    def total_chars(self):
        """
        Total number of characters in all prefixes in the subtree rooted at this node.

        This includes the prefix of this node plus all prefixes in its subtree.
        """
        return len(self.prefix) + sum(
            child.total_chars for child in self.children.values()
        )

    def _search_node(self, key):
        search_node = self
        search_key = key
        while search_node:
            common_prefix, node_prefix, next_node = (
                search_node._find_common_prefix_child(search_key)
            )
            node = search_node  # Save the current node
            # update the search key by dropping the common prefix
            search_key = search_key[len(common_prefix) :]
            search_node = next_node

        if key != node.key:
            return None
        if "" in node.children:
            return node.children[""]
        if len(node.children) != 0:
            return None
        return node

    def __getitem__(self, key):
        node = self._search_node(key)
        if node is None:
            raise KeyError
        return node.value

    def pop(self, key):
        node = self._search_node(key)
        if node is None:
            raise KeyError
        parent = node.parent

        # Delete the key
        del parent.children[node.prefix]

        # The root node is special in that it doesn't need to be updated
        if parent.is_root:
            return node.value

        # If there is a single child, merge with parent
        if len(parent.children) == 1:
            single_child = next(iter(parent.children.values()))

            # Update grandparent's parent key and the parent's prefix
            del parent.parent.children[parent.prefix]
            parent.prefix = f"{parent.prefix}{single_child.prefix}"
            parent.parent.children[parent.prefix] = parent

            # Update value if there is one
            if single_child.value is not None:
                parent.value = single_child.value

            # Finally, delete the single child
            del parent.children[single_child.prefix]
        return node.value
