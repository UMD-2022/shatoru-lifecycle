import json
import random

from locust import HttpUser, between, task


class ShuttleDemo(HttpUser):
    wait_time = between(1, 5)

    @task(1)
    def get_shuttle(self):
        shuttles_response = self.client.get(
            "/shuttles/",
        )
        if shuttles_response.status_code != 200:
            return
        shuttles = json.loads(shuttles_response.content)
        shuttle_id = random.choice(shuttles)["id"]
        self.client.get(
            f"/shuttles/{shuttle_id}/",
        )

    @task(4)
    def get_schedule(self):
        # First, retrieve a list of all schedules so we can choose one at random
        response = self.client.get(
            "/shuttles/schedules/",
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
