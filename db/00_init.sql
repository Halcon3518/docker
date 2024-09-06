CREATE USER replicator WITH REPLICATION ENCRYPTED PASSWORD 'replicator_password';
SELECT pg_create_physical_replication_slot('replication_slot');
CREATE DATABASE db_bot;

\c db_bot

CREATE TABLE phonenumbers (
    id SERIAL PRIMARY KEY,
    phonenumber VARCHAR(100) NOT NULL
);

CREATE TABLE emails (
    id SERIAL PRIMARY KEY,
    email VARCHAR(100) NOT NULL
);
