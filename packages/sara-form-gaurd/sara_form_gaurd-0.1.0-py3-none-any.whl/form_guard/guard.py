import time
import hashlib

class FormGuard:
    def __init__(self, cooldown_seconds=300, store=None):
        self.cooldown = cooldown_seconds
        self.store = store if store is not None else {}

    def _make_key(self, user_id, form_data):
        raw = f"{user_id}-{form_data}"
        return hashlib.sha256(raw.encode()).hexdigest()

    def is_allowed(self, user_id, form_data):
        key = self._make_key(user_id, form_data)
        now = time.time()
        ts = self.store.get(key)
        if ts and now - ts < self.cooldown:
            return False
        self.store[key] = now
        return True
