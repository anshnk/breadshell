# IMPORT ALL DEPENDENCIES

# built-in libraries
import os
import time
import datetime
import random
import subprocess
import socket
import re

# the point of this code is to install the modules if the user doesn't already have them installed

# import colorama
try:
    import colorama
except:
    print('colorama not installed, installing now')
    os.system('sudo apt install python3-colorama -y')
    import colorama

# makes sure that bash shell is used
os.environ['SHELL'] = '/bin/bash'

# version number and other information
version = '0.5-pre1d'
versiontype = 2 # 1 = release, 2 = prerelease, 3 = development build

# clear the console
os.system('clear')

# define colors
class c:
    red = colorama.Fore.RED
    yellow = colorama.Fore.YELLOW
    green = colorama.Fore.GREEN
    blue = colorama.Fore.BLUE
    magenta = colorama.Fore.MAGENTA
    cyan = colorama.Fore.CYAN
    white = colorama.Fore.WHITE
    black = colorama.Fore.BLACK
    r = colorama.Fore.RESET # resets color to default

# background colors
class bc:
    red = colorama.Back.RED
    yellow = colorama.Back.YELLOW
    green = colorama.Back.GREEN
    blue = colorama.Back.BLUE
    magenta = colorama.Back.MAGENTA
    cyan = colorama.Back.CYAN
    white = colorama.Back.WHITE
    black = colorama.Back.BLACK
    r = colorama.Back.RESET # resets color to default

# used for networktest utility
def ping_ip(ip_address):
    try:
        pingOutput = subprocess.check_output(['ping', '-c', '1', ip_address]).decode('utf-8')
        
        timeMatch = re.search(r'time=([\d.]+) ms', pingOutput)
        if timeMatch:
            responseTime = float(timeMatch.group(1))
            return responseTime
        else:
            return None
        
    except subprocess.CalledProcessError:
        # Handle if the ping command fails
        return None

# check if breadshell is installed
try:
    currentdir = os.getcwd()
    scriptdir = os.path.dirname(__file__)

    # now time to load settings
    settingsdir = f'/home/{os.getlogin()}/.config/breadshell'
    settingspath = settingsdir+'/settings.ini'
    # read the settings and return all key/value pairs
    def read_settings():
        config = {}
        # create the file if it doesn't already exist
        try:
            with open(settingspath, 'a') as file:
                pass
        except:
            os.mkdir(settingsdir)
            with open(settingspath, 'a') as file:
                pass
        
        with open(settingspath, 'r') as file:
            for line in file:
                # skip empty lines and comment lines
                if line.strip() and not line.startswith('#'):
                    key, value = line.strip().split('=',1)
                    # remove quotes
                    value = value.strip('"').strip("'")
                    config[key] = value
        return config
    
    # overwrite the settings and add new values
    def add_settings(key, value):
        config = read_settings()
        config[key] = value
        # write to the file
        with open(settingspath, 'w') as file:
            for key, value in config.items():
                file.write(f'{key}={value}\n')

    settings = read_settings()

    # if this doesn't work, it will give an error, which is how this works
    os.chdir('/usr/src/breadshell')
    os.chdir(currentdir)
    
    if scriptdir == '/usr/src/breadshell':
        installed = True
        runfrominstall = True

    else:
        print(f'{c.red}you are running breadshell from a file, even though breadshell is installed{c.r}')
        installed = True
        runfrominstall = False

    # change back to the previous directory
    os.chdir(currentdir)

except:
    print(f'{c.red}breadshell is not installed{c.r}')
    installed = False
    runfrominstall = False

# basic functions
    
# returns yellow error
def throwerror(msg='An unknown error has occured'):
    print(f'{c.yellow}{msg}{c.r}')

# returns red error and exits to prevent corruption or something
def fatalerror(msg='A fatal error has occured, exiting immediately'):
    print(f'{c.red}{msg}{c.r}')
    exit()

# game scripts

# utility scripts

def startu_colortester():
    # random colors+chars for 256 characters
    chars = '`1234567890-=~!@#$%^&*()_+qwertyuiop[]\\asdfghjkl;\'zxcvbnm,./QWERTYUIOP{}|ASDFGHJKL:"ZXCVBNM<>?'
    str = ''
    for i in range(4096):
        a = random.randint(0,len(chars)-1)
        char = chars[a]

        # define colors by lists instead of classes
        foregroundColors = [c.red,c.yellow,c.green,c.blue,c.cyan,c.magenta,c.white,c.black,c.r]
        backgroundColors = [bc.red,bc.yellow,bc.green,bc.blue,bc.cyan,bc.magenta,bc.white,bc.black,bc.r]
        # get random item in the lists
        b = foregroundColors[random.randint(0,len(foregroundColors)-1)]
        # used _c here since c is already used for the main colors class
        _c = backgroundColors[random.randint(0,len(foregroundColors)-1)]

        # add it to the main string
        str=str+b+_c+char

    # +c.r+bc.r is needed to reset the colors
    print(str+c.r+bc.r)

def startu_calculator():
    while True:
        # command (meant to be an expression)
        cmd = input(f'{c.cyan}calculator{c.r} > ')
        if cmd == 'exit':
            utillauncher()
        # funny easter egg
        elif cmd == '9+10':
            print(21)
        # as of 0.5-pre1d the user can no longer execute any command in the calculator
        elif cmd.startswith('exec('):
            throwerror()
        else:
            try:
                # print() is needed because simply executing 1+1 does not display 2
                exec(f'print({cmd})')
            except:
                throwerror()

def startu_python():
    while True:
        # command
        cmd = input(f'{c.cyan}python{c.r} > ')

        if cmd == 'exit':
            utillauncher()
        else:
            try:
                exec(cmd)
            except:
                throwerror()

def startu_networktest():
    print(f'network tester v0.1')
    rt = ping_ip('8.8.8.8')
    print(f'{rt}ms')


# game launcher
def games():
    globalversion = '0.2'
    # list amount of games here
    games = ['GAMES COMING SOON']

    print(f'bread games version {globalversion}')
    print(f'please select the game you would like to start ({len(games)} found):')

    i = 1
    for game in games:
        print(f'{c.yellow}{i} - {game}')
        i += 1
    
    print(f'{c.yellow}exit - exit')

    game = input(f'{c.cyan}breadgames{c.r} > ')

    if game == 'exit':
        main()
    if games[int(game)-1] in games:
        print(f'Loading {games[int(game)-1]}...')
        exec(f'startg_{games[int(game)-1]}()')

# utility launcher (totally not just modified game launcher)

def utillauncher():
    globalversion = '0.3'
    # list amount of games here
    utilities = ['colortester','calculator','python','networktest']
    versions = ['1.1','1.0','1.0','0.1']

    print(f'bread utilities version {globalversion}')
    print(f'please select the utility you would like to start ({len(utilities)} found):')

    i = 1
    for utility in utilities:
        print(f'{c.yellow}{i} - {utility} {c.cyan}v{versions[i-1]}{c.r}')
        i += 1

    print(f'{c.yellow}exit - exit')

    utility = input(f'{c.cyan}breadutils{c.r} > ')

    if utility == 'exit':
        main()
    if utilities[int(utility)-1] in utilities:
        print(f'Loading {utilities[int(utility)-1]}...')
        exec(f'startu_{utilities[int(utility)-1]}()')

badStart = False

def reportBadStart(a):
    global badStart
    if not badStart:
        print(f'{c.red}{a}{c.r}')
        print(f'{c.red}username will not be loaded to fix compatibility issues{c.r}')
        badStart = True

# start of program, shown when opening the file
print(f'version {c.cyan}{version}{c.r}, latest login {c.magenta}{datetime.datetime.now()}{c.r}')
print(f'type {c.yellow}bhelp{c.r} for a list of custom commands')
# main loop
def main():
    while True:
        # main input (user@hostname path/to/directory > command typed in)
        try:
            cmd = input(f"{c.blue}{os.getlogin()}@{socket.gethostname()} {c.green}{os.getcwd()}{c.r} > ")
        except Exception as e:
            reportBadStart(e)
            cmd = input(f"{c.blue}user@{socket.gethostname()} {c.green}{os.getcwd()}{c.r} > ")
        # for special commands
            
        # change directory (cd)
        if cmd.startswith('cd'):
            try:
                os.chdir(cmd.split(' ')[1])
            except:
                throwerror('Invalid directory, or a directory was not specified')

        # breadhelp (bhelp)
        elif cmd.startswith('bhelp'):
            print(f'''
    breadshell version {c.cyan}{version}{c.r}

    --- CUSTOM COMMANDS ---

    {c.yellow}bhelp{c.r} - open this page
    {c.yellow}bfetch{c.r} - get system information
    {c.yellow}inst{c.r} {c.cyan}<package-name>{c.r} - easy way to install packages
    {c.yellow}uninst{c.r} {c.cyan}<package-name>{c.r} - easy way to uninstall packages
    {c.yellow}bpkgs{c.r} {c.cyan}<query>{c.r} - search packages
    {c.yellow}bgames{c.r} - start game launcher
    {c.yellow}butils{c.r} - start utility launcher
    {c.yellow}version{c.r} - displays version information
    {c.yellow}settings{c.r} - change your breadshell settings
    {c.red}exit{c.r} - exits breadshell
    ''')
            
        # breadfetch (bfetch)
        elif cmd.startswith('bfetch'):
            print('making this later, for now just have neofetch')
            subprocess.run(['bash','-c','neofetch'])

        # breadinstall (inst)
        elif cmd.startswith('inst'):
            try:
                subprocess.run(['bash','-c',f'sudo apt install {cmd.split(" ")[1]} -y'])
            except:
                throwerror('Invalid package name, or a package was not specfied')

        # breaduninstall (uninst)
        elif cmd.startswith('uninst'):
            try:
                subprocess.run(['bash','-c',f'sudo apt remove {cmd.split(" ")[1]} -y'])
            except:
                throwerror('Invalid package name, or a package was not specfied')

        # breadpackages (bpkgs)
        elif cmd.startswith('bpkgs'):
            try:
                subprocess.run(['bash','-c',f'apt search {cmd.split(" ")[1]}'])
            except:
                throwerror('Invalid package name, or a package was not specfied')

        # exit... self explanatory
        elif cmd.startswith('exit'):
            exit()

        # "developer commands"
            
        # throw a generic error
        elif cmd.startswith('dev-generic-error'):
            throwerror()
            
        # throw a FATAL generic error, which is red...
        elif cmd.startswith('dev-generic-fatalerror'):
            fatalerror()

        # launch games
        elif cmd.startswith('bgames'):
            games()

        # launch utilities
        elif cmd.startswith('butils'):
            utillauncher()

        # display version info
        elif cmd.startswith('version'):
            print(f'breadshell version {c.cyan}{version}{c.r}')

            # display version type
            if versiontype == 1:
                print(f'this is a {c.green}release{c.r} build of breadshell')
            elif versiontype == 2:
                print(f'this is a {c.yellow}prerelease{c.r} build of breadshell')
            elif versiontype == 3:
                print(f'this is a {c.magenta}development{c.r} build of breadshell')
            else:
                print(f'this is an {c.red}unknown{c.r} build of breadshell')

            # display installation status
            if installed == True:
                print(f'breadshell is {c.green}installed{c.r}')
            else:
                print(f'breadshell is {c.red}not installed{c.r}')

            # running from file or not
            if runfrominstall == True:
                print(f'running from {c.green}install{c.r}')
            else:
                print(f'running from {c.red}file{c.r}')

            print(f'made by {c.blue}wheatbread2056{c.r} on github')

        # edit settings
        elif cmd.startswith('settings'):
            print('which setting would you like to change?')

            if settings == {}:
                throwerror(f'No settings were found, or there was an error reading settings.ini ({settingspath})')
                main()
            else:
                for key, value in settings.items():
                    print(f"{key} - {c.cyan}{value}{c.r}")

            while True:
                setting = input(f'{c.cyan}settings{c.r} > ')
                if setting in settings:
                    print('Enter a new value:')
                    newValue = input(f'{c.cyan}{setting}{c.r} > ')
                    if newValue.lower() == 'true':
                        add_settings(setting,True)
                        break
                    elif newValue.lower() == 'false':
                        add_settings(setting,False)
                        break
                    else:
                        add_settings(setting,newValue)
                        break
                elif setting == 'exit':
                    break
                else:
                    throwerror('Invalid setting')


        # if none of the above commands were selected, it will run this (run any command inside the input)
            
        else:
            try:
                subprocess.run(['bash','-c',cmd])
            except:
                fatalerror()
            
# run main function (moved from while loop to function in 0.3 so the user can be returned back to the shell in case anything goes wrong)
main()