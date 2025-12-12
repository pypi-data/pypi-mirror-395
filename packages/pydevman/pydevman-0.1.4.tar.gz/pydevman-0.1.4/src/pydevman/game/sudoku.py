"""
create_time: 2022-04
author: Jacky Lee
description: 数独解密
"""


class Sudoku:
    def __init__(self, units: list[list[int]]) -> None:
        """
        units(9,9)
        """
        self.flag = False
        self.units = units

    def _validation(self, row: int, col: int, num: int) -> bool:
        """
        validation the value.
        """
        if self.units[row][col]:
            return False
        block_row = row // 3 * 3
        block_col = col // 3 * 3
        for unit in self.units:
            for j in range(9):
                if self.units[row][j] == num or unit[col] == num:
                    return False
        for i in range(block_row, block_row + 3):
            for j in range(block_col, block_col + 3):
                if self.units[i][j] == num:
                    return False
        return True

    def draw(self):
        """
        draw sudoku.
        """
        for row in self.units:
            print(row)

    def dfs(self, row: int, col: int):
        """
        deep first search
        """
        if row == 9:
            self.flag = True
            return
        elif self.units[row][col] > 0:
            self.dfs(row + (col + 1) // 9, (col + 1) % 9)
        for i in range(1, 10):
            if not self._validation(row, col, i):
                continue
            self.units[row][col] = i
            self.dfs(row + (col + 1) // 9, (col + 1) % 9)
            if self.flag:
                return
            self.units[row][col] = 0


def test_sudoku():
    """
    test sample
    """
    units = [
        [0, 0, 0, 8, 0, 0, 0, 0, 9],
        [0, 1, 9, 0, 0, 5, 8, 3, 0],
        [0, 4, 3, 0, 1, 0, 0, 0, 7],
        [4, 0, 0, 1, 5, 0, 0, 0, 3],
        [0, 0, 2, 7, 0, 4, 0, 1, 0],
        [0, 8, 0, 0, 9, 0, 6, 0, 0],
        [0, 7, 0, 0, 0, 6, 3, 0, 0],
        [0, 3, 0, 0, 7, 0, 0, 8, 0],
        [9, 0, 4, 5, 0, 0, 0, 0, 1],
    ]
    sudoku = Sudoku(units)
    sudoku.dfs(0, 0)
    sudoku.draw()


if __name__ == "__main__":
    test_sudoku()
