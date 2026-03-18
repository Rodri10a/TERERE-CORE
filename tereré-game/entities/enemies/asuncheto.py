from entities.enemy import Enemy

class Asuncheto(Enemy):
    #Clase especifica del enemigo de Asuncion
    def __init__(self, x, y):
        super().__init__(x, y, speed=4.0, health=200, damage=20)

        self.chase_range = 350
        self.attack_range = 85
