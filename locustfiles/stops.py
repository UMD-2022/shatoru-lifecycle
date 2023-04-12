import json

from locust import HttpUser, between, task


class ShuttleStops(HttpUser):
    wait_time = between(1, 5)

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

    @task
    def create_stop(self):
        for i in range(10):
            name = f"Stop {i}"
            abbr = f"S{i}"
            data = {"name": name, "abbr": abbr}
            headers = {
                "Authorization": f"Token {self.access_token}",
                "content-type": "application/json",
            }
            response = self.client.post(
                "/stops/",
                data=json.dumps(data),
                headers=headers,
            )
            if response.status_code != 201:
                print(f"Insertion failed: {response.status_code} - {response.content}")
