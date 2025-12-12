"""
Simple Konkani messages for Riya
"""

import random


class KonkaniLove:
    """
    Simple everyday Konkani phrases.
    """
    
    def __init__(self):
        self.messages = [
            {"konkani": "Raav tu", "meaning": "Wait for me"},
            {"konkani": "Ravta", "meaning": "I am waiting"},
            {"konkani": "Teek bai", "meaning": "Okay fine"},
            {"konkani": "Jevan zalem?", "meaning": "Did you eat?"},
            {"konkani": "Bore nidh", "meaning": "Sleep well"},
            {"konkani": "Ghara vach", "meaning": "Go home"},
            {"konkani": "Kalle", "meaning": "Tomorrow"},
            {"konkani": "Sang mare", "meaning": "Tell me"},
            {"konkani": "Tuka miss karta", "meaning": "Missing you"},
            {"konkani": "Kit asa tu?", "meaning": "Where are you?"},
            {"konkani": "Kitem korta?", "meaning": "What are you doing?"},
            {"konkani": "Yeta hanv", "meaning": "I am coming"},
            {"konkani": "Zata raav", "meaning": "Will change with time"},
            {"konkani": "Tu jaisi hai vaisi teek", "meaning": "You are perfect as you are"},
            {"konkani": "Ani kai naka", "meaning": "Nothing else needed"},
        ]
    
    def random(self):
        """Get a random message."""
        return random.choice(self.messages)
    
    def all(self):
        """Get all messages."""
        return self.messages
    
    def say(self):
        """Print a random message."""
        msg = self.random()
        print(f"{msg['konkani']} - {msg['meaning']}")
        return msg
    
    def show_all(self):
        """Print all messages."""
        for msg in self.messages:
            print(f"{msg['konkani']} - {msg['meaning']}")


def get_random_message():
    """Get a random message."""
    return KonkaniLove().random()


def get_all_messages():
    """Get all messages."""
    return KonkaniLove().all()
