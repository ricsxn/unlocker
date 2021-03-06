# unlocker

[![Documentation Status](https://readthedocs.org/projects/unlocker/badge/?version=latest)](https://unlocker.readthedocs.io/en/latest/?badge=latest)

Unlock your mac using bluetooth devices.

## Structure

This utility avoid the user to manually enter its password once its mac device goes in locking status.
It works discovering bluetooth device inside an infinite loop and as soon the mac is locked and one of the discovered device is present in the list of allowed devices, it will unlock the machine automatically.

## Configuration

Before to install the utility on your mac, it is needed to configure the devices and the password used to unlock the machine.
The current version is intended to run at user level and it uses just one passoword value configured inside a python file `config.py`. Precise instructions are available under **Installtion** chapter.

## Installation

Please use the following step to install the service on your mac. These installation steps assume that this software has been donloaded from GitHub with the `git clone` command and the working directory points to the extracted project directory.

### 1) Install `blueutil`

This version makes use of the `blueutil` application, since earlier implementations based on pybluez library, were extremely unstable.
The `blueutil` is available both for [brew](https://brew.sh) (recommended) or [MacPorts](https://www.macports.org), or even from source code. For more information, please visit the [`blueutil`](https://github.com/toy/blueutil) [GitHub](https://github.com) page.

These instructions assume brew as the source to install `blueutil` application.
Instructions to install brew are available [here](https://docs.brew.sh/Installation)

Once brew is installed, use the following command to install `blueutil`

```bash
brew install blueutil
```

### 2) Python requirements

Go in the source code folder and take care of python requirements

```bash
python3 -m venv ./venv
. ./venv/bin/activate
pip install -r requirements.txt
pip install pyobjc
```

**Attention** pjobjc is not included into requirements for compatibility purposes with readthedocs.

### 3) Generate the key to encrypt the password

This step has to be done only once and requires to edit the python code `genkey.py`. Inside that file configure at the top of the boolean value `gen_key` as shown below:

```python
gen_key = True
```

Then run the command:

```bash
./genkey.py
```

This operation will produce a private key file named `secret.key` used by the application to decrypy the encoded password while the service operates.

**Attention** It is suggested to make the key file only readable by your user with the command `chmod 400 secret.key`

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

/chmod

**Attention** The execution above will print on the terminal the password, be aware of that. After this operation it is also highly recommended to remove the password value from varialbe `gen_password`.

### 4) Configure devices and the password

To accomplish this step, you have to know the bluetooth address number and the device name associated to the device you would like to use to unlock your Mac. To discover these value, you may use the `blueutil` application, as explained below:

```bash
blueutil --inquiry
address: xx-xx-xx-xx-xx-xx, not connected, not favourite, not paired, name: "<device name>", recent access date: -
```

You can get values of **address** and **name** for respectively the device address and name to complete this step.

**Attention** do not forget to make your bluetooth device visibile while doing this step.

From the step avove, take the text of the encrypted password and create/open the `config.py` code and apply the changes as reported below:

```python
allowed_devices = [
    {"name": "<name of the bluetooth device>",
     "addr": b"<address of the bluetooth device>"},
]

user_credentials = {
    "user": "<your username (unused)",
    "password": b"<the password encrypted value>",
}
```

**Attention** The `user` field is not used, since this utility operates at user level.

### 5) Install the service

This is the last step and requires only to execute a bash script that will install the **unlocker** service on your mac automatically just executing:

```bash
./unlocker install
```

### 6) Take care of accessibility privilege

New mac OS releases, may require from **System Preferences** to enable: `Full Disk Access` and `Accessibility` privileges in **Security and Privacy/Privacy** for `/bin/bash` application. In case the unlocker is manually launched from the terminal, enable the same privileges for `Terminal` application.
Sometime the OS system will request to unlock automatically these privileges by follow the instructions provided by Mac OS attempting to use the utility but logging manually untile all necessary rights have been reached. However this procedure is not always successful.

**Attention** To monitor `unlocker` daemon activity, it is possible to open MacOS `console` application, select the system.log and filter by `ùnlocker` keyword. It is also possible to log `launchd` activity activating commented lines into the `it.ricsxn.unlocker.plist` file.

To monitor the `unlocker` internal activity, a log file named `unlocker.log` is generated. To configure the log behavior, just edit the file `logging.conf`. It is suggested to switch log levels to `INFO` rather than the default `DEBUG` value, which has to be used just for development/debugging purposes.

**Attention** iOS users may need to go on `Setting/Bluetooth` panel in order to make the device discoverable.
