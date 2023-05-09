# build.sh

pip install -r requirements.txt

python3.9 -m pip install -r requirements.txt
python3.9 -m manage.py collectstatic --noinput

python3.9 -m manage.py makemigrations
python3.9 -m manage.py migrate
