LINK VIDEO YOUTUBE (UNLISTED): [MASUKKAN LINK VIDEO DI SINI]

# Restaurant Management API

REST API untuk manajemen restoran menggunakan FastAPI dan SQLite.

## Fitur
- CRUD Menu Restoran
- Membuat transaksi pesanan
- Melihat daftar transaksi
- Melihat detail transaksi
- Filter transaksi berdasarkan status
- BackgroundTasks untuk memproses pesanan
- asyncio.Lock untuk mencegah race condition

## Teknologi
- Python
- FastAPI
- SQLite
- aiosqlite
- Uvicorn
- Locust

## Instalasi

1. Clone repository:

```bash
git clone [https://github.com/231220076-creator/UTS_Restaurant_API.git]
```

2. Masuk ke folder proyek:

```bash
cd UTS_Restaurant_API
```

3. Buat virtual environment:

```bash
python -m venv venv
```

4. Aktifkan virtual environment (Windows):

```powershell
venv\Scripts\activate
```

5. Install library:

```bash
pip install -r requirements.txt
```

## Menjalankan Aplikasi

Jalankan perintah:

```bash
python -m uvicorn main:app --reload
```

Buka dokumentasi API:

http://127.0.0.1:8000/docs

## Menambahkan Data Awal

Jalankan:

```bash
python seed.py
```

## Pengujian Race Condition

Jalankan:

```bash
python test_race.py
```

## Pengujian Locust

Jalankan:

```bash
locust -f locustfile.py
```

Buka:

http://localhost:8089
