Building and Deploying netmagus_python
--------------------------------------

The package uses ``pyproject.toml`` for all package definition and relies upon `uv
<https://docs.astral.sh/uv/>`_ for all operations.  **Install it first!**

----

To build the package:

1. Run ``uv build`` to create the resources in the ``./dist`` folder

To deploy package to test.pypi.org:

1. Run ``uv publish --publish-url https://test.pypi.org/legacy/`` to push to the test instance
2. View result at https://test.pypi.org/project/netmagus/
3. Install the test package into a fresh virtualenv for testing with ``pip install --index-url https://test.pypi.org/simple --extra-index-url https://pypi.org/simple netmagus``

To deploy to PyPi:

1. Run ``uv publish``
