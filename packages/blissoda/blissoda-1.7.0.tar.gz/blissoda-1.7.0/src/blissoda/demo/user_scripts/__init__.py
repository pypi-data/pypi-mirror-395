"""Scripts for the Bliss demo session.

Set the script home directory to the directory of the module  ``blissoda.demo.user_scripts``

.. code-block:: python

    DEMO_SESSION [1]: user_script_homedir_oda()

Load an ODA user script, for example ``all.py``

.. code-block:: python

    DEMO_SESSION [2]: user_script_load("all")
    Loading [/home/denolf/projects/blissoda/src/blissoda/demo/user_scripts/all.py]
    Exported [user] namespace in session.

Print all ODA processors

.. code-block:: python

    DEMO_SESSION [3]: user.all_print()

Run all integration tests

.. code-block:: python

    DEMO_SESSION [4]: user.all_demo()
"""
