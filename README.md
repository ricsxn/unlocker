# unlocker

Unlock your mac using your bluetooth device.

## Structure

This utility avoid the user to manually enter its password once its mac device goes in locking status.
It works discovering bluetooth devices inside an infinite loop and as soon the mac is locked and one of the discovered device is present in the list of allowed devices, it will unlock the machine automatically.

## Configuration

Before to install the utility on yuor mac, it is needed to configure the devices and the encrypted password used to unlock the machine.
The current version is intended to run at user level and it uses just one passowrd value configured inside the `unlocker.py` code hold by the variable `user_credentials`.

```bash
user_credentials = {
    "user": "<your username>",
    "password": b"<your encrypyed password value>",
}
```

**Attention** Password value is encrypted in order to avoid placing a clear copy of your password in the filesystem. The `genkey.py` code does this for you.

## Installation

Please use the following step to install the service on your mac

### 1) Python requirements

Go in the source code folder and take care of python requirements

```bash
python3 -m venv ./venv3
. ./venv3/bin/activate
pip install -r requirements.txt
```

**Attention** One of the requirements is Quartz that may have problems with direct pip installation. In such case, please use the following instructions:

```bash
Run: pip download quartz
Find the downloaded quartz-0.0.1.dev0.tar.gz # Do not care if the installation does not complete
Extract the archive and inside the new directory locate the setup.py file, then find the following line:

install_requires=read_dependencies("requirements.txt")

changing it to:

install_requires=read_dependencies("quartz.egg-info/requires.txt")

then run:

pip install -e ./quartz-0.0.1.dev0
```

For more information on this phase, please visit [here](https://stackoverflow.com/questions/42530309/no-such-file-requirements-txt-error-while-installing-quartz-module).

### 2) Generate the key to encrypt the password

This step has to be done **only once** and it requires to edit the python code `genkey.py`. Inside that file, configure the boolean value `gen_key` as shown below:

```python
gen_key = True
```

Then run the command:

```bash
./genkey.py
```

This operation will produce a private key file named `secret.key` used by the application to decrypy the encoded password while the service operates. This file should have user only read permissions.

Now it is possible to generate and test the encrypted password value, opening again the `genkey.py` and applying the following changes:

```python
gen_key = False
gen_password = "<place here your password>"
```

Execute again the `genkey.py` code to generate the encrypted password value:

```bash
./genkey.py
encrypted message: b'... the password encrypted value ...'
dencrypted message: <... unencrypted password ...>
```

### 3) Configure devices and the password

From the step avove, take the text of the encrypted password and open the `unlocker4.py` code and apply the changes as reported below:

```python
allowed_devices = [
    {"name": "<name of the bluetooth device>",
     "addr": b"<address of the bluetooth device>"},
]

user_credentials = {
    "user": "<your username (unused)>",
    "password": b"<the password encrypted value>",
}
```

**Attention** the `user` field inside `user_credentials`dictionary is not used at the moment, the utility just use the `password` vaule.

Finally configure the lock only or lock/unlock feature, changing the boolean variable `lock_allowed`. When this variable is `True`, the system will lock automatcally if the bluetooth device is no longer discoverable.

**Attention** Some devices are discoverable just for a limited time (iOS devices), in this cases it is highly recommended to leave to `False` this value.

### 4) Install the service

This is the last step and requires only to execute a bash script that will install the **unlocker** service on your Mac automatically just executing:

```bash
./unlocker install
```

**Attention** New mac OS releases, may require to enable **accessibility** privilege to the `bash` application; please allow this otherwise the service will not work.

At this stage the utility should work.
