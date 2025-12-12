## Adding new changes to the pip
**Add your code changes to __main__.py in gendoc and then do the following:**
1. Update the version number in setup.py
2. Run the following commands:
```ps
python setup.py sdist bdist_wheel
pip install --upgrade twine
twine upload dist/*
```
3. supply API token when asked
4. Done! Your package should be live on PyPI.