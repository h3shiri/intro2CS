import copy
import ship_helper
############################################################
# Helper class
############################################################

# Direction class used for moving the ships around hte board
class Direction:
    """
    Class representing a direction in 2D world.
    You may not change the name of any of the constants (UP, DOWN, LEFT, RIGHT,
     NOT_MOVING, VERTICAL, HORIZONTAL, ALL_DIRECTIONS), but all other
     implementations are for you to carry out.
    """
    # Magic numbers for the directions
    STEP = 1
    OPPOSITE = -1
    STABLE = 0

    UP = (STABLE, OPPOSITE)
    DOWN = (STABLE, STEP)
    LEFT = (OPPOSITE, STABLE)
    RIGHT = (STEP, STABLE)

    NOT_MOVING = "stranded"

    VERTICAL = (UP, DOWN)
    HORIZONTAL = (LEFT, RIGHT)

    ALL_DIRECTIONS = (UP, DOWN, LEFT, RIGHT)

############################################################
# Class definition
############################################################


class Ship:
    """
    A class representing a ship in Battleship game.
    A ship is 1-dimensional object that could be laid in either horizontal or
    vertical alignment. A ship sails on its vertical\horizontal axis back and
    forth until reaching the board's boarders and then changes its direction to
    the opposite (left <--> right, up <--> down).
    If a ship is hit in one of its coordinates, it ceases its movement in all
    future turns.
    A ship that had all her coordinates hit is considered terminated.
    """
    # Building a ship object
    def __init__(self, pos, length, direction, board_size):
        """
        A constructor for a Ship object
        :param pos: A tuple representing The ship's head's (x, y) position
        :param length: Ship's length
        :param direction: Initial direction in which the ship is sailing
        :param board_size: Board size in which the ship is sailing
        """
        # Position in the form (x,y), minimal coordinate in orientation
        X_VALUE = 0
        Y_VALUE = 1
        CUT = -1
        self.pos = [pos[X_VALUE],pos[Y_VALUE]]
        self.__length = length
        self.__direction = direction
        self.board_size = board_size
        #create a variable to store head/tail of the ship.
        head =[None,None]
        if direction in Direction.VERTICAL:
            head_x = pos[X_VALUE]
            head_y = (pos[Y_VALUE] + length + CUT)
            head = [head_x, head_y]
        elif direction in Direction.HORIZONTAL:
            head_x = (pos[X_VALUE] + length + CUT)
            head_y = pos[X_VALUE]
            head = [head_x, head_y]
        tail = [pos[X_VALUE],pos[Y_VALUE]]
        # Notice head and tail order
        self.__head_and_tail = [tail,head]
        # list of current damaged cells
        self.__damaged = []
        WORKING_SHIP = "moving"
        self.__functioning_state = WORKING_SHIP
        self.__locations = self.coordinates()

    def __repr__(self):
        """
        Return a string representation of the ship.
        :return: A tuple converted to string. The tuple's content should be (in
        the exact following order):
            1. A list of all the ship's coordinates.
            2. A list of all the ship's hit coordinates.
            3. Last sailing direction.
            4. The size of the board in which the ship is located.
        """
        r1 = self.__locations
        r2 = self.__damaged
        r3 = ship_helper.direction_repr_str(Direction, self.__direction)
        r4 = self.board_size
        res = (r1, r2, r3, r4)
        return str(res)

    # Assisting function to check board peripheral border
    def border(self):
        n = self.board_size
        minus = -1
        # we have a two dimensions to be in boarder vertical or horizontal
        res = []
        for i in range(n):
            res.append([minus, i])
            res.append([n, i])
            res.append([i, minus])
            res.append([i, n])
        return res

    def move(self):
        """
        Make the ship move one board unit.
        Movement is in the current sailing direction, unless such movement would
        take it outside of the board in which case the shp switches direction
        and sails one board unit in the new direction.
        the ship
        :return: A direction object representing the current movement direction.
        """
        X_axis = 0
        Y_axis = 1
        opposite = -1
        # We defined the head of the shp in this manner
        head = self.__head_and_tail[1]
        # if the ship was hit we don't change anything
        DAMAGED = "stranded"
        border = self.border()
        if self.__functioning_state == DAMAGED:
            return Direction.NOT_MOVING
        # we work on a valid direction
        else:
            potential_pos = [(self.pos[X_axis] + self.__direction[X_axis]), \
                             (self.pos[Y_axis] + self.__direction[Y_axis])]
            potential_tail = copy.copy(potential_pos)
            potential_head = [(head[X_axis] + self.__direction[X_axis]), \
                              (head[Y_axis]) + self.__direction[Y_axis]]
            if potential_head in border or potential_tail in border:
                # Swap the direction and update positions
                X_direction = (self.__direction[X_axis] * opposite)
                Y_direction = (self.__direction[Y_axis] * opposite)
                #TODO: check for issues here
                candidate = (X_direction, Y_direction)
                for direction in Direction.ALL_DIRECTIONS:
                    if candidate == direction:
                        self.__direction = direction
                self.pos = [(self.pos[X_axis] + self.__direction[X_axis]), \
                             (self.pos[Y_axis] + self.__direction[Y_axis])]
                new_tail = copy.deepcopy(self.pos)
                new_head = [(head[X_axis] + self.__direction[X_axis]), \
                              (head[Y_axis]) + self.__direction[Y_axis]]
                self.__head_and_tail = [new_tail, new_head]
                self.__locations = self.coordinates()
                return copy.deepcopy(self.__direction)
            # Otherwise we stayed in bounds
            else:
                self.pos = potential_pos
                self.__head_and_tail = [potential_tail, potential_head]
                self.__locations = self.coordinates()
                return copy.deepcopy(self.__direction)

    def hit(self, pos):
        """
        Inform the ship that a bomb hit a specific coordinate. The ship updates
         its state accordingly.
        If one of the ship's body's coordinate is hit, the ship does not move
         in future turns. If all ship's body's coordinate are hit, the ship is
         terminated and removed from the board.
        :param pos: A tuple representing the (x, y) position of the hit.
        :return: True if the bomb generated a new hit in the ship, False
         otherwise.
        """
        DAMAGED = "stranded"
        TERMINATED = "dead"
        # Check target and status in coordinate
        if pos not in self.__locations or pos in self.__damaged:
            return False
        else:
            # add a new attribute (damaged) and generating a list of damaged cells.
            self.__damaged.append(pos)
            self.__functioning_state = DAMAGED
            self.__direction = Direction.NOT_MOVING
            # if all the coordinates are hit
            if len(self.__damaged) == len(self.__locations):
                self.__functioning_state = TERMINATED
            return True

    def terminated(self):
        """
        :return: True if all ship's coordinates were hit in previous turns, False
        otherwise.
        """
        # check whether the ship status is TERMINATED
        TERMINATED = "dead"
        return (self.__functioning_state == TERMINATED)


    def __contains__(self, pos):
        """
        Check whether the ship is found in a specific coordinate.
        :param pos: A tuple representing the coordinate for check.
        :return: True if one of the ship's coordinates is found in the given
        (x, y) coordinates, False otherwise.
        """
        # check if a position is in ship coordinates.
        return (pos in self.__locations)

    def coordinates(self):
        """
        Return ship's current positions on board.
        :return: A list of (x, y) tuples representing the ship's current
        position.
        """
        res =[]
        X_VALUE = 0
        Y_VALUE = 1
        temp_pos = copy.copy(self.pos)
        starting_point = [temp_pos[X_VALUE], temp_pos[Y_VALUE]]
        # Check direction
        #TODO: watch out for code repetition here..
        if self.__direction in Direction.VERTICAL:
            current_x_value = starting_point[X_VALUE]
            for mark in range(self.__length):
                current_y_value = starting_point[Y_VALUE] + mark
                res.append((current_x_value, current_y_value))
        elif self.__direction in Direction.HORIZONTAL:
            current_y_value = starting_point[Y_VALUE]
            for mark in range(self.__length):
                current_x_value = starting_point[X_VALUE] + mark
                res.append((current_x_value, current_y_value))
        # In case the ship is not moving
        else:
            res = copy.deepcopy(self.__locations)
            #TODO: check u don't get an infinte loop here..etc
        return res

    def damaged_cells(self):
        """
        Return the ship's hit positions.
        :return: A list of tuples representing the (x, y) coordinates of the
         ship which were hit in past turns (If there are no hit coordinates,
         return an empty list). There is no importance to the order of the
         values in the returned list.
        """
        # Copying all the damaged cells list
        res = copy.deepcopy(self.__damaged)
        return res

    def direction(self):
        """
        Return the ship's current sailing direction.
        :return: One of the constants of Direction class :
         [UP, DOWN, LEFT, RIGHT] according to current
         sailing direction or NOT_MOVING if the ship is hit and not moving.
        """
        DAMAGED = "stranded"
        if self.__functioning_state == DAMAGED:
            return Direction.NOT_MOVING
        else:
            return copy.deepcopy(self.__direction)

    def cell_status(self, pos):
        """
        Return the state of the given coordinate (hit\not hit)
        :param pos: A tuple representing the coordinate to query.
        :return:
            if the given coordinate is not hit : False
            if the given coordinate is hit : True
            if the coordinate is not part of the ship's body : None 
        """
        # Check position is in ship coordinates
        if pos not in self.coordinates():
            return None
        # Whether its hit or not
        elif pos in self.damaged_cells():
            return True
        else:
            return False

#TODO: delete these tests later on
'''
ship = Ship((1,1),6,Direction.DOWN,22)
#Testiing __repr__
print(ship)
#Test cell_status and hit
print("cell status:",ship.cell_status((1,1)))
ship.hit((1,2))
print("hitting twice the same target:", ship.hit((1,2)))
print("cell status:",ship.cell_status((1,2)))
#Test termination
print("terminated the ship:",ship.terminated())
#Test contains
print("Test Contains:",(1,3) in ship)
ship.move()
print("new position:",ship.pos)
print("ship direction:", ship.direction())
'''