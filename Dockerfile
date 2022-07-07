FROM python:3.9-alpine3.13
LABEL maintainer="andreworellano"

# prints directly to console? not sure what this means
ENV PYTHONUNBUFFERED 1

# copies requirements txt from local host to docker env
COPY ./requirements.txt /tmp/requirements.txt
# copies another requirements txt folder to a temp folder this one is only for dev envs
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
# local app files to docker app files
COPY ./app /app
# when running docker commands will run from this directory instead of setting full path
WORKDIR /app
# expose port 8000 from container to localhost
EXPOSE 8000

# setting a default value that DEV is false, in the docker-compose file we are overriding that with TRUE
ARG DEV=false
# runs when docker container is spun up
# python -m venv /py creates a virtual environment for python dependencies - not necessariliy needed but it helps with edge cases
RUN python -m venv /py && \
    # upgrades pip in venv
    /py/bin/pip install --upgrade pip && \
    # installs requirements inside docker image --> venv
    /py/bin/pip install -r /tmp/requirements.txt && \
    # an if statement that looks for true and then installs dev requirements (flake8 linting)
    if [ $DEV = "true" ]; \
        then /py/bin/pip install -r /tmp/requirements.dev.txt ; \
    # shell scripting fi = if backwards to end the if loop
    # starting to think that && \ is another way to execute another line of code?
    fi && \
    # executes a rm of the /tmp directory where we temporarily stored the requirements txt copied from localhost
    rm -rf /tmp && \
    # creates a user within the alpine container **avoid using container as root user**
    # helps against hackers gaining root access
    adduser \
        # this is the username, can be anything but in this case we're using this container for django so django-user makes sense
        # django-user \
        # no pw access, can only be access when you're logging in through the app
        --disabled-password \
        # don't create a home directory C:/users/orell for example
        --no-create-home \
        # this is the username, can be anything but in this case we're using this container for django so django-user makes sense
        django-user
   
    # addgroup -S -g 9999 bob && \
    # adduser -S -u 9999 -g bob bob

# updates environment variable in the container
# updating the path where executables can be run 
# this is here because we created a venv, don't want to specifiy the path /py/bin anytime we run code so added it to path
ENV PATH="/py/bin:$PATH"

# up until this point everything is being executed as the root user
# now this command switches our access to user (instead of root which we want to avoid)
# USER django-user

USER django-user

# make sure that when you spin this up it's from the right place. If your app is running on docker-compose use docker-compose not docker [ docker build .] :)