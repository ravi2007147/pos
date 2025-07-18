import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
    QPushButton, QLabel, QFrame, QGridLayout
)
from PyQt5.QtCore import Qt


class DashboardUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Point of Sale Dashboard")
        self.setGeometry(100, 100, 800, 500)

        # Central widget and main layout
        central_widget = QWidget()
        main_layout = QHBoxLayout()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

        # Left Sidebar
        sidebar = QFrame()
        sidebar.setFrameShape(QFrame.StyledPanel)
        sidebar.setFixedWidth(200)
        sidebar_layout = QVBoxLayout()
        sidebar.setLayout(sidebar_layout)

        sidebar_label = QLabel("Dashboard")
        sidebar_label.setAlignment(Qt.AlignCenter)
        sidebar_label.setStyleSheet("font-weight: bold; font-size: 16px;")
        sidebar_layout.addWidget(sidebar_label)

        buttons = ["Dashboard", "Product List", "Point of Sale", "Sales Report"]
        for text in buttons:
            btn = QPushButton(text)
            btn.setFixedHeight(40)
            sidebar_layout.addWidget(btn)

        sidebar_layout.addStretch()

        # Main Dashboard Area
        dashboard_area = QWidget()
        dashboard_layout = QVBoxLayout()
        dashboard_area.setLayout(dashboard_layout)

        header = QLabel("Dashboard")
        header.setStyleSheet("font-size: 20px; font-weight: bold;")
        dashboard_layout.addWidget(header)

        grid = QGridLayout()
        dashboard_layout.addLayout(grid)

        # Four panels
        panels = {
            "Sales": (0, 0),
            "Inventory": (0, 1),
            "Top Products": (1, 0),
            "Recent Sales": (1, 1)
        }

        for title, pos in panels.items():
            panel = QFrame()
            panel.setFrameShape(QFrame.Panel)
            panel.setStyleSheet("background-color: #e0e0e0; padding: 15px;")
            panel_layout = QVBoxLayout()
            panel.setLayout(panel_layout)

            label = QLabel(title)
            label.setAlignment(Qt.AlignCenter)
            label.setStyleSheet("font-weight: bold; font-size: 14px;")
            panel_layout.addWidget(label)

            grid.addWidget(panel, *pos)

        # Add sidebar and main content to layout
        main_layout.addWidget(sidebar)
        main_layout.addWidget(dashboard_area)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DashboardUI()
    window.show()
    sys.exit(app.exec_())
