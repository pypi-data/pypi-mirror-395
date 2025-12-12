import click

from .api import get_players, score_players, get_best_player

players = get_players()
scored_players = score_players(players)


@click.group()
def main():
    pass


@main.command(name='PlayPause')
def playpause():
    player = get_best_player(scored_players)
    player.call_method('PlayPause')


@main.command(name='Previous')
def play_prev():
    player = get_best_player(scored_players)
    player.call_method('Previous')


@main.command(name='Next')
def play_next():
    player = get_best_player(scored_players)
    player.call_method('Next')


@main.command(name='players')
def _players():
    for score, player in scored_players.items():
        print(score, player)


if __name__ == '__main__':
    main()
