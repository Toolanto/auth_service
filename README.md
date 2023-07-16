# Auth Service [![Version](https://img.shields.io/badge/version-1.0.0-<COLOR>.svg)](https://shields.io/)


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
With the `OTP ID` and the `OTP VALUE` it's possible to get the JWT token calling the `/otp-login`.


## Develop setup 🔨
### Prerequisites
This repo assumes that are [pyenv](https://github.com/pyenv/pyenv), [poetry](https://python-poetry.org/) and [docker-compose](https://docs.docker.com/compose/) are already installed.

### Install
- clone the repo and cd into
- active a compatible python version `pyenv local 3.9.5`
- install the repo with all its dependencies: `make install`

To run and test in local you need to start the docker-compose
```
docker-compose up
```

```
make install
```

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

## Endpoint documentation
After start the image you should be able to get the Swagger documentation page.
```
http://localhost:8000/docs
```
![Home](https://drive.google.com/uc?id=1dJaTeGsAjRUicMdxRq4I2LQm8eg6m2zX)

## Requests example

To test you can use the swagger page.

Here some curl request

### NO 2FA

#### Create user req
```sh
curl -X POST localhost:8000/users -H "Content-Type: application/json" -d '{"email":"test@email.com","password":"password123","name":"test"}'
```
```sh
{"email":"test@email.com","name":"test","last_name":null,"two_factor_auth_enabled":false}
```
#### Invalid credentials
```sh
curl -X POST localhost:8000/login -H "Content-Type: application/json" -d '{"email":"test@email.com","password":"password123fdc"}'
```
```sh
{"detail":"Invalid credentials"}
```
#### Get JWT
```sh
curl -X POST localhost:8000/login -H "Content-Type: application/json" -d '{"email":"test@email.com","password":"password123"}'
```
```sh
{"token":"...","otp_id":null}
```

### 2FA

#### Create user req
```sh
curl -X POST localhost:8000/users -H "Content-Type: application/json" -d '{"email":"test1@email.com","password":"password123","name":"test", "two_factor_auth_enabled":true}'
```
```sh
{"email":"test1@email.com","name":"test","last_name":null,"two_factor_auth_enabled":true}
```
#### Invalid credentials
```sh
curl -X POST localhost:8000/login -H "Content-Type: application/json" -d '{"email":"test1@email.com","password":"password123fdc"}'
```
```sh
{"detail":"Invalid credentials"}
```
#### Get OTP
```sh
curl -X POST localhost:8000/login -H "Content-Type: application/json" -d '{"email":"test1@email.com","password":"password123"}'
```
```sh
{"token":null,"otp_id":"861caa01-08e4-4476-97f7-163b59b0f64a"}
```
Email:
```
INFO 2023-07-16 22:13:13,349  Sent email to: test1@email.com - subject: OTP - body: Hi test, the OTP is 66399
```
#### Invalid OTP
```sh
curl -X POST localhost:8000/otp-login -H "Content-Type: application/json" -d '{"otp_id":"861caa01-08e4-4476-97f7-163b59b0f64a","otp_value":"invalid"}'
```
```sh
{"detail":"Invalid OTP"}
```

#### Get JWT
```sh
curl -X POST localhost:8000/otp-login -H "Content-Type: application/json" -d '{"otp_id":"861caa01-08e4-4476-97f7-163b59b0f64a","otp_value":"66399"}'
```
```sh
{"token":"...","otp_id":null}
```

## Build applications (Docker) and deploy in production.
Build the image
```sh
docker build -t auth-service .
```
run the container
```sh
docker run -d --name auth-service -p 8000:8000 -v "$(pwd)/.env:/code/.env" auth-service
```
Set the correct `.env` file to point the production postgres db.

## Implemantion notes

### Tests
There are two types of tests: unit and integration.
The intergation test are marked `integration`.
Coverange: 95%.

Even for unit and integration is needed to run the docker-compose because a db clean process is executed after every test.
It's possibile, in the future, to execute this process only after the integration tests.
### API
It's used Fastapi to expose the enpoint.


### OTP Email
The email is a faker implementation that logs on a stdout.
Ex.
```
INFO 2023-07-16 13:22:44,488  Sent email to: antonio@test.it - subject: OTP - body: Hi antonio, the OTP is 74919
```
### Peristence
Now are stored only the users and the otps. In a next implementation could be saved the JWT token and add more stricted checks.
For example not emit a new JWT if there is a valid jwt.
