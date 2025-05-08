import time
import threading
from pynput.mouse import Button, Controller as MouseController
from pynput.keyboard import Key, Controller as KeyboardController, Listener as KeyboardListener
import sys

# Global settings
settings = {
    'click_type': 'mouse',  # mouse, keyboard, sequence
    'interval': 0.1,
    'mouse_button': 'left',
    'keyboard_key': 'a',
    'sequence': [],  # Each step: {'type': 'mouse'/'keyboard', 'value': ...}
    'hotkey_start': 'f6',
    'hotkey_stop': 'f7',
    'running': False
}

mouse = MouseController()
keyboard = KeyboardController()

# Helper for pretty menus
LINE = '=' * 50

def clear():
    print('\033[2J\033[H', end='')

def main_menu():
    while True:
        clear()
        print(LINE)
        print('           GAME CLICKER - MAIN MENU')
        print(LINE)
        print('1. Start Clicker')
        print('2. Settings')
        print('3. About')
        print('4. Exit')
        print(LINE)
        choice = input('Select an option: ')
        if choice == '1':
            start_clicker_menu()
        elif choice == '2':
            settings_menu()
        elif choice == '3':
            about_menu()
        elif choice == '4':
            sys.exit(0)
        else:
            input('Invalid choice. Press Enter to continue...')

def about_menu():
    clear()
    print(LINE)
    print('Game Clicker v2.0')
    print('By NoahH')
    print('Features:')
    print('- Mouse autoclicking')
    print('- Keyboard key pressing')
    print('- Sequences of mouse and keyboard actions')
    print('- Hotkey start/stop')
    print('- Customizable settings')
    print(LINE)
    input('Press Enter to return to main menu...')

def settings_menu():
    while True:
        clear()
        print(LINE)
        print('                SETTINGS MENU')
        print(LINE)
        print(f'1. Click Type: {settings["click_type"]}')
        print(f'2. Interval: {settings["interval"]} seconds')
        print(f'3. Mouse Button: {settings["mouse_button"]}')
        print(f'4. Keyboard Key: {settings["keyboard_key"]}')
        print(f'5. Sequence: {sequence_str()}')
        print(f'6. Hotkey Start: {settings["hotkey_start"]}')
        print(f'7. Hotkey Stop: {settings["hotkey_stop"]}')
        print('8. Back to Main Menu')
        print(LINE)
        choice = input('Select a setting to change: ')
        if choice == '1':
            click_type_menu()
        elif choice == '2':
            try:
                settings['interval'] = float(input('Enter interval in seconds (e.g., 0.1): '))
            except ValueError:
                input('Invalid number. Press Enter to continue...')
        elif choice == '3':
            settings['mouse_button'] = input('Enter mouse button (left/right/middle): ').lower()
        elif choice == '4':
            settings['keyboard_key'] = input('Enter key to press (e.g., a, space): ')
        elif choice == '5':
            sequence_menu()
        elif choice == '6':
            settings['hotkey_start'] = input('Enter hotkey to start (e.g., f6): ').lower()
        elif choice == '7':
            settings['hotkey_stop'] = input('Enter hotkey to stop (e.g., f7): ').lower()
        elif choice == '8':
            break
        else:
            input('Invalid choice. Press Enter to continue...')

def click_type_menu():
    clear()
    print(LINE)
    print('             CLICK TYPE MENU')
    print(LINE)
    print('1. Mouse Click')
    print('2. Keyboard Key Press')
    print('3. Sequence (mouse and/or keyboard)')
    print(LINE)
    choice = input('Select click type: ')
    if choice == '1':
        settings['click_type'] = 'mouse'
    elif choice == '2':
        settings['click_type'] = 'keyboard'
    elif choice == '3':
        settings['click_type'] = 'sequence'
    else:
        input('Invalid choice. Press Enter to continue...')

def sequence_str():
    if not settings['sequence']:
        return '[empty]'
    return ', '.join([
        f"{step['type']}({step['value']})" for step in settings['sequence']
    ])

def sequence_menu():
    while True:
        clear()
        print(LINE)
        print('           SEQUENCE EDITOR')
        print(LINE)
        print('Current sequence:')
        for i, step in enumerate(settings['sequence']):
            print(f" {i+1}. {step['type']}({step['value']})")
        print(LINE)
        print('1. Add Step')
        print('2. Remove Step')
        print('3. Clear Sequence')
        print('4. Back')
        print(LINE)
        choice = input('Select an option: ')
        if choice == '1':
            t = input('Step type (mouse/keyboard): ').strip().lower()
            if t not in ('mouse', 'keyboard'):
                input('Invalid type. Press Enter to continue...')
                continue
            v = input('Value (mouse: left/right/middle, keyboard: key name): ').strip().lower()
            settings['sequence'].append({'type': t, 'value': v})
        elif choice == '2':
            idx = input('Step number to remove: ')
            try:
                idx = int(idx) - 1
                if 0 <= idx < len(settings['sequence']):
                    settings['sequence'].pop(idx)
                else:
                    input('Invalid index. Press Enter to continue...')
            except ValueError:
                input('Invalid input. Press Enter to continue...')
        elif choice == '3':
            settings['sequence'] = []
        elif choice == '4':
            break
        else:
            input('Invalid choice. Press Enter to continue...')

def start_clicker_menu():
    clear()
    print(LINE)
    print('         READY TO START CLICKER')
    print(LINE)
    print(f"Type: {settings['click_type']}")
    print(f"Interval: {settings['interval']}s")
    if settings['click_type'] == 'mouse':
        print(f"Mouse Button: {settings['mouse_button']}")
    elif settings['click_type'] == 'keyboard':
        print(f"Keyboard Key: {settings['keyboard_key']}")
    elif settings['click_type'] == 'sequence':
        print(f"Sequence: {sequence_str()}")
    print(f"Start Hotkey: {settings['hotkey_start'].upper()}")
    print(f"Stop Hotkey: {settings['hotkey_stop'].upper()}")
    print(LINE)
    input('Press Enter and use the hotkey to start...')
    run_clicker_with_hotkeys()

def run_clicker_with_hotkeys():
    settings['running'] = False
    stop_listener = threading.Event()
    def on_press(key):
        try:
            k = key.char.lower() if hasattr(key, 'char') and key.char else str(key).replace('Key.', '').lower()
        except:
            k = str(key).replace('Key.', '').lower()
        if k == settings['hotkey_start']:
            if not settings['running']:
                print('Clicker started! (Press stop hotkey to end, or ESC to exit to menu)')
                settings['running'] = True
                threading.Thread(target=clicker_thread, args=(stop_listener,), daemon=True).start()
        elif k == settings['hotkey_stop']:
            if settings['running']:
                print('Clicker stopped!')
                settings['running'] = False
        elif k == 'esc':
            print('Exiting clicker loop...')
            settings['running'] = False
            stop_listener.set()
            return False  # Stop listener
    with KeyboardListener(on_press=on_press) as listener:
        print(f"Waiting for hotkey ({settings['hotkey_start'].upper()})...")
        listener.join()

def clicker_thread(stop_event):
    while settings['running'] and not stop_event.is_set():
        if settings['click_type'] == 'mouse':
            btn = getattr(Button, settings['mouse_button'], Button.left)
            mouse.click(btn)
        elif settings['click_type'] == 'keyboard':
            key = settings['keyboard_key']
            send_keyboard(key)
        elif settings['click_type'] == 'sequence':
            for step in settings['sequence']:
                if not settings['running'] or stop_event.is_set():
                    break
                if step['type'] == 'mouse':
                    btn = getattr(Button, step['value'], Button.left)
                    mouse.click(btn)
                elif step['type'] == 'keyboard':
                    send_keyboard(step['value'])
                time.sleep(settings['interval'])
        time.sleep(settings['interval'])

def send_keyboard(key):
    if len(key) == 1:
        keyboard.press(key)
        keyboard.release(key)
    else:
        k = getattr(Key, key, None)
        if k:
            keyboard.press(k)
            keyboard.release(k)

def main():
    try:
        main_menu()
    except KeyboardInterrupt:
        print('\nExiting...')
        sys.exit(0)

if __name__ == '__main__':
    main() 