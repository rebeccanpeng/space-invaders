#Rebecca Peng
#period 11- HCP
#Assignment: Final project
#Description: Space invaders

#---------- references ----------
# 1. ship png image
#space invaders by Made by Made from the Noun Project: Space invaders images found on 5/2/2018 at https://thenounproject.com/term/space-invaders/1175319/
# 2. bullet png image
#http://pngimg.com/uploads/bullets/bullets_PNG35574.png?i=1 found on 5/3/2018
# 3. bullet icon image
#https://www.iconfinder.com/icons/115169/bullets_gun_icon found on 5/20/18
# 4. freeze icon image
#https://www.iconfinder.com/icons/264356/christmas_cold_freeze_frost_frozen_snow_snowflake_vanished_vanishing_weather_winter_icon 5/20/18
# 5. explosion sound
# https://www.audiomicro.com/free-sound-effects/free-guns-and-weapons# found on 5/17/18
# 6. leaderboard code
# developed by me for my snake program
# 7. typing name code
# developed by me for my hangman program

import pygame, sys, math, random, copy

#initialize game engine
pygame.init()
clock = pygame.time.Clock()

#Set up drawing surface
w = 480
h = 640
size=(w,h)
surface = pygame.display.set_mode(size)

#set window title bar
pygame.display.set_caption("Space Invaders")

#Color constants
BLACK = (  0,  0,  0)
WHITE = (255,255,255)
RED =   (255,  0,  0)
GREEN = (  0,255,  0)
BLUE =  (  0,  0,255)

#images
shipImage = pygame.image.load("spaceship.png")
shipImage = pygame.transform.scale(shipImage, (70, 55))

bulletImage = pygame.image.load("bullet.png")
bulletImage = pygame.transform.scale(bulletImage, (10, 20))
flippedBulletImage = pygame.transform.rotate(bulletImage, 180)

monsterImage = pygame.image.load("monster1.png")
monsterImage = pygame.transform.scale(monsterImage, (25, 25))

backgroundImage = pygame.image.load("background.jpg")

explodeImage = pygame.image.load("explode.png")
explodeImage = pygame.transform.scale(explodeImage, (25, 25))

bulletIcon = pygame.image.load("bulletIcon.png")
bulletIcon = pygame.transform.scale(bulletIcon, (25, 25))
bulletIcon = pygame.transform.rotate(bulletIcon, 90)

freezeIcon = pygame.image.load("freezeIcon.png")
freezeIcon = pygame.transform.scale(freezeIcon, (25, 25))

#sound files
explosionSound = pygame.mixer.Sound("explosion.wav")
lonogExplosionSound = pygame.mixer.Sound("longExplosion.wav")


#controls speed of certain animations 
SPEED = 6

#-----------functions-----------------
'''
makes text ready to be displayed
'''
def showMessage(words, size, fontName, xVal, yVal, forecolor, bg=None):
    font = pygame.font.SysFont(fontName, size, False, False)
    text = font.render(words, True, forecolor, bg)
    #get a bounding rectangle for the text
    textBounds = text.get_rect()
    textBounds.center=(xVal, yVal)
    return text, textBounds

'''
draws just the grid/board part
'''
def drawBoard():
    x, y, = 0, 0 
    rWidth = w/20 #width of a row
    rHeight = w/20 #height of each row
    numRows = 0
    numCols = 0
    
    while y < h: #draw rows until the entire screen is filled
        pygame.draw.rect(surface, WHITE, (x, y, rWidth, rHeight), 1)
        
        #keep drawing columns of squares until the entire screen is filled
        if x + rWidth > w:
            x = 0
            y += rHeight
            numRows += 1 #counter to keep track of rows
        else:
            x += rWidth
            numCols += 1 #counter for columns
            
    numCols = int(numCols/numRows)
    board = []
    #empty 2d list using dimensions
    for i in range(numRows):
        board.append([0]*numCols)   
        
    return board

'''
makes sure player cannot leave playing surface
'''
def checkCollisions(player):
    if player.right >= w:
        player.right = w-1
    if player.left <= 0:
        player.left = 1
    if player.top <= 0:
        player.top = 1
    if player.bottom >= h:
        player.bottom = h-1
        
    return player

'''
moves the ship based on which way the user wants to move
'''
def moveShip(keys, player):
    if keys[pygame.K_LEFT]:
        player.left-= SPEED
        checkCollisions(player)
  
    if keys[pygame.K_RIGHT]:
        player.left+= SPEED
        checkCollisions(player)
      
    return player

'''
checks if a bullet shot by the user has hit an alien
'''
def checkShot(bullet, board, score):
    rWidth = w/len(board[0])
    rHeight = w/len(board)    
    x, y = 0, 0    
    alienDown = False #true if alien has been shot
    
    #loop through entire grid and check if the bullet has shot an alien
    for r in range(len(board)):
        for c in range(len(board[0])):            
            if board[r][c] == 1:
                if bullet.colliderect(x, y, rWidth, rHeight):
                    board[r][c] = 'z' #z denotes an explostion image
                    alienDown = True
                    score += 10 #10 points per alien
                    explosionSound.play()   
                    
            x += rWidth
        x = 0
        y += rHeight 
            
    return board, alienDown, score
 
'''
moves the bullet towards the top of the screen when the user presses space
'''
def shootBullet(ship, board, userBullets, score):
    
    for bullet in userBullets:
        
        if bullet.top > 0:
            bullet.top -= SPEED #keep moving the bullet up until it is stopped
            
            if bullet.top <= 0: #if the bullet reaches the top, remove the bullet
                userBullets.remove(bullet)
                
            board, alienDown, score = checkShot(bullet, board, score) #checks if bullet has hit an alien
            if alienDown: #if an alien is shot, remove the bullet
                if bullet in userBullets:
                    userBullets.remove(bullet)
        
    return userBullets, score

'''
randomly chooses an alien to shoot a bullet at the user
'''
def chooseAlienShooter(board, alienBullets):
    rWidth = w/len(board[0])
    rHeight = w/len(board)    
    x, y = 0, 0    
    
    #loop through entire grid and choose a random alien to shoot a bullet
    choiceR = random.randint(0, len(board)-1) #random row for an alien
    choiceC = random.randint(0, len(board[0])-1) #random column for an alien
    
    while board[choiceR][choiceC] != 1: #loop until the random row and column holds an alien
        choiceR = random.randint(0, len(board)-1)
        choiceC = random.randint(0, len(board[0])-1)        
        
    for r in range(len(board)):
        for c in range(len(board[0])): 
            if r == choiceR and c == choiceC:
                bullet = pygame.Rect(x, y, 10, 20)
                alienBullets.append(bullet) #add a bullet to the alien list at the randomly selected coordinates
                return alienBullets
                
            x += rWidth
        x = 0
        y += rHeight     
    
'''
'shoots' the alien bullets towards the bottom of the screen
'''
def shootAlienBullets(board, alienBullets, counter):
    
    for bullet in alienBullets:
        
        if bullet.bottom > 0:
            bullet.bottom += SPEED #keep moving the bullet down
            
            if bullet.bottom >= h: #if the bullet reaches the bottom of the screen, remove it
                alienBullets.remove(bullet)
                
    return alienBullets

'''
places the monster in a group at the top of the screen
'''
def placeMonsters(board, level):
    rows = level + 1 #total number of rows of aliens
    
    if level + 1 != len(board[0]): #makes sure num of aliens doesn't exceed the lenght of the board
        numAliens = level + 1 #number of aliens per row
    else:
        numAliens = len(board[0])-1
  
    monsterR = 1 #row number for aliens to start spawning at        
    
    while rows != 0: #blit aliens in an array for the number of specified rows
        for col in range(numAliens):
            board[monsterR][col] = 1
            
        rows -= 1
        monsterR += 1
         
    return board

'''
moves the monsters
'''
def moveMonsters(board, direction, moveDown):
    
    numCols = len(board[0])
    
    if moveDown == True:
        
        #gets last row
        lastRow=board.pop(-1)
        
        #inserts last row to top
        board.insert(0, lastRow)
        
        #stop the aliens from moving down after they've moved down one unit after hitting the sides
        moveDown = False
        
    else:
        
        if direction =='right':
            
            for row in board:
                
                #the last value of the list
                lastValue = row.pop(numCols-1)
                
                #inserts last value of the list and puts it to beginning of the list 
                row.insert(0, lastValue)
                
                if row[numCols-1]==1: #if alien reaches right side of screen and movement was to the right
                    moveDown=True
                    direction='left'        
                    
        elif direction=='left':
            
            for row in board:
                
                firstValue=row.pop(0)
                
                #insert first value into the end of the list
                row.insert(numCols-1, firstValue)  
                
                if row[0]==1: #if alien reaches left side of screen and movement was to the left
                    
                    moveDown=True
                    direction='right'
                
                
    return board, direction, moveDown
 
'''
checks the game status
'''
def checkGameOver(gameOver, win, lose, alienBullets, ship, board, level, direction):
    
    #check if the user has been hit by an alien's bullet
    for bullet in alienBullets:
        if bullet.colliderect(ship):
            gameOver = True
            lose = True
            
    #check if the user has hit all the aliens
    numAliens = 0
    for r in range(len(board)):
        for c in range(len(board[0])):
            if board[r][c] == 1:
                numAliens += 1
                
    if numAliens == 0: #if all the aliens have been shot, start over with new level
        level += 1
        direction = 'right'
        board = placeMonsters(board, level)    
        
    #check if any aliens have reached the bottom of the screen
    if 1 in board[len(board)-1]: #check if there are aliens in the last row
        gameOver = True
        lose = True
        
    return gameOver, win, lose, level, board, direction

'''
checks to see if the user's current score is the new high score
'''
def keepHiScore(score, hiScore):
    if score>hiScore:
        hiScore = score

    return hiScore

'''
checks validity of a letter the user has typed
'''
def isValidLetter(letterEntered):
    #letter out of range a-z
    if letterEntered.lower() > 'z' or letterEntered.lower() < 'a':
        return False

    return True #letter is valid
    
'''
makes the leaderboard
'''
def makeHiList():
    inFile = open("highScores.txt", 'r') #leaderboard file
    hiDict = {}

    for line in inFile:
        if len(line) == 0:
            break
        #takes line from file, strips off \n, splits into a list, adds to dictionary
        data = line.strip().split(', ')
        name = data[0]
        hiScore = data[1:]
        hiScore = int(hiScore[0])
        
        if name in hiDict: #if the name is already on the leaderboard, append the score to a list
            hiDict[name].append(hiScore)
            
        else: #if the name is new, make the score a list
            hiDict[name] = [hiScore]
          
    names = hiDict.keys()
    hiScores = [] #all high scores in one list
    for highList in hiDict.values():
        for highScore in highList:
            hiScores.append(highScore)  
          
    hiScores = sorted(hiScores) #put the scores in order

    while len(hiScores) > 5: #only want the top 5 on the leaderboard
        
        #if the leaderboard has more than 5 scores, loop and delete lowest score until there are only 5 
        for highScore in hiScores:
            for name in names:
                if hiScores[0] in hiDict[name]: 
                    hiDict[name].remove(min(hiDict[name]))
                    hiScores.remove(highScore)
                   
                    break
            break
        
          
    return hiDict, hiScores
        
'''
adds a new high score to the txt file
'''
def addScore(name, score):
    outFile = open("highScores.txt", 'a')
    outFile.write('\n' + name + ", " + str(score))
    outFile.close()

'''
checks to see if the user made it onto the leaderboard (if they are in the top 5)
'''
def checkHiScore(score, hiDict, hiScores):
    orderedHiScores = sorted(hiScores) #the scores sorted from lowest to highest 
    
    if score > int(orderedHiScores[0]): #if the score is greater than the lowest score on the leaderboard, they made it
        return True
    
    if len(orderedHiScores)<5:
        return True
    
    return False

'''
chooses a random location to drop a power up from
'''
def choosePowerLoc(board, powerList):
    rWidth = w/len(board[0])
    rHeight = w/len(board)    
    x, y = 0, 0    
    
    choiceC = random.randint(0, len(board[0])-1) #random column to drop powerup from
   
    #loop through entire board and add the rect for a powerup into a list
    for r in range(len(board)):
        for c in range(len(board[0])): 
            if c == choiceC:
                powerUp = pygame.Rect(x, y, 10, 20)
                powerList.append(powerUp)
                return powerList
                
            x += rWidth
        x = 0
        y += rHeight     
  
'''
drop power ups from the top of the screen to the bottom
'''
def dropPowerUps(powerList, board):
    for powerUp in powerList:
        
        if powerUp.bottom > 0:
            powerUp.bottom += SPEED*1.5 #drop the powerup at a slightly faster speed than the bullets
            
            if powerUp.bottom >= h: #if it reaches the bottom without being caught, remove it from the list
                powerList.remove(powerUp)
                
    return powerList        
    
'''
check if the user has caught the power up
'''
def checkCaughtPower(powerList, ship, caughtPower):
    for powerUp in powerList:
        if powerUp.colliderect(ship):
            caughtPower = True
      
    return caughtPower

'''
blits the directions onto the screen
'''
def drawDirections(showDirections):
    if showDirections:
        pygame.draw.rect(surface, BLACK, (w/10, h/10, w*4/5, h*4/5), 0) #colored rectangle background for all the directions
        moveText, moveBounds = showMessage("Use your arrow keys to move the ship left and right.", 15, 'Calibri', w/2, h*20/100, WHITE)
        shootText, shootBounds = showMessage("Press space to shoot (you can only shoot one bullet at a time!)", 15, 'Calibri', w/2, h*25/100, WHITE)
        surface.blit(moveText, moveBounds)
        surface.blit(shootText, shootBounds)
        
        #powerup section 
        powerText, powerBounds = showMessage("Catch some power ups!", 17, "Calibri", w/2, h*35/100, WHITE)
        surface.blit(powerText, powerBounds)
        
        surface.blit(bulletIcon, (w*20/100, h*40/100))
        bulletText, bulletBounds = showMessage(" = automatic continuous shooting", 15, "Calibri", w/2, h*42/100, WHITE)
        surface.blit(bulletText, bulletBounds)
        
        surface.blit(freezeIcon, (w*20/100, h*50/100))
        freezeText, freezeBounds = showMessage(" = freeze the aliens", 15, "Calibri", w*5/12, h*52/100, WHITE)
        surface.blit(freezeText, freezeBounds)
        
        closeText, closeBounds = showMessage("Press / (forward slash) to close this window", 15, "Calibri", w/2, h*60/100, WHITE)
        orText, orBounds = showMessage("(or to reference this window at any time during the game)", 15, "Calibri", w/2, h*63/100, WHITE)
        surface.blit(closeText, closeBounds)
        surface.blit(orText, orBounds)
   
'''
blits all the text on the screen
'''
def drawText(win, lose, gameOver, score, hiScore, hiDict, hiScores, inputName, nameSubmitted, level, playAgain, counter):
     
    #text that is always on the screen
    scoreText, scoreBounds = showMessage(" Current score: " + str(score) + " ", 15, "Calibri", w*15/100, h/50, BLACK, WHITE)
    surface.blit(scoreText, scoreBounds)
    
    hiScoreText, hiScoreBounds = showMessage(" High score: " + str(hiScore) + " ", 15, "Calibri", w*85/100, h/50, BLACK, WHITE)
    surface.blit(hiScoreText, hiScoreBounds)  
    
    levelText, levelBounds = showMessage(" Level " + str(level) + ' ', 15, "Calibri", w/2, h/50, BLACK, WHITE)
    surface.blit(levelText, levelBounds)
    
    #text that is sometimes on the screen      
    highTitle, highTitleBounds = showMessage("High scores:", 20, "Calibri", w*4/16, h*7/16, BLACK)    
    highText, highBounds = showMessage("Congratulations you got onto the leaderboard!", 20, "Calibri", w/2, h*4/16, GREEN, BLACK)
    inputnameText, inputnameBounds = showMessage("Enter your name: " + inputName, 20, "Calibri", w/2, h*5/16, GREEN, BLACK)
    loseText, loseBounds = showMessage("You lose", 30, "Calibri", w/2, h/5, GREEN, BLACK)
    againText, againBounds = showMessage("Press 1 to play again", 30, "Calibri", w/2, h*7/8, GREEN, BLACK)
    enterText, enterBounds = showMessage("Press enter when done typing your name", 15, "Calibri", w/2, h*6/16, GREEN, BLACK)

    if gameOver:
        
        if lose:
            surface.blit(loseText, loseBounds) 
            
        surface.blit(againText, againBounds)
        
        pygame.draw.rect(surface, GREEN, (w/8, h*13/32, w*3/4, h*7/16), 0) #background for leaderboard        
        surface.blit(highTitle, highTitleBounds)              
        
        #if the user made it onto the leaderboard
        if checkHiScore(score, hiDict, hiScores):
            surface.blit(highText, highBounds)
            if not nameSubmitted:
                surface.blit(inputnameText, inputnameBounds) #prompts the user to type their name
                surface.blit(enterText, enterBounds)
       
        orderedHiScores = sorted(hiScores, reverse = True) #the scores sorted from highest to lowest
        
        tempHiDict = copy.deepcopy(hiDict) #make a copy of the hiDict to be manipulated
        names = tempHiDict.keys()
   
        listTop = h/2 #the height where the list begins

        for highScore in orderedHiScores:
            highScoreText, highScoreBounds = showMessage(str(highScore), 15, "Calibri", w*3/4, listTop, BLACK)
            surface.blit(highScoreText, highScoreBounds) #displays all of the scores on the leaderboard
            
            for name in names:
                
                if highScore in tempHiDict[name]: #finds the name associated with the current high score being looped through
                    nameText, nameBounds = showMessage(name, 15, "Calibri", w/4, listTop, BLACK)
                    surface.blit(nameText, nameBounds)  
                    
                    tempHiDict[name].remove(highScore) #remove the score that was just displayed
                  
                    listTop += h/16 #moves the next line of the leaderboard down
                    break #continue onto the next score so that multiple names are not displayed for the same score
     
'''
draws graphic aspect of surface
'''           
def drawScreen(board, ship, originalBullet, userBullets, alienBullets, gameOver, counter, shootPowerList, freezePowerList):
    surface.fill(WHITE)
    surface.blit(backgroundImage, (0, 0))
        
    if not gameOver:
        surface.blit(shipImage, ship)
    
        #only blit bullet at top of ship when no bullets are currently traveling
        if len(userBullets) == 0:
            surface.blit(bulletImage, originalBullet)
    
        for bullet in userBullets:
            surface.blit(bulletImage, bullet)
            
        for bullet in alienBullets:
            surface.blit(flippedBulletImage, bullet)
            
        for powerUp in shootPowerList:
            surface.blit(bulletIcon, powerUp)
            
        for powerUp in freezePowerList:
            surface.blit(freezeIcon, powerUp)

    rWidth = w/len(board[0])
    rHeight = h/len(board)    
    x, y = 0, 0
    
    for r in range(len(board)):
        for c in range(len(board[0])):
       
            if board[r][c] == 1:
                surface.blit(monsterImage, (x, y, rWidth, rHeight))
                
            if board[r][c] == 'z':
                surface.blit(explodeImage, (x, y, rWidth, rHeight))
                if counter%30 == 0: #temporarily blit an explosion image
                    board[r][c] = 0
                
            x += rWidth
        x = 0
        y += rHeight
        
#----------Main Program Loop ----------

def main():
    level = 1 #level of the game
    ship =  pygame.Rect(w/6, h*44/50, 70, 55) #location (rect) of the ship
    originalBullet = pygame.Rect(ship.centerx - (bulletImage.get_width())/2, ship.top,10, 20) #one bullet at the top of the ship
    board = drawBoard() 
    board = placeMonsters(board, level) 
    
    direction = 'right' #direction the aliens are moving
    moveDown=False  #determines if aliens should move down
    
    #lists of moving objects
    userBullets = []
    alienBullets = []
    shootPowerList = []
    freezePowerList = []
    
    counter = 0 #helps control animation speed of different aspects
    
    #boolean variables for controlling gameplay
    gameOver = False
    win = False
    lose = False
    playAgain = False
    bulletFired = False    
    caughtShootPower = False
    caughtFreezePower = False
    
    #score/high score variables
    score = 2000
    hiDict, hiScores = makeHiList()
    hiScore = int(max(hiScores))
    inputName = ""
    letterEntered = ""
    nameSubmitted = False   
    showDirections = True
    
    while(True):
        keys = pygame.key.get_pressed() #get all keys pressed for ship movement
        counter += 1 #help control animation of certain objects
        
        for event in pygame.event.get():
            if( event.type==pygame.QUIT or (event.type==pygame.KEYDOWN and event.key == pygame.K_ESCAPE)):
                pygame.quit()
                sys.exit()
                
            if not gameOver:   
                if not caughtShootPower: #if the user does not have the power up
                    if len(userBullets)<1: #only shoot one bullet at a time  
                        if event.type == pygame.KEYDOWN:
                            if event.key == pygame.K_SPACE: #press space to shoot bullet
                                userBullets.append(originalBullet)
                      
            if event.type == pygame.KEYDOWN: 
                if event.key == pygame.K_SLASH: #press forward slash for directions (and to close directions)
                    if showDirections == True:
                        showDirections = False
                    else:
                        showDirections = True
                
                if not showDirections:    
                    if gameOver:     
                        if event.key == pygame.K_1: #press 1 to play again
                            playAgain = True
                        
                        if checkHiScore(score, hiDict, hiScores):       
                            
                            if not nameSubmitted:
                                #if the user made it onto the leaderboard and the game is over, let them enter their name   
                                letterEntered = (event.unicode).lower() #gets letter typed
                                               
                                if isValidLetter(letterEntered) and len(inputName)<20:
                                    inputName += letterEntered
                                    
                                if event.key == pygame.K_BACKSPACE: #backspace functionality
                                    inputName = inputName[:len(inputName)-1]
                                    
                                if event.key == pygame.K_RETURN: #enter = user done typing name
                                    addScore(inputName, score)
                                    inputName = ""
                                    nameSubmitted = True
                                    
                                hiDict, hiScores = makeHiList() #make the leaderboard

        #--------game logic goes here---------------
        if playAgain: #reset all variables if the user is playing again
            
            level = 1 #level of the game
            ship =  pygame.Rect(w/6, h*44/50, 70, 55) #location (rect) of the ship
            originalBullet = pygame.Rect(ship.centerx - (bulletImage.get_width())/2, ship.top,10, 20) #one bullet at the top of the ship
            board = drawBoard() 
            board = placeMonsters(board, level) 
            
            direction = 'right' #direction the aliens are moving
            moveDown=False  #determines if aliens should move down
            
            #lists of moving objects
            userBullets = []
            alienBullets = []
            shootPowerList = []
            freezePowerList = []
            
            counter = 0 #helps control animation speed of different aspects
            
            #boolean variables for controlling gameplay
            gameOver = False
            win = False
            lose = False
            playAgain = False
            bulletFired = False    
            caughtShootPower = False
            caughtFreezePower = False
            
            #score/high score variables
            score = 0
            hiDict, hiScores = makeHiList()
            hiScore = int(max(hiScores))
            inputName = ""
            letterEntered = ""
            nameSubmitted = False   
            
        if not gameOver and not showDirections: #during gameplay
            #moves the ship based on the keys the user has pressed    
            ship = moveShip(keys, ship)
            #one bullet is always at the top of the ship
            originalBullet = pygame.Rect(ship.centerx - (bulletImage.get_width())/2, ship.top,10, 20)                 
            #shoots a bullet using the list of bullets the user has shot
            userBullets, score = shootBullet(ship, board, userBullets, score)            
        
            if not caughtFreezePower: #if the aliens are not frozen
                if counter % 20 == 0: #controls speed of alien movement
                    board, direction, moveDown = moveMonsters(board, direction, moveDown)
            
            if not caughtFreezePower: #if the aliens are not frozen      
                if counter%100 == 0: #controls speed of having an alien shoot at the user
                    alienBullets = chooseAlienShooter(board, alienBullets)
            
            #shoot bullets from the aliens    
            alienBullets = shootAlienBullets(board, alienBullets, counter)
            
            if not caughtShootPower: #only spawn power ups when the user does not currently have one
                
                if counter%500 == 0 and counter != 0: #controls speed of dropping a power up
                    shootPowerList = choosePowerLoc(board, shootPowerList)
                    
            if caughtShootPower:
                
                if counter%3 == 0:
                    userBullets.append(originalBullet) #automatic continuous shooting
                    
                if counter%100 == 0:
                    caughtShootPower = False    
                    
            shootPowerList = dropPowerUps(shootPowerList, board)
            caughtShootPower = checkCaughtPower(shootPowerList, ship, caughtShootPower)  
            
            if not caughtFreezePower: #only spawn powerup if not currently using one
                
                if counter%700 == 0 and counter != 0:
                    freezePowerList = choosePowerLoc(board, freezePowerList)
                    
            if caughtFreezePower:
                
                if counter%500 == 0:
                    caughtFreezePower = False
                
            freezePowerList = dropPowerUps(freezePowerList, board)
            caughtFreezePower = checkCaughtPower(freezePowerList, ship, caughtFreezePower)        
        
        gameOver, win, lose, level, board, direction = checkGameOver(gameOver, win, lose, alienBullets, ship, board, level, direction)
        hiScore = keepHiScore(score, hiScore)
        
        #draws the entire screen
        drawScreen(board, ship, originalBullet, userBullets, alienBullets, gameOver, counter, shootPowerList, freezePowerList)
        drawText(win, lose, gameOver, score, hiScore, hiDict, hiScores, inputName, nameSubmitted, level, playAgain, counter)
        drawDirections(showDirections)
        
        pygame.display.update()
        
        #controls animation speed
        clock.tick(60)
        
main()

