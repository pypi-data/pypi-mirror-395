"""
create_time: 2022-09
author: Jacky Lee
description: 并查集
"""


class UnionFind:
    def __init__(self, n: int):
        self.uf = list(range(n + 1))
        self.rank = [1] * (n + 1)  # 规模

    def find(self, x: int) -> int:
        r = x
        if self.uf[x] != x:
            x = self.uf[x]
        # 路径压缩
        while r != x:
            self.uf[r], r = x, self.uf[r]
        return x

    def union(self, x: int, y: int) -> None:
        fx, fy = self.find(x), self.find(y)
        if fx == fy:
            return
        # 小规模往大规模合并
        if self.rank[fx] < self.rank[fy]:
            fx, fy = fy, fx
        self.rank[fx] += self.rank[fy]
        self.uf[fy] = fx

    def is_connected(self, x: int, y: int) -> bool:
        return self.find(x) == self.find(y)
