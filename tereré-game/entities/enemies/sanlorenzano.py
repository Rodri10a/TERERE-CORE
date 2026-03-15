from entities.enemy import Enemy

class Salorensano(Enemy):
    #Clase especifica del enemigo de Luque
    def __init__(self, x, y):
        super().__init__(x, y, speed=3.0, health=100, damage=10)

        self.chase_range = 300
        self.attack_range = 80