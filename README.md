
# ValVault

[![PyPI - Version](https://img.shields.io/pypi/v/ValVault?label=ValVault)](https://pypi.org/project/ValVault/)
![GitHub deployments](https://img.shields.io/github/deployments/ValUtils/ValVault/deploy?label=deploy)
![GitHub](https://img.shields.io/github/license/ValUtils/ValVault)

This python module stores the user credentials of riot users and also provides the riot auth api in one simple package so it can be used in multiple projects.

## Features

- Full auth flow
- Request helpers
- Basic endpoints for Valorant
- Captcha "bypass" without using external services
- Ability to use external Captcha solvers

## Installation

The prefered method of instaltion is through `pip` but if you know better use the package manager that you want.

```sh
pip install ValVault
```

## Reference

### Ussage

#### For terminal applications

The `terminal` module in `ValVault` is special for terminal applications since it has loose methods and it has a built-in password input.

```python
from ValVault import terminal as Vault

Vault.init_auth()
Vault.new_user("Test", "Password")
username = Vault.get_users()[0]
user = User(username, Vault.get_pass(username))
auth = Vault.get_auth(user)
```

#### For other applications

If you want to implement your own password prompt or need to use a GUI you should use the class directly.

```python
import ValVault

db_password = "MySecret"
db = ValVault.EncryptedDB(db_password)
entry = db.save_user("Test", "Password")
auth = db.get_auth(entry.username)
```

### Structure

#### Basic

`ValVault` is based off `ValLib` thus some DataClasses are shared like:

- `User` a dataclass containing username and password
- `Auth` a dataclass containing ever auth param

If you want to read more about ValLib go [here](https://github.com/ValUtils/ValLib)

`ValVault` contains:

- `Entry` a custom DataClass to make database compabilty easier that contains all info about an user
- `EncryptedDB` a class to handle the database

#### Terminal

`ValVault.terminal` contains the following methods:

- `init_vault` to setup the Vault and promt the user for the password
- `get_auth` provided an `User` get authenticated
- `get_users` get all usernames
- `get_aliases` get all alias
- `get_name` get the username of a given alias
- `set_alias` set the alias of a user
- `new_user` add an user to the Vault

#### Class

The `EncryptedDB` contains the following methods:

- `save_user` to add or modify an user
- `find` to find several entries
- `find_one` to find only one entry
- `get_auth` to get the auth for a given username
- `fix_database` to fix broken entries in the database

And the following properties:

- `entries` a list of every `Entry`
- `users` a list of all usernames
- `aliases` a list of all aliases

## Roadmap

- [ ] Async (?)
- [ ] More user properties
- [ ] Better documentation
- [ ] Better auth

## Running Tests

Tests need to be run in a development enviroment with GUI, a navigator, `pytest` and filling this enviroment variables.

```sh
USERNAME="TestUser"
PASSWORD="TestPassword"
```

And then running `pytest`.

## Acknowledgements

- Thanks to [Techdoodle](https://github.com/techchrism) for his API docs
- Thanks to the Valorant App Developers discord
