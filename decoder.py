import pathlib
import struct

class Replay:
    def __init__(self, path: str):
        self.data = self.open_file(path)
        self.offset = 0

    def open_file(self, path: str) -> bytes:
        file = open(pathlib.Path(path), 'rb')
        data = file.read()
        file.close()
        return data

    def decode_replay(self) -> dict:
        replay_data = dict()
        replay_data['game_mode'] = self.decode_data('b')
        replay_data['game_version'] = self.decode_data('i')
        replay_data['beatmap_hash'] = self.decode_string()
        replay_data['player_name'] = self.decode_string()
        replay_data['replay_hash'] = self.decode_string()
        replay_data['300_count'] = self.decode_data('h')
        replay_data['100_count'] = self.decode_data('h')
        replay_data['50_count'] = self.decode_data('h')
        replay_data['geki_count'] = self.decode_data('h')
        replay_data['katu_count'] = self.decode_data('h')
        replay_data['miss_count'] = self.decode_data('h')
        replay_data['total_score'] = self.decode_data('i')
        replay_data['highest_combo'] = self.decode_data('h')
        replay_data['perfect_combo'] = self.decode_data('b')
        replay_data['mods_used'] = self.decode_data('i')
        replay_data['life_bar_graph'] = self.decode_string()
        replay_data['time_stamp'] = self.decode_data('l')
        replay_data['byte_length'] = self.decode_data('i')
        replay_data['byte_array'] = self.decode_data('b')
        replay_data['online_score_id'] = self.decode_data('l')
        replay_data['target_practice_mod'] = self.decode_data('d')

        return replay_data
    
    def decode_data(self, data_type: str) -> int:
        output = struct.unpack_from(data_type, self.data, self.offset)
        self.offset += struct.calcsize(data_type)
        return output[0]
    
    def decode_string(self) -> str:
        if self.data[self.offset] == 0x00:
            self.offset += 1
        elif self.data[self.offset] == 0x0b:
            self.offset += 1
            length = self.decode_ule(self.data[self.offset])
            self.offset += 1
            string = self.data[self.offset:self.offset+length].decode('utf-8')
            self.offset += length
            return string
        else:
            raise ValueError('Initial value is ', self.data[self.offset], ', expected 0x00 or 0x0b')
        
    def decode_ule(self, value: int) -> int:
        '''
        Converts a value in unsigned little endian base 128 to decimal
        '''
        output = 0
        iteration = 0
        
        while True:
            chunk = value & 0b01111111          # ignore the most significant bit
            output += chunk << iteration * 7    # insert the chunk into the return value
            if value < 0b10000000:              # exit loop if the most significant bit is zero
                break
            iteration += 1                      # constant to multiple by 7
            value = value >> 8                  # shift to next byte

        return output
    
def run() -> None:
    path = 'replay/chmpchmp - supercell - Hero [Villain] (2023-04-19) Osu.osr'
    path = 'replay/chmpchmp - Suzuyu - Euphorium [The Dream Of White Star.] (2022-10-28) Osu.osr'
    replay = Replay(path)
    replay_data = replay.decode_replay()

    for key, value in replay_data.items():
        print(f'>> {key}: {value}')

if __name__ == '__main__':
    run()