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
                parent_id INTEGER DEFAULT 0,
                FOREIGN KEY (parent_id) REFERENCES category(category_id))
        """)
        
        c.execute("""
            CREATE TABLE IF NOT EXISTS product (
                product_id INTEGER PRIMARY KEY AUTOINCREMENT,
                name TEXT NOT NULL,
                sku TEXT,
                category_id INTEGER,
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
            (name, sku, category_id, unit, price, cost_price, tax_rate, reorder_level, is_active, description)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """, product_data)
        conn.commit()
        conn.close()
    
    