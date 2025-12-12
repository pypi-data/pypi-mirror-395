guillotina_nuclia – Quick Setup
================================

This package lets your Guillotina instance talk to **Nuclia**.
Below is the only thing you have to do: drop the utility in ``app_settings``
and export your credentials.

Install
-------

.. code-block:: bash

    pip install guillotina_nuclia

Configure the Nuclia utility
----------------------------

These are the settings regarding nuclia already configured in the package.
You mostly need to set up the next env variables: NUA_KEY, APIKEY, KBID, GENERATIVE_MODEL

.. code-block:: python

    import os

    app_settings = {
        "load_utilities": {
            "nuclia": {
                # interface that the utility will provide
                "provides": "guillotina_nuclia.utility.INucliaUtility",
                # dotted path to the factory
                "factory": "guillotina_nuclia.utility.NucliaUtility",
                # parameters forwarded to the factory
                "settings": {
                    # which LLM model Nuclia will use for generative answers
                    "generative_model": os.environ.get("GENERATIVE_MODEL", "chatgpt4o"),
                    # your personal Nuclia key (required)
                    "nua_key": os.environ.get("NUA_KEY"),
                    # hard limit for tokens (optional)
                    "max_tokens": os.environ.get("MAX_TOKENS"),
		    # Nuclia's API KEY
		    "apikey": os.environ.get("APIKEY"),
		    # Knowledge Box ID
		    "kbid": os.environ.get("KBID", ""),
		    
                },
            }
        }
    }

Set the environment variables
-----------------------------

.. list-table:: Environment variables
   :header-rows: 1

   * - Variable
     - Required
     - Example value
     - Description
   * - ``NUA_KEY``
     - **Yes**
     - ``nua_pk_live_…``
     - API token generated in the Nuclia dashboard.
   * - ``GENERATIVE_MODEL``
     - No
     - ``chatgpt4o`` (default)
     - LLM used for ``ask`` / ``predict``.
   * - ``MAX_TOKENS``
     - No
     - ``2048``
     - Maximum tokens per answer.

Export them before launching Guillotina:

.. code-block:: bash

    export NUA_KEY=\"nua_pk_live_your_token_here\"
    export KBID=\"Knwoledge box id\"
    export API_KEY=\"Nuclia's api key\"
    export GENERATIVE_MODEL=\"chatgpt4o\"   # optional
    export MAX_TOKENS=2048                 # optional

Done!
-----

Start Guillotina as usual—``INucliaUtility`` is now available
everywhere and the built-in routes POST (``@NucliaAsk``,
``@NucliaFind``, ``@NucliaPredict``, ``@NucliaSearch``,
``@NucliaAskStream``, etc.) will automatically work.

❤️  Happy coding!
