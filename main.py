from ast import literal_eval
import webbrowser

import price_differences
import order_update
import settings
import sso_utils

VERSION = '0.1'


def print_intro():
    print(f'    EVE Online Market Trading Helper')
    print(f'    Version {VERSION}')
    print()


def get_command(inputs):
    current_user = sso_utils.get_character(sso_session)
    print(f'SSO Status: {f"Logged in as {current_user}" if current_user else "Not logged in"}')

    print('Main Menu:')
    for num, (title, func) in inputs.items():
        print(f'  [{num}]  {title}')

    while True:
        res = input(' > ')
        try:
            res = int(res)
            return inputs[res]
        except ValueError:
            print('Please input an integer.')
        except KeyError:
            print('Input command not found.')


def start_regional():
    url = price_differences.price_differences(settings.settings)
    webbrowser.open(url)


def start_update():
    if not sso_session:
        print('SSO login is required for this feature!')
        return

    print('Starting order update tool...')

    order_update.update_all(settings.settings, sso_session)


def start_sso():
    global sso_session
    sso_session = sso_utils.oauth_session()


def start_statistics():
    print('Not yet implemented!')


def start_settings():

    def _update_settings(inputs):
        while True:
            # Get a valid key
            key = input('[Key] > ')
            if not key:
                return False
            if key not in inputs:
                print('Input key not found.')
                continue

            # Get the type of our valid key
            T = type(inputs[key])

            # Get a valid value
            value = input('Value > ')

            if T != str:
                try:
                    value = literal_eval(value)
                    if type(value) != T:
                        raise ValueError(f'Input type {type(value).__name__} does not match setting type {T.__name__}')
                except (ValueError, SyntaxError):
                    print(f'Invalid input for literal of type {T.__name__}')
                    continue

            inputs[key] = value
            return True

    editing = True
    while editing:
        print('Editing settings:')
        for key, value in settings.settings.items():
            print(f'  [{key}] = {value}: {type(value).__name__}')
        editing = _update_settings(settings.settings)
        print()


"""
    save = input('Save settings to file? [Y/n] > ')
    if save != 'n':
        settings.save_to_file(settings.settings)
        print('Settings saved to settings.yaml!')
"""

menu_choices = {
    1: ('Regional Trading Calculator', start_regional),
    2: ('Fast Order Update', start_update),
    7: ('Sign-in with SSO', start_sso),
    8: ('Statistics', start_statistics),
    9: ('Settings', start_settings),
    0: ('Quit', exit),
}

if __name__ == '__main__':
    print_intro()
    sso_session = None
    while res := get_command(menu_choices):
        title, function = res

        print(f'{title+" ":─<83}')
        print()

        function()

        print()
        print('─' * 83)
