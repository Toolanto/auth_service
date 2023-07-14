# Auth Service

Is a simple service that allows to register and login a user.
At the registration time a user can choose to enable the 2FA (property `two_factor_auth_enabled`). 

If a user has the 2FA disabled the `/login` endpoint returns the following json:
```sh
{
    "token":"a JWT token"
}
```
If the 2FA is enabled the response will be:
```sh
{
    "session_id":"session_id"
}
```
and an OTP will be send (now it's logged).
With the `session_id` and the `OTP` it's possible to get the JWT token calling the `/otp-token`.

The endpoint documentation is under
```
http://localhost:8000/docs
```

## Run applications (Docker)
Build the image
```sh
docker build -t auth-service .
```
run the container
```sh
docker run -d --name auth-service -p 8000:8000 auth-service
```
run the container with mounted volum
```sh
docker run -d --name auth-service -p 8000:8000 -v "$(pwd)/container:/code/data" auth-service 
```
watch the container log
```sh
docker container logs --follow auth-service
```

You should be able to get the documentation page
```
http://localhost:8000/docs
```
![Home](https://drive.google.com/uc?id=1dJaTeGsAjRUicMdxRq4I2LQm8eg6m2zX)

## Requests example

## Develop setup 🔨
### Prerequisites
This repo assumes that are [pyenv](https://github.com/pyenv/pyenv) and [poetry](https://python-poetry.org/) are already installed.

### Install
- clone the repo and cd into
- active a compatible python version `pyenv local 3.9.5`
- install the repo with all its dependencies: `make install`

### Run test
```
make test
```
### Run unit test
```
make test-unit
```
### Run in local
```
make dev
```

By default two file will be created under the data

## NOTE

The user and otp informations are store in two files and they are loaded at starting time in memory.
Different implementations could be used extend the two abstract classes `UserStore` and `OtpStore`.


By now the Otp email is only logged on the stdout.