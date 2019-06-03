import pygame
import time
import random
import math
from rain_drop import droplet
from lightning import Lightning
from drop_down_menu import dropDownMenu
import threading
from queue import Queue

FPS = 60

window_dimensions = [1280,720]

pygame.init()
screen = pygame.display.set_mode(window_dimensions)
pygame.display.set_caption('Rain Simulator')

#icon = pygame.image.load('apple.png')
#pygame.display.set_icon(icon)

pygame.display.update()

clock = pygame.time.Clock()
font = pygame.font
cyan = (0,155,255)
black = (0,0,0)
white = (255,255,255)

dropDownDict = {
    "Precipitation Type": ["Rain", "Snow"],
    "Intensity": ["Light","Moderate","Heavy"],
    "Wind Speed": [10,20,30,40,50,60,70,80,90,100],
    "Wind Force": ["Constant", "Varying"],
    "Lightning": ["On","Off"],
    "Lightning Branches": ["On","Off"]
    }
ddIndexValues = {key: 0 for key in dropDownDict.keys()}

dropDownWidth = 150
#ddIndexValues = [0 for keyIndex in range(len(dropDownDict))]

elementDropDown = dropDownMenu(window_dimensions[0]-(dropDownWidth*2+1), 0, dropDownWidth, 30, list(dropDownDict.keys()), screen)
for values in dropDownDict.keys():
    elementValues = dropDownMenu(window_dimensions[0]-dropDownWidth, 0, dropDownWidth, 30, dropDownDict[values], screen)
    break

def createAndModDroplets(droplet_width, rainIntensity = "light"):

    if rainIntensity == "light":
        intensity = 3
    elif rainIntensity == "moderate":
        intensity = 4
    elif rainIntensity == "heavy":
        intensity = 5

    return [[droplet(dCols) for dCols in range(math.ceil(window_dimensions[0]/droplet_width))] 
                   for dRows in range(intensity)]

def messageToScreen(msg, xCentered, yCentered, fontSize = 10):

    TextSurf, TextRect = textObjects(text, pygame.font.Font(None, fontSize))
    TextRect.center(xCentered, yCentered)
    screen.blit()

def drawDrops(dropletList, currentSet, start, stop):

    for currentDrop in range(start,stop):
        drop = dropletList[currentSet][currentDrop]

        #if the current droplet falls of the screen then check if that droplet index of all droplet sets 
        #are x distance away from the top of the screen before moving back above the screen to make sure 
        #new droplets don't overlap each other

        if drop.y > window_dimensions[1]:
            for setIndex in range(len(dropletList)):
                #allow only one droplet of a specific index of all droplet sets to be dropped at once
                if (dropletList[setIndex][currentDrop].y <= -50) and (currentSet != setIndex):
                    dropletList[setIndex][currentDrop].x = dropletList[setIndex][currentDrop].xOrignal
                    break
                if setIndex == len(dropletList)-1:
                    drop.resetSpeed(currentDrop*drop.width)

        if drop.isSnow:
            pygame.draw.circle(screen, white, [int(drop.x), int(drop.y)], drop.width)
        else:
            pygame.draw.rect(screen, cyan, [drop.x, drop.y, drop.width, drop.height])
        drop.increaseDropSpeed()

def gameLoop():

    rainIntensity = 3
    droplet_width = 4
    # creating all droplets
    dropletList = [[droplet(dCols) for dCols in range(math.ceil(window_dimensions[0]/droplet_width))] 
                   for dRows in range(rainIntensity)]

    boltStrikeSeconds = random.randrange(3,7)
    secondsPassed = 0
    bolt = Lightning(window_dimensions[0],window_dimensions[1])
    
    for i in range(1, len(dropletList)):
        for drop in dropletList[i]:
            drop.y = window_dimensions[1]

    gameExit = False

    while gameExit is not True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
                gameExit = True
            if event.type == pygame.K_ESCAPE:
                pygame.quit()
                quit()
                gameExit = True

        #draws over all previous drawings
        screen.fill(black)
        dropletIndex = 0


        if bolt.color == black and ddIndexValues["Lightning"] == 0:
            secondsPassed +=1

            if (FPS*boltStrikeSeconds) / secondsPassed <= 1:
                #start drawing lighting
                bolt.generateSwayPoints()
                if ddIndexValues["Lightning Branches"] == 1:
                    bolt.addBranches = False
                bolt.color = white
                bolt.resetPosition()
                boltStrikeSeconds = random.randrange(3,7)
                secondsPassed = 0

        drawEnvironment(dropletList,bolt)

        pygame.display.update()
        clock.tick(FPS)

    pygame.quit()
    quit()

def drawEnvironment(dropletList, bolt):
    threadJobs = 100
    threaderList = []

    #intialDropping

    for currentSet in range(len(dropletList)):
        startingJob = 0

        while True:

            if startingJob+threadJobs >= len(dropletList[0])-1:
                threaderList.append(threading.Thread(target = drawDrops(dropletList, currentSet, startingJob, len(dropletList[0]))))
                break
            else:
                threaderList.append(threading.Thread(target = drawDrops(dropletList, currentSet, startingJob, startingJob+threadJobs)))

            startingJob+=threadJobs
                
#        for dropObject in dropletList[i]:
#            drawDrops(dropletList, currentSet, currentDrop, dropObject)
#            currentDrop+=1
    time1 = time.time()
    for t in threaderList:
        t.start()
    print("total time: ", time.time()-time1)

    if bolt.color != black:
        bolt.fadeColor()
        index = 0
        while len(bolt.swayPoints) > index+1:
            pygame.draw.line(screen, bolt.color, [bolt.swayPoints[index][0],bolt.swayPoints[index][1]],[bolt.swayPoints[index+1][0],bolt.swayPoints[index+1][1]], bolt.thickness)#width=bolt.thickness
            index += 1
        for branch in bolt.branches:
            pygame.draw.line(screen, bolt.color, [branch[0],branch[1]],[branch[2],branch[3]], int(bolt.thickness/2))

    newElement = elementDropDown.createDropDown()
    newValue = elementValues.createDropDown()
    if newElement is not None:
        elementValues.items = list(dropDownDict[newElement])
        elementValues.defaultSelection = ddIndexValues[newElement]

    if newValue is not None:
        ddIndexValues[elementDropDown.items[elementDropDown.defaultSelection]] = elementValues.items.index(newValue)

        if ddIndexValues["Precipitation Type"] == 1:
            for indexku in range(len(dropletList)):
                for drop in dropletList[indexku]:
                    drop.isSnow = True
        if ddIndexValues["Precipitation Type"] == 0:
            for indexSu in range(len(dropletList)):
                for drop in dropletList[indexSu]:
                    drop.isSnow = False
                    drop.x = drop.xOrignal
            

if __name__ == '__main__':
    gameLoop()
    quit()