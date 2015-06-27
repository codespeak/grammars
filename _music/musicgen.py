import configparser
import random
import os
import time
import subprocess
import multiprocessing
import difflib
from pynhost.grammars import baseutils, extension
from pynhost import grammarbase
from pynhost import api
from pynhost import dynamic
from pynhost import constants
from pynhost.grammars._music import musicutils, obj

class MusicGeneralGrammar(extension.ExtensionGrammar):
    def __init__(self):
        super().__init__()
        self.mapping = {
                '<hom_music> <hom_play> <any> <1->': self.play_song,
                '(<hom_music> <hom_stop> | <hom_music>.)': self.stop_song,
                '<hom_music> random': self.random_song,
                '<hom_music> mode (<hom_shuffle>)': self.shuffle_mode,
                '<hom_music> <hom_queue> <any> <1->': self.queue_music,
        }
        self.track_handler = obj.TrackHandler(musicutils.load_track_info(self.dirs['music']))
        self.tracks = musicutils.load_track_info(self.dirs['music'])
        self.play_process = None

    def play_song(self, words):
        music_search = obj.MusicSearch(words[2:], self.tracks)
        tracks = music_search.filter_results()
        if tracks:
            self.track_handler.play_tracks(tracks)

    def stop_song(self, words):
        self.track_handler.stop_song()

    def random_song(self, words):
        self.track_handler.play_random()

    def shuffle_mode(self, words):
        self.track_handler.mode = 'shuffle'

    def queue_music(self, words):
        music_search = obj.MusicSearch(words[2:], self.tracks)
        tracks = music_search.filter_results()
        if tracks:
            self.track_handler.track_queue.extendleft(tracks)
