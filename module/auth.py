import json
import os
import hashlib
import uuid


class AuthManager:
    def __init__(self, file_path="data/users.json"):
        self.file_path = file_path
        self.users = {}
        self.current_user = None
        self._load_users()

    # -------------------- FILE HANDLING --------------------

    def _load_users(self):
        """Load users from JSON file"""
        if os.path.exists(self.file_path):
            with open(self.file_path, "r") as file:
                try:
                    self.users = json.load(file)
                except json.JSONDecodeError:
                    self.users = {}
        else:
            self._save_users()

    def _save_users(self):
        """Save users to JSON file"""
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)
        with open(self.file_path, "w") as file:
            json.dump(self.users, file, indent=4)

    # -------------------- PASSWORD SECURITY --------------------

    def _hash_password(self, password, salt=None):
        """Hash password with salt"""
        if not salt:
            salt = uuid.uuid4().hex

        hashed = hashlib.sha256((password + salt).encode()).hexdigest()
        return hashed, salt

    # -------------------- AUTH FUNCTIONS --------------------

    def signup(self, username, password):
        """Register a new user"""
        if username in self.users:
            raise ValueError("Username already exists")

        if len(password) < 6:
            raise ValueError("Password must be at least 6 characters long")

        hashed_password, salt = self._hash_password(password)

        self.users[username] = {
            "password": hashed_password,
            "salt": salt
        }

        self._save_users()
        return True

    def login(self, username, password):
        """Login user"""
        user = self.users.get(username)

        if not user:
            raise ValueError("User not found")

        hashed_password, _ = self._hash_password(password, user["salt"])

        if hashed_password != user["password"]:
            raise ValueError("Invalid password")

        self.current_user = username
        return True

    def logout(self):
        """Logout current user"""
        self.current_user = None

    def get_current_user(self):
        """Return current logged-in user"""
        return self.current_user

    # -------------------- USER MANAGEMENT --------------------

    def delete_user(self, username):
        """Delete a user account"""
        if username not in self.users:
            raise ValueError("User not found")

        del self.users[username]
        self._save_users()

        if self.current_user == username:
            self.logout()

    def change_password(self, username, old_password, new_password):
        """Change user password"""
        user = self.users.get(username)

        if not user:
            raise ValueError("User not found")

        # verify old password
        old_hashed, _ = self._hash_password(old_password, user["salt"])
        if old_hashed != user["password"]:
            raise ValueError("Incorrect old password")

        # set new password
        new_hashed, new_salt = self._hash_password(new_password)
        user["password"] = new_hashed
        user["salt"] = new_salt

        self._save_users()
        return True

