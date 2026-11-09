from pydantic import BaseModel, Field, ConfigDict


# Model untuk menerima data menu baru
class MenuCreate(BaseModel):
    nama: str = Field(min_length=2)
    kategori: str
    harga: float = Field(gt=0)
    deskripsi: str
    stok: int = Field(ge=0)


# Model untuk memperbarui data menu
class MenuUpdate(BaseModel):
    nama: str = Field(min_length=2)
    kategori: str
    harga: float = Field(gt=0)
    deskripsi: str
    stok: int = Field(ge=0)


# Model untuk menampilkan data menu
class MenuResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    nama: str
    kategori: str
    harga: float
    deskripsi: str
    stok: int


# Model untuk menerima transaksi baru
class TransactionCreate(BaseModel):
    menu_id: int = Field(gt=0)
    qty: int = Field(gt=0)


# Model untuk menampilkan data transaksi
class TransactionResponse(BaseModel):
    id: int
    menu_id: int
    qty: int
    total_harga: float
    status: str
    created_at: str
