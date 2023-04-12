import json
import random

from locust import HttpUser, between, task


class Shuttle(HttpUser):
    wait_time = between(1, 5)

    url = "/shuttles/schedules/"

    def on_start(self):
        # Authenticate with the API
        response = self.client.post(
            "/auth/login/",
            data={
                "username": "admin",
                "password": "admin",
            },
        )
        if response.status_code != 200:
            raise Exception("Failed to authenticate with the API")
        self.access_token = json.loads(response.content)["token"]

    @task(1)
    def create_schedule(self):
        data = {
            "shuttle": "My Shuttle",
            "days": ["Sunday", "Wednesday", "Friday"],
            "start_time": "06:00:00 AM",
            "end_time": "10:00:00 PM",
            "stops": {
                "7640112e-3112-44df-9dd2-f77e620e23ac": "10",
                "e9550ac8-5b6e-42c1-ac50-695d4aa8c280": "20",
                "5da60b7e-89de-44ad-9e11-3b8c0e5ff3b0": "15",
                "a240bdba-b9d1-4748-b5e0-7a07545d2107": "10",
            },
        }
        self.client.post(
            self.url,
            headers={"Authorization": f"Token {self.access_token}"},
            json=data,
        )

    @task(4)
    def get_schedule(self):
        # First, retrieve a list of all schedules so we can choose one at random
        response = self.client.get(
            self.url,
        )
        if response.status_code != 200:
            return
        schedules = json.loads(response.content)
        if not schedules:
            return
        schedule_id = random.choice(schedules)["id"]

        self.client.get(
            f"/shuttles/schedules/{schedule_id}/",
        )

    @task(1)
    def update_schedule(self):
        # First, retrieve a list of all schedules so we can choose one at random
        response = self.client.get(
            self.url,
            headers={"Authorization": f"Token {self.access_token}"},
        )
        if response.status_code != 200:
            return
        schedules = json.loads(response.content)
        if not schedules:
            return
        schedule_id = random.choice(schedules)["id"]

        data = {
            "stops": {
                "7640112e-3112-44df-9dd2-f77e620e23ac": "5",
                "e9550ac8-5b6e-42c1-ac50-695d4aa8c280": "10",
                "5da60b7e-89de-44ad-9e11-3b8c0e5ff3b0": "5",
                "a240bdba-b9d1-4748-b5e0-7a07545d2107": "10",
            },
        }
        self.client.patch(
            f"/schedules/{schedule_id}/",
            headers={"Authorization": f"Token {self.access_token}"},
            json=data,
        )

    @task(1)
    def delete_schedule(self):
        # First, retrieve a list of all schedules so we can choose one at random
        response = self.client.get(
            "/schedules/",
            headers={"Authorization": f"Token {self.access_token}"},
        )
        if response.status_code != 200:
            return
        schedules = json.loads(response.content)
        if not schedules:
            return
        schedule_id = random.choice(schedules)["id"]

        self.client.delete(
            f"/schedules/{schedule_id}/",
            headers={"Authorization": f"Token {self.access_token}"},
        )
