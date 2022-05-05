import subprocess

def open_property_window_mac(file_name):
    command = "osascript"
    arg_1 = f"-e set aFile to (POSIX file \"{file_name}\") as alias"
    arg_2 = "-e tell application \"Finder\" to open information window of aFile"
    arg_3 = "-e tell application \"Finder\" to activate"

    args = []
    args.append(command)
    args.append(arg_1)
    args.append(arg_2)
    args.append(arg_3)
    subprocess.run(args)
