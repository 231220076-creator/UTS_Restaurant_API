import aiosqlite

DB_NAME = "restaurant.db"


# Membuat tabel database jika belum tersedia
async def init_db():
    async with aiosqlite.connect(DB_NAME) as db:

        await db.execute("PRAGMA foreign_keys = ON")

        # Tabel menu restoran
        await db.execute("""
            CREATE TABLE IF NOT EXISTS menus (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nama TEXT NOT NULL,
                kategori TEXT NOT NULL,
                harga REAL NOT NULL,
                deskripsi TEXT NOT NULL,
                stok INTEGER NOT NULL
            )
        """)

        # Tabel transaksi restoran
        await db.execute("""
            CREATE TABLE IF NOT EXISTS transactions (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                menu_id INTEGER NOT NULL,
                qty INTEGER NOT NULL,
                total_harga REAL NOT NULL,
                status TEXT NOT NULL DEFAULT 'pending',
                created_at TEXT NOT NULL,
                FOREIGN KEY (menu_id) REFERENCES menus(id)
            )
        """)

        await db.commit()


# Koneksi database asynchronous
async def get_db():
    db = await aiosqlite.connect(DB_NAME)
    db.row_factory = aiosqlite.Row

    await db.execute("PRAGMA foreign_keys = ON")

    try:
        yield db
    finally:
        await db.close()
