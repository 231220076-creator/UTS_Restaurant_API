from fastapi import APIRouter, Depends, HTTPException, status, Query
import aiosqlite

from database import get_db
from models import MenuCreate, MenuUpdate, MenuResponse


router = APIRouter(
    prefix="/menus",
    tags=["Menu Restoran"]
)


# 1. GET: Menampilkan semua menu dengan pagination
@router.get("/", response_model=list[MenuResponse])
async def get_menus(
    skip: int = Query(default=0, ge=0),
    limit: int = Query(default=10, ge=1, le=100),
    db: aiosqlite.Connection = Depends(get_db)
):
    cursor = await db.execute(
        "SELECT * FROM menus LIMIT ? OFFSET ?",
        (limit, skip)
    )

    rows = await cursor.fetchall()

    return [dict(row) for row in rows]


# 2. GET: Menampilkan detail menu berdasarkan ID
@router.get("/{menu_id}", response_model=MenuResponse)
async def get_menu(
    menu_id: int,
    db: aiosqlite.Connection = Depends(get_db)
):
    cursor = await db.execute(
        "SELECT * FROM menus WHERE id = ?",
        (menu_id,)
    )

    row = await cursor.fetchone()

    if row is None:
        raise HTTPException(
            status_code=404,
            detail="Menu tidak ditemukan"
        )

    return dict(row)


# 3. POST: Menambahkan menu baru
@router.post(
    "/",
    response_model=MenuResponse,
    status_code=status.HTTP_201_CREATED
)
async def create_menu(
    menu: MenuCreate,
    db: aiosqlite.Connection = Depends(get_db)
):
    cursor = await db.execute(
        """
        INSERT INTO menus
        (nama, kategori, harga, deskripsi, stok)
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            menu.nama,
            menu.kategori,
            menu.harga,
            menu.deskripsi,
            menu.stok
        )
    )

    await db.commit()

    new_id = cursor.lastrowid

    cursor = await db.execute(
        "SELECT * FROM menus WHERE id = ?",
        (new_id,)
    )

    row = await cursor.fetchone()

    return dict(row)


# 4. PUT: Memperbarui menu berdasarkan ID
@router.put("/{menu_id}", response_model=MenuResponse)
async def update_menu(
    menu_id: int,
    menu: MenuUpdate,
    db: aiosqlite.Connection = Depends(get_db)
):
    cursor = await db.execute(
        "SELECT id FROM menus WHERE id = ?",
        (menu_id,)
    )

    row = await cursor.fetchone()

    if row is None:
        raise HTTPException(
            status_code=404,
            detail="Menu tidak ditemukan"
        )

    await db.execute(
        """
        UPDATE menus
        SET nama = ?, kategori = ?, harga = ?,
            deskripsi = ?, stok = ?
        WHERE id = ?
        """,
        (
            menu.nama,
            menu.kategori,
            menu.harga,
            menu.deskripsi,
            menu.stok,
            menu_id
        )
    )

    await db.commit()

    cursor = await db.execute(
        "SELECT * FROM menus WHERE id = ?",
        (menu_id,)
    )

    updated_row = await cursor.fetchone()

    return dict(updated_row)


# 5. DELETE: Menghapus menu secara permanen
@router.delete("/{menu_id}")
async def delete_menu(
    menu_id: int,
    db: aiosqlite.Connection = Depends(get_db)
):
    cursor = await db.execute(
        "SELECT id FROM menus WHERE id = ?",
        (menu_id,)
    )

    row = await cursor.fetchone()

    if row is None:
        raise HTTPException(
            status_code=404,
            detail="Menu tidak ditemukan"
        )

    await db.execute(
        "DELETE FROM menus WHERE id = ?",
        (menu_id,)
    )

    await db.commit()

    return {
        "message": "Menu berhasil dihapus"
    }
