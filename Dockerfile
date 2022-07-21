FROM python:3.9

# Set the following environmental variables
ENV REACT_APP_BASE_URL=https://isntagram_app.herokuapp.com
ENV FLASK_APP=app
ENV FLASK_ENV=production
ENV SQLALCHEMY_ECHO=True

# Set the directory for upcoming commands to /var/www
WORKDIR /var/www

# Copy all the files from your repo to the working directory
COPY . .

# Copy the built react app from the /react-app/build directory
# into the app/static directory
COPY /react-app/build/* app/static/

# Install Python Dependencies
RUN pip install -r requirements.txt
RUN pip install psycopg2

# Run flask environment
CMD [ "gunicorn", "app:app" ]
