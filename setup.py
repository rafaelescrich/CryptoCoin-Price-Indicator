import os
import shutil
from os.path import expanduser
import os.path as ospath
import subprocess
from subprocess import call
import codecs

HOME = expanduser("~")

USERNAME = ospath.split(HOME)[-1] 
ICON = os.path.abspath(HOME+"/.local/share/applications/bitcoinicon.png")
LTCICON = os.path.abspath(HOME+"/.local/share/applications/litecoinicon.png")
SETTINGSFILE = os.path.abspath(HOME+"/.local/share/applications/settingsCryptoIndicator.dat")
INDICATORFILE = os.path.abspath(HOME+"/.local/share/applications/cryptocoin-price-indicator.py")
AUTODESKTOPFILE = os.path.abspath(HOME+"/.config/autostart/cryptocoin-price-indicator.desktop")
DESKTOPFILE = os.path.abspath(HOME+"/.local/share/applications/cryptocoin-price-indicator.desktop")

removeIn = raw_input("Setup Or Remove (Remove only available if installed in applicationsDir)?: ")
removePack = False

if "emove" in removeIn.lower().strip():
    removePack = True
    print "Removing from system."

if removePack:
    FILES = [ICON,LTCICON, SETTINGSFILE, INDICATORFILE, AUTODESKTOPFILE, DESKTOPFILE]
    for FILE in FILES:
        if os.path.exists(FILE):
            os.remove(FILE)
            print 'Removed:',FILE
    print 'Removed files.'
else:
    dirIn = str(raw_input( "Basic Setup (Input anything other than *advanced* for basic setup):"))
    if os.path.exists(SETTINGSFILE):
        os.remove(SETTINGSFILE)
    if not  'dvanced' in dirIn:
        dirApp = os.getcwd()
        dirIn = dirApp
        subprocess.call(["sudo",  dirIn + "/installDependencies.sh"])
        deskTemp = dirIn+"/cryptocoin-price-indicator.desktop"
        settingsTemp = dirIn+"/res/settingsCryptoIndicator.dat"
        print "Installing dependencies"
        subprocess.call(["sh",  dirIn + "/makeDesktopFile.sh",dirApp])
        subprocess.call(["chown",USERNAME,deskTemp])
        print "Making desktop file, Run to launch ticker."
        INDICATORFILE = os.path.abspath(dirIn+"/cryptocoin-price-indicator.py")
        if not os.path.exists(HOME+"/.local/share/applications/"):
            subprocess.call(["mkdir", HOME+"/.local/share/applications/"])
            print "Making folder:",HOME+"/.local/share/applications/"
    else:
        dirIn = raw_input( "Enter directory of extracted zip file (default is current directory):")

        defaultLoc = raw_input( "Install in user applications dir? (Must type NO for custom location)")
        if "NO" in defaultLoc:
            dirApp = raw_input( "Destination directory with out the ending '/' ?")
            if not os.path.exists(dirApp+"/res/"):
                subprocess.call(["mkdir", dirApp+"/res/"])
                print "Making folder:",dirApp+"/res/"
            ICON = os.path.abspath(dirApp+"/res/bitcoinicon.png")
            LTCICON = os.path.abspath(dirApp+"/res/litecoinicon.png")
            INDICATORFILE = os.path.abspath(dirApp+"/cryptocoin-price-indicator.py")

        else:
            dirApp = HOME+"/.local/share/applications"

        if dirIn == '':
            dirIn = '.'

        if dirIn.endswith('/'):
            dirIn = dirIn[:-1]

        dirIn = os.path.abspath(dirIn)
        print "Setup from:",dirIn

        iconTemp = dirIn+"/res/bitcoinicon.png"
        iconLTCTemp = dirIn+"/res/litecoinicon.png"
        indTemp = dirIn+"/cryptocoin-price-indicator.py"
        deskTemp = dirIn+"/cryptocoin-price-indicator.desktop"
        settingsTemp = dirIn+"/res/settingsCryptoIndicator.dat"

        subprocess.call(["sudo", dirIn + "/installDependencies.sh"])
        print "Installing dependencies"

        subprocess.call(["sh",  dirIn + "/makeDesktopFile.sh"])
        subprocess.call(["chown",USERNAME,deskTemp])
        print "Making desktop file, Run to launch ticker."

        if not os.path.exists(HOME+"/.local/share/applications/"):
            subprocess.call(["mkdir", HOME+"/.local/share/applications/"])
            print "Making folder:",HOME+"/.local/share/applications/"

        #Try moving btc icon
        try:
            shutil.copyfile(iconTemp,ICON)
            print 'Moving btc icon to',ICON
        except IOError:
            print 'Error moving btc icon.'

        #Try moving ltc icon
        try:
            shutil.copyfile(iconLTCTemp,LTCICON)
            print 'Moving ltc icon to',LTCICON
        except IOError:
            print 'Error moving ltc icon.'

        #Try moving indicator
        try:
            shutil.copyfile(indTemp,INDICATORFILE)
            print 'Moving application to',INDICATORFILE
        except IOError:
            print 'Error moving application.'

    #Try moving indicator desktop file
    try:
        shutil.copyfile(deskTemp,DESKTOPFILE)
        print 'Moving application desktop file to',DESKTOPFILE
    except IOError:
        print 'Error moving application desktop file.'

    #Ask to move file to startup
    if 'y' in raw_input("Run on startup? (Y/N): ").lower().strip():
        if not os.path.exists(HOME+"/.config/autostart/"):
            subprocess.call(["mkdir", HOME+"/.config/autostart/"])
            print "Making folder:",HOME+"/.config/autostart/"
        try:
            shutil.copyfile(deskTemp,AUTODESKTOPFILE)
            print 'Moving desktop file to autostart folder.'
        except IOError:
            print 'Error desktop file to autostart folder.'

    
    subprocess.call(["chmod","+x",INDICATORFILE])
    subprocess.call(["chmod","+x",DESKTOPFILE])
    subprocess.call(["chown",USERNAME,DESKTOPFILE])
    print "Script is located at: "+INDICATORFILE

    try:
        print 'Make default settings file :',SETTINGSFILE
        file = open(SETTINGSFILE, 'w')
        file.write(dirApp+' \n')
        file.write('10 \n')
        file.write('bitfinex \n')
        file.write('True \n')
        file.write('bitstamp \n')
        file.write('True \n')
        file.close()
    except IOError:
        print "IO ERROR"


    makeAlias = str(raw_input( "Make indicator alias for terminal (Input anything other than *yes* to skip alias setup):"))
    if "yes" in makeAlias:
        try:
            subprocess.call(["sudo", dirIn + "/setupAlias.sh",INDICATORFILE])
            print "---------------------------------"
            print "Indicator installed close terminal"
            print "To run script type: btc-indicator"
            print "You must open a new terminal first"
        except OSError:
            print 'Error creating script alias'
exit(0)
