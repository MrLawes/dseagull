# vim ~/.pypirc
# [distutils]index-servers=pypi

# [pypi]repository = https://upload.pypi.org/legacy/
# username = __token__
# password = pypi-yours

rm -rf dist
pytest
python3 -m pip install --upgrade build
python3 -m build
python3 -m twine upload --repository pypi dist/*

# todo ValidationError