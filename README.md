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
    "otp_id":"otp-123"
}
```
and an OTP will be send (now it's logged).
With the `OTP ID` and the `OTP VALUE` it's possible to get the JWT token calling the `/otp-token`.



## Run applications (Docker)
Build the image
```sh
docker build -t auth-service .
```
run the container
```sh
docker run -d --name auth-service -p 8000:8000 auth-service
```
run the container with mounted volume
```sh
docker run -d --name auth-service -p 8000:8000 -v "$(pwd)/container:/code/data" auth-service
```
watch the container log
```sh
docker container logs --follow auth-service
```

## Endpoint documentation
After start the image you should be able to get the Swagger documentation page.
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
By default two files will be created under the data folder. If you want change some configuration you can update the `.env` file.

## Implemantion notes

### Tests
There are two types of tests: unit and integration.
The intergation test are marked `integration`.
Coverange: 89%.

### API
It's used Fastapi to expose the enpoint.

### Peristence
The persistence is implemented using a file and at starting time all values are loaded in memory.
Since all persistence classes are only implementation from abstract class(`UserStore`, `OtpStore`) and in the usecases dependes only from the abstract class is easy to use a different implementation (Using a relational db or a NOSql db).

### OTP Email
The email is a faker implementation that logs on a stdout.
Ex.
```
INFO 2023-07-16 13:22:44,488  Sent email to: antonio@test.it - subject: OTP - body: Hi antonio, the OTP is 74919
```
