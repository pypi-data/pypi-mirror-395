import pytest
from libfelix.music import get_players, score_players


@pytest.fixture
def players():
    return list(get_players())


def test_dbus_usage(players):
    """
    try https://dbus.freedesktop.org/doc/dbus-python/tutorial.html#interfaces-and-methods
    """
    assert players[0].proxy.Introspect(
        dbus_interface='org.freedesktop.DBus.Introspectable'
    )


def test():
    players = get_players()
    scored_players = score_players(players)
    for score, player in scored_players.items():
        assert score >= 0
        assert player.playback_status()
