from screen import Screen
import sys
import math
from torpedo import Torpedo
from ship import Ship
from asteroid import Asteroid
# Magic numbers
DEFAULT_ASTEROIDS_NUM = 5
SHIP_CRUSH_MESSAGE = "Your ship has smashed into an Asteroid!"
CRUSH_TITLE = "Ship_Crush"
MAX_NOF_TORPEDOS = 15
REMOVED_ALL_AST = "You have cleaned our galaxy from asteroids!"
NO_MORE_LIFE = "Your ship has been completely destroyed, you have failed this city!"
USED_THE_ESCAPE_BUTTON = "Good luck in the next round"
ENDGAME_TITLE = "The game has ended"

class GameRunner:
    def __init__(self, asteroids_amnt=3):
        self.__asteroid_array =[]
        self._screen = Screen()
        self.__score = 0
        self.__torpedo_array = []

        for i in range(asteroids_amnt):
            self.__asteroid_array.append(Asteroid())
            ast = self.__asteroid_array[i]
            self._screen.register_asteroid(ast, ast.size())
        self.screen_max_x = Screen.SCREEN_MAX_X
        self.screen_max_y = Screen.SCREEN_MAX_Y
        self.screen_min_x = Screen.SCREEN_MIN_X
        self.screen_min_y = Screen.SCREEN_MIN_Y
        self.ship = Ship()

    def run(self):
        self._do_loop()
        self._screen.start_screen()

    def _do_loop(self):
        # You don't need to change this method!
        self._game_loop()

        # Set the timer to go off again
        self._screen.update()
        self._screen.ontimer(self._do_loop,5)

    # Check for a collision
    def check_for_asteroid_ship_collision(self, ship, asteroid_array):
        for ast in asteroid_array:
            if ast.get_intersection(ship):
                    HIT = -1
                    ship.life += HIT
                    self._screen.remove_life()
                    self._screen.unregister_asteroid(ast)
                    self.__asteroid_array.remove(ast)
                    self._screen.show_message(CRUSH_TITLE, SHIP_CRUSH_MESSAGE)


    def _game_loop(self):
        ship = self.ship
        # Print the ship
        self._screen.draw_ship(ship.coordinate_X(), ship.coordinate_Y(), ship.heading())
        for ast in self.__asteroid_array:
            self._screen.draw_asteroid(ast, ast.coordinate_X(), ast.coordinate_Y())
            ast.move()
        self.check_for_asteroid_ship_collision(ship, self.__asteroid_array)
        for torpedo in self.__torpedo_array:
            if torpedo.update_age():
                self._screen.unregister_torpedo(torpedo)
                self.__torpedo_array.remove(torpedo)
                continue
            self._screen.draw_torpedo(torpedo, torpedo.coordinate_X(), torpedo.coordinate_Y(), torpedo.heading())
            torpedo.move()
        self.check_for_torpedo_hit()
        #TODO: check when excactly should u move the ship..
        ship.move()

        # Select user input
        if self._screen.is_right_pressed():
            ship.spin_right()
        elif self._screen.is_left_pressed():
            ship.spin_left()
        elif self._screen.is_up_pressed():
            ship.accelerate()
        # makes ship shoot torpedo
        elif self._screen.is_space_pressed():
            self.shoot_torpedo()
        elif self._screen.should_end():
            self._screen.show_message(ENDGAME_TITLE, USED_THE_ESCAPE_BUTTON)
            self._screen.end_game()
            quit()
        else:
            self.finish()


    def shoot_torpedo(self):
        if len(self.__torpedo_array) >= MAX_NOF_TORPEDOS:
            return
        ship = self.ship
        torpedo = Torpedo(ship.coordinate_X(), ship.coordinate_Y(),ship.X_speed(), ship.Y_speed(), ship.heading())
        self.__torpedo_array.append(torpedo)
        self._screen.register_torpedo(torpedo)

    def check_for_torpedo_hit(self):
        for torp in self.__torpedo_array:
            for ast in self.__asteroid_array:
                if ast.get_intersection(torp):
                    self.__score += ast.get_score_for_hit()
                    self._screen.set_score(self.__score)
                    #if torpedo intersect with an asteroid, remove it from the list and unregister
                    self._screen.unregister_torpedo(torp)
                    self.__torpedo_array.remove(torp)
                    self._screen.unregister_asteroid(ast)
                    self.__asteroid_array.remove(ast)
                    old_size = ast.size()
                    old_ast_x_speed = ast.speed_X()
                    old_ast_y_speed = ast.speed_Y()
                    old_torp_x_speed = torp.speed_X()
                    old_torp_y_speed = torp.speed_Y()
                    if (old_size > 1):
                        new_size = old_size - 1
                        new_x_speed = (old_torp_x_speed + old_ast_x_speed) / math.sqrt(pow(old_ast_x_speed, 2) + pow(old_ast_y_speed, 2))
                        new_y_speed = (old_torp_y_speed + old_ast_y_speed) / math.sqrt(pow(old_ast_x_speed, 2) + pow(old_ast_y_speed, 2))
                        for i in range(2):
                            new_ast = Asteroid(new_size, ast.coordinate_X(), ast.coordinate_Y(), new_x_speed, new_y_speed)
                            self._screen.register_asteroid(new_ast, new_size)
                            self.__asteroid_array.append(new_ast)
                            #mult by -1 for second astroid
                            new_x_speed *= -1
                            new_y_speed *= -1

    # finish the game by removing all the asteroids
    def finish(self):
        if len(self.__asteroid_array) == 0:
            self._screen.show_message(ENDGAME_TITLE, REMOVED_ALL_AST)
            self._screen.end_game()
            quit()

        elif self.ship.life == 0:
            self._screen.show_message(ENDGAME_TITLE, NO_MORE_LIFE)
            self._screen.end_game()
            quit()




def main(amnt):
    runner = GameRunner(amnt)
    runner.run()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        main(int(sys.argv[1]))
    else:
        main(DEFAULT_ASTEROIDS_NUM)
