#!/usr/bin/python

# TODO
# - make this work without ANY dependencies
# - same thing for colors
# X remove bloat!
# - make small
# - make it actally good

from random import randint
import os, subprocess, time, datetime, socket
# import random <-- commenting this is going to break some things but core functionality will still work
# Replacement for getpass module (literally stolen code)
def getuser():
    for name in ('LOGNAME', 'USER', 'LNAME', 'USERNAME'):
        user = os.environ.get(name)
        if user:
            return user
    try:
        import pwd
        return pwd.getpwuid(os.getuid())[0]
    except (ImportError, KeyError) as e:
        raise OSError('No username set in the environment') from e
DEFAULT_SETTINGS = True
LEGACY_PROMPT = True # just uses prompt() which was used in every version before 1.0
# version number and other information --version
version = '1.0-dev5c'
bshversion = '0.2'
devnote = 'twice as good as breadshell!'
# define colors --customization
# foreground colors
class c:
    red = '\033[31m'
    yellow = '\033[33m'
    green = '\033[32m'
    blue = '\033[34m'
    magenta = '\033[35m'
    cyan = '\033[36m'
    white = '\033[37m'
    black = '\033[30m'
    b = '\033[1m' # bold
    i = '\033[3m' # italic
    u = '\033[4m' # underline
    e = '\033[0m' # end
    r = '\033[39m' # resets color to default
# background colors
class bc:
    red = '\033[41m'
    yellow = '\033[43m'
    green = '\033[42m'
    blue = '\033[44m'
    magenta = '\033[45m'
    cyan = '\033[46m'
    white = '\033[47m'
    black = '\033[40m'
    r = '\033[49m' # resets color to default
user = getuser()
    
# now time to load settings --settings
try:
    settingsdir = f'/home/{user}/.config/breadshell'
except:
    settingsdir = '/home/user/.config/breadshell'
settingspath = settingsdir+'/settings.ini'
# read the settings and return all key/value pairs
def read_settings():
    global DEFAULT_SETTINGS
    config = {}
    # create the file if it doesn't already exist
    try:
        with open(settingspath, 'a') as file:
            file.close()
    except:
        try:
            os.mkdir(settingsdir)
        except:
            DEFAULT_SETTINGS = True
        try:
            with open(settingspath, 'a') as file:
                file.close()
        except:
            DEFAULT_SETTINGS = True
    if DEFAULT_SETTINGS == False:
        with open(settingspath, 'r') as file:
            for line in file:
                # skip empty lines and comment lines
                if line.strip() and not line.startswith('#'):
                    key, value = line.strip().split('=',1)
                    # remove quotes
                    value = value.strip('"').strip("'")
                    config[key] = value
            file.close()
        return config

if DEFAULT_SETTINGS == False:
    settings = read_settings()

# overwrite the settings and add new values
def add_settings(key, value):
    if value == True or value == False:
        settings[key] = str(value)
    else:
        settings[key] = value
    # write to the file
    if DEFAULT_SETTINGS == False:
        with open(settingspath, 'w') as file:
            for key, value in settings.items():
                file.write(f'{key}={value}\n')
            file.close()

# remove a setting (broken idk why)
def remove_settings(key1):
    # write to the file
    if DEFAULT_SETTINGS == False:
        with open(settingspath, 'w') as file:
            for key, value in settings.items():
                if not key1 == key:
                    file.write(f'{key}={value}\n')
            file.close()

# generate default settings
# changed in bshv2 to have MY defaults because they are simply better
defaultSettings = {
    'loginColor': 'red',
    'dirColor': 'white',
    'textColor': 'r',
    'pointerColor': 'r',
    'pointerChar': '$:',
    'showLogin': 'True',
    'showDir': 'True',
    'showPointer': 'True',
    'showHost': 'False',
    'clearOnBoot': 'False',
    'shortenDir': 'True',
}
temp1494861 = 0 # what is this for? i have no idea
# checks for settings (kinda sucks but it works)
if DEFAULT_SETTINGS == False:
    for setting in defaultSettings:
        try:
            temp1494861 = settings[setting]
        except:
            add_settings(setting,defaultSettings[setting])
else:
    settings = defaultSettings.copy()

# settings friendly names
friendlySettings = {
    'loginColor': 'Username Color',
    'dirColor': 'Directory Color',
    'textColor': 'Text Color',
    'pointerColor': 'Pointer Color',
    'pointerChar': 'Pointer Character',
    'showLogin': 'Show Current User',
    'showDir': 'Show Current Directory',
    'showPointer': 'Show Pointer',
    'showHost': 'Show Hostname',
    'clearOnBoot': 'Clear On Boot',
    'shortenDir': 'Shorten User Directory',
}
types = {
    'color': ['default', 'red', 'yellow', 'green', 'cyan', 'blue', 'magenta', 'white', 'black', 'r'],
    'texteffect': ['none', 'bold', 'italic', 'underline'],
    'bool': ['true', 'false', 't', 'f'],
    'str': 'any',
    'num': 'any',
}
settingtypes = {
    'loginColor': 'color',
    'dirColor': 'color',
    'textColor': 'color',
    'pointerColor': 'color',
    'pointerChar': 'str',
    'showLogin': 'bool',
    'showDir': 'bool',
    'showPointer': 'bool',
    'showHost': 'bool',
    'clearOnBoot': 'bool',
    'shortenDir': 'bool',
    'dirType': 'num', # add this later
}
boolTranslation = {
    'true': True,
    'false': False,
    't': True,
    'f': False
}
# clear console
if settings['clearOnBoot'] == 'True':
    os.system('clear')
# basic functions
# returns yellow error
def throwerror(msg='An unknown error has occured'):
    print(f'{c.yellow}{msg}{c.r}')

if DEFAULT_SETTINGS == True:
    throwerror(f'{settingspath.replace(f"/home/{user}", "~")} couldn\'t be generated, default settings will be used. Settings will not save.')

if LEGACY_PROMPT == True:
    throwerror('Legacy fallback prompt is enabled. Command history will not work and functionality will be limited.')

# start of program, shown when opening the file

def color(col):
    global c
    return c.__getattribute__(c, col)

print(f'{c.magenta}[bshv2] {c.red}settings were force-disabled along with the command history{c.r}')
print(f'breadshellv2 {c.cyan}{bshversion}{c.r}, latest login {c.magenta}{datetime.datetime.now()}{c.r}')
print(f'type {c.yellow}bhelp{c.r} for a list of custom commands.')
# main loop
def main():
    global cmdhistory
    while True:
        # generate the prompt
        tempcmd = ""
        if settings['showLogin'] == 'True':
            try:
                tempcmd += f"{color(settings['loginColor'])}{c.b}{user}{c.e}@{socket.gethostname()}{c.r} "
                if not settings['showHost'] == 'True':
                    tempcmd = tempcmd.split('@')[0]+f'{c.r} '
            except Exception as e:
                throwerror(e)
                tempcmd += f"{color(settings['loginColor'])}{c.b}{user}{c.e}@{socket.gethostname()}{c.r} "
                if not settings['showHost'] == 'True':
                    tempcmd = tempcmd.split('@')[0]+f'{c.r} '

        if settings['showDir'] == 'True':
            if settings['shortenDir'] == 'True':
                tempcmd += f"{color(settings['dirColor'])}{os.getcwd()}{c.r} ".replace(f'/home/{user}', '~')
            else:
                tempcmd += f"{color(settings['dirColor'])}{os.getcwd()}{c.r} "

        if settings['showPointer'] == 'True':
            tempcmd += f"{color(settings['pointerColor'])}{settings['pointerChar']} {c.r}"

        tempcmd += color(settings['textColor'])

        cmd = input(tempcmd)
        cmdargs = cmd.split(' ')

        # new prompt with command history removed because its too much bloat! i hope you can understand,.
        
        print(c.r + c.e,end='') # attempt to stop command output from using the set text color

        # for special commands
            
        # change directory (cd)
        if cmdargs[0] == ('cd'):
            try:
                os.chdir(cmd.split(' ')[1])
            except:
                throwerror('Invalid directory, or a directory was not specified')
        # breadhelp (bhelp)
        elif cmdargs[0] == ('bhelp'):
            print(f'''---
{c.yellow}bhelp{c.r} - list built-in breadshell commands
{c.yellow}version{c.r} - displays version information
{c.yellow}settings{c.r} - change your breadshell settings
{c.red}exit{c.r} - exits breadshell

unlisted commands: {c.cyan}dev-generic-error{c.r}, {c.cyan}dev-exec{c.r}
---''')
        # exit... self explanatory
        elif cmdargs[0] == ('exit'):
            exit()
        # "developer commands"
        # throw a generic error
        elif cmdargs[0] == ('dev-generic-error'):
            throwerror()
        # actually useful, directly execute code from breadshell.py
        # able to execute multiple commands at a time without semicolon seperators
        elif cmdargs[0] == ('dev-exec'):
            try:
                exec(' '.join(cmdargs[1:]))
            except Exception as e:
                throwerror('(Python) '+str(e))
        elif cmdargs[0] == ('dev-text-effects-demo'):
            print(f'''
{c.b}this text should be bold{c.e} and this text is normal
{c.i}this should be italic{c.e}
{c.u}this should be underlined{c.e}
''')
        # display version info
        elif cmdargs[0] == ('version'):
            print(f'breadshellv2 {c.cyan}{bshversion}{c.r}')                
            print(f'based on breadshell {c.red}{version}{c.r}')

            if not devnote == """""" and not devnote == '' and not devnote == None:
                print(devnote)
        # edit settings --editsettings
        elif cmdargs[0] == ('settings'):
            if settings == {}:
                throwerror(f'No settings were found, or there was an error reading settings.ini ({settingspath})')
                main()
            else:
                tm0 = 0
                reflist = []
                for key, value in settings.items():
                    if not key.startswith('h_') and not key.startswith('s_'):
                        if key in friendlySettings:
                            if settings[key] == 'False':
                                print(f"({c.yellow}{tm0}{c.r}) {friendlySettings[key]} - {c.red}{value}{c.r}")
                            elif settings[key] == 'True':
                                print(f"({c.yellow}{tm0}{c.r}) {friendlySettings[key]} - {c.green}{value}{c.r}")
                            else:
                                print(f"({c.yellow}{tm0}{c.r}) {friendlySettings[key]} - {c.cyan}{value}{c.r}")

                        else:
                            print(f"({c.yellow}{tm0}{c.r}) {c.yellow}{key}{c.r} - {c.cyan}{value}{c.r}") # if there is no friendly name for the setting
                        reflist.append(key)
                        tm0 += 1
            print('Type the number of the setting you would like to change, or list to list settings, or exit to leave')
            while True:
                setting = input(f'{c.cyan}settings{c.r} {settings["pointerChar"]} ')
                completed = False
                # new (1.0+) settings, number-based selection
                # legacy settings removed because i am NOT updating the code twice whenever i need to change this
                try:
                    if int(setting) < len(reflist) and int(setting) > -1:
                        print('Enter a new value:')
                        newValue = input(f'{c.green}{friendlySettings[reflist[int(setting)]]}{c.r} {settings["pointerChar"]} ')
                        if settingtypes[reflist[int(setting)]] == 'bool':
                            if newValue.lower() in boolTranslation:
                                try:
                                    add_settings(reflist[int(setting)],boolTranslation[newValue.lower()])
                                    print(f'Successfully updated the setting {c.green}{friendlySettings[reflist[int(setting)]]}{c.r}.')
                                except:
                                    throwerror(f'Failed to update the setting {c.green}{friendlySettings[reflist[int(setting)]]}{c.r}')
                            else:
                                throwerror(f'Invalid value, type \'{settingtypes[reflist[int(setting)]]}\' only allows values {types["bool"]}')
                        elif newValue.lower() == 'exit':
                            pass
                        else:
                            if not types[settingtypes[reflist[int(setting)]]] == 'any' and not types[settingtypes[reflist[int(setting)]]] == None:
                                if newValue.lower() in types[settingtypes[reflist[int(setting)]]]:
                                    try:
                                        if settingtypes[reflist[int(setting)]] == 'color':
                                            if newValue.lower() == 'default':
                                                add_settings(reflist[int(setting)],'r')
                                            else:
                                                add_settings(reflist[int(setting)], newValue.lower())
                                        elif settingtypes[reflist[int(setting)]] == 'texteffect':
                                            if newValue.lower() == 'none':
                                                add_settings(reflist[int(setting)],'e')
                                            elif newValue.lower() == 'bold':
                                                add_settings(reflist[int(setting)],'b')
                                            elif newValue.lower() == 'italic':
                                                add_settings(reflist[int(setting)],'i')
                                            elif newValue.lower() == 'underline':
                                                add_settings(reflist[int(setting)],'u')              
                                        else:
                                            add_settings(reflist[int(setting)], newValue)

                                        print(f'Successfully updated the setting {c.green}{friendlySettings[reflist[int(setting)]]}{c.r}.')
                                    except:
                                        throwerror(f'Failed to update the setting {c.green}{friendlySettings[reflist[int(setting)]]}{c.r}')
                                else:
                                    throwerror(f'Invalid value, type \'{settingtypes[reflist[int(setting)]]}\' only allows values {types[settingtypes[reflist[int(setting)]]]}')
                            else:
                                try:
                                    add_settings(reflist[int(setting)], newValue)
                                    print(f'Successfully updated the setting {c.green}{friendlySettings[reflist[int(setting)]]}{c.r}.')
                                except:
                                    throwerror(f'Failed to update the setting {c.green}{friendlySettings[reflist[int(setting)]]}{c.r}')
                        completed = True
                except:
                    pass
                if setting.lower() == 'list':
                    tm0 = 0
                    reflist = []
                    for key, value in settings.items():
                        if not key.startswith('h_') and not key.startswith('s_'):
                            if key in friendlySettings:
                                if settings[key] == 'False':
                                    print(f"({c.yellow}{tm0}{c.r}) {friendlySettings[key]} - {c.red}{value}{c.r}")
                                elif settings[key] == 'True':
                                    print(f"({c.yellow}{tm0}{c.r}) {friendlySettings[key]} - {c.green}{value}{c.r}")
                                else:
                                    print(f"({c.yellow}{tm0}{c.r}) {friendlySettings[key]} - {c.cyan}{value}{c.r}")

                            else:
                                print(f"({c.yellow}{tm0}{c.r}) {c.yellow}{key}{c.r} - {c.cyan}{value}{c.r}") # if there is no friendly name for the setting
                            reflist.append(key)
                            tm0 += 1

                elif setting.lower() == 'dev-list':
                    tm0 = 0
                    reflist = []
                    for key, value in settings.items():
                        if not key.startswith('h_') and not key.startswith('s_'):
                            if key in friendlySettings:
                                if key in settingtypes:
                                    if settings[key] == 'False' and settingtypes[key] == 'bool':
                                        print(f"({c.yellow}{tm0}{c.r}) {friendlySettings[key]} [{key}] - {c.red}{value}{c.r} [{c.yellow}bool{c.r}]")
                                    elif settings[key] == 'True' and settingtypes[key] == 'bool':
                                        print(f"({c.yellow}{tm0}{c.r}) {friendlySettings[key]} [{key}] - {c.green}{value}{c.r} [{c.yellow}bool{c.r}]")
                                    else:
                                        print(f"({c.yellow}{tm0}{c.r}) {friendlySettings[key]} [{key}] - {c.cyan}{value}{c.r} [{c.yellow}{settingtypes[key]}{c.r}]")
                                else:
                                    print(f"({c.yellow}{tm0}{c.r}) {friendlySettings[key]} [{key}] - {c.cyan}{value}{c.r}")
                            else:
                                if key in settingtypes:
                                    print(f"({c.yellow}{tm0}{c.r}) {key} - {c.cyan}{value}{c.r} [{c.yellow}{settingtypes[key]}{c.r}]")
                                else:
                                    print(f"({c.yellow}{tm0}{c.r}) {key} - {c.cyan}{value}{c.r}")
                            reflist.append(key)
                            tm0 += 1
                        else:
                            if key in friendlySettings:
                                if key in settingtypes:
                                    if settings[key] == 'False' and settingtypes[key] == 'bool':
                                        print(f"({c.red}X{c.r}) {friendlySettings[key]} [{c.red}{key}{c.r}] - {c.red}{value}{c.r} [{c.yellow}bool{c.r}]")
                                    elif settings[key] == 'True' and settingtypes[key] == 'bool':
                                        print(f"({c.red}X{c.r}) {friendlySettings[key]} [{c.red}{key}{c.r}] - {c.green}{value}{c.r} [{c.yellow}bool{c.r}]")
                                    else:
                                        print(f"({c.red}X{c.r}) {friendlySettings[key]} [{c.red}{key}{c.r}] - {c.cyan}{value}{c.r} [{c.yellow}{settingtypes[key]}{c.r}]")
                                else:
                                    print(f"({c.red}X{c.r}) {friendlySettings[key]} [{c.red}{key}{c.r}] - {c.cyan}{value}{c.r}")
                            else:
                                if key in settingtypes:
                                    print(f"({c.red}X{c.r}) {c.red}{key}{c.r} - {c.cyan}{value}{c.r} [{c.yellow}{settingtypes[key]}{c.r}]")
                                else:
                                    print(f"({c.red}X{c.r}) {c.red}{key}{c.r} - {c.cyan}{value}{c.r}")

                elif setting.lower() == 'exit':
                    break

                elif completed == True: # variable added to stop throwing errors when nothing went wrong
                    pass

                else:
                    throwerror('Invalid setting')
            
        else:
            try:
                subprocess.run(['bash','-c',cmd])
            except Exception as e:
                throwerror('An error has occured: '+str(e))
            
# run main function (moved from while loop to function in 0.3 so the user can be returned back to the shell in case anything goes wrong)
main()