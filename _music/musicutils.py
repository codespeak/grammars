import os
import subprocess
import difflib
from pynhost.grammars._music import obj

def load_track_info(music_dir):
    tracks = []
    for filename in os.listdir(music_dir):
        track_info = {
            'full path': os.path.join(music_dir, filename.replace('"', r'\"')),
            'artist': None,
            'album': None,
            }
        full_path = os.path.join(music_dir, filename.replace('"', r'\"'))
        track = obj.Track(full_path)
        raw_metadata = subprocess.check_output(['id3tool',
            '{}'.format(full_path)], stderr=open(os.devnull, 'wb'))
        metadata = raw_metadata.decode('utf8', 'ignore').split('\n')
        for piece in metadata:
            try:
                data, value = piece.split(':', 1)
                value = value.strip()
                if data == 'Song Title':
                    track.title = value
                elif data == 'Artist':
                    track.artist = value
                elif data == 'Album':
                    track.album = value
            except ValueError:
                pass
        tracks.append(track)
    return tracks


def search_tracks(search_info, tracks):
    tracks = []
    track_matches, album_matches, artist_matches = [], [], []
    if search_info['title']:
        track_matches = search_subject(search_info['title'], [track.lower() for track in tracks])
    if search_info['album']:
        album_matches = search_subject(search_info['album'], [track['album'].lower() for track in tracks])
    if search_info['artist']:
        artist_matches = search_subject(search_info['artist'], [track['artist'].lower() for track in tracks])
    if track_matches and artist_matches: 
        pass

    print(track_matches, album_matches, artist_matches)

def filter_matches(track_matches, album_matches, artist_matches):
   pass 
