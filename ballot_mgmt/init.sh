CONTAINER_ALREADY_STARTED="CONTAINER_ALREADY_STARTED_PLACEHOLDER"
if [ ! -e $CONTAINER_ALREADY_STARTED ]; then
    touch $CONTAINER_ALREADY_STARTED
    echo "-- First container startup --"
    python manage.py migrate
    python manage.py createsuperuser --no-input
else
    echo "-- Not first container startup --"
fi

python manage.py runserver 0.0.0.0:8000