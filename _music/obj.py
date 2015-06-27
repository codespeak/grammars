import threading
import random
import threading
import time
import collections
import os
import difflib
import subprocess
from pynhost.grammars import baseutils

class TrackHandler:
    def __init__(self, tracks):
        self.tracks = tracks
        self.play_process = None
        self.current_track = None
        self.continuous = True
        # artist, album, title, shuffle. only matters when self.continuous is True
        self.play_by = 'title'
        self.track_queue = collections.deque()

    def stop_song(self):
        try:
            self.play_process.kill()
        except (AttributeError, ProcessLookupError):
            pass
        self.play_process = None
        self.track_queue.clear()
    
    def play_tracks(self, tracks):
        self.stop_song()
        self.track_queue.extendleft(tracks[1:])
        t = threading.Thread(target=self.begin_play_thread, args=(tracks[0],))
        t.start()

    def play_random(self):
        self.stop_song()
        random_track = random.choice(self.tracks)
        t = threading.Thread(target=self.begin_play_thread, args=(random_track,))
        t.start()
          
    def begin_play_thread(self, track):
        self.play_process = self.start_play_process(track)
        while self.continuous:
            try:
                self.play_process.poll()
                if self.play_process.returncode is not None:
                    print('next')
                    next_track = self.select_next_track()
                    self.play_process = self.start_play_process(next_track)
            except ValueError: # self.play_process is None - manual stop
                print('manual')
                return
            except ProcessLookupError: # song has ended on its own
                print('automatic')
                next_track = self.select_next_track()
                self.play_process = self.start_play_process(track)
            time.sleep(1)

    def select_next_track(self):
        print(self.track_queue)
        if self.track_queue:
            return self.track_queue.pop()
        return random.choice(self.tracks)

    def start_play_process(self, track):
        return subprocess.Popen(['mpg123', track.filename], stderr = open(os.devnull, 'wb'))

class Track:
    def __init__(self, filename):
        self.artist = ''
        self.album = ''
        self.title = ''
        self.filename = filename

    def __str__(self):
        return '<Track: {} - {}>'.format(self.artist, self.title)

    def __repr__(self):
        return str(self)

class MusicSearch:
    def __init__(self, search_text, tracks):
        self.tracks = tracks
        self.tracks_to_queue = []
        self.search_info = self.get_search_info(search_text)
        self.search_matches = self.get_search_matches()

    def get_search_info(self, search_words):
        subject = 'title'
        covered_subjects = set(['title'])
        search_info = {
            'title': '',
            'artist': '',
            'album': '',
        }
        for word in search_words:
            word = word.lower()
            if word in covered_subjects or word not in search_info:
                if search_info[subject]:
                    search_info[subject] += ' '
                search_info[subject] += word
            else:
                subject = word
                covered_subjects.add(subject)
        return search_info

    def get_search_matches(self):
        search_matches = {
            'title': [],
            'album': [],
            'artist': [],
        }
        for info in search_matches:
            if self.search_info[info]:
                search_matches[info] = self.search_subject(self.search_info[info],
                    [getattr(track, info).lower() for track in self.tracks if track])
        return search_matches

    def search_subject(self, search_value, info_list):
        print(search_value, info_list)
        matches = difflib.get_close_matches(search_value, info_list, cutoff=.6)
        # matches = baseutils.get_lev_matches(search_value, info_list)
        print('mat', matches)
        no_dupl_matches = []
        for match in matches:
            if match not in no_dupl_matches:
                no_dupl_matches.append(match)
        return no_dupl_matches

    def filter_results(self):
        filtered = []
        if self.search_matches['title']:
            filtered = self.filter_helper('title')
        elif self.search_matches['album']:
            filtered = self.filter_helper('album')
        else:
            filtered = self.filter_helper('artist')
        # for track in filtered:
        #     if difflib.get_close_matches(track.title.lower(), [self.search_matches['artist']], cutoff=.6):
        #         return [track]
        return filtered

    def filter_helper(self, primary_type, helper=None):
        filtered = []
        for result in self.search_matches[primary_type]:
            for track in self.tracks:
                if getattr(track, primary_type).lower() == result:
                    if primary_type == 'title' and helper is None:
                        return [track]
                    filtered.append(track)
        random.shuffle(filtered)
        return filtered