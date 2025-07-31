import sys 
from PyQt5.QtWidgets import(QApplication, QFrame,QLabel, QWidget, QMainWindow, QVBoxLayout, QHBoxLayout,
    QPushButton,QLineEdit)
from PyQt5.QtWidgets import (
    QWidget, QLabel, QLineEdit, QTextEdit, QComboBox, QSpinBox, QDoubleSpinBox,
    QPushButton, QVBoxLayout, QHBoxLayout, QGridLayout, QFileDialog, QMessageBox,QHeaderView
)
from PyQt5.QtCore import Qt
import datetime
from PyQt5.QtWidgets import QTableWidget, QTableWidgetItem

from posdatabase import database


class pos_system(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("POS System")
        self.showMaximized()  
        self.db = database()
        self.db.initialize_db()
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
        Button3.clicked.connect(self.open_sales_report)
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
        inventory_box.clicked.connect(self.open_inventory)
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

    def open_sales_report(self):
        self.sales_report_window = SalesReportWindow()
        self.sales_report_window.show()

    def open_inventory(self):
        self.inventory_window = InventoryWindow()
        self.inventory_window.show()


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

        
        main_layout = QHBoxLayout()
        self.setLayout(main_layout)

        sidebar = QFrame()
        sidebar.setFixedWidth(200)
        sidebar.setStyleSheet("background-color: #f0f0f0;")
        sidebar_layout = QVBoxLayout()
        sidebar.setLayout(sidebar_layout)

        label = QLabel("Sales Report")
        label.setStyleSheet("font-weight: bold; font-size: 16px;")
        label.setAlignment(Qt.AlignCenter)
        sidebar_layout.addWidget(label)

        report_btn = QPushButton("Sale Report")
        summary_btn = QPushButton("Sales Summary")
        report_btn.setFixedHeight(40)
        summary_btn.setFixedHeight(40)

        sidebar_layout.addWidget(report_btn)
        sidebar_layout.addWidget(summary_btn)
        sidebar_layout.addStretch()

        main_layout.addWidget(sidebar)

        content = QFrame()
        content_layout = QVBoxLayout()
        content.setLayout(content_layout)

        title = QLabel("Sales Report")
        title.setAlignment(Qt.AlignCenter)
        title.setStyleSheet("font-size: 20px; font-weight: bold;")
        content_layout.addWidget(title)

        date_layout = QHBoxLayout()
        date_label = QLabel("Date Range:")
        from_input = QLineEdit()
        from_input.setPlaceholderText("From")
        from_input.setFixedWidth(100)

        to_input = QLineEdit()
        to_input.setPlaceholderText("To")
        to_input.setFixedWidth(100)

        date_layout.addWidget(date_label)
        date_layout.addSpacing(10)
        date_layout.addWidget(from_input)
        date_layout.addSpacing(10)
        date_layout.addWidget(to_input)
        date_layout.addStretch()

        content_layout.addLayout(date_layout)

        # Chart & Summary Placeholder
        chart_box = QLabel("\n\n[ Sales Chart Will Be Shown Here ]\n")
        chart_box.setStyleSheet("border: 1px solid gray; color: gray;")
        chart_box.setAlignment(Qt.AlignCenter)
        chart_box.setFixedHeight(300)
        content_layout.addWidget(chart_box)

        summary = QLabel("[ Report Summary / Notes ]")
        summary.setStyleSheet("color: gray;")
        summary.setAlignment(Qt.AlignLeft)
        content_layout.addWidget(summary)

        main_layout.addWidget(content, stretch=1)
        
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
        self.items_per_page = 10

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

        # form_layout.addWidget(QLabel("Image"), 9, 0)
        # form_layout.addWidget(self.image_url_input, 9, 1)
        # form_layout.addWidget(self.browse_button, 9, 2)

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
        
        
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = pos_system()
    window.show()
    sys.exit(app.exec_())