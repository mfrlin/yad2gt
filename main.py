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
)
from PySide6.QtGui import QIcon, QPalette, QColorConstants, QFont, QFontDatabase, QColor

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

    color_window = ListOverlayWindow()
    color_window.show()
    screen_width, screen_height = color_window.screen().size().toTuple()
    x = screen_width - color_window.width()
    y = (screen_height - color_window.height()) / 2
    color_window.move(x, y)

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
