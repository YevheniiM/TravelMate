from enum import Enum


class Progress(Enum):
    """
    The class represents the current progress of a player in the
    conversation with bot.

    """
    #  Welcome Part
    tour_does_not_start = 0
    are_you_ready_w = 1
    how_it_works_w = 2
    want_to_start = 3

    # The tour part
    tour_started = 4
