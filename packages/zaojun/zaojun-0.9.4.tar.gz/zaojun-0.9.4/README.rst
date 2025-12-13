""""""""""""""""""""""""""
zaojun
""""""""""""""""""""""""""

|Repo| |CI| |Downloads|

|PySentry| |uv-secure| |CodeLimit|

|Codestyle| |Version| |Wheel|

|AGPL|



zaojun is a command line (CLI) tool to check versions of your dependencies as defined in `pyproject.toml`
file against the latest version published on `PyPi`_

Install and run from `Source <https://codeberg.org/marvin8/zaojun>`_
==============================================================================================

Alternatively you can run zaojun from source by cloning the repository using the following command line::

    git clone https://codeberg.org/marvin8/zaojun.git

zaojun uses `uv`_ for dependency control, please install UV before proceeding further.

Before running, make sure you have all required python modules installed. With uv this is as easy as::

    uv sync

Run zaojun with the command `uv run zaojun`

As a `pre-commit`_ hook
=========================

To run zaojun as a `pre-commit`_ hook, just add the below snippet into your `.pre-commit-config.yaml` file:

.. code-block:: yaml

   - repo: https://codeberg.org/marvin8/zaojun
   rev: 0.9.0
   hooks:
     - id: zaojun
       args:
       - "--groups"


Significance of Name zaojun
===========================

Zao Jun is the Chinese god that acts as a household guardian, overseeing domestic harmony and reporting family conduct to the heavens—reinforcing moral behavior within the kin unit.
This tool tries to keep your project and its dependencies in harmony. It doesn't do any reporting to third parties though :)

I know is a little far fetched, but I like it, so there :)

If you'd like to go down the rabbit hole of learning more about Zao Jun, the Chinese kitchen god, you can follow these links:

   - `Wikipedia`_
   - `Columbia University`_

.. _Wikipedia: https://en.wikipedia.org/wiki/Kitchen_God
.. _Columbia University: https://afe.easia.columbia.edu/cosmos/prb/earthly.htm


Licensing
=========
zaojun is licensed under the `GNU Affero General Public License v3.0 <http://www.gnu.org/licenses/agpl-3.0.html>`_

Supporting zaojun
==============================

There are a number of ways you can support zaojun:

- Create an issue with problems or ideas you have with/for zaojun
- Create a pull request if you are more of a hands on person.
- You can `buy me a coffee <https://www.buymeacoffee.com/marvin8>`_.
- You can send me small change in Monero to the address below:

Monero donation address
-----------------------
``88xtj3hqQEpXrb5KLCigRF1azxDh8r9XvYZPuXwaGaX5fWtgub1gQsn8sZCmEGhReZMww6RRaq5HZ48HjrNqmeccUHcwABg``


.. _uv: https://docs.astral.sh/uv/

.. _pre-commit: https://pre-commit.com

.. _PyPi: https://pypi.org

.. |AGPL| image:: https://img.shields.io/pypi/l/zaojun
   :alt: Licensed: AGPL 3.0 or later
   :target:  https://codeberg.org/marvin8/zaojun/src/branch/main/LICENSE.md

.. |Repo| image:: https://img.shields.io/badge/repo-Codeberg.org-blue
   :alt: Repo at Codeberg.org
   :target: https://codeberg.org/marvin8/zaojun

.. |PySentry| image:: https://img.shields.io/badge/PySentry-Checked-green
   :alt: Checked with PySentry
   :target: https://pysentry.com

.. |uv-secure| image:: https://img.shields.io/badge/uv--secure-checked-green
   :alt: Checked with uv-secure
   :target: https://github.com/owenlamont/uv-secure

.. |CI| image:: https://ci.codeberg.org/api/badges/13971/status.svg
   :alt: CI / Woodpecker
   :target: https://ci.codeberg.org/repos/13971

.. |CodeLimit| image:: https://img.shields.io/badge/CodeLimit-checked-green.svg
   :target: https://github.com/getcodelimit/codelimit

.. |Downloads| image:: https://img.shields.io/pepy/dt/zaojun
   :alt: Pepy Total Downloads

.. |Codestyle| image:: https://img.shields.io/badge/Codestyle-Ruff-green
   :alt: Code formated with ruff
   :target: https://docs.astral.sh/ruff/

.. |Version| image:: https://img.shields.io/pypi/pyversions/zaojun
   :alt: PyPI - Python Version

.. |Wheel| image:: https://img.shields.io/pypi/wheel/zaojun
   :alt: PyPI - Wheel
