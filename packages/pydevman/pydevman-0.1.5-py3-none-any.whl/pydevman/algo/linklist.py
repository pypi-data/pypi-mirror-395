from __future__ import annotations

from typing import Optional


class ListNode:
    def __init__(
        self, val: object = None, next_node: Optional[ListNode] = None
    ) -> None:
        self.val = val
        self.next_node = next_node


class LinkList:
    def __init__(self) -> None:
        """
        create linklist with head
        """
        # 哨兵节点
        self.head = self.tail = ListNode(None)

    def traverse_linklist(self, call=print) -> None:
        """
        traverse link list
        """
        node = self.head
        while node:
            call(node.val)
            node = node.next_node

    @staticmethod
    def build_from_list(nums: list[object]) -> None:
        """
        build linklist with list
        """
        ll = LinkList()
        if nums is None:
            return ll

        for idx, item in enumerate(nums):
            node = ListNode(item, None)
            if idx == 0:
                ll.head.next_node = node
            ll.tail = node
