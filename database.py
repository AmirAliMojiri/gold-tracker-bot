import aiosqlite
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
    # سکه‌ها
    'coin_emami', 'coin_emami_buy',
    'coin_bahar', 'coin_bahar_buy',
    'coin_half_new', 'coin_half_new_buy',
    'coin_half_old', 'coin_half_old_buy',
    'coin_rob_new', 'coin_rob_new_buy',
    'coin_rob_old', 'coin_rob_old_buy',
    'coin_grami', 'coin_grami_buy',
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
        """ایجاد جداول و مهاجرت ستون‌های جدید در صورت نیاز"""
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

            # جدول جامع دارایی‌های کاربر
            cols_def = ", ".join([f"{col} REAL DEFAULT 0.0" for col in ALL_MAIN_FIELDS])
            await db.execute(f"""
                CREATE TABLE IF NOT EXISTS portfolio_holdings (
                    user_id INTEGER PRIMARY KEY,
                    {cols_def},
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY(user_id) REFERENCES users(user_id)
                )
            """)

            # بررسی و افزودن ستون‌های احتمالی در دیتابیس قدیمی
            async with db.execute("PRAGMA table_info(portfolio_holdings)") as cursor:
                existing_cols = [row[1] for row in await cursor.fetchall()]
                for col in ALL_MAIN_FIELDS:
                    if col not in existing_cols:
                        await db.execute(f"ALTER TABLE portfolio_holdings ADD COLUMN {col} REAL DEFAULT 0.0")

            # جدول دارایی‌های سکه پارسیان
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

            # بررسی ستون buy_price در جدول پارسیان
            async with db.execute("PRAGMA table_info(parsian_holdings)") as cursor:
                p_cols = [row[1] for row in await cursor.fetchall()]
                if 'buy_price' not in p_cols:
                    await db.execute("ALTER TABLE parsian_holdings ADD COLUMN buy_price REAL DEFAULT 0.0")

            await db.commit()

    async def register_user(self, user_id: int, first_name: str, username: Optional[str] = None):
        """ثبت نام یا به‌روزرسانی اطلاعات کاربر"""
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
            await db.commit()

    async def get_holdings(self, user_id: int) -> Dict[str, Any]:
        """دریافت تمام دارایی‌ها و قیمت‌های خرید کاربر"""
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
        """به‌روزرسانی مقدار دارایی و قیمت خرید آن"""
        if field_name not in ALL_MAIN_FIELDS and f"{field_name}_buy" not in ALL_MAIN_FIELDS:
            raise ValueError(f"فیلد نامعتبر است: {field_name}")

        buy_field = f"{field_name}_buy"
        async with aiosqlite.connect(self.db_path) as db:
            # مقدار صفر دارایی، قیمت خرید را نیز ریست می‌کند
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
        """به‌روزرسانی تعداد و قیمت خرید سکه پارسیان"""
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
        """حذف و صفر کردن تمام دارایی‌های کاربر"""
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

# نمونه سراسری دیتابیس
db_service = Database()
