
from typing import List
from bot import Bot
from type.poker_action import PokerAction
from type.round_state import RoundStateClient

import eval7


class SimplePlayer(Bot):
    hands_data = {
        # Pocket Pairs
        'AA': [0.8490, 0.7320, 0.6360, 0.5560, 0.4900],
        'KK': [0.8210, 0.6860, 0.5800, 0.4950, 0.4270],
        'QQ': [0.7960, 0.6470, 0.5320, 0.4440, 0.3760],
        'JJ': [0.7710, 0.6090, 0.4890, 0.4000, 0.3320],
        'TT': [0.7470, 0.5720, 0.4490, 0.3600, 0.2950],
        '99': [0.7170, 0.5330, 0.4080, 0.3230, 0.2630],
        '88': [0.6870, 0.4960, 0.3730, 0.2910, 0.2370],
        '77': [0.6570, 0.4610, 0.3410, 0.2640, 0.2150],
        '66': [0.6270, 0.4280, 0.3120, 0.2420, 0.1980],
        '55': [0.5960, 0.3960, 0.2860, 0.2210, 0.1820],
        '44': [0.5630, 0.3640, 0.2600, 0.2030, 0.1700],

        # Ace-High hands
        'AKs': [0.6620, 0.4980, 0.4050, 0.3450, 0.3020],
        'AKo': [0.6450, 0.4730, 0.3760, 0.3140, 0.2700],
        'AQs': [0.6400, 0.4640, 0.3650, 0.3020, 0.2570],
        'AQo': [0.6400, 0.4640, 0.3650, 0.3020, 0.2570],
        'AJs': [0.6300, 0.4500, 0.3490, 0.2850, 0.2400],
        'AJo': [0.6300, 0.4500, 0.3490, 0.2850, 0.2400],
        'ATs': [0.6200, 0.4370, 0.3340, 0.2700, 0.2260],
        'ATo': [0.6200, 0.4370, 0.3340, 0.2700, 0.2260],
        'A9s': [0.6000, 0.4080, 0.3040, 0.2410, 0.1980],
        'A8s': [0.5890, 0.3960, 0.2910, 0.2290, 0.1870],
        'A7s': [0.5770, 0.3820, 0.2790, 0.2170, 0.1770],
        'A6s': [0.5640, 0.3680, 0.2660, 0.2070, 0.1680],
        'A5s': [0.5630, 0.3700, 0.2700, 0.2110, 0.1730],
        'A4s': [0.5530, 0.3600, 0.2620, 0.2050, 0.1680],

        # King-High hands
        'KQs': [0.6240, 0.4610, 0.3720, 0.3150, 0.2740],
        'KQo': [0.6050, 0.4340, 0.3420, 0.2830, 0.2400],
        'KJs': [0.5990, 0.4260, 0.3330, 0.2740, 0.2320],
        'KJo': [0.5990, 0.4260, 0.3330, 0.2740, 0.2320],
        'KTs': [0.5900, 0.4130, 0.3190, 0.2600, 0.2190],
        'KTo': [0.5900, 0.4130, 0.3190, 0.2600, 0.2190],
        'K9s': [0.5700, 0.3860, 0.2900, 0.2310, 0.1910],
        'K8s': [0.5500, 0.3610, 0.2650, 0.2080, 0.1700],

        # Queen-High hands
        'QJs': [0.5910, 0.4310, 0.3450, 0.2910, 0.2510],
        'QJo': [0.5700, 0.4020, 0.3140, 0.2580, 0.2180],
        'QTs': [0.5650, 0.3960, 0.3090, 0.2530, 0.2130],
        'QTo': [0.5650, 0.3960, 0.3090, 0.2530, 0.2130],
        'Q9s': [0.5450, 0.3690, 0.2800, 0.2240, 0.1860],

        # Jack-High hands
        'JTs': [0.5620, 0.4070, 0.3260, 0.2740, 0.2370],
        'JTo': [0.5380, 0.3770, 0.2940, 0.2410, 0.2020],
        'J9s': [0.5230, 0.3570, 0.2740, 0.2210, 0.1840],

        # Ten-High hands
        'T9s': [0.5240, 0.3740, 0.2970, 0.2470, 0.2120],
    }

    def __init__(self):
        super().__init__()
        self.starting_chips = 0
        self.player_hands = []
        self.blind_amount = 0
        self.big_blind_player_id = 0
        self.small_blind_player_id = 0
        self.all_players = []
        self.num_active_players = 0

    def on_start(self, starting_chips: int, player_hands: List[str], blind_amount: int, big_blind_player_id: int, small_blind_player_id: int, all_players: List[int]):
        print("Player called on game start")
        print("Player hands: ", player_hands)
        print("Blind: ", blind_amount)
        print("Big blind player id: ", big_blind_player_id)
        print("Small blind player id: ", small_blind_player_id)
        print("All players in game: ", all_players)
        self.starting_chips = starting_chips
        self.player_hands = [player_hands[i] for i in range(len(player_hands))]
        self.blind_amount = blind_amount
        self.big_blind_player_id = big_blind_player_id
        self.small_blind_player_id = small_blind_player_id
        self.all_players = all_players
        self.num_active_players = len(all_players)

    def on_round_start(self, round_state: RoundStateClient, remaining_chips: int):
        print("Player called on round start")
        print("Round state: ", round_state)

    def get_action(self, round_state: RoundStateClient, remaining_chips: int):
        """ Returns the action for the player. """
        print("Player called get action")
        amount_to_call = round_state.current_bet - round_state.player_bets[str(self.id)]

        probability = 0
        if round_state.round_num == 0:
            probability = self.prob_preflop(probability)
            if probability == 0 and amount_to_call > 0:
                print(f"Folded on a hand of {self.player_hands}")
                return PokerAction.FOLD, 0
            elif probability > 0:
                print(f"Called on a hand of {self.player_hands}")
            else:
                print("Checked as the big blind")

        raised = False
        for player_action in round_state.player_actions.values():
            if player_action == "Raise":
                raised = True
                break

        if not raised and round_state.round_num == 1:
            return PokerAction.RAISE, 100
        
        if round_state.current_bet == 0:
            return PokerAction.CHECK, 0

        return PokerAction.CALL, amount_to_call

    def on_end_round(self, round_state: RoundStateClient, remaining_chips: int):
        """ Called at the end of the round. """
        print("Player called on end round")

    def on_end_game(self, round_state: RoundStateClient, player_score: float, all_scores: dict, active_players_hands: dict):
        print("Player called on end game, with player score: ", player_score)
        print("All final scores: ", all_scores)
        print("Active players hands: ", active_players_hands)
        self.num_active_players = len(active_players_hands)

    def prob_preflop(self, probability):
        hand = self.player_hands[0][0] + self.player_hands[1][0]
        if self.player_hands[0][0] != self.player_hands[1][0]:
            if self.player_hands[0][1] == self.player_hands[1][1]:
                hand += 's'
            else:
                hand += 'o'
        if hand in self.hands_data.keys():
            probability = self.hands_data[hand][self.num_active_players - 2]
        elif len(hand) == 3:
            hand_alt = hand[1] + hand[0] + hand[2]
            if hand_alt in self.hands_data.keys():
                probability = self.hands_data[hand_alt][self.num_active_players - 2]
        return probability
