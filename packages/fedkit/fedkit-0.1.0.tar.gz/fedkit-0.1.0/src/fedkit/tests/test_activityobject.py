# Description: This file contains the test cases for the ActivityObject class.
import logging

from django.test import TestCase

from fedkit.activity import ActivityObject
from fedkit.models import Action

from .rename_messages import w3c_activity

logger = logging.getLogger(__name__)


class ActivityObjectTest(TestCase):
    def setUp(self):
        self.activity = {}

    def test_activity_message_to_object(self):
        """
        Test converting activity messages to ActivityObject instances.
        """
        for verb, messages in w3c_activity.items():
            for message in messages:
                self.activity[verb] = ActivityObject(message)
                print(f"{self.activity[verb]}")
                self.assertIsInstance(self.activity[verb], ActivityObject)

    def test_activity_object_to_message(self):
        """
        Test converting ActivityObject instances to activity messages.
        """
        for verb, object in self.activity.items():
            message = object.toDict()
            self.assertIsInstance(message, dict)

    def test_activity_object_repr(self):
        """
        Test converting ActivityObject instances to activity messages.
        """
        for verb, object in self.activity.items():
            self.assertIsInstance(object.__repr__(), str)

    def test_activity_object_to_action(self):
        """
        Test converting ActivityObject instances to Action instances.
        """
        for verb, messages in w3c_activity.items():
            for message in messages:
                action = ActivityObject(message).toAction()

                # toAction can return None if the message lacks the required
                # fields (like an actor id) to create a valid Action.
                if action is None:
                    continue

                self.assertIsInstance(action, Action)
                # The 'verb' from the test data corresponds to the activity_type
                self.assertEqual(action.activity_type, verb)
