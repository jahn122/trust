from ._builtin import Page, WaitPage
from .models import Constants
from otree.api import Currency as c, currency_range

class PrepPage(Page):

    form_model = 'player'

    form_fields = ['participant_number']

    def is_displayed(self):
        return self.round_number == 1


class Introduction(Page):
    def is_displayed(self):
        return self.round_number == 1


class Send(Page):
    """Investors:
    Send an amount (all, some, or none) to the Trustee
    The amount you give will be tripled by experimenter,
    (i.e if you send 5, the amount received by the other player  is 15)"""

    form_model = 'group'
    form_fields = ['invest']

    def is_displayed(self):
        return self.player.id_in_group == 1


class SendBackWaitPage(WaitPage):
    template_name = 'trust/WaitPage.html'
    pass


class SendBack(Page):
    """This page is only for RAs
    The RA will send an amount (of the tripled amount received) to the participant"""

    form_model = 'group'

    form_fields = ['reciprocate']

    def is_displayed(self):
        return self.player.id_in_group == 2

    def vars_for_template(self):
        tripled_amount = self.group.invest * Constants.multiplier

        payoffA = Constants.endowment - self.group.invest

        # self.player.condition_number = Constants.condition_num
        # condition_number = self.group.condition_number
        # self ~ this

        # return name after finishing function through dictionary

        return dict(
            round_number=self.round_number,
            tripled_amount=tripled_amount,
            payoffA=payoffA,
            prompt='Please choose the range of percentage you want to give back from amount of money you have: {}'.format(
                tripled_amount)
        )


class ResultsWaitPage(WaitPage):

    template_name = 'trust/WaitPage.html'

    def after_all_players_arrive(self):
        self.group.set_payoffs()


class Results(Page):
    """Earnings of each player"""

    def vars_for_template(self):
        return dict(
            round_number=self.round_number,
            tripled_amount=self.group.invest * Constants.multiplier,
            reciprocate=c(round(self.group.invest * Constants.multiplier * self.group.reciprocate, 0)),
            reciprocate_percent = int(self.group.reciprocate * 100),
            user_total_profits = self.subsession.session.vars['user_profits'][self.round_number - 1],
            pa_total_profits = self.subsession.session.vars['ra_profits'][self.round_number - 1]
        )


'''
note:

1. Unit points instead of money

2. survey: before round 1, 5, the end 

3. Y/N order randomly flipped between subjects at the beginning

4. researcher<->participants if{one of participants not showing up}
Tell researcher still get reward points
researcher {a. mean person b. generous}

5. randomly assigned SAD measure

6. demographic(age, sex, race, first language)

'''

page_sequence = [
    PrepPage,
    Introduction,
    Send,
    SendBackWaitPage,
    SendBack,
    ResultsWaitPage,
    Results,
]
