from random import randint
import curses

# TODO: Fix the 'invisible food' bug.

# Initializes the screen.
# TODO: create a black background for the whole window.
screen = curses.initscr()
curses.start_color()
curses.init_pair(1, curses.COLOR_RED, curses.COLOR_BLACK)
curses.init_pair(2, curses.COLOR_GREEN, curses.COLOR_BLACK)

# Sets the cursor to be invisible (0 for invisible, 1 for normal, 2 for very visible)
curses.curs_set(0)

# sh, sw = screen height, screen width
sh, sw = screen.getmaxyx()
window = curses.newwin(sh - 3, sw, 0, 0)

# Draw info window below main game play window.
window2 = curses.newwin(3, sw, sh - 3, 0)
window2.border(0)
window2.refresh()

# Allows the window to accept key presses from the user.
window.keypad(True)


# Set snake start position.
snake_y = sh // 2
snake_x = sw // 4

# Creates snake head and body variables. snake_head is index 0 of snake_body.
snake_head = [snake_y, snake_x]
snake_body = [
    [snake_y, snake_x],
    [snake_y, snake_x - 1],
    [snake_y, snake_x - 2]
]

# Creates food and score variables.
food = [sh // 2, sw // 2]
score = 0

# Sets food start position on the screen.
# Reference for NCURSES Extended Characters:
# http://www.melvilletheatre.com/articles/ncurses-extended-characters/index.html
window.addch(food[0], food[1], 96, curses.ACS_DIAMOND | curses.color_pair(1))


# Sets variables for snake movement.
prev_button_direction = 1
button_direction = 1
key = curses.KEY_RIGHT


def collision_with_snake(snake_body):
    """Use to trigger 'game over; if snake_head collides with snake_body."""
    snake_head = snake_body[0]
    if snake_head in snake_body[1:]:
        return 1
    else:
        return 0


def collision_with_walls(snake_body):
    """Use to trigger 'game over; if snake_head collides with walls."""
    if snake_body[0][0] > sh-5 or snake_body[0][0] < 1 or snake_body[0][1] > sw-2 or snake_body[0][1] < 1:
        return 1
    else:
        return 0


def food_placement():
    """Places food at a random coordinate in the window, excluding coordinates in snake_body."""
    exclude = snake_body
    food = [randint(2, sh-5), randint(2, sw-2)]
    return food_placement() if food in exclude else food


def collision_with_food(score):
    """Updates score when food is eaten."""
    score += 1
    return score


# Main game play loop begins here:
while True:
    window.border(0)
    window.timeout(100)
    window2.addstr(1, sw // 4, f"Score: {score}")
    window2.refresh()

    # Get user input.
    next_key = window.getch()

    if next_key == -1:
        key = key
    else:
        key = next_key

    # 0-Left, 1-Right, 3-Up, 2-Down
    if key == curses.KEY_LEFT and prev_button_direction != 1:
        button_direction = 0
    elif key == curses.KEY_RIGHT and prev_button_direction != 0:
        button_direction = 1
    elif key == curses.KEY_UP and prev_button_direction != 2:
        button_direction = 3
    elif key == curses.KEY_DOWN and prev_button_direction != 3:
        button_direction = 2
    else:
        pass

    prev_button_direction = button_direction

    # Change the head position based on the button direction
    if button_direction == 1:
        snake_head[1] += 1
    elif button_direction == 0:
        snake_head[1] -= 1
    elif button_direction == 2:
        snake_head[0] += 1
        curses.napms(30)
    elif button_direction == 3:
        snake_head[0] -= 1
        curses.napms(30)

    if snake_head == food:
        # Updates score, food placement, and snake_body length.
        score = collision_with_food(score)
        food = food_placement()
        snake_body.insert(0, list(snake_head))
        window.addch(food[0], food[1], 96, curses.ACS_DIAMOND | curses.color_pair(1))
    else:
        # Animate snake movement by adding to and removing from snake body.
        snake_body.insert(0, list(snake_head))
        last = snake_body.pop()
        window.addch(last[0], last[1], ' ')

    # Display the whole snake on the screen.
    window.addch(snake_body[0][0], snake_body[0][1], 97, curses.ACS_CKBOARD | curses.color_pair(2))

    # Kill the snake if it collides with walls or itself.
    if collision_with_walls(snake_body) == 1 or collision_with_snake(snake_body) == 1:
        break


# Display final score and ends curses window.
window.addstr(sh // 2, sw // 4, f"Your score: {score}")
window.refresh()
curses.napms(5000)
curses.endwin()
