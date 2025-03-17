class item:
    def __init__(self,name,description,effect):
        self.__name = name
        self.__description = description
        self.__effect = effect
#assume inventory is included in player class
#modify player class to include interactions with items
#define locations on map(map.py) for item pickup
#include collision - similar to wall collision for pick up
#