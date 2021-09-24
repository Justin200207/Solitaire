import pygame
import card
import random
import copy
import game
import constants as c
import unittest


class TestGame(unittest.TestCase):
    def test_move_cards_one_card(self):
        """ Tests moving one card """
        g = game.Game()
        g.held_card = "HEARTSA"
        g.move_cards(100, 200)
        self.assertEqual(
            (g.cards["HEARTSA"].get_x(), g.cards["HEARTSA"].get_y()),
            (100, 200))

    def test_move_cards_stack(self):
        """ Tests moving a stack of cards """
        g = game.Game()
        g.held_card = "HEARTS3"
        g.held_stack = ["CLUBS2", "DIAMONDSA"]
        g.move_cards(100, 200)
        self.assertEqual(
            (g.cards["HEARTS3"].get_x(), g.cards["HEARTS3"].get_y()),
            (100, 200))
        self.assertEqual(
            (g.cards["CLUBS2"].get_x(), g.cards["CLUBS2"].get_y()),
            (100, 215))
        self.assertEqual(
            (g.cards["DIAMONDSA"].get_x(), g.cards["DIAMONDSA"].get_y()),
            (100, 230))

    def test_reset_deck_empty(self):
        """ Tests trying to reset a deck with no cards to cycle """
        g = game.Game()
        g.valid_pos["DECK"][2].clear()
        g.reset_deck()
        self.assertEqual(g.valid_pos["DECK"][2], [])

    def test_reset_deck_one(self):
        """ Tests reseting the deck with one card being cycled """
        g = game.Game()
        g.valid_pos["HAND0"][2].append(g.valid_pos["DECK"][2].pop())
        g.valid_pos["DECK"][2].clear()
        test_card = g.valid_pos["HAND0"][2][0] + ""
        g.cards[test_card].set_x(g.valid_pos["HAND0"][0])
        g.cards[test_card].set_y(g.valid_pos["HAND0"][1])
        g.reset_deck()
        self.assertEqual(
            (g.cards[test_card].get_x(), g.cards[test_card].get_y()),
            (g.valid_pos["DECK"][0], g.valid_pos["DECK"][1])
        )
        self.assertEqual(g.valid_pos["DECK"][2], [test_card])
        self.assertEqual(g.valid_pos["HAND0"][2], [])

    def test_reset_deck_two(self):
        """ Tests reseting the deck with two cards being cycled """
        g = game.Game()
        g.valid_pos["HAND0"][2].append(g.valid_pos["DECK"][2].pop())
        g.valid_pos["HAND1"][2].append(g.valid_pos["DECK"][2].pop())
        g.valid_pos["DECK"][2].clear()
        test_card_1 = g.valid_pos["HAND0"][2][0]
        g.cards[test_card_1].set_x(g.valid_pos["HAND0"][0])
        g.cards[test_card_1].set_y(g.valid_pos["HAND0"][1])
        test_card_2 = g.valid_pos["HAND1"][2][0]
        g.cards[test_card_2].set_x(g.valid_pos["HAND1"][0])
        g.cards[test_card_2].set_y(g.valid_pos["HAND1"][1])
        g.reset_deck()
        self.assertEqual(
            (g.cards[test_card_1].get_x(), g.cards[test_card_1].get_y()),
            (g.valid_pos["DECK"][0], g.valid_pos["DECK"][1])
        )
        self.assertEqual(
            (g.cards[test_card_2].get_x(), g.cards[test_card_2].get_y()),
            (g.valid_pos["DECK"][0], g.valid_pos["DECK"][1])
        )
        self.assertEqual(g.valid_pos["DECK"][2], [test_card_2, test_card_1])
        self.assertEqual(g.valid_pos["HAND0"][2], [])
        self.assertEqual(g.valid_pos["HAND1"][2], [])

    def test_reset_deck_three(self):
        """ Tests reseting the deck with three cards being cycled """
        g = game.Game()
        g.valid_pos["HAND0"][2].append(g.valid_pos["DECK"][2].pop())
        g.valid_pos["HAND1"][2].append(g.valid_pos["DECK"][2].pop())
        g.valid_pos["HAND2"][2].append(g.valid_pos["DECK"][2].pop())
        g.valid_pos["DECK"][2].clear()
        test_card_1 = g.valid_pos["HAND0"][2][0]
        g.cards[test_card_1].set_x(g.valid_pos["HAND0"][0])
        g.cards[test_card_1].set_y(g.valid_pos["HAND0"][1])
        test_card_2 = g.valid_pos["HAND1"][2][0]
        g.cards[test_card_2].set_x(g.valid_pos["HAND1"][0])
        g.cards[test_card_2].set_y(g.valid_pos["HAND1"][1])
        test_card_3 = g.valid_pos["HAND2"][2][0]
        g.cards[test_card_3].set_x(g.valid_pos["HAND2"][0])
        g.cards[test_card_3].set_y(g.valid_pos["HAND2"][1])
        g.reset_deck()
        self.assertEqual(
            (g.cards[test_card_1].get_x(), g.cards[test_card_1].get_y()),
            (g.valid_pos["DECK"][0], g.valid_pos["DECK"][1])
        )
        self.assertEqual(
            (g.cards[test_card_2].get_x(), g.cards[test_card_2].get_y()),
            (g.valid_pos["DECK"][0], g.valid_pos["DECK"][1])
        )
        self.assertEqual(
            (g.cards[test_card_3].get_x(), g.cards[test_card_3].get_y()),
            (g.valid_pos["DECK"][0], g.valid_pos["DECK"][1])
        )
        self.assertEqual(g.valid_pos["DECK"][2],
                         [test_card_3, test_card_2, test_card_1])
        self.assertEqual(g.valid_pos["HAND0"][2], [])
        self.assertEqual(g.valid_pos["HAND1"][2], [])
        self.assertEqual(g.valid_pos["HAND2"][2], [])

    def test_reset_deck_ten(self):
        """ Tests reseting the deck with ten cards being cycled """
        g = game.Game()
        for a in range(8):
            g.valid_pos["HAND0"][2].append(g.valid_pos["DECK"][2].pop())
        g.valid_pos["HAND1"][2].append(g.valid_pos["DECK"][2].pop())
        g.valid_pos["HAND2"][2].append(g.valid_pos["DECK"][2].pop())
        g.valid_pos["DECK"][2].clear()
        test_cards = []
        test_cards.extend(g.valid_pos["HAND0"][2])
        for a in range(8):
            g.cards[test_cards[0]].set_x(g.valid_pos["HAND0"][0])
            g.cards[test_cards[0]].set_y(g.valid_pos["HAND0"][1])
        test_cards.append(g.valid_pos["HAND1"][2][0])
        g.cards[test_cards[8]].set_x(g.valid_pos["HAND1"][0])
        g.cards[test_cards[8]].set_y(g.valid_pos["HAND1"][1])
        test_cards.append(g.valid_pos["HAND2"][2][0])
        g.cards[test_cards[9]].set_x(g.valid_pos["HAND2"][0])
        g.cards[test_cards[9]].set_y(g.valid_pos["HAND2"][1])
        test_cards.reverse()
        g.reset_deck()
        for a in range(10):
            self.assertEqual(
                (g.cards[test_cards[a]].get_x(),
                 g.cards[test_cards[a]].get_y()),
                (g.valid_pos["DECK"][0], g.valid_pos["DECK"][1])
            )
        self.assertEqual(g.valid_pos["DECK"][2],
                         test_cards)
        self.assertEqual(g.valid_pos["HAND0"][2], [])
        self.assertEqual(g.valid_pos["HAND1"][2], [])
        self.assertEqual(g.valid_pos["HAND2"][2], [])

    def test_will_table_take_existing_true(self):
        """ Tests to will_table_take with a good card """
        g = game.Game()
        g.valid_pos["TABLE0"][2].extend(["HEARTSK", "SPADESQ"])
        g.held_card = "DIAMONDSJ"
        result = g.will_table_take("TABLE0")
        self.assertTrue(result)

    def test_will_table_take_existing_false_suit(self):
        """ Tests to will_table_take with a card with a bad suit """
        g = game.Game()
        g.valid_pos["TABLE0"][2].extend(["HEARTSK", "SPADESQ"])
        g.held_card = "SPADESJ"
        result = g.will_table_take("TABLE0")
        self.assertFalse(result)

    def test_will_table_take_existing_false_rank(self):
        """ Tests to will_table_take with a card with a bad rank """
        g = game.Game()
        g.valid_pos["TABLE0"][2].extend(["HEARTSK", "SPADESQ"])
        g.held_card = "HEARTS10"
        result = g.will_table_take("TABLE0")
        self.assertFalse(result)

    def test_will_table_take_empty_true(self):
        """ Tests to will_table_take putting a king on an empty slot"""
        g = game.Game()
        g.held_card = "HEARTSK"
        g.valid_pos["TABLE0"][2].clear()
        result = g.will_table_take("TABLE0")
        self.assertTrue(result)

    def test_will_table_take_empty_false(self):
        """ Tests to will_table_take putting a non-king on an empty slot"""
        g = game.Game()
        g.held_card = "HEARTSQ"
        g.valid_pos["TABLE0"][2].clear()
        result = g.will_table_take("TABLE0")
        self.assertFalse(result)

    def test_will_ace_take_empty_true(self):
        """ Tests to will_ace_take putting an ace on an empty slot"""
        g = game.Game()
        g.held_card = "HEARTSA"
        result = g.will_ace_take("ACE0")
        self.assertTrue(result)

    def test_will_ace_take_empty_false(self):
        """ Tests to will_ace_take putting a non-ace on an empty slot"""
        g = game.Game()
        g.held_card = "SPADESK"
        result = g.will_ace_take("ACE0")
        self.assertFalse(result)

    def test_move_to_hand_empty(self):
        """ Tests move_to_hand with no cards in hand"""
        g = game.Game()
        old_deck = g.valid_pos["DECK"][2] + []
        test_card = old_deck.pop()
        g.move_to_hand(test_card)
        self.assertEqual(g.valid_pos["DECK"][2], old_deck)
        self.assertEqual(g.valid_pos["HAND0"][2], [test_card])
        self.assertEqual(
            (g.cards[test_card].get_x(), g.cards[test_card].get_y()),
            (g.valid_pos["HAND0"][0], g.valid_pos["HAND0"][1])
        )

    def test_move_to_hand_far_full(self):
        """ Tests move_to_hand with a card in the far hand"""
        g = game.Game()
        old_deck = g.valid_pos["DECK"][2] + []
        test_card_1 = old_deck.pop()
        g.move_to_hand(test_card_1)
        test_card_2 = old_deck.pop()
        g.move_to_hand(test_card_2)
        self.assertEqual(g.valid_pos["DECK"][2], old_deck)
        self.assertEqual(g.valid_pos["HAND0"][2], [test_card_1])
        self.assertEqual(
            (g.cards[test_card_1].get_x(), g.cards[test_card_1].get_y()),
            (g.valid_pos["HAND0"][0], g.valid_pos["HAND0"][1])
        )
        self.assertEqual(g.valid_pos["HAND1"][2], [test_card_2])
        self.assertEqual(
            (g.cards[test_card_2].get_x(), g.cards[test_card_2].get_y()),
            (g.valid_pos["HAND1"][0], g.valid_pos["HAND1"][1])
        )

    def test_move_to_hand_mid_full(self):
        """ Tests move_to_hand with a card in the mid hand"""
        g = game.Game()
        old_deck = g.valid_pos["DECK"][2] + []
        test_card_1 = old_deck.pop()
        g.move_to_hand(test_card_1)
        test_card_2 = old_deck.pop()
        g.move_to_hand(test_card_2)
        test_card_3 = old_deck.pop()
        g.move_to_hand(test_card_3)
        self.assertEqual(g.valid_pos["DECK"][2], old_deck)
        self.assertEqual(g.valid_pos["HAND0"][2], [test_card_1])
        self.assertEqual(
            (g.cards[test_card_1].get_x(), g.cards[test_card_1].get_y()),
            (g.valid_pos["HAND0"][0], g.valid_pos["HAND0"][1])
        )
        self.assertEqual(g.valid_pos["HAND1"][2], [test_card_2])
        self.assertEqual(
            (g.cards[test_card_2].get_x(), g.cards[test_card_2].get_y()),
            (g.valid_pos["HAND1"][0], g.valid_pos["HAND1"][1])
        )
        self.assertEqual(g.valid_pos["HAND2"][2], [test_card_3])
        self.assertEqual(
            (g.cards[test_card_3].get_x(), g.cards[test_card_3].get_y()),
            (g.valid_pos["HAND2"][0], g.valid_pos["HAND2"][1])
        )

    def test_move_to_hand_all_full(self):
        """ Tests move_to_hand with a card in the mid hand"""
        g = game.Game()
        old_deck = g.valid_pos["DECK"][2] + []
        test_card_1 = old_deck.pop()
        g.move_to_hand(test_card_1)
        test_card_2 = old_deck.pop()
        g.move_to_hand(test_card_2)
        test_card_3 = old_deck.pop()
        g.move_to_hand(test_card_3)
        test_card_4 = old_deck.pop()
        g.move_to_hand(test_card_4)
        self.assertEqual(g.valid_pos["DECK"][2], old_deck)
        self.assertEqual(g.valid_pos["HAND0"][2], [test_card_1, test_card_2])
        self.assertEqual(
            (g.cards[test_card_1].get_x(), g.cards[test_card_1].get_y()),
            (g.valid_pos["HAND0"][0], g.valid_pos["HAND0"][1])
        )
        self.assertEqual(
            (g.cards[test_card_2].get_x(), g.cards[test_card_2].get_y()),
            (g.valid_pos["HAND0"][0], g.valid_pos["HAND0"][1])
        )
        self.assertEqual(g.valid_pos["HAND1"][2], [test_card_3])
        self.assertEqual(
            (g.cards[test_card_3].get_x(), g.cards[test_card_3].get_y()),
            (g.valid_pos["HAND1"][0], g.valid_pos["HAND1"][1])
        )
        self.assertEqual(g.valid_pos["HAND2"][2], [test_card_4])
        self.assertEqual(
            (g.cards[test_card_4].get_x(), g.cards[test_card_4].get_y()),
            (g.valid_pos["HAND2"][0], g.valid_pos["HAND2"][1])
        )

    def test_undo_move_to_hand(self):
        """ Test moving a card from the deck to the hand and undoing"""
        g = game.Game()
        save = g.save_state()
        g.last.append(save)
        test_deck = g.valid_pos["DECK"][2] + []
        test_card = g.valid_pos["DECK"][2][-1]
        g.move_to_hand(test_card)
        g.undo()
        self.assertEqual(
            (g.cards[test_card].get_x(), g.cards[test_card].get_y()),
            (g.valid_pos["DECK"][0], g.valid_pos["DECK"][1])
        )
        self.assertEqual(g.valid_pos["HAND0"][2], [])
        self.assertEqual(g.valid_pos["DECK"][2], test_deck)

    def test_undo_move_multiple_cards(self):
        """ Test moving a stack of cards from on spot to another on the table"""
        g = game.Game()
        g.held_card = "HEARTS3"
        g.held_stack = ["CLUBS2", "DIAMONDSA"]
        g.valid_pos["TABLE1"][2].extend(["HEARTS3", "CLUBS2", "DIAMONDSA"])
        old_table_0 = g.valid_pos["TABLE0"][2] + []
        old_table_1 = g.valid_pos["TABLE1"][2] + []
        g.last = [g.save_state()]
        g.move_cards(g.valid_pos["TABLE0"][0], g.valid_pos["TABLE0"][1])
        g.valid_pos["TABLE0"][2].append(g.held_card)
        g.valid_pos["TABLE0"][2].extend(g.held_stack)
        g.undo()
        self.assertEqual(g.valid_pos["TABLE0"][2], old_table_0)
        self.assertEqual(g.valid_pos["TABLE1"][2], old_table_1)


if __name__ == '__main__':
    unittest.main()
