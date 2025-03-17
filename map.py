import pygame as pg
import random
from puzzles import allPuzzles #imports the array of all the puzzles from puzzles.py
_ = False

mini_map = [
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, _, 3, 3, 3, 3, 3, _, _, 3, 3, 3, _, _, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, _, 1],
    [1, _, _, 3, 4, 4, 4, 3, _, _, 3, 4, 3, _, _, 3, 4, 4, 4, 4, 3, 4, 4, 4, 4, 3, _, 1],
    [1, _, _, 3, 4, 4, 4, 3, _, _, 3, 4, 3, _, _, 3, 4, 4, 4, 4, 3, 4, 4, 4, 4, 3, _, 1],
    [1, _, _, 3, 4, 4, 4, 3, _, _, 3, 4, 3, _, _, 3, 4, 4, 4, 4, 3, 4, 4, 4, _, 3, _, 1],
    [1, _, _, 3, _, 3, 3, 3, _, _, 3, _, 3, _, _, 3, 3, 3, _, 3, 3, 3, 3, 3, _, 3, _, 1],
    [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, _, 3, 3, 3, 3, 3, 3, _, 3, 3, 3, 3, _, 3, _, 3, 3, 3, 3, 3, 3, _, _, _, _, 1],
    [1, _, _, 3, 4, 4, 4, 4, 3, _, 3, 4, 4, 3, _, 3, 4, 4, 4, 4, 4, 4, _, _, _, _, _, 1],
    [1, _, _, 3, 4, 4, 4, 4, 4, _, 4, 4, 4, 3, _, 3, 4, 4, 4, 4, 3, 4, 3, _, _, _, _, 1],
    [1, _, _, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, _, 3, 3, 3, 3, 3, 3, _, 3, _, _, _, _, 1],
    [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, _, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
]
offset = 0.5
placedlocs = []
inMapPuzzles = [] #these are the puzzles that placed in the map
spiderloc = []
doorloc = []
pickedRooms = [] #stores that rooms that have items in them
roomBound = [[[4,4],[6,6]],[[4,11],[6,11]],[[4,16],[6,19]],[[4,21],[6,24]],[[11,4],[12,12]],[[11,16],[12,21]]] #y,x

def genpuzzles(inputmap):
        walldoor = random.randint(0,3)
        #walldoor = 3
        if walldoor == 0:
            mini_map[0][random.randint(1,(len(mini_map[0])-1))] = 5
        elif walldoor == 1:
            mini_map[len(mini_map)-1][random.randint(1,(len(mini_map[0])-1))] = 5
            #mini_map[len(mini_map[0])-1][random.randint(1,len(mini_map)-1)] = 5
        elif walldoor == 2:
            mini_map[random.randint(1,(len(mini_map)-1))][0] = 5
            #mini_map[random.randint(1,len(mini_map[random.randint(1,len(mini_map)-1)]))][0] = 5
        elif walldoor == 3:
            mini_map[random.randint(1,(len(mini_map)-1))][len(mini_map[0])-1] = 5
            #mini_map[random.randint(1,len(mini_map[random.randint(1,len(mini_map)-1)][len(mini_map[0])]))] = 5
        
        #randomly placing puzzles
        placed = 0
        doorplace = False
        while placed < 4:
            #Randomly picks a room to place the item in
            room = random.randint(0,len(roomBound)-1)
            while room in pickedRooms:
                room = random.randint(0,len(roomBound)-1)
            pickedRooms.append(int(room))

            #Randomly generate cords
            x = random.randint(roomBound[room][0][1],roomBound[room][1][1])
            y = random.randint(roomBound[room][0][0],roomBound[room][1][0])
            while mini_map[y][x] == _: #checking incase if the area cant place puzzles
                x = random.randint(roomBound[room][0][1],roomBound[room][1][1])
                y = random.randint(roomBound[room][0][0],roomBound[room][1][0])
            
            if (placed == 3): #places spider
                spiderloc.append([x+offset,y+offset])
                placedlocs.append([x+offset,y+offset])
                placed += 1
            else:
                placedlocs.append([x+offset,y+offset])

                #randomly placing the puzzle in the room
                ran = random.randint(0,len(allPuzzles)-1)
                while allPuzzles[ran] in inMapPuzzles: #checking if its already been added
                    ran = random.randint(0,len(allPuzzles)-1)
                inMapPuzzles.append(allPuzzles[ran])
                
                placed += 1

        #get rid of '4' and replace with blank                   
        for count in range(len(mini_map)):
            for i in range(len(mini_map[count])):
                if mini_map[count][i] == 4:
                    mini_map[count][i] = _
        #door placement
        while doorplace == False:
            if walldoor == 0:
                 for count in range(len(mini_map[0])):
                    if mini_map[0][count] == 5:
                        doorloc.append([count+offset,1+offset])
                        placedlocs.append(([count+offset,1+offset]))
                        doorplace = True
            elif walldoor == 1:
                 for count in range(len(mini_map[0])):
                    if mini_map[len(mini_map)-1][count] == 5:
                        doorloc.append([count+offset,len(mini_map)-2+offset])
                        placedlocs.append(([count+offset,len(mini_map)-2+offset]))
                        doorplace = True
            elif walldoor == 2:
                 for count in range(len(mini_map)):
                    if mini_map[count][0] == 5:
                        doorloc.append([1+offset,count+offset])
                        placedlocs.append(([1+offset,count+offset]))
                        doorplace = True
            elif walldoor == 3:
                 for count in range(len(mini_map)):
                    if mini_map[count][len(mini_map[0])-1] == 5:
                        doorloc.append([len(mini_map[0])-2+offset,count+offset])
                        placedlocs.append(([len(mini_map[0])-2+offset,count+offset]))
                        doorplace = True
        return inputmap

class Map:
    def __init__(self, game):
        self.game = game
        self.mini_map = genpuzzles(mini_map)
        self.world_map = {}
        self.get_map()

    def get_map(self):
        for j, row in enumerate(self.mini_map):
            for i, value in enumerate(row):
                if value:
                    self.world_map[(i, j)] = value

    def draw(self):
        [pg.draw.rect(self.game.screen, 'darkgray', (pos[0] * 100, pos[1] * 100, 100, 100), 2)
         for pos in self.world_map]