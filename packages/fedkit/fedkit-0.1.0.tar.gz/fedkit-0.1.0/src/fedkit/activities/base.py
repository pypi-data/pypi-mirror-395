from fedkit.activity import ActivityObject
from fedkit.models import Actor
from fedkit.signature import Signature


class BaseActivity(object):
    def __init__(
        self, target: Actor, activity: ActivityObject, signature: Signature
    ) -> None:
        self.actor = target
        self.activity = activity
        self.signature = signature

    def __str__(self):
        return f"Activity ID: {self.activity_id}, Name: {self.name}, Description: {self.description or 'No description provided'}"

    def respond(self) -> (dict, bool):
        """Method to respond to the activity."""
        raise NotImplementedError("This method should be overridden by subclasses.")
