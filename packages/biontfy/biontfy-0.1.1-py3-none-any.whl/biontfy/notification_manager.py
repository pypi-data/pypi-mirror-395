import os
from PyQt6.QtCore import (
    Qt, QObject, pyqtSignal, QPropertyAnimation, QTimer, QPoint, QEasingCurve,
    
)
from PyQt6.QtGui import (
    QGuiApplication, QScreen, QFont, QColor
)
from PyQt6.QtWidgets import (
    QPushButton, QGraphicsDropShadowEffect, QApplication
)
from collections import deque
from typing import List, Tuple
from .notification_item import NotificationItem
from .notification_utilities import load_vazirmatn_font, play_notification_sound

class NotificationManager(QObject):
    # C++: Q_OBJECT
    
    # C++: signals
    notificationReplied = pyqtSignal(str, str)

    # Singleton instance holder
    _instance = None

    # C++: Constants
    MAX_VISIBLE_NOTIFICATIONS = 2
    NOTIFICATION_SPACING = 3
    SCREEN_MARGIN = 5
    HIDE_ALL_HEIGHT = 30

    def __init__(self, parent: QObject = None):
        # C++: explicit NotificationManager(QObject *parent = nullptr);
        super().__init__(parent)
        
        # C++: QList<NotificationItem*> m_activeNotifications;
        self.m_activeNotifications: List[NotificationItem] = []
        # C++: QQueue<std::tuple<QString, QString, QString>> m_notificationQueue;
        # Using deque for the queue: (userPicPath, title, message)
        # Using deque for the queue: (userPicPath, title, message, bg_color, reply_text)
        self.m_notificationQueue: deque[Tuple[str, str, str, str, str]] = deque()
        
        # Customization defaults
        self.m_default_bg_color = "#232D37"
        self.m_default_reply_text = "Reply"
        self.m_hide_all_text = "Hide all"
        self.m_hide_all_color = "#6A99D3"
        
        # C++: QPushButton *m_hideAllButton;
        self.m_hideAllButton: QPushButton = None
        # C++: QPropertyAnimation *m_hideAllAnimation;
        self.m_hideAllAnimation: QPropertyAnimation = None

    @classmethod
    def instance(cls) -> 'NotificationManager':
        # C++: static NotificationManager& instance();
        if cls._instance is None:
            cls._instance = NotificationManager()
        return cls._instance

    def sendNotification(self, user_pic_path: str, title: str, message: str, bg_color: str = None, reply_text: str = None):
        # C++: void sendNotification(const QString &userPicPath, const QString &title, const QString &message);
        
                # Use defaults if not provided
        final_bg_color = bg_color if bg_color is not None else self.m_default_bg_color
        final_reply_text = reply_text if reply_text is not None else self.m_default_reply_text
        
        if len(self.m_activeNotifications) >= self.MAX_VISIBLE_NOTIFICATIONS:
            self.m_notificationQueue.append((user_pic_path, title, message, final_bg_color, final_reply_text))
            return

        item = NotificationItem(user_pic_path, title, message, final_bg_color, final_reply_text)
        self.m_activeNotifications.append(item)

        # Connect signals
        item.closed.connect(self.onNotificationClosed)
        item.replied.connect(self.onNotificationReplied)
        item.animationFinished.connect(self.onNotificationAnimationFinished)

        # Initial positioning (off-screen bottom right)
        screen = QGuiApplication.primaryScreen()
        if screen:
            g = screen.availableGeometry()
            x = g.width() - NotificationItem.WIDTH - self.SCREEN_MARGIN
            y = g.height()
            item.move(x, y)

                self.repositionNotifications()
        item.showAnimated()
        play_notification_sound()

    # C++: Q_INVOKABLE void sendFiveTestNotifications();
        def set_customization(self, default_bg_color: str = None, default_reply_text: str = None, hide_all_text: str = None, hide_all_color: str = None):
        if default_bg_color is not None:
            self.m_default_bg_color = default_bg_color
        if default_reply_text is not None:
            self.m_default_reply_text = default_reply_text
        if hide_all_text is not None:
            self.m_hide_all_text = hide_all_text
            if self.m_hideAllButton:
                self.m_hideAllButton.setText(self.m_hide_all_text)
        if hide_all_color is not None:
            self.m_hide_all_color = hide_all_color
            if self.m_hideAllButton:
self.m_hideAllButton.setStyleSheet(
                "QPushButton { background: " + self.m_default_bg_color + "; color:" + self.m_hide_all_color + "; border:none; font-weight:bold; }"
                "QPushButton:hover { background: " + self.m_default_bg_color + "; }"
            )

    # C++: Q_INVOKABLE void sendFiveTestNotifications();
    def sendFiveTestNotifications(self):
        # C++: sendNotification("userpic1.png", "Telegram Desktop", "This is a sample notification.");
        self.sendNotification("userpic1.png", "Telegram Desktop", "This is a sample notification.")
        # C++: sendNotification("userpic2.png", "نقاشات خطوط أحمد الغريب", "يا رب رضاك والجنة.");
        self.sendNotification("userpic2.png", "نقاشات خطوط أحمد الغريب", "يا رب رضاك والجنة.")
        # C++: sendNotification("userpic1.png", "Bot Telegram", "Telegram: @ElgharibFonts");
        self.sendNotification("userpic1.png", "Bot Telegram", "Telegram: @ElgharibFonts")
        # C++: sendNotification("userpic2.png", "Queued Notification 1", "Should be queued.");
        self.sendNotification("userpic2.png", "Queued Notification 1", "Should be queued.")
        # C++: sendNotification("userpic1.png", "Queued Notification 2", "Should be queued.");
        self.sendNotification("userpic1.png", "Queued Notification 2", "Should be queued.")

    # C++: private slots
    def onNotificationClosed(self, item: NotificationItem):
        # C++: void onNotificationClosed(NotificationItem *item);
        if item in self.m_activeNotifications:
            self.m_activeNotifications.remove(item)
            self.repositionNotifications()
            self.showNextNotification()

    def onNotificationAnimationFinished(self, item: NotificationItem):
        # C++: void onNotificationAnimationFinished(NotificationItem *item);
        # In Python, we rely on item.close() in NotificationItem.onAnimationFinished
        # to trigger the closed signal, which calls onNotificationClosed.
        # The C++ logic for deleteLater() is handled by Qt.WA_DeleteOnClose.
        pass

    def onNotificationReplied(self, item: NotificationItem):
        # C++: void onNotificationReplied(NotificationItem *item);
        self.notificationReplied.emit(item.title(), item.message())

    def onHideAllClicked(self):
        # C++: void onHideAllClicked();
        # Iterate over a copy of the list because hideAnimated() will eventually
        # remove items from m_activeNotifications via onNotificationClosed
        items_to_hide = list(self.m_activeNotifications)
        for n in items_to_hide:
            n.hideAnimated()

        if self.m_hideAllButton:
            # C++: m_hideAllButton->hide(); m_hideAllButton->deleteLater(); m_hideAllButton = nullptr;
            self.m_hideAllButton.hide()
            self.m_hideAllButton.deleteLater()
            self.m_hideAllButton = None
        
        if self.m_hideAllAnimation:
            # C++: m_hideAllAnimation->deleteLater(); m_hideAllAnimation = nullptr;
            self.m_hideAllAnimation.deleteLater()
            self.m_hideAllAnimation = None

    # C++: private methods
    def ensureHideAllButton(self):
        # C++: void ensureHideAllButton();
        if not self.m_hideAllButton:
            self.m_hideAllButton = QPushButton(self.m_hide_all_text)
            
            # C++: setWindowFlags(Qt::FramelessWindowHint | Qt::Tool | Qt::WindowStaysOnTopHint | Qt::WindowDoesNotAcceptFocus);
            flags = (
                Qt.WindowType.FramelessWindowHint | 
                Qt.WindowType.Tool | 
                Qt.WindowType.WindowStaysOnTopHint | 
                Qt.WindowType.WindowDoesNotAcceptFocus
            )
            self.m_hideAllButton.setWindowFlags(flags)
            
            # C++: setAttribute(Qt::WA_TranslucentBackground);
            self.m_hideAllButton.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
            
            # C++: setFixedSize(NotificationItem::WIDTH, HIDE_ALL_HEIGHT);
            self.m_hideAllButton.setFixedSize(NotificationItem.WIDTH, self.HIDE_ALL_HEIGHT)
            
            # C++: setFont(NotificationUtilities::loadVazirmatnFont(10));
            self.m_hideAllButton.setFont(load_vazirmatn_font(10))
            
            # C++: setStyleSheet(...)
self.m_hideAllButton.setStyleSheet(
                    "QPushButton { background: " + self.m_default_bg_color + "; color: " + self.m_hide_all_color + "; border:none; font-weight:bold; }"
                    "QPushButton:hover { background: " + self.m_default_bg_color + "; }"
                )

            # C++: QGraphicsDropShadowEffect
            shadow = QGraphicsDropShadowEffect(self.m_hideAllButton)
            shadow.setBlurRadius(15)
            shadow.setOffset(0, 2)
            shadow.setColor(QColor(0, 0, 0, 160))
            self.m_hideAllButton.setGraphicsEffect(shadow)

            # C++: connect(m_hideAllButton, &QPushButton::clicked, this, &NotificationManager::onHideAllClicked);
            self.m_hideAllButton.clicked.connect(self.onHideAllClicked)

            # C++: m_hideAllAnimation = new QPropertyAnimation(m_hideAllButton, "windowOpacity", this);
            self.m_hideAllAnimation = QPropertyAnimation(self.m_hideAllButton, b"windowOpacity", self)
            self.m_hideAllAnimation.setDuration(300)

    def repositionNotifications(self):
        # C++: void repositionNotifications();
        screen = QGuiApplication.primaryScreen()
        if not screen:
            return

        g = screen.availableGeometry()

        # 1. Calculate total height of all notifications
        total_notifications_height = 0
        for _ in self.m_activeNotifications:
            total_notifications_height += NotificationItem.HEIGHT
        
        # Add spacing between notifications
        if len(self.m_activeNotifications) > 0:
            total_notifications_height += (len(self.m_activeNotifications) - 1) * self.NOTIFICATION_SPACING

        # 2. Determine if "Hide all" button should be visible
        show_hide_all = len(self.m_activeNotifications) + len(self.m_notificationQueue) > 1

        # 3. Calculate total height including the "Hide all" button and its spacing
        total_height = total_notifications_height
        if show_hide_all:
            total_height += self.HIDE_ALL_HEIGHT + self.NOTIFICATION_SPACING

        # 4. Calculate the starting Y position (top of the entire stack)
        start_y = g.height() - total_height - self.SCREEN_MARGIN

        # 5. Reposition "Hide all" button if visible
        current_y = start_y
        x = g.width() - NotificationItem.WIDTH - self.SCREEN_MARGIN

        if show_hide_all:
            if not self.m_hideAllButton:
                self.ensureHideAllButton()
            
            # Move the button to its final position immediately (no slide animation)
            self.m_hideAllButton.move(x, current_y)

            if not self.m_hideAllButton.isVisible():
                self.m_hideAllButton.setWindowOpacity(0.0)
                self.m_hideAllButton.show()
                
                # C++: QPropertyAnimation *opacityAnim = new QPropertyAnimation(m_hideAllButton, "windowOpacity", this);
                opacity_anim = QPropertyAnimation(self.m_hideAllButton, b"windowOpacity", self)
                opacity_anim.setDuration(300)
                opacity_anim.setStartValue(0.0)
                opacity_anim.setEndValue(1.0)
                # C++: opacityAnim->start(QAbstractAnimation::DeleteWhenStopped);
                # In PyQt, we can just start it and let Python's garbage collection handle it
                # after the animation finishes, or manually manage it if needed.
                # For simplicity and 1:1 logic, we'll let it run.
                opacity_anim.start()
                # Store a reference to prevent immediate GC if needed, though QPropertyAnimation's parent should suffice.
                self._hide_all_opacity_anim_in = opacity_anim 

            self.m_hideAllButton.raise_()
            current_y += self.HIDE_ALL_HEIGHT + self.NOTIFICATION_SPACING
        else:
            if self.m_hideAllButton and self.m_hideAllButton.isVisible() and len(self.m_activeNotifications) + len(self.m_notificationQueue) <= 1:
                # Animate out and hide
                opacity_anim = QPropertyAnimation(self.m_hideAllButton, b"windowOpacity", self)
                opacity_anim.setDuration(300)
                opacity_anim.setStartValue(1.0)
                opacity_anim.setEndValue(0.0)
                opacity_anim.start()
                self._hide_all_opacity_anim_out = opacity_anim
                
                # C++: QTimer::singleShot(300, this, [this](){ if (m_hideAllButton) m_hideAllButton->hide(); });
                QTimer.singleShot(300, lambda: self.m_hideAllButton.hide() if self.m_hideAllButton else None)

        # 6. Reposition notifications (from top to bottom)
        for item in self.m_activeNotifications:
            # C++: QPropertyAnimation *anim = new QPropertyAnimation(item, "pos", this);
            anim = QPropertyAnimation(item, b"pos", self)
            anim.setDuration(300)
            anim.setEndValue(QPoint(x, current_y))
            anim.start()
            # Store a reference to prevent immediate GC
            item._reposition_anim = anim 

            current_y += NotificationItem.HEIGHT + self.NOTIFICATION_SPACING

    def showNextNotification(self):
        # C++: void showNextNotification();
        if self.m_notificationQueue and len(self.m_activeNotifications) < self.MAX_VISIBLE_NOTIFICATIONS:
            # C++: auto [pic, title, msg] = m_notificationQueue.dequeue();
            pic, title, msg = self.m_notificationQueue.popleft()
            
                        # The queued item now includes customization options
            pic, title, msg, bg_color, reply_text = self.m_notificationQueue.popleft()
            
            # C++: QTimer::singleShot(100, this, [this, pic, title, msg]() { sendNotification(pic, title, msg); });
            QTimer.singleShot(100, lambda: self.sendNotification(pic, title, msg, bg_color, reply_text))

# The C++ destructor logic is not strictly needed in Python due to garbage collection,
# but for completeness, we can add a cleanup method if the manager were to be explicitly destroyed.
# Since it's a singleton, it lives for the duration of the application.
