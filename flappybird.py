import pygame, random, os
pygame.init()

fps = pygame.time.Clock()
screen = pygame.display.set_mode([1280, 720])

WHITE = (255, 255, 255)

bg = pygame.image.load("flap\images\\flapbg.png")
bg = pygame.transform.scale(bg, (1280, 720))

btn_img = pygame.image.load("flap\images\\button.png")
btn_img = pygame.transform.scale(btn_img, (212, 101))

jumping = False
scroll_speed = 4
ground_scroll = 0
pipe_scroll = 800

def get_font(size):
    return pygame.font.SysFont('Futura', size)

class Button():
	def __init__(self, image, pos, text_input, font, base_color, hovering_color):
		self.image = image
		self.x_pos = pos[0]
		self.y_pos = pos[1]
		self.font = font
		self.base_color, self.hovering_color = base_color, hovering_color
		self.text_input = text_input
		self.text = self.font.render(self.text_input, True, self.base_color)
		if self.image is None:
			self.image = self.text
		self.rect = self.image.get_rect(center=(self.x_pos, self.y_pos))
		self.text_rect = self.text.get_rect(center=(self.x_pos, self.y_pos))

	def update(self, screen):
		if self.image is not None:
			screen.blit(self.image, self.rect)
		screen.blit(self.text, self.text_rect)

	def checkForInput(self, position):
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			return True
		return False

	def changeColor(self, position):
		if position[0] in range(self.rect.left, self.rect.right) and position[1] in range(self.rect.top, self.rect.bottom):
			self.text = self.font.render(self.text_input, True, self.hovering_color)
		else:
			self.text = self.font.render(self.text_input, True, self.base_color)

class Bird(pygame.sprite.Sprite):
    def __init__(self, vel, x, y):
        super().__init__()
        self.images = []
        self.index = 0
        self.counter = 0
        for num in range(1, 3):
            img = pygame.image.load(f'flap\images\\bird{num}.png')
            self.images.append(img)
        self.image = self.images[self.index]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.vel = vel
        self.clicked = False
        
    def update(self):
        
        self.vel += 0.5
        if self.vel > 8:
            self.vel = 8
        
        if self.rect.bottom < 720:
            self.rect.y += int(self.vel)

        if pygame.mouse.get_pressed()[0] == 1 and self.clicked == False:
                self.clicked = True
                self.vel = -10
        if pygame.mouse.get_pressed()[0] == 0:
            self.clicked = False
        
        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP and self.clicked == False:
                    self.clicked = True
                    self.vel = -10
                if event.key == pygame.K_SPACE and self.clicked == False:
                    self.clicked = True
                    self.vel = -10
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    self.clicked = False
                if event.key == pygame.K_SPACE:
                    self.clicked = False
            
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
    def collisions(self):
        collided = pygame.sprite.spritecollide(bird, collidables, False)
        if collided:
            collided = None
            game_over()
    
    def animation(self):
        self.counter += 1
        flap_cooldown = 10
        
        if self.counter > flap_cooldown:
            self.counter = 0
            self.index += 1
            if self.index >= len(self.images):
                self.index = 0
        self.image = self.images[self.index]
        self.image = pygame.transform.rotate(self.images[self.index], self.vel * -2)
              
class Ground(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('flap\images\ground.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (1800, 70))
        self.rect = self.image.get_rect()
        
        self.x = ground_scroll
        self.y = 650
        
        
    def scrolling(self):
        global ground_scroll
        ground_scroll -= scroll_speed
        self.x = ground_scroll
        self.rect.x = self.x
        self.rect.y = self.y
        if abs(ground_scroll) > 300:
            ground_scroll = 0

class Pipe(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = pygame.image.load('flap\images\pipe.png').convert_alpha()
        self.rect = self.image.get_rect()
        self.x = pipe_scroll
        self.y = 320
        
    def scrolling(self):
        global pipe_scroll
        pipe_scroll -= scroll_speed
        self.x = pipe_scroll
        self.rect.x = self.x
        self.rect.y = self.y
        if abs(pipe_scroll) < 0:
            self.kill()
    
bird_group = pygame.sprite.Group()  
bird = Bird(6, 300, 300)
bird_group.add(bird)

ground_group = pygame.sprite.Group()
ground = Ground()
ground_group.add(ground)

collidables = pygame.sprite.Group()
pipe = Pipe()
collidables.add(ground, pipe)
            
def game_loop():
    pygame.display.set_caption('Flap!')
    
    global score
    score = 0
    bird.rect.y = 300 
    global pipe_scroll
    pipe_scroll = 800
    global ground_scroll
    ground_scroll = 0
    
    title_font = pygame.font.SysFont('Futura', 110)
    score_text = title_font.render(f'Score: {score}', False, WHITE)
    title_rect = score_text.get_rect(center= (640, 100))
    
    while True:
        screen.fill((0, 0, 0))
        screen.blit(bg, (0,0))
        screen.blit(score_text, title_rect)
        
        bird_group.draw(screen)
        bird_group.update()
        collidables.draw(screen)
        
        bird.collisions()
        bird.animation()
        ground.scrolling()
        pipe.scrolling()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
        
        pygame.display.update()
        fps.tick(60)
        
def game_over():
    pygame.display.set_caption('Game Over!')
    
    title_font = pygame.font.SysFont('Futura', 80)
    game_over_title = title_font.render('Game Over!', False, WHITE)
    
    score_text = title_font.render(f'Score: {score}', True, (255, 0, 17))
    
    title_rect = game_over_title.get_rect(center= (640, 100))
    score_rect = score_text.get_rect(center= (640, 180))
    
    while True:
        screen.fill((0, 0, 0))
        screen.blit(bg, (0,0))
        screen.blit(game_over_title, title_rect)
        screen.blit(score_text, score_rect)
        
        MENU_MOUSE_POS = pygame.mouse.get_pos()
        
        quit_btn = Button(image=btn_img, pos=(640, 500), text_input="Quit",
                            font=get_font(75), base_color="White", hovering_color="#00d9ff")
        retry_btn = Button(image=btn_img, pos=(640, 350), text_input="Retry",
                            font=get_font(75), base_color="White", hovering_color="#00d9ff")
        
        for button in [quit_btn, retry_btn]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(screen)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if retry_btn.checkForInput(MENU_MOUSE_POS):
                    game_loop()
                if quit_btn.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    quit()

        pygame.display.update()
        fps.tick(60)
        
def main_menu():
    pygame.display.set_caption('Main Menu')
    
    title_font = pygame.font.SysFont('Futura', 110)
    title = title_font.render('Flappy Bird!', False, WHITE)
    title_rect = title.get_rect(center= (640, 100))
    while True:
        screen.fill((0, 0, 0))
        screen.blit(bg, (0,0))
        screen.blit(title, title_rect)
        
        MENU_MOUSE_POS = pygame.mouse.get_pos()
        
        quit_btn = Button(image=btn_img, pos=(640, 500), text_input="Quit",
                            font=get_font(75), base_color="White", hovering_color="#00d9ff")
        play_btn = Button(image=btn_img, pos=(640, 350), text_input="Play",
                            font=get_font(75), base_color="White", hovering_color="#00d9ff")
        
        for button in [quit_btn, play_btn]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(screen)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if play_btn.checkForInput(MENU_MOUSE_POS):
                    game_loop()
                if quit_btn.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    quit()

        pygame.display.update()
        fps.tick(60)
main_menu()