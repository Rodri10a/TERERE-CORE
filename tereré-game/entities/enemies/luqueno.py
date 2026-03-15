from entities.enemy import Enemy

class Luqueno(Enemy):
    #Clase especifica del enemigo de Luque
    def __init__(self, x, y):
        super().__init__(x, y, speed=4.5, health=70, damage=20)

        self.chase_range = 350
        self.attack_range = 85