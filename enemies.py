import random

pistol_ammo = 5
shotgun_ammo = 2


#I need to fix all of this. this is one big mess. 


zombie = {
  "id": "zombie",
  "zombie_health": 20,
  "speed": 1,
  "zombie_attack": {
    "type": "melee",
    "damage": random.randint(1, 10)*2,
    "range": 1,
    "accuracy": 0, #0 means dead straight, anything else is at an angle
  },
  "drops": "nothing"
}


police_zombie = {
  "id": "policezombie",
  "health": 20,
  "speed": 2,
  "zombie_police_attack": {
    "type": "ranged",
    "damage": random.randint(1, 5)*3,
    "range": 10, #pistol
    "accuracy": random.randint(-30, 30),
  },
  "drops": pistol_ammo
}

shotgunner = {
  "id": "shotgunner",
  "shotgunner_health": 20,
  "shotgunner_speed": 2,
  "shotgunner_attack": {
    "type": "ranged",
    "damage": random.randint(1, 5)*3*3,
    "range": 3, #shotgun
  },
  "drops": shotgun_ammo
}

imp = {
  "id": "imp",
  "imphealth": 60,
  "speed": 1,
  "imp_attack": {
    "impdamage": random.randint(1, 8)*3,
    "range": 10,
  },
  "drops": "nothing"
}

demon = {
  "id": "demon",
  "demon_health": 150,
  "demon_attack": {
    
  }
}