import subprocess
from prettytable import PrettyTable
import enum
import platform
import os


class OperatingSystem(enum.Enum):
    WINDOWS = 'windows'
    LINUX = 'linux'
    MAC = 'mac'


def get_wifi_passwords(os=OperatingSystem.WINDOWS):
    method_to_call = {OperatingSystem.WINDOWS: (get_windows_wifi_passwords, 'Windows'),
                      OperatingSystem.LINUX: (get_linux_wifi_passwords, 'Linux'),
                      OperatingSystem.MAC: (get_mac_wifi_passwords, 'Darwin')
                      }

    if not isinstance(os, OperatingSystem):
        raise TypeError('{} is not of type OperatingSystem'.format(os))

    method_name, platform_name = method_to_call[os]

    if platform.system() != platform_name:
        raise Exception('This is a {} Platform not {} OS as specified by you..'.format(platform.system(), os))

    return method_name()


def get_linux_wifi_passwords():
    print('*' * 50)
    print('\tLINUX WiFi PASSWORD GETTER')
    print('*' * 50)
    wifi_passwords_table = PrettyTable(['SSID Name', 'Password'])
    wifi_names = [name for name in os.listdir('/etc/NetworkManager/system-connections/') if not name.startswith('.')]
    for SSID in wifi_names:
        data = subprocess.getoutput('sudo cat /etc/NetworkManager/system-connections/"{}" | grep psk=' \
                                    .format(SSID))
        if data:
            password = data.split('=')[1].strip()
            wifi_passwords_table.add_row([SSID, password])
    return wifi_passwords_table


def get_mac_wifi_passwords():
    print('*' * 50)
    print('\tMAC WiFi PASSWORD GETTER')
    print('*' * 50)
    wifi_passwords_table = PrettyTable(['SSID Name', 'Password'])
    wifi_names = subprocess.getoutput('networksetup -listpreferredwirelessnetworks en0').split('\n')

    for SSID in wifi_names:
        data = subprocess.getoutput('security find-generic-password -wa "{}"' \
                                    .format(SSID))
        print('Getting password for {} .......'.format(SSID))
        if not 'could not be found' in data:
            password = data.split(':')[1].strip()
            wifi_passwords_table.add_row([SSID, password])
    return wifi_passwords_table


def get_windows_wifi_passwords():
    print('*' * 50)
    print('\tWINDOWS WiFi PASSWORD GETTER')
    print('*' * 50)
    wifi_passwords_table = PrettyTable(['SSID Name', 'Password'])
    wifi_names = [name.split(':')[1].strip() for name in
                  subprocess.getoutput("netsh wlan show profiles | findstr All").split('\n')]
    for SSID in wifi_names:
        data = subprocess.getoutput('netsh wlan show profile "{}" key=clear | findstr "Key" | findstr "Content" ' \
                                    .format(SSID))
        print('Getting password for {} .......'.format(SSID))
        if data:
            password = data.split(':')[1].strip()
            wifi_passwords_table.add_row([SSID, password])
    return wifi_passwords_table


if __name__ == '__main__':
    print(get_wifi_passwords(os=OperatingSystem.WINDOWS))
