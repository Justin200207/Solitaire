import pygame
import constants as c


class Card:
    """
    Class representing a card

    ===Attributes===
    suit:
        str corresponding to the suit of the card
    rank:
        str corresponding to the face value of the card
    x:
        int x position
    y:
        int y position
    visible:
        bool representing whether or not the card face is visible
    locked:
        bool storing if the card can move or not
    face_x:
        int x position of face sprite on the sprite sheet
    face_y:
        int y position of face sprite on the sprite sheet
    """
    suit: str
    rank: str
    x: int
    y: int
    visible: bool
    locked: bool
    img_x: int
    img_y: int

    def __init__(self, i: int, j: int) -> None:
        """
        Initializes a new card

        Preconditions:
            back_x, back_y:
                These should correlate to the x and y
                position of the top left corner of
                the back image for cards on the sprite sheet in use
            width, height:
                This should be the width and height
                of each sprite on the sprite sheet in use
        """
        self.suit = c.SUITS[i]
        self.rank = c.RANKS[j]
        self.x = 0
        self.y = 0
        self.visible = True
        self.locked = False
        self.face_x = j * c.CARD_WIDTH
        self.face_y = i * c.CARD_HEIGHT

    def get_suit(self) -> str:
        """Returns the suit of the card"""
        return self.suit

    def get_col(self) -> int:
        """Returns 1 or -1 depending on suit of the card"""
        if self.suit == c.SUITS[0] or self.suit == c.SUITS[1]:
            return 1
        return -1

    def get_rank(self) -> str:
        """Returns the rank of the card"""
        return self.rank

    def get_x(self) -> int:
        """Get the x pos of the card"""
        return self.x

    def set_x(self, x: int) -> None:
        """
        Change the x position of the card to x
        Will not allow the card go off screen
        """
        if 0 <= x <= c.SCREEN_WIDTH - c.CARD_WIDTH:
            self.x = x
        else:
            # Put the card at the edge it would have crossed over
            if x <= 0:
                self.x = 0
            else:
                self.x = c.SCREEN_WIDTH - c.CARD_WIDTH

    def get_y(self) -> int:
        """Get the x pos of the card"""
        return self.y

    def set_y(self, y: int) -> None:
        """
        Change the y position of the card to y
        Will not allow the card go off screen
        """
        if 0 <= y <= c.SCREEN_HEIGHT - c.CARD_HEIGHT:
            self.y = y
        else:
            # Put the card at the edge it would have crossed over
            if y <= 0:
                self.y = 0
            else:
                self.y = c.SCREEN_HEIGHT - c.CARD_HEIGHT

    def flip_visible(self) -> None:
        """Flips the state of self.visible"""
        if self.visible:
            self.visible = False
            return
        self.visible = True

    def get_visible(self) -> bool:
        """get self.visible"""
        return self.visible

    def set_visible(self, state: bool) -> None:
        """Changes the visibility of the card to state"""
        self.visible = state

    def get_locked(self) -> bool:
        """"Gets self.locked"""
        return self.locked

    def set_locked(self, state: bool) -> None:
        """Sets self.lock to state"""
        self.locked = state

    def draw(self, img: pygame.Surface, screen: pygame.Surface) -> None:
        """Draws this cards sprite from img to screen"""
        if self.visible:
            screen.blit(img, (self.x, self.y),
                        pygame.Rect(self.face_x, self.face_y,
                        c.CARD_WIDTH, c.CARD_HEIGHT))
        else:
            screen.blit(img, (self.x, self.y),
                        pygame.Rect(c.CARD_BACK_X, c.CARD_BACK_Y,
                        c.CARD_WIDTH, c.CARD_HEIGHT))

    def picked(self, mouse_x: int, mouse_y: int) -> bool:
        """Checks if this card is being clicked"""
        # Check if x is in range
        if self.x <= mouse_x < self.x + c.CARD_WIDTH:
            # Check if y is in range
            if self.y <= mouse_y < self.y + c.CARD_HEIGHT:
                return True
        return False

    def calc_x_offset(self, mouse_x: int) -> int:
        """
        Returns how far from the vertical edge
        of the card the mouse clicked
        """
        return mouse_x - self.x

    def calc_y_offset(self, mouse_y: int) -> int:
        """
        Returns how far from the horizontal edge
        of the card the mouse clicked
        """
        return mouse_y - self.y
