import sys
from PyQt5.QtWidgets import(QApplication, QFrame,QLabel, QWidget, QMainWindow, QVBoxLayout, QHBoxLayout,
    QPushButton,QLineEdit)
from PyQt5.QtCore import Qt


class pos_system(QMainWindow):
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
        Button1.clicked.connect(self.open_product_list)
        Button1.setFixedHeight(40)
        sidebar_layout.addWidget(Button1)

        Button2 = QPushButton("Point of sale")
        Button2.clicked.connect(self.open_point_of_sale)
        Button2.setFixedHeight(40)
        sidebar_layout.addWidget(Button2)

        Button3 = QPushButton("Sales report")
        Button3.setFixedHeight(40)
        sidebar_layout.addWidget(Button3)

        dashboard_layout.addWidget(sidebar)

# ===================================================================
                
        main_dashboard = QFrame()
        main_dashboard.setFrameShape(QFrame.StyledPanel)
        main_layout = QVBoxLayout()
        main_dashboard.setLayout(main_layout)

        
        title = QLabel("Dashboard")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 24px; font-weight: bold;")
        main_layout.addWidget(title)

    
        top_row = QHBoxLayout()
        top_row.addStretch()

        sales_box = QPushButton("Sales")
        sales_box.setFixedSize(200, 100)
        top_row.addWidget(sales_box)
        top_row.addSpacing(40)

        inventory_box = QPushButton("Inventory")
        inventory_box.setFixedSize(200, 100)
        top_row.addWidget(inventory_box)

        top_row.addStretch()
        main_layout.addLayout(top_row)


        bottom_row = QHBoxLayout()
        bottom_row.addStretch()

        top_products_btn = QPushButton("Top Products")
        top_products_btn.setFixedSize(200, 100)
        bottom_row.addWidget(top_products_btn)
        bottom_row.addSpacing(40)

        recent_sales_btn = QPushButton("Recent Sales")
        recent_sales_btn.setFixedSize(200, 100)
        bottom_row.addWidget(recent_sales_btn)

        bottom_row.addStretch()
        main_layout.addLayout(bottom_row)


        dashboard_layout.addWidget(main_dashboard)

    def open_product_list(self):
        self.product_window = ProductListWindow()
        self.product_window.show()

    def open_point_of_sale(self):
        self.pos_window = PointOfSaleWindow()
        self.pos_window.show()



class ProductListWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Product List")
        self.resize(800, 600)

        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        title = QLabel("Product List")
        title.setStyleSheet("font-size: 20px; font-weight: bold;")
        title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title)

        search_layout = QHBoxLayout()
        search_label = QLabel("Search:")
        search_label.setFixedWidth(50)
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Enter product name...")
        self.search_input.setFixedHeight(30)
        search_button = QPushButton("Search")
        search_button.setFixedHeight(30)
        search_button.clicked.connect(self.search_products)

        search_layout.addWidget(search_label)
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(search_button)
        main_layout.addLayout(search_layout)

        
        add_button = QPushButton("Add Product")
        add_button.setFixedWidth(120)
        main_layout.addWidget(add_button, alignment=Qt.AlignRight)

        
        self.table_placeholder = QLabel("\n\n[ Product Table Will Be Displayed Here ]\n")
        self.table_placeholder.setStyleSheet("border: 1px solid gray; color: gray;")
        self.table_placeholder.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.table_placeholder, stretch=1)

    def search_products(self):
        search_text = self.search_input.text()
        self.table_placeholder.setText(f"Searching for: {search_text}")

class PointOfSaleWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Point of Sale")
        self.resize(800, 600)

        main_layout = QVBoxLayout()
        self.setLayout(main_layout)

        
        title = QLabel("Point of Sale")
        title.setStyleSheet("font-size: 20px; font-weight: bold;")
        title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(title)

        
        cart_frame = QFrame()
        cart_frame.setStyleSheet("border: 1px solid gray;")
        cart_layout = QVBoxLayout()
        cart_frame.setLayout(cart_layout)

        cart_title = QLabel("Cart")
        cart_title.setStyleSheet("font-size: 16px; font-weight: bold;")
        cart_layout.addWidget(cart_title)

        customer_label = QLabel("Customer: ____________")
        total_label = QLabel("Total: ____________")
        cart_layout.addWidget(customer_label)
        cart_layout.addWidget(total_label)

        main_layout.addWidget(cart_frame)

        
        process_btn = QPushButton("Process Sale")
        process_btn.setFixedHeight(40)
        main_layout.addWidget(process_btn, alignment=Qt.AlignCenter)


class SalesReportWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Sales Report")
        self.resize(800, 600)

        layout = QVBoxLayout()
        self.setLayout(layout)

        
        title = QLabel("Sales Report")
        title.setStyleSheet("font-size: 20px; font-weight: bold;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        
      





        
        
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = pos_system()
    window.show()
    sys.exit(app.exec_())