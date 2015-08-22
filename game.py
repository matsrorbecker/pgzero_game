from pygame.time import get_ticks

WIDTH = 480
HEIGHT = 600
TITLE = '---=== SPACE INVADERS ===---'

class Cannon(Actor):
    def __init__(self, sprite, position):
        super(Cannon, self).__init__(sprite, position)
        self.speed = 5
        self.last_fire = 0
        self.firing_interval = 300
        
    def move_right(self):
        self.x += self.speed
        if self.right >= WIDTH - 40:
            self.right = WIDTH - 40
    
    def move_left(self):
        self.x -= self.speed
        if self.left <= 40:
            self.left = 40
            
class Bullet(Actor):
    def __init__(self, sprite, position):
        super(Bullet, self).__init__(sprite, position)
        self.speed = 20
  
    def update(self):
        self.y -= self.speed

    def is_dead(self):
        return self.bottom <= 0

class Alien(Actor):
    def __init__(self, sprite, position):
        super(Alien, self).__init__(sprite, position)
        self.movement = 20
        self.max_movement = 40
        self.x_speed = 1
        self.y_speed = 7
        self.lives = 3
         
    def update(self):
        self.x += self.x_speed
        self.movement += self.x_speed
        if abs(self.movement) >= self.max_movement:
            self.x_speed *= -1
            self.y += self.y_speed
            self.movement = 0                

    def is_dead(self):
        return self.lives == 0

class PlayScene:
    def __init__(self, game):
        self.cannon = Cannon('cannon', (WIDTH / 2, 560))
        self.bullets = []
        self.aliens = []
        self.score = 0
        self.create_aliens()

    def create_aliens(self):
        alien_x = 60
        alien_y = 40
        for i in range(5):
            for i in range(7):
                self.aliens.append(Alien('alien', (alien_x, alien_y)))
                alien_x += 60
            alien_x = 60
            alien_y += 40        

    def update(self):
        if keyboard.right:
            self.cannon.move_right()
        elif keyboard.left:
            self.cannon.move_left()
      
        if keyboard.space:
            if get_ticks() - self.cannon.last_fire > self.cannon.firing_interval:
                self.bullets.append(Bullet('bullet', self.cannon.pos))
                sounds.shot.play()
                self.cannon.last_fire = get_ticks()      

        for bullet in self.bullets[:]:
            bullet.update()
            if bullet.is_dead():
                self.bullets.remove(bullet)
        
        for alien in self.aliens[:]:
            alien.update()
            for bullet in self.bullets[:]:
                if alien.colliderect(bullet):
                    alien.lives -= 1
                    if alien.is_dead():
                        self.aliens.remove(alien)
                        sounds.explosion.play()
                        self.score += 100
                    self.bullets.remove(bullet)                
        
    def draw(self):
        screen.clear()
        self.cannon.draw()
      
        for bullet in self.bullets:
            bullet.draw()

        for alien in self.aliens:
            alien.draw()

        screen.draw.text("SCORE: %d" % self.score, (20, 20), fontname="space_invaders", fontsize=20)

class Game:
    def __init__(self):
        self.scenes = (PlayScene(self),)
        self.current_scene = 0
        
    def update(self):
        self.scenes[self.current_scene].update()
        
    def draw(self):
        self.scenes[self.current_scene].draw()

    def change_scene(self, new_scene):
        self.current_scene = new_scene
        
game = Game()
                          
def update():
    game.update()
    
def draw():
    game.draw()
