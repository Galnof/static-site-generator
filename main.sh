# Shell script that hosts the site on a local server.
python3 src/main.py
cd docs && python3 -m http.server 8888
