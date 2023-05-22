import sys
import database
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import *
from PyQt5.QtGui import *
from user_management import create_user, get_user

#Tabbed browsing
class BrowserTab(QWidget):
    def __init__(self, parent=None):
        super(BrowserTab, self).__init__(parent)
        self.browser = QWebEngineView()
        self.browser.setUrl(QUrl('http://google.com'))
        self.browser.loadProgress.connect(self.update_progress)
        layout = QVBoxLayout()
        layout.addWidget(self.browser)

        self.setLayout(layout)
    
    def navigate_to_url(self, url):
        self.browser.setUrl(QUrl(url))
    def update_progress(self, p):
        window.status.showMessage(f'Loading... {p}%', 2000 if p==100 else 0)
class Omnibox(QLineEdit):
    def __init__(self, parent=None):
        super(Omnibox, self).__init__(parent)
        self.history = []

    def update_history(self, url):
        if url not in self.history:
            self.history.append(url)

    def keyPressEvent(self, event):
        super(Omnibox, self).keyPressEvent(event)
        if event.key() == Qt.Key_Down:
            self.show_suggestions()
    def show_suggestions(self):
        completion_model = QStringListModel(self.history, self)
        completer = QCompleter(completion_model, self)
        self.setCompleter(completer)
        completer.complete()
        

class UserProfileDialog(QDialog):
    def __init__(self, parent=None):
        super(UserProfileDialog, self).__init__(parent)
        self.setWindowTitle("User Profile")
        self.username_label = QLabel("Username")
        self.password_label = QLabel("Password")
        self.username_input = QLineEdit()
        self.password_input = QLineEdit()
        self.ok_button = QPushButton("OK")
        self.ok_button.clicked.connect(self.create_user)

        layout = QVBoxLayout()
        layout.addWidget(self.username_label)
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_label)
        layout.addWidget(self.password_input)
        layout.addWidget(self.ok_button)

        self.setLayout(layout)

    def create_user(self):
        create_user(self.username_input.text(), self.password_input.text())
        self.accept()


class MainWindow(QMainWindow):
    
    def __init__(self):
        super(MainWindow, self).__init__()

        # Initialize database
        self.db = database.Database()
        
        # Initialize user
        self.user = None

        #navbar 
        navbar = QToolBar()
        self.addToolBar(navbar)
                
        #backbutton
        backbutton = QAction(QIcon('./images/back.png'), '<-', self)
        backbutton.triggered.connect(self.navigate_back)
        navbar.addAction(backbutton)

        #frontbutton
        frontbutton = QAction(QIcon('./images/forward.png'), '->', self)
        frontbutton.triggered.connect(self.navigate_forward)
        navbar.addAction(frontbutton)

        #reloadbutton
        reloadbutton = QAction(QIcon('./images/reload.png'), 'Reload', self)
        reloadbutton.triggered.connect(self.navigate_reload)
        navbar.addAction(reloadbutton)

        #homebutton
        homebutton = QAction(QIcon('./images/home.png'), 'Home', self)
        homebutton.triggered.connect(self.navigate_home)
        navbar.addAction(homebutton)
                
        #urlbar
        self.url_bar = Omnibox()
        self.url_bar.returnPressed.connect(self.navigatetourl)
        navbar.addWidget(self.url_bar)

        # User profile button
        user_button = QAction(QIcon('./images/user.png'), 'User', self)
        user_button.triggered.connect(self.show_user_profile)
        navbar.addAction(user_button)

        # Adding actions to the navigation bar
        add_tab_action = QAction(QIcon('./images/addtab.png'), 'Add Tab', self)
        add_tab_action.triggered.connect(self.add_tab)
        navbar.addAction(add_tab_action)

        bookmark_action = QAction(QIcon('./images/bookmark.png'), 'Bookmark', self)
        bookmark_action.triggered.connect(self.bookmark_page)
        navbar.addAction(bookmark_action)
                
        select_bookmark_action = QAction(QIcon('./images/selectbookmark.png'), 'Select Bookmark', self)
        select_bookmark_action.triggered.connect(self.select_bookmark)
        navbar.addAction(select_bookmark_action)
        
        self.status = QStatusBar()
        self.setStatusBar(self.status)

        # Tabbed browsing
        self.tabs = QTabWidget()
        self.tabs.setDocumentMode(True)
        self.tabs.setTabsClosable(True)
        self.tabs.tabCloseRequested.connect(self.close_tab)
        
        main_layout = QVBoxLayout()
        main_layout.addWidget(self.tabs)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        main_widget = QWidget()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)
        self.showMaximized()



        self.bookmarks = {}
        self.add_tab()
        
        self.setStyleSheet("""
            QMainWindow {
                background-color: #333;
            }

            QToolBar {
                background-color: #555;
            }

            QLineEdit {
                height: 25px;
                background-color: #fff;
                color: #000;
            }

            QPushButton {
                background-color: #f00;
                color: #fff;
                height: 25px;
                border: none;
            }
        """)


    def show_user_profile(self):
        dialog = UserProfileDialog(self)
        if dialog.exec_():
            self.user = get_user(dialog.username_input.text())

    def updateurl(self, q):
        self.url_bar.setText(q.toString())
        self.url_bar.update_history(q.toString())        
        
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
            # Instead of adding a tab, just set the current tab's URL to the bookmarked one
            current_tab = self.tabs.currentWidget()
            current_tab.navigate_to_url(url)
        
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
