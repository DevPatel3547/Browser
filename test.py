import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *

#Tabbed browsing
class BrowserTab(QWidget):
    def __init__(self, parent=None):
        super(BrowserTab, self).__init__(parent)
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl('http://google.com'))

        layout = QVBoxLayout()
        layout.addWidget(self.browser)

        self.setLayout(layout)
    
    def navigate_to_url(self, url):
        self.browser.setUrl(QUrl(url))


class MainWindow(QMainWindow):
    
    def __init__(self):
        super(MainWindow, self).__init__()
        # self.browser = QWebEngineView()
        # self.browser.setUrl(QUrl('http://google.com') )
        # self.setCentralWidget(self.browser)
        # self.showMaximized()
        
        #navbar 
        navbar = QToolBar()
        self.addToolBar(navbar)
        
        #backbutton
        backbutton = QAction('<-', self)
        backbutton.triggered.connect(self.navigate_back)
        navbar.addAction(backbutton)

        #frontbutton
        frontbutton = QAction('->', self)
        frontbutton.triggered.connect(self.navigate_forward)
        navbar.addAction(frontbutton)

        #reloadbutton
        reloadbutton = QAction('Reload', self)
        reloadbutton.triggered.connect(self.navigate_reload)
        navbar.addAction(reloadbutton)

        
        #homebutton
        homebutton = QAction('Home', self)
        homebutton.triggered.connect(self.navigate_home)
        navbar.addAction(homebutton)
        
        #urlbar
        self.url_bar = QLineEdit()
        self.url_bar.returnPressed.connect(self.navigatetourl)
        navbar.addWidget(self.url_bar)


        
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        
        self.setCentralWidget(self.tabs)
        self.showMaximized()

        navbar = QToolBar()
        self.addToolBar(navbar)

        # Adding actions to the navigation bar
        add_tab_action = QAction('Add Tab', self)
        add_tab_action.triggered.connect(self.add_tab)
        navbar.addAction(add_tab_action)

        bookmark_action = QAction('Bookmark', self)
        bookmark_action.triggered.connect(self.bookmark_page)
        navbar.addAction(bookmark_action)
        
        select_bookmark_action = QAction('Select Bookmark', self)
        select_bookmark_action.triggered.connect(self.select_bookmark)
        navbar.addAction(select_bookmark_action)


        self.bookmarks = {}
        self.add_tab()
        
        
    def navigate_home(self):
        current_tab = self.tabs.currentWidget()
        current_tab.navigate_to_url('http://google.com')

    def navigatetourl(self):
        url = self.url_bar.text()
        current_tab = self.tabs.currentWidget()
        current_tab.navigate_to_url(url)

    def updateurl(self, q):
        current_tab = self.tabs.currentWidget()
        current_url = current_tab.browser.url().toString()
        self.url_bar.setText(current_url)

        
    def add_tab(self):
        tab = BrowserTab()
        i = self.tabs.addTab(tab, "New Tab")
        tab.browser.urlChanged.connect(self.updateurl)  # add this line
        self.tabs.setCurrentIndex(i)


    def select_bookmark(self):
        bookmark, ok = QInputDialog.getItem(self, "Select bookmark", "Select bookmark", list(self.bookmarks.keys()), 0, False)
        if ok and bookmark:
            self.navigate_to_bookmark(bookmark)


    def close_tab(self, i):
        if self.tabs.count() > 1:
            self.tabs.removeTab(i)

    def bookmark_page(self):
        current_tab = self.tabs.currentWidget()
        current_url = current_tab.browser.url().toString()
        self.bookmarks[current_url] = current_tab
        print("Bookmarked:", current_url)

    def navigate_to_bookmark(self, url):
        if url in self.bookmarks:
            tab = self.bookmarks[url]
            i = self.tabs.addTab(tab, url)
            self.tabs.setCurrentIndex(i)      
    def navigate_back(self):
        current_tab = self.tabs.currentWidget()
        current_tab.browser.back()

    def navigate_forward(self):
        current_tab = self.tabs.currentWidget()
        current_tab.browser.forward()

    def navigate_reload(self):
        current_tab = self.tabs.currentWidget()
        current_tab.browser.reload()
        
app = QApplication(sys.argv)
QApplication.setApplicationName("Overse")
window = MainWindow()
app.exec_()


