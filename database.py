class ContextManager:
    def __init__(self):
        self.storage = {}

    def get_context(self, user_id):
        if user_id not in self.storage:
            self.storage[user_id] = []
        return self.storage[user_id]

    def add_message(self, user_id, role, content):
        if user_id not in self.storage:
            self.storage[user_id] = []
        self.storage[user_id].append({"role": role, "content": content})

    def reset_context(self, user_id):
        self.storage[user_id] = []

db = ContextManager()