mypy --install-types --non-interactive lib main.py
flake8 lib main.py
coverage run -m pytest lib
coverage report --show-missing --skip-covered --skip-empty
