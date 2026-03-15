from entities.enemy import Enemy

class Cheto(Enemy):
    #Clase especifica del Cheto
    def __init__(self, x, y):
        super().__init__(x, y, speed=3.0, health=100, damage=8)

        self.chase_range =400
        self.attack_range = 90