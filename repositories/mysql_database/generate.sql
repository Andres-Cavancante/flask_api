CREATE DATABASE IF NOT EXISTS flask_api;

USE flask_api;

CREATE TABLE authorization (
    client_id varchar(8) not null UNIQUE,
    client_secret varchar(255) not null UNIQUE,
    refresh_token varchar(255) not null UNIQUE
);

CREATE TABLE basic (
    date varchar (10) not null,
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
);