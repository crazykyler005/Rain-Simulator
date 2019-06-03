import random

class droplet:

    def __init__(self, width_spacing, isSnow = False): #intensity
        #self.intensity = intensity
        self.isSnow = isSnow
        self.maxRanHeight = -250
        self.minRanHeight = -50
        self.width = 4
        self.height = 20
        self.x = self.width * width_spacing
        self.xOrignal = self.x
        self.y = random.randrange(self.maxRanHeight,self.minRanHeight)
        self.speed = 0.5
        self.windSpeed = 0
        self.swaySpeed = random.choice([-0.3, 0.3])
        
    def increaseDropSpeed(self, dropRate=0.05, maxSpeed = 9.8):

        #apply x direction change when on screen
        if (self.y-self.height > 0) and (self.windSpeed is not 0):
            self.x += self.windSpeed

        if not self.isSnow:

            if self.speed < maxSpeed:
                self.speed += self.speed*dropRate
            elif self.speed > maxSpeed:
                self.speed = 9.8
            self.y += self.speed

        else:
            self.snowFallSway()

    def snowFallSway(self, snowSpeed=2, dropRate = 0.05):

        if (self.x-self.xOrignal > 4) or (self.x-self.xOrignal < -4):
            self.swaySpeed *= -1
            self.x += self.swaySpeed
        else:
            self.x += self.swaySpeed

        self.y += snowSpeed

    def resetSpeed(self, originalX):
        self.speed = 0.5
        self.y = random.randrange(self.maxRanHeight,self.minRanHeight)
        self.x = originalX