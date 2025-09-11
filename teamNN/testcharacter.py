# This is necessary to find the main code
import sys
import time
import math
import heapq
sys.path.insert(0, '../bomberman')
# Import necessary stuff
from entity import CharacterEntity
from colorama import Fore, Back

class TestCharacter(CharacterEntity):

    # Initial state!
    # (I want to add more states in the future...)
    state = "goal"
    search_depth = 7

    action = "move"

    exitie = ()
    initial_x = 0
    initial_y = 0

    num_steps = 0

    dx = 0
    dy = 0

    def do(self, wrld):
        # Your code here
        self.mon_checker(wrld.from_world(wrld))

        if (self.state == "goal"):
            self.a_star_move(wrld.from_world(wrld))
        elif (self.state == "mon dodge"):
            self.expectimax_search(wrld.from_world(wrld), self.search_depth)

        if (self.action == "move"):
            self.move(self.dx, self.dy)
            print("dx: ", self.dx, ", dy: ", self.dy)

        self.num_steps = self.num_steps + 1

        if (self.state == "mon dodge"):
            time.sleep(2.5)
        else:
            time.sleep(0.1)


    # Find the exit!
    # (This is mainly used for calculating the utility)
    def find_exit(self, wrld):
        self.initial_x = self.y
        self.initial_y = self.x
        for posy_x in range(0, wrld.width()):
            for posy_y in range(0, wrld.height()):
                if wrld.exit_at(posy_x, posy_y):
                    self.exitie = (posy_x, posy_y)

    def mon_checker(self, wrld):
         for key in wrld.monsters:
            for mon in wrld.monsters[key]:
                mon_dist = math.sqrt((((mon.x) - wrld.me(self).x)**2) + (((mon.y) - wrld.me(self).y)**2))
                if (mon_dist <= 5):
                    self.state = "mon dodge"
                else:
                    self.state = "goal"


######################################################
##### Expectimax Functions ###########################
######################################################

    def expectimax_search(self, wrld, depth):
        self.action = "move"
        self.find_exit(wrld)

        # Keep track of the best score found to determine which move is the best!
        top_score = -math.inf

        # Loop through the possible moves for the player character
        for posy_x in [-1, 0, 1]:
            if (self.x + posy_x >= 0) and (self.x + posy_x < wrld.width()):
                for posy_y in [-1, 0, 1]:
                    if (posy_x != 0) or (posy_y != 0):
                        new_wrld = wrld.from_world(wrld)
                        bomberman = new_wrld.me(self)
                        if(bomberman.y + posy_y >= 0) and (bomberman.y + posy_y < wrld.height()):
                            if not wrld.wall_at((bomberman.x + posy_x), (bomberman.y + posy_y)):
                                bomberman.move(posy_x, posy_y)
                                move_points = self.expval(new_wrld.next()[0], new_wrld.next()[1], (depth - 1))
                                print("Points are: ", move_points)
                                if move_points > top_score:
                                    top_score = move_points
                                    self.dx = posy_x
                                    self.dy = posy_y

        print("Top Score: ", top_score)
        

    def expval(self, wrld, events, depth):
        # If the character has died or found the goal, calculate the utility
        if (wrld.me(self) == None):
            return -9999.0 * (depth + 1)
        
        if (len(events) > 0):
            for event in events:
                if ((3 == event.tpe) or
                    (2 == event.tpe) or
                    (4 == event.tpe)):
                    return self.state_utility(wrld, events, depth)
        # If the depth limit has been reached, calculate the utility
        elif (depth == 0):
            return self.state_utility(wrld, events, depth)
        
        v = 0

        # Loop through all the monsters in the world
        for key in wrld.monsters:
            for mon in wrld.monsters[key]:
                moves = []
                worlds = []
                
                # Loop through all the possible moves for the current monster
                for posy_x in [-1, 0, 1]:
                    for posy_y in [-1, 0, 1]:
                        if (posy_x != 0) and (posy_y != 0):
                            if (mon.x + posy_x >= 0) and (mon.x + posy_x < wrld.width()):
                                if(mon.y + posy_y >= 0) or (mon.y + posy_y < wrld.height()):
                                    if not wrld.wall_at((mon.x + posy_x), (mon.y + posy_y)):
                                        # Calculate the distance between the monster and the character after the move
                                        char_dist = math.sqrt((((mon.x + posy_x) - wrld.me(self).x)**2) + (((mon.y + posy_y) - wrld.me(self).y)**2))

                                        # If the monster is more than three squares away, then it can be ignored
                                        if (char_dist >= math.sqrt(18.0)):
                                            # Calculate the score based off of that
                                            dist_score = 1.0 / (char_dist + 0.001)
                                            # Add this to the scores for all the moves
                                            moves.append(dist_score)

                                            # Create a new world and monsters
                                            new_wrld = wrld.from_world(wrld)
                                            new_mon = new_wrld.monsters[key][0]
                                            new_mon.move(posy_x, posy_y)
                                            worlds.append(new_wrld)

                if (len(moves) == 0):
                    return self.maxval(wrld.next()[0], wrld.next()[1], (depth - 1))
                
                total_move_score = sum(moves)

                # Iterate through the worlds and calculate the probability
                # based on how close to the player the monster will be
                # (The player assumes that the monsters are more likely to move towards them)
                for i in range(len(moves)):
                    proby = moves[i] / total_move_score
                    new_wrld = worlds[i].next()[0]
                    new_events = worlds[i].next()[1]

                    # Move on to the next step!
                    v = v + (proby * self.maxval(new_wrld, new_events, (depth - 1)))

        if (v == 0):
            v = v + self.maxval(wrld.next()[0],  wrld.next()[1], (depth - 1))

        return v
    
    def maxval(self, wrld, events, depth):
        bomberman = wrld.me(self)
        if (bomberman == None):
            return -9999.0 * (depth + 1)
        
        if (len(events) > 0):
            for event in events:
                if ((3 == event.tpe) or
                    (2 == event.tpe) or
                    (4 == event.tpe)):
                    return self.state_utility(wrld, events, depth)
        elif (depth == 0):
            return self.state_utility(wrld, events, depth)
        
        v = -math.inf 

        for posy_x in [-1, 0, 1]:
            if (bomberman.x + posy_x >= 0) and (bomberman.x + posy_x < wrld.width()):
                for posy_y in [-1, 0, 1]:
                    if (posy_x != 0) or (posy_y != 0):
                        if(bomberman.y + posy_y >= 0) and (bomberman.y + posy_y < wrld.height()):
                            if not wrld.wall_at((bomberman.x + posy_x), (bomberman.y + posy_y)):
                                # Make a clone of the world and the character
                                new_wrld = wrld.from_world(wrld)
                                baby_bomber = new_wrld.me(self)
                                baby_bomber.move(posy_x, posy_y)
                                # Move on to the next step!
                                v = max(v, self.expval(new_wrld.next()[0], new_wrld.next()[1], (depth - 1)))
        
        return v
    

    def state_utility(self, wrld, events, depth):
        if (len(events) > 0):
            for event in events:
                if ((3 == event.tpe) or
                    (2 == event.tpe)):
                    # If the character has died, return a big negative reward!
                    return -9999.0 * (depth + 1)
                elif (self.state == 'goal'):
                    # If the goal is found, return a big reward!
                    # (Multiply it by the depth so that lower depths are better)
                    if (4 == event.tpe):
                        return 9999.0 * (depth + 1)
        
        else:
            
            # Calculate the distance to the exit from the current cell
            exit_dist = (math.sqrt(((self.exitie[0] - wrld.me(self).x)**2) + ((self.exitie[1] - wrld.me(self).y)**2)))

            # Calculate the distance of the closest monster
            closey_mon = math.sqrt((wrld.height()**2) + (wrld.width()**2)) + 0.5
            for key in wrld.monsters:
                for mon in wrld.monsters[key]:
                    mon_dist = (math.sqrt(((mon.x - wrld.me(self).x)**2) + ((mon.y - wrld.me(self).y)**2)))
                    if (closey_mon > mon_dist):
                        closey_mon = mon_dist
                        
            # Get the total value
            return  (1.0 *-exit_dist) - (0.5 * closey_mon) - self.num_steps
        

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

            if (current_spot == tuple(self.exitie)):
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

                            total_score = starty_score + abs(neighbor_spot[0] - self.exitie[0]) + abs(neighbor_spot[1] - self.exitie[1])
                            heapq.heappush(open_set, (total_score, neighbor_spot))

        return []

        


        
