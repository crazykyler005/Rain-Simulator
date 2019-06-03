import random
import numpy

class Lightning:

    def __init__(self, window_x, window_y, addBranches = True):
        self.x = random.randrange(100, window_x-100)
        self.y = 0
        self.thickness = 7
        self.length = window_y
        self.screenWidth = window_x
        self.color = (0,0,0)
        self.swayPoints = []
        self.addBranches = addBranches
        self.branches = []*4

    def fadeColor(self, rate = 2):
        fadeValue = (-rate,-rate,-rate)
        self.color = tuple(numpy.add(self.color, fadeValue))
        if self.color[0] <=0:
            self.color = (0,0,0)

    def generateSwayPoints(self):

        swayXY = []
        ySway = self.y
        xSwayLimit = 30
        segmentMinLength = 45
        segmentMaxLength = 75
        while ySway <= self.length:
            
            swayXY.append([random.randrange(self.x-xSwayLimit,self.x+xSwayLimit),ySway])
            ySway += random.randrange(segmentMinLength,segmentMaxLength)

        swayXY.append([random.randrange(self.x-xSwayLimit,self.x+xSwayLimit),ySway])
        self.swayPoints = swayXY

        if self.addBranches:
            self.createBranches()
            self.extendBranches(self.branches, branchExtensions=3)
        else:
            self.branches = []*4

    def createBranches(self, maxBranches = 4):

        branchTotal = random.randrange(4,int(len(self.swayPoints)/2))
        xyMax = 100
        xyMin = 50
        branchNum = []
        index = 1
        branches = []

        while len(self.swayPoints) > index+1:
            branchNum.append(index)
            index += 1

        for i in range(branchTotal):

            branchValue = random.choice(branchNum)
            swayCoordinate = self.swayPoints[branchValue]
            if swayCoordinate[0] > self.swayPoints[branchValue - 1][0]:
                x = swayCoordinate[0] + random.randrange(xyMin,xyMax)
            #x = random.choice([swayCoordinate[0] + random.randrange(-xyMax,-xyMin),swayCoordinate[0] + random.randrange(xyMin,xyMax)])
            else:
                x = swayCoordinate[0] + random.randrange(-xyMax,-xyMin)

            y = swayCoordinate[1] + random.randrange(xyMin, xyMax)
            branches.append([swayCoordinate[0],swayCoordinate[1], x, y])
            branchNum.remove(branchValue)

        self.branches = branches

    def extendBranches(self, branchCoordinates, branchExtensions = 0):

        #branchTotal = 2
        branchTotal = random.randrange(1, len(branchCoordinates))
        branchNum = []
        newBranches = []
        xyMin = 50
        xyMax = 70

        for index in range(len(branchCoordinates)):
            branchNum.append(index)

        for i in range(branchTotal):

            branchValue = random.choice(branchNum)
            currentCoordinates = branchCoordinates[branchValue]
            
            for z in range(2):

                if currentCoordinates[0] < currentCoordinates[2]:
                    x = currentCoordinates[2] + random.randrange(xyMin, xyMax)
                else:
                    x = currentCoordinates[2] + random.randrange(-xyMax, -xyMin)
                
                if z == 0:
                    y = currentCoordinates[3] + random.randrange(-xyMax, -xyMin)
                else:
                    y = currentCoordinates[3] + random.randrange(xyMin, xyMax)

                branch = [currentCoordinates[2],currentCoordinates[3], x, y]
                newBranches.append(branch)
                self.branches.append(branch)
                #branchCoordinates.append(branch)

            branchNum.remove(branchValue)

        #print(newBranches)
        if branchExtensions > 0:
            self.extendBranches(newBranches, branchExtensions - 1)

    def resetPosition(self):

        self.x = random.randrange(100, self.screenWidth-100)

    def flashScreen(self):

        fadeValue = (-5,-5,-5)
        self.screenColor = tuple(numpy.add(self.screenColor, fadeValue))
        if self.color[0] <=0:
            self.color = (0,0,0)