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
    QHBoxLayout,
    QFormLayout,
    QLineEdit,
    QLayout,
    QAbstractButton,
    QCheckBox,
    QSizePolicy,
)
from PySide6.QtGui import (
    QIcon, 
    QKeyEvent, 
    QPalette, 
    QColorConstants,
    QFont,
    QFontDatabase, 
    QColor, 
    QPainter, 
    QPixmap, 
    QTransform, 
    QCursor,
)

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

class HandCursor(QCursor):
    def __init__(self):
        p = QPixmap("assets\\ohand.sprite.00.png").transformed(QTransform().fromScale(0.5, 0.5))
        super().__init__(p, hotX=0, hotY=0)



class ListOverlayWindow(QWidget):
    DEFAULT_STATE =  (
        QtCore.Qt.WindowStaysOnTopHint
        | QtCore.Qt.FramelessWindowHint
        | QtCore.Qt.WindowTransparentForInput
        | QtCore.Qt.Tool
    )
    CLICKABLE_STATE =  (
        QtCore.Qt.WindowStaysOnTopHint
        | QtCore.Qt.FramelessWindowHint
        | QtCore.Qt.Tool
    )
    def __init__(self):
        super().__init__()
        self.setCursor(HandCursor())
        # palette = QPalette()
        # palette.setColor(QPalette.ColorRole.Window, QColor(0, 0, 0, 100))
        # self.setPalette(palette)
        # self.setWindowOpacity(1)
        self._locked = True
        self.setStyleSheet("background-color: rgba(0, 0, 0, 0.6);")
        self.vlayout = QVBoxLayout()
        self.setLayout(self.vlayout)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
        self.setAttribute(
            QtCore.Qt.WA_NoSystemBackground, False
        )  # setting WA_TranslucentBackground also sets WA_NoSystemBackground to True
        self.setWindowFlags(self.DEFAULT_STATE)
        
        self.uniques_label = QLabel("")
        self.uniques_label.setFont(QFont("ExocetBlizzardMixedCapsOTMedium", 15))
        self.uniques_label.setStyleSheet(
            "QLabel { color: rgba(199, 179, 119, 0.8); background-color: transparent; }"
        )
        self.vlayout.addWidget(self.uniques_label)

        self.sets_label = QLabel("")
        self.sets_label.setFont(QFont("ExocetBlizzardMixedCapsOTMedium", 15))
        self.sets_label.setStyleSheet(
            "QLabel { color: rgba(0, 255, 0, 0.8); background-color: transparent; }"
        )
        self.vlayout.addWidget(self.sets_label)

        self.runes_label = QLabel("")
        self.runes_label.setFont(QFont("ExocetBlizzardMixedCapsOTMedium", 15))
        self.runes_label.setStyleSheet(
            "QLabel { color: rgba(175, 117, 5, 0.8); background-color: transparent; }"
        )
        self.vlayout.addWidget(self.runes_label)

        self.set_stats()
    
    def show(self):
        self.set_stats()
        super().show()
    
    def set_stats(self):
        uniques = 0
        found_uniques = 0
        sets = 0
        found_sets = 0
        runes = 0
        found_runes = 0
        for item in items._ITEMS:
            if item.rarity == items.Rarity.UNIQUE:
                uniques += 1
                if item.id in items._FOUND_ITEMS_IDS:
                    found_uniques += 1
            elif item.rarity == items.Rarity.SET:
                sets += 1
                if item.id in items._FOUND_ITEMS_IDS:
                    found_sets += 1
            elif item.slot == items.Slot.RUNE:
                runes += 1
                if item.id in items._FOUND_ITEMS_IDS:
                    found_runes += 1
        uniqes_stats = f"[{found_uniques}/{uniques}][{int(found_uniques/uniques*100)}%]"
        self.uniques_label.setText(f"[+] Uniques {'':>{27-12-len(uniqes_stats)}}{uniqes_stats}")

        sets_stats = f"[{found_sets}/{sets}][{int(found_sets/sets*100)}%]"
        self.sets_label.setText(f"[+] Sets {'':>{27-7-len(uniqes_stats)}}{sets_stats}")

        runes_stats = f"[{found_runes}/{runes}][{int(found_runes/runes*100)}%]"
        self.runes_label.setText(f"[+] Runes {'':>{27-9-len(runes_stats)}}{runes_stats}")


    def toggle_locked(self):
        visible = self.isVisible()
        if self._locked:
            self.setWindowFlags(self.CLICKABLE_STATE)
        else:
            self.setWindowFlags(self.DEFAULT_STATE)
        if visible:
            # setWindowFlags hides the window
            # if window was visible before call show()
            self.show()
        self._locked = not self._locked


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
        return self.picture.size()
    
    def _mouse_press(self):
        self.setPicture(self.press_picture)
    
    def _mouse_release(self):
        self.setPicture(self.default_picture)   

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.drawPixmap(0, 0, self.picture)


class ListLockButton(QAbstractButton):
    def __init__(self, parent):
        super().__init__(parent)
        self._locked = True
        self.locked_picture = QPixmap("assets\\lootbody.sprite.00.png")
        self.pressed_picture = QPixmap("assets\\lootbody.sprite.01.png")
        self.unlocked_picture = QPixmap("assets\\lootbody.sprite.02.png")
        self._default_picture = self.locked_picture
        self.setPicture(self.locked_picture)
        self.pressed.connect(self._mouse_press)
        self.released.connect(self._mouse_release)
        self.clicked.connect(self._toggle)

    def setPicture(self, picture):
        self._picture = picture
        self.update()

    def sizeHint(self):
        return self._picture.size()
    
    def _mouse_press(self):
        self.setPicture(self.pressed_picture)
    
    def _mouse_release(self):
        self.setPicture(self._default_picture)
    
    def _toggle(self):
        self._locked = not self._locked
        if self._locked:
            self._default_picture = self.locked_picture
        else:
            self._default_picture = self.unlocked_picture
        self.setPicture(self._default_picture)

    def paintEvent(self, e):
        painter = QPainter(self)
        painter.drawPixmap(0, 0, self._picture)


class ButtonWindow(QWidget):
    def __init__(self, list_window, toggle_windows):
        super().__init__()

        self.list_window = list_window
        self.list_window_locked = True

        self.search_button = PictureButton(self)
        self.setCursor(HandCursor())
        # self.setFixedSize(self.search_button.sizeHint())
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
        self.setWindowFlags(
            QtCore.Qt.WindowStaysOnTopHint
            | QtCore.Qt.FramelessWindowHint
            | QtCore.Qt.Tool
        )
        self.search_button.clicked.connect(toggle_windows)

        self.list_button = ListLockButton(self)
        self.setCursor(HandCursor())
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
        self.setWindowFlags(
            QtCore.Qt.WindowStaysOnTopHint
            | QtCore.Qt.FramelessWindowHint
            | QtCore.Qt.Tool
        )
        self.list_button.clicked.connect(self.list_window.toggle_locked)

        self.hlayout = QHBoxLayout()
        self.setLayout(self.hlayout)
        self.hlayout.addWidget(self.search_button)
        self.hlayout.addWidget(self.list_button)

class ItemCheckbox(QCheckBox):
    def __init__(self, item_id):
        super().__init__()
        self.item_id = item_id
        self.clicked.connect(self.mark_item)

    def mark_item(self, checked: bool):
        if checked:
            items.mark_found(self.item_id)
        else:
            items.mark_missing(self.item_id)


class SearchWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setCursor(HandCursor())
        self.setStyleSheet("background-color: rgba(0, 0, 0, 0.6);")
        self.vlayout = QVBoxLayout()
        self.setLayout(self.vlayout)
        self.flayout = QFormLayout()
        self.search_bar = QLineEdit()
        self.search_bar.setMinimumWidth(665)  # TODO: why doesn't this work on window
        self.search_bar.setFont(QFont("ExocetBlizzardMixedCapsOTMedium", 20))
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
        self.vlayout.addWidget(self.search_bar)
        self.vlayout.addLayout(self.flayout)
        # shrink window when removing items
        self.vlayout.setSizeConstraint(QLayout.SetFixedSize)

        self.setAttribute(QtCore.Qt.WA_TranslucentBackground, True)
        self.setAttribute(
            QtCore.Qt.WA_NoSystemBackground, False
        )  # setting WA_TranslucentBackground also sets WA_NoSystemBackground to True
        self.setWindowFlags(
            QtCore.Qt.WindowStaysOnTopHint
            | QtCore.Qt.FramelessWindowHint
            | QtCore.Qt.Tool
        )

    def search(self):
        while self.flayout.rowCount():
            self.flayout.removeRow(0)

        result_items = items.search(self.search_bar.text())
        for item in result_items[:20]:
            label = QLabel(f"{item.name} - {item.base}")
            if item.rarity == items.Rarity.UNIQUE:
                color = "199, 179, 119"
            elif item.rarity == items.Rarity.SET:
                color = "0, 255, 0"
            elif item.slot == items.Slot.RUNE:
                # color = '255, 168, 0'  # crafted
                color = "175, 117, 5"
            label.setFont(QFont("ExocetBlizzardMixedCapsOTMedium", 20))
            label.setStyleSheet(
                f"QLabel {{ color: rgba({color}, 0.8); background-color: transparent; }}"
            )
            checkbox = ItemCheckbox(item_id=item.id)
            checkbox.setStyleSheet(
                "QCheckBox::indicator { width: 20px; height: 18px;}"
                f"QCheckBox::indicator::unchecked {{ border: 1px solid rgba({color}, 0.8); background: transparent; }}"
                f"QCheckBox::indicator::checked {{ background: rgb({color}); }}"
            )
            if item.id in items._FOUND_ITEMS_IDS:
                checkbox.setChecked(True)
            self.flayout.addRow(checkbox, label)
    
    def hide(self):
        self.search_bar.clear()
        super().hide()
    
    def set_toggle_function(self, toggle_function):
        self.toggle_function = toggle_function
    
    def keyPressEvent(self, event: QKeyEvent) -> None:
        if event.key() == QtCore.Qt.Key.Key_Escape:
            # TODO: where does focus go after hiding this? can we focus D2 app?
            self.toggle_function()
        return super().keyPressEvent(event)
    

def main():
    app = QApplication(sys.argv)
    QFontDatabase.addApplicationFont(
        str(Path(__file__).parent / 'assets' / 'exocetblizzardot-medium.otf')
    )
    app.setQuitOnLastWindowClosed(False)

    trayIcon = SystemTrayIcon(QIcon(str(Path(__file__).parent / 'assets' / 'icon.png')))

    trayIcon.show()
    list_window = ListOverlayWindow()
    list_window.show()
    screen_width, screen_height = list_window.screen().size().toTuple()
    x = screen_width - list_window.width()
    y = (screen_height - list_window.height()) / 2
    list_window.move(x, y)

    search_window = SearchWindow()
    search_window.move(screen_width - 670, y)

    show_list_window = True
    def toggle_windows():
        nonlocal show_list_window
        if show_list_window:
            list_window.hide()
            search_window.show()
            search_window.activateWindow()
        else:
            search_window.hide()
            list_window.show()
        show_list_window = not show_list_window
    
    # TODO: figure out something to deal with this interconnected state
    search_window.set_toggle_function(toggle_windows)



    button_window = ButtonWindow(list_window, toggle_windows)
    button_window.show()
    button_window.move(x + list_window.width() - button_window.width(), y - button_window.height())
    

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
