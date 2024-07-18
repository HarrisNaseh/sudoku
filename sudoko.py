class sudoko_solver:
    def __init__(self, board):
        self.board = board
    
    def _get_row_start(self, index):
        if index < 3:
            return 0
        if index < 6:
            return 3
        return 6
    
    def _get_col_start(self, index):
        if index % 3 == 0:
            return 0
        if index % 3 == 1:
            return 1
        return 2

    def _valid(self,Box, row, col, num):
        #check if num is in the box
        if num in Box[row]:
            return False
        
        return self._check_row(Box, row, col, num) and self._check_col(Box, row, col, num)
    

    def _check_row(self, Box, row, col, num):

        col = self._get_row_start(col)
        #it is on the left side of board
        if row % 3 == 0:
            for i in range(1,3):
                for x in range(0, 3):
                    if Box[row + i][col+x] == num:
                        return False
        #if it is on the right side of board
        elif row % 3 == 2:
            for i in range(1,3):
                for x in range(0, 3):
                    if Box[row - i][col+x] == num:
                        return False
        else:           
        #The postion is in the middle of the board
            for x in range(0, 3):
                if Box[row + 1][col+x] == num or Box[row - 1][col+x] == num:
                    return False 

        return True 

    def _check_col(self, Box, row, col, num):

        col = self._get_col_start(col)

        #if box is in the top of the board
        if row < 3:
            for i in range(3,7,3):
                for x in range(0,7,3):
                    if Box[row + i][col + x] == num:
                        return False
        elif row < 6: # If box is in middle
            for x in range(0, 7, 3):
                if Box[row + 3][col + x] == num or Box[row - 3][col + x] == num:
                    return False
                
        else:
            for i in range(3,7,3):
                for x in range(0,7,3):
                    if Box[row - i][col + x] == num:
                        return False
        return True
        
        
    def _get_least_conflicts(self, board):
        dic = dict()
        for row in range(9):
            for col in range(9):
                if board[row][col] == 0:
                    dic[(row, col)] = list()
                    for num in range(1, 10):
                        if self._valid(board, row, col, num):
                            dic[(row, col)].append(num)
        
        return dic


    def _solve(self, board):
        dic = self._get_least_conflicts(board)

        if not dic:
            return True
        
        sorted_d_as_list = sorted(dic.items(), key=lambda item: len(item[1]))

        key, value = sorted_d_as_list[0]
        row, col = key

        for val in value:
            board[row][col] = val
            if self._solve(board):
                return True
            board[row][col] = 0
            
        return False
    
    def solve(self):
        self._solve(self.board)
    
    def print_board(self) -> str:
        output = ""
        for x in range(0, 9, 3):
            for y in range(0, 9, 3):
                output += "|| "
                for i in range(3):
                    for u in range(3):
                        if self.board[x + i][u + y]:
                            output += str(self.board[x + i][u+y])+ " | "
                        else:
                            output += "  | "
                    str_list = list(output)
                    str_list[len(output) - 1] = "| "
                    # output+= "| "
                    output = "".join(str_list)
                if y != 6: output += "\n" + "-" *41+ " \n"
            output += "\n"+ "=" *41+ "\n"
        return output

# board = [
#     [0, 0, 5, 0, 0, 9, 0, 0, 0],
#     [0, 9, 0, 0, 0, 1, 0, 0, 3],
#     [7, 0, 0, 0, 6, 5, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 2, 0, 4],
#     [0, 0, 0, 7, 6, 9, 0, 0, 0],
#     [3, 0, 8, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 7, 2, 0, 0, 0, 8],
#     [8, 0, 0, 4, 0, 0, 0, 3, 0],
#     [0, 0, 0, 8, 0, 0, 5, 0, 0]
# ]

# board = [
#     [1, 2, 0, 0, 3, 0, 0, 9, 0],
#     [6, 0, 0, 0, 0, 0, 8, 0, 0],
#     [0, 5, 3, 0, 0, 0, 0, 7, 0],
#     [0, 0, 0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 7, 0, 4],
#     [0, 9, 0, 2, 0, 1, 0, 8, 0],
#     [5, 0, 0, 8, 0, 0, 0, 0, 0],
#     [3, 0, 0, 0, 0, 6, 0, 5, 0],
#     [0, 0, 6, 0, 0, 7, 4, 2, 0]
# ]






