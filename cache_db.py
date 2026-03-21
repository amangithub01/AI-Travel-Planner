import sqlite3

# This creates the file travel_cache.db in your main folder
conn = sqlite3.connect('travel_cache.db')
cursor = conn.cursor()

# Create the tables
cursor.execute('''
CREATE TABLE IF NOT EXISTS accommodations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT,
    location_city TEXT,
    price_per_night REAL,
    rating REAL,
    url TEXT
)
''')

cursor.execute('''
CREATE TABLE IF NOT EXISTS flights (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    airline TEXT,
    origin TEXT,
    destination TEXT,
    price REAL,
    url TEXT
)
''')

# Seed the database with mock data for Mumbai
cursor.execute("INSERT INTO accommodations (name, location_city, price_per_night, rating, url) VALUES ('Hotel Marine Plaza', 'Mumbai', 95.0, 8.2, 'https://hotelmarine.com')")
cursor.execute("INSERT INTO flights (airline, origin, destination, price, url) VALUES ('Indigo', 'BLR', 'Mumbai', 85.0, 'https://goindigo.in')")

conn.commit()
conn.close()
print("✅ Local database successfully created and seeded with Mumbai data!")
