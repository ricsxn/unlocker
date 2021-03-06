Install
=======

Please use the following step to install the service on your mac. These installation steps assume that this software has been donloaded from GitHub with the `git clone` command and the working directory points to the extracted project directory.

1. Install `blueutil`
---------------------

This version makes use of the `blueutil` application, since earlier implementations based on pybluez library, were extremely unstable.
The `blueutil` is available both for `brew <https://brew.sh>`_ (recommended) or `MacPorts <https://www.macports.org>`_, or even from source code. For more information, please visit the `blueutil <https://github.com/toy/blueutil>`_ `GitHub <https://github.com>`_ page.

These instructions assume brew as the source to install `blueutil` application.
Instructions to install brew are available `here <https://docs.brew.sh/Installation>`_.

Once brew is installed, use the following command to install `blueutil`

.. code-block:: bash

    brew install blueutil

2. Python requirements
----------------------

Go in the source code folder and take care of python requirements

.. code-block:: bash

    python3 -m venv ./venv
    . ./venv/bin/activate
    pip install -r requirements.txt
    pip install pyobjc

**Attention** pjobjc is not included into requirements for compatibility purposes with readthedocs.

3. Generate the key to encrypt the password
-------------------------------------------

This step has to be done only once and requires to edit the python code `genkey.py`. Inside that file configure at the top of the boolean value `gen_key` as shown below:

.. code-block:: python

    gen_key = True


Then run the command:

.. code-block:: bash

    ./genkey.py


This operation will produce a private key file named `secret.key` used by the application to decrypy the encoded password while the service operates.

**Attention** It is suggested to make the key file only readable by your user with the command `chmod 400 secret.key`

Now it is possible to generate and test the encrypted password value, opening again the `genkey.py` and applying the following changes:

.. code-block:: python

    gen_key = False
    gen_password = "<place here your password>"

Execute again the `genkey.py` code to generate the encrypted password value:

.. code-block:: python

    ./genkey.py
    encrypted message: b'... the password encrypted value ...'
    dencrypted message: <... unencrypted password ...>


**Attention** The execution above will print on the terminal the password, be aware of that. After this operation it is also highly recommended to remove the password value from varialbe `gen_password`.

4. Configure devices and the password
-------------------------------------

To accomplish this step, you have to know the bluetooth address number and the device name associated to the device you would like to use to unlock your Mac. To discover these value, you may use the `blueutil` application, as explained below:

.. code-block:: bash

    blueutil --inquiry

address: xx-xx-xx-xx-xx-xx, not connected, not favourite, not paired, name: "<device name>", recent access date: -
You can get values of **address** and **name** for respectively the device address and name to complete this step.

**Attention** do not forget to make your bluetooth device visibile while doing this step.

From the step avove, take the text of the encrypted password and create/open the `config.py` code and apply the changes as reported below:

.. code-block:: python

    allowed_devices = [
        {"name": "<name of the bluetooth device>",
        "addr": b"<address of the bluetooth device>"},
    ]

    user_credentials = {
        "user": "<your username (unused)",
        "password": b"<the password encrypted value>",
    }


**Attention** The `user` field is not used, since this utility operates at user level.

5. Install the service
----------------------

This is the last step and requires only to execute a bash script that will install the **unlocker** service on your mac automatically just executing:

.. code-block:: bash

    ./unlocker install


6. Take care of accessibility privilege
---------------------------------------

New mac OS releases, may require to enable **accessibility** to both the `terminal` (in case the unlocker is manually launched from the terminal) and `bash`.
To allow these requests, it is necessary to lock the screen, use the device to unlock the machine, then login manually (because the unlocker will be halted), and follow the instructions provided by Mac OS to enable the **accessibility** privilege.

**Attention** To monitor `unlocker` daemon activity, it is possible to open MacOS `console` application, select the system.log and filter by `ùnlocker` keyword.

To monitor the `unlocker` internal activity, a log file named `unlocker.log` is generated. To configure the log behavior, just edit the file `logging.conf`. It is suggested to switch log levels to `INFO` rather than `DEBUG` which has to be used just for development purposes.

**Attention** IOS users may need to go on `Setting/Bluetooth` panel in order to make the device discoverable.
