#!/bin/sh

/nakama/nakama migrate up --database.address postgres_user:postgres_password@postgres:5432/postgres_db
/nakama/nakama --name nakama1 --database.address postgres_user:postgres_password@postgres:5432/postgres_db --logger.level DEBUG --session.token_expiry_sec 7200
