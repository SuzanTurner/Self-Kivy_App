import requests


BASE_URL = "http://127.0.0.1:8000"


class API:
    def __init__(self):
        self.access_token = None
        self.refresh_token = None

    def login(self, username, password):
        response = requests.post(
            f"{BASE_URL}/api/auth/login/",
            json={
                "username": username,
                "password": password,
            },
            timeout=10,
        )

        if response.status_code != 200:
            return False, response.json()

        data = response.json()

        self.access_token = data["access"]
        self.refresh_token = data["refresh"]

        return True, data

    def get_feed(self):
        if not self.access_token:
            return False, {"detail": "Not authenticated"}

        response = requests.get(
            f"{BASE_URL}/api/feed/",
            headers={
                "Authorization": f"Bearer {self.access_token}"
            },
            timeout=10,
        )

        if response.status_code != 200:
            return False, response.json()

        return True, response.json()
    
    def upload_post(self, file_path):

        if not self.access_token:
            return False, {"detail": "Not authenticated"}

        try:
            with open(file_path, "rb") as image_file:

                response = requests.post(
                    f"{BASE_URL}/api/posts/",
                    headers={
                        "Authorization": f"Bearer {self.access_token}"
                    },
                    files={
                        "photo": image_file
                    },
                    timeout=30
                )

            if response.status_code != 201:
                return False, response.json()

            return True, response.json()

        except Exception as e:
            return False, {
                "detail": str(e)
            }
        
    def get_my_profile(self):
        if not self.access_token:
            return False, {"detail": "Not authenticated"}

        try:
            response = requests.get(
                f"{BASE_URL}/api/users/me/",
                headers={
                    "Authorization": f"Bearer {self.access_token}"
                },
                timeout=10,
            )

            if response.status_code != 200:
                try:
                    return False, response.json()
                except Exception:
                    return False, {
                        "detail": response.text
                    }

            return True, response.json()

        except Exception as e:
            return False, {
                "detail": str(e)
            }
    
    def get_profile(self, username):
        if not self.access_token:
            return False, {"detail": "Not authenticated"}

        try:
            response = requests.get(
                f"{BASE_URL}/api/users/{username}/",
                headers={
                    "Authorization": f"Bearer {self.access_token}"
                },
                timeout=10,
            )

            if response.status_code != 200:
                try:
                    return False, response.json()
                except Exception:
                    return False, {
                        "detail": response.text
                    }

            return True, response.json()

        except Exception as e:
            return False, {
                "detail": str(e)
            }
        
    def search_users(self, query):
        if not self.access_token:
            return False, {"detail": "Not authenticated"}

        try:
            response = requests.get(
                f"{BASE_URL}/api/search/",
                params={"q": query},
                headers={
                    "Authorization": f"Bearer {self.access_token}"
                },
                timeout=10,
            )

            if response.status_code != 200:
                try:
                    return False, response.json()
                except Exception:
                    return False, {
                        "detail": response.text
                    }

            return True, response.json()

        except Exception as e:
            return False, {
                "detail": str(e)
            }
            
    def follow_user(self, user_id):
        if not self.access_token:
            return False, {"detail": "Not authenticated"}

        try:
            response = requests.post(
                f"{BASE_URL}/api/users/{user_id}/follow/",
                headers={
                    "Authorization": f"Bearer {self.access_token}"
                },
                timeout=10,
            )

            if response.status_code != 200:
                try:
                    return False, response.json()
                except Exception:
                    return False, {
                        "detail": response.text
                    }

            return True, response.json()

        except Exception as e:
            return False, {
                "detail": str(e)
            }


    def unfollow_user(self, user_id):
        if not self.access_token:
            return False, {"detail": "Not authenticated"}

        try:
            response = requests.delete(
                f"{BASE_URL}/api/users/{user_id}/follow/",
                headers={
                    "Authorization": f"Bearer {self.access_token}"
                },
                timeout=10,
            )

            if response.status_code != 200:
                try:
                    return False, response.json()
                except Exception:
                    return False, {
                        "detail": response.text
                    }

            return True, response.json()

        except Exception as e:
            return False, {
                "detail": str(e)
            }