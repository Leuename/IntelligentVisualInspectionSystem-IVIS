"""
- CaptureDB: Main SQLite database handler.
Functions/Methods:
- CaptureDB.__init__: Initializes thread locks, state variables, and creates/verifies the database schema.
- CaptureDB.init_db: Configures SQLite pragmas (WAL, foreign keys) and creates tables for magazines, packages, and stripes.
- CaptureDB._init_state: Recovers the system state (current magazine, package, stripe count) from the last database write upon startup.
- CaptureDB.reset_package_counter: Clears current package/stripe tracking in RAM to force starting a new package within the ongoing magazine.
- CaptureDB.get_all_capture_data: Retrieves a flat join of all stored data for spreadsheet export formatting.
- CaptureDB.add_stripe: Core transaction that stores a detected stripe, automatically advancing packages and magazines when limits are reached.
Workflows/Interactions:
- Uses threading.Lock() to guarantee thread-safe writes from background processing threads.
- Saves robust state securely in user app data directories preventing permission issues.
"""

import sqlite3
import threading
from typing import Optional, List, Tuple
import os
from appdirs import user_data_dir

DB_PATH = "captures.db"
APP_NAME = "IVIS"
APP_AUTHOR = "Fastech"

DATA_DIR = user_data_dir(APP_NAME, APP_AUTHOR)
os.makedirs(DATA_DIR, exist_ok=True)

class CaptureDB:
    def __init__(self):
        self.db_path = os.path.join(DATA_DIR, DB_PATH)
        self.lock = threading.Lock()
        
        self.packages_per_magazine = 20
        self.stripes_per_package = 10

        self.current_magazine_id: Optional[int] = None
        self.current_package_id: Optional[int] = None
        self.current_stripe_number: int = 0

        self.init_db()
        self._init_state()

    def init_db(self):
        conn = sqlite3.connect(self.db_path, timeout=30, isolation_level=None)
        conn.execute("PRAGMA foreign_keys = ON;")
        conn.execute("PRAGMA journal_mode = WAL;")
        conn.execute("PRAGMA synchronous = NORMAL;")
        conn.execute("""
            CREATE TABLE IF NOT EXISTS magazines (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                operator TEXT NOT NULL,
                magazine_from TEXT NOT NULL,
                magazine_to TEXT NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS packages (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                magazine_id INTEGER NOT NULL REFERENCES magazines(id) ON DELETE CASCADE,
                package_number INTEGER NOT NULL,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(magazine_id, package_number)
            )
        """)
        conn.execute("""
            CREATE TABLE IF NOT EXISTS stripes (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                package_id INTEGER NOT NULL REFERENCES packages(id) ON DELETE CASCADE,
                stripe_number INTEGER NOT NULL,
                description TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                UNIQUE(package_id, stripe_number)
            )
        """)
        conn.commit()
        conn.close()

    def _init_state(self):
        with self.lock:
            conn = sqlite3.connect(self.db_path, timeout=30)
            cur = conn.cursor()
            try:
                cur.execute("SELECT id FROM magazines ORDER BY id DESC LIMIT 1")
                mag_row = cur.fetchone()
                if mag_row is None:
                    return
                self.current_magazine_id = mag_row[0]

                cur.execute("SELECT COUNT(id) FROM packages WHERE magazine_id = ?",
                            (self.current_magazine_id,))
                package_count = cur.fetchone()[0]
                if package_count == 0:
                    return

                cur.execute("SELECT id FROM packages WHERE magazine_id = ? ORDER BY package_number DESC LIMIT 1",
                            (self.current_magazine_id,))
                pkg_row = cur.fetchone()
                if pkg_row is None:
                     return
                self.current_package_id = pkg_row[0]

                cur.execute("SELECT COUNT(id) FROM stripes WHERE package_id = ?",
                            (self.current_package_id,))
                stripe_count = cur.fetchone()[0]

                if stripe_count < self.stripes_per_package:
                    self.current_stripe_number = stripe_count
                else:
                    self.current_package_id = None
                    self.current_stripe_number = 0
                    if package_count >= self.packages_per_magazine:
                        self.current_magazine_id = None
                        
            except Exception as e:
                print(f"Error initializing DB state: {e}")
                self.current_magazine_id = None
                self.current_package_id = None
                self.current_stripe_number = 0
            finally:
                cur.close()
                conn.close()

    def reset_package_counter(self):
        with self.lock:
            self.current_package_id = None
            self.current_stripe_number = 0

    def get_all_capture_data(self) -> List[Tuple]:
        with self.lock:
            conn = sqlite3.connect(self.db_path, timeout=30)
            cur = conn.cursor()
            try:
                cur.execute("""
                    SELECT
                        m.id, m.operator, m.magazine_from, m.magazine_to,
                        p.package_number, s.stripe_number, s.description
                    FROM magazines m
                    JOIN packages p ON m.id = p.magazine_id
                    JOIN stripes s ON p.id = s.package_id
                    ORDER BY m.id, p.package_number, s.stripe_number
                """)
                return cur.fetchall()
            except Exception as e:
                print(f"Error fetching data for export: {e}")
                return []
            finally:
                cur.close()
                conn.close()
                
    def add_stripe(self, description: str, operator: str = "default_operator",
                   mag_from: str = "A", mag_to: str = "Z") -> Tuple[int, int, int]:
        with self.lock:
            conn = sqlite3.connect(self.db_path, timeout=30)
            cur = conn.cursor()
            conn.execute("PRAGMA foreign_keys = ON;")

            try:
                if self.current_magazine_id is not None:
                    cur.execute("SELECT operator, magazine_from, magazine_to FROM magazines WHERE id = ?",
                                (self.current_magazine_id,))
                    row = cur.fetchone()
                    if row:
                        old_operator, old_mag_from, old_mag_to = row
                        if (old_operator != operator or
                            old_mag_from != mag_from or
                            old_mag_to != mag_to):
                            self.current_magazine_id = None
                            self.current_package_id = None
                            self.current_stripe_number = 0

                conn.execute("BEGIN")

                if self.current_magazine_id is None:
                    cur.execute("INSERT INTO magazines(operator, magazine_from, magazine_to) VALUES (?, ?, ?)",
                                (operator, mag_from, mag_to))
                    self.current_magazine_id = cur.lastrowid
                    self.current_package_id = None
                    self.current_stripe_number = 0

                if self.current_package_id is None:
                    cur.execute("SELECT COUNT(id) FROM packages WHERE magazine_id = ?",
                                (self.current_magazine_id,))
                    package_count = cur.fetchone()[0]

                    if package_count >= self.packages_per_magazine:
                        cur.execute("INSERT INTO magazines(operator, magazine_from, magazine_to) VALUES (?, ?, ?)",
                                    (operator, mag_from, mag_to))
                        self.current_magazine_id = cur.lastrowid
                        self.current_package_id = None
                        self.current_stripe_number = 0
                        package_count = 0

                    new_package_number = package_count + 1
                    cur.execute("INSERT INTO packages (magazine_id, package_number) VALUES (?, ?)",
                                (self.current_magazine_id, new_package_number))
                    self.current_package_id = cur.lastrowid
                    self.current_stripe_number = 0

                new_stripe_number = self.current_stripe_number + 1
                
                cur.execute("""
                    INSERT INTO stripes (package_id, stripe_number, description)
                    VALUES (?, ?, ?)
                """, (self.current_package_id, new_stripe_number, description))
                
                self.current_stripe_number = new_stripe_number
                
                mag_id = self.current_magazine_id
                pkg_id = self.current_package_id
                stripe_num = self.current_stripe_number

                if self.current_stripe_number >= self.stripes_per_package:
                    self.current_package_id = None
                    self.current_stripe_number = 0
                    
                    cur.execute("SELECT COUNT(id) FROM packages WHERE magazine_id = ?",
                                (self.current_magazine_id,))
                    final_package_count = cur.fetchone()[0]
                    
                    if final_package_count >= self.packages_per_magazine:
                        self.current_magazine_id = None

                conn.commit()
                return (mag_id, pkg_id, stripe_num)

            except Exception as e:
                conn.rollback()
                print(f"Transaction failed: {e}")
                raise
            finally:
                cur.close()
                conn.close()

if __name__ == "__main__":
    db = CaptureDB()
    db.reset_package_counter()
    for i in range(1, 6):
        db.add_stripe(f"Stripe {i}", "TestOp", "A", "B")