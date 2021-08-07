
from otree.api import *
c = cu

doc = '\nThis is a one-shot "Prisoner\'s Dilemma". Two players are asked separately\nwhether they want to cooperate or defect. Their choices directly determine the\npayoffs.\n'
class Constants(BaseConstants):
    name_in_url = 'prisoner1'
    players_per_group = 2
    num_rounds = 10
    betray_payoff = cu(5)
    betrayed_payoff = cu(0)
    both_cooperate_payoff = cu(3)
    both_defect_payoff = cu(1)
    instructions_template = 'prisoner1/instructions.html'
def after_all_players_arrive1(subsession):
    session = subsession.session
    subsession.group_randomly()
class Subsession(BaseSubsession):
    my_field = models.CurrencyField()
def set_payoffs(group):
    for p in group.get_players():
        set_payoff(p)
class Group(BaseGroup):
    pass
def other_player(player):
    group = player.group
    return player.get_others_in_group()[0]
def set_payoff(player):
    payoff_matrix = dict(
        Cooperate=dict(
            Cooperate=Constants.both_cooperate_payoff, Defect=Constants.betrayed_payoff
        ),
        Defect=dict(
            Cooperate=Constants.betray_payoff, Defect=Constants.both_defect_payoff
        ),
    )
    player.payoff = payoff_matrix[player.decision][other_player(player).decision]
    
class Player(BasePlayer):
    decision = models.StringField(choices=[['Cooperate', 'Cooperate'], ['Defect', 'Defect']], doc='This player s decision', widget=widgets.RadioSelect)
class ShuffleWaitPage(WaitPage):
    wait_for_all_groups = True
    after_all_players_arrive = 'after_all_players_arrive1'
class Introduction(Page):
    form_model = 'player'
    timeout_seconds = 300
class Decision(Page):
    form_model = 'player'
    form_fields = ['decision']
    timeout_seconds = 300
class ResultsWaitPage(WaitPage):
    after_all_players_arrive = 'set_payoffs'
class Results(Page):
    form_model = 'player'
    timeout_seconds = 300
    @staticmethod
    def vars_for_template(player):
        me = player
        opponent = other_player(me)
        return dict(
            my_decision=me.decision,
            opponent_decision=opponent.decision,
            same_choice=me.decision == opponent.decision,
        )
        
page_sequence = [ShuffleWaitPage, Introduction, Decision, ResultsWaitPage, Results]