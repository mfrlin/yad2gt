import ctypes

def activate_d2_window():
    # TODO: name should probably be configurable
    window_name = 'Diablo II: Resurrected'
    d2_window = ctypes.windll.user32.FindWindowW(None, window_name)
    if d2_window == 0:
        print(f'ERROR: "{window_name}" window not found')
    result = ctypes.windll.user32.SetForegroundWindow(d2_window)
    if result == 0:
        print('ERROR: Failed to activate D2 window')