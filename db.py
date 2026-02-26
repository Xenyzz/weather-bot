import sqlite3

# +-----------+       +-----------+       +--------------+
# |  users    |       |  cities   |       |  user_cities |
# +-----------+       +-----------+       +--------------+
# | user_id PK|<----+ | city_id PK|<--+   | user_id PK,FK|
# | name      |       | city_name |       | city_id PK,FK|
# +-----------+       +-----------+       +--------------+

conn = sqlite3.connect("user_data.db")
cursor = conn.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS users(
    user_id INTEGER PRIMARY KEY,
    name TEXT NOT NULL
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS cities(
    city_id INTEGER PRIMARY KEY AUTOINCREMENT,
    city_name TEXT UNIQUE NOT NULL
);
""")

cursor.execute("""
CREATE TABLE IF NOT EXISTS user_cities(
    city_id INTEGER,
    user_id INTEGER,
    PRIMARY KEY(user_id, city_id),
    FOREIGN KEY(user_id) REFERENCES users(user_id),
    FOREIGN KEY(city_id) REFERENCES cities(city_id)
);
""")

conn.commit()
conn.close()


def sqlite_conn(func):
    def wrapper(*args, **kwargs):
        with sqlite3.connect("user_data.db") as conn:
            cursor = conn.cursor()
            return func(cursor=cursor, *args, **kwargs)
    return wrapper


@sqlite_conn
def link_user_and_city(*, cursor, city: str, user_id: int, user_name: str) -> None:
    cursor.execute("INSERT OR IGNORE INTO users (user_id, name) VALUES (?, ?)", (user_id, user_name))
    cursor.execute("INSERT OR IGNORE INTO cities (city_name) VALUES (?)", (city,))
    cursor.execute("SELECT city_id FROM cities WHERE city_name = ?", (city,))
    city_id = cursor.fetchone()[0]
    cursor.execute("INSERT OR IGNORE INTO user_cities (user_id, city_id) VALUES (?, ?)", (user_id, city_id))


@sqlite_conn
def unlink_user_and_city(*, cursor, city: str, user_id: str) -> bool:
    try:
        cursor.execute("SELECT city_id FROM cities WHERE city_name = ?", (city,))
        city_id = cursor.fetchone()[0]
        cursor.execute("DELETE FROM user_cities WHERE user_id = ? and city_id = ?", (user_id, city_id))
        return True
    except:
        return False


@sqlite_conn
def print_users_cities(*, cursor, user_id: int):
    cursor.execute("SELECT city_id FROM user_cities WHERE user_id = ?", (user_id,))
    city_id_list = cursor.fetchall()
    city_name_list = []
    for city in city_id_list:
        cursor.execute("SELECT city_name FROM cities WHERE city_id = ?", (city))
        city_name = cursor.fetchone()[0]
        city_name_list.append(city_name)
    return city_name_list
