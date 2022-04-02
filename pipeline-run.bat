ECHO "Type checking with mypy"
mypy --install-types --non-interactive lib main.py || goto ERROR_HANDLING
ECHO "Coding style checking with flake8"
flake8 lib main.py || goto ERROR_HANDLING
ECHO "Running tests"
coverage run -m pytest lib || goto ERROR_HANDLING
ECHO "Coverage report"
coverage report --show-missing --skip-covered --skip-empty || goto ERROR_HANDLING
ECHO "Pipeline finished successfully"
goto END

: ERROR_HANDLING
ECHO "Pipeline failed"

: END
pause