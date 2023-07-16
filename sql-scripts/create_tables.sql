CREATE TABLE IF NOT EXISTS "user" (
  id varchar(36) NOT NULL PRIMARY KEY,
  email varchar(254) NOT NULL UNIQUE,
  password varchar(30) NOT NULL,
  name varchar(100) NOT NULL,
  last_name varchar(100),
  two_factor_auth_enabled boolean NOT NULL DEFAULT false
);

CREATE TABLE IF NOT EXISTS "otp" (
  id varchar(36) NOT NULL PRIMARY KEY,
  value varchar(5) NOT NULL,
  created TIMESTAMP WITH TIME ZONE NOT NULL,
  expired TIMESTAMP WITH TIME ZONE NOT NULL,
  user_id varchar(36) NOT NULL,
  checked boolean NOT NULL DEFAULT false,
  CONSTRAINT fk_user FOREIGN KEY(user_id) REFERENCES "user"(id)
);
