#!/bin/bash
set -e

clickhouse client -n <<-EOSQL
    CREATE DATABASE IF NOT EXISTS geo;
    CREATE TABLE IF NOT EXISTS geo.balance (user_id Int32, points Int32, created DateTime DEFAULT now()) ENGINE = Log;
EOSQL