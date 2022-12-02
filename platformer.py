from random import randrange
import pygame
from pygame.constants import *
from pygame.math import Vector2
from physics_objects import Circle, PhysicsObject, Polygon, Wall
import contact
from forces import *
import math


# Fonts
#nope


# Colors
RED=(255,0,0)
WHITE=(230,230,230)
GREY=(100,100,100)
BLUE=(0,0,200)
YELLOW=(255,255,0)
GREEN=(0,200,0)
BLACK=(0,0,0)
ORANGE=(255,125,0)
VIOLET=(200,0,200)
bg_color=WHITE

# Create window
width, height = 800, 400
window = pygame.display.set_mode([width, height])
windowx=window.get_width()
windowy=window.get_height()
# Clock object for timing
clock = pygame.time.Clock()
fps = 60
dt = 1/fps

#objects
objects = []
phys_obj = []

platforms = []

player = Circle(window, 20, WHITE, pos=(0,0), mass=5)
playerHP = 100
shots = []

hazards = []
enemies = []
enemyhealth = []
superenemies = []
superhealth = []
bullets = []
superbullets = []

effects=[]

#controls variables
space=0
leftkey=0
upkey=0
rightkey=0
downkey=0
shiftkey=0

#game variables
score=0
startpos=(50,windowy-50)
platformcount1st=[9,7,6,5,4]
platformcount2nd=[7,5,4,3,2]
platformcount3rd=[6,4,3,2,1]
enemycount1st=[2,3,2,2,3]
enemycount2nd=[0,1,3,4,4]
enemycount3rd=[1,1,2,3,3]
level=0
playerdamage=20
playermaxHP=100
startj=0
modj=0
starti=0
modi=0
framecount=0
playerangle=0
playerangle2=0
targetarrow=Polygon(window, pos=startpos)
anglelock=0
canjump=1
jumping=0
jumpstrength=300



#I might not even need this, but i'm putting it here anyway (I'll probably delete it later, but for now at least i have walls)
# WALLS
walls=[]
## top wall
topWall=Wall(window,(0,0),(windowx,0))
walls.append(topWall)
#physics_Objects.append(topWall)
objects.append(topWall)
##right wall
rightWall=Wall(window,(windowx,0),(windowx,windowy))
walls.append(rightWall)
#physics_Objects.append(rightWall)
objects.append(rightWall)
##bottom wall
bottomWall=Wall(window,(windowx,windowy),(0,windowy))
walls.append(bottomWall)
#physics_Objects.append(bottomWall)
objects.append(bottomWall)
##Left Wall
leftWall=Wall(window,(0,windowy),(0,0))
walls.append(leftWall)
#physics_Objects.append(leftWall)
objects.append(leftWall)


#OTHER OBJECTS

players = []
players.append(player)

#gravity
gravity = Gravity(objects_list=players, acc=(0,600))

#friction
#TODO



#FUNCTIONS
def generate_platforms():
    global platforms
    global objects
    for p in platforms:
        objects.remove(p)
        platforms.remove(p)
    global window
    global windowx
    global windowy
    global platformcount1st
    global platformcount2nd
    global platformcount3rd
    global level
    #walls
    wallpoints=[[0,0],[10,0],[10,windowy],[0,windowy]]
    wallpoints.reverse()
    #wall to the left
    leftside = Polygon(window,wallpoints,BLUE,pos=(0,0),mass=math.inf)
    objects.append(leftside)
    platforms.append(leftside)
    #wall to the right
    rightside=Polygon(window,wallpoints,BLUE,pos=(windowx-10,0),mass=math.inf)
    objects.append(rightside)
    platforms.append(rightside)
    #floors
    floorpoints=[[0,0],[windowx,0],[windowx,10],[0,10]]
    floorpoints.reverse()
    #bottomfloor
    bottomfloor=Polygon(window,floorpoints,BLUE,pos=(0,windowy-10),mass=math.inf)
    objects.append(bottomfloor)
    platforms.append(bottomfloor)
    #roof
    roof=Polygon(window,floorpoints,BLUE,pos=(0,0), mass=math.inf)
    objects.append(roof)
    platforms.append(roof)
    #platform parameters
    platformpoints=[[0,0],[windowx/10,0],[windowx/10,10],[0,10]]
    platformpoints.reverse()
    platformpositions=[]
    startpoint=0
    #1st floor
    for i in range (platformcount1st[level-1]):
        check=0
        while check==0:
            startpoint=randrange(10)
            if startpoint not in platformpositions:
                platformpositions.append(startpoint)
                check=1
    for p in platformpositions:
        platform=Polygon(window,platformpoints,BLUE,pos=(p*(windowx/10),windowy-100),mass=math.inf)
        objects.append(platform)
        platforms.append(platform)    
    platformpositions.clear()
    startpoint=0
    #secondfloor
    for i in range (platformcount2nd[level-1]):
        check=0
        while check==0:
            startpoint=randrange(10)
            if startpoint not in platformpositions:
                platformpositions.append(startpoint)
                check=1
    for p in platformpositions:
        platform=Polygon(window,platformpoints,BLUE,pos=(p*(windowx/10),windowy-200),mass=math.inf)
        objects.append(platform)
        platforms.append(platform)   
    platformpositions.clear()
    startpoint=0
    #thirdfloor
    for i in range (platformcount3rd[level-1]):
        startpoint=randrange(10)
        if startpoint not in platformpositions:
            platformpositions.append(startpoint)
        else:
            i=i-1
    for p in platformpositions:
        platform=Polygon(window,platformpoints,BLUE,pos=(p*(windowx/10),windowy-300),mass=math.inf)
        objects.append(platform)
        platforms.append(platform)   
    

def generate_enemies():
    global objects
    global enemies
    global bullets
    global window
    global windowx
    global windowy
    global enemycount1st
    global enemycount2nd
    global enemycount3rd
    global level
    for e in enemies:
        if e in objects:
            objects.remove(e)
            enemies.remove(e)
    for b in bullets:
        if b in objects:
            objects.remove(b)
            bullets.remove(b)
    enemypositions=[]
    startpoint=0
    #1st floor
    for i in range (enemycount1st[level-1]):
        check=0
        while check==0:
            startpoint=randrange(10)
            if startpoint not in enemypositions:
                enemypositions.append(startpoint)
                check=1
    for p in enemypositions:
        enemy=Circle(window,25,RED,pos=(p*(windowx/10)+(windowx/20), windowy-350), mass=math.inf)
        objects.append(enemy)
        enemies.append(enemy) 
    enemypositions.clear()
    startpoint=0
    #2nd floor
    for i in range (enemycount2nd[level-1]):
        check=0
        while check==0:
            startpoint=randrange(10)
            if startpoint not in enemypositions:
                enemypositions.append(startpoint)
                check=1
    for p in enemypositions:
        enemy=Circle(window,25,RED,pos=(p*(windowx/10)+(windowx/20), windowy-250), mass=math.inf)
        objects.append(enemy)
        enemies.append(enemy) 
    enemypositions.clear()
    startpoint=0
    #3rd floor
    for i in range (enemycount3rd[level-1]):
        check=0
        while check==0:
            startpoint=randrange(10)
            if startpoint not in enemypositions:
                enemypositions.append(startpoint)
                check=1
    for p in enemypositions:
        enemy=Circle(window,25,RED,pos=(p*(windowx/10)+(windowx/20), windowy-150), mass=math.inf)
        objects.append(enemy)
        enemies.append(enemy) 
    enemypositions.clear()
    startpoint=0
    for e in enemies:
        enemyhealth.append(100)
    for s in superenemies:
        superhealth.append(100)
    


def generate_player():
    global player
    global playerHP
    global startpos
    global shots
    global targetarrow
    shots.clear()
    arrowoffsets=[[30,-5],[35,0],[30,5]]
    if player in objects:
        objects.remove(targetarrow)
        objects.remove(player)
    players.clear()
    player=Circle(window, 20, WHITE, pos=startpos, mass=5)
    players.append(player)
    objects.append(player)
    playerHP = 100
    targetarrow=Polygon(window,arrowoffsets,WHITE,mass=math.inf,pos=player.pos,angle=playerangle2)
    objects.append(targetarrow)


def new_level():
    global level
    level+=1
    generate_platforms()
    generate_enemies()
    generate_player()

#TODO
def game_over():
    print("game over")
    pass


def fire():
    global player
    global shots
    global objects
    global playerangle
    randx1=randrange(-15,15)
    randx2=randrange(-15,15)
    randy1=randrange(-15,15)
    randy2=randrange(-15,15)
    randoffsetx=(randx1+3*randx2/4)
    randoffsety=(randy1+3*randy2/4)
    randoffset=Vector2(randoffsetx,randoffsety)
    shotvel=(0,0)
    for i in range(8):
        if playerangle==i:
            shotvel=640*Vector2(math.cos(i*math.pi/4),math.sin(i*math.pi/4))
    newshot=Circle(window,10,WHITE,mass=5,pos=player.pos+randoffset,vel=shotvel, angle=playerangle2)
    objects.append(newshot)
    shots.append(newshot)

#TODO
def jump():
    pass

def shoot():
    global enemies
    global superenemies
    global bullets
    global superbullets
    global objects
    for e in enemies:
        for i in range(8):
            newbullet=Circle(window,10,RED,4,mass=5,pos=e.pos,vel=640*Vector2(math.cos((math.pi/4)*i),math.sin((math.pi/4)*i)))
            objects.append(newbullet)
            bullets.append(newbullet)

def setangle():
    global upkey
    global rightkey
    global downkey
    global leftkey
    global playerangle
    global playerangle2
    global anglelock
    global objects
    if anglelock==0:
        #1111
        if upkey==1 and rightkey==1 and downkey==1 and leftkey==1:
            playerangle=0
        #1110
        elif upkey==1 and rightkey==1 and downkey==1 and leftkey==0:
            playerangle=0
        #1101
        elif upkey==1 and rightkey==1 and downkey==0 and leftkey==1:
            playerangle=6
        #1100
        elif upkey==1 and rightkey==1 and downkey==0 and leftkey==0:
            playerangle=7
        #1011
        elif upkey==1 and rightkey==0 and downkey==1 and leftkey==1:
            playerangle=4
        #1010
        elif upkey==1 and rightkey==0 and downkey==1 and leftkey==0:
            playerangle=0
        #1001   
        elif upkey==1 and rightkey==0 and downkey==0 and leftkey==1:
            playerangle=5
        #1000   
        elif upkey==1 and rightkey==0 and downkey==0 and leftkey==0:
            playerangle=6
        #0111
        elif upkey==0 and rightkey==1 and downkey==1 and leftkey==1:
            playerangle=2
        #0110
        elif upkey==0 and rightkey==1 and downkey==1 and leftkey==0:
            playerangle=1
        #0101
        elif upkey==0 and rightkey==1 and downkey==0 and leftkey==1:
            playerangle=0
        #0100
        elif upkey==0 and rightkey==1 and downkey==0 and leftkey==0:
            playerangle=0
        #0011
        elif upkey==0 and rightkey==0 and downkey==1 and leftkey==1:
            playerangle=3
        #0010
        elif upkey==0 and rightkey==0 and downkey==1 and leftkey==0:
            playerangle=2
        #0001
        elif upkey==0 and rightkey==0 and downkey==0 and leftkey==1:
            playerangle=4
        #0000
    targetarrow.angle=playerangle*math.pi/4
    targetarrow.pos = player.pos
    targetarrow.update_polygon()
    

    


new_level()
shoot()
game_end = False
# Game loop
running = True
while running:
    pygame.display.update()
    clock.tick(fps)
    window.fill(bg_color)
    # EVENTS
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    # KEY STATE
        #spaceber
        elif event.type==KEYDOWN and event.key==K_SPACE:
            space=1
        elif event.type==KEYUP and event.key==K_SPACE:
            space=0
            
        #left
        elif event.type==KEYDOWN and (event.key==K_LEFT or event.key==K_a):
            leftkey=1
        elif event.type==KEYUP and (event.key==K_LEFT or event.key==K_a):
            leftkey=0
            
        #up
        elif event.type==KEYDOWN and (event.key==K_UP or event.key==K_w):
            upkey=1
        elif event.type==KEYUP and (event.key==K_UP or event.key==K_w):
            upkey=0
            
        #right
        elif event.type==KEYDOWN and (event.key==K_RIGHT or event.key==K_d):
            rightkey=1
        elif event.type==KEYUP and (event.key==K_RIGHT or event.key==K_d):
            rightkey=0

        #down
        elif event.type==KEYDOWN and (event.key==K_DOWN or event.key==K_s):
            downkey=1
        elif event.type==KEYUP and (event.key==K_DOWN or event.key==K_s):
            downkey=0
        
        #shift
        elif event.type==KEYDOWN and (event.key==K_LSHIFT or event.key==K_RSHIFT):
            shiftkey=1
        elif event.type==KEYUP and (event.key==K_LSHIFT  or event.key==K_RSHIFT):
            shiftkey=0

    
    # #test controls
    redcolor=0
    bluecolor=0
    greencolor=0
    # if space==1:
    #     redcolor+=100
    # if leftkey==1:
    #     redcolor+=75
    #     greencolor+=75
    # if upkey==1:
    #     bluecolor+=100
    # if rightkey==1:
    #     bluecolor+=75
    #     redcolor+=75
    # if downkey==1:
    #     greencolor+=100
    # if shiftkey==1:
    #     greencolor+=75
    #     bluecolor+=75
    bg_color=(redcolor,greencolor,bluecolor)
    #I'm gonna keep the above line of code around because I want the background to be black anyway.
    #MOVEMENT
    playerspeed=300
    playervel=Vector2(0,0)
    if rightkey:
        player.vel[0]=playerspeed
    if leftkey:
        player.vel[0]=-playerspeed
    if not rightkey and not leftkey:
        player.vel[0]=0

    #Here comes the hard one
    #JUMPING
    if space==0:
        jumpstrength=0
        jumping=0
    if canjump==1 and jumping==0:
        jumpstrength=50
        jumping=1
        canjump=0
    if jumping==1 and jumpstrength>0:
        player.vel[1]-=jumpstrength
        jumpstrength-=3

    #GAME CONTROLS
    if shiftkey==1:
        anglelock=1
        fire()
    else:
        anglelock=0
    setangle()

    #GAME LOGIC
    #if all the enemies have been defeated, progress to the next level
    if len(enemies)==0:
        new_level()

    #if all players have been defeated, game over
    if game_end:
        game_over()

    #if a bullet collides with a platform, erase the bullet
    #while we're here, better handle walls too
    #superbullets do not collide with platforms
    
    for b in bullets:
        for p in platforms:
            c = contact.generate(p, b, restitution=1, resolve=True)
            if c.overlap>0 and b in bullets:
                objects.remove(b)
                bullets.remove(b)

    for b in bullets:
        for w in walls:
            c = contact.generate(w, b, restitution=1, resolve=True)
            if c.overlap>0 and b in bullets:
                objects.remove(b)
                bullets.remove(b)
    

    #if an enemy collides with a platform, redirect the enemy
    #superenemies do not collide with platforms
    for e in enemies:
        for p in platforms:
            c = contact.generate(p, e, restitution=1, resolve=True)
            
    #if a superenemy collides with a wall
    for s in superenemies:
        for w in walls:
            c = contact.generate(w, s, restitution=1, resolve=True)

    #if a superbullet collides with a wall
    for s in superbullets:
        for w in walls:
            c = contact.generate(w, s, restitution=1, resolve=True)
            if c.overlap>0 and s in superbullets:
                objects.remove(s)
                superbullets.remove(s)

    #If a player collides with a platform
    #TODO friction
    for p in platforms:
        c = contact.generate(p, player, restitution=0, resolve=True)
        if c.overlap>0 and jumping==0:
            canjump=1
    #TODO friction

    #if a players' shot collides with a platform
    for s in shots:
        for p in platforms:
            c = contact.generate(p, s, restitution=1, resolve=True)
            if c.overlap>0 and s in shots:
                objects.remove(s)
                shots.remove(s)

    #if a bullet collides with a player
    for i, b in enumerate(bullets):
        c = contact.generate(b, player, restitution=1, resolve=True)
        if c.overlap>0 and b in bullets:
            playerHP-=10
            bullets.remove(b)
            objects.remove(b)
        if playerHP<=0:
            players.remove(player)
            objects.remove(player)
            game_end = True

    #if a superbullet collides with a player
    for i, sb in enumerate(superbullets):
        c = contact.generate(sb, player, restitution=1, resolve=True)
        if c.overlap>0 and sb in superbullets:
            playerHP-=10
            superbullets.remove(sb)
            objects.remove(sb)
        if playerHP<=0:
            player.pos = startpos
            players.remove(player)
            objects.remove(player)
            game_end = True

    #if a bullet collides with a players' shot, remove both projectiles
    for b in bullets:
        for s in shots:
            c = contact.generate(s, b, restitution=1, resolve=True)
            if c.overlap>0 and b in bullets and s in shots:
                objects.remove(b)
                bullets.remove(b)
                objects.remove(s)
                shots.remove(s)
                
    #if a superbullet collides with a players' shot, remove both projectiles
    for sb in superbullets:
        for sh in shots:
            c = contact.generate(sh, sb, restitution=1, resolve=True)
            if c.overlap>0 and sb in superbullets and sh in shots:
                objects.remove(sb)
                superbullets.remove(sb)
                objects.remove(sh)
                shots.remove(sh)

    #if a players' shot collides with an enemy,
    for j, e in enumerate(enemies):
        for i, s in enumerate(shots):
            c = contact.generate(s, e, restitution=1, resolve=True)
            print(j, enemyhealth[j])
            if c.overlap>0 and s in shots:
                enemyhealth[j]-=playerdamage
                objects.remove(s)
                shots.remove(s)
            if enemyhealth[j]<=0 and e in enemies:
                objects.remove(e)
                enemies.remove(e)
                enemyhealth.remove(enemyhealth[j])
                break
    
    #if a players' shot collides with a superenemy
    for j, su in enumerate(superenemies):
        for i, sh in enumerate(shots):
            c = contact.generate(sh, su, restitution=1, resolve=True)
            if c.overlap>0 and sh in shots:
                superhealth[j]-=playerdamage
                objects.remove(sh)
                shots.remove(sh)
            if superhealth[j]<=0 and su in superenemies:
                objects.remove(su)
                superenemies.remove(su)
                superhealth.remove(superhealth[j])

    framecount+=1
    if framecount%60==0:
        shoot()




    
    # PHYSICS
    # Clear force from all particles
    for obj in objects:
        obj.clear_force()
    # Add forces
    gravity.apply()
    # Update particles
    
        
    # GRAPHICS
    
    ## Clear window
    window.fill(bg_color)
    ## Draw objects
    for obj in objects:
        obj.update(dt)
        obj.draw()
    
    ## Draw Text
    #TODO

