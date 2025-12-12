import random
import string
import tkinter as tk
import pygame
from tkinter import font as tkfont

def generate_password_legacy(length: int = 16) -> str:
    """Generate random password (legacy method)

    Args:
        length: Password length

    Returns:
        Generated password
    """
    password = ''
    char_ranges = [[97, 122], [65, 90], [48, 57], [33, 47]]
    for _ in range(length):
        char_range = random.choice(char_ranges)
        password += chr(random.randint(*char_range))
    return password


def generate_password(length: int = 16) -> str:
    """Generate secure random password

    Args:
        length: Password length

    Returns:
        Generated password
    """
    # Character sets
    characters = string.ascii_letters + string.digits + string.punctuation

    # Ensure password has at least one of each character type
    password_chars = [
        random.choice(string.ascii_lowercase),
        random.choice(string.ascii_uppercase),
        random.choice(string.digits),
        random.choice(string.punctuation)
    ]

    # Fill remaining characters
    password_chars.extend(random.choice(characters) for _ in range(length - 4))

    # Shuffle characters
    random.shuffle(password_chars)

    return ''.join(password_chars)


def generate_verification_code(length: int = 4) -> str:
    """Generate verification code

    Args:
        length: Code length

    Returns:
        Generated verification code
    """
    characters = string.ascii_letters + string.digits
    return ''.join(random.choices(characters, k=length))


def display_verification_code_tkinter(code: str):
    """Display verification code in Tkinter window

    Args:
        code: Verification code to display
    """
    root = tk.Tk()
    root.title("Verification Code")

    # Set window size and position
    window_width = 200
    window_height = 100
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width - window_width) // 2
    y = (screen_height - window_height) // 2
    root.geometry(f"{window_width}x{window_height}+{x}+{y}")

    # Create canvas
    canvas = tk.Canvas(root, width=window_width, height=window_height, bg='white')
    canvas.pack()

    # Set font
    custom_font = tkfont.Font(size=30, weight='bold')

    # Draw text
    canvas.create_text(window_width / 2, window_height / 2,
                       text=code,
                       font=custom_font)

    # Add noise lines
    for _ in range(5):
        x1 = random.randint(0, window_width)
        y1 = random.randint(0, window_height)
        x2 = random.randint(0, window_width)
        y2 = random.randint(0, window_height)
        canvas.create_line(x1, y1, x2, y2, fill='gray')

    root.mainloop()


def display_verification_code_pygame(code: str):
    """Display verification code in Pygame window

    Args:
        code: Verification code to display
    """
    pygame.init()

    # Setup window
    width, height = 200, 100
    screen = pygame.display.set_mode((width, height))
    pygame.display.set_caption("Verification Code")

    # Setup font
    font = pygame.font.Font(None, 60)

    # Main loop
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.locals.QUIT:
                running = False

        # White background
        screen.fill((255, 255, 255))

        # Render code
        text = font.render(code, True, (0, 0, 0))
        text_rect = text.get_rect(center=(width / 2, height / 2))

        # Add noise lines
        for _ in range(5):
            start_pos = (random.randint(0, width), random.randint(0, height))
            end_pos = (random.randint(0, width), random.randint(0, height))
            pygame.draw.line(screen, (128, 128, 128), start_pos, end_pos)

        screen.blit(text, text_rect)
        pygame.display.flip()

    pygame.quit()