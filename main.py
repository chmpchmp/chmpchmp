from replay import Replay

def run() -> None:
    path = 'replay/chmpchmp - supercell - Hero [Villain] (2023-04-19) Osu.osr'
    path = 'replay/chmpchmp - Suzuyu - Euphorium [The Dream Of White Star.] (2022-10-28) Osu.osr'
    replay = Replay(path)
    replay_data = replay.decode_replay()

    for key, value in replay_data.items():
        print(f'>> {key}: {value}')

if __name__ == '__main__':
    run()