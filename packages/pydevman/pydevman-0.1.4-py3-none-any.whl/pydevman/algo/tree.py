from __future__ import annotations

import queue
from typing import List


class TreeNode:
    def __init__(self, val=None, left=None, right=None):
        self.val = val
        self.left = left
        self.right = right


class Tree:
    def __init__(self, root: TreeNode = None) -> None:
        self.root = root

    def inorder(self, node: TreeNode, call=print):
        """
        traverse in-order
        """
        if node is None:
            return
        self.inorder(node.left) if node.left else 1
        call(node.val)
        self.inorder(node.right) if node.right else 1

    def preorder(self, node: TreeNode, call=print):
        """
        traverse pre-order
        """
        if node is None:
            return
        call(node.val)
        self.preorder(node.left) if node.left else 1
        self.preorder(node.right) if node.right else 1

    def postorder(self, node: TreeNode, call=print):
        """
        traverse post-order
        """
        if node is None:
            return
        self.postorder(node.left) if node.left else 1
        self.postorder(node.right) if node.right else 1
        call(node.val)

    def add_node(self, root, l_val, r_val):
        if root is None:
            return None, None
        l_node = None if l_val is None else TreeNode(l_val)
        r_node = None if r_val is None else TreeNode(r_val)
        root.left, root.right = l_node, r_node
        return l_node, r_node

    def add_tree(self, nums: List[int]):
        # nums = [3, 1, 5, 0, 2, 4, 6]
        i, n = 0, len(nums)
        q = queue.Queue()
        # build root node
        self.root = TreeNode(nums[0])
        self.val = nums[i]
        q.put(self.root)
        # build child root
        while i < n:
            node = q.get()
            l_val = None if 2 * i + 1 >= n else nums[2 * i + 1]
            r_val = None if 2 * i + 2 >= n else nums[2 * i + 2]
            l_node, r_node = self.add_node(node, l_val, r_val)
            q.put(l_node)
            q.put(r_node)
            i += 1
        return
