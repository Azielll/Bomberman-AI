import heapq
import time
import math
import random
from .base import BombermanAlgorithm

class QLearningAlgorithm(BombermanAlgorithm):

    def __init__(self, depth=3):
        super().__init__("Qlearning")
        self.depth = depth

        ### These variables are for moving the agent ###
        # x - this is the current x position of the agent
        self.x = 0
        # y - this is the current y position of the agent
        self.y = 0
        # dx - this is the target change in x position for the agent
        self.dx = 0
        # dy - this is the target change in y position for the agent
        self.dy = 0
        # place_bomb - this is to determine if the character will place a bomb or move
        self.place_bomb = False
        # bomb_placed - this is used to track if the character has placed a bomb so that 
        #               they will not try to place another when they cannot
        self.bomb_placed = False
        # bomb_x - this tracks the x position of a bomb that has been placed
        self.bomb_x = 0
        # bomb_y - this tracks the y position of a bomb that has been placed
        self.bomb_y = 0
        # bomb_ticks - this is used to track how long a bomb has before it explodes
        self.bomb_ticks = -1
        # exity_pos - this is used to track the location of the exit
        self.exity_pos = (0, 0)

        ### These variables are for calculating Q ###
        # exit_w - this is the weight for the distance to the exit
        self.exit_w = 4
        # mon_w - this is the weight for the distance to the closest monster
        self.mon_w = -1
        # bomb_w - this is the weight for the closest explosion
        self.bomb_w = -2

        self.old_Q = 0.0
        self.epsilon = 0.99

        # These values are used for training Bomberman
        self.training = True
        self.training_pos_x = self.x
        self.training_pos_y = self.y
        self.exp_pos_x = self.x + self.dx
        self.exp_pos_y = self.x + self.dy

    

    def get_action(self, wrld, character):
        self.find_exit(wrld)

        # make a clone of the world and agent
        worldy = wrld.from_world(wrld)
        bomberman = worldy.me(character)

        if (self.bomb_placed):
            print("Checking Bomb")
            print("Danger! Bomb at: (", self.bomb_x, ", ", self.bomb_y, ")")
            self.check_boom(wrld)

        print("----------Weights----------")
        print(" - Exit Weight: ", self.exit_w)
        print(" - Mon Weight: ", self.mon_w)
        print(" - Bomb Weight: ", self.bomb_w)
        print("--------------------------")
        self.dx = 0
        self.dy = 0

        # calculate the prediction
        best_Q = -math.inf
        print("Current Q Value: ", best_Q)
        print("Calculating Q Values")
        for posy_x in [-1, 0, 1]:
            for posy_y in [-1, 0, 1]:
                # if not ((posy_x == 0) and (posy_y == 0)):
                if ((0 <= bomberman.x + posy_x < worldy.width()) and (0 <= bomberman.y + posy_y < worldy.height())):
                    if ((not (worldy.wall_at((bomberman.x + posy_x), (bomberman.y + posy_y)))) and 
                        (not (worldy.explosion_at((bomberman.x + posy_x), (bomberman.y + posy_y)))) and
                        (not (worldy.next()[0].explosion_at((bomberman.x + posy_x), (bomberman.y + posy_y))))):
                        new_worldy = wrld.from_world(worldy)
                        bomber_jr = new_worldy.me(bomberman)
                        bomber_jr.move(posy_x, posy_y)
                        new_worldy = new_worldy.next()[0]
                        bomber_jr = new_worldy.me(bomberman)
                        Q_jr = self.calc_Q(new_worldy, bomber_jr)
                        print("   - Q Value for (", posy_x, ", ", posy_y, "): ", Q_jr)
                        # If Bomberman finds the exit, he will choose it over all other spots
                        if (bomberman.x + posy_x == self.exity_pos[0]) and (bomberman.y + posy_y == self.exity_pos[1]):
                            self.dx = posy_x
                            self.dy = posy_y
                            best_Q = Q_jr
                            print("EXIT FOUND!!!")
                            break
                        elif (Q_jr > best_Q):
                            best_Q = Q_jr
                            self.dx = posy_x
                            self.dy = posy_y

        # if Bomberman is in the process of training, he will use greedy epsilon
        if (self.training and (random.random() < self.epsilon)):
            self.dx = random.randint(-1, 1)
            self.dy = random.randint(-1, 1)
            print("Epsilon: ", self.epsilon, "     Making a Random Move!")

        print("Exit Distance: ", self.get_exit_distance(wrld, character))
        print("Monster Distance: ", self.get_closest_mon_distance(wrld, character))
        print("Moving to (", self.dx, ", ", self.dy, ")")
        self.old_Q = best_Q

        self.x = bomberman.x
        self.y = bomberman.y

        self.exp_pos_x = bomberman.x + self.dx
        self.exp_pos_y = bomberman.y + self.dy

        print("Exit at: (", self.exity_pos[0], ", ", self.exity_pos[1], ")")
        print("Expected Position: (", self.exp_pos_x, ", ", self.exp_pos_y, ")")

        # if there is no path to the goal, have Bomberman place a bomb instead of move
        # TODO: The logic here can definitely be improved on
        if ((self.place_bomb) and (not (self.bomb_placed))):
            self.dx = -999
            self.dy = -999
            self.place_bomb = False
            self.bomb_placed = True
            self.bomb_ticks = -1
            self.bomb_x = bomberman.x
            self.bomb_y = bomberman.y
            print("No Path to Goal! Placing Bomb at: (", self.x, ", ", self.y, ")")
            self.exp_pos_x = bomberman.x
            self.exp_pos_y = bomberman.y
        
        # return the target move for Bomberman
        # [Placing a bomb is represented by (-999, -999)]
        return (self.dx, self.dy)
    
    # calc_Q
    # This function is run to calculate the Q value for a possible move
    def calc_Q(self, wrld, character):
        # start by making a clone of the world and agent
        worldy = wrld.from_world(wrld)
        bomberman = worldy.me(character)

        exit_val = self.exit_w * (1 / (1 + self.get_exit_distance(worldy, bomberman)))
        mon_val = self.mon_w * (1 / (1 + self.get_closest_mon_distance(worldy, bomberman)))
        boom_val = self.bomb_w * (1 / (1 + self.get_closest_explosion_distance(worldy, bomberman)))

        Q = exit_val + mon_val + boom_val

        return Q
    
    # calc_reward 
    # This function is run to calculate the reward Bomberman will get for a given move
    def calc_reward(self, wrld, character):
        # start by making a clone of the world and agent
        worldy = wrld.from_world(wrld)
        bomberman = worldy.me(character)
        reward = 0

        # check the events in the world
        if (len(worldy.events) > 0):
            for event in worldy.events:
                if ((3 == event.tpe) or
                    (2 == event.tpe)):
                    reward = reward + -100.0
                elif (4 == event.tpe):
                    reward = reward + 100.0
                # elif (0 == event.tpe):
                #     reward = reward + 1.0
                # elif (1 == event.tpe):
                #     reward = reward + 5.0

        # check to see if the agent moved
        if not (bomberman == None):
            if not ((bomberman.x == self.x) and (bomberman.y == self.y)):
                reward = reward + 0.11  

        return reward
    
    # update_w
    # This function will update the weights for the exit, the monster distance, and
    # the bomb distance
    def update_w(self, wrld, character):
        # start by making a clone of the world and agent
        worldy = wrld.from_world(wrld)

        gamma = 0.9
        alpha = 0.5
        delta = (self.calc_reward(wrld, character) + (gamma * self.old_Q)) - self.calc_Q(wrld, character)
        self.exit_w = self.exit_w + (alpha * delta * (1 / (1 + self.get_exit_distance(wrld, character))))
        self.mon_w = self.mon_w + (alpha * delta * (1 / (1 + self.get_closest_mon_distance(wrld, character))))
        self.bomb_w = self.bomb_w + (alpha * delta * (1 / (1 + self.get_closest_explosion_distance(wrld, character))))

        # To prevent Bomberman from drifting towards bad behaviors, I chose to 
        # bound the weights. This was mainly do to the bomb implementation. I think
        # having it so that Bomberman tracks when bombs will explode would help to 
        # replace this. 
        self.exit_w = max(100, min(0, self.exit_w))
        self.mon_w = max(-100, min(0, self.mon_w))
        self.bomb_w = max(-100, min(0, self.bomb_w))

    # check_boom
    # This function will check to see if the bomb previously placed by 
    # Bomberman has exploded yet.
    def check_boom(self, wrld):
        worldy = wrld.from_world(wrld)
        if (worldy.explosion_at(self.bomb_x, self.bomb_y)):
            print(" - Bomb at (", self.bomb_x, ", ", self.bomb_y, ") Exploded!")
            # If the bomb exploded, allow Bomberman to place another bomb
            self.bomb_placed = False
        # ↓This↓ was for me experimenting with tracking explosion times...
        # elif (self.bomb_placed):
        #     print(" - Checking time to Explosion")
        #     worldy = wrld.from_world(worldy)
        #     self.bomb_ticks = -1
        #     while(not (worldy.explosion_at(self.bomb_x, self.bomb_y))):
        #         self.bomb_ticks = self.bomb_ticks + 1
        #         worldy = worldy.next()[0]
        #     print(" - Turns to Boom: ", self.bomb_ticks)
                        
    # find_exit
    # This function is run initially to determine the location of the 
    # exit. This location is then stored as a global variable for the
    # rest of the game. 
    def find_exit(self, wrld):
        for posy_x in range(0, wrld.width()):
            for posy_y in range(0, wrld.height()):
                if wrld.exit_at(posy_x, posy_y):
                    self.exity_pos = (posy_x, posy_y)
                    return (posy_x, posy_y)

    # get_exit_distance
    # This function will calculate the Manhattan distance
    # from the agent's current position to the position of
    # the exit
    def get_exit_distance(self, wrld, character):
        # start by making a clone of the world and agent
        worldy = wrld.from_world(wrld)
        bomberman = worldy.me(character)

        if (bomberman == None): 
            # calculate the distance to the exit
            exity_dist_man = math.sqrt(((self.exity_pos[0] - self.training_pos_x)**2) + ((self.exity_pos[1] - self.training_pos_y)**2))
            exity_dist = len(self.a_star(wrld, (self.exp_pos_x), (self.exp_pos_y)))
        else: 
            # calculate the distance to the exit
            exity_dist_man = math.sqrt(((self.exity_pos[0] - character.x)**2) + ((self.exity_pos[1] - character.y)**2))
            exity_dist = len(self.a_star(wrld, character.x, character.y))
        
        # return the distance to the exit
        if ((exity_dist == 0) and (exity_dist_man > 0)):
            self.place_bomb = True
            # If there is no path to the goal, then Bomberman will instead consider
            # the Manhattan distance to the goal. This should keep him from getting 
            # stuck (^ ̳• ·̫ • ̳^)
            exity_dist = exity_dist_man

        return exity_dist
    
    # get_closest_mon_distance
    # This function will calculate the Manhattan distance
    # from the agent's current position to the position of 
    # the closest monster
    def get_closest_mon_distance(self, wrld, character):
        # start by making a clone of the world and agent
        worldy = wrld.from_world(wrld)
        bomberman = worldy.me(character)

        # set the initial mon_dist
        # for this, I chose to set it to the maximum distance in the world to start
        mon_dist = 3.5
        # iterate through each of the monsters and calculate the distance between
        # them and the agent. Keep the shortest distance!
        for key in worldy.monsters:
            for mon in wrld.monsters[key]:
                if (bomberman == None):
                    dist = 0
                else:
                    dist = math.sqrt(((bomberman.x - mon.x)**2) + ((bomberman.y - mon.y)**2))
                # if the new distance is smaller, keep that one!
                if (dist < mon_dist):
                    mon_dist = dist
        
        # return the distance to the closest monster
        # Bound the monster distance so that Bomberman is less scares 
        if (mon_dist > 3.5):
            mon_dist = 3.5
        return mon_dist
    
    # get_closest_explosion_distance
    # This function will calculate the Manhattan distance
    # from the agent's current position to the position of
    # the closest explosion square
    def get_closest_explosion_distance(self, wrld, character):
        # start by making a clone of the world and agent
        worldy = wrld.from_world(wrld)
        bomberman = worldy.me(character)

        # determine the boom distance
        if (self.bomb_placed):
            if (bomberman == None):
                boom_dist = 0
            else:
                # find the minimum difference between Bomberman and the bomb's x or y position
                if (bomberman.x == self.bomb_x) or (bomberman.y == self.bomb_y):
                    boom_dist = 0
                else: 
                    boom_dist = math.sqrt((worldy.width()**2) + (worldy.height()**2))
                    # boom_dist = abs(min((bomberman.x - self.bomb_x), (bomberman.y - self.bomb_y)))

        else:
            boom_dist = math.sqrt((worldy.width()**2) + (worldy.height()**2))

        print("Boom Distance: ", boom_dist)

        return boom_dist
    
    def initial_learning(self, wrld, character):
        # start by making a clone of the world and agent
        win_count = 0
        steps = 0

        # get the weights from the txt file
        self.load_weights()

        while (steps < 1000):
            worldy = wrld.from_world(wrld)
            bomberman = worldy.me(character)
            self.x = bomberman.x
            self.y = bomberman.y
            self.bomb_placed = False
            self.bomb_ticks = -1
            self.bomb_x = 0
            self.bomb_y = 0
            self.epsilon =self.epsilon / 1.01

            while not (bomberman == None):
                self.get_action(worldy, bomberman)
                if ((self.dx == -999) and (self.dy == -999)):
                    bomberman.place_bomb()
                else:
                    bomberman.move(self.dx, self.dy)
                    
                worldy = worldy.next()[0]
                bomberman = worldy.me(character)

                steps = steps + 1

                # update the weights
                self.update_w(worldy, bomberman)

                print("-----Weights Updated!-----")
                print(" - New Exit Weight: ", self.exit_w)
                print(" - New Mon Weight: ", self.mon_w)
                print(" - New Bomb Weight: ", self.bomb_w)
                print("--------------------------")

                if not (bomberman == None):
                    self.training_pos_x = bomberman.x
                    self.training_pos_y = bomberman.y

        self.training = False
        self.bomb_placed = False

        self.save_weights()


    def save_weights(self, filename = "bomberweights.txt"):
        with open(filename, "w") as my_weights:
            my_weights.write(f"{self.exit_w}, {self.mon_w}, {self.bomb_w}\n")

    def load_weights(self, filename = "bomberweights.txt"):
        try:
            with open(filename, "r") as my_weights:
                line = my_weights.readline()
                exit_w, mon_w, bomb_w = map(float, line.strip().split(","))
                self.exit_w = exit_w
                self.mon_w = mon_w
                self.bomb_w = bomb_w
        except FileNotFoundError:
            print("I could not find my weights. Using default values.")
            

    ######################################################
    ##### A* Functions ###################################
    ######################################################
    def a_star_move(self, wrld):
        pathy = self.a_star(wrld, self.x, self.y)

        if len(pathy) == 0:
            self.dx = 0
            self.dy = 0

        nexty_pos = pathy[0]
        self.dx = nexty_pos[0] - self.x
        self.dy = nexty_pos[1] - self.y


    def a_star(self, wrld, start_x, start_y):
        self.find_exit(wrld)

        open_set = []
        heapq.heappush(open_set, (0, (start_x, start_y)))

        fromy_spot = {}
        spoty_score = {(start_x, start_y): 0}

        while open_set:
            _, current_spot = heapq.heappop(open_set)

            if (current_spot == tuple(self.exity_pos)):
                goaly_path = []
                while current_spot in fromy_spot:
                    goaly_path.append(current_spot)
                    current_spot = fromy_spot[current_spot]
                
                goaly_path.reverse()
                return goaly_path
                
            for posy_x in [-1, 0, 1]:
                for posy_y in [-1, 0, 1]:
                    if (posy_x == 0) and (posy_y ==0):
                        continue
                    
                    neighbor_spot = ((current_spot[0] + posy_x), (current_spot[1] + posy_y))
                    if ((neighbor_spot[0] >= 0) and (neighbor_spot[0] < wrld.width()) and
                        (neighbor_spot[1] >= 0) and (neighbor_spot[1] < wrld.height()) and
                        not (wrld.wall_at(neighbor_spot[0], neighbor_spot[1]))):

                        starty_score =  spoty_score[current_spot] + 1

                        if ((neighbor_spot not in spoty_score) or (starty_score < spoty_score[neighbor_spot])):
                            fromy_spot[neighbor_spot] = current_spot
                            spoty_score[neighbor_spot] = starty_score

                            total_score = starty_score + abs(neighbor_spot[0] - self.exity_pos[0]) + abs(neighbor_spot[1] - self.exity_pos[1])
                            heapq.heappush(open_set, (total_score, neighbor_spot))

        return []
