import subprocess
import os
import re
from pynhost import api, dynamic, utilities
from pynhost.grammars.vimtastic import vimutils, vimextension
from pynhost.grammars import baseutils

class VimGitGrammar(vimextension.VimExtensionGrammar):
    def __init__(self):
        super().__init__()
        self.mapping = {
        '<hom_git> <hom_remote>': self.git_remote,
        '<hom_git> <hom_update>': self.git_update,
        }

    def git_remote(self, words):
        filepath = vimutils.get_clipboard_contents('{F11}{space}1a')
        up_dir = os.path.split(filepath)[:-1][0]
        while up_dir:
            try:
                with open(os.path.join(up_dir, '.git', 'config')) as f:
                    for line in f:
                        split_line = line.split()
                        if split_line[0] == 'url':
                            url = re.sub(r'[a-z]+@', '', split_line[-1])
                            baseutils.open_firefox_url(url)
                            return
            except FileNotFoundError:
                pass
            up_dir = os.path.split(up_dir[:-1])[0]

    def git_update(self, words):
        commit_message = vimutils.get_clipboard_contents('{esc}dd').strip()
        filepath = vimutils.get_clipboard_contents('{esc}' +
            vimutils.FUNCTIONS['FilenameToClipboard'] + 'a')
        containing_dir = os.path.split(filepath)[:-1][0]
        os.chdir(containing_dir)
        subprocess.call(['git', 'add', '--all', ':/'])
        subprocess.call(['git', 'commit', '-m', "{}".format(commit_message)])
        subprocess.call(['git', 'push'])
        print('Git repo updated!')