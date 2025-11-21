# CMSE202-Section-4-Project-6
What are the primary factors that determine the health of an ecosystem (animals +
environment)? How accurately can ecosystem models reflect real world scenarios? Can
they be used to predict outcomes and inform policies for real ecosystems?

# Classes
There are 5 main classes and sub-classes used in this project. The Classes are World and Animal. The sub-classes are Carnivore, Omnivore, Herbivore
## World(rows, cols, environment, animals)
#### The World class takes 4 arguments

    rows/cols: these determine the number of rows and columns. These values accept an integer
    
    environment: This is the initial environment of the world. Choose from (Jungle, Forest, Meadow, Savannah, Desert). This argument accepts a string. This value determines the initial amount of water and vegetation in each cell with Jungle having the most and Desert having the least. The environment will change based on the current state of the board. Each turn it counts the number of tiles with vegetation in each range [0,10] [10,20] [20,30] [30,40] [40+] then changes the environment to the range with the most cells. ex if more than half of the cells have an amount of vegetation between 30 and 40 then the environment will be set to Forest. During an animation the current environment is displayed at the bottom of the animation. The current environment is used to determine the rate at which plants on any given tile regrow. 

    animals: This argument accepts a list of animal objects composed of Carnivores, Omnivores and Herbivores

    An example of a complete World class is:
    Example_world = World(rows=20, cols=20, environment='Jungle', animals = Example_Animal_lst)

#### The World class has several relevant functions

    World.(self, x_pos, y_pos): This functions accepts the x and y position(Intigers) of a tile on the world and returns a list containing the amount of water, vegetation and meat on the selected tile

    World.add_animal(self, animal): This function accepts an animal object and appends that anamial to the world's animal list adding it to the world

    World.remove_animal(self, animal): This function accepts an animal object and removes that animal from the animal list and adds meat to the tile the animal previously occupied.

    World.count_animals(self): This function returns a dictionary containing the numebr of carnivores, omnivores and herbivores in the world

    World.update_environment(self): This function updates the current environment of the world depending on the current amount of vegetation on each cell

    World.draw_board(self): This functions draws the current board using a heatmap to show the vegetation for each tile and a scatter plot to show the poitions of the animals. 

    World.run_animation(self, time): This function accepts and intiger and displays an animation of the simulation running for that number of steps

    World.run_data(self, time): This function accepts and intiger and returns data about the simulation running for the intiger number of steps. 
    The data is formatted formated as a list containing three nested lists.
    The first nested list is a list from 0 to time represent the timestep
    The second nested list is a list of tuples containing the number of Carnivores, Omnivores and Herbivres in that order ex. (5,10,40)
    The third nested list is a list of tuples containing the average amount of water, vegitation and meat per tile in that order ex. (34.7, 30.02, 9.9)

## Animal(posX, posY, max_satiety, speed, vision, lifespan)
#### The animal class takes 6 arguments

    posX/posY: The initial x and y position of the animal. These arguments accept an integer

    max_satiety: This is the maximum satiety and animal can have. Saitety is replenished by eating and decreases as time passes or the animal moves. If satiety is to low the animal cannot move and if satiety reaches 0 the animal dies. Initial Satiety is between 90 and 100% of max satiety determinded randomly. This argument accepts an intiger

    speed: The maximum distance an animal can move. It accepts and intiger

    vision: The maximum distance and animal can see. It accepts an intiger.
    NOTE: setting speed and vision to different values may result in an error

    lifespan: The number to timesteps an animal can live before it dies of old age

#### The animal class has several relevant functions

    Animal.look(self): This reaturns a list of the x an y cordinates of the board tiles you can see

    Animal.move(self, posX, posY): accepts 2 intigers moves the animal to the specified x and y position if the animal has sufficient speed and satiety

    Animal.eat(self, food_present): accepts 1 intiger pr float. it returns the remaining food from the food present given and adjusts the satiety of the given animal based on the difference between food_present and the remaining food

    Animal.get_position(self): returns a list containg the current x and y position of the animal as intigers

    Animal.reproduce(self, world): This function accepts a world object and checks if the animal is old enough, has enough satiety and if there is an another animal nearby in which case it adds a new animal to the list of animals associated with the provided world object.

### The Animal class has three sub-classes all of these subclass accept the same arguments however each of the sub-classes have different functions
### Carnivore

    Carnivore.decide_move(self, world): Accepts a world. If satiety is sufficiently high it runs Animal.reproduce(self, world). Otherwise it looks at all tiles within the range of vision and moves to the one with the highest amount of meat. If there is no meat on a surrounding tile it calls the hunt function instead

    Carnivore.hunt(self, world): Accepts a world, looks at all nearby animals then moves to the herbivore with the highest satiety. If there are no herbivores in range it instead moves to the omnivore with the highest satiety, if there are no omnivores in range it moves to the carnivore with the highest satiety. Then animal the carnivore moved to is removed from the world using World.remove_animal. 

    Carnivore.eat(self, meat_present): accepts 1 intiger or float. it returns the remaining meat and adjusts the satiety of the given animal based on the difference between meat_present and the remaining meat.


### Omnivore

    Omnivore.decide_move(self, world): Accepts a world. If satiety is sufficiently high it runs Animal.reproduce(self, world). Otherwise it looks at all tiles within the range of vision and moves to the one with the highest combined amount of meat and vegetation. 

    Omnivore.eat(self, veg_present, meat_present): Accepts 2 intigers or floats, returns a list containing the amount of remaining vegetation and meat. eats meat first and then vegetation and increases current satiety

### Herbivore

    Herbivore.decide_move(self, world): Accepts a world. If satiety is sufficiently high it runs Animal.reproduce(self, world). Otherwise it looks at all tiles within the range of vision and moves to the one with the highest combined amount of vegetation

    Herbivore.eat(self, veg_present): accepts 1 intiger or float. it returns the remaining vegetation and adjusts the satiety of the given animal based on the difference between veg_present and the remaining vegetation.



##  Here is some example code showing how to run a simulation
"""
### Import Relevant Information

    from Environment_Simulation import World
    from Environment_Simulation import Animal
    from Environment_Simulation import Carnivore
    from Environment_Simulation import Omnivore
    from Environment_Simulation import Herbivore

    import matplotlib.pyplot as plt
    import numpy as np
    import random
    from IPython.display import display, clear_output
    import time
    import matplotlib.colors as mcolors


### Create and fill a list with animals
    example_animal_list = []

    for x in range(50): ## Creates 50 Herbivores
        example_animal_list.append(Herbivore(random.randint(0, 19), random.randint(0, 19), 50, 1, 1, 20))
    for x in range(5): ## Creates 5 Omnivores
        example_animal_list.append(Omnivore(random.randint(0, 19), random.randint(0, 19), 50, 2, 2, 25))
    for x in range(4):  ## Creates 4 Carnivores
        example_animal_list.append(Carnivore(random.randint(0, 19), random.randint(0, 19), 50, 3, 3, 30))

### Create a World
    Example_world = World(rows=20, cols=20, environment='Jungle', animals = example_animal_list)

### Run an animation
    Example_world.run_animation(time=50)
"""

## Group Member Contributions
### Connor Owen-Smith
    World Class
    Carnivore Hunt function
    Animal Get Position and Reproduce Functions
    All animal subclasses decided move function modifications
    Getting all classes and subclasses to work together and do things withought crashing
    Parts of the Presentation slideshow and project report

### Allan Morse
    ***

### Zach Nolff
    *** 
    
    
                    