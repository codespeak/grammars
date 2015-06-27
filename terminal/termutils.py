import time
import os
import tempfile
import subprocess
from pynhost import api
from pynhost.grammars import baseutils

def get_command_results(cmd):
    _, temp_name = tempfile.mkstemp()
    results = api.send_string('{} > {}'.format(cmd, temp_name) + '{enter}')
    time.sleep(.5)
    lines = []
    try:
        with open(temp_name) as f:
            for line in f:
                lines.append(line.strip())
    finally:
        if os.path.isfile(temp_name):
            os.remove(temp_name)
        return lines    

def open_shell():
    clipboard_contents = baseutils.get_clipboard_contents()
    api.send_string("{escape}:let @+ = expand('%:p'){enter}")
    subprocess.call(['x-terminal-emulator'])
    time.sleep(1)
    api.send_string('cd {}'.format(os.path.dirname(baseutils.get_clipboard_contents())) + '{enter}')
    baseutils.set_clipboard_contents(clipboard_contents)
    time.sleep(.2)
