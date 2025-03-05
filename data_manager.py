import json
import os
from datetime import datetime
import hashlib

class DataManager:
    def __init__(self):
        """Initialize file paths and storage."""
        self.users_file = "users.json"
        self.progress_file = "progress.json"
        self.topics_file = "topics.json"
        self.deadlines_file = "deadlines.json"
        self._initialize_storage()

    def _hash_password(self, password):
        """Hash password using SHA-256"""
        return hashlib.sha256(password.encode()).hexdigest()

    def _initialize_storage(self):
        """Ensure necessary files exist and initialize admin user"""
        admin_password = "125Nasir"
        admin_hash = self._hash_password(admin_password)

        # Initialize users file
        if not os.path.exists(self.users_file):
            with open(self.users_file, 'w') as f:
                json.dump({"MdNasir": {"password": admin_hash, "role": "admin"}}, f, indent=4)

        # Initialize other files if missing
        for file in [self.progress_file, self.topics_file, self.deadlines_file]:
            if not os.path.exists(file):
                with open(file, 'w') as f:
                    json.dump({}, f, indent=4)

    def save_user(self, username, password, role="student"):
        """Save a new user"""
        users = self._load_json(self.users_file)
        users[username] = {"password": self._hash_password(password), "role": role}
        self._save_json(self.users_file, users)

    def get_user(self, username):
        """Retrieve user details"""
        users = self._load_json(self.users_file)
        return users.get(username)

    def get_topics(self, track):
        """Return topics for a given track (Data Analyst or Data Scientist)"""
        data = self._load_json(self.topics_file)
        return data.get(track, {})

    def save_progress(self, username, track, topic, subtopic, progress):
        """Save student progress"""
        all_progress = self._load_json(self.progress_file)

        if username not in all_progress:
            all_progress[username] = {}

        if track not in all_progress[username]:
            all_progress[username][track] = {}

        if topic not in all_progress[username][track]:
            all_progress[username][track][topic] = {}

        all_progress[username][track][topic][subtopic] = {
            "progress": progress,
            "timestamp": datetime.now().isoformat()
        }

        self._save_json(self.progress_file, all_progress)

    def get_student_progress(self, username):
        """Retrieve student progress"""
        all_progress = self._load_json(self.progress_file)
        return all_progress.get(username, {})

    def save_deadline(self, username, track, topic, deadline):
        """Save deadlines"""
        all_deadlines = self._load_json(self.deadlines_file)

        if username not in all_deadlines:
            all_deadlines[username] = {}

        if track not in all_deadlines[username]:
            all_deadlines[username][track] = {}

        all_deadlines[username][track][topic] = {
            "deadline": deadline,
            "timestamp": datetime.now().isoformat()
        }

        self._save_json(self.deadlines_file, all_deadlines)

    def get_deadlines(self, username):
        """Retrieve deadlines"""
        all_deadlines = self._load_json(self.deadlines_file)
        return all_deadlines.get(username, {})

    def _load_json(self, file_path):
        """Load JSON file safely"""
        try:
            with open(file_path, 'r') as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return {}

    def _save_json(self, file_path, data):
        """Save JSON data safely"""
        with open(file_path, 'w') as f:
            json.dump(data, f, indent=4)
