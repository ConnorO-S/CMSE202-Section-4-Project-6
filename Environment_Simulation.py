import matplotlib.pyplot as plt
import numpy as np
import random
from IPython.display import display, clear_output
import time
import matplotlib.colors as mcolors

class World: 
    def __init__(self, rows=50, cols=50, environment='placeholder', animals=None):
        """
        Initializes a Board.

        Args:
            rows/cols: The size of the world
            
            environment: Choose from (Jungle, Forest, Meadow, Savannah, Desert)
                - Jungle has most vegetation/water
                - Desert has least
                
            animals: A list of all of the animals in the world initially 
        """
        if animals is None:
            animals = []

        self.rows = rows
        self.cols = cols
        self.environment = environment
        self.animals = animals
        self.world_grid = None  ## make this in setup
        
        self.basic_setup(rows, cols, environment, animals)

    def basic_setup(self, rows, cols, environment, animals):
        """Sets up the world grid."""
        
        # make a variable that changes enviorment into something usefull
        env_order = ['Jungle', 'Forest', 'Meadow', 'Savannah', 'Desert']
        if environment in env_order:
            env_var = 5 - env_order.index(environment)
        else:
            env_var = 1  # default if invalid environment name

        self.env_value = env_var 

        # initlize world grid
        world_grid = np.zeros((rows, cols, 3)) # the three are water vegetitation and meat in that order
        for x in range(rows):
            for y in range(cols):
                water = random.randint(40, 50) * (env_var /5)
                veg = random.randint(40, 50) * (env_var /5)
                meat = 0 
                world_grid[x, y] = [water, veg, meat]
        
        self.world_grid = world_grid

    def get_tile(self, x_pos, y_pos):
        return self.world_grid[x_pos, y_pos]


    def add_animal(self, animal):
    # Adds an animal to the world.
        self.animals.append(animal)

    def remove_animal(self, animal):
       # Removes an animal from the world.

        if animal in self.animals:
            position = animal.get_position()
            self.world_grid[position[0], position[1]][2]+= 30
            self.animals.remove(animal)
            
    def count_animals(self):
        count_dict = {'carn': 0, 'omni': 0, 'herb': 0}
        for animal in self.animals:
            if isinstance(animal, Carnivore):
                count_dict['carn']+=1
            elif isinstance(animal, Omnivore):
                count_dict['omni']+=1
            elif isinstance(animal, Herbivore):
                count_dict['herb']+=1
        return count_dict
        

    def update_environment(self):  # corrected spelling
        env_dict = {'Jungle': 0,'Forest': 0,'Meadow': 0,'Savannah': 0,'Desert': 0,}
        for x in range(self.rows):
            for y in range(self.cols):
                tile = self.get_tile(x,y)
                if tile[0] <10:
                    env_dict['Desert'] += 1
                elif tile[0] <20:
                    env_dict['Savannah'] += 1
                elif tile[0] <30:
                    env_dict['Meadow'] += 1
                elif tile[0] <40:
                    env_dict['Forest'] += 1
                else:
                    env_dict['Jungle'] += 1
        env_val = 0
        max_env = ''
        for env, count in env_dict.items():  # fixed logic
            if count > env_val:
                max_env = env
                env_val = count
        self.environment = max_env

        env_order = ['Jungle', 'Forest', 'Meadow', 'Savannah', 'Desert']
        if self.environment in env_order:
            env_var = 5 - env_order.index(self.environment)
        else:
            env_var = 1  # default if invalid environment name

        self.env_value = env_var
            


    def draw_board(self):
        """
        Draws the world board using matplotlib.
        Darws board with vegetation level, animal position
        """
        # Extract vegetation layer (assuming index 1 represents vegetation)
        layer = self.world_grid[:, :, 1]

        an_color_lst = []
        an_x_lst = []
        an_y_lst = []

        # Collect animal positions and colors
        for animal in self.animals:
            x, y = animal.get_position()
            an_x_lst.append(x)
            an_y_lst.append(y)
            if isinstance(animal, Carnivore):
                an_color_lst.append('red')
            elif isinstance(animal, Omnivore):
                an_color_lst.append('yellow')
            elif isinstance(animal, Herbivore):
                an_color_lst.append('green')
            else:
                an_color_lst.append('black')


        ## make good colormap:
        brown = (0.59, 0.29, 0.0)  # Example brown
        green = (0.0, 0.5, 0.0)    # Example green

        colors = [brown, green]
        cmap_BrGn = mcolors.LinearSegmentedColormap.from_list("BrownToGreen", colors)

        fig, ax = plt.subplots(figsize=(6, 6))

        img = ax.imshow(layer, cmap=cmap_BrGn, alpha=0.7, vmin=0, vmax=50)
        ax.scatter(an_y_lst, an_x_lst, c=an_color_lst, edgecolors='white', s=40)  # swapped x/y + edgecolors fix
        ax.set_title("World Map: Vegetation and Animal Positions")
        ax.set_xlabel(f"Current Environment: {self.environment}")       
        fig.colorbar(img, ax=ax, label="Vegetation Level")
        return ax

    def run_animation(self, time=50): ### time is the number of steps to run the animation for
        fig, ax = plt.subplots(figsize=(10, 5))
        
        for count in range(time):
            for animal in list(self.animals):  # list() so adding/removing animals doesn’t break loop
                animal.age += 1
                animal.energy +=1
                animal.satiety -= 2
                if animal.age > animal.lifespan:
                    self.remove_animal(animal)
                if animal.satiety<=0:
                    self.remove_animal(animal)
            
        
                animal.decide_move(self)
                pos = animal.get_position()

                # Correct coordinate order
                meat = self.get_tile(pos[0], pos[1])[2]
                veg  = self.get_tile(pos[0], pos[1])[1]

                if isinstance(animal, Carnivore):
                    meat_left = animal.eat(meat)
                    self.world_grid[pos[0], pos[1]][2] = meat_left
                elif isinstance(animal, Herbivore):
                    veg_left = animal.eat(veg)
                    self.world_grid[pos[0], pos[1]][1] = veg_left
                elif isinstance(animal, Omnivore):
                    veg_left, meat_left = animal.eat(veg, meat)
                    self.world_grid[pos[0], pos[1]][2] = meat_left
                    self.world_grid[pos[0], pos[1]][1] = veg_left
            
        # Update the world (regrowth, environment, etc.)
            for x in range(self.rows):
                for y in range(self.cols):
                    water_diff = 0
                    if self.world_grid[x,y][2]>=1:
                        self.world_grid[x,y][2] -= 1  ### Make meat decay (fixed)
                    if self.world_grid[x,y][0] > self.world_grid[x,y][1]:
                        water_diff = self.world_grid[x,y][0] - self.world_grid[x,y][1]
                        if water_diff>0:
                            self.world_grid[x,y][1] += water_diff/2
                            self.world_grid[x,y][0] -= water_diff/2
                    if self.world_grid[x,y][0] <=60:  ### cap max water and vegetation level
                        self.world_grid[x,y][0] += 1 * (self.env_value /5)
            self.update_environment()  # corrected spelling

        # Draw the updated world
            clear_output(wait=True)
            ax.clear()
            ax = self.draw_board()
            plt.pause(0.2)


    def run_data(self, time=50): ### time is the number of steps to run the simulation for
        """
     Generates and returns a nested list containing data baout the simulation for each timestep.
     The first nested list is a list from 0 to time represent the timestep
     The second nested list is a list of tuples containing the number of Carnivores, Omnivores and Herbivres in that order ex. (5,10,40)
     The third nested list is a list of tuples containing the average amount of water, vegitation and meat per tile in that order ex. (34.7, 30.02, 9.9)
        """
        
        data = [[],[],[]]
        for count in range(time):
            ### add info for step to data
            #add step to list
            data[0].append(count)

            #add animal tuple to list
            animals = self.count_animals()
            data[1].append((animals['carn'], animals['omni'], animals['herb']))

            #add enviornment tuple to list
            tile_lst = []
            for x in range(self.rows):
                for y in range(self.cols):
                    tile = self.get_tile(x,y)
                    tile_lst.append(tile)
            avg_water = 0
            avg_veg = 0
            avg_meat = 0
            for tile in tile_lst:
                avg_water += tile[0]
                avg_veg += tile[1]
                avg_meat += tile[2]
            data[2].append((round(avg_water/len(tile_lst), 2), round(avg_veg/len(tile_lst), 2), round(avg_meat/len(tile_lst), 2)))
            
                
            for animal in list(self.animals):  # list() so adding/removing animals doesn’t break loop
                animal.age += 1
                animal.energy +=1
                animal.satiety -= 2
                if animal.age > animal.lifespan:
                    self.remove_animal(animal)
                if animal.satiety<=0:
                    self.remove_animal(animal)
            
        
                animal.decide_move(self)
                pos = animal.get_position()

                # Correct coordinate order
                meat = self.get_tile(pos[0], pos[1])[2]
                veg  = self.get_tile(pos[0], pos[1])[1]

                if isinstance(animal, Carnivore):
                    meat_left = animal.eat(meat)
                    self.world_grid[pos[0], pos[1]][2] = meat_left
                elif isinstance(animal, Herbivore):
                    veg_left = animal.eat(veg)
                    self.world_grid[pos[0], pos[1]][1] = veg_left
                elif isinstance(animal, Omnivore):
                    veg_left, meat_left = animal.eat(veg, meat)
                    self.world_grid[pos[0], pos[1]][2] = meat_left
                    self.world_grid[pos[0], pos[1]][1] = veg_left
            
        # Update the world (regrowth, environment, etc.)
            for x in range(self.rows):
                for y in range(self.cols):
                    water_diff = 0
                    if self.world_grid[x,y][2]>=1:
                        self.world_grid[x,y][2] -= 1  ### Make meat decay (fixed)
                    if self.world_grid[x,y][0] > self.world_grid[x,y][1]:
                        water_diff = self.world_grid[x,y][0] - self.world_grid[x,y][1]
                        if water_diff>0:
                            self.world_grid[x,y][1] += water_diff/2
                            self.world_grid[x,y][0] -= water_diff/2
                    if self.world_grid[x,y][0] <=60:  ### cap max water and vegetation level
                        self.world_grid[x,y][0] += 1 * (self.env_value /5)
            self.update_environment()  # corrected spelling

        return data

class Animal:
    def __init__ (self, posX, posY, max_satiety, speed, vision, lifespan):
        self.age = 0
        self.energy = 0 # how old the animal is
        self.posX = posX          # where on the board this animal is located
        self.posY = posY          # intuitive
        self.max_satiety = max_satiety    # how much energy the animal can store in eaten food
        self.satiety = random.randint(90, 100)/100 * max_satiety        # Update so animals no longer start at max saitety
        self.speed = speed        # how many tiles it can move every time time advances
        self.vision = vision      # how many tiles it will look at to find the best place to go
        self.lifespan = lifespan
    

    def look(self): # returns every location that this animal looks at
        search_area = []
        for x in range (1+self.vision*2):
            for y in range (1+self.vision*2):
                lookX = self.posX - self.vision + x
                lookY = self.posY - self.vision + y
                search_area.append([lookX, lookY])
        return search_area

    def move(self, posX, posY): # changes the position of the animal
        distance = max(abs(posX - self.posX), abs(posY - self.posY))
        if (distance <= self.speed):  # FIXED: uses speed instead of satiety
            self.posX = posX
            self.posY = posY
            self.satiety -= 3*distance
            

    def eat(self, food_present):  # returns the food left that the animal did not eat
        max_bite = 10
        food_wanted = self.max_satiety - self.satiety
        if food_wanted >= max_bite:
            food_wanted = max_bite
        
        if food_wanted > food_present:
            self.satiety += food_present
            return(0)
        else:
            food_present -= food_wanted
            self.satiety += max_bite
            return(food_present)

    def get_position(self):
        return [self.posX, self.posY]


    def reproduce(self, world):
        self_type = type(self)

        # Only reproduce if energetic
        if self.energy < 5:
            return 0

        mate_lst = []
        for x, y in self.look():
            for animal in world.animals:
                if animal is not self and isinstance(animal, self_type):
                    if animal.get_position() == [x, y]:
                        if animal.age >= 5 and animal.satiety >= 0.8 * animal.max_satiety:
                            mate_lst.append(animal)
        if not mate_lst:
            return 0

        mate_max = 'placeholder'
        sait_max = 0
        for mate in mate_lst:
            if mate.satiety > sait_max:
                mate_max = mate
                sait_max = mate.satiety
        new_pos = mate_max.get_position()
        
        self.move(new_pos[0], new_pos[1])
        
        age = 0              
        posx = self.posX 
        posy = self.posY 
        max_sait = self.max_satiety
        speed = self.speed
        vision = self.vision
        lifespan = self.lifespan

        baby = self_type(posx, posy, max_sait, speed, vision, lifespan)
        baby.age = 0
        baby.satiety = 0.5 * self.max_satiety  # start half-fed
        world.add_animal(baby)

        # Prevent Infinite reproduction loop
        self.satiety *= 0.7
        mate_max.satiety *= 0.7
        self.energy = 0
        mate_max.energy = 0

        return 1

class Carnivore(Animal):

    def eat(self, food_present):
        """
        Carnivores only eat meat.
        Returns remaining meat after eating.
        """
        max_bite = 15
        food_wanted = self.max_satiety - self.satiety
        if food_wanted > max_bite:
            food_wanted = max_bite

        # amount actually eaten
        eaten = min(food_present, food_wanted)
        self.satiety += eaten
        return food_present - eaten

    def decide_move(self, world):
        """
        Carnivore looks for tiles with the most meat within its vision range,
        otherwise hunts for nearby prey.
        """
        # Try reproduce if full & old enough
        if self.satiety > 0.9 * self.max_satiety and self.age >= 5:
            if self.reproduce(world):
                return

        # Look for highest meat tile in vision
        best_tile = (self.posX, self.posY)
        best_meat = world.world_grid[self.posX, self.posY, 2]

        for x, y in self.look():
            if 0 <= x < world.rows and 0 <= y < world.cols:
                meat = world.world_grid[x, y, 2]
                if meat > best_meat:
                    best_meat = meat
                    best_tile = (x, y)

        if best_meat > 0:
            self.move(*best_tile)
        else:
            # no meat found; try hunting animals
            self.hunt(world)

    def hunt(self, world):
        """Look for highest-satiety Herbivore first then Omnivore; move and kill."""
        best_prey = None
        best_sat = -1

        prey_type = None
        for x, y in self.look():
            if 0 <= x < world.rows and 0 <= y < world.cols:
                for animal in world.animals:
                    if animal is self:
                        continue
                    if animal.get_position() == [x, y]:
                        # prioritize Herbivore, then Omnivore by satiety
                        if isinstance(animal, Herbivore) and animal.satiety > best_sat:
                            best_prey = animal
                            best_sat = animal.satiety
                            prey_type = 'Herbivore'
                        elif isinstance(animal, Omnivore) and best_prey is None and animal.satiety > best_sat:
                            # only pick omnivore if no herbivore found yet
                            best_prey = animal
                            best_sat = animal.satiety
                            prey_type = 'Omniivore'                            
                        elif isinstance(animal, Carnivore) and best_prey is None and animal.satiety > best_sat and self.satiety<= self.max_satiety*0.5:
                            # only pick omnivore if no herbivore found yet
                            best_prey = animal
                            best_sat = animal.satiety
                            prey_type = 'Carnivore'    

        if best_prey:
            if prey_type == 'Carnivore':
                self.satiety -= 10
            if prey_type == 'Omnivore':
                self.satiety -= 5
            prey_pos = best_prey.get_position()
            self.move(prey_pos[0], prey_pos[1])
            world.remove_animal(best_prey)
        else:
            pass


class Omnivore(Animal):

    def eat(self, veg_present, meat_present):
        """
        Omnivores eat both veg and meat.
        Returns remaining (veg, meat) after eating.
        """
        max_bite = 10
        food_wanted = self.max_satiety - self.satiety
        if food_wanted > max_bite:
            food_wanted = max_bite

        total_available = veg_present + meat_present
        eaten = min(total_available, food_wanted)

        # eat meat first
        meat_eaten = min(meat_present, eaten)
        veg_eaten = eaten - meat_eaten

        self.satiety += veg_eaten + meat_eaten
        return (veg_present - veg_eaten, meat_present - meat_eaten)

    def decide_move(self, world):
        # try reproduce if full & old enough
        if self.satiety > 0.9 * self.max_satiety and self.age >= 5:
            if self.reproduce(world):
                return

        # look for best (veg + meat)
        best_tile = (self.posX, self.posY)
        best_score = world.world_grid[self.posX, self.posY, 1] + world.world_grid[self.posX, self.posY, 2]

        for x, y in self.look():
            if 0 <= x < world.rows and 0 <= y < world.cols:
                water, veg, meat = world.world_grid[x, y]
                score = veg + meat
                if score > best_score:
                    best_score = score
                    best_tile = (x, y)

        self.move(*best_tile)


class Herbivore(Animal):
    def eat(self, food_present):
        """
        Herbivores only eat veg.
        Returns remaining veg after eating.
        """
        max_bite = 10
        food_wanted = self.max_satiety - self.satiety
        if food_wanted > max_bite:
            food_wanted = max_bite

        eaten = min(food_present, food_wanted)
        self.satiety += eaten
        return food_present - eaten

    def decide_move(self, world):
        # try reproduce if full & old enough
        if self.satiety > 0.9 * self.max_satiety and self.age >= 5:
            if self.reproduce(world):
                return

        best_tile = (self.posX, self.posY)
        best_veg = world.world_grid[self.posX, self.posY, 1]

        for x, y in self.look():
            if 0 <= x < world.rows and 0 <= y < world.cols:
                veg = world.world_grid[x, y, 1]
                if veg > best_veg:
                    best_veg = veg
                    best_tile = (x, y)

        self.move(*best_tile)