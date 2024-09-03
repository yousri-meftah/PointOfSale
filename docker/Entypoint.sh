echo 'Running Migrations'
alembic upgrade head



echo 'Running Server'
if [[ $ENVIRONMENT == "PRODUCTION" ]]; then
  python src/main.py
else
  python src/main.py
fi