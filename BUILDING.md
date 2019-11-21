Developer information
=====================

To package python distribution and upload to test pypi from virtual environment containing wheel and twine:
```
pip install wheel twine
rm -R build dist bpss_prime_minister.egg-info
python setup.py sdist       # only required for source distribution
python setup.py bdist_wheel
twine upload --repository-url https://test.pypi.org/legacy/ dist/*.whl
```

To install from test pypi:

    pip install --index-url https://test.pypi.org/simple/ bpss_prime_minister==0.0.7

To upload to pypi:

    twine upload dist/*.whl

To install from pypi:

    pip install bpss_prime_minister

