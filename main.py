import pygame
import time
import random

pygame.font.init()

HEIGHT, WIDTH = 700, 800
WIN= pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Space Dodger")

BG= pygame.transform.scale(pygame.image.load("bg3.jpg"),(WIDTH, HEIGHT)) #for the image file to not show any error drag the image directly into project folder then open the folder here

PLAYER_WIDTH, PLAYER_HEIGHT=   40, 60
PLAYER_VEL= 5

STAR_WIDTH = 10
STAR_HEIGHT = 20
STAR_VEL= 3

FONT = pygame.font.SysFont("comicsans",30)

def draw(player, elapsed_time, stars):
    WIN.blit(BG, (0, 0))

    time_text = FONT.render(f"Time: {round(elapsed_time)}s", 1, "white")
    WIN.blit(time_text, (10, 10))

    pygame.draw.rect(WIN, "red", player)

    for star in stars:
        pygame.draw.rect(WIN, "white", star)

    pygame.display.update()

def main():
    run= True
    player= pygame.Rect(200, HEIGHT - PLAYER_HEIGHT, PLAYER_WIDTH, PLAYER_HEIGHT)

    clock = pygame.time.Clock()

    start_time= time.time()
    elapsed_time= 0

    star_add_increment = 2000
    star_count = 0

    stars= []
    hit = False

    while run:
        star_count += clock.tick(60) #to set a fixed time for velocity so that PLAYER_VEL speed doesn't depend on computer speed
        elapsed_time= time.time() - start_time

        if star_count > star_add_increment:
            for _ in range(3):
                star_x = random.randint(0, WIDTH - STAR_WIDTH) #selecting x- coordinate as any random point within range of the horizontal screen
                star= pygame.Rect(star_x, -STAR_HEIGHT, STAR_WIDTH, STAR_HEIGHT) # selecting y-coordinate to be a little above the screen( hence the minus star height) so that players can't see where it's coming from
                stars.append(star)
            
            star_add_increment = max(200, star_add_increment - 50) #to make the star frequency gradually faster
            star_count = 0
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run =  False
                break

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - PLAYER_VEL>= 0: #function of left arrow button(K_LEFT) and setting condition so that character doesn't go out of left of screen
            player.x -= PLAYER_VEL
        if keys[pygame.K_RIGHT] and player.x + PLAYER_VEL + PLAYER_WIDTH <= WIDTH: #function of right arrow button(K_RIGHT) and setting condition so that character doesn't go out of right of screen
            player.x += PLAYER_VEL
        
        for star in stars[:]:
            star.y += STAR_VEL
            if star.y > HEIGHT: #to remove stars that hit bottom of screen
                stars.remove(star)
            elif star.y + star.height >= player.y and star.colliderect(player):
                stars.remove(star)
                hit= True
                break

        if hit:
            lost_text= FONT.render("You Lost!", 1, "white")
            score_text= FONT.render(f"Your Score: {round(elapsed_time)}", 1, "white")

            WIN.blit(lost_text, (WIDTH/2 - lost_text.get_width()/2, HEIGHT/2.25 - lost_text.get_height()/2.25))
            WIN.blit(score_text, (WIDTH/2 - score_text.get_width()/2, HEIGHT/2 - score_text.get_height()/2))
            pygame.display.update()
            pygame.time.delay(4000)
            break


        draw(player, elapsed_time, stars)
    pygame.quit()

if __name__ == "__main__":  #to get access only when the file is directly called
    main()
