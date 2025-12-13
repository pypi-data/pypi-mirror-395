# form_guard
Prevent users from submitting the same form data within a cooldown period.

## Usage
```python
from form_guard import FormGuard

guard = FormGuard(300)

user_id = 123
data = {"email": "test@example.com"}

if guard.is_allowed(user_id, data):
    print("Allowed")
else:
    print("Duplicate — blocked")
