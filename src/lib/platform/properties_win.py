from ctypes import Structure, c_ulong, c_char_p, c_int, c_void_p, sizeof, byref, windll
from ctypes.wintypes import BOOL, DWORD, HANDLE, HINSTANCE, HKEY

SEE_MASK_NOCLOSEPROCESS = 0x00000040
SEE_MASK_INVOKEIDLIST = 0x0000000C

class SHELLEXECUTEINFO(Structure):
    _fields_ = (
        ("cbSize",DWORD),
        ("fMask", c_ulong),
        ("hwnd", HANDLE),
        ("lpVerb", c_char_p),
        ("lpFile", c_char_p),
        ("lpParameters", c_char_p),
        ("lpDirectory", c_char_p),
        ("nShow", c_int),
        ("hInstApp", HINSTANCE),
        ("lpIDList", c_void_p),
        ("lpClass", c_char_p),
        ("hKeyClass", HKEY),
        ("dwHotKey", DWORD),
        ("hIconOrMonitor", HANDLE),
        ("hProcess", HANDLE),
    )

ShellExecuteEx = windll.shell32.ShellExecuteEx
ShellExecuteEx.restype = BOOL

def open_property_window_win(file_name):
    sei = SHELLEXECUTEINFO()
    sei.cbSize = sizeof(sei)
    sei.fMask = SEE_MASK_NOCLOSEPROCESS | SEE_MASK_INVOKEIDLIST
    sei.lpVerb = b"properties"
    sei.lpFile = bytes(file_name, encoding='utf8')
    sei.nShow = 1
    ShellExecuteEx(byref(sei))
