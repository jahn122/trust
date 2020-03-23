from otree.api import Currency as c, currency_range
from . import pages
from ._builtin import Bot
from .models import Constants

class PlayerBot(Bot):

    def play_round(self):

        yield (pages.Introduction)

        if self.player.id_in_group == 1:
            yield (pages.Send, {"invest": 4})

        else:
            yield (pages.SendBack, {'reciprocate': 8})

        yield (pages.Results)
