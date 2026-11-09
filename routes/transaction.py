from fastapi import APIRouter, Depends, HTTPException, BackgroundTasks, Query
from aiosqlite import Connection
import aiosqlite
import asyncio

from database import get_db
from models import TransactionCreate, TransactionResponse

router = APIRouter(
    prefix="/transactions",
    tags=["Transaksi Pesanan"]
)

@router.post("/", response_model=TransactionResponse, status_code=202)
async def create_transaction(
    data: TransactionCreate,
    background_tasks: BackgroundTasks,
    db: Connection = Depends(get_db)
):
    # Periksa apakah menu tersedia
    cursor = await db.execute(
        "SELECT * FROM menus WHERE id = ?",
        (data.menu_id,)
    )
    menu = await cursor.fetchone()

    if menu is None:
        raise HTTPException(
            status_code=404,
            detail="Menu tidak ditemukan"
        )

    # Periksa jumlah stok
    if menu["stok"] < data.qty:
        raise HTTPException(
            status_code=409,
            detail="Stok menu tidak mencukupi"
        )

    # Hitung total harga pesanan
    total_harga = menu["harga"] * data.qty

    # Simpan transaksi dengan status pending
    from datetime import datetime

    created_at = datetime.now().isoformat()

    cursor = await db.execute(
        """
        INSERT INTO transactions
        (menu_id, qty, total_harga, status, created_at)
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            data.menu_id,
            data.qty,
            total_harga,
            "pending",
            created_at
        )
    )

    await db.commit()

    transaction_id = cursor.lastrowid
    background_tasks.add_task(process_transaction, transaction_id)

    return {
        "id": transaction_id,
        "menu_id": data.menu_id,
        "qty": data.qty,
        "total_harga": total_harga,
        "status": "pending",
        "created_at": created_at
    }
# Fungsi untuk memproses transaksi di background
async def process_transaction(transaction_id: int):

    # Ubah status menjadi processing
    async with aiosqlite.connect("restaurant.db") as db:
        await db.execute(
            "UPDATE transactions SET status = 'processing' WHERE id = ?",
            (transaction_id,)
        )
        await db.commit()

    # Simulasi proses pesanan selama 3 detik
    await asyncio.sleep(3)

    # Ubah status menjadi completed
    async with aiosqlite.connect("restaurant.db") as db:
        await db.execute(
            "UPDATE transactions SET status = 'completed' WHERE id = ?",
            (transaction_id,)
        )
        await db.commit()

        

@router.get("/", response_model=list[TransactionResponse])
async def get_transactions(
    status: str | None = Query(default=None),
    db: Connection = Depends(get_db)
):
    if status:
        cursor = await db.execute(
            "SELECT * FROM transactions WHERE status = ? ORDER BY id DESC",
            (status,)
        )
    else:
        cursor = await db.execute(
            "SELECT * FROM transactions ORDER BY id DESC"
        )

    transactions = await cursor.fetchall()

    return [dict(transaction) for transaction in transactions]

@router.get("/{transaction_id}", response_model=TransactionResponse)
async def get_transaction(
    transaction_id: int,
    db: Connection = Depends(get_db)
):
    cursor = await db.execute(
        "SELECT * FROM transactions WHERE id = ?",
        (transaction_id,)
    )
    transaction = await cursor.fetchone()

    if transaction is None:
        raise HTTPException(
            status_code=404,
            detail="Transaksi tidak ditemukan"
        )

    return dict(transaction)

