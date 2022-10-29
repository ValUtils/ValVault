
# ValVault

This python module stores the user credentials of riot users and also provides the riot auth api in one simple package so it can be used in multiple projects.

## Usage/Examples

```python
from ValVault import (
 init as init_auth,
 make_headers,
 get_users,
 get_pass,
 get_auth,
 new_user,
 User
)

init_auth()
new_user("Test", "Password")
username = get_users()[0]
user = User(username, get_pass(username))
auth = get_auth(user)
headers = make_headers(auth)
#Use auth headers to do whatever
```
