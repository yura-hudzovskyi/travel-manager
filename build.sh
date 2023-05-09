# build.sh

pip install -r requirements.txt

python -m pip install -r requirements.txt
python -m manage.py collectstatic --noinput

python -m manage.py makemigrations
python -m manage.py migrate
