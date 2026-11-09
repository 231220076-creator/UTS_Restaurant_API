import asyncio
import aiosqlite

from database import DB_NAME

# Membuat pengunci agar transaksi berjalan bergantian
stock_lock = asyncio.Lock()


async def pesan_menu(nama_pelanggan):
    # Hanya satu pelanggan yang boleh memeriksa dan mengubah stok
    # pada satu waktu.
    async with stock_lock:
        async with aiosqlite.connect(DB_NAME) as db:
            cursor = await db.execute(
                "SELECT stok FROM menus WHERE id = 1"
            )
            menu = await cursor.fetchone()

            stok = menu[0]

            print(f"{nama_pelanggan} melihat stok: {stok}")

            if stok >= 1:
                await asyncio.sleep(1)

                await db.execute(
                    "UPDATE menus SET stok = stok - 1 WHERE id = 1",
                )
                await db.commit()

                print(f"{nama_pelanggan} berhasil memesan!")
            else:
                print(f"{nama_pelanggan} gagal, stok habis!")


async def main():
    # Atur stok awal menjadi 1
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute(
            "UPDATE menus SET stok = 1 WHERE id = 1"
        )
        await db.commit()

    # Dua pelanggan memesan secara bersamaan
    await asyncio.gather(
        pesan_menu("Pelanggan A"),
        pesan_menu("Pelanggan B")
    )

    # Tampilkan stok akhir
    async with aiosqlite.connect(DB_NAME) as db:
        cursor = await db.execute(
            "SELECT stok FROM menus WHERE id = 1"
        )
        hasil = await cursor.fetchone()

        print("\nStok akhir:", hasil[0])


if __name__ == "__main__":
    asyncio.run(main())
