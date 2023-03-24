import game_state as gs
import boards as b
import algorithms as alg
import pygame
import time

# initialize Pygame
pygame.init()

def draw_board(board):

    # display window
    size = board["size"]
    cell_size = 50
    width = size[0] * cell_size
    height = size[1] * cell_size
    screen = pygame.display.set_mode((width, height))

    # define colors
    BLACK = (0, 0, 0)
    WHITE = (255, 255, 255)
    RED = (255, 0, 0)
    BLUE = (0, 0, 255)
    YELLOW = (255, 255, 0)
    BRIGHT_YELLOW = (255, 215, 0)

    # draw the blank squares
    for pos in board["blank"]:
        rect = pygame.Rect(pos[0] * cell_size, pos[1] * cell_size, cell_size, cell_size)
        pygame.draw.rect(screen, WHITE, rect)

    # draw the colored pieces
    for color, pieces in board.items():
        if color == "blank" or color == "size":
            continue
        color_value = None
        if color == "red":
            color_value = RED
        elif color == "blue":
            color_value = BLUE
        elif color == "yellow":
            color_value = BRIGHT_YELLOW 
        elif color == "orange":
            color_value = pygame.Color('orange')
        if color_value is not None:
            for size, positions in pieces.items():
                for pos in positions:
                    rect = pygame.Rect(pos[0] * cell_size, pos[1] * cell_size, cell_size, cell_size)
                    pygame.draw.rect(screen, color_value, rect)

    # update the display
    pygame.display.flip()


def draw_boards(boards):

    # loop through the boards and draw them with a delay of 1 second
    for board in boards:
        draw_board(board)

        # wait for 1 second
        time.sleep(1)

    # set up the screen
    screen_width = 800
    screen_height = 600
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Cohesion")

    # set up font
    font = pygame.font.SysFont(None, 48)

    # define colors
    black = (0, 0, 0)
    white = (255, 255, 255)
    main_menu()




# set up the screen
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Cohesion")

# set up font
font = pygame.font.SysFont(None, 48)

# define colors
black = (0, 0, 0)
white = (255, 255, 255)

# define button class
class Button:
    def __init__(self, x, y, width, height, text, color, highlight_color, action=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.color = color
        self.highlight_color = highlight_color
        self.action = action
        self.highlighted = False
    
    def draw(self, surface):
        color = self.color
        pygame.draw.rect(surface, color, self.rect)
        text_surface = font.render(self.text, True, white)
        text_rect = text_surface.get_rect(center=self.rect.center)
        surface.blit(text_surface, text_rect)
    
    def handle_event(self, event):
        if event.type == pygame.MOUSEMOTION:
            self.highlighted = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos) and self.action:
                self.action()

class Piece:
    def __init__(self, color, squares):
        self.color = color
        self.squares = squares
        self.selected = False
        self.offset_x = 0
        self.offset_y = 0
        
    def draw(self, screen):
        for square in self.squares:
            pygame.draw.rect(screen, self.color, square)
            pygame.draw.rect(screen, black, square, 1)

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_pos = event.pos
            for square in self.squares:
                if square.collidepoint(mouse_pos):
                    self.selected = True
                    self.offset_x = square.x - mouse_pos[0]
                    self.offset_y = square.y - mouse_pos[1]
        elif event.type == pygame.MOUSEBUTTONUP and event.button == 1:
            self.selected = False
        elif event.type == pygame.MOUSEMOTION and self.selected:
            mouse_pos = event.pos
            for square in self.squares:
                square.x = mouse_pos[0] + self.offset_x
                square.y = mouse_pos[1] + self.offset_y


# define main menu
def main_menu():
    # define buttons
    play_button = Button(260, 200, 250, 50, "Play", black, white, puzzle_menu_player)
    ai_button = Button(260, 300, 250, 50, "Solve with AI", black, white, puzzle_menu_ai)
    quit_button = Button(260, 400, 250, 50, "Quit", black, white, pygame.quit)
    buttons = [play_button, ai_button, quit_button]
    
    # wait for the user to close the window
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            for button in buttons:
                button.handle_event(event)
        # draw background
        screen.fill(white)
        # draw buttons
        for button in buttons:
            button.draw(screen)
        pygame.display.flip()

# define puzzle menu
def puzzle_menu_player():
    # define buttons
    puzzle1_button = Button(300, 200, 200, 50, "Puzzle 1", black, white, lambda: playable_game(b.b1))
    puzzle2_button = Button(300, 300, 200, 50, "Puzzle 2", black, white, lambda: playable_game(b.b3))
    puzzle3_button = Button(300, 400, 200, 50, "Puzzle 3", black, white, lambda: playable_game(b.b6))
    back_button = Button(300, 500, 200, 50, "Back", black, white, main_menu)
    buttons = [puzzle1_button, puzzle2_button, puzzle3_button, back_button]
    
    # wait for the user to close the window
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            for button in buttons:
                button.handle_event(event)
        # draw background
        screen.fill(white)
        # draw buttons
        for button in buttons:
            button.draw(screen)
        pygame.display.flip()


def puzzle_menu_ai():
    # define buttons
    puzzle1_button = Button(300, 200, 200, 50, "Puzzle 1", black, white, lambda: alg_menu(b.b1,b.b1_sol))
    puzzle2_button = Button(300, 300, 200, 50, "Puzzle 2", black, white, lambda: alg_menu(b.b3,b.b3_sol))
    puzzle3_button = Button(300, 400, 200, 50, "Puzzle 3", black, white, lambda: alg_menu(b.b6,b.b6_sol))
    back_button = Button(300, 500, 200, 50, "Back", black, white, main_menu)
    buttons = [puzzle1_button, puzzle2_button, puzzle3_button, back_button]
    
    # wait for the user to close the window
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            for button in buttons:
                button.handle_event(event)
        # draw background
        screen.fill(white)
        # draw buttons
        for button in buttons:
            button.draw(screen)
        pygame.display.flip()

def choose_func(al,h,board,bsol):
    if al == 1 and h == 1:
        draw_boards(alg.greedy_search(gs.CohesionState(board,[]),bsol,alg.h1)[0])
    elif al == 1 and h == 2:
        draw_boards(alg.greedy_search(gs.CohesionState(board,[]),bsol,alg.h2)[0])
    elif al == 2 and h == 1:
        draw_boards(alg.a_star_search(gs.CohesionState(board,[]),bsol,alg.h1)[0])
    elif al == 2 and h == 2:
        draw_boards(alg.a_star_search(gs.CohesionState(board,[]),bsol,alg.h2)[0])
    elif al == 3 and h == 1:
        draw_boards(alg.weighted_a_star_search(gs.CohesionState(board,[]),bsol,alg.h1,3)[0])
    elif al == 3 and h == 2:
        draw_boards(alg.weighted_a_star_search(gs.CohesionState(board,[]),bsol,alg.h2,3)[0])

def heuristic_menu(alg,board,bsol):
    # define buttons
    puzzle1_button = Button(300, 200, 200, 50, "Heuristic 1", black, white, lambda: choose_func(alg,1,board,bsol))
    puzzle2_button = Button(300, 300, 200, 50, "Heuristic 2", black, white, lambda: choose_func(alg,2,board,bsol))
    back_button = Button(300, 500, 200, 50, "Back", black, white, main_menu)
    buttons = [puzzle1_button, puzzle2_button, back_button]
    
    # wait for the user to close the window
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            for button in buttons:
                button.handle_event(event)
        # draw background
        screen.fill(white)
        # draw buttons
        for button in buttons:
            button.draw(screen)
        pygame.display.flip()


def alg_menu(board,bsol):
    # define buttons
    puzzle1_button = Button(300, 20, 200, 50, "BFS", black, white, lambda: draw_boards(alg.bfs(gs.CohesionState(board,[]))[1]))
    puzzle2_button = Button(300, 120, 200, 50, "IDDFS (50)", black, white, lambda: draw_boards(alg.ids(gs.CohesionState(board,[]),50)[1]))
    puzzle3_button = Button(300, 220, 200, 50, "Greedy", black, white, lambda: heuristic_menu(1,board,bsol))
    puzzle4_button = Button(300, 320, 200, 50, "A*", black, white, lambda: heuristic_menu(2,board,bsol))
    puzzle5_button = Button(300, 420, 200, 50, "Weighted A*", black, white, lambda: heuristic_menu(3,board,bsol))
    back_button = Button(300, 520, 200, 50, "Back", black, white, puzzle_menu_ai)
    buttons = [puzzle1_button, puzzle2_button, puzzle3_button,puzzle4_button,puzzle5_button, back_button]
    
    # wait for the user to close the window
    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            for button in buttons:
                button.handle_event(event)
        # draw background
        screen.fill(white)
        # draw buttons
        for button in buttons:
            button.draw(screen)
       
        pygame.display.flip()

def playable_game(board):
    # Create the game state
    state = gs.CohesionState(board, [])

    draw_board(state.board)

    # Initialize the selected piece and movement direction
    selected_piece = None
    direction = None

    # Main loop
    while True:

        if state.isComplete():
            # set up the screen
            screen_width = 800
            screen_height = 600
            screen = pygame.display.set_mode((screen_width, screen_height))
            pygame.display.set_caption("Cohesion")

            # set up font
            font = pygame.font.SysFont(None, 48)

            # define colors
            black = (0, 0, 0)
            white = (255, 255, 255)
            main_menu()
            return
        # Handle events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return

            # Handle mouse events
            elif event.type == pygame.MOUSEBUTTONDOWN:
                # Get the position of the mouse click
                mouse_pos = pygame.mouse.get_pos()
                print(mouse_pos)

                # Check if a piece was clicked
                for color, pieces in state.board.items():
                    if color == "blank" or color == "size":
                        continue
                    for piece_id, positions in pieces.items():
                        for pos_id, pos in enumerate(positions):
                            rect = pygame.Rect(pos[0]*50, pos[1]*50, 50, 50)
                            if rect.collidepoint(*mouse_pos):
                                selected_piece = (color, piece_id, pos_id)
                                print(selected_piece)

            # Handle key events
            elif event.type == pygame.KEYDOWN and selected_piece:
                if event.key == pygame.K_UP:
                    direction = "up"
                elif event.key == pygame.K_DOWN:
                    direction = "down"
                elif event.key == pygame.K_LEFT:
                    direction = "left"
                elif event.key == pygame.K_RIGHT:
                    direction = "right"
        
        # Move the selected piece if a direction is selected
        if selected_piece and direction:
            if direction == "up":
                color, piece_id, pos_id = selected_piece
                if state.up(color,piece_id):
                    print(color,piece_id,"up")
                    state = state.up(color,piece_id)
                    draw_board(state.board)
                    selected_piece = None
                    direction = None
                else: continue
            
            elif direction == "down":
                color, piece_id, pos_id = selected_piece
                if state.down(color,piece_id):
                    print(color,piece_id,"down")
                    state = state.down(color,piece_id)
                    draw_board(state.board)
                    selected_piece = None
                    direction = None
                else: continue

            elif direction == "left":
                color, piece_id, pos_id = selected_piece
                if state.left(color,piece_id):
                    print(color,piece_id,"left")
                    state = state.left(color,piece_id)
                    draw_board(state.board)
                    selected_piece = None
                    direction = None
                else: continue

            elif direction == "right":
                color, piece_id, pos_id = selected_piece
                if state.right(color,piece_id):
                    print(color,piece_id,"right")
                    state = state.right(color,piece_id)
                    draw_board(state.board)
                    selected_piece = None
                    direction = None
                else: continue



# start main menu
main_menu()
