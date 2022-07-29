import subprocess

def open_terminal_window_win(path):
    subprocess.Popen(f'cmd.exe /k "cd /d {path}"', creationflags=subprocess.CREATE_NEW_CONSOLE)