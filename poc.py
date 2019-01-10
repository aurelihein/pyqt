#!/usr/bin/python3
#aurelien BOUIN

#interesting : https://www.youtube.com/watch?v=D5nsMh2zmXk
#another interesting app (1252 lines) : https://github.com/alandmoore/wcgbrowser/blob/master/browser.py
#https://github.com/mfitzp/15-minute-apps

#sudo apt-get install python3-pyqt5.qtwebkit python3-pyqt5.qtwebengine
#python3 test.py

import argparse
import os.path

import sys
from PyQt5 import QtCore, QtGui, QtWidgets, QtNetwork
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebKit import *
from PyQt5.QtWebKitWidgets import *
from PyQt5.QtWidgets import QApplication, QWidget, QMainWindow
from PyQt5.QtNetwork import QNetworkRequest, QNetworkAccessManager,QNetworkProxy

URL="https://pythonspot.com/creating-a-webbrowser-with-python-and-pyqt-tutorial/"
FLAGS = None


class Browser(QWebView):
    def __init__(self):
        # QWebView
        self.view = QWebView.__init__(self)
        self.settings().setAttribute(QWebSettings.DeveloperExtrasEnabled, True)
        #localStorage
        self.settings().setAttribute(QWebSettings.LocalStorageEnabled, True)
        #settings->setLocalStoragePath("/tmp")
        #self.view.setPage(MyBrowser())
        self.setWindowTitle('Loading...')
        self.titleChanged.connect(self.adjustTitle)
        #super(Browser).connect(self.ui.webView,QtCore.SIGNAL("titleChanged (const QString&amp;)"), self.adjustTitle)
        #Will ignore ssl handshake
        self.myNetworkManager = QtNetwork.QNetworkAccessManager()
        self.myNetworkManager.sslErrors.connect(self.mySslErrors)

    def mySslErrors(self,reply, errors):
        #print("reply:"+str(reply))
        #print("errors:"+str(errors))
        reply.ignoreSslErrors()

    def load(self,url):
        self.page().setNetworkAccessManager(self.myNetworkManager)
        self.setUrl(QUrl(url))

    def start_inspector(self):
        self.inspect = QWebInspector()
        self.inspect.setPage(self.page())
        self.inspect.show()

    def adjustTitle(self):
        self.setWindowTitle(self.title())

    def disableJS(self):
        self.settings.setAttribute(QWebSettings.JavascriptEnabled, False)

def old_main():
    print("FLAGS.url:"+str(FLAGS.url))
    app = QApplication(sys.argv)
    abrowser = Browser()
    abrowser.showMaximized()
    abrowser.load(FLAGS.url)
    if FLAGS.inspector :
        abrowser.start_inspector()
    sys.exit(app.exec_())

class MainWindow(QMainWindow):
    def __init__(self,*args,**kwargs):
        super(MainWindow,self).__init__(*args,**kwargs)
        self.setWindowTitle("Aurelien is testing qt")

    def start_browser(self,url):
        self.abrowser = Browser()
        self.abrowser.showMaximized()
        self.abrowser.load(url)
        if FLAGS.inspector :
            self.abrowser.start_inspector()
        self.setCentralWidget(self.abrowser)


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.start_browser(FLAGS.url)
    window.show()
    window.showMaximized()
    sys.exit(app.exec_())


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
      '--url',
      type=str,
      default=URL,
      help='url to join'
    )
    parser.add_argument(
      '--inspector',
      type=bool,
      default=0,
      help='if set to 1 it enable QWebInspector'
    )
    FLAGS, unparsed = parser.parse_known_args()
    main()

