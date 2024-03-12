import requests
from URLS import urls


class TokenGenerator:

    @staticmethod
    def generate_new_token():
        headers = {'Content-Type': 'application/json'}
        request_body_create = {
            "username": "admin",
            "password": "password123"
        }
        response_create = requests.post(urls.AUTH_URL, headers=headers, json=request_body_create)
        assert response_create.status_code == 200
        return response_create.json()["token"]
#
# if __name__ == "__main__":
#     my_token = TokenGenerator.generate_new_token()
#     print(f"Generated token: {my_token}")


# import requests
#
# class TokenGenerator:
#     _token = None  # Class variable to store the token
#
#     @classmethod
#     def get_token(cls):
#         if cls._token is None:
#             cls._token = cls._generate_new_token()
#         return cls._token
#
#     @staticmethod
#     def _generate_new_token():
#         # Set the authentication URL
#         AUTH_URL = urls.AUTH_URL # Replace with your actual URL
#
#         # Define the request body
#         request_body_create = {
#             "username": "admin",
#             "password": "password123"
#         }
#
#         # Make the POST request
#         headers = {'Content-Type': 'application/json'}
#         response_create = requests.post(AUTH_URL, headers=headers, json=request_body_create)
#
#         # Ensure a successful response
#         assert response_create.status_code == 200
#
#         # Extract the token from the response
#         return response_create.json()["token"]

# Example usage
# if __name__ == "__main__":
#     my_token = TokenGenerator.get_token()
#     print(f"Generated token: {my_token}")

