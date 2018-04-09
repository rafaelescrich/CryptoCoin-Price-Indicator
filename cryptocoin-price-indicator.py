#!/usr/bin/env python

#	CryptoCoin-Price-Indicator
#--------------------------------------
#	by jj9,
#
# 	generalizes and combines old btc version enhanced by RichHorrocks and Zapsoda (btcapicalls/setupfile maintainance for old btc version)  and ltc version
#
#	if you feel the need to share some bitcoin thanks or love
#	do so here. If you use this please credit it 
#
#   Updated in 2018 by github.com/rafaelescrich
#   Remove some altcoins and make methods more generals in terms of exchanges and cryptocoin

import sys
import gtk
import appindicator
import urllib2
import json
import os

from os.path import expanduser
HOME = expanduser("~")

SETTINGSFILE = os.path.abspath(HOME+"/.local/share/applications/settingsCryptoIndicator.dat")
BAD_RETRIEVE = 0.00001

class CryptoCoinPriceIndicator:
    PING_FREQUENCY = 1 # seconds
    BTCICON = os.path.abspath(HOME+"/.local/share/applications/bitcoinicon.png")
    LTCICON = os.path.abspath(HOME+"/.local/share/applications/litecoinicon.png")

    APPDIR = HOME+"/.local/share/applications/"
    APPNAME = 'CryptoCoin Indicator';VERSION = '0.5'
    BTCMODE = True; BTCInit = False;
    LTCMODE = True; LTCInit = False;

    def __init__(self):
        self.initFromFile()
        self.ind = appindicator.Indicator("new-bitcoin-indicator", self.BTCICON,appindicator.CATEGORY_APPLICATION_STATUS)
        self.ind.set_status(appindicator.STATUS_ACTIVE)
        self.menu_setup()
        self.ind.set_menu(self.menu)

    def main(self):
        self.updateIndicators()
        if self.BTCMODE:
            gtk.timeout_add(self.PING_FREQUENCY * 1000, self.getNewPricesBTC)
        if self.LTCMODE:
            gtk.timeout_add(self.PING_FREQUENCY * 1000, self.getNewPricesLTC)
        gtk.main()

    def updateIndicators(self):
        if self.BTCMODE:
            self.updateBTCIndicator()
        if self.LTCMODE:
            self.updateLTCIndicator()

    def updateBTCIndicator(self):
        self.getNewPricesBTC()
    def updateLTCIndicator(self):
        self.getNewPricesLTC()

    def menu_setup(self):
        self.menu = gtk.Menu()
        self.BTCtickers = None

        self.bitstampBTC = gtk.RadioMenuItem(self.BTCtickers,"BitStamp"); self.bitstampBTC.connect("activate", lambda x: self.toggleBTCdisplay("bitstamp")); self.bitstampBTC.show()
        self.BTCtickers = self.bitstampBTC

        self.bitfinexBTC = gtk.RadioMenuItem(self.BTCtickers,"Bitfinex"); self.bitfinexBTC.connect("activate", lambda x: self.toggleBTCdisplay("bitfinex")); self.bitfinexBTC.show()
        self.BTCtickers = self.bitfinexBTC

        self.defSet = gtk.MenuItem("Choose exchange : "); self.defSet.show()
        self.menu.append(self.defSet)
        self.menu.append(self.bitstampBTC); self.menu.append(self.bitfinexBTC)

        self.setRefreshMenu(self.menu)

        self.getNewPricesBTC()
        
        self.about = gtk.MenuItem("About"); self.about.connect("activate",self.menu_about_response);self.about.show()
        self.menu.append(self.about)
        self.quit_item = gtk.MenuItem("Quit Indicator"); self.quit_item.connect("activate", self.quit); self.quit_item.show()
        self.menu.append(self.quit_item)

    def menu_setupLTC(self):
        self.menuLTC = gtk.Menu()
        self.LTCtickers = None
        self.bitfinexLTC = gtk.RadioMenuItem(self.LTCtickers,"Bitfinex"); self.bitfinexLTC.connect("activate", lambda x: self.toggleLTCdisplay("bitfinex")); self.bitfinexLTC.show()
        self.LTCtickers = self.bitfinexLTC

        defSetLTC = gtk.MenuItem("Choose exchange : "); defSetLTC.show()
        self.menuLTC.append(defSetLTC)
        self.menuLTC.append(self.bitfinexLTC)
        self.setRefreshMenu(self.menuLTC)

        self.getNewPricesLTC()
        
        self.kill_LTC = gtk.MenuItem("LTC Off"); self.kill_LTC.connect("activate", self.noLTC); self.kill_LTC.show(); self.menuLTC.append(self.kill_LTC)
        self.quit_item = gtk.MenuItem("Quit Indicator"); self.quit_item.connect("activate", self.quit); self.quit_item.show()
        self.menuLTC.append(self.quit_item)
        self.LTCInit = True



    def noLTC(self,widget):
        self.indLTC.set_label("")
        self.indLTC.set_icon("")
        self.LTCMODE = False
        self.LTCInit = False

    def setRefreshMenu(self,menuIn):
        refreshmenu = gtk.Menu()
        refMenu =gtk.MenuItem("Set refresh rate :")
        refMenu.set_submenu(refreshmenu)

        self.refreshRates = None
        menuRefresh1 = gtk.RadioMenuItem(self.refreshRates,"3s"); menuRefresh1.connect("activate",lambda x: self.setPing(3)); menuRefresh1.show()
        self.refreshRates = menuRefresh1
        menuRefresh2 = gtk.RadioMenuItem(self.refreshRates,"10s"); menuRefresh2.connect("activate",lambda x: self.setPing(10)); menuRefresh2.show()
        self.refreshRates = menuRefresh2
        menuRefresh3 = gtk.RadioMenuItem(self.refreshRates,"30s"); menuRefresh3.connect("activate",lambda x: self.setPing(30)); menuRefresh3.show()
        self.refreshRates = menuRefresh3
        menuRefresh4 = gtk.RadioMenuItem(self.refreshRates,"1m"); menuRefresh4.connect("activate",lambda x: self.setPing(60)); menuRefresh4.show()
        self.refreshRates = menuRefresh4
        menuRefresh5 = gtk.RadioMenuItem(self.refreshRates,"5m"); menuRefresh5.connect("activate",lambda x: self.setPing(300)); menuRefresh5.show()
        self.refreshRates = menuRefresh5
        menuRefresh6 = gtk.RadioMenuItem(self.refreshRates,"10m"); menuRefresh6.connect("activate",lambda x: self.setPing(600)); menuRefresh6.show()
        self.refreshRates = menuRefresh6;

        refreshmenu.append(menuRefresh1);refreshmenu.append(menuRefresh2);refreshmenu.append(menuRefresh3);
        refreshmenu.append(menuRefresh4);refreshmenu.append(menuRefresh5);refreshmenu.append(menuRefresh6);
        refMenu.show(); refreshmenu.show()
        menuIn.append(refMenu)

    def setPing(self,newTime):
        self.PING_FREQUENCY = newTime

	# toggle function for exchanges
    def toggleBTCdisplay(self, exch):
        self.exchange = exch

	# toggle function for exchanges
    def toggleLTCdisplay(self, exch):
        self.exchangeLTC = exch

	# function that is being called by main which will refresh data	
    def getNewPricesBTC(self):
        updatedRecently = self.update_priceBTC()
        return True
    def getNewPricesLTC(self):
        updatedRecentlyLTC = self.update_priceLTC()
        return True


	# build string to be used by indicator and update the display label
    def update_priceBTC(self):
        dataOut = ""
        priceNow = BAD_RETRIEVE

        priceNow = self.getBitStampBTCPrice()
        if priceNow == BAD_RETRIEVE:
            priceNow = "TempDown"
        else:
            priceNow = str(priceNow)+" USD"
        if "bitstamp" in self.exchange:
            dataOut = dataOut + ' | ' if dataOut != "" else dataOut
            dataOut = dataOut + "Bitstamp: "+priceNow
        self.bitstampBTC.set_label("Bitstamp | "+str(priceNow))

        priceNow = self.getBitfinexBTCPrice()
        if priceNow == BAD_RETRIEVE:
            priceNow = "TempDown"
        else:
            priceNow = str(priceNow)+" USD"
        if "bitfinex" in self.exchange:
            dataOut = dataOut + ' | ' if dataOut != "" else dataOut
            dataOut = dataOut + "Bitfinex: "+priceNow
        self.bitfinexBTC.set_label("Bitfinex | "+str(priceNow))

        self.ind.set_label(dataOut)
        return True

    # build string to be used by indicator and update the display label
    def update_priceLTC(self):
        dataOut = ""
        priceNow = BAD_RETRIEVE

        priceNow = self.getBitfinexUSD("ltc")
        if priceNow == BAD_RETRIEVE:
            priceNow = "TempDown"
        else:
            priceNow = str(priceNow)+" USD"
        if "bitfinex" in self.exchangeLTC:
            dataOut = dataOut + ' | ' if dataOut != "" else dataOut
            dataOut = dataOut + "Bitfinex: "+priceNow
        self.bitfinexLTC.set_label("Bitfinex | "+str(priceNow))
        if self.LTCMODE:
            self.indLTC.set_label(dataOut)
        return True


    def getBitfinexUSD(self,coin):
        lstBitfinex = BAD_RETRIEVE
        try :
            if coin is "ltc":
                web_page = urllib2.urlopen("https://api.bitfinex.com/v1/pubticker/ltcusd").read()
            else:
                web_page = urllib2.urlopen("https://api.bitfinex.com/v1/pubticker/btcusd").read()
            data = json.loads(web_page)
            lstBitfinex = data['last_price']
        except urllib2.HTTPError :
            print("HTTPERROR!")
        except urllib2.URLError :
            print("URLERROR!")
        return "{0:,.2f}".format(float(lstBitfinex))

	# get BitStamp data using json
    def getBitStampBTCPrice(self):
        lstBitStamp = BAD_RETRIEVE
        try :
            web_page = urllib2.urlopen("https://www.bitstamp.net/api/ticker").read()
            data = json.loads(web_page)
            lstBitStamp = data['last']
        except urllib2.HTTPError :
            print("HTTPERROR!")
        except urllib2.URLError :
            print("URLERROR!")
        except ValueError:  # includes simplejson.decoder.JSONDecodeError
            print 'Decoding JSON has failed'
        return "{0:,.2f}".format(float(lstBitStamp))
    
    # get Bitfinex data using json
    def getBitfinexBTCPrice(self):
        lstBitfinex = BAD_RETRIEVE
        try :
            web_page = urllib2.urlopen("https://api.bitfinex.com/v1/pubticker/btcusd").read()
            data = json.loads(web_page)
            lstBitfinex = data['last_price']
        except urllib2.HTTPError :
            print("HTTPERROR!")
        except urllib2.URLError :
            print("URLERROR!")
        except ValueError:  # includes simplejson.decoder.JSONDecodeError
            print 'Decoding JSON has failed'
        return "{0:,.2f}".format(float(lstBitfinex))


    #############################################
    ##########Settings###File####################
    #############################################
	# grab settings from file
    def initFromFile(self):
        try:
            with open(SETTINGSFILE): pass
        except IOError:
            print 'Need to make new file.'
            file = open(SETTINGSFILE, 'w')
            file.write(os.getcwd()+'\n')
            file.write('10 \n')
            file.write('bitfinex \n')
            file.write('True \n')
            file.write('bitstamp \n')
            file.write('True \n')
            file.close()
        f = open(SETTINGSFILE, 'r')
        lines = f.readlines()
        currDir = (lines[0].strip())
        if ".local/share/applicatins" not in currDir:
            self.setAppDir(currDir)
        print "App Directory : "+self.APPDIR
        print "Refresh rate:",int(lines[1]),"seconds"
        self.PING_FREQUENCY = int(lines[1])
        print "BTC Exchange :",(lines[2].strip()),"   Display :",self.str2bool(lines[3].strip())
        self.exchange = (lines[2].strip())
        self.BTCMODE = self.str2bool(lines[3].strip())
        print "LTC Exchange :",(lines[4].strip()),"   Display :",self.str2bool(lines[5].strip())
        self.exchangeLTC = (lines[4].strip())
        self.LTCMODE = self.str2bool(lines[5].strip())
        f.close()

    def setAppDir(self,currDir):
        self.BTCICON = os.path.abspath(currDir+"/res/bitcoinicon.png")
        self.LTCICON = os.path.abspath(currDir+"/res/litecoinicon.png")
        self.APPDIR = currDir

	# utility function for settings file grab
    def str2bool(self,word):
        return word.lower() in ("yes", "true", "t", "1","ok")

    def quit(self, widget, data=None):
        gtk.main_quit()
	# save settings at quit and kill indicator
    def quit(self, widget):
        try:
            print 'Saving Last State.'
            file = open(SETTINGSFILE, 'w')
            file.write(str(self.APPDIR)+'\n')
            file.write(str(self.PING_FREQUENCY)+'\n')
            file.write(str(self.exchange)+'\n')
            file.write(str(self.BTCMODE)+'\n')
            file.write(str(self.exchangeLTC)+'\n')
            file.write(str(self.LTCMODE)+'\n')
            file.close()
        except IOError:
            print " ERROR WRITING QUIT STATE"
        gtk.main_quit()
        sys.exit(0)

    def menu_about_response(self,widget):
        self.menu.set_sensitive(False)
        widget.set_sensitive(False)
        ad=gtk.AboutDialog()
        ad.set_name(self.APPNAME)
        ad.set_version(self.VERSION)
        ad.set_comments("A bitcoin ticker indicator")
        ad.set_license(''+
        'This program is free software: you can redistribute it and/or modify it\n'+
        'under the terms of the GNU General Public License as published by the\n'+
        'Free Software Foundation, either version 2 of the License, or (at your option)\n'+
        'any later version.\n\n'+
        'This program is distributed in the hope that it will be useful, but\n'+
        'WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY\n'+
        'or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for\n'+
        'more details.\n\n'+
        'You should have received a copy of the GNU General Public License along with\n'+
        'this program.  If not, see <http://www.gnu.org/licenses/>.')
        ad.set_website('https://github.com/rafaelescrich/Bitcoin-Price-Indicator')
        ad.set_authors(['Written by jj9 and updated by rafaelescrich'])
        ad.run()
        ad.destroy()
        self.menu.set_sensitive(True)
        widget.set_sensitive(True)

if __name__ == "__main__":
    indicator = CryptoCoinPriceIndicator()
    indicator.main()
