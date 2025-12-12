#!/home/felix/bin/.venv/bin/python
import logging
import os
import re
from typing import Dict, Iterable, Literal, cast

import dbus

logging.basicConfig(level=os.environ.get('LOGLEVEL', 'warning').upper())
log = logging.getLogger('music')


RE_NAME = re.compile(r'org\.mpris\.MediaPlayer2\.(.+)(\.instance\d+)?')

bus = dbus.SessionBus()
PlaybackStatus = Literal['Playing', 'Paused']


class Player:
    MUSIC_PLAYERS = ['mpv', 'vlc']
    IFACE_PLAYER = 'org.mpris.MediaPlayer2.Player'
    IFACE_PROPS = 'org.freedesktop.DBus.Properties'

    def __init__(self, bus_name):
        self.bus_name = bus_name
        log.debug(f'Player("{bus_name}")')
        self.name = RE_NAME.match(bus_name).group(1)  # pyright: ignore[reportOptionalMemberAccess]
        self.proxy = bus.get_object(bus_name, '/org/mpris/MediaPlayer2')
        self.interface = dbus.Interface(
            self.proxy, dbus_interface=self.IFACE_PLAYER
        )
        self.props_iface = dbus.Interface(
            self.proxy, dbus_interface=self.IFACE_PROPS
        )

    def call_method(self, method_name):
        method = self.interface.get_dbus_method(method_name)
        return method()

    def get_prop(self, prop_name) -> str:
        return str(self.props_iface.Get(self.IFACE_PLAYER, prop_name))

    def playback_status(self) -> PlaybackStatus:
        # busctl --user get-property org.mpris.MediaPlayer2.spotify /org/mpris/MediaPlayer2 org.mpris.MediaPlayer2.Player PlaybackStatus
        return cast(PlaybackStatus, self.get_prop('PlaybackStatus'))

    def is_music_player(self) -> bool:
        return any([key in self.name for key in self.MUSIC_PLAYERS])

    def __repr__(self):
        return f'Player(name="{self.name}")'

    def __str__(self):
        return self.name


def get_players():
    # busctl --user | rg org.mpris.MediaPlayer2
    for n in bus.list_names():  # pyright: ignore[reportOptionalIterable]
        if n.startswith('org.mpris.MediaPlayer2'):
            p = Player(n)
            log.info(f'found player {p}')
            yield p


ScoredPlayers = Dict[float, Player]


def score_players(players: Iterable[Player]) -> ScoredPlayers:
    result = {}
    for player in players:
        score = 0
        if player.playback_status() == 'Playing':
            score += 3
            log.debug('playing: +3')
        if player.is_music_player():
            score += 2
            log.debug('is_music_player: +2')
        if 'firefox' in player.name:  # prefer firefox
            score += 1
            log.debug('firefox: +1')
        if 'spotify' in player.name:  # prefer spotify
            score += 1.1
            log.debug('spotify: +1.1')
        if score in result:  # on indentical scores, last one wins
            score = score + 0.01
            log.debug('last one: +0.01')
        log.debug(f'score({player}) = {score}')
        result[score] = player
    return result


def get_best_player(scored: ScoredPlayers) -> Player:
    highscore = next(reversed(sorted(scored)))
    winner = scored[highscore]
    log.debug(f'winner = {winner}')
    return winner
