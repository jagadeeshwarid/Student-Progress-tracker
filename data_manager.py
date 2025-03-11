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
        self.user_data_file = "user_data.json"
        self._initialize_storage()

    def _initialize_storage(self):
        """Ensure necessary files exist with proper structure"""
        files = {
            self.users_file: {},
            self.progress_file: {},
            self.topics_file: self._get_default_topics(),
            self.deadlines_file: {},
            self.user_data_file: {}
        }

        for file_path, default_data in files.items():
            if not os.path.exists(file_path):
                self._save_json(file_path, default_data)

    def _get_default_topics(self):
        """Load default topics structure"""
        if os.path.exists(self.topics_file):
            return self._load_json(self.topics_file)
        return {
            "Data Analyst": {},
            "Data Scientist": {}
        }

    def save_user(self, username, hashed_password, role="student"):
        """Save a new user with hashed password"""
        try:
            users = self._load_json(self.users_file)
            users[username] = {
                "password": hashed_password,
                "role": role
            }
            self._save_json(self.users_file, users)
            print(f"Successfully saved user: {username}")  # Debug logging
            return True
        except Exception as e:
            print(f"Error saving user: {e}")
            return False

    def get_user(self, username):
        """Retrieve user details"""
        users = self._load_json(self.users_file)
        return users.get(username)

    def initialize_user_progress(self, username):
        """Initialize empty progress data for new user"""
        try:
            print(f"Initializing user progress for: {username}")  # Debug log

            # Initialize in user_data.json
            user_data = self._load_json(self.user_data_file)
            if username not in user_data:
                user_data[username] = {
                    "career_path": None,
                    "progress": {}
                }
                self._save_json(self.user_data_file, user_data)
                print(f"Created user data for: {username}")  # Debug log

            # Initialize in progress.json
            progress = self._load_json(self.progress_file)
            if username not in progress:
                progress[username] = {}
                self._save_json(self.progress_file, progress)
                print(f"Created progress data for: {username}")  # Debug log

            # Verify data was saved
            saved_user_data = self._load_json(self.user_data_file)
            saved_progress = self._load_json(self.progress_file)
            print(f"Verification - User data exists: {username in saved_user_data}")
            print(f"Verification - Progress data exists: {username in saved_progress}")

            return True
        except Exception as e:
            print(f"Error initializing user progress: {e}")
            return False

    def get_topics(self, track):
        """Return topics for a given career track"""
        topics = self._load_json(self.topics_file)
        return topics.get(track, {})

    def save_progress(self, username, track, topic, subtopic, progress_value):
        """Save student progress with proper structure"""
        try:
            # Update progress.json
            progress_data = self._load_json(self.progress_file)
            if username not in progress_data:
                progress_data[username] = {}
            if track not in progress_data[username]:
                progress_data[username][track] = {}
            if topic not in progress_data[username][track]:
                progress_data[username][track][topic] = {}

            progress_data[username][track][topic][subtopic] = {
                "progress": progress_value,
                "timestamp": datetime.now().isoformat()
            }
            self._save_json(self.progress_file, progress_data)

            # Update user_data.json
            user_data = self._load_json(self.user_data_file)
            if username not in user_data:
                user_data[username] = {"career_path": track, "progress": {}}

            progress_key = f"{track}_{topic}_{subtopic}"
            user_data[username]["progress"][progress_key] = {
                "completion": progress_value,
                "timestamp": datetime.now().isoformat()
            }
            self._save_json(self.user_data_file, user_data)

            return True
        except Exception as e:
            print(f"Error saving progress: {e}")
            return False

    def get_student_progress(self, username):
        """Retrieve student progress"""
        print(f"Getting progress for student: {username}")  # Debug log
        progress_data = self._load_json(self.progress_file)
        progress = progress_data.get(username, {})
        print(f"Found progress data: {bool(progress)}")  # Debug log
        return progress

    def get_all_students_progress(self):
        """Retrieve progress data for all students"""
        return self._load_json(self.progress_file)

    def _load_json(self, file_path):
        """Load JSON file safely"""
        try:
            if os.path.exists(file_path):
                with open(file_path, 'r') as f:
                    content = f.read().strip()
                    return json.loads(content) if content else {}
            return {}
        except (FileNotFoundError, json.JSONDecodeError) as e:
            print(f"Error loading {file_path}: {e}")
            return {}

    def _save_json(self, file_path, data):
        """Save JSON data safely using atomic write"""
        temp_file = f"{file_path}.tmp"
        try:
            with open(temp_file, 'w') as f:
                json.dump(data, f, indent=4)
            os.replace(temp_file, file_path)
            print(f"Successfully saved {file_path}")  # Debug logging
        except Exception as e:
            print(f"Error saving {file_path}: {e}")
            if os.path.exists(temp_file):
                os.remove(temp_file)
            raise

    def update_career_path(self, username, career_path):
        """Update user's career path"""
        user_data = self._load_json(self.user_data_file)
        if username not in user_data:
            user_data[username] = {"progress": {}}
        user_data[username]["career_path"] = career_path
        self._save_json(self.user_data_file, user_data)