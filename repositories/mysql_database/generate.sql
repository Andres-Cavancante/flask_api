CREATE DATABASE IF NOT EXISTS flask_api;

USE flask_api;

CREATE TABLE authorization (
    client_id varchar(8) not null UNIQUE,
    client_secret varchar(72) not null UNIQUE,
    refresh_token varchar(36) not null UNIQUE
);

CREATE TABLE basic (
    user_id varchar (255) not null,
    date DATE not null,
    account_id varchar (14) not null,
    account_name varchar (255) not null,
    campaign_name varchar (255) not null,
    campaign_id varchar (255) not null,
    adset_name varchar (255) not null,
    adset_id varchar (255) not null,
    ad_name varchar (255) not null,
    ad_id varchar (255) not null,
    clicks int,
    cost float,
    impressions int,
    revenue float
)
PARTITION BY RANGE (YEAR(date)) (
    PARTITION partition2021 VALUES LESS THAN (2022),
    PARTITION partition2022 VALUES LESS THAN (2023),
    PARTITION partition2023 VALUES LESS THAN (2024),
    PARTITION partition2024 VALUES LESS THAN (2025)
);
ALTER TABLE basic ADD INDEX idx_account_id (account_id);