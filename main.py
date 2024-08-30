import pygame

from settings import *
from colors import *
from PIL import Image
from collections import deque

# PyGame Setup
pygame.init()

if FULLSCREEN:
    SCREEN = pygame.display.set_mode(RESOLUTION, pygame.FULLSCREEN)
else:
    SCREEN = pygame.display.set_mode(RESOLUTION)

pygame.display.set_caption(WINDOW_NAME)
clock = pygame.time.Clock()
delta_time = 0

roboto = pygame.font.Font("Roboto.ttf", 32)


# Classes
class Text:
    def __init__(
        self,
        text,
        font,
        color,
        position,
        anti_aliasing,
        background=False,
        bg_color=(0, 0, 0),
    ):
        self.text = text
        self.font = font
        self.color = color
        self.position = position
        self.anti_aliasing = anti_aliasing
        self.background = background
        self.bg_color = bg_color

    def draw(self, pos):
        if not self.background:
            self.text = self.font.render(self.text, self.anti_aliasing, self.color)
        elif self.background:
            self.text = self.font.render(
                self.text, self.anti_aliasing, self.color, self.bg_color
            )

        self.text_rect = self.text.get_rect()

        if pos.lower() == "center":
            self.text_rect.center = (self.position[0], self.position[1])
        if pos.lower() == "bottom":
            self.text_rect.bottom = (self.position[0], self.position[1])
        if pos.lower() == "bottomleft":
            self.text_rect.bottomleft = (self.position[0], self.position[1])
        if pos.lower() == "bottomright":
            self.text_rect.bottomright = (self.position[0], self.position[1])
        if pos.lower() == "midbottom":
            self.text_rect.midbottom = (self.position[0], self.position[1])
        if pos.lower() == "midleft":
            self.text_rect.midleft = (self.position[0], self.position[1])
        if pos.lower() == "midright":
            self.text_rect.midright = (self.position[0], self.position[1])
        if pos.lower() == "midtop":
            self.text_rect.midtop = (self.position[0], self.position[1])
        if pos.lower() == "top":
            self.text_rect.top = (self.position[0], self.position[1])
        if pos.lower() == "topleft":
            self.text_rect.topleft = (self.position[0], self.position[1])
        if pos.lower() == "topright":
            self.text_rect.topright = (self.position[0], self.position[1])
        if pos.lower() == "left":
            self.text_rect.left = (self.position[0], self.position[1])
        if pos.lower() == "right":
            self.text_rect.right = (self.position[0], self.position[1])

        SCREEN.blit(self.text, self.text_rect)


# Functions
def brush(size, color):
    pygame.draw.circle(SCREEN, color, pygame.mouse.get_pos(), size)


def update_rainbow(speed, tup):
    # Convert the tuple to a list to allow modifications
    rainbow = list(tup)

    # Cycle through colors in a rainbow pattern
    if rainbow[0] == 255 and rainbow[1] < 255 and rainbow[2] == 0:
        # Transition from Red to Yellow (increase Green)
        rainbow[1] += speed
        if rainbow[1] > 255:
            rainbow[1] = 255
    elif rainbow[1] == 255 and rainbow[0] > 0 and rainbow[2] == 0:
        # Transition from Yellow to Green (decrease Red)
        rainbow[0] -= speed
        if rainbow[0] < 0:
            rainbow[0] = 0
    elif rainbow[1] == 255 and rainbow[2] < 255:
        # Transition from Green to Cyan (increase Blue)
        rainbow[2] += speed
        if rainbow[2] > 255:
            rainbow[2] = 255
    elif rainbow[2] == 255 and rainbow[1] > 0:
        # Transition from Cyan to Blue (decrease Green)
        rainbow[1] -= speed
        if rainbow[1] < 0:
            rainbow[1] = 0
    elif rainbow[2] == 255 and rainbow[0] < 255:
        # Transition from Blue to Magenta (increase Red)
        rainbow[0] += speed
        if rainbow[0] > 255:
            rainbow[0] = 255
    elif rainbow[0] == 255 and rainbow[2] > 0:
        # Transition from Magenta to Red (decrease Blue)
        rainbow[2] -= speed
        if rainbow[2] < 0:
            rainbow[2] = 0

    return tuple(rainbow)


def check_color(color_to_look_for, color_to_check, threshold):
    return (
        abs(color_to_look_for[0] - color_to_check[0]) <= threshold
        and abs(color_to_look_for[1] - color_to_check[1]) <= threshold
        and abs(color_to_look_for[2] - color_to_check[2]) <= threshold
    )


def paint_bucket(threshold, start_pos, fill_color):
    original_color = SCREEN.get_at(start_pos)[:3]  # Get the original color (R, G, B)

    if fill_color == original_color:
        return  # No need to fill if the color is the same

    queue = deque([start_pos])
    visited = set([start_pos])

    while queue:
        x, y = queue.popleft()

        current_color = SCREEN.get_at((x, y))[:3]

        if not check_color(original_color, current_color, threshold):
            continue

        # Change color of the current pixel
        SCREEN.set_at((x, y), fill_color)

        # Check neighbors
        for dx, dy in [(-1, 0), (1, 0), (0, -1), (0, 1)]:  # Left, Right, Up, Down
            nx, ny = x + dx, y + dy

            if 0 <= nx < WIDTH and 0 <= ny < HEIGHT and (nx, ny) not in visited:
                queue.append((nx, ny))
                visited.add((nx, ny))


def save_image():
    img = Image.new("RGB", (WIDTH, HEIGHT - 100), (255, 255, 255))

    pixels = img.load()

    for i in range(img.size[0]):
        for j in range(img.size[1]):
            new_color_value = list(SCREEN.get_at((i, j + 100)))
            new_color_value = tuple(new_color_value[: len(new_color_value) - 1])
            pixels[i, j] = new_color_value

    img.save("image.png")


SCREEN.fill(WHITE)
drawing = False
erasing = False
brush_size = 10
color = BLACK
rainbow_mode = False


def draw():
    if drawing:
        brush(brush_size, color)
    if erasing:
        brush(brush_size, WHITE)

    pygame.draw.rect(SCREEN, BLACK, pygame.Rect(0, 0, WIDTH, 100))

    brush_size_text = Text(f"Brush Size: {brush_size}", roboto, WHITE, (50, 50), True)
    brush_size_text.draw("midleft")

    tutorial = Text(
        f"LMB: Brush    RMB: Eraser    MMB: Paint Bucket    1-9: Colors    0: Rainbow    P : Save    ESC: Quit",
        roboto,
        WHITE,
        (WIDTH - 50, 50),
        True,
    )
    tutorial.draw("midright")

    color_text = Text(
        f"COLOR: {color}",
        roboto,
        color,
        (600, 50),
        True,
        True,
        bg_color=WHITE if color == BLACK else BLACK,
    )
    color_text.draw("center")

    pygame.display.flip()


def main():
    global delta_time
    global drawing
    global erasing
    global brush_size
    global color
    global RAINBOW
    global rainbow_mode

    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                if event.key == pygame.K_1:
                    color = BLACK
                    rainbow_mode = False
                if event.key == pygame.K_2:
                    color = GRAY
                    rainbow_mode = False
                if event.key == pygame.K_3:
                    color = WHITE
                    rainbow_mode = False
                if event.key == pygame.K_4:
                    color = RED
                    rainbow_mode = False
                if event.key == pygame.K_5:
                    color = GREEN
                    rainbow_mode = False
                if event.key == pygame.K_6:
                    color = BLUE
                    rainbow_mode = False
                if event.key == pygame.K_7:
                    color = YELLOW
                    rainbow_mode = False
                if event.key == pygame.K_8:
                    color = PURPLE
                    rainbow_mode = False
                if event.key == pygame.K_9:
                    color = CYAN
                    rainbow_mode = False
                if event.key == pygame.K_0:
                    rainbow_mode = True  # Toggle rainbow mode
                    if not rainbow_mode:
                        color = RAINBOW  # Reset to start of rainbow when turning off
                if event.key == pygame.K_p:
                    save_image()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    drawing = True
                if event.button == 2:
                    if pygame.mouse.get_pos()[1] > 100:
                        paint_bucket(5, pygame.mouse.get_pos(), color)
                if event.button == 3:
                    erasing = True
            if event.type == pygame.MOUSEBUTTONUP:
                if event.button == 1:
                    drawing = False
                if event.button == 3:
                    erasing = False
            if event.type == pygame.MOUSEWHEEL:
                if event.y > 0:
                    brush_size += 1
                if event.y < 0:
                    brush_size -= 1

        if erasing and drawing:
            erasing = False

        if brush_size < 1:
            brush_size = 1

        if rainbow_mode:
            RAINBOW = update_rainbow(2, RAINBOW)  # Update the rainbow color
            color = RAINBOW  # Set the brush color to the updated rainbow color

        RAINBOW = update_rainbow(2, RAINBOW)
        draw()
        delta_time = 1 / clock.tick(FPS)

    pygame.quit()


if __name__ == "__main__":
    main()
