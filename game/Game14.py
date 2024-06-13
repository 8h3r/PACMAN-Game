import os
import sys
import pygame
import Levels

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
PURPLE = (255, 0, 255)
SKYBLUE = (0, 191, 255)
BGMPATH = os.path.join(os.getcwd(), 'resources/sounds/bg.mp3')
ICONPATH = os.path.join(os.getcwd(), 'resources/images/icon.png')
FONTPATH = os.path.join(os.getcwd(), 'resources/font/ALGER.TTF')
HEROPATH = os.path.join(os.getcwd(), 'resources/images/pacman.png')
BlinkyPATH = os.path.join(os.getcwd(), 'resources/images/Blinky.png')
ClydePATH = os.path.join(os.getcwd(), 'resources/images/Clyde.png')
InkyPATH = os.path.join(os.getcwd(), 'resources/images/Inky.png')
PinkyPATH = os.path.join(os.getcwd(), 'resources/images/Pinky.png')

def startLevelGame(level, screen, font):
    clock = pygame.time.Clock()
    SCORE = 0
    wall_sprites = level.setupWalls(SKYBLUE)
    gate_sprites = level.setupGate(WHITE)
    hero_sprites, ghost_sprites = level.setupPlayers("E:/Documents/game/files/pacman.png", ["E:/Documents/game/files/Blinky.png", "E:/Documents/game/files/Clyde.png", "E:/Documents/game/files/Inky.png","E:/Documents/game/files/Pinky.png"])
    food_sprites = level.setupFood(YELLOW, WHITE)
    is_clearance = False

    # Load sound effects
    eat_sound = pygame.mixer.Sound("E:/Documents/game/audio/eat.wav")  # Load eat sound effect
    die_sound = pygame.mixer.Sound("E:/Documents/game/audio/die.wav")  # Load die sound effect

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit(-1)
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or event.key == pygame.K_a:
                    for hero in hero_sprites:
                        hero.changeSpeed([-1, 0])
                        hero.is_move = True
                elif event.key == pygame.K_RIGHT or event.key == pygame.K_d:
                    for hero in hero_sprites:
                        hero.changeSpeed([1, 0])
                        hero.is_move = True
                elif event.key == pygame.K_UP or event.key == pygame.K_w:
                    for hero in hero_sprites:
                        hero.changeSpeed([0, -1])
                        hero.is_move = True
                elif event.key == pygame.K_DOWN or event.key == pygame.K_s:
                    for hero in hero_sprites:
                        hero.changeSpeed([0, 1])
                        hero.is_move = True
            if event.type == pygame.KEYUP:
                if (event.key == pygame.K_LEFT or event.key == pygame.K_a) or (event.key == pygame.K_RIGHT or event.key == pygame.K_d) or (event.key == pygame.K_UP or event.key == pygame.K_w) or (event.key == pygame.K_DOWN or event.key == pygame.K_s):
                    hero.is_move = False
        screen.fill(BLACK)
        for hero in hero_sprites:
            hero.update(wall_sprites, gate_sprites)
        hero_sprites.draw(screen)
        for hero in hero_sprites:
            food_eaten = pygame.sprite.spritecollide(hero, food_sprites, True)
            for food in food_eaten:
                eat_sound.play()  # Play eat sound effect
        SCORE += len(food_eaten)
        wall_sprites.draw(screen)
        gate_sprites.draw(screen)
        food_sprites.draw(screen)
        for ghost in ghost_sprites:
            if ghost.tracks_loc[1] < ghost.tracks[ghost.tracks_loc[0]][2]:
                ghost.changeSpeed(ghost.tracks[ghost.tracks_loc[0]][0: 2])
                ghost.tracks_loc[1] += 1
            else:
                if ghost.tracks_loc[0] < len(ghost.tracks) - 1:
                    ghost.tracks_loc[0] += 1
                elif ghost.role_name == 'Clyde':
                    ghost.tracks_loc[0] = 2
                else:
                    ghost.tracks_loc[0] = 0
                ghost.changeSpeed(ghost.tracks[ghost.tracks_loc[0]][0: 2])
                ghost.tracks_loc[1] = 0
            if ghost.tracks_loc[1] < ghost.tracks[ghost.tracks_loc[0]][2]:
                ghost.changeSpeed(ghost.tracks[ghost.tracks_loc[0]][0: 2])
            else:
                if ghost.tracks_loc[0] < len(ghost.tracks) - 1:
                    loc0 = ghost.tracks_loc[0] + 1
                elif ghost.role_name == 'Clyde':
                    loc0 = 2
                else:
                    loc0 = 0
                ghost.changeSpeed(ghost.tracks[loc0][0: 2])
            ghost.update(wall_sprites, None)
        ghost_sprites.draw(screen)
        score_text = font.render("Score: %s" % SCORE, True, RED)
        screen.blit(score_text, [10, 10])
        if len(food_sprites) == 0:
            is_clearance = True
            break
        if pygame.sprite.groupcollide(hero_sprites, ghost_sprites, False, False):
            die_sound.play()  # Play die sound effect
            is_clearance = False
            break
        pygame.display.flip()
        clock.tick(10)
    return is_clearance

def showText(screen, font, is_clearance, flag=False):
	clock = pygame.time.Clock()
	msg = 'Game Over!' if not is_clearance else 'Congratulations, you won!'
	positions = [[235, 233], [65, 303], [170, 333]] if not is_clearance else [[145, 233], [65, 303], [170, 333]]
	surface = pygame.Surface((400, 200))
	surface.set_alpha(10)
	surface.fill((128, 128, 128))
	screen.blit(surface, (100, 200))
	texts = [font.render(msg, True, WHITE),
			 font.render('Press ENTER to continue or play again.', True, WHITE),
			 font.render('Press ESCAPE to quit.', True, WHITE)]
	while True:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				sys.exit()
				pygame.quit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_RETURN:
					if is_clearance:
						if not flag:
							return
						else:
							main(initialize())
					else:
						main(initialize())
				elif event.key == pygame.K_ESCAPE:
					sys.exit()
					pygame.quit()
		for idx, (text, position) in enumerate(zip(texts, positions)):
			screen.blit(text, position)
		pygame.display.flip()
		clock.tick(10)

def initialize():
	pygame.init()
	icon_image = pygame.image.load("E:/Documents/game/files/icon.png")
	pygame.display.set_icon(icon_image)
	screen = pygame.display.set_mode([606, 606])
	pygame.display.set_caption('Pacman')
	return screen

def showAbout(screen, font):
    clock = pygame.time.Clock()
    about_bg = pygame.image.load("E:/Documents/game/files/bg.jpg")  # Load about background image
    screen.blit(about_bg, (0, 0))

    msg = 'Pacman game created with Pygame by ATHER!'
    surface = pygame.Surface((400, 200))
    surface.set_alpha(10)
    surface.fill((128, 128, 128))
    screen.blit(surface, (100, 350))  # Adjusted position to prevent overlap
    text = font.render(msg, True, WHITE)
    screen.blit(text, [(screen.get_width() // 2) - (text.get_width() // 2), 383])  # Adjusted position to prevent overlap

    back_text = font.render("Press ESCAPE to go back", True, WHITE)
    screen.blit(back_text, [(screen.get_width() // 2) - (back_text.get_width() // 2), 433])  # Added back button text

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return showLevelMenu(screen, font)  # Go back to the main menu

        pygame.display.flip()
        clock.tick(10)
def showLevelMenu(screen, font):
    clock = pygame.time.Clock()
    menu_bg = pygame.image.load("E:/Documents/game/files/bg.jpg")  # Load background image
    screen.blit(menu_bg, (0, 0))

    # Sound effects (optional)
    pygame.mixer.init()
    hover_sound = pygame.mixer.Sound("E:/Documents/game/audio/hover.wav")  # Load hover sound
    click_sound = pygame.mixer.Sound("E:/Documents/game/audio/click.wav")  # Load click sound

    title_text = font.render("Pacman Game", True, WHITE)
    title_rect = title_text.get_rect(midtop=(screen.get_width() // 2, 50))
    screen.blit(title_text, title_rect)

    menu_options = ["Play", "About", "Exit"]
    menu_rects = []

    for i, option in enumerate(menu_options):
        option_text = font.render(option, True, WHITE)
        option_rect = option_text.get_rect(midtop=(screen.get_width() // 2, 150 + i * 50))
        menu_rects.append(option_rect)
        screen.blit(option_text, option_rect)

    mouse_hover = None  # Track which option is hovered over (or None if not hovering)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEMOTION:
                # Check for hover over menu options
                new_hover = None
                for rect in menu_rects:
                    if rect.collidepoint(event.pos):
                        new_hover = rect
                        break  # Exit loop if hovering over any option
                mouse_hover = new_hover
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if mouse_hover:  # Check if hovering over an option before clicking
                    click_sound.play()
                    if mouse_hover == menu_rects[0]:  # Play option
                        return showLevelList(screen, font)
                    elif mouse_hover == menu_rects[1]:  # About option
                        showAbout(screen, font)
                    elif mouse_hover == menu_rects[2]:  # Exit option
                        sys.exit()

        # Hover animation (optional)
        if mouse_hover:
            for i, rect in enumerate(menu_rects):
                if rect == mouse_hover:
                    new_color = (255, 200, 0)  # Example: slightly yellow on hover
                    new_text = font.render(menu_options[i], True, new_color)
                    screen.blit(new_text, rect)
                    break  # Only apply hover effect to the hovered option
        else:
            # Reset hover effect if mouse not hovering over any option
            for rect in menu_rects:
                screen.blit(font.render(menu_options[rect.y // 50 - 3], True, WHITE), rect)  # Restore default text

        pygame.display.flip()
        clock.tick(60)

def showLevelList(screen, font):
    clock = pygame.time.Clock()
    menu_bg = pygame.image.load("E:/Documents/game/files/bg.jpg")  # Load background image
    screen.blit(menu_bg, (0, 0))

    # Sound effects (optional)
    pygame.mixer.init()
    hover_sound = pygame.mixer.Sound("E:/Documents/game/audio/hover.wav")  # Load hover sound
    click_sound = pygame.mixer.Sound("E:/Documents/game/audio/click.wav")  # Load click sound

    title_text = font.render("Select Level", True, WHITE)
    title_rect = title_text.get_rect(midtop=(screen.get_width() // 2, 50))
    screen.blit(title_text, title_rect)

    level_options = [f"Level {i}" for i in range(1, Levels.NUMLEVELS + 1)]
    level_rects = []

    for i, option in enumerate(level_options):
        option_text = font.render(option, True, WHITE)
        option_rect = option_text.get_rect(midtop=(screen.get_width() // 2, 150 + i * 50))  # Centered level options
        level_rects.append(option_rect)
        screen.blit(option_text, option_rect)

    back_text = font.render("Press ESCAPE to go back", True, WHITE)
    screen.blit(back_text, [(screen.get_width() // 2) - (back_text.get_width() // 2), screen.get_height() - 50])  # Added back button text

    mouse_hover = None  # Track which option is hovered over (or None if not hovering)

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys.exit()
            elif event.type == pygame.MOUSEMOTION:
                # Check for hover over level options
                new_hover = None
                for rect in level_rects:
                    if rect.collidepoint(event.pos):
                        new_hover = rect
                        break  # Exit loop if hovering over any option
                mouse_hover = new_hover
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if mouse_hover:  # Check if hovering over an option before clicking
                    click_sound.play()
                    selected_level = mouse_hover.y // 50 + 1
                    level_class = Levels.Level1 if selected_level == 1 else Levels.Level2
                    level = level_class()
                    is_clearance = startLevelGame(level, screen, font)
                    if selected_level == Levels.NUMLEVELS:
                        showText(screen, font, is_clearance, True)
                    else:
                        showText(screen, font, is_clearance)
                    return  # Go back to the main menu after the game ends
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    return showLevelMenu(screen, font)  # Go back to the main menu

        # Hover animation (optional)
        if mouse_hover:
            for i, rect in enumerate(level_rects):
                if rect == mouse_hover:
                    new_color = (255, 200, 0)  # Example: slightly yellow on hover
                    new_text = font.render(level_options[i], True, new_color)
                    screen.blit(new_text, rect)
                    break  # Only apply hover effect to the hovered option
        else:
            # Reset hover effect if mouse not hovering over any option
            for rect in level_rects:
                screen.blit(font.render(level_options[rect.y // 50 - 3], True, WHITE), rect)  # Restore default text

        pygame.display.flip()
        clock.tick(60)

def main(screen):
    pygame.mixer.init()
    pygame.font.init()
    font_small = pygame.font.Font("E:/Documents/game/files/ALGER.TTF", 18)
    font_big = pygame.font.Font("E:/Documents/game/files/ALGER.TTF", 24)

    selected_level = showLevelMenu(screen, font_big)

    level_class = Levels.Level1 if selected_level == 1 else Levels.Level2
    level = level_class()

    is_clearance = startLevelGame(level, screen, font_small)
    if selected_level == Levels.NUMLEVELS:
        showText(screen, font_big, is_clearance, True)
    else:
        showText(screen, font_big, is_clearance)

if __name__ == '__main__':
    main(initialize())