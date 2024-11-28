from firebase_admin import auth, credentials, initialize_app

# Initialize Firebase Admin SDK with your service account key
cred = credentials.Certificate(r'C:\Users\dilll\Backend\backend\cleaning_app\credentials\neatnest-308c4-firebase-adminsdk-8bt91-be2f5d5a1b.json')
default_app = initialize_app(cred)

# Example Firebase ID token to verify (replace this with an actual Firebase token)
token = "eyJhbGciOiJSUzI1NiIsImtpZCI6IjkyODg2OGRjNDRlYTZhOThjODhiMzkzZDM2NDQ1MTM2NWViYjMwZDgiLCJ0eXAiOiJKV1QifQ.eyJpc3MiOiJodHRwczovL3NlY3VyZXRva2VuLmdvb2dsZS5jb20vbmVhdG5lc3QtMzA4YzQiLCJhdWQiOiJuZWF0bmVzdC0zMDhjNCIsImF1dGhfdGltZSI6MTczMjMyMjc5NywidXNlcl9pZCI6IjM0aUFySklkZXdYajRhQ2dmSjA0bHk1SGFUcDEiLCJzdWIiOiIzNGlBckpJZGV3WGo0YUNnZkowNGx5NUhhVHAxIiwiaWF0IjoxNzMyMzIyNzk3LCJleHAiOjE3MzIzMjYzOTcsImVtYWlsIjoiZmdoakBnbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6ZmFsc2UsImZpcmViYXNlIjp7ImlkZW50aXRpZXMiOnsiZW1haWwiOlsiZmdoakBnbWFpbC5jb20iXX0sInNpZ25faW5fcHJvdmlkZXIiOiJwYXNzd29yZCJ9fQ.FGNHYDwz7AHOM9o_Uj6EiDzlattQKB81I7px1LGcCgbYDr15kHLBRlyY45wlnjSfWkwuGEUnlDul9YKy8tVkMUH8LoxJqv_Of4O2eJM7j9u7r4b2wVB4FZLBb6vMtWtg8PTQR_XIlIPcSgm8ZmR8rss_XnI7JAJqELRZlxndylM17ddiJ8WVpFvyj0OmAIP5ZLczoBK5XGQGiMGoPHOf3GWiAt-kQ3cbKeMKAFhO4qSVl3q56L0oNrjpgWBGthVxnYqfPmcMCtLMhrpesXBT_TxeqDtEivNxz_IM0tka1f8iAwqttDM6ZxNi9qWtKYEZeFvHaXZfT5b63iy1ysutQQ"  # Replace this with a real Firebase ID token

try:
    decoded_token = auth.verify_id_token(token)
    print(decoded_token)  # This will print the decoded token if it's valid
except auth.InvalidIdTokenError:
    print("Invalid token!")
except auth.ExpiredIdTokenError:
    print("Token has expired!")
except Exception as e:
    print(f"Error verifying token: {e}")
