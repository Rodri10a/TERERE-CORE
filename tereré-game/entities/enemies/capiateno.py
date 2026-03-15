from entities.enemy import Enemy


class Capiateno(Enemy):
    #Clase especifica del enemigo de Luque
    def __init__(self, x, y):
        super().__init__(x, y, speed=2.0, health=60, damage=6)

        self.chase_range = 150
        self.attack_range = 60