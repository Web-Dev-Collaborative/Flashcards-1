from random import randint, choice

import pytest
from django.test import TestCase

from flashcards.leitner.models import Card, Box, Session
from flashcards.users.models import User

pytestmark = pytest.mark.django_db


class TestModelsWithOneUserAndSession(TestCase):
    def setUp(self) -> None:
        self.user = User.objects.create_user('test_username', 'testmail@example.com', 'testing321')
        self.session = Session.objects.create(
            description='Irrelevant description',
            created_by=self.user,
        )
        self.card_list = []
        for i in range(10):  # Don't change this number!
            card = Card.objects.create(
                front_text=f'Front text {i}',
                back_text=f'Back text {i}',
                created_by=self.user
            )
            self.card_list.append(card)

    def test_adding_and_deleting_boxes_on_session(self):
        boxes = []
        n = 10  # Number of boxes to create
        j = 3  # Must be strictly less than n. Box number to delete.
        # Box creation
        for i in range(n):
            boxes.append(self.session.add_box(f'Box number {i}'))
        self.assertEqual(self.session.box_set.count(), n)  # Asserts box have been added
        # Box deletion
        self.session.delete_box(boxes[j])
        self.assertEqual(self.session.box_set.count(), n - 1)  # Asserts box has been deleted
        for idx, box in enumerate(self.session.box_set.all().order_by('position')):
            self.assertEqual(box.position, idx)  # Asserts boxes are in ascending order

    def test_exception_when_deleting_box_not_in_session(self):
        new_session = Session.objects.create(
            description='Nothing important',
            created_by=self.user,
        )
        with self.assertRaises(AttributeError):
            new_box = Box.objects.create(description='random description', session=new_session,
                                         position=0)
            self.session.delete_box(new_box)

    def test_add_cards_to_box(self):
        # add 3 boxes to the session
        boxes = [Box.objects.create(description=f'Box number {i}',
                                    session=self.session,
                                    position=i)
                 for i in range(3)]
        self.assertEqual(self.session.box_set.count(), 3)  # Make sure the boxes were created

        # Add cards to random box in random locations
        for card in self.card_list:
            # FixMe: I should not use randoms in tests
            selected_box = boxes[randint(0, 2)]
            selected_box.add_card(card, where=choice(('first', 'last')))
            self.assertTrue(card in selected_box.cards_in_box())

        # Assert the cards are in order
        for box in boxes:
            for idx, relation in enumerate(box.cardboxrelation_set.all().order_by('card_position_in_box')):
                self.assertEqual(idx, relation.card_position_in_box)

        # Assert exception is raised when adding a card already in the session
        self.assertRaises(AttributeError, boxes[0].add_card, self.card_list[0])

        with self.assertRaises(ValueError):
            # When the 'where' argument isn't valid
            new_card = Card.objects.create(front_text='a', back_text='b',
                                           created_by=self.user)
            boxes[0].add_card(new_card, where='Wherever')

    def test_delete_and_move_cards_between_boxes(self):
        boxes = [self.session.add_box('First box'), self.session.add_box('Second box'),
                 self.session.add_box('Third box')]

        for idx, card in enumerate(self.card_list):
            box_number = idx % 3
            where = ('first', 'last')[idx % 2]
            boxes[box_number].add_card(card, where=where)
            # box 0 has 4 cards, boxes 1 and 2 have 3 cards

        self.assertEqual(self.session.box_set.count(), 3)  # Make sure we have 3 boxes
        boxes[0].delete_card(self.card_list[3])  # Card in position 1 that exists in the box,
        # remember position starts at 0
        self.assertEqual(boxes[0].cards_in_box().count(), 3)  # Confirms the card has been deleted

        for idx, card_relation in enumerate(boxes[0].cardboxrelation_set.order_by('card_position_in_box')):
            # Make sure the cards are ordered
            self.assertEqual(card_relation.card_position_in_box, idx)

        # Move card from one box to another
        boxes[0].move_card_to_box(self.card_list[0], boxes[1])
        # Assert a card was removed from box 0 and a card was added to box 1
        self.assertEqual(boxes[0].cards_in_box().count(), 2)
        self.assertEqual(boxes[1].cards_in_box().count(), 4)

        # Assert the cards are correctly ordered in both boxes
        for idx, card_relation in enumerate(boxes[0].cardboxrelation_set.order_by('card_position_in_box')):
            self.assertEqual(card_relation.card_position_in_box, idx)

        for idx, card_relation in enumerate(boxes[1].cardboxrelation_set.order_by('card_position_in_box')):
            self.assertEqual(card_relation.card_position_in_box, idx)

        # Assert the card was moved correctly
        self.assertTrue(self.card_list[0] not in boxes[0].card_set.all())
        self.assertTrue(self.card_list[0] in boxes[1].card_set.all())

        # Assert can't move a card that is not in the box
        self.assertRaises(KeyError, boxes[0].move_card_to_box, self.card_list[0], boxes[2])
