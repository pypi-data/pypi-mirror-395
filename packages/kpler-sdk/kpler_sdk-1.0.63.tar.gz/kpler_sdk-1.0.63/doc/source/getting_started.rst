Getting started
***************

Setup
-----

Supported Python: ``3.9``, ``3.10``, ``3.11``, ``3.12`` and ``3.13``

.. code-block::
   :linenos:

    pip install kpler.sdk

Upgrade an existing installation:

.. code-block::
   :linenos:

   pip install kpler.sdk --upgrade

You can be notified about new available Python SDK versions via a log message at each ``Configuration`` object creation.
In order to see that log message, you must set the log level to Info :

.. code-block:: python
   :linenos:

   config = Configuration(Platform.Liquids, "<your email>", "<your password>", log_level="INFO")

Example of update message :
``"A new versions 1.2.3 is available, please upgrade the Kpler SDK."``



Authentication
--------------

Create a ``Configuration`` with the targeted ``Platform``, your ``email`` and ``password`` to pass it to the client:

.. code-block:: python
   :linenos:


   from kpler.sdk.configuration import Configuration
   from kpler.sdk import Platform
   config = Configuration(Platform.Liquids, "<your email>", "<your password>")

   from kpler.sdk.resources.trades import Trades
   trades_client = Trades(config)

Available platforms:

   - ``LNG``
   - ``LPG``
   - ``Dry``
   - ``Liquids``


Access behind a proxy
---------------------

Proxies configuration can be passed to the ``Configuration`` as an additional dict parameter:

.. code-block:: python
   :linenos:

   proxies = {
      "http" : "http:////proxy.mycompany.com:1234",
      "https" : "http:////proxy.mycompany.com:1234"
   }

   config = Configuration(Platform.Liquids, "login", "password", proxies)


SSL troubleshooting
-------------------

If you're experiencing SSL issues, you can try one of the following :

Client side certificates
________________________

You can specify your own certificate, as a single file (containing the private key and the certificate) or as a tuple of both files:

.. code-block:: python
   :linenos:

   cert=('/path/client.cert', '/path/client.key')
   config = Configuration(Platform.Liquids, "login", "password", certificate=cert)


Disable SSL verification
________________________

**Disclaimer : the certificate verification is made to prevent man-in-the-middle attacks, use it at your own risks.**

You can disable ssl verification :

.. code-block:: python
   :linenos:

   config = Configuration(Platform.Liquids, "login", "password", verify=False)


Set request timeout duration
----------------------------

Unless specified, there is no timeout by default. You can specify a timeout duration (in seconds) for your requests:

.. code-block:: python
   :linenos:

   config = Configuration(Platform.Liquids, "login", "password", timeout=60)
