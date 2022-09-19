
# ValVault

This python module stores the user credentials of riot users and also provides the riot auth api in one simple package so it can be used in multiple projects.

## Usage/Examples

```python
from ValVault import (
 init as init_auth,
 makeHeaders,
 getUsers,
 getPass,
 getAuth,
 newUser,
 User
)

init_auth()
newUser("Test", "Password")
username = getUsers()[0]
user = User(username, getPass(username))
auth = getAuth(user)
headers = makeHeaders(auth)
#Use auth headers to do whatever
```
