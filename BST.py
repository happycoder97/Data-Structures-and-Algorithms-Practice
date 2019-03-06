import unittest
import random


class Node:
    def __init__(self, value, parent=None, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right
        self.parent = parent


class BST:
    def __init__(self):
        self.root = None

    def insert(self, x):
        par = None
        cur = self.root
        while cur != None:
            par = cur
            if x >= cur.value:
                cur = cur.right
            else:
                cur = cur.left

        if par is None:
            self.root = Node(x)
        else:
            if x >= par.value:
                par.right = Node(x, par)
            else:
                par.left = Node(x, par)

    def change_parent_linkage(self, node, new_node):
        if node is self.root:
            self.root = new_node
            new_node.parent = None
        else:
            if node.parent.left is node:
                node.parent.left = new_node
            else:
                node.parent.right = new_node

    def delete(self, x):
        elem = self.find(x)
        if elem is None:
            return

        if elem.left is None:
            self.change_parent_linkage(elem, elem.right)
        elif elem.right is None:
            self.change_parent_linkage(elem, elem.left)
        else:
            successor = self.subtree_min(elem.right)
            self.change_parent_linkage(successor, successor.right)
            self.change_parent_linkage(elem, successor)
            successor.left = elem.left
            successor.right = elem.right

    def find(self, x):
        cur = self.root

        # Invariant: cur is None or cur is a child of root

        while cur is not None and cur.value != x:
            if x > cur.value:
                cur = cur.right
            else:
                cur = cur.left

        # Termination: cur is None or cur.value = x

        # Inv && Term =>
        #   cur is None or (cur is a child of root && cur.value = x)

        return cur

    def subtree_min(self, node):
        cur = node
        # Invariant:
        # all nodes in (node, cur] are left child of their parents
        while cur.left is not None:
            cur = cur.left

        return cur

    def subtree_max(self, node):
        cur = node
        # Invariant:
        # all nodes in (node, cur] are right child of their parents
        while cur.right is not None:
            cur = cur.right
        return cur

    def successor(self, x):
        elem = self.find(x)
        if elem is None:
            return None

        if elem.right is not None:
            return self.subtree_min(elem.right)
        else:
            cur = elem
            while cur.parent is not None and cur.parent.right is cur:
                cur = cur.parent
            return cur.parent

    def predecessor(self, x):
        elem = self.find(x)
        if elem is None:
            return None

        if elem.left is not None:
            return self.subtree_max(elem.left)
        else:
            cur = elem
            while cur.parent is not None and cur.parent.left is cur:
                cur = cur.parent
            return cur.parent

    def inorder(self):
        ret = []

        def inorder_rec(node, arr):
            if node is None:
                return

            inorder_rec(node.left, arr)
            arr += [node.value]
            inorder_rec(node.right, arr)

        inorder_rec(self.root, ret)
        return ret

class BSTTest(unittest.TestCase):
    def setUp(self):
        self.bst = BST()

    def get_distinct_rands(self):
        rands = []
        for i in range(10):
            x = int(random.uniform(0, 100))
            while x in rands:
                x = int(random.uniform(0, 100))
            rands += [x]
        return rands

    def test_insert(self):
        rands = self.get_distinct_rands()
        for r in rands:
            self.bst.insert(r)

        rands.sort()
        self.assertEqual(self.bst.inorder(), rands)

    def test_delete(self):
        rands = self.get_distinct_rands()
        for r in rands:
            self.bst.insert(r)

        self.bst.delete(rands[0])
        rands = rands[1:]
        rands.sort()

        self.assertEqual(self.bst.inorder(), rands)

    def test_successor(self):
        rands = self.get_distinct_rands()
        for r in rands:
            self.bst.insert(r)

        rands.sort()

        m = rands[len(rands) // 2]
        s = rands[(len(rands) // 2) + 1]
        self.assertIsNotNone(self.bst.successor(m))
        self.assertEqual(self.bst.successor(m).value, s)

        m = rands[0]
        s = rands[1]
        self.assertIsNotNone(self.bst.successor(m))
        self.assertEqual(self.bst.successor(m).value, s)

        m = rands[len(rands) - 1]
        self.assertIsNone(self.bst.successor(m))

    def test_predecessor(self):
        rands = self.get_distinct_rands()
        for r in rands:
            self.bst.insert(r)

        rands.sort()

        m = rands[len(rands) // 2]
        p = rands[(len(rands) // 2) - 1]
        self.assertIsNotNone(self.bst.predecessor(m))
        self.assertEqual(self.bst.predecessor(m).value, p)

        m = rands[len(rands)-1]
        p = rands[len(rands)-2]
        self.assertIsNotNone(self.bst.predecessor(m))
        self.assertEqual(self.bst.predecessor(m).value, p)

        m = rands[0]
        self.assertIsNone(self.bst.predecessor(m))

if __name__ == "__main__":
    unittest.main(verbosity=2)
