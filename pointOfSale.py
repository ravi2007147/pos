import sys
from PyQt5.QtWidgets import(QApplication, QFrame,QLabel, QWidget, QMainWindow, QVBoxLayout, QHBoxLayout,
    QPushButton,)
from PyQt5.QtCore import Qt


class pointofsale(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("POS System")
        self.showMaximized()  

        widget = QWidget()
        dashboard_layout = QHBoxLayout()
        widget.setLayout(dashboard_layout)
        self.setCentralWidget(widget)

        
        sidebar = QFrame()
        sidebar.setFrameShape(QFrame.StyledPanel)
        sidebar.setFixedWidth(200)
        sidebar_layout = QVBoxLayout()
        sidebar.setLayout(sidebar_layout)

        sidebar_label = QLabel("Dashboard")
        sidebar_label.setAlignment(Qt.AlignCenter)
        sidebar_label.setStyleSheet("font-weight: bold; font-size: 16px;")
        sidebar_layout.addWidget(sidebar_label)

        Button = QPushButton("Dashboard")
        Button.setFixedHeight(40)
        sidebar_layout.addWidget(Button)

        Button1 = QPushButton("Product List")
        Button1.setFixedHeight(40)
        sidebar_layout.addWidget(Button1)

        Button2 = QPushButton("Point of sale")
        Button2.setFixedHeight(40)
        sidebar_layout.addWidget(Button2)

        Button3 = QPushButton("Sales report")
        Button3.setFixedHeight(40)
        sidebar_layout.addWidget(Button3)

        dashboard_layout.addWidget(sidebar)

        
        
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = pointofsale()
    window.show()
    sys.exit(app.exec_())