import asyncio
import aiosqlite

from database import DB_NAME


async def migrate():
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute("PRAGMA foreign_keys = OFF")

        # Buat tabel menu baru tanpa CHECK stok >= 0
        await db.execute("""
            CREATE TABLE menus_new (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nama TEXT NOT NULL,
                kategori TEXT NOT NULL,
                harga REAL NOT NULL,
                deskripsi TEXT NOT NULL,
                stok INTEGER NOT NULL
            )
        """)

        # Salin seluruh data menu lama
        await db.execute("""
            INSERT INTO menus_new
            SELECT * FROM menus
        """)

        # Ganti tabel lama dengan tabel baru
        await db.execute("DROP TABLE menus")
        await db.execute("ALTER TABLE menus_new RENAME TO menus")

        await db.commit()
        await db.execute("PRAGMA foreign_keys = ON")

        print("Migrasi database berhasil!")
        print("Data menu dan transaksi tetap dipertahankan.")


if __name__ == "__main__":
    asyncio.run(migrate())
