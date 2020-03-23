from otree.api import (
    models, widgets, BaseConstants, BaseSubsession, BaseGroup, BasePlayer,
    Currency as c, currency_range
)
import random

doc = """
This is a standard 2-player trust game where the amount sent by player 1 gets
tripled. The trust game was first proposed by
<a href="http://econweb.ucsd.edu/~jandreon/Econ264/papers/Berg%20et%20al%20GEB%201995.pdf" target="_blank">
    Berg, Dickhaut, and McCabe (1995)
</a>.
"""


class Constants(BaseConstants):
    name_in_url = 'trust'
    players_per_group = 2
    num_rounds = 40
    condition_number = random.randint(1, 2)
    print('[STARTUP] Condition is ', condition_number)
    instructions_template = 'trust/instructions.html'

    # Initial amount allocated to each player
    endowment = c(10)
    multiplier = 3

class Subsession(BaseSubsession):
    def creating_session(self):
        if self.round_number == 1:
            self.session.vars['choice_prob'] = [None] * Constants.num_rounds
            self.session.vars['user_profits'] = [None] * Constants.num_rounds
            self.session.vars['ra_profits'] = [None] * Constants.num_rounds

        self.session.vars['choice_prob'][self.round_number - 1] = random.random()
        self.session.vars['user_profits'][self.round_number - 1] = 0
        self.session.vars['ra_profits'][self.round_number - 1] = 0
    pass


class Group(BaseGroup):  # investors/trustee role

    # invest
    invest = models.CurrencyField(
        min=0,
        max=Constants.endowment,
        choices=range(0, 10 + 1),
        widget=widgets.RadioSelectHorizontal,
        # individual choices (circle), comment out this line for dropdown choice menu
        doc="""Amount sent by Investor""",
    )

    #reciprocate by conditions

    if Constants.condition_number == 1: #con 1
        print('[Group] Set to condition 1')
        # Trustee (RA)
        reciprocate = models.FloatField(
            doc="""[RA only] Amount of money sent back by Trustee""",

            choices=[
                [0.45, "Block 1: 45-55%"],
                [0.55, "Block 2: 55-65%"],
                [0.65, "Block 3: 65-75%"],
                [0.75, "Block 4: 75-85%"]
            ],

            widget=widgets.RadioSelectHorizontal,
        )
    # self.session.vars['choice_prob'][self.round_number-1]
    else: #con 2
        print('[Group] Set to condition 2')
        reciprocate = models.FloatField(
            doc="""[RA only] Amount of money sent back by Trustee""",
            choices=[
                [0.45, "Block 1: 45-55%"],
                [0.35, "Block 2: 35-45%"],
                [0.25, "Block 3: 25-35%"],
                [0.15, "Block 4: 15-25%"]
            ],
            widget=widgets.RadioSelectHorizontal,
        )


    def reciprocate_max(self):
        return 1

    # Total payoff (result)
    def set_payoffs(self):
        p1 = self.get_player_by_id(1)
        p2 = self.get_player_by_id(2)
        self.reciprocate = self.reciprocate + self.subsession.session.vars['choice_prob'][self.round_number-1] * 0.1
        self.reciprocate = round(self.reciprocate, 3)
        p1.payoff = Constants.endowment - self.invest + (self.invest * Constants.multiplier * self.reciprocate)
        p2.payoff = self.invest * Constants.multiplier - (self.invest * Constants.multiplier * self.reciprocate)
        p1.payoff = round(p1.payoff, 0)
        p2.payoff = round(p2.payoff, 0)
        if self.round_number != 0:
            self.subsession.session.vars['user_profits'][self.round_number-1] = self.subsession.session.vars['user_profits'][self.round_number - 2] + p1.payoff
            self.subsession.session.vars['ra_profits'][self.round_number - 1] = self.subsession.session.vars['ra_profits'][self.round_number - 2] + p2.payoff
        else:
            self.subsession.session.vars['user_profits'][self.round_number-1] = p1.payoff
            self.subsession.session.vars['ra_profits'][self.round_number - 1] = p2.payoff

        p1.block_profits = self.subsession.session.vars['user_profits'][self.round_number - 1]
        p2.block_profits = self.subsession.session.vars['ra_profits'][self.round_number - 1]

class Player(BasePlayer):

    def role(self):
        return {1: 'Investor', 2: 'Trustee'}[self.id_in_group]

    invest = models.CurrencyField()
    reciprocate = models.CurrencyField()
    payoff_RA = models.CurrencyField()
    payoff_ppt = models.CurrencyField()
    participant_number = models.StringField()
    block_profits = models.CurrencyField(initial=0)
    total_profits = models.CurrencyField(initial=0)
    condition_number = models.IntegerField(initial=Constants.condition_number)