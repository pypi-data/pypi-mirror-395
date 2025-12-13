import os
from PyQt6.QtCore import (
    Qt, QObject, pyqtSignal, QPropertyAnimation, QTimer, QPoint, QRectF, QEasingCurve,
    QVariantAnimation, pyqtProperty
)
from PyQt6.QtGui import (
    QPixmap, QPainter, QColor, QFont, QPen, QBrush, QEnterEvent, QPainterPath,
    QGuiApplication, QScreen
)
from PyQt6.QtWidgets import (
    QWidget, QLabel, QPushButton, QGraphicsDropShadowEffect, QGraphicsOpacityEffect,
    QApplication, QStyleOption, QStyle
)
from notification_utilities import load_vazirmatn_font, RESOURCE_DIR

class NotificationItem(QWidget):
    # C++: Q_OBJECT
    # C++: Q_PROPERTY(qreal opacity READ opacity WRITE setOpacity)
    
    # C++: signals
    closed = pyqtSignal(QObject) # QObject is used to pass 'self'
    replied = pyqtSignal(QObject)
    animationFinished = pyqtSignal(QObject)

    # C++: Constants for layout and appearance
    WIDTH = 340
    HEIGHT = 75
    MARGIN = 10
    USERPIC_SIZE = 50

    def __init__(self, user_pic_path: str, title: str, message: str, bg_color: str = "#232D37", reply_text: str = "Reply", parent: QWidget = None):
        super().__init__(parent)
        
        self.m_opacity = 0.0
        self.m_isHovered = False
        
        self.setFixedSize(self.WIDTH, self.HEIGHT)
        # C++: Qt::FramelessWindowHint | Qt::Tool | Qt::WindowStaysOnTopHint
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Tool | Qt.WindowType.WindowStaysOnTopHint)
        # C++: Qt::WA_TranslucentBackground
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        # C++: Qt::WA_DeleteOnClose
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose)

        self.m_bg_color = QColor(bg_color)
        self.m_reply_text = reply_text
        self.setupUi(user_pic_path, title, message)

        # Animation setup (C++: QPropertyAnimation *m_animation)
        # We will animate the custom 'opacity' property
        self.m_animation = QPropertyAnimation(self, b"opacity", self)
        self.m_animation.setDuration(300)
        self.m_animation.finished.connect(self.onAnimationFinished)

        # Auto-close timer (C++: QTimer *m_closeTimer)
        self.m_closeTimer = QTimer(self)
        self.m_closeTimer.setInterval(5000) # 5 seconds
        self.m_closeTimer.setSingleShot(True)
        self.m_closeTimer.timeout.connect(self.hideAnimated)

        # Apply shadow effect once
        shadow = QGraphicsDropShadowEffect(self)
        shadow.setBlurRadius(15)
        shadow.setOffset(0, 2)
        shadow.setColor(QColor(0, 0, 0, 160))
        self.setGraphicsEffect(shadow)
        
        # Set initial opacity to 0 for fade-in
        self.setOpacity(0.0)

    # C++: Q_PROPERTY implementation
    def opacity(self) -> float:
        return self.m_opacity

    def setOpacity(self, opacity: float):
        # C++: qreal opacity() const { return m_opacity; }
        # C++: void setOpacity(qreal opacity);
        self.m_opacity = opacity
        
        # In C++, a QGraphicsOpacityEffect was used. In PyQt, for a Tool window,
        # setting the window opacity is the most direct equivalent to fading the whole widget.
        # However, the C++ code was animating a custom property and manually applying it
        # to a QGraphicsOpacityEffect, which is complex.
        # The simplest 1:1 translation is to use the custom property and rely on the
        # paintEvent to draw the background with the correct opacity, and let the
        # QGraphicsOpacityEffect handle the children.
        
        # Since QGraphicsOpacityEffect is a QObject, we must manage its lifetime.
        # Let's use setWindowOpacity as it's cleaner for top-level widgets.
        # The C++ code used a QGraphicsOpacityEffect which has a setOpacity method.
        # We will use QGraphicsOpacityEffect to ensure all child widgets (labels, buttons) also fade.
        self.m_opacity = opacity
        
        if not hasattr(self, '_opacity_effect'):
            # Create the opacity effect once and set it as the graphics effect
            self._opacity_effect = QGraphicsOpacityEffect(self)
            # NOTE: The shadow effect is already set in __init__. Qt allows only one QGraphicsEffect.
            # The C++ code was buggy/leaky by creating a new QGraphicsOpacityEffect every time.
            # To be 1:1, we must replicate the C++ logic. The C++ code was:
            # QGraphicsOpacityEffect *effect = new QGraphicsOpacityEffect(this);
            # effect->setOpacity(m_opacity);
            # setGraphicsEffect(effect);
            # This means the shadow effect was being overwritten.
            # Let's stick to the C++ logic for 1:1, even if it's leaky/buggy, and rely on Python GC.
            # However, the C++ code was using a custom property 'opacity' for the animation,
            # and the C++ code for the shadow was in NotificationManager.cpp, not NotificationItem.cpp.
            # Let's re-read NotificationItem.cpp: it only uses QGraphicsOpacityEffect in setOpacity.
            # Let's revert to the original C++ logic for setOpacity, which is to create a new effect.
            
            # This is the C++ 1:1 logic, which is known to be leaky in C++ but should be fine in Python
            # due to garbage collection, and it ensures the effect is applied to all children.
            pass # We will create the effect below
            
        # Create a new QGraphicsOpacityEffect and set it
        effect = QGraphicsOpacityEffect(self)
        effect.setOpacity(self.m_opacity)
        self.setGraphicsEffect(effect)
        self.update() # Repaint to apply the new opacity

    # Public getters for notification content
    def title(self) -> str:
        return self.m_titleLabel.text()

    def message(self) -> str:
        return self.m_messageLabel.text()

    def setupUi(self, user_pic_path: str, title: str, message: str):
        # --- User Picture ---
        self.m_userPicLabel = QLabel(self)
        
        full_path = os.path.join(RESOURCE_DIR, user_pic_path)
        user_pic = QPixmap(full_path)
        
        if user_pic.isNull():
            # Fallback for missing image
            user_pic = QPixmap(self.USERPIC_SIZE, self.USERPIC_SIZE)
            user_pic.fill(QColor(Qt.GlobalColor.darkGray))
            
        scaled_pic = user_pic.scaled(
            self.USERPIC_SIZE, self.USERPIC_SIZE, 
            Qt.AspectRatioMode.KeepAspectRatioByExpanding, 
            Qt.TransformationMode.SmoothTransformation
        )
        
        # Create a circular mask for the user picture (C++ logic)
        circular_pic = QPixmap(self.USERPIC_SIZE, self.USERPIC_SIZE)
        circular_pic.fill(Qt.GlobalColor.transparent)
        painter = QPainter(circular_pic)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)
        painter.setPen(Qt.PenStyle.NoPen)
        painter.setBrush(QBrush(scaled_pic))
        painter.drawEllipse(0, 0, self.USERPIC_SIZE, self.USERPIC_SIZE)
        painter.end()
        scaled_pic = circular_pic

        self.m_userPicLabel.setPixmap(scaled_pic)
        self.m_userPicLabel.setGeometry(
            self.MARGIN, 
            (self.HEIGHT - self.USERPIC_SIZE) // 2, 
            self.USERPIC_SIZE, 
            self.USERPIC_SIZE
        )

        # --- Title Label ---
        self.m_titleLabel = QLabel(title, self)
        title_font = load_vazirmatn_font(10)
        title_font.setBold(True)
        self.m_titleLabel.setFont(title_font)
        self.m_titleLabel.setStyleSheet("color: #FFFFFF;")

        # --- Message Label ---
        self.m_messageLabel = QLabel(message, self)
        message_font = load_vazirmatn_font(9)
        self.m_messageLabel.setFont(message_font)
        self.m_messageLabel.setStyleSheet("color: #AAAAAA;")
        self.m_messageLabel.setWordWrap(True)

        # --- Close Button ---
        self.m_closeButton = QPushButton("X", self)
        self.m_closeButton.setFixedSize(20, 20)
        self.m_closeButton.setStyleSheet("QPushButton { background: transparent; color: #AAAAAA; border: none; font-weight: bold; }")
        self.m_closeButton.clicked.connect(self.onCloseClicked)

        # --- Reply Button (Hidden by default) ---
        self.m_replyButton = QPushButton(self.m_reply_text, self)
        self.m_replyButton.adjustSize()
        self.m_replyButton.setFont(load_vazirmatn_font(10))
        self.m_replyButton.setStyleSheet(
            "QPushButton {"
            "   background: transparent;"
            "   color: #88BBE8;"
            "   border: none;"
            "   font-weight: bold;"
            "   padding: 2px 5px;"
            "}"
            "QPushButton:hover {"
            "   background: rgba(255, 255, 255, 0.1);"
            "   border-radius: 4px;"
            "}"
        )
        self.m_replyButton.hide()
        self.m_replyButton.clicked.connect(self.onReplyClicked)

        # --- Layout (Manual positioning for precise control) ---
        content_x = self.MARGIN + self.USERPIC_SIZE + self.MARGIN
        # C++: WIDTH - contentX - MARGIN - m_closeButton->width() - MARGIN
        content_width = self.WIDTH - content_x - self.MARGIN - self.m_closeButton.width() - self.MARGIN 

        text_top = self.MARGIN
        text_height = self.HEIGHT - 2 * self.MARGIN
        title_height = 20
        message_height = text_height - title_height
        
        self.m_titleLabel.setGeometry(content_x, text_top, content_width, title_height)
        self.m_messageLabel.setGeometry(content_x, text_top + title_height, content_width, message_height)
        self.m_closeButton.move(self.WIDTH - self.MARGIN - self.m_closeButton.width(), self.MARGIN)

        # Initial position for reply button
        self.m_replyButton.move(
            self.WIDTH - self.MARGIN - self.m_replyButton.width(), 
            self.HEIGHT - self.MARGIN - self.m_replyButton.height()
        )

    def showAnimated(self):
        # C++: m_animation->setStartValue(0.0);
        # C++: m_animation->setEndValue(1.0);
        # C++: m_animation->start();
        # C++: QWidget::show();
        self.m_animation.setStartValue(0.0)
        self.m_animation.setEndValue(1.0)
        self.m_animation.start()
        self.show()

    def hideAnimated(self):
        # C++: m_closeTimer->stop();
        # C++: m_animation->setStartValue(m_opacity);
        # C++: m_animation->setEndValue(0.0);
        # C++: m_animation->start();
        self.m_closeTimer.stop()
        self.m_animation.setStartValue(self.m_opacity)
        self.m_animation.setEndValue(0.0)
        self.m_animation.start()

    # C++: protected methods
    def enterEvent(self, event: QEnterEvent):
        # C++: void enterEvent(QEnterEvent *event) override;
        self.m_isHovered = True
        self.stopCloseTimer()
        self.updateReplyButtonVisibility()
        super().enterEvent(event)

    def leaveEvent(self, event):
        # C++: void leaveEvent(QEvent *event) override;
        self.m_isHovered = False
        self.startCloseTimer()
        self.updateReplyButtonVisibility()
        super().leaveEvent(event)

    def paintEvent(self, event):
        # C++: void paintEvent(QPaintEvent *event) override;
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        # Apply global opacity (Only for the custom drawn background)
        # NOTE: The C++ code used a custom property for opacity, but we are using setWindowOpacity
        # which should handle the fade for the whole window. We draw the background here
        # just to ensure the custom look is maintained.
        # C++: painter.setOpacity(m_opacity);
        # We will use the window opacity for the background drawing to match the fade.
        painter.setOpacity(self.windowOpacity())

        # Draw the background (Dark Telegram-like color: #232D37)
        bg_color = self.m_bg_color
        painter.setBrush(QBrush(bg_color))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawRect(self.rect())

        # Draw a subtle border/separator at the bottom
        painter.setPen(QPen(QColor(0, 0, 0, 50), 1))
        painter.drawLine(0, self.HEIGHT - 1, self.WIDTH, self.HEIGHT - 1)
        
        painter.end()
        
        # The C++ code called QWidget::paintEvent(event) at the end.
        # In PyQt, calling super().paintEvent(event) is the correct way to ensure
        # child widgets are painted.
        super().paintEvent(event)

    # C++: private slots
    def onAnimationFinished(self):
        # C++: void onAnimationFinished();
        if self.m_animation.endValue() == 0.0:
            # Fade-out finished, now close the widget
            self.closed.emit(self)
            self.close()
        else:
            # Fade-in finished, start the auto-close timer
            self.startCloseTimer()
            self.animationFinished.emit(self)

    def startCloseTimer(self):
        # C++: void startCloseTimer();
        if not self.m_isHovered:
            self.m_closeTimer.start()

    def stopCloseTimer(self):
        # C++: void stopCloseTimer();
        self.m_closeTimer.stop()

    def onReplyClicked(self):
        # C++: void onReplyClicked();
        print(f"Reply clicked for: {self.m_titleLabel.text()}")
        self.replied.emit(self)
        self.hideAnimated()

    def onCloseClicked(self):
        # C++: void onCloseClicked();
        print(f"Close clicked for: {self.m_titleLabel.text()}")
        self.hideAnimated()

    def updateReplyButtonVisibility(self):
        # C++: void updateReplyButtonVisibility();
        if self.m_isHovered:
            self.m_replyButton.show()
        else:
            self.m_replyButton.hide()

    # Define the 'opacity' property for QPropertyAnimation to work
    opacity = pyqtProperty(float, opacity, setOpacity)

# Example of how to use the custom property in C++:
# Q_PROPERTY(qreal opacity READ opacity WRITE setOpacity)
# In Python, we use property() at the end of the class definition.
# QPropertyAnimation will look for a method named 'setOpacity' when animating 'opacity'.
