import re
from logging import getLogger
from typing import Optional, Set, Tuple

from .bidding_system import BiddingSystem
from .playing_system import PlayingSystem
from .socket_interface import SocketInterface
from .. import Bid, BiddingPhase, BiddingPhaseState, Card, Contract, Pair, \
    Player, Suit, Vul
from ..playing_phase import ObservedPlayingPhase

logger = getLogger(__file__)


class Client(SocketInterface):
    """Client of network computer bridge programs.
    Four clients play each hand.

    Protocol version == 18 (1 August 2005)
    http://www.bluechipbridge.co.uk/protocol.htm
    """
    PROTOCOL_VERSION = 18

    def __init__(self,
                 player: Player,
                 team_name: str,
                 bidding_system: BiddingSystem,
                 playing_system: PlayingSystem,
                 ip_address: str,
                 port: int):
        super().__init__(ip_address=ip_address, port=port)
        self.player = player
        self.team_name = team_name
        self.bidding_system = bidding_system
        self.playing_system = playing_system

        # assigned in self._connection()
        self.opponent_team_name: Optional[str] = None

    def _connect(self) -> None:
        """Connects with the server."""
        self._socket.connect((self.ip_address, self.port))
        super().send_message(f'Connecting "{self.team_name}" as '
                             f'{self.player.formal_name} using '
                             f'protocol version {self.PROTOCOL_VERSION}')

        reply = super().receive_message()
        if reply != f'{self.player.formal_name} {self.team_name} seated' and \
                reply != f'{self.player.formal_name} ("{self.team_name}") seated':
            raise Exception(f'Unexpected message received. {reply}')

        super().send_message(f'{self.team_name} ready for teams')

        team_ns, team_ew = self.parse_team_names(super().receive_message())
        if self.player.pair is Pair.NS:
            if team_ns != self.team_name:
                raise Exception('')
            self.opponent_team_name = team_ew
        else:
            if team_ew != self.team_name:
                raise Exception('')
            self.opponent_team_name = team_ns

        super().send_message(f'{self.player.formal_name} ready to start')

    @staticmethod
    def parse_team_names(content: str) -> Tuple[str, str]:
        """Parses a message about teams.

        The message style is
        "Teams : N/S : "[N/S team name]". E/W : "[E/W team name]""

        :param content: Message to be parsed.
        :return: Team names of NS pair and EW pair.
        """
        pattern = r'Teams : N/S : "(.*)".? E/W : "(.*)"'
        match = re.match(pattern, content)
        if not match:
            raise Exception('Parse exception. '
                            f'Content "{content}" does not match the pattern.')
        team_ns, team_ew = match.group(1), match.group(2)
        return team_ns, team_ew

    @staticmethod
    def parse_board(content: str) -> Tuple[int, Player, Vul]:
        pattern = r'Board number (\d+)\. Dealer (.*)\. (.*) vulnerable\.'
        match = re.match(pattern, content)
        if match is None:
            raise Exception('Parse exception. '
                            f'Content "{content}" does not match the pattern.')
        board_num = int(match.group(1))
        dealer = Player.convert_formal_name(match.group(2))
        str_vulnerable = match.group(3)
        vul: Vul
        if str_vulnerable == 'Neither':
            vul = Vul.NONE
        elif str_vulnerable == 'N/S':
            vul = Vul.NS
        elif str_vulnerable == 'E/W':
            vul = Vul.EW
        elif str_vulnerable == 'Both':
            vul = Vul.BOTH
        else:
            raise Exception('Vulnerable does not match correct patterns.')
        return board_num, dealer, vul

    @staticmethod
    def parse_cards(content: str, player_name: str) -> str:
        pattern = fr'{player_name}\'s cards : (.*)'
        match = re.match(pattern, content)
        if not match:
            raise Exception('Parse exception. '
                            f'Content "{content}" does not match the pattern.')
        hand_str = match.group(1)
        return hand_str

    @staticmethod
    def parse_hand(content: str) -> Tuple[Set[Card], Tuple[int, ...]]:
        pattern = r'S (.*)\. H (.*)\. D (.*)\. C (.*)\.\s?'
        match = re.match(pattern, content)
        if not match:
            raise Exception('Parse exception. '
                            f'Content "{content}" does not match the pattern.')
        hand_list = [0] * 52
        hand_set = set()
        for ranks, suit in zip(map(lambda s: s.split(' '), match.groups()),
                               [Suit.S, Suit.H, Suit.D, Suit.C]):
            for rank in ranks:
                if rank == '-':
                    continue
                card = Card(Card.rank_str_to_int(rank), suit)
                hand_set.add(card)
                hand_list[int(card)] = 1
        return hand_set, tuple(hand_list)

    @staticmethod
    def parse_bid(content: str, player_name: str) -> Bid:
        bid_pattern = fr'{player_name} bids (\d)(C|D|H|S|NT)'
        match = re.match(bid_pattern, content)
        if match:
            return Bid.level_suit_to_bid(level=int(match.group(1)),
                                         suit=Suit[match.group(2)])
        pattern = fr'{player_name} (.*)'
        match = re.match(pattern, content)
        if not match:
            raise Exception('Parse exception. '
                            f'Content "{content}" does not match the pattern.')
        bid = match.group(1).lower()
        if bid == 'passes':
            return Bid.Pass
        elif bid == 'doubles':
            return Bid.X
        elif bid == 'redoubles':
            return Bid.XX
        raise Exception(f'Illegal bid received. {bid}')

    def _deal(self):
        super().send_message(f'{self.player.formal_name} ready for deal')
        self.board_num, self.dealer, self.vul = self.parse_board(
            super().receive_message())
        self.send_message(f'{self.player.formal_name} ready for cards')

        hand_str = self.parse_cards(super().receive_message(),
                                    self.player.formal_name)
        self.hand_set, self.hand_binary = self.parse_hand(hand_str)

        logger.info(f'board num #{self.board_num}, dealer = {self.dealer}, '
                    f'vul = {self.vul}, hand = {self.hand_set} '
                    f'({self.hand_binary})')

    @staticmethod
    def create_bid_message(bid: Bid, player_name: str) -> str:
        if bid is Bid.Pass:
            str_bid = 'passes'
        elif bid is Bid.X:
            str_bid = 'doubles'
        elif bid is Bid.XX:
            str_bid = 'redoubles'
        else:
            str_bid = f'bids {bid}'
        return f'{player_name} {str_bid}'

    # TODO: unit test
    def bidding_phase(self) -> Contract:
        """Bidding phase.

            If the Table Manager (Server) receives an illegal bid, it will
            ignore it and respond "illegal Bid". It is assumed that playing
            programs will ensure that playing programs will ensure that they do
            not make illegal bids. The protocol does not define what will then
            happen.

        :return: Contract of the bidding phase.
        """
        # TODO: Consider alerting
        env = BiddingPhase(dealer=self.dealer, vul=self.vul)
        logger.info(f'player: {self.player}')
        while not env.has_done():
            logger.info(f'active player: {env.active_player}')
            if env.active_player is self.player:
                # take an action
                bid = self.bidding_system.bid(self.hand_binary, env)
                super().send_message(
                    self.create_bid_message(bid, self.player.formal_name))
            else:
                assert env.active_player is not None
                super().send_message(f'{self.player.formal_name} ready '
                                     f'for {env.active_player.formal_name}\'s bid')
                message = super().receive_message()
                bid = self.parse_bid(message,
                                     env.active_player.formal_name)
            bidding_phase_state = env.take_bid(bid)
            if bidding_phase_state is BiddingPhaseState.illegal:
                raise Exception('')
            if bidding_phase_state is BiddingPhaseState.finished:
                break

        contract = env.contract()
        assert contract is not None
        # TODO: Consider not to return None when env is not finished.
        return contract

    @staticmethod
    def parse_leader_message(content: str, dummy: Player) -> Player:
        pattern = r'(.*) to lead'
        match = re.match(pattern, content)
        if not match:
            raise Exception('Parse exception. '
                            f'Content "{content}" does not match the pattern.')
        player_name = match.group(1)
        if player_name == 'Dummy':
            return dummy
        return Player.convert_formal_name(player_name)

    @staticmethod
    def card_str(card: Card) -> str:
        """Convert card object to str of format [value] + [suit].

            an alternative suggestion is [suit] + [value] format, which is same
            as str(card).

        :param card: Card instance.
        :return: [value] + [suit] format.
        """
        return Card.rank_int_to_str(card.rank) + card.suit.name

    @staticmethod
    def parse_card(content: str, player: Player) -> Card:
        pattern = f'{player.formal_name} plays (.*)'
        match = re.match(pattern, content)
        if not match:
            raise Exception('Parse exception. '
                            f'Content "{content}" does not match the pattern.')
        card_str = match.group(1).upper()
        if card_str[0] in {'S', 'H', 'D', 'C'}:
            return Card(Card.rank_str_to_int(card_str[1]), Suit[card_str[0]])
        return Card(Card.rank_str_to_int(card_str[0]), Suit[card_str[1]])

    # TODO: unit test
    # Use this function?
    @staticmethod
    def parse_timing(content: str):
        pattern = r'Timing - N/S : this board (*.), total (*.). ' \
                  r'E/W : this board (*.), total (.*)'
        match = re.match(pattern, content)
        if not match:
            raise Exception('Parse exception. '
                            f'Content "{content}" does not match the pattern.')
        # TODO: process matched pattern

    # TODO: unit test
    def playing_phase(self, contract: Contract) -> None:
        assert not contract.is_passed_out()
        declarer = contract.declarer
        assert declarer is not None
        dummy = declarer.partner

        env = ObservedPlayingPhase(contract=contract,
                                   player=self.player,
                                   hand=self.hand_set)
        hand_open = False
        while not env.has_done():
            if (env.active_player is self.player and self.player is not dummy) \
                    or (env.active_player is dummy and self.player is declarer):
                leader = self.parse_leader_message(super().receive_message(),
                                                   dummy)
                assert leader is env.active_player

            for _ in range(4):
                # open dummy's hand
                if env.active_player is dummy and not hand_open:
                    hand_open = True
                    if dummy is not self.player:
                        super().send_message(f'{self.player.formal_name} '
                                             f'ready for dummy')
                        dummy_hand, _ = self.parse_hand(
                            self.parse_cards(super().receive_message(),
                                             'Dummy'))
                        env.set_dummy_hand(dummy_hand)

                if env.active_player is self.player and self.player is not dummy:
                    card = self.playing_system.play(self.hand_set, env)
                    env.play_card_by_player(card, self.player)
                    super().send_message(
                        f'{self.player.formal_name} plays {self.card_str(card)}')
                elif env.active_player is dummy and self.player is declarer:
                    assert env.dummy_hand is not None
                    card = self.playing_system.play(env.dummy_hand, env)
                    env.play_card_by_player(card, dummy)
                    super().send_message(
                        f'{dummy.formal_name} plays {self.card_str(card)}')
                else:
                    active_player_name = env.active_player.formal_name if \
                        env.active_player is not dummy else 'dummy'
                    super().send_message(
                        f'{self.player.formal_name} ready for '
                        f'{active_player_name}\'s card to '
                        f'trick {env.trick_num}')
                    card = self.parse_card(super().receive_message(),
                                           env.active_player)
                    env.play_card_by_player(card, env.active_player)

    def run(self) -> None:
        """Runs the client."""
        print('run')
        self._connect()

        message = super().receive_message()
        board_num = 1
        while True:
            if message != 'Start of Board':
                raise Exception()

            self._deal()

            contract = self.bidding_phase()
            if contract.is_passed_out():
                continue
            logger.info(f'contract is {contract}')

            self.playing_phase(contract)

            message = super().receive_message()
            if message == 'End of session':
                break
            board_num += 1