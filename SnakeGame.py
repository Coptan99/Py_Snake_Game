import random
import curses

name = input("Enter your name: ")
difficulty = input("Choose your difficulty: (easy/medium/hard): ")
if difficulty == "easy":
    delay = 130
elif difficulty == "medium":
    delay = 125
elif difficulty == "hard":
    delay = 100
else:
    print("Unknown input")

# Initalize the curses library to create our screen
screen = curses.initscr()

# Hide the mouse cursor
curses.curs_set(0)

# Getmax screen height and width
screen_height, screen_width = screen.getmaxyx()

# Create a new window
window = curses.newwin(screen_height, screen_width, 0, 0)

# Allow window to receive input from keyboard
window.keypad(1)

# Set the delay to update the screen
# window.timeout(delay)
window.timeout(125)

# Set the x, y coordinates of the initial position of the snake's head and the score
snk_x = screen_width // 4  # Integer division
snk_y = screen_height // 2

# Define the initial position of the snake body
snake = [
    [snk_y, snk_x],
    [snk_y, snk_x-1],
    [snk_y, snk_x-2]
]

# Declare positions
food = [screen_height // 2, screen_width // 2]
name_position = [0, 0]
score_position = [1, 0]
score = 0

# Add food by using PI character from curses module
window.addch(food[0], food[1], curses.ACS_DIAMOND)
window.addstr(name_position[0], name_position[1], "Name: " + str(name))
window.addstr(score_position[0], score_position[1], "Score: " + str(score))

# Set initial movement direction to right
key = curses.KEY_RIGHT

# Create game loop that loops forever until player loses or quits the game
while True:

    # Get the next key that will be pressed by the user
    next_key = window.getch()

    # If the user doesn't input anything, key remains same, else key will be set to the new
    key = key if next_key == -1 else next_key

    # Check if the snake collided with the wall or itself
    if snake[0][0] in [0, screen_height] or snake[0][1] in [0, screen_width] or snake[0] in snake[1:]:
        curses.endwin()  # Closing the window
        score_file = open("scores.txt", "a")
        score_file.write("\n" + name + ": " + str(score) + " (" + difficulty + ")")
        score_file.close()
        print(name, ":", score)
        quit()
    new_head = [snake[0][0], snake[0][1]]
    if key == curses.KEY_DOWN:
        new_head[0] += 1
    elif key == curses.KEY_UP:
        new_head[0] -= 1
    elif key == curses.KEY_RIGHT:
        new_head[1] += 1
    elif key == curses.KEY_LEFT:
        new_head[1] -= 1

    # Insert the new head to the snake list
    snake.insert(0, new_head)

    # Check if the snake ate the food
    if snake[0] == food:
        # Remove food if snake ate it
        food = None
        score += 1

        # Generate a new food if the snake ate it
        while food is None:
            new_food = [
                random.randint(1, screen_height - 1),
                random.randint(1, screen_width - 1)
            ]

            # Set the food to new food if the generated is not in the snake body
            food = new_food if new_food not in snake else None
        window.addch(food[0], food[1], curses.ACS_DIAMOND)
    else:
        # Otherwise remove the last segment of the snake body
        tail = snake.pop()
        window.addch(tail[0], tail[1], ' ')

    # Update the position of the snake on the screen
    window.addch(snake[0][0], snake[0][1], curses.ACS_CKBOARD)

    # Clear the previous score display
    window.addstr(score_position[0], score_position[1], " " * (len("Score: ") + len(str(score))))

    # Update the score display
    window.addstr(score_position[0], score_position[1], "Score: " + str(score))
