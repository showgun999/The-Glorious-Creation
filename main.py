import os
import pickle
import random
import sys
import time

import pygame

import enemies
import maptextures
import playersprites
import world1
"""
to do: 
1- make the player info bar, (done, needs improvement later as needed)
2- create sprites,
3- make player attacking work (sprites, damage, etc),
4- read the map and print it on the output and have it updatable,
4.1- colisions in map for walls and doors/other stuff,
5- make item sprites (32px size?),
6- make entities readable from map,
7- create entity ai with colision w| walls, doors, and player,
8- adjustable screen to automatically fit screen size, 
9- menu screen,
10- sounds & music!,
11- make the player face the mouse position for combat mechanics?,
12- Gore!,
13- remove diagonal movement?,
14- redo the weapon/inventory system for better layout/moding?
15- reduce speed when going diagnal!
more stuff later as I go along =)
"""

#releace date next year! =) 2025!

#how to render image: screen.blit(image_name, (x, y))

# Initialize Pygame
pygame.init()

#add text phonts
font = pygame.font.Font(None, 32)

# Set up the display
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 704  #640+64 to add player info at bottom :)
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("my 2d game :)")
#info = pygame.display.Info()
#SCREEN_WIDTH, SCREEN_HEIGHT = info.current_w, info.current_h
#screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.FULLSCREEN)

#clock stuff
clock = pygame.time.Clock()


def cs():
  #clear terminal
  os.system('clear')


def ext():
  sys.exit()


weapon_damage = {
    "fists_damage": random.randint(1, 10) * 2,
    "chainsaw_damage": random.randint(3, 10) * 10,
    "pistol_damage": random.randint(1, 3) * 5,
    "shotgun_damage": random.randint(4, 7) * random.randint(1, 3) * 5,
    "rocket_launcher_damage": random.randint(1, 8) * 20,
}


def reload_weapon_damage():
  global weapon_damage
  weapon_damage["fists_damage"] = random.randint(1, 10) * 2
  weapon_damage["chainsaw_damage"] = random.randint(5, 10) * 10
  weapon_damage["pistol_damage"] = random.randint(1, 3) * 5
  weapon_damage["shotgun_damage"] = random.randint(4, 7) * random.randint(1, 3) * 5
  weapon_damage["rocket_launcher_damage"] = random.randint(1, 8) * 20


player_info = {
    "player health": 100,
    "player health max": 100,
    "player stamina": 100,
    "player stamina max": 100,
    "player armor": 0,
    "player x": 0,
    "player y": 0,
    "player height": 64,
    "player width": 64,
    "player speed": 2,
    "player direction": "north",
}


def restart_player_info():
  global player_info
  player_info["player health"] = 100
  player_info["player health max"] = 100
  player_info["player stamina"] = 100
  player_info["player stamina max"] = 100
  player_info["player defense"] = 0
  player_info["player x"] = 0
  player_info["player y"] = 0
  player_info["player height"] = 64
  player_info["player width"] = 64
  player_info["player speed"] = 2
  player_info["player direction"] = "North"


inventory = {
    "weapons": {
        "fists": {
            "has": True,
            "equiped": True,
            "ammo loaded": "inf",
            "max ammo load": "inf",
            "range": 1,
            #in units of 64 px (tiles)
            "speed": 1,
            #seconds before attacking again with this weapon
            "damage": weapon_damage["fists_damage"],
        },
        "chainsaw": {
            "has": True,
            "equiped": False,
            "ammo loaded": 1,
            "max ammo load": 1,
            "range": 2,
            "speed": 1,
            "damage": weapon_damage["chainsaw_damage"],
        },
        "pistol": {
            "has": True,
            "equiped": False,
            "ammo loaded": 5,
            "max ammo load": 16,
            "range": 10,
            "speed": .4,
            "damage": weapon_damage["pistol_damage"],
        },
        "shotgun": {
            "has": True,
            "equiped": False,
            "ammo loaded": 4,
            "max ammo load": 9,
            "range": 3,
            "speed": 0.8,
            "damage": weapon_damage["shotgun_damage"],
        },
        "rifle": {
          "has": True,
          "equiped": False,
          "ammo loaded": 27,
          "max ammo load": 31,
          "range": 10,
          "speed": 0.2,
          "damage": weapon_damage["pistol_damage"],
        },
        "rocket launcher": {
            "has": True,
            "equiped": False,
            "ammo loaded": 1,
            "max ammo load": 4,
            "range": 8,
            "speed": 1/1.75,
            #attack every 0.5714285714... seconds.
            "damage": weapon_damage["rocket_launcher_damage"],
        },
    },
    "ammo": {
        "cans of gasoline": {
          "has": 2,
          "maxhold": 4
#all ammo maxhold is doubled rn for testing, maybe copy doom's backpack mechanics?
        },
        "bullets": {
            "has": 50,
            "maxhold": 200
        },
        "shells": {
            "has": 24,
            "maxhold": 50
        },
        "rockets": {
            "has": 2,
            "maxhold": 25
        }
    }
}


def restart_inventory():
  global inventory
  inventory['weapons']['fists']['equiped'] = True
  inventory['weapons']['chainsaw']['has'] = False
  inventory['weapons']['chainsaw']['equiped'] = False
  inventory['weapons']['chainsaw']['ammo loaded'] = inventory['weapons']['chainsaw'] \
  ['max ammo load']
  inventory['weapons']['pistol']['has'] = False
  inventory['weapons']['pistol']['equiped'] = False
  inventory['weapons']['pistol']['ammo loaded'] = inventory['weapons']['pistol'] \
  ['max ammo load']
  inventory['weapons']['shotgun']['has'] = False
  inventory['weapons']['shotgun']['equiped'] = False
  inventory['weapons']['shotgun']['ammo loaded'] = inventory['weapons']['shotgun'] \
  ['max ammo load']
  inventory['weapons']['rifle']['has'] = False
  inventory['weapons']['rifle']['equiped'] = False
  inventory['weapons']['rifle']['ammo loaded'] = inventory['weapons']['rifle'] \
  ['max ammo load']
  inventory['weapons']['rocket launcher']['has'] = False
  inventory['weapons']['rocket launcher']['equiped'] = False
  inventory['weapons']['rocket launcher']['ammo loaded'] = inventory['weapons'] \
  ['rocket launcher']['max ammo load']
  inventory['ammo']['cans of gasoline']['has'] = 0
  inventory['ammo']['cans of gasoline']['maxhold'] = 2
  inventory['ammo']['bullets']['has'] = 0
  inventory['ammo']['bullets']['maxhold'] = 200
  inventory['ammo']['shells']['has'] = 0
  inventory['ammo']['shells']['maxhold'] = 50
  inventory['ammo']['rockets']['has'] = 0
  inventory['ammo']['rockets']['maxhold'] = 25


def save_game():
  print("saving game...")
  print("Which file do you want to save on?")
  print("Save file 1, 2, or 3?")
  print("or do you want to exit?")
  tryagain = True
  filename = ""
  while tryagain is True:
    filechoice = input("")
    filename = ""
    if filechoice == "1":
      filename = "save1"
      break
    elif filechoice == "2":
      filename = "save2"
      break
    elif filechoice == "3":
      filename = "save3"
      break
    elif filechoice == "4":
      filename = "exit"
      break
    else:
      print("Invalid input, please type 1, 2, 3, or 4 to exit.")
  if filename == "exit":
    ext()
  else:
    with open("saves/" + filename + ".pkl", "wb") as f:
      pickle.dump((player_info, inventory), f)
  cs()
  print("file saved")
  print("press any key to continue")
  input()
  cs()


def load_game():
  global player_info, inventory
  try:
    print("What save file do you want to load?")
    print(
        "You can type 1, 2, or 3 to open one of the 3 save files, or 4 to exit. "
    )
    tryagain = True
    filechoice = ""
    while tryagain is True:
      filename = input("")
      filechoice = ""
      if filename == "1":
        filechoice = "save1"
        break
      elif filename == "2":
        filechoice = "save2"
        break
      elif filename == "3":
        filechoice = "save3"
        break
      elif filename == "4":
        filechoice = "exit"
        break
      else:
        print("Invalid input, please type 1, 2, 3, or 4.")
    if filechoice != "exit":
      with open("saves/" + filechoice + ".pkl", "rb") as f:
        player_info, inventory = pickle.load(f)
      print("Game loaded.")
      print("press any key to continue")
      input()
      cs()
    else:
      ext()
  except FileNotFoundError:
    print("Save file not found.")
    input("press a key")
    terminalstart()


def auto_save():
  with open("saves/autosave" + ".pkl", "wb") as f:
    pickle.dump((player_info, inventory), f)


"""
def equipstuff():
  if inventory['weapons']['fists']['equiped'] is True:
    playerinfo["playerdamage"] = fists_damage
  if inventory['weapons']['chainsaw']['equiped'] is True:
    playerinfo["playerdamage"] = chainsaw_damage
  if inventory['weapons']['pistol']['equiped'] is True:
    playerinfo["playerdamage"] = pistol_damage
  if inventory['weapons']['shotgun']['equiped'] is True:
    playerinfo["playerdamage"] = shotgun_damage
  if inventory['weapons']['rocket launcher']['equiped'] is True:
    playerinfo["playerdamage"] = rocket_launcher_damage
"""


def terminalstart():
  cs()
  print("game demo")
  print("this is just for testing")
  print("1: save data")
  print("2: load data")
  print("3: stop process")
  menu = input("")
  if menu == "1":
    cs()
    save_game()
  elif menu == "2":
    cs()
    load_game()
  elif menu == "3":
    ext()
  else:
    cs()
    print("press a number key then enter to interact")
    time.sleep(2)
    cs()
    terminalstart()


"""
start()
save_game()
load_game()
print(player_info)
print(inventory)
"""

# Before the screen.blit line, load the image directly in the main file
#change this into a def that will load different images depending on texture & map files
barrel = pygame.image.load('maptextures/Photo_barrel.png')
bluestone = pygame.image.load('maptextures/Photo_bluestone.png')
colorstone = pygame.image.load('maptextures/Photo_colorstone.png')
eagle = pygame.image.load('maptextures/Photo_eagle.png')
greenlight = pygame.image.load('maptextures/Photo_greenlight.png')
greystone = pygame.image.load('maptextures/Photo_greystone.png')
mossy = pygame.image.load('maptextures/Photo_mossy.png')
pillar = pygame.image.load('maptextures/Photo_pillar.png')
purplestone = pygame.image.load('maptextures/Photo_purplestone.png')
redbrick = pygame.image.load('maptextures/Photo_redbrick.png')
wood = pygame.image.load('maptextures/Photo_wood.png')
# Then use the loaded image in the screen.blit function


def Draw_player():
  global player_info
  circle = pygame.image.load('playersprites/circle.png')
  face_east = pygame.image.load('playersprites/face_east.png')
  face_north = pygame.image.load('playersprites/face_north.png')
  face_west = pygame.image.load('playersprites/face_west.png')
  face_south = pygame.image.load('playersprites/face_south.png')
  face_northeast = pygame.image.load('playersprites/face_northeast.png')
  face_northwest = pygame.image.load('playersprites/face_northwest.png')
  face_southeast = pygame.image.load('playersprites/face_southeast.png')
  face_southwest = pygame.image.load('playersprites/face_southwest.png')
  for i in player_info:
    if player_info["player direction"] == "northeast":
      screen.blit(face_northeast,
                  (player_info["player x"], player_info["player y"]))
      break
    if player_info["player direction"] == "northwest":
      screen.blit(face_northwest,
                  (player_info["player x"], player_info["player y"]))
      break
    if player_info["player direction"] == "southeast":
      screen.blit(face_southeast,
                  (player_info["player x"], player_info["player y"]))
      break
    if player_info["player direction"] == "southwest":
      screen.blit(face_southwest,
                  (player_info["player x"], player_info["player y"]))
      break
    if player_info["player direction"] == "north":
      screen.blit(face_north,
                  (player_info["player x"], player_info["player y"]))
      break
    if player_info["player direction"] == "south":
      screen.blit(face_south,
                  (player_info["player x"], player_info["player y"]))
      break
    if player_info["player direction"] == "west":
      screen.blit(face_west,
                  (player_info["player x"], player_info["player y"]))
      break
    if player_info["player direction"] == "east":
      screen.blit(face_east,
                  (player_info["player x"], player_info["player y"]))
      break
    if player_info["player direction"] == "":
      screen.blit(circle, (player_info["player x"], player_info["player y"]))
      break


def Load_world1():
  world1.start()


"""
def Load_world2():
  world2.start()

def Load_world3():
  world3.start()
"""
loadingweapon = False
sprinting = False
sprintingcooldown = False
heldKeys = []
def getevents():
  global heldKeys
  global inventory
  global player_info
  global sprinting
  global sprintingcooldown
  global loadingweapon
  for i in pygame.event.get():
    if i.type == pygame.QUIT:
      pygame.quit()
      sys.exit()
    if i.type == pygame.KEYDOWN:  #Track down key presses here
      if i.key == pygame.K_s:
        heldKeys.append('DOWN')
      if i.key == pygame.K_w:
        heldKeys.append('UP')
      if i.key == pygame.K_a:
        heldKeys.append('LEFT')
      if i.key == pygame.K_d:
        heldKeys.append('RIGHT')
      if i.key == pygame.K_r:
        reload()
      #make aswd keys for movement and numbers for equiping weapons
      if i.key==pygame.K_LSHIFT and sprintingcooldown is False:
        #double speed
        #add sprinting cooldown with stamina mechanic
        sprinting = True
        player_info["player speed"] = player_info["player speed"] * 2
      if i.key == pygame.K_1 and inventory["weapons"]["chainsaw"]["has"] is True and \
      inventory["weapons"]["fists"]["equiped"] is True:
        inventory["weapons"]["fists"]["equiped"] = False
        inventory["weapons"]["chainsaw"]["equiped"] = True
        inventory["weapons"]["pistol"]["equiped"] = False
        inventory["weapons"]["shotgun"]["equiped"] = False
        inventory["weapons"]["rifle"]["equiped"] = False
        inventory["weapons"]["rocket launcher"]["equiped"] = False
      elif i.key == pygame.K_1 and inventory["weapons"]["fists"]["has"] is True and \
      loadingweapon is False:
        inventory["weapons"]["fists"]["equiped"] = True
        inventory["weapons"]["chainsaw"]["equiped"] = False
        inventory["weapons"]["pistol"]["equiped"] = False
        inventory["weapons"]["shotgun"]["equiped"] = False
        inventory["weapons"]["rifle"]["equiped"] = False
        inventory["weapons"]["rocket launcher"]["equiped"] = False
      if i.key == pygame.K_2 and inventory["weapons"]["pistol"]["has"] is True and \
      loadingweapon is False:
        inventory["weapons"]["fists"]["equiped"] = False
        inventory["weapons"]["chainsaw"]["equiped"] = False
        inventory["weapons"]["pistol"]["equiped"] = True
        inventory["weapons"]["shotgun"]["equiped"] = False
        inventory["weapons"]["rifle"]["equiped"] = False
        inventory["weapons"]["rocket launcher"]["equiped"] = False
      if i.key == pygame.K_3 and inventory["weapons"]["shotgun"]["has"] is True and \
      loadingweapon is False:
        inventory["weapons"]["fists"]["equiped"] = False
        inventory["weapons"]["chainsaw"]["equiped"] = False
        inventory["weapons"]["pistol"]["equiped"] = False
        inventory["weapons"]["shotgun"]["equiped"] = True
        inventory["weapons"]["rifle"]["equiped"] = False
        inventory["weapons"]["rocket launcher"]["equiped"] = False
      if i.key == pygame.K_4 and inventory["weapons"]["rifle"]["has"] is True and \
      loadingweapon is False:
        inventory["weapons"]["fists"]["equiped"] = False
        inventory["weapons"]["chainsaw"]["equiped"] = False
        inventory["weapons"]["pistol"]["equiped"] = False
        inventory["weapons"]["shotgun"]["equiped"] = False
        inventory["weapons"]["rifle"]["equiped"] = True
        inventory["weapons"]["rocket launcher"]["equiped"] = False
      if i.key == pygame.K_5 and inventory["weapons"]["rocket launcher"] \
      ["has"] is True and loadingweapon is False:
        inventory["weapons"]["fists"]["equiped"] = False
        inventory["weapons"]["chainsaw"]["equiped"] = False
        inventory["weapons"]["pistol"]["equiped"] = False
        inventory["weapons"]["shotgun"]["equiped"] = False
        inventory['weapons']['rifle']['equiped'] = False
        inventory["weapons"]["rocket launcher"]["equiped"] = True
    elif i.type == pygame.KEYUP:  #Track down key releases here
      if i.key == pygame.K_s:
        heldKeys.remove('DOWN')
      if i.key == pygame.K_w:
        heldKeys.remove('UP')
      if i.key == pygame.K_a:
        heldKeys.remove('LEFT')
      if i.key == pygame.K_d:
        heldKeys.remove('RIGHT')
      if i.key == pygame.K_LSHIFT and sprinting:
        sprinting = False
        player_info['player speed'] = player_info['player speed'] / 2

moving_one_way = ""
def checkheldkeys():  #use this in your game loop to move your character
  global player_info
  global heldkeys
  global moving_one_way
  for i in heldKeys:
    if 'DOWN' in heldKeys:
      moving_one_way = "down"
      player_info["player y"] += player_info["player speed"]
      if player_info["player y"] > 640 - 64:
        player_info["player y"] = 640 - 64
    if 'UP' in heldKeys:
      moving_one_way = "up"
      player_info["player y"] -= player_info["player speed"]
      if player_info["player y"] < 0:
        player_info["player y"] = 0
    if 'LEFT' in heldKeys:
      moving_one_way = "left"
      player_info["player x"] -= player_info["player speed"]
      if player_info["player x"] < 0:
        player_info["player x"] = 0
    if 'RIGHT' in heldKeys:
      moving_one_way = "right"
      player_info["player x"] += player_info["player speed"]
      if player_info["player x"] > SCREEN_WIDTH - 64:
        player_info["player x"] = SCREEN_WIDTH - 64
    for i in heldKeys:
      if 'DOWN' in heldKeys:
        player_info["player direction"] = "south"
      if 'UP' in heldKeys:
        player_info["player direction"] = "north"
      if 'LEFT' in heldKeys:
        player_info["player direction"] = "west"
      if 'RIGHT' in heldKeys:
        player_info["player direction"] = "east"
      """
      get rid of diagonals!
      """
      if 'UP' in heldKeys and 'RIGHT' in heldKeys:
        player_info["player direction"] = "northeast"
      if 'UP' in heldKeys and 'LEFT' in heldKeys:
        player_info["player direction"] = "northwest"
      if 'DOWN' in heldKeys and 'RIGHT' in heldKeys:
        player_info["player direction"] = "southeast"
      if 'DOWN' in heldKeys and 'LEFT' in heldKeys:
        player_info["player direction"] = "southwest"


def sprintornot():
  global player_info
  global sprinting
  global sprintingcooldown
  if sprinting is False:
    player_info['player stamina'] += 0.5
    if player_info['player stamina'] > player_info['player stamina max']:
      player_info['player stamina'] = player_info['player stamina max']
    if player_info['player stamina'] == player_info['player stamina max']:
      sprintingcooldown = False
  if sprinting is True and not sprintingcooldown:
    player_info['player stamina'] -= 0.5
    if player_info['player stamina'] <= 0:
      player_info['player stamina'] = 0
      sprinting = False
      sprintingcooldown = True
      player_info['player speed'] = player_info['player speed'] / 2


def drawplayerstats():
  global player_info
  global inventory
  global ammotext, ammocount, ammoloadedcount, ammoloadedtext
  global sprintingcooldown
  pygame.draw.rect(screen, (93, 93, 93), pygame.Rect(0, 640, SCREEN_WIDTH, 64))
  #this is the bottom bar that displays the player info
  #make different if elif stuff for weapon pictures
  fist = pygame.image.load('playerweapons/fist.png')
  chainsaw = pygame.image.load('playerweapons/chainsaw.png')
  pistol = pygame.image.load('playerweapons/pistol.png')
  shotgun = pygame.image.load('playerweapons/shotgun.png')
  rifle = pygame.image.load('playerweapons/rifle.png')
  rocketlauncher = pygame.image.load('playerweapons/rocket launcher.png')
  #this stuff below is all for displaying weapon & ammo info.
  weaponpicture = pygame.image.load('playersprites/circle.png')
  ammotext = font.render("ammo:", True, (255, 255, 255))
  ammocount = font.render("not", True, (255, 255, 255))
  ammoloadedtext = font.render("loaded:", True, (255, 255, 255))
  ammoloadedcount = font.render("not", True, (255, 255, 255))
  weaponequiped = font.render("nothing", True, (255, 255, 255))
  healthtext = font.render("health:", True, (255, 255, 255))
  healthcount = font.render(str(player_info["player health"]) + "%", True, (255, 255, 255))
  staminatext = font.render("stamina:", True, (255, 255, 255))
  staminacount = font.render(str(player_info["player stamina"]) + "%", True, (255, 255, 255))
  armortext = font.render("armor:", True, (255, 255, 255))
  armorcount = font.render(str(player_info["player armor"]) + "%", True, (255, 255, 255))
  #checks for what is equiped to display the right stuff
  if inventory['weapons']['fists']['equiped'] is True:
    ammocount = font.render("tear!", True, (255, 255, 255))
    ammoloadedcount = font.render("=)", True, (255, 255, 255))
    ammotext = font.render("rip &", True, (255, 255, 255))
    ammoloadedtext = font.render("", True, (255, 255, 255))
    weaponequiped = font.render("fists:", True, (255, 255, 255))
    weaponpicture = fist
  elif inventory['weapons']['chainsaw']['equiped'] is True:
    ammocount = font.render(str(inventory['ammo']['cans of gasoline']['has']) + "/" + \
                            str(inventory['ammo']['cans of gasoline']['maxhold']), \
                            True, (255, 255, 255))
    ammoloadedcount = font.render(str(inventory['weapons']['chainsaw'] \
                            ['ammo loaded']) + "/" + str(inventory['weapons'] \
                            ['chainsaw']['max ammo load']), True, (255, 255, 255))
    ammotext = font.render("gasoline:", True, (255, 255, 255))
    weaponequiped = font.render("chainsaw", True, (255, 255, 255))
    weaponpicture = chainsaw
  elif inventory['weapons']['pistol']['equiped'] is True:
    ammocount = font.render(str(inventory['ammo']['bullets']['has']) + "/" + \
                            str(inventory['ammo']['bullets']['maxhold']), \
                            True, (255, 255, 255))
    ammoloadedcount = font.render(str(inventory['weapons']['pistol'] \
                            ['ammo loaded']) + "/" + str(inventory['weapons'] \
                            ['pistol']['max ammo load']),True,(255, 255, 255))
    ammotext = font.render("bullets:", True, (255, 255, 255))
    weaponequiped = font.render("pistol", True, (255, 255, 255))
    weaponpicture = pistol
  elif inventory['weapons']['shotgun']['equiped'] is True:
    ammocount = font.render(str(inventory['ammo']['shells']['has']) + "/" + \
                            str(inventory['ammo']['shells']['maxhold']), \
                            True, (255, 255, 255))
    ammoloadedcount = font.render(str(inventory['weapons']['shotgun'] \
                            ['ammo loaded']) + "/" + str(inventory['weapons'] \
                            ['shotgun']['max ammo load']), True, (255, 255, 255))
    ammotext = font.render("shells:", True, (255, 255, 255))
    weaponequiped = font.render("shotgun", True, (255, 255, 255))
    weaponpicture = shotgun
  elif inventory['weapons']['rifle']['equiped'] is True:
    ammocount = font.render(str(inventory['ammo']['bullets']['has']) + "/" + \
                            str(inventory['ammo']['bullets']['maxhold']), \
                            True, (255, 255, 255))
    ammoloadedcount = font.render(str(inventory['weapons']['rifle'] \
                            ['ammo loaded']) + "/" + str(inventory['weapons'] \
                            ['rifle']['max ammo load']), True,(255, 255, 255))
    ammotext = font.render("bullets:", True, (255, 255, 255))
    weaponequiped = font.render("rifle", True, (255, 255, 255))
    weaponpicture = rifle
  elif inventory['weapons']['rocket launcher']['equiped'] is True:
    ammocount = font.render(str(inventory['ammo']['rockets']['has']) + "/" + \
                            str(inventory['ammo']['rockets']['maxhold']), \
                            True, (255, 255, 255))
    ammoloadedcount = font.render(str(inventory['weapons']['rocket launcher'] \
                            ['ammo loaded']) + "/" + str(inventory['weapons'] \
                            ['rocket launcher']['max ammo load']), True,(255, 255, 255))
    ammotext = font.render("rockets:", True, (255, 255, 255))
    weaponequiped = font.render("rocket launcher", True, (255, 255, 255))
    weaponpicture = rocketlauncher
    #now we display the things.
  screen.blit(ammotext, (0, 640))  #ammo:
  screen.blit(ammocount, (0, 672))  #amount of ammo in numbers
  #screen.blit(ammoloadedtext, (96, 640))  #loaded:
  screen.blit(ammoloadedcount, (96, 672))  #below weapon name
  screen.blit(weaponequiped, (96, 640)) #fists
  screen.blit(healthtext, (400, 640)) #health:
  screen.blit(healthcount, (400, 672)) #100%
  screen.blit(armortext, (500, 640)) #armor:
  screen.blit(armorcount, (500, 672)) #100%
  screen.blit(weaponpicture, (576, 640)) #weapon picture
  screen.blit(staminatext, (285, 640)) #stamina:
  screen.blit(staminacount, (285, 672)) #100%
  if sprintingcooldown is True:
    pygame.draw.rect(screen, (93, 93, 93), pygame.Rect(285, 672, 64, 64))
    resting_text = font.render("resting...", True, (255, 255, 255))
    screen.blit(resting_text, (285, 672))
  #where to start? how about the weapon equiped and ammo?
  #or maybe player health and armor?


def reload():
  global player_info
  global inventory
  global ammocount, ammoloadedcount #ammoloadedcount will say reloading
  global ticksneeded
  global loadingweapon
  #global ammo texts please for enhancement ("loading")
  if inventory['weapons']['pistol']['equiped'] is True:
    ammo_needed = inventory['weapons']['pistol']['max ammo load'] - inventory['weapons']['pistol']['ammo loaded']
    if inventory['ammo']['bullets']['has'] >= ammo_needed:
      inventory['ammo']['bullets']['has'] -= ammo_needed
      inventory['weapons']['pistol']['ammo loaded'] = inventory['weapons']['pistol']['max ammo load']
    else:
      inventory['weapons']['pistol']['ammo loaded'] += inventory['ammo']['bullets']['has']
      inventory['ammo']['bullets']['has'] -= inventory['ammo']['bullets']['has']
    
  if inventory['weapons']['shotgun']['equiped'] is True and \
  inventory['ammo']['shells']['has'] > 0 and \
  inventory['weapons']['shotgun']['ammo loaded'] < \
  inventory['weapons']['shotgun']['max ammo load']:

    inventory['ammo']['shells']['has'] -= 1
    inventory['weapons']['shotgun']['ammo loaded'] += 1
    #super simple, just load one shell at a time ;)
    
  if inventory['weapons']['rifle']['equiped'] is True:
    ammo_needed = inventory['weapons']['rifle']['max ammo load'] - inventory['weapons']['rifle']['ammo loaded']
    if inventory['ammo']['bullets']['has'] >= ammo_needed:
      inventory['ammo']['bullets']['has'] -= ammo_needed
      inventory['weapons']['rifle']['ammo loaded'] = inventory['weapons']['rifle']['max ammo load']
    else:
      inventory['weapons']['rifle']['ammo loaded'] += inventory['ammo']['bullets']['has']
      inventory['ammo']['bullets']['has'] -= inventory['ammo']['bullets']['has']

  if inventory['weapons']['rocket launcher']['equiped'] is True:
    ammo_needed = inventory['weapons']['rocket launcher']['max ammo load'] - inventory['weapons']['rocket launcher']['ammo loaded']
    if inventory['ammo']['rockets']['has'] >= ammo_needed:
      inventory['ammo']['rockets']['has'] -= ammo_needed
      inventory['weapons']['rocket launcher']['ammo loaded'] = inventory['weapons']['rocket launcher']['max ammo load']
    if inventory['ammo']['rockets']['has'] == 0:
      print("there is nothing to load!")
    else:
      inventory['weapons']['rocket launcher']['ammo loaded'] += inventory['ammo']['rockets']['has']
      inventory['ammo']['rockets']['has'] -= inventory['ammo']['rockets']['has']
      #ticksneeded = 60
      #count_ticks_to_reload()
      
  if inventory['weapons']['fists']['equiped'] is True:
    ammocount = "*cracks"
    ammoloadedcount = " knuckles*"
    
  if inventory['weapons']['chainsaw']['equiped'] is True and \
  inventory['ammo']['cans of gasoline']['has'] > 0 and \
  inventory['weapons']['chainsaw']['ammo loaded'] < inventory['weapons']['chainsaw'] \
  ['max ammo load']:
    #same as shotgun, make weapon function like in doom eternal i guess
    inventory['ammo']['cans of gasoline']['has'] -= 1
    inventory['weapons']['chainsaw']['ammo loaded'] += 1
    #ticksneeded = 300
    #count_ticks_to_reload()
"""
ticks = 0
ticksneeded = 0
loadingweapon = False
def count_ticks_to_reload():
  global ticks, ticksneeded
  global loadingweapon
  loadingweapon = True
  while ticks <= ticksneeded:
    ticks += 1
  if ticks == ticksneeded:
    loadingweapon = False
"""
  
  
  
"""
"shotgun": {
  "has": True,
  "equiped": False,
  "ammo loaded": 4,
  "max ammo load": 8,
  "range": 4,
  "speed": 1.25,
  "damage": weapon_damage["shotgun_damage"],
"""
    
"""
"shells": {
"has": 24,
"maxhold": 100
"""
popupstart = True #make starting screen
#Pygame Loop begins Here
while True:
  getevents()
  checkheldkeys()
  
  # Fill the screen with a default color
  screen.fill((255, 0, 0))
  #now draw the map
  #Load_world1()
  #"""
  screen.blit(barrel, (320, 64))
  screen.blit(bluestone, (64, 0))
  screen.blit(colorstone, (0, 64))
  screen.blit(eagle, (64, 64))
  screen.blit(greenlight, (128, 0))
  screen.blit(greystone, (128, 64))
  screen.blit(mossy, (192, 0))
  screen.blit(pillar, (192, 64))
  screen.blit(purplestone, (256, 0))
  screen.blit(redbrick, (256, 64))
  screen.blit(wood, (320, 0))
  #"""
  #drawing those pictures are just a test

  #now draw the player stats
  drawplayerstats()

  #Draw character centered on the screen
  Draw_player()
  sprintornot()
  #Update the display
  pygame.display.flip()

  #Cap the frame rate
  clock.tick(60)
