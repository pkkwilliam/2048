from BaseAI import BaseAI

last_move = 2
shift = False

class PlayerAI(BaseAI):
    def getMove(self, grid):
        global last_move
        global shift
        moves = grid.getAvailableMoves()
        # basic move so that bigger number at corner DONE
        if do_shift(grid) and shift == False:
            shift = True
            return 3

        if shift:
            shift = False
            return 1

        if last_move == 2:
            if 1 in moves:
                last_move = 1
                return 1
            elif 2 in moves:
                return 2
        if last_move == 1:
            if 2 in moves:
                last_move = 2
                return 2
            elif 1 in moves:
                return 1
        # basic move end
        # if down and left is not movable
        if last_move == 5:
            return get_direction(grid, moves)
        elif 3 in moves:
            last_move = 5
            return 3
        elif 4 in moves:
            last_move = 5
            return 4
        else:
            last_move = 2
            return 0


def get_direction(grid, moves):
    global last_move
    bottom_score = bottom_roll_score(grid)
    average = get_direction_average(grid)
    empty_cell = get_available_cell(grid)
    for i in range(len(average)):
        average[i] *= 2
    for i in range(len(empty_cell)):
        empty_cell[i] *= 1
    weight = [None for x in range(3)]
    for i in range(len(weight)):
        weight[i] = average[i] + empty_cell[i]
    weight[1] += bottom_score
    if weight[0] >= weight[1] and weight[0] >= weight[2]:
        last_move = 1
        return 1
    elif weight[1] > weight[0]:
        last_move = 2
        return 2
    elif 3 in moves:
        last_move = 5
        return 3

def do_shift(grid):
    grid_copy = grid.clone()
    grid_copy.move(3)
    row_four = get_row(grid_copy,3)
    row_three = get_row(grid_copy,2)
    row_two = get_row(grid_copy,1)
    row_one = get_row(grid_copy,0)

    # compare row 4 to row 3
    if row_cell(row_four) == 0:
        if row_four[1] == row_three[1]:
            return True
        elif row_four[2] == row_three[2]:
            return True
        elif row_four[3] == row_three[3]:
            return True
    else:
        return False

    # compare row 3 to row 2
    if row_cell(row_three) == 0:
        if row_three[1] == row_two[1]:
            return True
        elif row_three[2] == row_two[2]:
            return True
        elif row_three[3] == row_two[3]:
            return True
    return False

    #compare row 2 to row 1
    if row_cell(row_two) == 0:
        if row_two[1] == row_one[1]:
            return True
        elif row_two[2] == row_one[2]:
            return True
        elif row_two[3] == row_one[3]:
            return True
    return False


def row_cell(row):
    count = 0
    for i in row:
        if i == 0:
            count += 1
    return count


def get_row(grid,row):
    list = []
    for i in range(grid.size):
        list.append(grid.map[row][i])
    return list


def bottom_roll_score(grid):
    list = []
    for i in range(grid.size):
        list.append(grid.map[3][i])
    for i in list:
        if i == 0:
            return 20
        return 0


def get_average(grid, direction):
    grid_copy = grid.clone()
    grid_copy.move(direction)
    cell = 16 - len(grid_copy.getAvailableCells())
    sum = 0
    for i in range(grid_copy.size):
        for j in range(grid_copy.size):
            sum += grid_copy.map[i][j]
    return sum / cell


def get_direction_average(grid):
    down_average = get_average(grid,1)
    left_average = get_average(grid,2)
    right_average = get_average(grid,3)

    return [down_average,left_average,right_average]


def direction_available_cell(grid, direction):
    grid_copy = grid.clone()
    grid_copy.move(direction)
    return grid_copy.getAvailableCells()

def get_available_cell(grid):

    down = len(direction_available_cell(grid, 1))
    left = len(direction_available_cell(grid, 2))
    right = len(direction_available_cell(grid, 3))

    return [down,left,right]


def getList(grid):
    list = []
    for i in range(grid.size):
        for j in range(grid.size):
            list.append(j)
    return list

def checkLeftZero(grid):
    list = getList(grid)
    left = 0
    while left < 12:
        if list[left] != 0:
            return False
        left += 4
    return True

def checkRightZero(grid):
    list = getList(grid)
    right = 3
    while right < 16:
        if list[right] != 0:
            return False
        right += 4
    return True