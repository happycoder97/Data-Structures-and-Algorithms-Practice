import unittest
import random


class Node:
    def __init__(self, value, parent=None, left=None, right=None):
        self.value = value
        self.left = left
        self.right = right
        self.parent = parent
        self.height = 0


class AVL:
    def __init__(self):
        self.root = None

    def get_root(self):
        return self.root

    def insert(self, x):
        pass

    def delete(self, x):
        pass

    def successor(self, x):
        pass

    def predecessor(self, x):
        pass

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


class AVLTest(unittest.TestCase):
    def setUp(self):
        self.avl = AVL()

    def get_distinct_rands(self):
        rands = []
        for i in range(10):
            x = int(random.uniform(0, 100))
            while x in rands:
                x = int(random.uniform(0, 100))
            rands += [x]
        return rands

    def verify_avl(self, root):
        if root is None:
            return

        l_height = 0 if root.left is None else root.left.height
        r_height = 0 if root.right is None else root.right.height
        self.assertEqual(root.height, max(l_height, r_height)+1)
        self.assertLessEqual(abs(l_height-r_height), 1)

        self.verify_avl(root.left)
        self.verify_avl(root.right)

    def verify_bst(self, root):
        if root is None:
            return
        
        if root.left is not None:
            self.assertLess(root.left.value, root.value)
            self.verify_bst(root.left)

        if root.right is not None:
            self.assertGreater(root.right.value, root.value)
            self.verify_bst(root.right)
        

    def test_insert(self):
        rands = self.get_distinct_rands()
        for r in rands:
            self.avl.insert(r)

        rands.sort()
        self.assertEqual(self.avl.inorder(), rands)
        self.verify_bst(self.avl.get_root())
        self.verify_avl(self.avl.get_root())

    def test_delete(self):
        rands = self.get_distinct_rands()
        for r in rands:
            self.avl.insert(r)

        self.avl.delete(rands[0])
        rands = rands[1:]
        rands.sort()

        self.assertEqual(self.avl.inorder(), rands)
        self.verify_bst(self.avl.get_root())
        self.verify_avl(self.avl.get_root())

    def test_successor(self):
        rands = self.get_distinct_rands()
        for r in rands:
            self.avl.insert(r)

        rands.sort()

        m = rands[len(rands) // 2]
        s = rands[(len(rands) // 2) + 1]
        self.assertIsNotNone(self.avl.successor(m))
        self.assertEqual(self.avl.successor(m).value, s)

        m = rands[0]
        s = rands[1]
        self.assertIsNotNone(self.avl.successor(m))
        self.assertEqual(self.avl.successor(m).value, s)

        m = rands[len(rands) - 1]
        self.assertIsNone(self.avl.successor(m))

    def test_predecessor(self):
        rands = self.get_distinct_rands()
        for r in rands:
            self.avl.insert(r)

        rands.sort()

        m = rands[len(rands) // 2]
        p = rands[(len(rands) // 2) - 1]
        self.assertIsNotNone(self.avl.predecessor(m))
        self.assertEqual(self.avl.predecessor(m).value, p)

        m = rands[len(rands) - 1]
        p = rands[len(rands) - 2]
        self.assertIsNotNone(self.avl.predecessor(m))
        self.assertEqual(self.avl.predecessor(m).value, p)

        m = rands[0]
        self.assertIsNone(self.avl.predecessor(m))


if __name__ == "__main__":
    unittest.main(verbosity=2)
