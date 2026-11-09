import asyncio
import aiosqlite
from database import DB_NAME


# Data awal menu restoran
data_menu = [
    ("Nasi Goreng", "Makanan", 15000, "Nasi goreng spesial", 20),
    ("Mie Goreng", "Makanan", 13000, "Mie goreng dengan telur", 15),
    ("Ayam Geprek", "Makanan", 18000, "Ayam geprek sambal pedas", 20),
    ("Soto Ayam", "Makanan", 15000, "Soto ayam kuah kuning", 15),
    ("Bakso", "Makanan", 12000, "Bakso kuah dengan mie", 25),
    ("Mie Ayam", "Makanan", 14000, "Mie ayam original", 20),
    ("Es Teh", "Minuman", 5000, "Es teh manis segar", 30),
    ("Jus Jeruk", "Minuman", 10000, "Jus jeruk segar", 15),
    ("Kopi Hitam", "Minuman", 8000, "Kopi hitam panas", 20),
    ("Air Mineral", "Minuman", 4000, "Air mineral kemasan", 30)
]


async def seed_database():
    async with aiosqlite.connect(DB_NAME) as db:

        # Memeriksa apakah data sudah tersedia
        cursor = await db.execute(
            "SELECT COUNT(*) FROM menus"
        )
        result = await cursor.fetchone()

        if result[0] == 0:

            await db.executemany("""
                INSERT INTO menus
                (nama, kategori, harga, deskripsi, stok)
                VALUES (?, ?, ?, ?, ?)
            """, data_menu)

            await db.commit()

            print("Berhasil menambahkan 10 data menu!")

        else:
            print("Data menu sudah tersedia, tidak perlu menambahkan lagi.")

        # Menampilkan seluruh data menu
        cursor = await db.execute(
            "SELECT * FROM menus"
        )
        menus = await cursor.fetchall()

        print("\nDAFTAR MENU RESTORAN")
        for menu in menus:
            print(menu)


if __name__ == "__main__":
    asyncio.run(seed_database())
