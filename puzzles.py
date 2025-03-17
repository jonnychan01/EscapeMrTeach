import pygame
import pygame as pg
import sys
from settings import *

#this file will contain the code for each puzzle
class puzzle:
    def __init__(self, correctAns, imgPath):
        pygame.init()

        #setting the correct answer to a pygame key input
        if correctAns == "1":
            self.correctAns = pygame.K_1
        elif correctAns == "2":
            self.correctAns = pygame.K_2
        elif correctAns == "3":
            self.correctAns = pygame.K_3
        else:
            self.correctAns = pygame.K_4
        
        self.imgPath = imgPath
        self.correctSound = pygame.mixer.Sound("resources\sound\correctAns.mp3")
        self.wrongSound = pygame.mixer.Sound("resources\sound\wrongAns.mp3")
        self.wrongSound.set_volume(0.7)

    #Display image
    def displayImg(self,game):
        screen = game.screen
        image = pygame.image.load(self.imgPath).convert_alpha() #loads the image
        #displays the image
        screen.blit(image,(500,200)) #the cords are hard coded so it will need to be change if RES is edited
    
    #Checking input
    def checkAns(self, game):
        game.player.inpuzzle = True

        self.displayImg(game) #display the img
        pygame.display.update()

        while True:
            # creating a loop to check events that
            # are occurring
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                # checking if keydown event happened or not
                if (event.type == pygame.KEYDOWN and event.key == self.correctAns):
                    game.player.inpuzzle = False
                    pygame.mixer.Sound.play(self.correctSound)

                    return True #this exits the loop
                
                #WORKING CODE FOR EXITING || HOWEVER you will need to recode how game checks for correct puzzle completion
                # elif (event.type == pygame.KEYDOWN and event.key == pygame.K_x): #exit the question interface
                #     game.player.inpuzzle = False
                #     return True

                 #u keep doing the question until you get it right lol
                elif (event.type == pygame.KEYDOWN and event.key != self.correctAns): #IF THE KEY PRESSED IS NOT THE CORRECT KEY!
                     #if you get it wrong then itll add to the "seentime", which is basically how long mr vantonder has LOS then gets mad
                    pygame.mixer.Sound.play(self.wrongSound) #plays sound effect for getting question wrong
                    
                    #raise Mr Van Tonders anger level
                    game.object_handler.npc_list[0].seentime += 100
                    game.wrongans = True # tells game you got Q wrong

                    #pygame.time.delay(1500) #wait 1.5 seconds || turn off if you donyt like this feel of this




#declaring all questions
# question0_0 = puzzle('1','resources\puzzles\question_0_0.png')
# question0_1 = puzzle('4','resources\puzzles\question_0_1.png')
# question0_2 = puzzle('2','resources\puzzles\question_0_2.png')
                
# question1_0 = puzzle('3','resources\puzzles\question_1_0.png')
# question2_0 = puzzle('2','resources\puzzles\question_2_0.png')
# question3_0 = puzzle('1','resources\puzzles\question_3_0.png')
# question4_0 = puzzle('3','resources\puzzles\question_4_0.png')

# allPuzzles = [question0_0, question0_1, question0_2, question1_0, question2_0, question3_0, question4_0]

allPuzzles = []
#Initalizes all puzzles
def puzzleInit():
    f = open('resources\questionAnswers.txt', "r")
    temp = f.readlines()

    for i in range(0,len(temp)-1):
        filePath = 'resources\puzzles\question_' + (temp[i])[0:3] + '.png' #uses name of puzzle to create the file path
        ans = (temp[i])[4] #sting manilipulation to get the answer
        allPuzzles.append(puzzle(ans, filePath))
    
    f.close()

puzzleInit()