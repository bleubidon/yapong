import pygame, time
from random import randint,random
from math import sqrt

pygame.init()

###INIT BEGIN###
# Window Parameters
displayWidth = 800
displayHeight = 600
fps = 250

greenScore, blueScore = 0, 0

# Colours Definition
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (50, 50, 255)
grey = (100, 100, 130)


###INIT END###

def message(textContent, textColor, textSize, textPos):
    font = pygame.font.Font(None, textSize)
    text = font.render(textContent, 1, textColor)
    textPos = textPos
    return text, textPos


def grantGreen(greenScore, blueScore):
    greenScore += 1
    return greenScore


def grantBlue(greenScore, blueScore):
    blueScore += 1
    return blueScore


gameDisplay = pygame.display.set_mode((displayWidth, displayHeight))
gameDisplay.fill(black)

pygame.display.set_caption('==PyPong==')
clock = pygame.time.Clock()

startTime = time.time()

##Main Loop
gameEnded = False
while not gameEnded:
    # Game Parameters
    gameOver = False

    # GamePlay Parameters
    # Players
    pl1XPos = 0
    pl1YPos = displayHeight / 2 - 75
    pl1Direction = 'none'

    pl2XPos = displayWidth - 15
    pl2YPos = displayHeight / 2 - 75
    pl2Direction = 'none'

    # Ball
    ballXPos = pl1XPos + 15 + 8
    ballYPos = pl1YPos + 75

    xSpeed, ySpeed = random(), random()*2-1
    mag=sqrt(xSpeed**2+ySpeed**2)/3;xSpeed/=mag;ySpeed/=mag
    speedIncr = 10
    speedAtt = .999

    while not gameOver:
        xSpeed = max(abs(xSpeed), 2) * abs(xSpeed) / float(xSpeed)
        # print('X: {}; Y: {} || Pl2X: {}; Pl2Y: {};;'.format(round(ballXPos), round(ballYPos), pl2XPos, pl2YPos))

        gameDisplay.fill(black)
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                gameEnded, gameOver = True, True

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP: pl1Direction = 'up'
                if event.key == pygame.K_DOWN: pl1Direction = 'down'

            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_UP and pl1Direction == 'up': pl1Direction = 'none'
                if event.key == pygame.K_DOWN and pl1Direction == 'down': pl1Direction = 'none'

        # Pl2 Move Computing
        # print('ballY: {}; pl2Y: {};;'.format(ballYPos, pl2YPos + 75))
        if ballYPos >= pl2YPos + 75:
            pl2Direction = 'down'
            #pl1Direction = 'down'
        else:
            pl2Direction = 'up'
            #pl1Direction = 'up'

        # Players Move Handling
        if pl1Direction == 'up' and pl1YPos > 0:
            pl1YPos -= 4
        elif pl1Direction == 'down' and pl1YPos < displayHeight - 150:
            pl1YPos += 4

        if pl2Direction == 'up' and pl2YPos > 0:
            pl2YPos -= 2
        elif pl2Direction == 'down' and pl2YPos < displayHeight - 150:
            pl2YPos += 2

        # Ball Borders Handling
        if (ballXPos < pl1XPos + 15 + 8 and ballYPos > pl1YPos and ballYPos < pl1YPos + 150) or (
                            ballXPos > pl2XPos - 8 and ballYPos > pl2YPos and ballYPos < pl2YPos + 150):
            xSpeed *= 1.8
            xSpeed *= -1
            ySpeed+=random()*2
            xSpeed = min(abs(xSpeed), 10) * abs(xSpeed) / float(xSpeed)
        elif ballXPos < pl1XPos + 15 + 8:
            gameOver = True
            blueScore = grantBlue(greenScore, blueScore)
        elif ballXPos > pl2XPos - 8:
            gameOver = True
            greenScore = grantGreen(greenScore, blueScore)

        if (ballYPos <= 8 and ySpeed < 0) or (ballYPos > displayHeight - 8 and ySpeed > 0):
            ySpeed *= -1

        xSpeed *= speedAtt
        ySpeed *= speedAtt

        ballXPos += xSpeed
        ballYPos += ySpeed

        ## Displaying
        # Scenery
        pygame.draw.line(gameDisplay, grey, (0, displayHeight / 2), (displayWidth, displayHeight / 2), 4)
        pygame.draw.line(gameDisplay, grey, (displayWidth / 2, 0), (displayWidth / 2, displayHeight), 4)
        pygame.draw.circle(gameDisplay, grey, (round(displayWidth / 2), round(displayHeight / 2)), 50, 4)

        # Players
        pygame.draw.rect(gameDisplay, green, (pl1XPos, pl1YPos, 15, 150))
        pygame.draw.rect(gameDisplay, blue, (pl2XPos, pl2YPos, 15, 150))

        # Ball
        pygame.draw.circle(gameDisplay, red, (round(ballXPos), round(ballYPos)), 8)

        # Score Displaying
        text, textPos = message('{} | {}'.format(greenScore, blueScore), red, 76,
                                (displayWidth / 2 - 49, displayHeight / 30))
        gameDisplay.blit(text, textPos)

        pygame.display.set_caption(
            '==*PyPong*== FPS : {} || Play Time : {}'.format(round(clock.get_fps()), round(time.time() - startTime, 2)))
        pygame.display.update()
        clock.tick(fps)

print('Game Over ! Lasted {} sec(s); Score: {} | {}'.format(round(time.time() - startTime, 2), greenScore, blueScore))
pygame.quit()