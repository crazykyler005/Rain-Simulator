import pygame

class button:

    def __init__(self, screen, msg, x, y, w, h):

        self.screen = screen
        self.x = x
        self.y = y
        self.w = w
        self.h = h
        self.msg = msg

    def text_objects(self, text, font):
        textSurface = font.render(str(text), True, (0,0,0))
        return textSurface, textSurface.get_rect()

    def button(self, msg, x, y, w, h):

        mouse = pygame.mouse.get_pos()
        color = self.inactColor
        returnValue = None

        if x+w > mouse[0] > x and y+h > mouse[1] > y:
            color = self.actColor
            #if leftclick has been pressed
            if pygame.mouse.get_pressed()[0] == 1:
                returnValue = msg

        pygame.draw.rect(self.screen, color, [x, y, w, h])

        smallText = pygame.font.Font(None,20)
        textSurf, textRect = self.text_objects(msg, smallText)
        textRect.center = ( (x+(self.width/2)), (y+(self.height/2)) )
        self.screen.blit(textSurf, textRect)

        return(returnValue)


class dropDownMenu:

    def __init__(self, x, y, width, height, items, window, imageLocation ="dropDown.png", inactColor = (0, 255, 0), actColor = (0, 200, 0)):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.inactColor = inactColor
        self.actColor = actColor
        self.imageLocation = imageLocation
        self.items = items
        self.imageRotated = False
        self.defaultSelection = 0
        self.isActive = False
        self.screen = window

    def text_objects(self, text, font):
        textSurface = font.render(str(text), True, (0,0,0))
        return textSurface, textSurface.get_rect()

    def button(self, msg, x, y, w, h):

        mouse = pygame.mouse.get_pos()
        color = self.inactColor
        returnValue = None

        if x+w > mouse[0] > x and y+h > mouse[1] > y:
            color = self.actColor
            #if leftclick has been pressed
            if pygame.mouse.get_pressed()[0] == 1:
                returnValue = msg

        pygame.draw.rect(self.screen, color, [x, y, w, h])

        smallText = pygame.font.Font(None,20)
        textSurf, textRect = self.text_objects(msg, smallText)
        textRect.center = ( (x+(self.width/2)), (y+(self.height/2)) )
        self.screen.blit(textSurf, textRect)

        return(returnValue)

    def createDropDown(self):

        #if dropDownButton is clicked or has been clicked on previously
        if (self.button(self.items[self.defaultSelection], self.x, self.y, self.width, self.height) != None) or self.isActive:
            self.isActive = True
            index = 0
            for item in self.items:
                if item == self.items[self.defaultSelection]:
                    continue
                index += 1

                if self.button(item, self.x, self.y+self.height*index, self.width, self.height) != None:
                    self.isActive = False
                    self.defaultSelection = self.items.index(item)
                    return(item)

        return(None)