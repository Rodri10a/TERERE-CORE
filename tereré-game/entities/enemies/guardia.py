from entities.enemy import Enemy

class Guardia(Enemy):
    #Clase especifica del guardia
    def __init__(self, x, y):
        super().__init__(x, y, speed=2.0, health=200, damage=18)

        self.chase_range = 200
        self.attack_range = 90