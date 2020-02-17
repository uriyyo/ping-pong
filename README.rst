.. raw:: html

    <h1 align="center">Ping Pong</h1>

    <p align="center">
        <img alt="Screenshot" src="/rsrs/screen.png"></a>
    </p>

General Information
-------------------

Classic ping pong game writen using ``python`` and ``pygame``.

There are two game mods:
* single-player
* multi-player

Installation
------------

.. raw:: bash

    $ pip install git+https://github.com/uriyyo/ping-pong

Example of usage
----------------

To start ``single-player``:

.. raw:: bash

    $ ping-pong-singleplayer


To start ``multi-player``:

.. raw:: bash

    # Start server
    $ ping-pong-multiplayer --server --port=8000

    $ Start client
    $ ping-pong-multiplayer --host=${ADDRESS_SERVER} --port=8000
