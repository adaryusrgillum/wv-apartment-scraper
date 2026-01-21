"""Database module for WV Apartment Scraper"""
import sqlite3
import os
from datetime import datetime
from config import DB_NAME, DB_PATH

class ApartmentDatabase:
    def __init__(self):
        self.db_path = os.path.join(DB_PATH, DB_NAME)
        self.ensure_db_exists()
    
    def ensure_db_exists(self):
        os.makedirs(DB_PATH, exist_ok=True)
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        # Create listings table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS listings (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                external_id TEXT UNIQUE,
                source TEXT NOT NULL,
                url TEXT UNIQUE,
                address TEXT,
                city TEXT,
                state TEXT DEFAULT 'WV',
                zip_code TEXT,
                price INTEGER,
                beds REAL,
                baths REAL,
                sqft INTEGER,
                property_type TEXT,
                listing_date TEXT,
                scraped_date TEXT,
                image_url TEXT,
                description TEXT,
                is_active BOOLEAN DEFAULT 1
            )
        ''')
        
        # Create price history table
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS price_history (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                listing_id INTEGER,
                price INTEGER,
                recorded_date TEXT,
                FOREIGN KEY(listing_id) REFERENCES listings(id)
            )
        ''')
        
        conn.commit()
        conn.close()
    
    def insert_or_update_listing(self, listing_data):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        today = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        try:
            cursor.execute('SELECT id, price FROM listings WHERE url = ?', (listing_data['url'],))
            existing = cursor.fetchone()
            
            if existing:
                listing_id, old_price = existing
                if listing_data['price'] != old_price:
                    cursor.execute(
                        'UPDATE listings SET price = ?, scraped_date = ? WHERE id = ?',
                        (listing_data['price'], today, listing_id)
                    )
                    cursor.execute(
                        'INSERT INTO price_history (listing_id, price, recorded_date) VALUES (?, ?, ?)',
                        (listing_id, listing_data['price'], today)
                    )
            else:
                cursor.execute('''
                    INSERT INTO listings (external_id, source, url, address, city, price, beds, baths, scraped_date)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (
                    listing_data.get('external_id'),
                    listing_data.get('source'),
                    listing_data.get('url'),
                    listing_data.get('address'),
                    listing_data.get('city'),
                    listing_data.get('price'),
                    listing_data.get('beds'),
                    listing_data.get('baths'),
                    today
                ))
            
            conn.commit()
        except Exception as e:
            print(f'Database error: {e}')
        finally:
            conn.close()
    
    def get_all_listings(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        
        cursor.execute('SELECT * FROM listings WHERE is_active = 1')
        rows = cursor.fetchall()
        conn.close()
        
        return [dict(row) for row in rows]
