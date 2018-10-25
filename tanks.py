import pygame
import random

#explosion_sound = pygame.mixer.Sound('explosion-01.wav')
#pygame.mixer.music.load('explosion-01.wav')
#pygame.mixer.music.play(-1)
pygame.init()
clock = pygame.time.Clock()
white = (255,255,255)
black = (0,0,0)
red = (177,25,0)
lightRed = (255,0,0)
green = (0,155,0)
lightGreen = (0,255,0)
blue = (0,0,255)
yellow = (200,200,0)
lightYellow = (255,255,0)
greyBlue = (155,155,255)
brown = (100,80, 0)

display_width= 800
display_height= 600
tankWidth = 40
tankHeight = 20
turretWidth = 5
wheelWidth  = 5
groundHeight = 35

tanksBackground = pygame.image.load('MyFirstPaint.png')



gameDisplay = pygame.display.set_mode((display_width,display_height))
pygame.display.set_caption("Tanks")

smallfont = pygame.font.SysFont("comicsansms", 25, bold= False, italic= True)
mediumfont = pygame.font.SysFont("comicsansms", 50, bold= False, italic= False)
largefont = pygame.font.SysFont("comicsansms", 100, bold= False, italic= False)
def text_object(text, color, font_size):
    if font_size == 'small':
        textSurf = smallfont.render(text, True, color)
    if font_size == 'medium':
        textSurf = mediumfont.render(text, True, color)
    if font_size == 'large':
        textSurf = largefont.render(text, True, color)
    textRect = textSurf.get_rect()
    return textSurf, textRect
def message_to_screen(text, color, y_coordinate, font_size='small'):
    textSurf, textRect = text_object(text, color, font_size)
    textRect.center = display_width/2, display_height/2 + y_coordinate
    gameDisplay.blit(textSurf, textRect)
def text_to_button(text, color, button_position_and_size_list, font_size= 'small'):
    textSurf, textRect = text_object(text, color, font_size)
    textRect.center = button_position_and_size_list[0]+((button_position_and_size_list[2])/2), button_position_and_size_list[1]+((button_position_and_size_list[3])/2)
    gameDisplay.blit(textSurf, textRect)

def button(text, inactive_color, active_color, but_position, text_color= black, action = None):
    global control
    cur = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    if but_position[0]+but_position[2]> cur[0] > but_position[0] and but_position[1]+but_position[3] > cur[1] > but_position[1]:
        pygame.draw.rect(gameDisplay, active_color, but_position)
        if click[0] == 1 and action != None :
            if action == "play":
                gameLoop()
            if action == "control":
                gamecontrol()
            if action == "quit":
                pygame.quit()
                quit()
            #if action == "main":
             #   gameintro()
    else:
        pygame.draw.rect(gameDisplay, inactive_color, but_position)
    text_to_button(text, text_color, but_position)

def gamecontrol():
    control = True

    while control:
        gameDisplay.fill(greyBlue)
        message_to_screen("CONTROLS", red, y_coordinate=-200, font_size='large')
        message_to_screen("Fire : spacebar", green, -30)
        message_to_screen("Tank Movement : up and down arrows", green, 10)
        message_to_screen("Turret Movement : left and right arrows", green, 50)
        message_to_screen("Pause : p", green, 90)

        button("Play", green, lightGreen, (150,500,100,50), action="play")
        #button("Main", yellow, lightYellow, (350,500,100,50), action="main")
        button("Quit", red, lightRed,(550,500,100,50), action="quit")

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        clock.tick(15)

def enemy_tank(x, y, turPos):
    x = int(x)
    y = int(y)
    possible_Turret_pos = [(x+27, y-2), (x+25, y-5), (x+23, y-7), (x+20, y-11), (x+18, y-15),
                           (x+15, y-19), (x+13, y-20), (x+10, y-21), (x+8, y-22)]
    pygame.draw.circle(gameDisplay, black, (x, y), int(tankHeight/2))
    pygame.draw.rect(gameDisplay, black, (x- (tankWidth/2), y, tankWidth, tankHeight))
    pygame.draw.line(gameDisplay, black, (x, y), possible_Turret_pos[turPos], turretWidth)
    for z in range(15,-16,-5):
        pygame.draw.circle(gameDisplay, black, (x-z, y+20), wheelWidth)
    return possible_Turret_pos[turPos]

def tank(x, y, turPos):
    x = int(x)
    y = int(y)
    possible_Turret_pos = [(x-27, y-2), (x-25, y-5), (x-23, y-7), (x-20, y-11), (x-18, y-15),
                           (x-15, y-19), (x-13, y-20), (x-10, y-21), (x-8, y-22)]
    possible_enemy_Turret_pos = [(x - 27, y - 2), (x - 25, y - 5), (x - 23, y - 7), (x - 20, y - 11), (x - 18, y - 15),
                           (x - 15, y - 19), (x - 13, y - 20), (x - 10, y - 21), (x - 8, y - 22)]
    pygame.draw.circle(gameDisplay, black, (x, y), int(tankHeight/2))
    pygame.draw.rect(gameDisplay, black, (x- (tankWidth/2), y, tankWidth, tankHeight))
    pygame.draw.line(gameDisplay, black, (x, y), possible_Turret_pos[turPos], turretWidth)
    for z in range(15,-16,-5):
        pygame.draw.circle(gameDisplay, black, (x-z, y+20), wheelWidth)
    return possible_Turret_pos[turPos]

def barrier(barrierx, barrierHeight, barrierWidth):
    pygame.draw.rect(gameDisplay, black, (barrierx, display_height-barrierHeight, barrierWidth, barrierHeight))

def fireShell(XnY, currentTurPos, gun_power, barrierx, barrierWidth, barrierHeight, etankX, etankY):
    fire = True
    damage = 0
    startingShell = list(XnY)
    while fire:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        pygame.draw.circle(gameDisplay, red, (startingShell[0], startingShell[1]), 5)
        startingShell[0] -= (12 - currentTurPos) * 2

        startingShell[1] += int((((startingShell[0]-XnY[0])*0.015/(gun_power/50.0))**2) - (currentTurPos*1.8 + currentTurPos/(12-currentTurPos) ) )
        if startingShell[1] > display_height-groundHeight:
            hit_x = int((startingShell[0]/(display_height-groundHeight))*startingShell[1])
            hit_y = int(startingShell[1])
            explosion(hit_x, hit_y)
            if etankX + 10 > hit_x > etankX - 10 :
                damage = 25
                print("critical Hit!")
            elif etankX + 15 > hit_x > etankX - 15:
                damage = 20
                print("Hard Hit!")
            elif etankX + 25 > hit_x > etankX - 25:
                damage = 15
                print("good Hit!")
            elif etankX + 35 > hit_x > etankX - 35:
                damage = 5
                print("Light Hit!")
            fire = False
        check_x1 = startingShell[0] <= barrierx + barrierWidth
        check_x2 = startingShell[0] >= barrierx

        check_y1 = startingShell[1] <= display_height
        check_y2 = startingShell[1] >= display_height -barrierHeight

        if check_x1 and check_x2 and check_y1 and check_y2:
            hit_x = int(startingShell[0] )
            hit_y = int(startingShell[1])
            explosion(hit_x, hit_y)
            fire = False
        clock.tick(40)
        pygame.display.update()
    return damage

def e_fireShell(XnY, currentTurPos, gun_power, barrierx, barrierWidth, barrierHeight, ptankX, ptankY):

    currentPower = 1
    damage = 0
    powerFound = False
    while not powerFound:
        currentPower += 1
        if currentPower > 100:
            powerFound =True

        fire = True
        startingShell = list(XnY)
        while fire:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    quit()

            #pygame.draw.circle(gameDisplay, red, (startingShell[0], startingShell[1]), 5)
            startingShell[0] += (12 - currentTurPos) * 2
            Egun_power = random.randrange(int(currentPower*0.9), int(currentPower*1.1))
            startingShell[1] += int((((startingShell[0] - XnY[0]) * 0.015 / (Egun_power / 50.0)) ** 2) - (currentTurPos * 1.8 + currentTurPos / (12 - currentTurPos)))
            if startingShell[1] > display_height - groundHeight:
                hit_x = int((startingShell[0] / (display_height - groundHeight)) * startingShell[1])
                hit_y = int(startingShell[1])
                #explosion(hit_x, hit_y)
                if ptankX+15> hit_x > ptankX-15:
                    print("Target acquired!")
                    powerFound = True
                fire = False
            check_x1 = startingShell[0] <= barrierx + barrierWidth
            check_x2 = startingShell[0] >= barrierx

            check_y1 = startingShell[1] <= display_height
            check_y2 = startingShell[1] >= display_height - barrierHeight

            if check_x1 and check_x2 and check_y1 and check_y2:
                hit_x = int(startingShell[0])
                hit_y = int(startingShell[1])
                #explosion(hit_x, hit_y)
                fire = False


    fire = True
    startingShell = list(XnY)
    while fire:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()

        pygame.draw.circle(gameDisplay, red, (startingShell[0], startingShell[1]), 5)
        startingShell[0] += (12 - currentTurPos) * 2

        startingShell[1] += int((((startingShell[0] - XnY[0]) * 0.015 / (Egun_power / 50.0)) ** 2) - (
                currentTurPos * 1.8 + currentTurPos / (12 - currentTurPos)))
        if startingShell[1] > display_height - groundHeight:
            hit_x = int((startingShell[0] / (display_height - groundHeight)) * startingShell[1])
            hit_y = int(startingShell[1])
            explosion(hit_x, hit_y)
            if ptankX + 10 > hit_x > ptankX - 10 :
                damage = 25
            elif ptankX + 15 > hit_x > ptankX - 15:
                damage = 20
            elif ptankX + 25 > hit_x > ptankX - 25:
                damage = 15
            elif ptankX + 35 > hit_x > ptankX - 35:
                damage = 5
            fire = False
        check_x1 = startingShell[0] <= barrierx + barrierWidth
        check_x2 = startingShell[0] >= barrierx

        check_y1 = startingShell[1] <= display_height
        check_y2 = startingShell[1] >= display_height - barrierHeight

        if check_x1 and check_x2 and check_y1 and check_y2:
            hit_x = int(startingShell[0])
            hit_y = int(startingShell[1])
            explosion(hit_x, hit_y)
            fire = False
        clock.tick(40)
        pygame.display.update()

    return damage



def explosion(x, y, size=50):
    #pygame.mixer.Sound.play(explosion_sound)
    explode= True
    while explode:
        colorChoice = [red, lightRed, yellow, lightYellow]
        magnitude = 1
        while magnitude < size:
            exploding_bit_x = x + random.randrange(-1*magnitude, magnitude)
            exploding_bit_y = y + random.randrange(-1*magnitude, magnitude)
            pygame.draw.circle(gameDisplay, colorChoice[random.randrange(0,4)], (exploding_bit_x, exploding_bit_y), random.randrange(1, 5))
            pygame.display.update()
            clock.tick(100)
            magnitude += 1
        explode = False

def healthBar(playerHealth, enemyHealth):
    if playerHealth > 50 :
        playerHealth_color = green
    elif playerHealth >25 :
        playerHealth_color = yellow
    else :
        playerHealth_color = red

    if enemyHealth > 50 :
        enemyHealth_color = green
    elif enemyHealth >25 :
        enemyHealth_color = yellow
    else :
        enemyHealth_color = red

    pygame.draw.rect(gameDisplay, playerHealth_color, [680,25,playerHealth,25])
    pygame.draw.rect(gameDisplay, enemyHealth_color, [20,25,enemyHealth,25])
    pygame.draw.line(gameDisplay, black, (780,25),(780,50), 2)
    pygame.draw.line(gameDisplay, black, (120,25),(120,50), 2)


def gameintro():
    intro = True

    while intro:
        gameDisplay.fill(greyBlue)
        message_to_screen("TANKS", red, y_coordinate=-200, font_size='large')
        message_to_screen("The objective of the game is to shoot and destroy", green, -30)
        message_to_screen("the enemy tanks before they destroy you", green, 10)
        message_to_screen("More you destroy them, better they get", green, 50)

        button("Play", green, lightGreen, (150,500,100,50), action="play")
        button("Control", yellow, lightYellow, (350,500,100,50), action="control")
        button("Quit", red, lightRed,(550,500,100,50), action= "quit")

        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    intro = False
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()
        clock.tick(15)
def gamepause():
    paused = True
    while paused:
        message_to_screen("PAUSED", red, -200, font_size='large')
        message_to_screen("Press c to play or Q to quit ", red, 150)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_c:
                    paused = False
                if event.key == pygame.K_q:
                    pygame.quit()
                    quit()



def gameOVER():
    gameDisplay.fill(greyBlue)
    message_to_screen("GAME OVER", red, -150, font_size='large')
    message_to_screen("You Died !", black, -50, font_size='small')
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()

    button("Play", green, lightGreen, (150, 500, 100, 50), action="play")
    button("Control", yellow, lightYellow, (350, 500, 100, 50), action="control")
    button("Quit", red, lightRed, (550, 500, 100, 50), action="quit")
    pygame.display.update()
    clock.tick(15)

def gameWon():
    gameDisplay.fill(greyBlue)
    message_to_screen("YOU WIN", red, -150, font_size='large')
    message_to_screen("Congratulations!", black, -50, font_size='small')
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
    button("Play", green, lightGreen, (150, 500, 100, 50), action="play")
    button("Control", yellow, lightYellow, (350, 500, 100, 50), action="control")
    button("Quit", red, lightRed, (550, 500, 100, 50), action="quit")
    pygame.display.update()
    clock.tick(15)


def gameLoop():
    gameExit = False
    tankMove = 0
    currentTurPos = 0
    changeTurPos = 0
    currentPower = 50
    changePower = 0
    mainTankX = display_width * 0.9
    mainTankY = display_height * 0.9
    enemyTankX = display_width * 0.1
    enemyTankY = display_height * 0.9
    barrierx = (display_width / 2) + random.randint(-display_width * 0.2, display_width * 0.2)
    barrierHeight = random.randrange(display_height * 0.1, display_height * 0.6)
    barrierWidth = 50
    enemyHealth = 100
    playerHealth = 100


    while not gameExit:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:
                    gamepause()
                elif event.key == pygame.K_LEFT:
                    tankMove = -10
                elif event.key== pygame.K_RIGHT:
                    tankMove = 10
                elif event.key == pygame.K_UP:
                    changeTurPos = 1
                elif event.key == pygame.K_DOWN:
                    changeTurPos = -1
                elif event.key == pygame.K_SPACE:
                    damageE = fireShell(gun, currentTurPos, currentPower, barrierx, barrierWidth, barrierHeight, enemyTankX, enemyTankY)
                    enemyHealth -= damageE

                    possibleMovement =['f', 'r']
                    moveIndex = random.randrange(0,2)
                    for x in range(random.randrange(0,10)):
                        if int(display_width*0.3) > enemyTankX >int(display_width*0.03):
                            if possibleMovement[moveIndex] == 'f':
                                enemyTankX += 5
                            if possibleMovement[moveIndex] == 'r':
                                enemyTankX -= 5
                        gameDisplay.blit(tanksBackground, (0, 0))
                        healthBar(playerHealth, enemyHealth)
                        gun = tank(mainTankX, mainTankY, currentTurPos)
                        enemy_gun = enemy_tank(enemyTankX, enemyTankY, 8)
                        message_to_screen("Power : " + str(currentPower) + "%", black, -250)
                        barrier(barrierx, barrierHeight, barrierWidth)
                        gameDisplay.fill(brown, rect=[0, display_height - groundHeight, display_width, groundHeight])
                        pygame.display.update()
                        clock.tick(15)


                    damageP = e_fireShell(enemy_gun, 8, currentPower, barrierx, barrierWidth, barrierHeight,mainTankX, mainTankY)
                    playerHealth -= damageP

                elif event.key == pygame.K_a:
                    changePower = -1
                elif event.key == pygame.K_d:
                    changePower = 1


            elif event.type == pygame.KEYUP:
                if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT :
                    tankMove = 0
                elif event.key == pygame.K_UP or  event.key == pygame.K_DOWN:
                    changeTurPos = 0
                elif event.key == pygame.K_a or event.key == pygame.K_d:
                    changePower = 0


        currentTurPos += changeTurPos
        currentPower += changePower
        mainTankX += tankMove

        if currentTurPos > 8:
            currentTurPos = 8
        elif currentTurPos < 0:
            currentTurPos = 0

        if mainTankX -(tankWidth/2) < barrierx + barrierWidth:
            mainTankX += 10
        if mainTankX + (tankWidth/2) > display_width :
            mainTankX -=10
        gameDisplay.blit(tanksBackground, (0,0))
        healthBar(playerHealth, enemyHealth)
        gun = tank(mainTankX, mainTankY, currentTurPos)
        enemy_gun = enemy_tank(enemyTankX, enemyTankY, 8)
        message_to_screen("Power : " + str(currentPower) + "%", black, -250)
        barrier(barrierx, barrierHeight, barrierWidth)
        gameDisplay.fill(brown, rect=[0, display_height-groundHeight, display_width, groundHeight])

        if playerHealth < 1:
            gameOVER()
        elif enemyHealth <1 :
            gameWon()
        if currentPower > 100:
            currentPower= 100
        if currentPower < 1:
            currentPower=1
        pygame.display.update()
        clock.tick(15)

    pygame.quit()
    quit()

gameintro()
gameLoop()