from locust import HttpUser, task, between, tag

class RestaurantUser(HttpUser):
    wait_time = between(0.1, 0.5)

    # Pengujian GET daftar menu
    @tag("read")
    @task
    def read_menus(self):
        self.client.get(
            "/menus/?skip=0&limit=10",
            name="GET /menus"
        )

    # Pengujian POST transaksi
    @tag("write")
    @task
    def create_transaction(self):
        self.client.post(
            "/transactions/",
            json={
                "menu_id": 1,
                "qty": 1
            },
            name="POST /transactions"
        )
