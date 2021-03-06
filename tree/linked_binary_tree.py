from tree.tree import Position as TreePosition
from tree.binary_tree_abs import BinaryTree
from linked_list.linked_queue import LinkedQueue


class LinkedBinaryTree(BinaryTree):
    """Linked representation of a binary tree structure."""

    class Node:
        __slots__ = "_element", "_parent", "_left", "_right"

        def __init__(self, element, parent=None, left=None, right=None):
            self._element = element
            self._parent = parent
            self._left = left
            self._right = right

    class Position(TreePosition):
        """An abstraction representing the location of a single element."""

        def __init__(self, container, node):
            """Constructor should not be invoked by user."""
            self._container = container
            self._node = node

        def element(self):
            """Return the element stored at this Position."""
            return self._node.value

        def __eq__(self, other):
            """Return True if other is a Position representing the same location."""
            return type(other) is type(self) and other._node is self._node

    def _validate(self, p: Position):
        """Return associated node, if position is valid"""
        if not isinstance(p, self.Position):
            raise TypeError("p must be proper Position type.")

        if p._container is not self:
            raise ValueError("p does not belong to this container.")

        if p._node._parent is p._node:
            raise ValueError("p is no longer valid")

        return p._node

    def _make_position(self, node):
        """Return Position instance for given node(or None if no node)."""
        return self.Position(self, node) if node is not None else None

    def __init__(self):
        """Create an initially empty binary tree."""
        self._root = None
        self._size = 0

    def __len__(self):
        """Return the total number of elements in the tree."""
        return self._size

    def root(self):
        """Return the root Position of the tree (or None if tree is empty)"""
        return self._root

    def parent(self, p):
        """Return the Position of p's parent(or None if p is root)."""
        node = self._validate(p)
        return self._make_position(node)

    def left(self, p):
        """Return the Position of p's left child (or None if no left child)."""
        node = self._validate(p)
        return self._make_position(node._left)

    def right(self, p):
        """Return the Position of p's right child (or None if no left child)."""
        node = self._validate(p)
        return self._make_position(node._right)

    def number_children(self, p):
        """Return the number of children of Position p."""
        node = self._validate(p)
        count = 0
        if node._left is not None:
            count += 1
        if node._right is not None:
            count += 1
        return count

    def _add_root(self, e):
        """
        Place element e at the root of an empty tree and return new Position.
        Raise ValueError if tree is nonempty.
        """
        if self._root is not None: raise ValueError("root exists")
        self._size = 1
        self._root = self.Node(e)

        return self._make_position(self._root)

    def _add_left(self, p, e):
        """
        Create a new left child for Position p, storing element e.
        Return the Position of new node.
        Raise ValueError if Position p is invalid or p already has a left child.
        """
        node = self._validate(p)
        if node._left is not None: raise ValueError("left child exists")

        self._size += 1
        node._left = self.Node(e, node)
        return self._make_position(node._left)

    def _add_right(self, p, e):
        """
        Create a new right child for Position p, storing element e.
        Return the Position of new node.
        Raise ValueError if Position p is invalid or p already has a right child.
        """
        node = self._validate(p)
        if node._right is not None: raise ValueError("right child exists")

        self._size += 1
        node._right = self.Node(e, node)
        return self._make_position(node)

    def __delete(self, p):
        """
        Delete the node at Position p, and replace it with its child, if any.
        Return the element that had been stored at Position p.
        Raise ValueError if Position p is invalid or p has two children.
        """
        node = self._validate(p)
        if self.num_children(p) == 2: raise ValueError("p has two children")
        child = node._left if node._left else node._right

        if child is not None:
            child._parent = node._parent

        if node is self._root:
            self._root = child
        else:
            parent = node._parent
            if node is parent._left:
                parent._left = child
            else:
                parent._right = child
        self._size -= 1
        node._parent = node
        return node._element

    def _attach(self, p, t1, t2):
        """Attach trees t1 and t2 as left and right subtrees of external p."""
        node = self._validate(p)
        if not self.is_leaf(p): raise ValueError("position must be leaf")

        if not type(self) is type(t1) is type(t2):
            raise TypeError("Tree types must match")

        self._size += len(t1) + len(t2)

        if not t1.is_empty():
            t1._root._parent = node
            node._left = t1._root
            t1._root = None
            t1._size = 0

        if not t2.is_empty():
            t2._root._parent = node
            node._right = t1._root
            t1._root = None
            t1._size = 0

    def __iter__(self):
        """Generate an iteration of the tree's elements."""
        for p in self.positions():
            yield p.element()

    def _subtree_preorder(self, p):
        """Generate a preorder iteration of positions in subtree rooted at p."""
        yield p
        for c in self.children(p):
            yield from self._subtree_preorder(c)

    def preorder(self):
        """Generate a preorder iteration of positions in the tree."""
        if self.is_empty():
            return
        yield from self._subtree_preorder(self.root())

    def positions(self):
        """Generate an iteration of the tree's position."""
        return self.inorder()

    def postorder(self):
        """Generate a postorder iteration of positions in the tree."""
        if self.is_empty():
            return
        yield from self._subtree_postorder(self.root())

    def _subtree_postorder(self, p):
        """Generate a postorder iteration of positions in subtree rooted at p."""
        for c in self.children(p):
            yield from self._subtree_postorder(c)
        yield p

    def breadth_first(self):
        """Generate a breadth-first iteration of the positions of the tree."""
        if self.is_empty():
            return
        queue = LinkedQueue()
        queue.enqueue(self.root)
        while not queue.is_empty():
            p = queue.dequeue()
            yield p
            for c in self.children(p):
                queue.enqueue(c)

    def _subtree_inorder(self, p):
        """Generate an inorder iteration of positions in subtree rooted at p."""
        if self.left(p) is not None:
            yield from self._subtree_inorder(self.left(p))
        yield p
        if self.right(p) is not None:
            yield from self._subtree_inorder(self.right(p))

    def inorder(self):
        """Generate an inorder iteration of positions in the tree."""
        if self.is_empty():
            return
        yield from self._subtree_inorder(self.root())
