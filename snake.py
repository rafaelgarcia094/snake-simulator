import random

NORTH, EAST, SOUTH, WEST = 0, 1, 2, 3


class SnakeGame:
    """
        Python implementation of the classic snake game
    """
    def __init__(self, board_size=30, snake_length=4):
        self.board_size = board_size
        self.snake_pos = self._reset_snake(snake_length)
        self.food_pos = self._generate_food()
        self.snake_dir = WEST
        self.points = 0

    def _reset_snake(self, snake_length):
        """
        Reset the game with the snake in the middle of the board with initial length

        :param snake_length: the snake's initial length
        :return: a list with each position occupied by the snake's body
        """
        pos_x, pos_y = self.board_size // 2, self.board_size // 2
        return [(x, pos_y) for x in range(pos_x, pos_x + snake_length)]

    def _generate_food(self):
        """
        Selects an empty cell to receive the food.

        :return: a randomly chosen cell
        """
        all_positions = {(x, y) for x in range(self.board_size) for y in range(self.board_size)}
        valid_positions = all_positions - set(self.snake_pos)
        return random.choice(list(valid_positions))

    def move_snake(self, action):
        """
        Moves the snake in one of the four cardinal directions.

        :param action: which direction the snake is moving to
        :return: how many points the snake has (equals to the number of times it ate the food)
                 -1 if the game is over
        """
        if abs(self.snake_dir - action) == 2:  # Snake cannot go backwards, game over
            return -1

        head_pos = self._update_head_pos(action)

        if head_pos in self.snake_pos[:-1]:  # Snake hit itself, game over
            return -1

        self.snake_pos.insert(0, head_pos)

        if head_pos == self.food_pos:  # if the food was eaten, generates a new one and updates number of points
            self.food_pos = self._generate_food()
            self.points += 1
        else:  # Only delete the tail when food wasn't eaten
            del self.snake_pos[-1]

        return self.points

    def _update_head_pos(self, action):
        """
        Generates the snake's head position after the action is performed.

        :param action: a movement in one of four cardinal directions
        :return: the new head position
        """
        self.snake_dir = action

        x, y = self.snake_pos[0]

        if action == NORTH:
            y = (y - 1) % self.board_size
        if action == EAST:
            x = (x + 1) % self.board_size
        if action == SOUTH:
            y = (y + 1) % self.board_size
        if action == WEST:
            x = (x - 1) % self.board_size

        return x, y

    def generate_board(self):
        """
        Generates the board in a list of list

        :return: a board with empty spaces represented as '.', snake body as 'X'. and food as '0'
        """
        board = [['.' for _ in range(self.board_size)] for _ in range(self.board_size)]
        board[self.food_pos[1]][self.food_pos[0]] = '0'

        for x, y in self.snake_pos:
            board[y][x] = 'X'

        return board


def print_board(board):
    for row in board:
        print(''.join(row))

    print('----')


if __name__ == "__main__":
    game = SnakeGame(board_size=10)
    points = 0

    while points != -1:
        print('Points:', points)
        print_board(game.generate_board())

        chosen_action = int(input())
        points = game.move_snake(chosen_action)
