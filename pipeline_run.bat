
echo "Installing dev dependencies"
pip install -r requirements-dev.txt

echo "Run linting"
flake8 sql_query_parser setup.py || goto :error

echo "Run type checking"
mypy --install-types --non-interactive sql_query_parser setup.py || goto :error

echo "Running tests"
coverage run --source=sql_query_parser -m pytest || goto :error
ECHO "Create HTML Coverage report"
coverage html || goto :error
ECHO "Coverage report"
coverage report --show-missing --skip-covered --skip-empty --omit="*test*,*exception*" || goto :error
goto :end

:error
echo Failed with error #%errorlevel%.
exit /b %errorlevel%

:end
echo Pipeline run succesfully
