import json

from locust import HttpUser, between, task


class AuthUser(HttpUser):
    """
    A Locust user that simulates password reset requests.
    """

    # Set the wait time between requests to be between 1 and 2 seconds
    wait_time = between(1, 2)

    @task
    def password_reset(self):
        """
        Simulate a password reset request.
        """

        # Make a POST request to the password reset API endpoint
        response = self.client.post(
            "/auth/password/reset/",
            json={"email": "test@example.com"},
        )

        # Check that the response was successful
        assert response.status_code == 200

        # Check that an email was sent to the user
        assert "email" in response.json()
        assert response.json()["email"] == "test@example.com"

    @task
    def login(self):
        # Login endpoint
        response = self.client.post(
            "/auth/login/",
            data=json.dumps({"username": "admin", "password": "admin"}),
            headers={"content-type": "application/json"},
        )
        if response.status_code == 200:
            auth_token = response.json()["token"]
            self.client.headers["Authorization"] = f"Token {auth_token}"

    @task
    def reset_password(self):
        # Request password reset endpoint
        response = self.client.post(
            "/auth/password/reset/",
            data=json.dumps({"email": "my_email@example.com"}),
            headers={"content-type": "application/json"},
        )

        # Confirm email was sent
        assert response.status_code == 200

        # Retrieve password reset token from email (hypothetical)
        reset_token = "my_password_reset_token"

        # Password reset endpoint
        response = self.client.post(
            "/auth/password/reset/confirm/",
            data=json.dumps({"token": reset_token, "password": "my_new_password"}),
            headers={"content-type": "application/json"},
        )

        # Confirm password was reset successfully
        assert response.status_code == 200
