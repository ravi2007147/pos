import sys 
from PyQt5.QtCore import Qt
import datetime
from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QTextEdit, QComboBox, QSpinBox, QDoubleSpinBox,
    QPushButton, QVBoxLayout, QHBoxLayout, QGridLayout, QFileDialog, QMessageBox,QHeaderView,QMdiArea,QMdiSubWindow
    ,QCompleter, QTableWidget, QTableWidgetItem,QApplication, QFrame,QLabel, QWidget, QMainWindow, QVBoxLayout, 
    QHBoxLayout, QPushButton,QLineEdit,QMdiSubWindow, QMessageBox,QCheckBox,QInputDialog)

from posdatabase import database
from reportlab.lib.pagesizes import letter
from reportlab.pdfgen import canvas
        
SWITCH_STYLE = """
    QCheckBox::indicator {
        width: 40px;
        height: 20px;
    }
    QCheckBox::indicator:unchecked {
        border-radius: 10px;
        background-color: #ccc;
        position: relative;
    }
    QCheckBox::indicator:unchecked::before {
        content: '';
        position: absolute;
        width: 18px;
        height: 18px;
        border-radius: 9px;
        background-color: white;
        margin: 1px;
    }
    QCheckBox::indicator:checked {
        border-radius: 10px;
        background-color: #4caf50;
        position: relative;
    }
    QCheckBox::indicator:checked::before {
        content: '';
        position: absolute;
        width: 18px;
        height: 18px;
        border-radius: 9px;
        background-color: white;
        margin: 1px 0 1px 21px;
    }
"""


LIGHT_THEME = """
    QWidget {
        font-family: 'Segoe UI';
        font-size: 14px;
        color: #000000;
        background-color: #f8f9fa;
    }
    QFrame#sidebar {
        background-color: #e9ecef;
        border-right: 1px solid #ccc;
    }
    QPushButton {
        background-color: #ffffff;
        border: 1px solid #ccc;
        padding: 10px;
        border-radius: 8px;
        font-weight: bold;
        color: #000000;
    }
    QPushButton:hover {
        background-color: #dee2e6;
    }
    QTableWidget {
        background-color: #ffffff;
        border: none;
        gridline-color: #ccc;
    }
    QHeaderView::section {
        background-color: #f1f3f5;
        padding: 5px;
        border: none;
        font-weight: bold;
        color: #000000;
    }
    QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox, QTextEdit {
        background-color: #ffffff;
        border: 1px solid #ccc;
        border-radius: 6px;
        padding: 5px;
        color: #000000;
    }
    QLabel {
        color: #000000;
    }
    QTableWidget QLineEdit {
    background-color: #ffffff;
    color: #000000;
    border: 1px solid #ccc;
    border-radius: 4px;
    padding: 4px;
}
QTableWidget QLineEdit:focus {
    border: 1px solid #0078d7;
}

"""

DARK_THEME ="""
    QWidget {
        font-family: 'Segoe UI';
        font-size: 14px;
        color: #f0f0f0;
        background-color: #121212;
    }
    QFrame#sidebar {
        background-color: #1e1e1e;
        border-right: 1px solid #333;
    }
    QPushButton {
        background-color: #2d2d2d;
        border: none;
        padding: 10px;
        border-radius: 8px;
        font-weight: bold;
        color: #f0f0f0;
    }
    QPushButton:hover {
        background-color: #3a3a3a;
    }
    QTableWidget {
        background-color: #1a1a1a;
        border: none;
        gridline-color: #333;
    }
    QHeaderView::section {
        background-color: #2a2a2a;
        padding: 5px;
        border: none;
        font-weight: bold;
        color: #f0f0f0;
    }
    QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox, QTextEdit {
        background-color: #1e1e1e;
        border: 1px solid #333;
        border-radius: 6px;
        padding: 5px;
        color: #f0f0f0;
    }
    QLabel {
        color: #ffffff;
    }
    QTableWidget QLineEdit {
            background-color: #1e1e1e;
            color: #f0f0f0;
            border: 1px solid #333;
            border-radius: 4px;
            padding: 4px;
        }
        QTableWidget QLineEdit:focus {
            border: 1px solid #5e81ac;
        }

"""


class pos_system(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("POS System")
        self.showMaximized()  
        self.current_theme = "dark"
        QApplication.instance().setStyleSheet(DARK_THEME)
        self.db = database()
        self.db.initialize_db()
        widget = QWidget()
        
       

        main_widget = QWidget()
        self.setCentralWidget(main_widget)

        self.dashboard_layout = QHBoxLayout()
        main_widget.setLayout(self.dashboard_layout)

        self.mdi_area = QMdiArea()
        self.mdi_area.setViewMode(QMdiArea.SubWindowView)
        self.mdi_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.mdi_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)

        sidebar = QFrame()
        sidebar.setFrameShape(QFrame.StyledPanel)
        sidebar.setFixedWidth(200)

        sidebar_layout = QVBoxLayout()
        sidebar_layout.setAlignment(Qt.AlignTop)
        sidebar.setLayout(sidebar_layout)
        sidebar_layout.setContentsMargins(10, 30, 10, 10)
        sidebar_layout.setSpacing(15)
        
        theme_btn = QPushButton("Toggle Theme")
        theme_btn.clicked.connect(self.toggle_theme)
        sidebar_layout.addWidget(theme_btn)

        Button = QPushButton("Dashboard")
        Button.setFixedHeight(50)
        Button.setStyleSheet("font-size: 14px; font-weight: bold;")
        sidebar_layout.addWidget(Button)

        Button1 = QPushButton("Product List")
        Button1.setFixedHeight(50)
        Button1.setStyleSheet("font-size: 14px; font-weight: bold;")
        Button1.clicked.connect(self.open_product_list)
        sidebar_layout.addWidget(Button1)

        Button2 = QPushButton("Point of sale")
        Button2.setFixedHeight(50)
        Button2.setStyleSheet("font-size: 14px; font-weight: bold;")
        Button2.clicked.connect(self.open_sales)
        sidebar_layout.addWidget(Button2)

        Button3 = QPushButton("Sales report")
        Button3.setFixedHeight(50)
        Button3.setStyleSheet("font-size: 14px; font-weight: bold;")
        Button3.clicked.connect(self.open_sales_report)
        sidebar_layout.addWidget(Button3)

        self.shop_name = "My Shop"   # default shop name

        shop_btn = QPushButton("Set Shop Name")
        shop_btn.setFixedHeight(50)
        shop_btn.setStyleSheet("font-size: 14px; font-weight: bold;")
        shop_btn.clicked.connect(self.set_shop_name)
        sidebar_layout.addWidget(shop_btn)


        self.dashboard_layout.addWidget(sidebar)
        self.dashboard_layout.addWidget(self.mdi_area)

# ===================================================================
        
        main_dashboard = QFrame()
        main_dashboard.setFrameShape(QFrame.StyledPanel)

        # This is the layout for main content
        content_layout = QVBoxLayout()
        content_layout.setAlignment(Qt.AlignTop)
        content_layout.setContentsMargins(20, 20, 20, 20)

        # ------------------------
        # Your top row (Sales & Inventory)
        top_row = QHBoxLayout()
        top_row.addStretch()

        button_style = """
        QPushButton {
            font-size: 16px;
            font-weight: bold;
        }
        """ 

        sales_box = QPushButton("Sales")
        sales_box.setFixedSize(200, 100)
        sales_box.setStyleSheet(button_style)
        top_row.addWidget(sales_box)
        top_row.addSpacing(40)

        inventory_box = QPushButton("Inventory")
        inventory_box.clicked.connect(self.open_inventory)
        inventory_box.setStyleSheet(button_style) 
        inventory_box.setFixedSize(200, 100)
        top_row.addWidget(inventory_box)

        top_row.addStretch()
        content_layout.addLayout(top_row)

        # ------------------------
        # Your bottom row (Top Products & Recent Sales)
        bottom_row = QHBoxLayout()
        bottom_row.addStretch()

        top_products_btn = QPushButton("Top Products")
        top_products_btn.setFixedSize(200, 100)
        top_products_btn.setStyleSheet(button_style)
        bottom_row.addWidget(top_products_btn)
        bottom_row.addSpacing(40)

        recent_sales_btn = QPushButton("Recent Sales")
        recent_sales_btn.setFixedSize(200, 100)
        recent_sales_btn.setStyleSheet(button_style)
        bottom_row.addWidget(recent_sales_btn)

        bottom_row.addStretch()
        content_layout.addLayout(bottom_row)

        # ------------------------
        # Footer
        footer_label = QLabel("Made by Himanshu")
        footer_label.setAlignment(Qt.AlignRight | Qt.AlignBottom)
        footer_label.setStyleSheet("""
            QLabel {
                color: #FFD700;  /* Gold */
                font-family: 'Segoe Script';
                font-size: 14px;
                font-style: italic;
                padding: 5px;
            }
        """)

        # Final wrapper so footer stays pinned
        wrapper_layout = QVBoxLayout()
        wrapper_layout.addLayout(content_layout)
        wrapper_layout.addStretch()
        wrapper_layout.addWidget(footer_label)

        main_dashboard.setLayout(wrapper_layout)
        self.dashboard_layout.addWidget(main_dashboard)





    def open_product_list(self):
        self.product_window = ProductListWindow()
        self.product_window.show()

    def open_sales_report(self):
        self.sales_report_window = SalesReportWindow()
        self.sales_report_window.show()

    def open_inventory(self):
        self.inventory_window = InventoryWindow()
        self.inventory_window.show()
        
    def open_sales(self):
        sub = ConfirmCloseSubWindow()   
        sub.setWindowTitle("Sales")
        sub.setWidget(SalesWindow())
        sub.setMinimumSize(600, 400)
        self.mdi_area.addSubWindow(sub)
        sub.show()
    def toggle_theme(self):
        if self.current_theme == "dark":
            QApplication.instance().setStyleSheet(LIGHT_THEME)
            self.current_theme = "light"
        else:
            QApplication.instance().setStyleSheet(DARK_THEME)
            self.current_theme = "dark"

    def set_shop_name(self):
        text, ok = QInputDialog.getText(self, "Shop Name", "Enter your shop name:", QLineEdit.Normal, self.shop_name)
        if ok and text.strip():
            self.shop_name = text.strip()
            QMessageBox.information(self, "Shop Name Set", f"Shop name updated to: {self.shop_name}")

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
        add_button.clicked.connect(self.open_add_product)
        add_button.setFixedWidth(120)
        main_layout.addWidget(add_button, alignment=Qt.AlignRight)

        self.table_placeholder = QLabel("\n\n[ Product Table Will Be Displayed Here ]\n")
        self.table_placeholder.setStyleSheet("border: 1px solid gray; color: gray;")
        self.table_placeholder.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.table_placeholder, stretch=1)

    def search_products(self):
        search_text = self.search_input.text()
        self.table_placeholder.setText(f"Searching for: {search_text}")
        
    def open_add_product(self):
        self.add_product_window = AddProductForm()
        self.add_product_window.show()

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
        self.resize(1000, 600)

        layout = QVBoxLayout()
        self.setLayout(layout)

        title = QLabel("Sales Report")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 20px; font-weight: bold;")
        layout.addWidget(title)

        # 🔎 Search by phone
        search_layout = QHBoxLayout()
        search_layout.addWidget(QLabel("Customer Phone:"))
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Enter phone to search...")
        search_layout.addWidget(self.search_input)

        search_btn = QPushButton("Search")
        search_btn.clicked.connect(self.load_sales_history)
        search_layout.addWidget(search_btn)

        layout.addLayout(search_layout)

        # 📋 Table for history
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "Sale ID", "Phone", "Date", "Product", "Quantity", "Total"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.table, stretch=1)

        self.db = database()
        self.load_sales_history()  # load all initially

    def load_sales_history(self):
        phone = self.search_input.text().strip()
        sales = self.db.get_sales_history(phone if phone else None)

        self.table.setRowCount(len(sales))
        for row, (sale_id, cust_id, phone, total, sale_date, product_name, qty, price) in enumerate(sales):
            self.table.setItem(row, 0, QTableWidgetItem(str(sale_id)))
            self.table.setItem(row, 1, QTableWidgetItem(phone or ""))
            self.table.setItem(row, 2, QTableWidgetItem(sale_date))
            self.table.setItem(row, 3, QTableWidgetItem(product_name))
            self.table.setItem(row, 4, QTableWidgetItem(str(qty)))
            self.table.setItem(row, 5, QTableWidgetItem(f"{qty * price:.2f}"))

        
class InventoryWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Inventory")
        self.resize(600, 400)
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        title = QLabel("Inventory List")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 20px; font-weight: bold;")
        layout.addWidget(title)
        
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Search product by name...")
        self.current_page = 1
        self.items_per_page = 5

        self.search_input.textChanged.connect(self.search_inventory)

        search_layout.addWidget(QLabel("Search:"))
        search_layout.addWidget(self.search_input)

        layout.addLayout(search_layout)
        
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels(["Product ID", "Name", "Quantity", "Price"])
        self.table.horizontalHeader().setStretchLastSection(True)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.table, stretch=1)

        pagination_layout = QHBoxLayout()
        pagination_layout.addStretch()  

        self.prev_btn = QPushButton("Previous")
        self.next_btn = QPushButton("Next")
        self.page_label = QLabel("Page 1")
        self.page_label.setAlignment(Qt.AlignCenter)

        self.prev_btn.clicked.connect(self.go_to_previous_page)
        self.next_btn.clicked.connect(self.go_to_next_page)

        pagination_layout.addWidget(self.prev_btn)
        pagination_layout.addWidget(self.page_label)
        pagination_layout.addWidget(self.next_btn)

        layout.addLayout(pagination_layout)
        
        self.load_inventory()
    
    def search_inventory(self):
        query = self.search_input.text().lower()
        filtered_products = [
            product for product in self.all_products
            if query in product[1].lower()
        ]

        self.display_inventory(filtered_products)

    def load_inventory(self):
        db = database()
        self.all_products = db.get_inventory() 
        self.display_inventory(self.all_products)
        
    def display_inventory(self, products):
        self.filtered_products = products
        total_items = len(products)
        total_pages = max(1, (total_items + self.items_per_page - 1) // self.items_per_page)
        self.current_page = min(max(1, self.current_page), total_pages)

        start = (self.current_page - 1) * self.items_per_page
        end = start + self.items_per_page
        page_items = products[start:end]

        self.table.setRowCount(len(page_items))
        for row_idx, (product_id, name, qty, price) in enumerate(page_items):
            self.table.setItem(row_idx, 0, QTableWidgetItem(str(product_id)))
            self.table.setItem(row_idx, 1, QTableWidgetItem(name))
            self.table.setItem(row_idx, 2, QTableWidgetItem(str(qty)))
            self.table.setItem(row_idx, 3, QTableWidgetItem(f"{price:.2f}"))

        self.page_label.setText(f"Page {self.current_page} of {total_pages}")
        self.prev_btn.setEnabled(self.current_page > 1)
        self.next_btn.setEnabled(self.current_page < total_pages)

    def go_to_previous_page(self):
        if self.current_page > 1:
            self.current_page -= 1
            self.display_inventory(self.filtered_products)

    def go_to_next_page(self):
        total_pages = (len(self.filtered_products) + self.items_per_page - 1) // self.items_per_page
        if self.current_page < total_pages:
            self.current_page += 1
            self.display_inventory(self.filtered_products)

class AddProductForm(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Add Product")
        self.setGeometry(200, 200, 500, 500)

        layout = QVBoxLayout()
        form_layout = QGridLayout()

        self.name_input = QLineEdit()
        self.sku_input = QLineEdit()
        self.category_input = QComboBox() 
        self.category_input.addItem("silk")
        self.category_input.addItem("cotton")
        self.category_input.addItem("synthetic")
        self.category_input.addItem("original")
        self.category_input.addItem("replica")
        self.category_input.addItem("Men")
        self.category_input.addItem("Women")
        self.category_input.addItem("kid")
        
        self.unit_input = QLineEdit()
        self.price_input = QDoubleSpinBox()
        self.price_input.setMaximum(1000000)

        self.cost_price_input = QDoubleSpinBox()
        self.cost_price_input.setMaximum(1000000)

        self.tax_input = QDoubleSpinBox()
        self.tax_input.setSuffix(" %")
        self.tax_input.setMaximum(100)

        self.reorder_input = QSpinBox()
        self.reorder_input.setMaximum(10000)

        self.is_active_input = QComboBox()
        self.is_active_input.addItems(["Yes", "No"])

        self.description_input = QTextEdit()

        form_layout.addWidget(QLabel("Name"), 0, 0)
        form_layout.addWidget(self.name_input, 0, 1)

        form_layout.addWidget(QLabel("SKU"), 1, 0)
        form_layout.addWidget(self.sku_input, 1, 1)

        form_layout.addWidget(QLabel("Category"), 2, 0)
        form_layout.addWidget(self.category_input, 2, 1)

        form_layout.addWidget(QLabel("Unit"), 3, 0)
        form_layout.addWidget(self.unit_input, 3, 1)

        form_layout.addWidget(QLabel("Price"), 4, 0)
        form_layout.addWidget(self.price_input, 4, 1)

        form_layout.addWidget(QLabel("Cost Price"), 5, 0)
        form_layout.addWidget(self.cost_price_input, 5, 1)

        form_layout.addWidget(QLabel("Tax Rate"), 6, 0)
        form_layout.addWidget(self.tax_input, 6, 1)

        form_layout.addWidget(QLabel("Reorder Level"), 7, 0)
        form_layout.addWidget(self.reorder_input, 7, 1)

        form_layout.addWidget(QLabel("Is Active"), 8, 0)
        form_layout.addWidget(self.is_active_input, 8, 1)

        form_layout.addWidget(QLabel("Description"), 10, 0)
        form_layout.addWidget(self.description_input, 10, 1, 2, 2)

        layout.addLayout(form_layout)

        self.submit_btn = QPushButton("Add Product")
        self.submit_btn.clicked.connect(self.save_product)
        layout.addWidget(self.submit_btn)

        self.setLayout(layout)
        
    def validate_fields(self):
        if not self.name_input.text().strip():
            QMessageBox.warning(self, "Validation Error", "Name is required.")
            return False

        if not self.sku_input.text().strip():
            QMessageBox.warning(self, "Validation Error", "SKU is required.")
            return False

        if self.category_input.currentText().strip() == "":
            QMessageBox.warning(self, "Validation Error", "Category must be selected.")
            return False

        if not self.unit_input.text().strip():
            QMessageBox.warning(self, "Validation Error", "Unit is required.")
            return False

        if self.price_input.value() == 0:
            QMessageBox.warning(self, "Validation Error", "Price must be greater than 0.")
            return False

        if self.cost_price_input.value() == 0:
            QMessageBox.warning(self, "Validation Error", "Cost Price must be greater than 0.")
            return False

        if self.tax_input.value() == 0:
            QMessageBox.warning(self, "Validation Error", "Tax Rate must be greater than 0.")
            return False

        if self.reorder_input.value() == 0:
            QMessageBox.warning(self, "Validation Error", "Reorder Level must be greater than 0.")
            return False

        if not self.description_input.toPlainText().strip():
            QMessageBox.warning(self, "Validation Error", "Description is required.")
            return False

        return True
        
    def save_product(self):
        if not self.validate_fields():
            return  
        name = self.name_input.text()
        sku = self.sku_input.text()
        category_id = self.category_input.currentData()
        unit = self.unit_input.text()
        price = self.price_input.value()
        cost_price = self.cost_price_input.value()
        tax_rate = self.tax_input.value()
        reorder_level = self.reorder_input.value()
        is_active = 1 if self.is_active_input.currentText() == "Yes" else 0
        description = self.description_input.toPlainText()

        QMessageBox.information(self, "Product Info", f"Saved: {name}, Price: {price}, Tax: {tax_rate}%")

        db = database()
        db.save_product((name, sku, unit, price, cost_price, tax_rate, reorder_level, is_active, description))

        QMessageBox.information(self, "Success", "Product saved successfully!")
        self.close()

class SalesWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.db = database()
        layout = QVBoxLayout()
        self.setLayout(layout)

        title = QLabel("Sales Entry")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(title)

        self.table = QTableWidget(0, 4)  
        self.table.setHorizontalHeaderLabels(["Product", "Quantity", "Price", "Total"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.table)

        self.table.cellChanged.connect(self.handle_cell_change)

        self.product_names = [p[1] for p in self.db.get_inventory()]
        self.completer = QCompleter(self.product_names)
        self.completer.setCaseSensitivity(Qt.CaseInsensitive)

        self.add_product_row()

        add_row_btn = QPushButton("Add Product Row")
        add_row_btn.clicked.connect(self.add_product_row)
        layout.addWidget(add_row_btn)

        self.total_label = QLabel("Total: ₹0.00")
        self.total_label.setAlignment(Qt.AlignRight)
        layout.addWidget(self.total_label)

        phone_layout = QHBoxLayout()
        phone_label = QLabel("Phone No:")
        phone_layout.addWidget(phone_label)
        self.phone_input = QLineEdit()
        self.phone_input.setPlaceholderText("Enter Phone Number")
        phone_layout.addWidget(self.phone_input)
        phone_layout.addStretch()
        layout.addLayout(phone_layout)

        submit_button = QPushButton("Submit Sale")
        submit_button.clicked.connect(self.submit_sale)
        layout.addWidget(submit_button, alignment=Qt.AlignRight)

    def add_product_row(self):
        row = self.table.rowCount()
        self.table.insertRow(row)

        product_input = QLineEdit()
        product_input.setCompleter(self.completer)
        product_input.textChanged.connect(lambda text, r=row: self.product_name_changed(text, r))
        self.table.setCellWidget(row, 0, product_input)

    def product_name_changed(self, text, row):
        if text:
            product = self.db.get_product_by_name(text)
            if product:
                product_id, price, quantity = product
                self.table.setItem(row, 2, QTableWidgetItem(f"{price:.2f}"))
                self.update_total()

    def handle_cell_change(self, row, column):
        if column == 0:   
            product_name_item = self.table.item(row, 0)
            if product_name_item:
                product_name = product_name_item.text()
                product = self.db.get_product_by_name(product_name)
                if product:
                    product_id, price, quantity = product
                    self.table.setItem(row, 2, QTableWidgetItem(f"{price:.2f}"))
                    qty_item = self.table.item(row, 1)
                    if qty_item and qty_item.text().isdigit():
                        qty = int(qty_item.text())
                        total = qty * price
                        self.table.setItem(row, 3, QTableWidgetItem(f"{total:.2f}"))
        elif column == 1:  
            qty_item = self.table.item(row, 1)
            price_item = self.table.item(row, 2)
            if qty_item and price_item:
                try:
                    qty = float(qty_item.text())
                    price = float(price_item.text())
                    total = qty * price
                    self.table.setItem(row, 3, QTableWidgetItem(f"{total:.2f}"))
                except:
                    pass

        self.update_total()

    def update_total(self):
        total = 0.0
        for row in range(self.table.rowCount()):
            try:
                total_item = self.table.item(row, 3)
                if total_item:
                    total += float(total_item.text())
            except:
                continue
        self.total_label.setText(f"Total: ₹{total:.2f}")

    def submit_sale(self):
        phone = self.phone_input.text().strip()
        total_amount = 0.0
        items = []

        for row in range(self.table.rowCount()):
            try:
                product_widget = self.table.cellWidget(row, 0)
                product_name = product_widget.text().strip() if product_widget else ""

                qty_item = self.table.item(row, 1)
                price_item = self.table.item(row, 2)

                if product_name and qty_item and price_item:
                    qty = int(qty_item.text())
                    price = float(price_item.text())
                    total_amount += qty * price
                    # store product_id instead of just name
                    product = self.db.get_product_by_name(product_name)
                    if product:
                        product_id = product[0]
                        items.append((product_id, qty, price))
            except:
                continue

        if not items:
            QMessageBox.warning(self, "No Products", "No valid products added.")
            return

        # save to database
        sale_id = self.db.save_sale(customer_id=None, phone=phone, items=items, total=total_amount)

        # show receipt window
        # Pass the shop name from parent window
        main_window = self.parentWidget().window()  # gets pos_system
        shop_name = getattr(main_window, "shop_name", "My Shop")

        self.receipt_window = ReceiptWindow(
            sale_id, phone,
            [(self.db.get_product_name_by_id(pid), qty, price) for pid, qty, price in items],
            total_amount, shop_name
        )
        self.receipt_window.show()
        self.close()

        

class ConfirmCloseSubWindow(QMdiSubWindow):
    def closeEvent(self, event):
        reply = QMessageBox.question(
            self,
            "Confirm Close",
            "Are you sure you want to close this window?",
            QMessageBox.Yes | QMessageBox.No
        )
        if reply == QMessageBox.Yes:
            event.accept()
        else:
            event.ignore()
        
class ReceiptWindow(QWidget):
    def __init__(self, sale_id, phone, items, total_amount, shop_name="My Shop"):
        super().__init__()
        self.sale_id = sale_id
        self.phone = phone
        self.items = items
        self.total_amount = total_amount
        self.shop_name = shop_name


        layout = QVBoxLayout()
        self.setLayout(layout)

        shop_label = QLabel(self.shop_name)
        shop_label.setAlignment(Qt.AlignCenter)
        shop_label.setStyleSheet("font-size: 20px; font-weight: bold;")
        layout.addWidget(shop_label)


        # Title
        title = QLabel("Receipt")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 18px; font-weight: bold;")
        layout.addWidget(title)

        # Invoice No
        invoice_label = QLabel(f"Invoice No: {self.sale_id}")
        layout.addWidget(invoice_label)

        # Date + Phone
        date_label = QLabel(f"Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        layout.addWidget(date_label)

        phone_label = QLabel(f"Customer Phone: {self.phone}")
        layout.addWidget(phone_label)

        # Items
        layout.addWidget(QLabel("Items:"))
        table = QTableWidget(len(self.items), 4)
        table.setHorizontalHeaderLabels(["Product", "Qty", "Price", "Total"])
        table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        for row, (name, qty, price) in enumerate(self.items):
            table.setItem(row, 0, QTableWidgetItem(name))
            table.setItem(row, 1, QTableWidgetItem(str(qty)))
            table.setItem(row, 2, QTableWidgetItem(f"{price:.2f}"))
            table.setItem(row, 3, QTableWidgetItem(f"{qty * price:.2f}"))

        layout.addWidget(table)

        # Total
        total_label = QLabel(f"Grand Total: ₹{self.total_amount:.2f}")
        total_label.setAlignment(Qt.AlignRight)
        total_label.setStyleSheet("font-size: 14px; font-weight: bold;")
        layout.addWidget(total_label)

        # Save PDF Button
        save_pdf_btn = QPushButton("Save as PDF")
        save_pdf_btn.clicked.connect(self.save_as_pdf)
        layout.addWidget(save_pdf_btn, alignment=Qt.AlignCenter)

    def save_as_pdf(self):
        file_path, _ = QFileDialog.getSaveFileName(
            self, "Save Receipt as PDF",
            f"receipt_{self.sale_id}.pdf", "PDF Files (*.pdf)"
        )
        if not file_path:
            return

        c = canvas.Canvas(file_path, pagesize=letter)
        c.setFont("Helvetica", 12)

        c.drawString(200, 750, "Sale Receipt")
        c.drawString(50, 730, f"Invoice No: {self.sale_id}")
        c.drawString(50, 715, f"Date: {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        c.drawString(50, 700, f"Customer Phone: {self.phone}")

        c.drawString(50, 670, "Items:")
        y = 650
        for name, qty, price in self.items:
            c.drawString(50, y, f"{name} (x{qty}) - ₹{price:.2f} = ₹{qty*price:.2f}")
            y -= 15

        c.drawString(50, y - 20, f"Grand Total: ₹{self.total_amount:.2f}")
        c.save()
        QMessageBox.information(self, "Saved", f"Receipt saved as {file_path}")
        c.setFont("Helvetica-Bold", 14)
        c.drawString(200, 770, self.shop_name)

        c.setFont("Helvetica", 12)
        c.drawString(200, 750, "Sale Receipt")



if __name__ == "__main__":
    app = QApplication(sys.argv)
    # Add this at the bottom before sys.exit(app.exec_())
    app.setStyleSheet("""
        QWidget {
            font-family: 'Segoe UI';
            font-size: 14px;
            color: #f0f0f0;
            background-color: #121212;
        }
        QFrame#sidebar {
            background-color: #1e1e1e;
            border-right: 1px solid #333;
        }
        QPushButton {
            background-color: #2d2d2d;
            border: none;
            padding: 10px;
            border-radius: 8px;
            font-weight: bold;
            color: #f0f0f0;
        }
        QPushButton:hover {
            background-color: #3a3a3a;
        }
        QPushButton:pressed {
            background-color: #505050;
        }
        QTableWidget {
            background-color: #1a1a1a;
            border: none;
            gridline-color: #333;
        }
        QHeaderView::section {
            background-color: #2a2a2a;
            padding: 5px;
            border: none;
            font-weight: bold;
            color: #f0f0f0;
        }
        QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox, QTextEdit {
            background-color: #1e1e1e;
            border: 1px solid #333;
            border-radius: 6px;
            padding: 5px;
            color: #f0f0f0;
        }
        QLineEdit:focus, QComboBox:focus, QSpinBox:focus, QDoubleSpinBox:focus, QTextEdit:focus {
            border: 1px solid #5e81ac;
        }
        QLabel {
            color: #ffffff;
        }
    """)
    window = pos_system()
    window.show()
    sys.exit(app.exec_())