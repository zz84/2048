import numpy as np
import random
import sys,tty
import time
import os

class Game2048:
    def __init__(self):
        self.board = np.array([[0 for _ in range(4)] for _ in range(4)])
        self.score = 0
        self.turn = 0
        self.terminate = False
        self.input = {
            ord('w'):'UP',
            ord('a'):'LEFT',
            ord('s'):'DOWN',
            ord('d'):'RIGHT'
        }

    def print_board(self):
        os.system('clear')
        print("turn: {}         score: {}".format(
            self.turn,
            self.score
        ))
        for i in range(len(self.board)):
            line = ''
            for j in range(len(self.board[i])):
                line += self.print_num(self.board[i][j])
                # line += str(self.board[i][j]).center(6)
            print(line)
        return

    def print_num(self, num):
        if num == 0:
            return '\033[1;30;47m' + ''.center(6)
        elif num == 2:
            return '\033[1;30;103m' + str(num).center(6)
        elif num == 4:
            return '\033[1;30;101m' + str(num).center(6)
        elif num == 8:
            return '\033[1;97;41m' + str(num).center(6)
        elif num == 16:
            return '\033[1;97;45m' + str(num).center(6)
        elif num == 32:
            return '\033[1;97;44m' + str(num).center(6)
        elif num == 64:
            return '\033[1;30;103m' + str(num).center(6)
        elif num == 128:
            return '\033[1;30;101m' + str(num).center(6)
        elif num == 2:
            return '\033[1;97;41m' + str(num).center(6)
        elif num == 2:
            return '\033[1;97;45m' + str(num).center(6)
        elif num == 2:
            return '\033[1;97;44m' + str(num).center(6)
        else:
            return '\033[1;30;47m' + str(num).center(6)

    def step(self, action):
        """
        :param action: 'LEFT', 'RIGHT', 'UP', 'DOWN'
        :returns: the resulting board
        """
        board = self.board.copy()
        if action == 'LEFT':
            for i in range(len(board)):
                board[i] = self.merge_left_up(board[i])
        elif action == 'RIGHT':
            for i in range(len(board)):
                board[i] = self.merge_right_down(board[i])
        elif action == 'UP':
            for i in range(len(board[0])):
                board[:,i] = self.merge_left_up(board[:,i])
        elif action == 'DOWN':
            for i in range(len(board[0])):
                board[:,i] = self.merge_right_down(board[:,i])
        return board

    def generate_numbers(self):
        numbers = [(2,2), (4,2)][random.randint(0,1)]
        empty = self.empty_squares()
        assert len(empty) > 0
        if len(empty) == 1:
            self.board[empty[0]] = numbers[0]
            self.score += numbers[0]
            return
        spots = random.sample(range(len(empty)), 2)
        spots = list(map(lambda x : empty[x], spots))
        self.board[spots[0]] = numbers[0]
        self.board[spots[1]] = numbers[1]
        self.score += sum(numbers)
        return

    def empty_squares(self):
        res = []
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                if self.board[i][j] == 0:
                    res.append((i,j))
        return res

    def check_terminate(self):
        """
        :returns: True if board have less than 2 empty squares and
        """
        if len(self.empty_squares()) >= 1:
            return False

        for action in ['UP', 'DOWN', 'LEFT', 'RIGHT']:
            if self.is_valid(action):
                return False
        return True

    def detect_action(self):
        tty.setcbreak(sys.stdin)
        key = ord(sys.stdin.read(1))
        while not key in self.input:
            key = ord(sys.stdin.read(1))
        # sys.exit(0)
        return self.input[key]

    def is_valid(self, action):
        return not (self.step(action) == self.board).all()

    def run(self):
        while not self.terminate:
            self.generate_numbers()
            self.turn += 1
            self.print_board()
            self.terminate = self.check_terminate()
            if self.terminate:
                break
            action = self.detect_action()
            while not self.is_valid(action):
                action = self.detect_action()
            self.board = self.step(action)
            self.print_board()
            time.sleep(0.3)
        print("Game over! score is {}!".format(self.score))
        return

    def combine(self, arr):
        for i in range(len(arr) - 1):
            if arr[i] != 0:
                next = i+1
                while next < len(arr) - 1 and arr[next] == 0:
                    next += 1
                if int(arr[i]) == int(arr[next]):
                    arr[i], arr[next] = 2*arr[i], 0
        return arr

    def merge_left_up(self, row):
        row = self.combine(row)
        values = list(filter(lambda x : int(x) != 0, row))
        return values + [0 for _ in range(len(row) - len(values))]

    def merge_right_down(self, row):
        row = self.combine(row[::-1])
        values = list(filter(lambda x : int(x) != 0, row))
        return [0 for _ in range(len(row) - len(values))] + values[::-1]

if __name__ == '__main__':
    game = Game2048()
    game.run()
