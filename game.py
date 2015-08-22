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

class Explosion(Actor):
    def __init__(self, sprite, position):
        super(Explosion, self).__init__(sprite, position)
        self.tick_limit = 15
        self.ticks = 0
        self.finished = False
        
    def update(self):
        self.ticks += 1
        if self.ticks > self.tick_limit:
            self.finished = True
        
    def is_finished(self):
        return self.finished
        
class MenuScene:
    def __init__(self, game):
        self.game = game
        self.sprites = (
            Cannon('cannon', (WIDTH/2, 420)),
            Bullet('bullet', (WIDTH/2, 360)),
            Alien('alien', (WIDTH/2, 220))
        )
        
    def update(self):
        if keyboard.s:
            self.game.change_scene(1)
        
    def draw(self):
        screen.clear()
        
        for sprite in self.sprites:
            sprite.draw()
            
        screen.draw.text("S P A C E", (140, 40), fontname="space_invaders", fontsize=40)
        screen.draw.text("I N V A D E R S", (85, 100), fontname="space_invaders", fontsize=40)
        screen.draw.text("PRESS 'S' TO START", (125, 520), fontname="space_invaders", fontsize=20)

class PlayScene:
    def __init__(self, game):
        self.game = game
        self.cannon = Cannon('cannon', (WIDTH / 2, 560))
        self.bullets = []
        self.aliens = []
        self.explosions = []
        self.score = 0
        self.create_aliens()
        self.running = True

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
        if self.running:
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
                if self.cannon.colliderect(alien):
                    self.explosions.append(Explosion('cannon_explosion', self.cannon.pos))
                    sounds.explosion.play()
                    self.running = False
                for bullet in self.bullets[:]:
                    if alien.colliderect(bullet):
                        alien.lives -= 1
                        if alien.is_dead():
                            self.explosions.append(Explosion('alien_explosion', alien.pos))
                            sounds.explosion.play()
                            self.aliens.remove(alien)
                            self.score += 100
                        self.bullets.remove(bullet)                
            
            for explosion in self.explosions[:]:
                explosion.update()
                if explosion.is_finished():
                    self.explosions.remove(explosion)
        else:
            for explosion in self.explosions[:]:
                explosion.update()
                if explosion.is_finished():
                    self.explosions.remove(explosion)
            if len(self.explosions) == 0:
                self.game.change_scene(2)

    def draw(self):
        screen.clear()
        self.cannon.draw()
      
        for bullet in self.bullets:
            bullet.draw()

        for alien in self.aliens:
            alien.draw()
        
        for explosion in self.explosions:
            explosion.draw()
            
        screen.draw.text("SCORE: %d" % self.score, (20, 20), fontname="space_invaders", fontsize=20)

class GameOverScene:
    def __init__(self, game):
        pass
        
    def update(self):
        pass
        
    def draw(self):
        pass

class Game:
    def __init__(self):
        self.scenes = (MenuScene(self), PlayScene(self), GameOverScene(self))
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
