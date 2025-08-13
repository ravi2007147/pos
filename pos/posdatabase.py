import sqlite3

DB_NAME="pointOfSale.db"

class database():
    def __init__(self):
        super().__init__()
        
    def get_connection(self):
        return sqlite3.connect(DB_NAME)
    
    def initialize_db(self):
        conn = self.get_connection()
        c = conn.cursor()
        c.execute(""" 
    CREATE TABLE IF NOT EXISTS category (
        category_id INTEGER PRIMARY KEY AUTOINCREMENT,
        category_name TEXT NOT NULL,
        parent_id INTEGER DEFAULT 0
    )
""")

        
        c.execute("""
            CREATE TABLE IF NOT EXISTS product (
            product_id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            sku TEXT,
            unit TEXT,
            price REAL,
            cost_price REAL,
            tax_rate REAL,
            reorder_level INTEGER,
            is_active BOOLEAN DEFAULT 1,
            image_url TEXT,
            description TEXT,
            created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (category_id) REFERENCES category(category_id)
            )   

        """)
        
        c.execute(""" 
            CREATE TABLE IF NOT EXISTS category_mapping (
                product_id INTEGER,
                category_id INTEGER
            )
        """)

    
        conn.commit()
        conn.close()
        
    def save_product(self, product_data):
        conn = self.get_connection()
        c = conn.cursor()
        c.execute("""
            INSERT INTO product 
            (name, sku, unit, price, cost_price, tax_rate, reorder_level, is_active, description)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, product_data)
        conn.commit()
        conn.close()
        
        
    def get_inventory(self):
        conn = self.get_connection()
        c = conn.cursor()
        c.execute("""
            SELECT product_id, name, reorder_level, price FROM product
        """)
        rows = c.fetchall()
        conn.close()
        return rows

    def get_product_by_name(self, product_name):
        conn = self.get_connection()
        c = conn.cursor()
        c.execute("SELECT product_id, price, reorder_level FROM product WHERE name = ?", (product_name,))
        result = c.fetchone()
        conn.close()
        return result

    def update_product_quantity(self, product_id, quantity_sold):
        conn = self.get_connection()
        c = conn.cursor()
        c.execute("UPDATE product SET reorder_level = reorder_level - ? WHERE product_id = ?", (quantity_sold, product_id))
        conn.commit()
        conn.close()

    def save_sale(self, customer_id, phone, items, total):
        conn = self.get_connection()
        c = conn.cursor()

        # create table if not exists
        c.execute("""
            CREATE TABLE IF NOT EXISTS sales (
                sale_id INTEGER PRIMARY KEY AUTOINCREMENT,
                customer_id TEXT,
                phone TEXT,
                total_amount REAL,
                sale_date TEXT
            )
        """)
        c.execute("""
            CREATE TABLE IF NOT EXISTS sale_items (
                sale_id INTEGER,
                product_id INTEGER,
                quantity INTEGER,
                price REAL,
                FOREIGN KEY (sale_id) REFERENCES sales(sale_id)
            )
        """)

        # insert sale
        c.execute("INSERT INTO sales (customer_id, phone, total_amount, sale_date) VALUES (?, ?, ?, datetime('now'))",
                (customer_id, phone, total))
        sale_id = c.lastrowid

        # insert each item
        for product_id, qty, price in items:
            c.execute("INSERT INTO sale_items (sale_id, product_id, quantity, price) VALUES (?, ?, ?, ?)",
                    (sale_id, product_id, qty, price))
            self.update_product_quantity(product_id, qty)

        conn.commit()
        conn.close()

    def get_product_name_by_id(self, product_id):
        conn = self.get_connection()
        c = conn.cursor()
        c.execute("SELECT name FROM products WHERE id = ?", (product_id,))
        result = c.fetchone()
        conn.close()
        return result[0] if result else None

