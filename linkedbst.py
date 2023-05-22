"""
File: linkedbst.py
Author: Ken Lambert
"""
from math import log
from abstractcollection import AbstractCollection
from bstnode import BSTNode
from linkedstack import LinkedStack
import random
import time
class LinkedBST(AbstractCollection):
    """An link-based binary search tree implementation."""

    def __init__(self, sourceCollection=None):
        """Sets the initial state of self, which includes the
        contents of sourceCollection, if it's present."""
        self._root = None
        AbstractCollection.__init__(self, sourceCollection)

    # Accessor methods
    def __str__(self):
        """Returns a string representation with the tree rotated
        90 degrees counterclockwise."""

        def recurse(node, level):
            sss = ""
            if node is not None:
                sss += recurse(node.right, level + 1)
                sss += "| " * level
                sss += str(node.data) + "\n"
                sss += recurse(node.left, level + 1)
            return sss

        return recurse(self._root, 0)

    def __iter__(self):
        """Supports a preorder traversal on a view of self."""
        if not self.isEmpty():
            stack = LinkedStack()
            stack.push(self._root)
            while not stack.isEmpty():
                node = stack.pop()
                yield node.data
                if node.right is not None:
                    stack.push(node.right)
                if node.left is not None:
                    stack.push(node.left)

    def preorder(self):
        """Supports a preorder traversal on a view of self."""
        return None

    def inorder(self):
        """Supports an inorder traversal on a view of self."""
        lyst = list()

        def recurse(node):
            if node != None:
                recurse(node.left)
                lyst.append(node.data)
                recurse(node.right)

        recurse(self._root)
        return iter(lyst)

    def postorder(self):
        """Supports a postorder traversal on a view of self."""
        return None

    def levelorder(self):
        """Supports a levelorder traversal on a view of self."""
        return None

    def __contains__(self, item):
        """Returns True if target is found or False otherwise."""
        return self.find(item) != None

    def find(self, item):
        """If item matches an item in self, returns the
        matched item, or None otherwise."""
        node = self._root
        while node is not None:
            if item == node.data:
                return node.data
            elif item < node.data:
                node = node.left
            else:
                node = node.right
        return None

    # Mutator methods
    def clear(self):
        """Makes self become empty."""
        self._root = None
        self._size = 0

    def add(self, item):
        """Adds item to the tree."""
        if self.isEmpty():
            self._root = BSTNode(item)
            self._size += 1
            return

        node = self._root
        while True:
            if item < node.data:
                if node.left is None:
                    node.left = BSTNode(item)
                    self._size += 1
                    return
                else:
                    node = node.left
            elif node.right is None:
                node.right = BSTNode(item)
                self._size += 1
                return
            else:
                node = node.right

    def remove(self, item):
        """Precondition: item is in self.
        Raises: KeyError if item is not in self.
        postcondition: item is removed from self."""
        if not item in self:
            raise KeyError("Item not in tree.""")

        # Helper function to adjust placement of an item
        def liftmaxinleftsubtreetotop(top):
            # Replace top's datum with the maximum datum in the left subtree
            # Pre:  top has a left child
            # Post: the maximum node in top's left subtree
            #       has been removed
            # Post: top.data = maximum value in top's left subtree
            parent = top
            current_node = top.left
            while not current_node.right is None:
                parent = current_node
                current_node = current_node.right
            top.data = current_node.data
            if parent == top:
                top.left = current_node.left
            else:
                parent.right = current_node.left

        # Begin main part of the method
        if self.isEmpty(): return None

        # Attempt to locate the node containing the item
        item_removed = None
        pre_root = BSTNode(None)
        pre_root.left = self._root
        parent = pre_root
        direction = 'L'
        current_node = self._root
        while not current_node is None:
            if current_node.data == item:
                item_removed = current_node.data
                break
            parent = current_node
            if current_node.data > item:
                direction = 'L'
                current_node = current_node.left
            else:
                direction = 'R'
                current_node = current_node.right

        # Return None if the item is absent
        if item_removed is None: return None

        # The item is present, so remove its node

        # Case 1: The node has a left and a right child
        #         Replace the node's value with the maximum value in the
        #         left subtree
        #         Delete the maximium node in the left subtree
        if not current_node.left is None \
                and not current_node.right is None:
            liftmaxinleftsubtreetotop(current_node)
        else:

            # Case 2: The node has no left child
            if current_node.left is None:
                new_child = current_node.right

                # Case 3: The node has no right child
            else:
                new_child = current_node.left

                # Case 2 & 3: Tie the parent to the new child
            if direction == 'L':
                parent.left = new_child
            else:
                parent.right = new_child

        # All cases: Reset the root (if it hasn't changed no harm done)
        #            Decrement the collection's size counter
        #            Return the item
        self._size -= 1
        if self.isEmpty():
            self._root = None
        else:
            self._root = pre_root.left
        return item_removed

    def replace(self, item, new_item):
        """
        If item is in self, replaces it with newItem and
        returns the old item, or returns None otherwise."""
        probe = self._root
        while probe is not None:
            if probe.data == item:
                old_data = probe.data
                probe.data = new_item
                return old_data
            elif probe.data > item:
                probe = probe.left
            else:
                probe = probe.right
        return None

    def height(self):
        '''
        Return the height of tree
        :return: int
        '''

        def height1(top):
            '''
            Helper function
            :param top:
            :return:
            '''
            if top.left is None and top.right is None:
                return 0
            else:
                left_h = 0
                right_h = 0
                if top.left is not None:
                    left_h = height1(top.left)
                if top.right is not None:
                    right_h = height1(top.right)
            return 1 + max(left_h, right_h)
        return height1(self._root)
    def is_balanced(self):
        '''
        Return True if tree is balanced
        :return:
        '''
        height = self.height()
        value = 2 * log((len(list(self.inorder())) + 1), 2) - 1
        if height < value:
            return True
        return False
    def range_find(self, low, high):
        '''
        Returns a list of the items in the tree, where low <= item <= high."""
        :param low:
        :param high:
        :return:
        '''
        return [item for item in self.inorder() if low <= item <= high]

    def rebalance(self):
        '''
        Rebalances the tree.
        :return:
        '''
        def rebalance1(item):
            if len(item) == 0:
                return None
            half = len(item) // 2
            node = BSTNode(item[half])
            node.right = rebalance1(item[half + 1:])
            node.left = rebalance1(item[:half])
            return node
        self._root = rebalance1(list(self.inorder()))

    def successor(self, item):
        """
        Returns the smallest item that is larger than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        return next((number for number in self.inorder() if number > item), None)

    def predecessor(self, item):
        """
        Returns the largest item that is smaller than
        item, or None if there is no such item.
        :param item:
        :type item:
        :return:
        :rtype:
        """
        return next((number for number in reversed(list(self.inorder())) if number < item), None)
    def demo_bst(self, path):
        """
        Demonstration of efficiency binary search tree for the search tasks.
        :param pa   th:
        :type path:
        :return:
        :rtype:
        """
        with open(path, 'r', encoding='utf-8') as file:
            data = []
            for line in file.readlines():
                data.append(line.strip())
                lst = data[:1000]
                random.shuffle(lst)
            start_list = time.time()
            if all(item in data for item in lst):
                print('Time with the list -', time.time() - start_list, 'seconds')
            
            binary_tree1 = LinkedBST()
            new_data = data[:1000]
            for item in new_data:
                binary_tree1.add(item)
            start_binary1 = time.time()
            for item in lst:
                binary_tree1.find(item)
            print('Time with binary tree -', time.time() - start_binary1, 'seconds')
            
            binary_tree2 = LinkedBST()
            random.shuffle(data)
            new_data = data[:1000]
            for item in new_data:
                binary_tree2.add(item)
            start_binary2 = time.time()
            for item in lst:
                binary_tree2.find(item)
            print('Time with binary tree (random) -', time.time() - start_binary2, 'seconds')
            
            binary_tree2.rebalance()
            new_data = data[:10000]
            for item in new_data:
                binary_tree2.add(item)
            start_rebalance =  time.time()
            for item in lst:
                binary_tree2.find(item)
            print('Time with rebalanced tree -', time.time() - start_rebalance, 'seconds')
            