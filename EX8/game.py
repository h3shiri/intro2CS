############################################################
# Imports
############################################################
import game_helper as gh
import copy
############################################################
# Class definition
############################################################


class Game:
    """
    A class representing a battleship game.
    A game is composed of ships that are moving on a square board and a user
    which tries to guess the locations of the ships by guessing their
    coordinates.
    """

    def __init__(self, board_size, ships):
        """
        Initialize a new Game object.
        :param board_size: Length of the side of the game-board
        :param ships: A list of ships that participate in the game.
        :return: A new Game object.
        """
        # Set working attributes for game..
        self.__board_size = board_size
        self.__ships_array = ships
        self.__bomb_dictionary = {}
        RUNNING = True
        self.__game_status = RUNNING

    # Play one round of the game according to specifications.
    def __play_one_round(self):
        """
        Note - this function is here to guide you and it is *not mandatory*
        to implement it. The logic defined by this function must be implemented
        but if you wish to do so in another function (or some other functions)
        it is ok.

        Te function runs one round of the game :
            1. Get user coordinate choice for bombing.
            2. Move all game's ships.
            3. Update all ships and bombs.
            4. Report to the user the result of current round (number of hits and
             terminated ships)
        :return:
            (some constant you may want implement which represents) Game status :
            GAME_STATUS_ONGOING if there are still ships on the board or
            GAME_STATUS_ENDED otherwise.
        """
        # Place a new bomb
        status = self.__game_status
        target = gh.get_target(self.__board_size)
        NEW = 4
        TURN = 1
        EXPIRED = 0
        # Move the ships
        self.__bomb_dictionary[target] = NEW
        for ship in self.__ships_array:
            ship.move()
        # Update hits and bomb array, ship array accordingly
        hits = []
        tot_num_of_hits = 0
        bombs_to_be_removed = []
        for bomb in self.__bomb_dictionary:
            ZERO_HITS = 0
            HIT = 1
            bomb_hit_counter = ZERO_HITS
            for ship in self.__ships_array:
                if ship.hit(bomb):
                    bomb_hit_counter += HIT
                    hits.append(copy.copy(bomb))
                    tot_num_of_hits += HIT
            self.__bomb_dictionary[bomb] -= TURN
            if bomb_hit_counter > ZERO_HITS or self.__bomb_dictionary[bomb] == EXPIRED:
                bombs_to_be_removed.append(bomb)
        for bomb in bombs_to_be_removed:
            del self.__bomb_dictionary[bomb]

        # Update damaged ships and working ships lists
        hit_ships = []
        ships_locai =[]
        ships = copy.deepcopy(self.__ships_array)
        for ship in self.__ships_array:
            if len(ship.damaged_cells()) > ZERO_HITS:
                hit_ships.extend(ship.damaged_cells())
            for cell in ship.coordinates():
                if not ship.cell_status(cell):
                    ships_locai.append(cell)

        # Print the board with al the parameters
        print(gh.board_to_string(self.__board_size, hits, self.__bomb_dictionary, hit_ships, ships_locai))
        # Remove terminated ships
        num_terminations = 0
        STEP = 1
        for ship in self.__ships_array:
            if ship.terminated():
                self.__ships_array.remove(ship)
                num_terminations += STEP
        gh.report_turn(tot_num_of_hits, num_terminations)
        ZERO_SHIPS = 0
        if len(self.__ships_array) == ZERO_SHIPS:
            ENDED = False
            status = ENDED
        return status



    def __repr__(self):
        """
        Return a string representation of the board's game
        :return: A tuple converted to string. The tuple should contain (maintain
        the following order):
            1. Board's size.
            2. A dictionary of the bombs found on the board
                 {(pos_x, pos_y) : remaining turns}
                For example :
                 {(0, 1) : 2, (3, 2) : 1}
            3. A list of the ships found on the board (each ship should be
                represented by its __repr__ string).
        """
        # Set arguments in tuple which shall be converted to string
        r1 = str(self.__board_size)
        r2 = str(copy.deepcopy(self.__bomb_dictionary))
        #TODO: watchout for r3 here
        r3 = str([print(ship) for ship in self.__ships_array])
        result = str(r1, r2, r3)
        return result

    def play(self):
        """
        The main driver of the Game. Manages the game until completion.
        completion.
        :return: None
        """
        # Print legend
        gh.report_legend()
        # Initial board print, notice we have no bombs or hits yet so we insert 0.
        ZERO = 0
        EMPTY_HITS = []
        NO_BOMBS = {}
        NO_DAMAGED_SHIPS = []
        ships_locations = []
        for ship in self.__ships_array:
            ships_locations.extend((ship.coordinates()))
        print(gh.board_to_string(self.__board_size, EMPTY_HITS, NO_BOMBS, NO_DAMAGED_SHIPS, ships_locations))
        # Play until all ships are eliminated
        play = self.__game_status
        while play:
            play = self.__play_one_round()
        gh.report_gameover()

'''
############################################################
# An example usage of the game
############################################################
if __name__=="__main__":
    game = Game(5, gh.initialize_ship_list(4, 2))
    game.play()
'''
