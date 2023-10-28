import pygame
import mido

# Initialize pygame and create a window
pygame.init()
screen = pygame.display.set_mode((1450, 300))
pygame.display.set_caption("Onscreen Keyboard")


# Define some colors and fonts
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
FONT = pygame.font.SysFont("Arial", 20)

# Define the positions and sizes of the keys
KEY_WIDTH = 21
KEY_HEIGHT = 105
KEY_SPACING = 5
KEY_OFFSET_X = 50
KEY_OFFSET_Y = 100
WHITE_KEYS = [0, 2, 3, 5, 7, 8, 10]  # C D E F G A B
BLACK_KEYS = [1, 4, 6, 9, 11]  # C# D# F# G# A#
WHITE_KEY_RECTS = []  # List of rectangles for the white keys
BLACK_KEY_RECTS = []  # List of rectangles for the black keys
NOTE_NAMES = [
    "A",
    "A#",
    "B",
    "C",
    "C#",
    "D",
    "D#",
    "E",
    "F",
    "F#",
    "G",
    "G#",
]  # List of note names

# Create the rectangles for the white keys
x = KEY_OFFSET_X



for i in range(88):
    note = i % 12  # Get the note number in an octave
    if note in BLACK_KEYS:  # If it is a black key
        rect = pygame.Rect(
            x, KEY_OFFSET_Y, KEY_WIDTH // 2, KEY_HEIGHT // 2
        )  # Create a rectangle
        BLACK_KEY_RECTS.append(rect)  # Add it to the list

    if (
        note == 0
        or note == 2
        or note == 3
        or note == 5
        or note == 7
        or note == 8
        or note == 10
    ):  # If it's A, B, C, D, E, F, G (0, 2, 4, 5, 7, 9, 11)
        rect = pygame.Rect(
            x, KEY_OFFSET_Y, KEY_WIDTH, KEY_HEIGHT
        )  # Create a rectangle for white keys
        WHITE_KEY_RECTS.append(rect)
        x += KEY_WIDTH + KEY_SPACING  # Increment the x position


# Draw a border around the white keys
# Draw a border around the white keys
for rect in WHITE_KEY_RECTS:
    pygame.draw.rect(screen, BLACK, rect, 2)  # 2 is the border width


# Open the midi input port using mido
port = mido.open_input()

# A dictionary to store the pressed keys and their colors
pressed_keys = {}

# A loop to handle the events
running = True
while running:
    # Get the events from pygame and mido
    pygame_events = pygame.event.get()
    midi_events = port.iter_pending()

    # Handle the pygame events
    for event in pygame_events:
        if event.type == pygame.QUIT:  # If the user closes the window
            running = False  # Stop the loop

    # Handle the midi events
    for message in midi_events:
        if message.type == "note_on":  # If a note is pressed
            note = (
                message.note - 21
            )  # Get the note number (21 is the lowest note on an 88-key keyboard)
            print(note)
            velocity = message.velocity  # Get the velocity of the note
            if (
                velocity > 0
            ):  # If the note is actually on (some devices send note_on with zero velocity for note_off)
                color = (
                    velocity * 2,
                    velocity * 2,
                    velocity * 2,
                )  # Create a color based on the velocity (darker means softer)
                pressed_keys[
                    note
                ] = color  # Add the note and its color to the dictionary
        elif message.type == "note_off":  # If a note is released
            note = message.note - 21  # Get the note number
            if note in pressed_keys:  # If the note is in the dictionary
                del pressed_keys[note]  # Remove it from the dictionary

    # Fill the screen with black
    screen.fill(BLACK)

    # Draw the white keys
    for i, rect in enumerate(WHITE_KEY_RECTS):
        note = (
            WHITE_KEYS[i % len(WHITE_KEYS)] + (i // len(WHITE_KEYS)) * 12
        )  # Get the note number from the index
        if note in pressed_keys:  # If the note is pressed
            color = pressed_keys[note]  # Get its color
        else:  # If the note is not pressed
            color = WHITE  # Use white color
        pygame.draw.rect(screen, color, rect)  # Draw the rectangle
        text = FONT.render(NOTE_NAMES[note % 12], True, BLACK)  # Render the note name

        screen.blit(
            text, (rect.centerx - text.get_width() // 2, rect.bottom + KEY_SPACING)
        )  # Blit the text below the key

    # Draw the black keys
    for i, rect in enumerate(BLACK_KEY_RECTS):
        note = (
            BLACK_KEYS[i % len(BLACK_KEYS)] + (i // len(BLACK_KEYS)) * 12
        )  # Get the note number from the index
        if note in pressed_keys:  # If the note is pressed
            color = pressed_keys[note]  # Get its color
        else:  # If the note is not pressed
            color = BLACK  # Use black color
        pygame.draw.rect(screen, color, rect)  # Draw the rectangle

    # Update the display
    pygame.display.flip()

# Quit pygame and close the midi port
pygame.quit()
port.close()
