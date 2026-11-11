import aiosqlite
import hashlib
import secrets
import json
from typing import Dict, Any, List, Optional
from config import DB_PATH

ALL_MAIN_FIELDS = [
    # طلا
    'gold_18k', 'gold_18k_buy',
    'gold_24k', 'gold_24k_buy',
    'gold_used', 'gold_used_buy',
    'gold_melted', 'gold_melted_buy',
    # نقره
    'silver_999', 'silver_999_buy',
    'silver_925', 'silver_925_buy',
    # سکه‌های بانکی
    'coin_emami', 'coin_emami_buy',
    'coin_bahar', 'coin_bahar_buy',
    'coin_half_new', 'coin_half_new_buy',
    'coin_rob_new', 'coin_rob_new_buy',
    'coin_grami', 'coin_grami_buy',
    # سکه‌های طرح قدیم (قبل ۸۶)
    'coin_emami_old', 'coin_emami_old_buy',
    'coin_half_old', 'coin_half_old_buy',
    'coin_rob_old', 'coin_rob_old_buy',
    # ارزها
    'currency_usd', 'currency_usd_buy',
    'currency_usdt', 'currency_usdt_buy',
    'currency_eur', 'currency_eur_buy',
    'currency_aed', 'currency_aed_buy',
    'currency_gbp', 'currency_gbp_buy',
    'currency_try', 'currency_try_buy',
    'currency_cad', 'currency_cad_buy',
    'currency_aud', 'currency_aud_buy',
    'currency_iqd', 'currency_iqd_buy',
]

class Database:
    def __init__(self, db_path: str = DB_PATH):
        self.db_path = db_path

    async def init_db(self):
        """ایجاد جداول و مهاجرت ستون‌ها"""
        async with aiosqlite.connect(self.db_path) as db:
            # جدول کاربران
            await db.execute("""
                CREATE TABLE IF NOT EXISTS users (
                    user_id INTEGER PRIMARY KEY,
                    first_name TEXT,
                    username TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            # جدول دارایی‌ها
            cols_def = ", ".join([f"{col} REAL DEFAULT 0.0" for col in ALL_MAIN_FIELDS])
            await db.execute(f"""
                CREATE TABLE IF NOT EXISTS portfolio_holdings (
                    user_id INTEGER PRIMARY KEY,
                    {cols_def},
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY(user_id) REFERENCES users(user_id)
                )
            """)

            # جدول سکه‌های پارسیان
            await db.execute("""
                CREATE TABLE IF NOT EXISTS parsian_holdings (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    weight REAL,
                    quantity INTEGER DEFAULT 0,
                    buy_price REAL DEFAULT 0.0,
                    FOREIGN KEY(user_id) REFERENCES users(user_id),
                    UNIQUE(user_id, weight)
                )
            """)

            # جدول هشدارهای قیمتی
            await db.execute("""
                CREATE TABLE IF NOT EXISTS price_alerts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER,
                    item_key TEXT,
                    item_title TEXT,
                    target_price REAL,
                    direction TEXT,
                    is_active INTEGER DEFAULT 1,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY(user_id) REFERENCES users(user_id)
                )
            """)

            # جدول تنظیمات کاربر
            await db.execute("""
                CREATE TABLE IF NOT EXISTS user_settings (
                    user_id INTEGER PRIMARY KEY,
                    daily_digest INTEGER DEFAULT 1,
                    bubble_alert INTEGER DEFAULT 1,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY(user_id) REFERENCES users(user_id)
                )
            """)

            # جداول اختصاصی حساب‌های کاربری وب و پرتفوی ابری
            await db.execute("""
                CREATE TABLE IF NOT EXISTS web_users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    username TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    display_name TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

            await db.execute("""
                CREATE TABLE IF NOT EXISTS web_portfolios (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL UNIQUE,
                    portfolio_json TEXT NOT NULL DEFAULT '[]',
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY(user_id) REFERENCES web_users(id)
                )
            """)

            await db.execute("""
                CREATE TABLE IF NOT EXISTS web_sessions (
                    token TEXT PRIMARY KEY,
                    user_id INTEGER NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY(user_id) REFERENCES web_users(id)
                )
            """)

            # مهاجرت ستون‌های دارایی
            async with db.execute("PRAGMA table_info(portfolio_holdings)") as cursor:
                existing_cols = [row[1] for row in await cursor.fetchall()]
                for col in ALL_MAIN_FIELDS:
                    if col not in existing_cols:
                        await db.execute(f"ALTER TABLE portfolio_holdings ADD COLUMN {col} REAL DEFAULT 0.0")

            await db.commit()

    async def register_user(self, user_id: int, first_name: str, username: Optional[str] = None):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
                INSERT INTO users (user_id, first_name, username)
                VALUES (?, ?, ?)
                ON CONFLICT(user_id) DO UPDATE SET
                    first_name = excluded.first_name,
                    username = excluded.username
            """, (user_id, first_name, username))

            await db.execute("""
                INSERT INTO portfolio_holdings (user_id)
                VALUES (?)
                ON CONFLICT(user_id) DO NOTHING
            """, (user_id,))

            await db.execute("""
                INSERT INTO user_settings (user_id, daily_digest, bubble_alert)
                VALUES (?, 1, 1)
                ON CONFLICT(user_id) DO NOTHING
            """, (user_id,))
            await db.commit()

    async def get_holdings(self, user_id: int) -> Dict[str, Any]:
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute("SELECT * FROM portfolio_holdings WHERE user_id = ?", (user_id,)) as cursor:
                row = await cursor.fetchone()
                main_holdings = dict(row) if row else {k: 0.0 for k in ALL_MAIN_FIELDS}

            async with db.execute(
                "SELECT weight, quantity, buy_price FROM parsian_holdings WHERE user_id = ? AND quantity > 0 ORDER BY weight ASC",
                (user_id,)
            ) as cursor:
                parsian_rows = await cursor.fetchall()
                parsian_list = [
                    {'weight': r['weight'], 'quantity': r['quantity'], 'buy_price': r['buy_price']}
                    for r in parsian_rows
                ]

            return {
                'main': main_holdings,
                'parsian': parsian_list
            }

    async def update_main_holding(self, user_id: int, field_name: str, amount: float, buy_price: float = 0.0):
        buy_field = f"{field_name}_buy"
        async with aiosqlite.connect(self.db_path) as db:
            if amount <= 0:
                amount = 0.0
                buy_price = 0.0

            query = f"""
                INSERT INTO portfolio_holdings (user_id, {field_name}, {buy_field}, updated_at)
                VALUES (?, ?, ?, CURRENT_TIMESTAMP)
                ON CONFLICT(user_id) DO UPDATE SET
                    {field_name} = excluded.{field_name},
                    {buy_field} = excluded.{buy_field},
                    updated_at = CURRENT_TIMESTAMP
            """
            await db.execute(query, (user_id, amount, buy_price))
            await db.commit()

    async def update_parsian_holding(self, user_id: int, weight: float, quantity: int, buy_price: float = 0.0):
        async with aiosqlite.connect(self.db_path) as db:
            if quantity <= 0:
                await db.execute("DELETE FROM parsian_holdings WHERE user_id = ? AND weight = ?", (user_id, weight))
            else:
                await db.execute("""
                    INSERT INTO parsian_holdings (user_id, weight, quantity, buy_price)
                    VALUES (?, ?, ?, ?)
                    ON CONFLICT(user_id, weight) DO UPDATE SET
                        quantity = excluded.quantity,
                        buy_price = excluded.buy_price
                """, (user_id, weight, quantity, buy_price))
            await db.commit()

    async def clear_all_holdings(self, user_id: int):
        reset_pairs = ", ".join([f"{col} = 0" for col in ALL_MAIN_FIELDS])
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(f"""
                UPDATE portfolio_holdings SET
                    {reset_pairs},
                    updated_at = CURRENT_TIMESTAMP
                WHERE user_id = ?
            """, (user_id,))
            await db.execute("DELETE FROM parsian_holdings WHERE user_id = ?", (user_id,))
            await db.commit()

    # --- مدیریت هشدارها ---
    async def add_price_alert(self, user_id: int, item_key: str, item_title: str, target_price: float, direction: str) -> int:
        async with aiosqlite.connect(self.db_path) as db:
            cursor = await db.execute("""
                INSERT INTO price_alerts (user_id, item_key, item_title, target_price, direction, is_active)
                VALUES (?, ?, ?, ?, ?, 1)
            """, (user_id, item_key, item_title, target_price, direction))
            await db.commit()
            return cursor.lastrowid

    async def get_active_alerts(self) -> List[Dict[str, Any]]:
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute("SELECT * FROM price_alerts WHERE is_active = 1") as cursor:
                rows = await cursor.fetchall()
                return [dict(r) for r in rows]

    async def get_user_alerts(self, user_id: int) -> List[Dict[str, Any]]:
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute("SELECT * FROM price_alerts WHERE user_id = ? AND is_active = 1 ORDER BY id DESC", (user_id,)) as cursor:
                rows = await cursor.fetchall()
                return [dict(r) for r in rows]

    async def deactivate_alert(self, alert_id: int):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("UPDATE price_alerts SET is_active = 0 WHERE id = ?", (alert_id,))
            await db.commit()

    async def delete_alert(self, alert_id: int, user_id: int):
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("DELETE FROM price_alerts WHERE id = ? AND user_id = ?", (alert_id, user_id))
            await db.commit()

    # --- تنظیمات کاربر ---
    async def get_user_settings(self, user_id: int) -> Dict[str, Any]:
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute("SELECT * FROM user_settings WHERE user_id = ?", (user_id,)) as cursor:
                row = await cursor.fetchone()
                if row:
                    return dict(row)
                return {'daily_digest': 1, 'bubble_alert': 1}

    async def toggle_setting(self, user_id: int, setting_name: str) -> int:
        current = await self.get_user_settings(user_id)
        new_val = 0 if current.get(setting_name, 1) == 1 else 1
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute(f"""
                INSERT INTO user_settings (user_id, {setting_name})
                VALUES (?, ?)
                ON CONFLICT(user_id) DO UPDATE SET
                    {setting_name} = ?,
                    updated_at = CURRENT_TIMESTAMP
            """, (user_id, new_val, new_val))
            await db.commit()
        return new_val

    async def get_all_digest_users(self) -> List[int]:
        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute("SELECT user_id FROM user_settings WHERE daily_digest = 1") as cursor:
                rows = await cursor.fetchall()
                return [r[0] for r in rows]

    # ==========================================
    # متدهای حساب کاربری وب و پرتفوی ابری
    # ==========================================
    @staticmethod
    def _hash_password(password: str) -> str:
        return hashlib.sha256(f"tala_salt_2026_{password}".encode()).hexdigest()

    async def register_web_user(self, username: str, password: str, display_name: str = "") -> Dict[str, Any]:
        username = username.strip().lower()
        if not username or len(username) < 3:
            return {'success': False, 'error': 'نام کاربری باید حداقل ۳ کاراکتر باشد.'}
        if not password or len(password) < 4:
            return {'success': False, 'error': 'رمز عبور باید حداقل ۴ کاراکتر باشد.'}

        display_name = display_name.strip() or username
        password_hash = self._hash_password(password)

        async with aiosqlite.connect(self.db_path) as db:
            async with db.execute("SELECT id FROM web_users WHERE username = ?", (username,)) as cursor:
                if await cursor.fetchone():
                    return {'success': False, 'error': 'این نام کاربری قبلاً ثبت شده است.'}

            cursor = await db.execute(
                "INSERT INTO web_users (username, password_hash, display_name) VALUES (?, ?, ?)",
                (username, password_hash, display_name)
            )
            user_id = cursor.lastrowid

            token = secrets.token_hex(24)
            await db.execute("INSERT INTO web_sessions (token, user_id) VALUES (?, ?)", (token, user_id))
            await db.commit()

            return {
                'success': True,
                'user': {
                    'id': user_id,
                    'username': username,
                    'display_name': display_name,
                },
                'token': token,
            }

    async def login_web_user(self, username: str, password: str) -> Dict[str, Any]:
        username = username.strip().lower()
        password_hash = self._hash_password(password)

        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute(
                "SELECT id, username, display_name FROM web_users WHERE username = ? AND password_hash = ?",
                (username, password_hash)
            ) as cursor:
                row = await cursor.fetchone()
                if not row:
                    return {'success': False, 'error': 'نام کاربری یا رمز عبور اشتباه است.'}

                user_id = row['id']
                display_name = row['display_name']

            token = secrets.token_hex(24)
            await db.execute("INSERT INTO web_sessions (token, user_id) VALUES (?, ?)", (token, user_id))

            portfolio = []
            async with db.execute("SELECT portfolio_json FROM web_portfolios WHERE user_id = ?", (user_id,)) as p_cur:
                p_row = await p_cur.fetchone()
                if p_row and p_row['portfolio_json']:
                    try:
                        portfolio = json.loads(p_row['portfolio_json'])
                    except Exception:
                        portfolio = []

            await db.commit()

            return {
                'success': True,
                'user': {
                    'id': user_id,
                    'username': username,
                    'display_name': display_name,
                },
                'token': token,
                'portfolio': portfolio,
            }

    async def get_web_user_by_token(self, token: str) -> Optional[Dict[str, Any]]:
        if not token:
            return None
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute("""
                SELECT u.id, u.username, u.display_name
                FROM web_users u
                JOIN web_sessions s ON u.id = s.user_id
                WHERE s.token = ?
            """, (token,)) as cursor:
                row = await cursor.fetchone()
                if row:
                    return dict(row)
        return None

    async def logout_web_user(self, token: str) -> bool:
        if not token:
            return False
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("DELETE FROM web_sessions WHERE token = ?", (token,))
            await db.commit()
            return True

    async def save_web_user_portfolio(self, user_id: int, portfolio: list) -> bool:
        portfolio_json = json.dumps(portfolio, ensure_ascii=False)
        async with aiosqlite.connect(self.db_path) as db:
            await db.execute("""
                INSERT INTO web_portfolios (user_id, portfolio_json, updated_at)
                VALUES (?, ?, CURRENT_TIMESTAMP)
                ON CONFLICT(user_id) DO UPDATE SET
                    portfolio_json = excluded.portfolio_json,
                    updated_at = CURRENT_TIMESTAMP
            """, (user_id, portfolio_json))
            await db.commit()
            return True

    async def get_web_user_portfolio(self, user_id: int) -> list:
        async with aiosqlite.connect(self.db_path) as db:
            db.row_factory = aiosqlite.Row
            async with db.execute("SELECT portfolio_json FROM web_portfolios WHERE user_id = ?", (user_id,)) as cursor:
                row = await cursor.fetchone()
                if row and row['portfolio_json']:
                    try:
                        return json.loads(row['portfolio_json'])
                    except Exception:
                        return []
        return []

db_service = Database()
