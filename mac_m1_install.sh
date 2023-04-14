brew install sqlcipher sqlite
SQLCIPHER_PATH=$(brew --prefix sqlcipher) LIBRARY_PATH=/lib C_INCLUDE_PATH=/include pip install -r requirements.txt
