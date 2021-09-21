import pygame
import card
import random
import constants as c
from typing import Tuple, List, Optional, Dict


class Game:
    """
    Main class for the game

    ===Attributes===
    clock:
        pygame.time.Clock to control the speed of the program
    screen:
        pygame.Surface to display the game to
    font:
        pygame.font.Font to use to draw text
    running:
        bool to hold the state of the game
    right_flag:
        bool of whether or not a right click action happened on the last click
    left_flag:
        bool of whether or not a left click action happened on the last click
    card_image:
        pygame.Surface containing the sprite sheet of cards
    held_card:
        str key of the card being held
    held_stack:
        List of str keys for cards below held_card to move in unison
    x_offset:
        int representing how far of the edge of the card was clicked
        on the x axis
    y_offset:
        int representing how far of the edge of the card was clicked
        on the y axis
    old_x:
        int x position of where held_card was taken from
    old_y:
        int x position of where held_card was taken from
    sprites:
        Dict of pygame.Surface containing sprites for the game
    cards:
        dict with str keys representing the suit and rank pointing
        to each card.Card object
    card_order:
        list of str holding the order to draw the cards
    valid_pos:
        dict holding the x and y coordinate of the top left corner
        of each valid box for a card to sit in, as well as a list
        of cards in that spot
    """
    clock: pygame.time.Clock
    screen: pygame.Surface
    font: pygame.font.Font
    running: bool
    right_flag: bool
    left_flag: bool
    held_card: Optional[str]
    held_stack: List[str]
    x_offset: int
    y_offset: int
    old_x: int
    old_y: int
    sprites: Dict[str, pygame.Surface]
    cards: Dict[str, card.Card]
    card_order: List[str]
    valid_pos: Dict[str, Tuple[int, int, List[str]]]

    # =====METHODS FOR STARTING A GAME===== #
    def __init__(self) -> None:
        """ Initialize the game """
        # Setup for pygame and game logic
        pygame.init()
        self.clock = pygame.time.Clock()
        self.screen = pygame.display.set_mode([c.SCREEN_WIDTH, c.SCREEN_HEIGHT])
        self.font = pygame.font.SysFont('Arial', 16)
        self.running = True
        self.right_flag = False
        self.left_flag = False
        self.held_card = None
        self.held_stack = []
        self.x_offset = 0
        self.y_offset = 0
        self.old_x = 0
        self.old_y = 0

        # Setup the cards and associated variables
        self.sprites = {
            "cards": pygame.image.load("sprites\\cards.png"),
            "logo": pygame.image.load("sprites\\logo.png")
        }
        self.cards = {}
        self.card_order = []
        self.create_cards()
        self.valid_pos = {
            # Position for cards in the deck
            "DECK": (c.SCREEN_WIDTH - c.CARD_WIDTH * 2, 30, []),
            # Position for cards in the 3 hand slots
            "HAND2": (c.SCREEN_WIDTH - c.CARD_WIDTH * 2 - 30 - c.CARD_WIDTH,
                      30, []),  # x pos for card in the hand
            "HAND1": (c.SCREEN_WIDTH - c.CARD_WIDTH * 2 - 30 -
                      c.CARD_WIDTH - c.CARD_WIDTH // 2, 30, []),
            "HAND0": (c.SCREEN_WIDTH - c.CARD_WIDTH * 2 - 30 -
                      c.CARD_WIDTH - c.CARD_WIDTH, 30, []),
            # Position for final stacks starting with ace
            "ACE0": (30, 30, []),  # x pos for where aces may start piles
            "ACE1": (60 + c.CARD_WIDTH, 30, []),
            "ACE2": (90 + 2 * c.CARD_WIDTH, 30, []),
            "ACE3": (120 + 3 * c.CARD_WIDTH, 30, []),
            # Position for cards on the table
            "TABLE0": ((c.SCREEN_WIDTH - (7 * c.CARD_WIDTH + 6 * 30)) // 2,
                       60 + c.CARD_HEIGHT, []),
            "TABLE1": ((c.SCREEN_WIDTH - (7 * c.CARD_WIDTH + 6 * 30)) // 2 +
                       30 + c.CARD_WIDTH,
                       60 + c.CARD_HEIGHT, []),
            "TABLE2": ((c.SCREEN_WIDTH - (7 * c.CARD_WIDTH + 6 * 30)) // 2 +
                       60 + 2 * c.CARD_WIDTH,
                       60 + c.CARD_HEIGHT, []),
            "TABLE3": ((c.SCREEN_WIDTH - (7 * c.CARD_WIDTH + 6 * 30)) // 2 +
                       90 + 3 * c.CARD_WIDTH,
                       60 + c.CARD_HEIGHT, []),
            "TABLE4": ((c.SCREEN_WIDTH - (7 * c.CARD_WIDTH + 6 * 30)) // 2 +
                       120 + 4 * c.CARD_WIDTH,
                       60 + c.CARD_HEIGHT, []),
            "TABLE5": ((c.SCREEN_WIDTH - (7 * c.CARD_WIDTH + 6 * 30)) // 2 +
                       150 + 5 * c.CARD_WIDTH,
                       60 + c.CARD_HEIGHT, []),
            "TABLE6": ((c.SCREEN_WIDTH - (7 * c.CARD_WIDTH + 6 * 30)) // 2 +
                       180 + 6 * c.CARD_WIDTH,
                       60 + c.CARD_HEIGHT, [])
        }
        self.place_cards()

    def create_cards(self) -> None:
        """ Method to create a dict of 52 cards """
        for i in range(4):
            for j in range(13):
                self.cards[c.SUITS[i] + c.RANKS[j]] = card.Card(i, j)
                self.card_order.append(c.SUITS[i] + c.RANKS[j])

    def place_cards(self) -> None:
        """ Shuffle and place the cards for a new game """
        # Variable to keep track of which card is being placed
        on_card = 0

        # Shuffle the cards
        random.shuffle(self.card_order)

        # Place the cards on the 7 table slots
        for a in range(7):
            for i in range(a + 1):
                self.cards[self.card_order[on_card]].set_x(
                    self.valid_pos["TABLE" + str(a)][0])
                self.cards[self.card_order[on_card]].set_y(
                    self.valid_pos["TABLE" + str(a)][1] + i * 15)
                self.valid_pos["TABLE" + str(a)][2].append(
                    self.card_order[on_card])
                if i != a:
                    # Flip all but the last card and make them immovable
                    self.cards[self.card_order[on_card]].set_visible(False)
                    self.cards[self.card_order[on_card]].set_locked(True)
                on_card += 1

        # Place the remaining cards in the deck position
        while on_card < len(self.card_order):
            self.cards[self.card_order[on_card]].set_x(
                self.valid_pos["DECK"][0])
            self.cards[self.card_order[on_card]].set_y(
                self.valid_pos["DECK"][1])
            self.valid_pos["DECK"][2].append(self.card_order[on_card])
            self.cards[self.card_order[on_card]].visible = False
            self.cards[self.card_order[on_card]].locked = True
            on_card += 1

        # Allow the top deck card to be moved
        self.cards[self.card_order[on_card - 1]].set_locked(False)

    def reset(self) -> None:
        """ Method to reset the game """
        self.right_flag = False
        self.left_flag = False
        self.held_card = None
        self.held_stack = []
        self.x_offset = 0
        self.y_offset = 0
        self.old_x = 0
        self.old_y = 0
        self.create_cards()
        self.place_cards()

    # =====GAME LOGIC METHODS===== #

    def menu(self) -> None:
        """ Method to create a menu for the game """
        # Variable to keep the loop running
        run_menu = True
        # Variable to track if the player wants to play or quit
        play = False
        while run_menu:
            for event in pygame.event.get():
                # Check quit
                if event.type == pygame.QUIT:
                    run_menu = False
                # Check for input to continue
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        run_menu = False
                        play = True

            # Draw the screen
            # Fill the background
            self.screen.fill(c.BACK_COLOUR)
            # Draw the logo
            self.screen.blit(
                self.sprites["logo"], (c.SCREEN_WIDTH // 2 - 148,
                                       c.SCREEN_HEIGHT // 2 - 79))
            # Draw the message
            text = self.font.render(
                "Press Space to Play!", True, (255, 255, 255))
            text_rect = text.get_rect(
                center=(c.SCREEN_WIDTH // 2, c.SCREEN_HEIGHT // 2 + 100))
            self.screen.blit(text, text_rect)

            # Flip the Screen
            pygame.display.flip()

        # Check to continue or quit
        if play:
            self.run()

    def run(self) -> None:
        """Method to run the game"""
        while self.running:
            # Start the clock
            self.clock.tick(60)

            # Check quit
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False

            # Get information about the mouse
            mouse_pressed = pygame.mouse.get_pressed(3)
            mouse_x = pygame.mouse.get_pos()[0]
            mouse_y = pygame.mouse.get_pos()[1]

            # Interact with the screen from the mouse
            # Left click
            if mouse_pressed[0]:
                # Left click has happened
                self.left_click(mouse_x, mouse_y)
            elif self.held_card is not None:
                # No left click, but a card was held on last iteration, meaning
                # the card is being let go of
                self.let_go(mouse_x, mouse_y)
            elif self.left_flag:
                # No left click, no card to drop, nothing happens this move
                self.left_flag = False

            # Right click
            # Unused, kept from development
            #if mouse_pressed[2]:
                # Right click has happened
                #self.right_click(mouse_x, mouse_y)
            #else:
                # Right click is over
                #self.right_flag = False

            # Draw to the screen
            self.draw()

            # Check for a win
            if self.check_win():
                self.play_again()

    def play_again(self) -> None:
        """ Method to control the end of the game """
        # Variable to keep the loop running
        run_menu = True
        # Variable to track if the player wants to play or quit
        play = False
        while run_menu:
            for event in pygame.event.get():
                # Check quit
                if event.type == pygame.QUIT:
                    run_menu = False
                # Check for input to continue
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        run_menu = False
                        play = True

            # Draw the screen
            # Fill the background
            self.screen.fill(c.BACK_COLOUR)

            # Draw border for the valid positions except the hand
            for key in self.valid_pos:
                if "HAND" not in key:
                    pygame.draw.rect(
                        self.screen, (255, 255, 255),
                        pygame.Rect(
                            self.valid_pos[key][0],
                            self.valid_pos[key][1],
                            c.CARD_WIDTH, c.CARD_HEIGHT), 1)

            # Draw the cards
            for key in self.card_order:
                self.cards[key].draw(self.sprites["cards"], self.screen)

            # Draw the message
            text = self.font.render(
                "Press Space to Play!", True, (255, 255, 255))
            text_rect = text.get_rect(
                center=(c.SCREEN_WIDTH // 2, c.SCREEN_HEIGHT // 2 + 100))
            self.screen.blit(text, text_rect)

            # Flip the Screen
            pygame.display.flip()

        # Check to continue or quit
        if play:
            self.__init__()
            self.run()

    def draw(self) -> None:
        """ Draw to the screen """
        # Fill the screen with green
        self.screen.fill(c.BACK_COLOUR)

        # Draw border for the valid positions except the hand
        for key in self.valid_pos:
            if "HAND" not in key:
                pygame.draw.rect(
                    self.screen, (255, 255, 255),
                    pygame.Rect(
                        self.valid_pos[key][0],
                        self.valid_pos[key][1], c.CARD_WIDTH, c.CARD_HEIGHT), 1)

        # Draw the cards
        for key in self.card_order:
            self.cards[key].draw(self.sprites["cards"], self.screen)

        # Flip the Screen
        pygame.display.flip()

    def right_click(self,  mouse_x: int, mouse_y: int) -> None:
        """ Control a right click """
        # Get which, if any, card was clicked
        pressed = self.get_pressed(mouse_x, mouse_y)

        # Handle when a card is pressed, nothing happened on the last move
        # and the card pressed is not locked
        if pressed is not None and not self.right_flag \
                and not self.cards[pressed[1]].get_locked():
            # Move the card to the top of the order
            self.card_order.pop(pressed[0])
            self.card_order.append(pressed[1])
            # Flip the clicked card
            self.cards[pressed[1]].flip_visible()
            # Flag that a card was flipped
            self.right_flag = True

    def left_click(self, mouse_x: int, mouse_y: int) -> None:
        """ Control a left click """
        # Get the card, if any, that was clicked
        pressed = self.get_pressed(mouse_x, mouse_y)

        # Check for a card already being held
        if self.held_card is not None:
            # Move the held card, ignore the new card
            self.move_cards(mouse_x, mouse_y)
        # Handle a click not pressing a card
        elif pressed is None:
            # Check if a move happened on this click then if the click is on the
            # deck
            if not self.left_flag and\
                    self.check_in_box(
                        mouse_x, mouse_y, self.valid_pos["DECK"][0],
                        self.valid_pos["DECK"][1], c.CARD_WIDTH, c.CARD_HEIGHT):
                # In this case, deck is empty, reset the cards in hand to deck
                self.reset_deck()
            # Flag something happened on this click
            self.left_flag = True
        # If a card is clicked,
        # the card is unlocked and nothing happened this click already
        elif pressed is not None \
                and not self.cards[pressed[1]].get_locked() \
                and not self.left_flag:
            # Grab the card
            self.grab_cards(pressed[0], pressed[1], mouse_x, mouse_y)

    def let_go(self, mouse_x: int, mouse_y: int) -> None:
        """ Handle a card being put down """
        # Get which pile it is dropping into and which pile it came from
        pile = self.check_pile(mouse_x, mouse_y)
        old_pile = self.check_pile(self.old_x, self.old_y)

        # No new pile or the same pile
        if pile is None or pile == old_pile:
            # Put the card back
            self.cards[self.held_card].set_x(self.old_x)
            self.cards[self.held_card].set_y(self.old_y)
            # Put any cards in the held_stack back
            for index, key in enumerate(self.held_stack):
                self.cards[key].set_x(self.old_x)
                self.cards[key].set_y(self.old_y + 15 * (index + 1))
            # Mark no card being held, and empty the held_stack
            self.held_card = None
            self.held_stack = []
            return

        # Taking a card from the hand
        if "HAND" in old_pile:
            # Unlock the next applicable card from the hand
            if old_pile == "HAND0":
                if len(self.valid_pos["HAND0"][2]) > 1:
                    self.cards[self.valid_pos["HAND0"][2][-1]].set_locked(False)
            elif old_pile == "HAND1":
                self.cards[self.valid_pos["HAND0"][2][-1]].set_locked(False)
            elif old_pile == "HAND2":
                self.cards[self.valid_pos["HAND1"][2][-1]].set_locked(False)

        # Put a card on the table
        if "TABLE" in pile:
            # Check if the card matches the pattern
            if self.will_table_take(pile):
                # Move the card to the pile
                self.cards[self.held_card].set_x(self.valid_pos[pile][0])
                self.cards[self.held_card].set_y(
                    self.valid_pos[pile][1] + 15 * len(self.valid_pos[pile][2]))
                self.valid_pos[old_pile][2].remove(self.held_card)
                self.valid_pos[pile][2].append(self.held_card)

                # Move the card in held_stack to the new pile on the table
                for key in self.held_stack:
                    self.cards[key].set_x(self.valid_pos[pile][0])
                    self.cards[key].set_y(
                        self.valid_pos[pile][1] + 15 * len(
                            self.valid_pos[pile][2]))
                    self.valid_pos[old_pile][2].remove(key)
                    self.valid_pos[pile][2].append(key)

                # Make the bottom card in the pile taken from in play
                if len(self.valid_pos[old_pile][2]) >= 1:
                    self.make_in_play(self.valid_pos[old_pile][2][-1])

                # No card is held, nothing in the stack to move alongside
                self.held_card = None
                self.held_stack = []

                # Card was put down, nothing else to check
                return

        # Put into a final pile
        elif "ACE" in pile:
            # Check to see if more than one card is being moved
            if len(self.held_stack) != 0:
                # Only one card can be put at a time, move the cards back
                self.cards[self.held_card].set_x(self.old_x)
                self.cards[self.held_card].set_y(self.old_y)
                for index, key in enumerate(self.held_stack):
                    self.cards[key].set_x(self.old_x)
                    self.cards[key].set_y(self.old_y + 15 * (index + 1))
            # Check if the card meets the pattern
            elif self.will_ace_take(pile):
                # Move the card to the slot
                self.cards[self.held_card].set_x(self.valid_pos[pile][0])
                self.cards[self.held_card].set_y(self.valid_pos[pile][1])
                self.valid_pos[old_pile][2].remove(self.held_card)
                self.valid_pos[pile][2].append(self.held_card)
                # Make the next card in the old pile in play
                if len(self.valid_pos[old_pile][2]) >= 1:
                    self.make_in_play(self.valid_pos[old_pile][2][-1])
                # No card held, and nothing in the stack to move
                self.held_card = None
                self.held_stack = []
                # Card was placed, nothing else to check
                return

        # Card is not being put in a proper spot, move it and the stack back
        self.cards[self.held_card].set_x(self.old_x)
        self.cards[self.held_card].set_y(self.old_y)
        for index, key in enumerate(self.held_stack):
            self.cards[key].set_x(self.old_x)
            self.cards[key].set_y(self.old_y + 15 * (index + 1))

        # No card is held and nothing in the stack
        self.held_card = None
        self.held_stack = []

    def check_win(self) -> bool:
        """ Check if the win condition is met """
        # If all 4 Ace spots are full, there is a win
        for a in range(4):
            if len(self.valid_pos["ACE" + str(a)]) != 13:
                return False
        return True

    # =====HELPER METHODS===== #

    def grab_cards(self, index: int, key: str,
                   mouse_x: int, mouse_y: int) -> None:
        """ Grab the card and cards below it if on the table"""
        # Move the new cards key to the top of the card_order
        self.card_order.pop(index)
        self.card_order.append(key)
        # Get the x and y offset for this card on this click
        self.x_offset = self.cards[key].calc_x_offset(mouse_x)
        self.y_offset = self.cards[key].calc_y_offset(mouse_y)
        # Store where the card came from
        self.old_x = self.cards[key].get_x()
        self.old_y = self.cards[key].get_y()

        # Check which pile the card came from
        pile = self.check_pile(self.cards[key].get_x(), self.cards[key].get_y())
        # Came from a table
        if "TABLE" in pile:
            # Grab the cards that were below the grabbed card
            self.held_stack = \
                self.valid_pos[pile][2][self.valid_pos[pile][2].index(key) + 1:]
        # Came from the deck
        if "DECK" in pile:
            # Check if something has already happened on this click
            if not self.left_flag:
                # Move the card to the hand and mark that a move was made
                self.move_to_hand(key)
                self.left_flag = True
            # Move happened, nothing else to check
            return

        # Move any cards taken with the grabbed card to the top of the order
        for extra in self.held_stack:
            self.card_order.pop(self.card_order.index(extra))
            self.card_order.append(extra)

        # Store which card was grabbed
        self.held_card = key
        # Move cards that need to be moved
        self.move_cards(mouse_x, mouse_y)

    def move_cards(self, x: int, y: int):
        """ Move held_card and any cards in held_stack """
        # Move held_card
        self.cards[self.held_card].set_x(x - self.x_offset)
        self.cards[self.held_card].set_y(y - self.y_offset)

        # Move the cards in held_stack
        for offset, key in enumerate(self.held_stack):
            self.cards[key].set_x(x - self.x_offset)
            self.cards[key].set_y(y - self.y_offset + 15 * (offset + 1))

    def make_in_play(self, key: str) -> None:
        """ Set necessary properties of the card to make it in play """
        self.cards[key].set_visible(True)
        self.cards[key].set_locked(False)

    def take_out_play(self, key: str) -> None:
        """ Set necessary properties of the card to make it out of play """
        self.cards[key].set_visible(False)
        self.cards[key].set_locked(True)

    def reset_deck(self) -> None:
        """ Move the cards in the hand back into the deck """
        if len(self.valid_pos["HAND2"][2]) > 0:
            # Move the card from the hand closest to the deck
            # Pop the card
            to_move = self.valid_pos["HAND2"][2].pop(-1)
            # Move it to the top of the order
            self.card_order.remove(to_move)
            self.card_order.append(to_move)
            # Add the card to the deck
            self.valid_pos["DECK"][2].append(to_move)
            # Move the card to the deck
            self.cards[to_move].set_x(self.valid_pos["DECK"][0])
            self.cards[to_move].set_y(self.valid_pos["DECK"][1])
            # Take the card of play
            self.take_out_play(to_move)

        if len(self.valid_pos["HAND1"][2]) > 0:
            # Move the card from the middle deck
            # Pop the card
            to_move = self.valid_pos["HAND1"][2].pop(-1)
            # Move the card to the top of the order
            self.card_order.remove(to_move)
            self.card_order.append(to_move)
            # Add the card to the deck
            self.valid_pos["DECK"][2].append(to_move)
            # Move the card to the deck
            self.cards[to_move].set_x(self.valid_pos["DECK"][0])
            self.cards[to_move].set_y(self.valid_pos["DECK"][1])
            # Take the card out of play
            self.take_out_play(to_move)

        # Move the cards in the hand furthest from the deck
        for key in reversed(self.valid_pos["HAND0"][2]):
            # Remove the card from the hand
            self.valid_pos["HAND0"][2].remove(key)
            # Add the card to the deck
            self.valid_pos["DECK"][2].append(key)
            # Move the card to the top of the order
            self.card_order.remove(key)
            self.card_order.append(key)
            # Move the card to the deck
            self.cards[key].set_x(self.valid_pos["DECK"][0])
            self.cards[key].set_y(self.valid_pos["DECK"][1])
            # Take the card out of play
            self.take_out_play(key)

        # Make the top card clickable
        self.cards[self.valid_pos["DECK"][2][-1]].set_locked(False)

    def check_pile(self, x: int, y: int) -> Optional[str]:
        """ Check which pile the card is in"""
        for key in self.valid_pos:
            if "TABLE" in key:
                # Get the height based on number of cards in this pile
                check_height = c.CARD_HEIGHT + 15 * len(self.valid_pos[key][2])
                if self.check_in_box(
                        x, y, self.valid_pos[key][0], self.valid_pos[key][1],
                        c.CARD_WIDTH, check_height):
                    return key
            elif "DECK" in key:
                if self.check_in_box(
                        x, y, self.valid_pos[key][0], self.valid_pos[key][1],
                        c.CARD_WIDTH, c.CARD_HEIGHT):
                    return key
            elif "HAND" in key:
                if self.check_in_box(
                        x, y, self.valid_pos[key][0], self.valid_pos[key][1],
                        c.CARD_WIDTH, c.CARD_HEIGHT):
                    return key
            elif "ACE" in key:
                if self.check_in_box(
                        x, y, self.valid_pos[key][0], self.valid_pos[key][1],
                        c.CARD_WIDTH, c.CARD_HEIGHT):
                    return key

        # No pile was placed
        return None

    def get_pressed(self, mouse_x, mouse_y) -> Optional[Tuple[int, str]]:
        """Get the pressed card"""
        for index, key in reversed(list(enumerate(self.card_order))):
            # Find and return the card clicked, closest to the top of the list
            if self.cards[key].picked(mouse_x, mouse_y):
                return index, key
        # Return None if no card was clicked
        return None

    def will_table_take(self, table: str) -> bool:
        """ Check if the card fits the pattern of the table """
        # Get the suit and rank of the held_card
        held_suit = self.cards[self.held_card].get_suit()
        held_rank = self.cards[self.held_card].get_rank()

        # Check if the card is a king
        if held_rank == c.RANKS[12]:
            # Check if there are other cards in the spot already
            if len(self.valid_pos[table][2]) == 0:
                # Only a king can be placed in an empty table spot
                return True
            return False

        # Get the key of, suit and rank of the bottom card in this table spot
        bot_key = self.valid_pos[table][2][-1]
        bot_suit = self.cards[bot_key].get_suit()
        bot_rank = self.cards[bot_key].get_rank()

        # Check if the ranks match the pattern
        if c.RANKS.index(held_rank) != c.RANKS.index(bot_rank) - 1:
            return False
        # Check if the suits match the pattern
        if held_suit == c.SUITS[0] or held_suit == c.SUITS[1]:
            if bot_suit == c.SUITS[2] or bot_suit == c.SUITS[3]:
                return True
            return False
        elif held_suit == c.SUITS[2] or held_suit == c.SUITS[3]:
            if bot_suit == c.SUITS[0] or bot_suit == c.SUITS[1]:
                return True
            return False

    def will_ace_take(self, ace: str):
        """ Check if the card fits the final piles pattern"""
        # Get the suit and rank of the held_card
        held_suit = self.cards[self.held_card].get_suit()
        held_rank = self.cards[self.held_card].get_rank()

        # Check if the card is an Ace
        if held_rank == c.RANKS[0]:
            # Check if this spot is empty
            if len(self.valid_pos[ace][2]) == 0:
                # Only an ace can be placed in an empty final pile
                return True
            return False

        # Get the key of, suit and rank of the bottom card in this table spot
        bot_key = self.valid_pos[ace][2][-1]
        bot_suit = self.cards[bot_key].get_suit()
        bot_rank = self.cards[bot_key].get_rank()

        # Check if the card matches the pattern of this spot
        if c.RANKS.index(held_rank) == \
                c.RANKS.index(bot_rank) + 1 and held_suit == bot_suit:
            return True
        return False

    def move_to_hand(self, key: str) -> None:
        """ Move the card from the deck to the hand"""
        # No card in the furthest spot
        if len(self.valid_pos["HAND0"][2]) == 0:
            # Move the card to the furthest hand
            self.valid_pos["DECK"][2].remove(key)
            self.valid_pos["HAND0"][2].append(key)
            self.cards[key].set_x(self.valid_pos["HAND0"][0])
            self.cards[key].set_y(self.valid_pos["HAND0"][1])
            # Make the card in play
            self.make_in_play(self.valid_pos["HAND0"][2][-1])
            # If there is still a card in the deck, make it clickable
            if len(self.valid_pos["DECK"][2]) > 0:
                self.cards[self.valid_pos["DECK"][2][-1]].set_locked(False)

        # No card in the middle spot
        elif len(self.valid_pos["HAND1"][2]) == 0:
            # Move the card to the middle hand
            self.valid_pos["DECK"][2].remove(key)
            self.valid_pos["HAND1"][2].append(key)
            self.cards[key].set_x(self.valid_pos["HAND1"][0])
            self.cards[key].set_y(self.valid_pos["HAND1"][1])
            # Make the card in play
            self.make_in_play(self.valid_pos["HAND1"][2][-1])
            # Make the next card in the deck clickable
            # If there is still a card in the deck, make it clickable
            if len(self.valid_pos["DECK"][2]) > 0:
                self.cards[self.valid_pos["DECK"][2][-1]].set_locked(False)
            # Lock the card in the furthest hand
            self.cards[self.valid_pos["HAND0"][2][0]].set_locked(True)

        # No card in the closest spot
        elif len(self.valid_pos["HAND2"][2]) == 0:
            # Move the card to the closest hand
            self.valid_pos["DECK"][2].remove(key)
            self.valid_pos["HAND2"][2].append(key)
            self.cards[key].set_x(self.valid_pos["HAND2"][0])
            self.cards[key].set_y(self.valid_pos["HAND2"][1])
            # Make the card in play
            self.make_in_play(self.valid_pos["HAND2"][2][-1])
            # Make the next card in the deck clickable
            # If there is still a card in the deck, make it clickable
            if len(self.valid_pos["DECK"][2]) > 0:
                self.cards[self.valid_pos["DECK"][2][-1]].set_locked(False)
            # Lock the card in the middle hand
            self.cards[self.valid_pos["HAND1"][2][0]].set_locked(True)

        # All hands have cards, move the cards away from the deck
        else:
            # Move the card from the middle to the furthest
            to_move = self.valid_pos["HAND1"][2][-1]
            self.cards[to_move].set_x(self.valid_pos["HAND0"][0])
            self.cards[to_move].set_y(self.valid_pos["HAND0"][1])
            self.valid_pos["HAND1"][2].remove(to_move)
            self.valid_pos["HAND0"][2].append(to_move)

            # Move the card from the closest to the middle and lock it
            to_move = self.valid_pos["HAND2"][2][-1]
            self.cards[to_move].set_locked(True)
            self.cards[to_move].set_x(self.valid_pos["HAND1"][0])
            self.cards[to_move].set_y(self.valid_pos["HAND1"][1])
            self.valid_pos["HAND2"][2].remove(to_move)
            self.valid_pos["HAND1"][2].append(to_move)

            # Move the top card from the deck to the closest hand
            self.valid_pos["DECK"][2].remove(key)
            self.valid_pos["HAND2"][2].append(key)
            self.cards[key].set_x(self.valid_pos["HAND2"][0])
            self.cards[key].set_y(self.valid_pos["HAND2"][1])
            # Make the card in play
            self.make_in_play(self.valid_pos["HAND2"][2][-1])
            # If there is still a card in the deck, make it clickable
            if len(self.valid_pos["DECK"][2]) > 0:
                self.cards[self.valid_pos["DECK"][2][-1]].set_locked(False)

    @staticmethod
    def check_in_box(
            px: int, py: int, bx: int, by: int, width: int, height: int)\
            -> bool:
        """
        Check if the coordinates in pos
        fall in the rectangle at position box with
        the defined width and height
        """
        # Compare x values
        if bx <= px <= bx + width:
            # Compare y values
            if by <= py <= by + height:
                return True
        return False


if __name__ == "__main__":
    game = Game()
    game.play_again()
