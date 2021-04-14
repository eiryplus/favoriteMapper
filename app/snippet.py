import os
import json
import matplotlib.pyplot as plt
import pygame
from enum import Enum

pygame.mixer.init()
EXTRACT_PATH = r'C:\var\development\favoriteMapper\data\extract\57c'


class Hand(Enum):
    LEFT = 0
    RIGHT = 1


class Arrow(Enum):
    UP = 0
    DOWN = 1
    LEFT = 2
    RIGHT = 3
    UPPER_LEFT = 4
    UPPER_RIGHT = 5
    LOWER_LEFT = 6
    LOWER_RIGHT = 7
    DOT = 8
    MAX = DOT


class Vertical(Enum):
    BOTTOM = 0
    MIDDLE = 1
    TOP = 2
    MAX = TOP


class Horizontal(Enum):
    LEFT = 0
    CENTER_LEFT = 1
    CENTER_RIGHT = 2
    RIGHT = 3
    MAX = RIGHT


class InfoDat:
    def __init__(self):
        with open(os.path.join(EXTRACT_PATH, "info.dat"), "r", encoding="utf-8") as fp:
            self._data = json.load(fp)

    def get_beats_per_minute(self):
        return self._data["_beatsPerMinute"]

    def get_song_length(self):
        song_file = os.path.join(EXTRACT_PATH, self._data["_songFilename"])
        sound = pygame.mixer.Sound(song_file)
        return sound.get_length()


class DifficultyMap:
    def __init__(self, difficulty_file, song_length, beats_per_minute):
        self.song_length = song_length
        self.beats_per_minute = beats_per_minute
        with open(os.path.join(EXTRACT_PATH, difficulty_file), "r", encoding="utf-8") as fp:
            self._data = json.load(fp)
        self._coefficient = 60 / beats_per_minute

    def get_nps(self):
        return len(self._data) / self.song_length

    def get_notes_per_second(self):
        seconds = list(range(int(self.song_length) + 1))
        all_notes = [0 for _ in seconds]
        left_notes = all_notes.copy()
        right_notes = all_notes.copy()
        for note in self._data["_notes"]:
            second = int(note["_time"] * self._coefficient)
            all_notes[second] += 1
            if note["_type"] == Hand.LEFT.value:
                left_notes[second] += 1
            else:
                right_notes[second] += 1
        return seconds, all_notes, left_notes, right_notes

    def get_chart_data(self):
        step = 5
        result_seconds = []
        result_all_notes = []
        result_left_notes = []
        result_right_notes = []
        seconds, all_notes, left_notes, right_notes = self.get_notes_per_second()
        for s in range(0, max(seconds), step):
            from_ = s
            to_ = s + step
            result_seconds.append(s)
            result_all_notes.append(max(all_notes[from_:to_]))
            result_left_notes.append(max(left_notes[from_:to_]))
            result_right_notes.append(max(right_notes[from_:to_]))
        return result_seconds, result_all_notes, result_left_notes, result_right_notes


def main():
    info_dat = InfoDat()
    map_ = DifficultyMap(
        "Hard.dat",
        info_dat.get_song_length(),
        info_dat.get_beats_per_minute()
    )
    seconds, all_notes, left_notes, right_notes = map_.get_chart_data()
    # chart initialization
    plt.xlabel("second")
    plt.ylabel("note count")
    plt.grid(True)
    plt.plot(seconds, all_notes, label="ALL")
    plt.plot(seconds, left_notes, label="LEFT")
    plt.plot(seconds, right_notes, label="RIGHT")
    plt.show()


if __name__ == "__main__":
    main()
    if True:
        hoge = "Hagu"
    print(hoge)
