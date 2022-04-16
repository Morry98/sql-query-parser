pip install wheel twine
python setup.py clean --all sdist bdist_wheel
twine upload --repository codeartifact dist/*
pause
