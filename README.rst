.. raw:: html

    <h1 align="center">Ping Pong</h1>

    <p align="center">
        <img alt="Screenshot" src="rsrc/screen.png"></a>
    </p>

General Information
-------------------

Classic ping pong game writen using ``python`` and ``pygame``.

There are two game mods:
* single-player
* multi-player

Installation
------------

.. code-block:: bash

    $ pip install git+https://github.com/uriyyo/ping-pong

Example of usage
----------------

To start ``single-player``:

.. code-block:: bash

    $ ping-pong-singleplayer


To start ``multi-player``:

.. code-block:: bash

    # Start server
    $ ping-pong-multiplayer --server --port=8000

    # Start client
    $ ping-pong-multiplayer --host=${SERVER_ADDRESS} --port=8000
