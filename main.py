import sys
from pathlib import Path

from PySide6 import QtCore
from PySide6.QtWidgets import (
    QApplication,
    QSystemTrayIcon,
    QMenu,
    QWidget,
    QLabel,
    QVBoxLayout,
    QLineEdit,
    QLayout,
    QAbstractButton,
)
from PySide6.QtGui import QIcon, QPalette, QColorConstants, QFont, QFontDatabase, QColor, QPainter, QPixmap, QTransform, QCursor

import items


class SystemTrayIcon(QSystemTrayIcon):
    def __init__(self, icon, parent=None):
        super().__init__(icon, parent)

        menu = QMenu(parent)
        exitAction = menu.addAction("Exit")
        self.setContextMenu(menu)
        QtCore.QObject.connect(exitAction, QtCore.SIGNAL("triggered()"), self.exit)

    def exit(self):
        QtCore.QCoreApplication.exit()


UNIQUE_ITEMS = [
    "Hand Axe",
    "Wand",
    "Holy Water Sprinkler",
    "Champion Axe",
    "Forged Knife",
    "Winged Harpoon",
    "Scourge",
    "Thunder Maul",
    "Cryptic Axe",
    "Caduceus", 
    "War Pike",
    "Phase Blade",
    "Colossus Blade",
    "Unearthed Wand",
    "----------------",
    "Cap",
    "Quilted Armor",
    "Boots",
    "Sash",
    "Winged Helm",
    "Linked Mail",
    "Battle Gauntlets",
    "Corona",
    "Bone Visage",
    "Shadow Plate",
    "Sacred Armor",
    "Blade Barrier",
    "Aegis",
    "Ogre Gauntlets",
    "Myrmidon Greaves",
    "Vampirefang Belt",
]


class ListOverlayWindow(QWidget):
    def __init__(self):
        super().__init__()
        # palette = QPalette()
        # palette.setColor(QPalette.ColorRole.Window, QColor(0, 0, 0, 100))
        # self.setPalette(palette)
        # self.setWindowOpacity(1)
        self.setStyleSheet("background-color: rgba(0, 0, 0, 0.4);")
        self.vlayout = QVBoxLayout()
        self.setLayout(self.vlayout)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
        self.setAttribute(
            QtCore.Qt.WA_NoSystemBackground, False
        )  # setting WA_TranslucentBackground also sets WA_NoSystemBackground to True
        self.setWindowFlags(
            QtCore.Qt.WindowStaysOnTopHint
            | QtCore.Qt.FramelessWindowHint
            | QtCore.Qt.WindowTransparentForInput
            | QtCore.Qt.Tool
        )

        for item in UNIQUE_ITEMS:
            label = QLabel(item)
            label.setFont(QFont("ExocetBlizzardMixedCapsOTMedium", 15))
            label.setStyleSheet(
                "QLabel { color: rgba(199, 179, 119, 0.8); background-color: transparent; }"
            )  # #00FF00 for sets
            self.vlayout.addWidget(label)


class PictureButton(QAbstractButton):

    def __init__(self, parent):
        super().__init__(parent)
        _mirror_tranform = QTransform().scale(-1, 1)
        self.default_picture = QPixmap("assets\\advancedstatsbutton.sprite.00.png").transformed(_mirror_tranform)
        self.press_picture = QPixmap("assets\\advancedstatsbutton.sprite.01.png").transformed(_mirror_tranform)
        self.setPicture(self.default_picture)
        self.pressed.connect(self._mouse_press)
        self.released.connect(self._mouse_release)

    def setPicture(self, picture):
        self.picture = picture
        self.update()

    def sizeHint(self):
        print('size hint called', self.picture.size())
        return self.picture.size()
    
    def _mouse_press(self):
        self.setPicture(self.press_picture)
    
    def _mouse_release(self):
        self.setPicture(self.default_picture)   

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.drawPixmap(0, 0, self.picture)


class ButtonWindow(QWidget):
    def __init__(self):
        super().__init__()

        self.button = PictureButton(self)
        p = QPixmap("assets\\ohand.sprite.00.png").transformed(QTransform().fromScale(0.5, 0.5))
        print('image size', p.size())
        self.button.setCursor(QCursor(p, hotX=0, hotY=0))
        self.setFixedSize(self.button.sizeHint())
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
        self.setWindowFlags(
            QtCore.Qt.WindowStaysOnTopHint
            | QtCore.Qt.FramelessWindowHint
            | QtCore.Qt.Tool
        )

class SearchWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setStyleSheet("background-color: rgba(0, 0, 0, 0.6);")
        self.vlayout = QVBoxLayout()
        self.setLayout(self.vlayout)
        self.search_bar = QLineEdit()
        self.search_bar.setFont(QFont("ExocetBlizzardMixedCapsOTMedium", 15))
        self.search_bar.setStyleSheet(
            """
            QLineEdit { 
                color: rgba(255, 255, 255, 0.8); 
                background-color: transparent;
                border: 1px solid gray;
                border-radius: 3px;
            }
            QLineEdit:focus { 
                border: 1px solid rgb(199, 179, 119);
            }
            """
        )
        self.search_bar.textChanged.connect(self.search)
        # self.search_bar.setFocus()
        self.vlayout.addWidget(self.search_bar)
        self.vlayout.setSizeConstraint(QLayout.SetFixedSize)
        # shrink window when removing labels

        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
        self.setAttribute(
            QtCore.Qt.WA_NoSystemBackground, False
        )  # setting WA_TranslucentBackground also sets WA_NoSystemBackground to True
        self.setWindowFlags(
            QtCore.Qt.WindowStaysOnTopHint
            | QtCore.Qt.FramelessWindowHint
            | QtCore.Qt.Tool
        )

        self.result_labels = []

    def search(self):
        for label in self.result_labels:
            self.vlayout.removeWidget(label)
            label.hide()
        self.result_labels = []

        result_items = items.search(self.search_bar.text())
        for item in result_items:
            label = QLabel(f"{item.name} - {item.base}")
            if item.rarity == items.UNIQUE:
                color = "199, 179, 119"
            elif item.rarity == items.SET:
                color = "0, 255, 0"
            elif item.rarity == items.RUNE:
                # color = '255, 168, 0'  # crafted
                color = "175, 117, 5"
            label.setFont(QFont("ExocetBlizzardMixedCapsOTMedium", 15))
            label.setStyleSheet(
                f"QLabel {{ color: rgba({color}, 0.8); background-color: transparent; }}"
            )
            self.vlayout.addWidget(label)
            self.result_labels.append(label)


def main():
    app = QApplication(sys.argv)
    id = QFontDatabase.addApplicationFont(
        str(Path(__file__).parent / 'assets' / 'exocetblizzardot-medium.otf')
    )
    # families = QFontDatabase.applicationFontFamilies(id)
    # print(families[0])
    app.setQuitOnLastWindowClosed(False)

    trayIcon = SystemTrayIcon(QIcon(str(Path(__file__).parent / 'assets' / 'icon.png')))

    trayIcon.show()
    button_window = ButtonWindow()
    list_window = ListOverlayWindow()
    list_window.show()
    screen_width, screen_height = list_window.screen().size().toTuple()
    x = screen_width - list_window.width()
    y = (screen_height - list_window.height()) / 2
    list_window.move(x, y)
    button_window.show()
    print('button window', button_window.width(), button_window.height())
    button_window.move(x + list_window.width() - button_window.width(), y - button_window.height())

    # search_window = SearchWindow()
    # search_window.show()
    # screen_width, screen_height = search_window.screen().size().toTuple()
    # x = screen_width / 2
    # y = screen_height / 2
    # search_window.move(x, y)
    # search_window.activateWindow()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
