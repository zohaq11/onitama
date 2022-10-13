# Import the pygame module
import pygame
# Import pygame.locals for easier access to key coordinates
# Updated to conform to flake8 and black standards
from pygame.locals import (
    MOUSEBUTTONUP,
    K_ESCAPE,
    KEYDOWN,
    QUIT,
)
from Player import Player, PlayerRandom
from OnitamaGame import OnitamaGame
from Pieces import Pieces
from Button import Button
from StyleImages import StyleImages
from Tile import Tile
from StyleCard import StyleCard
from typing import List, Tuple


class Screen:
    """
    The main Screen for this pygame GUI.
    """
    # Define constants for the screen width and height
    SCREEN_WIDTH: int = 1000
    SCREEN_HEIGHT: int = 800
    BG: Tuple[int, int, int] = (0, 255, 0)
    BG_IMG: str = './assets/img/space.png'
    # BG_IMG: str = './assets/img/sayu_cry.gif'
    tiles: List[Tile]
    dest_tiles: List[Tile]
    player_styles: List[StyleCard]
    buttons: List[Button]
    pieces: Pieces
    style_images: StyleImages
    mouse_pos: Tuple[int, int]
    tile_origin: Tile
    tile_dest: Tile
    chosen_style: StyleCard
    # 0: HvH, 1: HvR 2: RvR
    game_mode: int = 0
    # Variable to keep the main loop running
    running: bool = True
    game_running: bool = True

    def __init__(self):
        """
        Initialize the Screen of the GUI
        """
        self.mouse_pos = (-1, -1)
        # Initialize pygame
        pygame.init()

        # Create the screen object
        # The size is determined by the constant SCREEN_WIDTH and SCREEN_HEIGHT
        self.screen = pygame.display.set_mode(
            (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))

        self.pieces = Pieces(pygame, Tile.width, Tile.height)
        self.style_images = StyleImages(pygame, 200, 125)
        # Load the background
        img = pygame.image.load(self.BG_IMG).convert()
        img = pygame.transform.smoothscale(
            img, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        self.screen.blit(img, (0, 0))
        self.reset()  # Initialize the game, tiles and style cards.
        # Create buttons that will be needed for the game.
        # Different Game Modes
        hvh = Button(self.screen, self.onitama, 775, 175, 'HvH')
        hvr = Button(self.screen, self.onitama, 775, 275, 'HvR')
        rvr = Button(self.screen, self.onitama, 775, 375, 'RvR')
        # Utility buttons to Undo a move and Reset the game.
        undo = Button(self.screen, self.onitama, 775, 475, 'Undo')
        reset = Button(self.screen, self.onitama, 775, 575, 'Reset')
        self.buttons = [hvh, hvr, rvr, undo, reset]
        # Update the display
        self.draw()
        pygame.display.flip()

    def init_tiles(self, offset_x, offset_y) -> None:
        """
        Initialize the tiles of the OnitamaBoard.
        """
        board = self.onitama.get_board()
        for i, row in enumerate(board):
            for j, _ in enumerate(row):
                self.tiles.append(
                    Tile(screen=self.screen,
                         onitama=self.onitama,
                         pieces=self.pieces,
                         row=i,
                         col=j,
                         offset_x=offset_x,
                         offset_y=offset_y
                         ))

    def init_player_styles(self, offset_x=0, offset_y=12) -> None:
        """
        Initialize all of the player styles of Onitama.
        """
        # Initialize the style images
        # p1 styles
        second_style_offset = (self.onitama.size // 2 + 1) * Tile.width
        p1_left = StyleCard(screen=self.screen,
                            onitama=self.onitama,
                            player_id=Pieces.G1,
                            style_name='',
                            style_images=self.style_images,
                            offset_x=offset_x, offset_y=offset_y)
        p1_right = StyleCard(screen=self.screen,
                             onitama=self.onitama,
                             player_id=Pieces.G1,
                             style_name='',
                             style_images=self.style_images,
                             offset_x=offset_x + second_style_offset,
                             offset_y=offset_y)
        # p2 styles
        p2_y_offset = ((self.SCREEN_HEIGHT - self.onitama.size *
                        Tile.height) // 2 + self.onitama.size * Tile.height)

        p2_left = StyleCard(screen=self.screen,
                            onitama=self.onitama,
                            player_id=Pieces.G2,
                            style_name='',
                            style_images=self.style_images,
                            offset_x=offset_x, offset_y=offset_y + p2_y_offset)

        p2_right = StyleCard(screen=self.screen,
                             onitama=self.onitama,
                             player_id=Pieces.G2,
                             style_name='',
                             style_images=self.style_images,
                             offset_x=offset_x + second_style_offset,
                             offset_y=offset_y + p2_y_offset)
        # fifth/extra style
        fifth_style = StyleCard(screen=self.screen,
                                onitama=self.onitama,
                                player_id=Pieces.EMPTY,
                                style_name='',
                                style_images=self.style_images,
                                offset_x=25, offset_y=350)
        # Assign them to a list
        self.player_styles = [p1_left, p1_right,
                              p2_left, p2_right, fifth_style]

    def update_styles(self):
        """
        Draw the style images on the surface.
        """
        self.chosen_style = None
        styles = self.onitama.get_styles()
        p1_styles = []
        p2_styles = []
        fifth_style = ''
        # Get an ordered version of the styles so that we can easily update our player_styles.
        for sty in styles:
            if sty.owner == Pieces.G1:
                p1_styles.append(sty.name)
            elif sty.owner == Pieces.G2:
                p2_styles.append(sty.name)
            else:
                fifth_style = sty.name

        ordered = []
        ordered.extend(p1_styles)
        ordered.extend(p2_styles)
        ordered.append(fifth_style)
        for i, sty_name in enumerate(ordered):
            self.player_styles[i].style_name = sty_name

    def reset_clicks(self) -> None:
        """
        Reset all clicked status on the tiles and style cards.
        """
        for tile in self.tiles:
            tile.clicked = False

        for sty in self.player_styles:
            sty.clicked = False

        self.tile_origin = None
        self.tile_dest = None
        self.dest_tiles = []
        self.chosen_style = None

    def reset(self) -> None:
        """
        Reset this game of Onitama to a new game and reset all relevant variables to their initial state.
        """
        self.onitama = OnitamaGame()
        self.tiles = []
        self.dest_tiles = []
        self.tile_origin = None
        self.tile_dest = None
        offset_x = (self.SCREEN_WIDTH -
                    self.onitama.size * Tile.width) // 2
        offset_y = (self.SCREEN_HEIGHT -
                    self.onitama.size * Tile.height) // 2

        self.init_tiles(offset_x, offset_y)
        self.init_player_styles(offset_x=offset_x)
        self.update_styles()
        self.set_op(0)

    def check_winner(self) -> None:
        """
        Check's the Onitama game's status on a winner and updates game_running accordingly.
        """
        if self.onitama.get_winner() is not None:
            # TODO: Add who won somewhere on the screen.
            self.game_running = False

    def move_ai(self) -> None:
        """
        Make an AI player's move on onitama if needed.
        """
        if isinstance(self.onitama.whose_turn, PlayerRandom):
            # time delay in milliseconds for the AI when watching RvR simulation is 500, 250 for HvR
            time_delay = 500 if self.game_mode == 2 else 250
            pygame.time.delay(time_delay)
            turn = self.onitama.whose_turn.get_turn()
            if turn is not None:
                self.onitama.move(turn.row_o, turn.col_o,
                                  turn.row_d, turn.col_d, turn.style_name)
                self.update_styles()
                self.reset_clicks()
            self.check_winner()

    def move(self) -> None:
        """
        Make a human player's move on onitama.
        """
        row_o = self.tile_origin.row
        col_o = self.tile_origin.col
        row_d = self.tile_dest.row
        col_d = self.tile_dest.col
        style_name = self.chosen_style.style_name
        if self.onitama.move(row_o, col_o, row_d, col_d, style_name):
            self.update_styles()
            self.reset_clicks()

        self.check_winner()

    def undo(self) -> None:
        """
        Undo's a move in Onitama and update's the styles as well as resets clicks on the tiles and style cards.
        """
        if not self.game_running:
            self.game_running = True
            self.set_op(0)
        self.onitama.undo()
        if self.game_mode == 1:
            self.onitama.undo()
        self.update_styles()
        self.reset_clicks()

    def set_op(self, game_mode: int) -> None:
        """
        Set's the other player's Player Type depending on the game mode.
        """
        self.game_mode = game_mode
        curr_turn = self.onitama.whose_turn.player_id
        if game_mode == 0 or game_mode == 2:
            # Set both players to PlayerRandom or a regular Player depending on the game mode.
            self.onitama.player1 = Player(self.onitama.player1.player_id) if game_mode == 0 else PlayerRandom(
                self.onitama.player1.player_id)
            self.onitama.player2 = Player(self.onitama.player2.player_id) if game_mode == 0 else PlayerRandom(
                self.onitama.player2.player_id)
            self.onitama.player1.set_onitama(self.onitama)
            self.onitama.player2.set_onitama(self.onitama)
            if curr_turn == self.onitama.player1.player_id:
                self.onitama.whose_turn = self.onitama.player1
            else:
                self.onitama.whose_turn = self.onitama.player2
            return

        # Set the other player to PlayerRandom
        op = self.onitama.other_player(self.onitama.whose_turn)
        if not op:
            return
        player = PlayerRandom(op.player_id)
        player.set_onitama(self.onitama)
        if self.onitama.whose_turn == self.onitama.player1:
            self.onitama.player2 = player
        else:
            self.onitama.player1 = player

    def btn_click(self, btn: Button) -> None:
        """
        Check which button was clicked and perform the respective actions.
        """
        if btn.text == 'Undo':
            self.undo()
            btn.clicked = False
        elif btn.text == 'Reset':
            self.reset()
            btn.clicked = False
            self.game_running = True
        elif btn.text == 'HvH':
            self.set_op(0)
        elif btn.text == 'HvR':
            self.set_op(1)
        elif btn.text == 'RvR':
            self.set_op(2)

    def update_dest_tiles(self) -> None:
        """
        Highlights the tiles which are valid destination spots for the currently selectiled piece if possible.
        """
        if not self.tile_origin:
            return
        # Highlight the pieces which are valid destinations
        valid_turns = self.onitama.whose_turn.get_valid_turns()
        turns = []

        # Check if a style has been chosen and only display those turns.
        if self.chosen_style and self.chosen_style.style_name in valid_turns:
            turns = valid_turns[self.chosen_style.style_name]
        else:
            for style_name in valid_turns:
                turns.extend(valid_turns[style_name])
        # Get all indices of tiles which are valid destinations for the chosen piece.
        highlighted = set()
        for turn in turns:
            if (turn.row_o, turn.col_o) == (self.tile_origin.row, self.tile_origin.col):
                highlighted.add(self.onitama.size *
                                turn.row_d + turn.col_d)
        # For each index, add the tile itself to the destination tiles.
        self.dest_tiles = []
        for i in highlighted:
            self.tiles[i].set_highlight(True)
            self.dest_tiles.append(self.tiles[i])

    def draw(self):
        """
        Draw all of the entities onto the screen.
        """
        # Draw tiles
        for tile in self.tiles:
            tile.draw()
        # Draw the style images.
        for sty_img in self.player_styles:
            sty_img.draw()

        # Draw all buttons
        for btn in self.buttons:
            btn.draw()

        # Update the current game_mode button to highlight it.
        self.buttons[self.game_mode].set_highlight(True)

    def hover(self):
        """
        Check if any of the entities are being hovered.
        """
        mouse_pos = pygame.mouse.get_pos()

        for tile in self.tiles:
            # Check if hovered
            if tile.hover(mouse_pos):
                return
        for sty_img in self.player_styles:
            if sty_img.hover(mouse_pos):
                return
        for btn in self.buttons:
            if btn.hover(mouse_pos):
                break

    def click(self):
        """
        Check if any of the entities have been clicked.
        """
        mouse_pos = pygame.mouse.get_pos()
        clicked = None

        # Check if any of the buttons have been clicked and handle them appropriately.
        for btn in self.buttons:
            # Reset all button highlights statuses
            btn.set_highlight(False)
            if btn.click(mouse_pos):
                clicked = btn

        if clicked:
            self.btn_click(clicked)
            return
        # If the game is not running, we do not want any clicks on the game.
        if not self.game_running:
            return

        # Check if any of the tiles have been clicked
        for tile in self.tiles:
            # Reset highlight
            tile.set_highlight(False)
            # Check if clicked
            if tile.click(mouse_pos):
                clicked = tile

        # If a tile has been clicked, update the origin tile and destination tiles.
        if clicked:
            # Check if this tile is in the highlighted tiles
            if self.tile_origin and self.chosen_style and self.dest_tiles and clicked in self.dest_tiles:
                self.tile_dest = clicked
                self.move()
            else:
                self.tile_origin = clicked
        else:
            for sty_img in self.player_styles:
                if sty_img.click(mouse_pos) and sty_img.player_id == self.onitama.whose_turn.player_id:
                    clicked = sty_img
            if clicked:
                self.chosen_style = clicked if self.chosen_style != clicked else None

        # Set the clicked attribute to true for the origin tile for green highlighting.
        if self.tile_origin:
            self.tile_origin.clicked = True
        # If nothing has been clicked, reset all click events.
        if not clicked:
            self.reset_clicks()
        # Update the highlight for the destination tiles.
        self.update_dest_tiles()

    def render(self):
        """
        Renders the screen for the pygame GUI.
        This is the main loop of the code.
        """
        # Main loop

        while self.running:
            # for loop through the event queue
            for event in pygame.event.get():
                # Check for KEYDOWN event
                if event.type == KEYDOWN:
                    # If the Esc key is pressed, then exit the main loop
                    if event.key == K_ESCAPE:
                        self.running = False
                # Check for QUIT event. If QUIT, then set running to false.
                elif event.type == QUIT:
                    self.running = False

                if event.type == MOUSEBUTTONUP:
                    # Check for click event
                    self.click()
            # If the game is moving, check if we need to move the AI.
            if self.game_running:
                self.move_ai()
            # Update the display
            self.draw()
            self.hover()

            # Update the display
            pygame.display.flip()


if __name__ == '__main__':
    screen = Screen()
    screen.render()
