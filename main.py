from replay import Replay

def run() -> None:
    path = 'replay/chmpchmp - Suzuyu - Euphorium [The Dream Of White Star.] (2022-10-28) Osu.osr'
    
    replay_data = Replay(path).decode_replay()

    for key, value in replay_data.items():
        print(f'>> {key}: {value}')

    #assert replay_data['online_score_id'] == '4303493392'

if __name__ == '__main__':
    run()