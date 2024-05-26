CREATE DATABASE IF NOT EXISTS flask_api;

USE flask_api;

-- CREATE TABLE users (
--     appId varchar(255) not null,
--     appPassword varchar(255) not null,
--     clientSecret varchar(255) not null
-- );

-- INSERT INTO users (
--     appId, 
--     appPassword,
--     clientSecret
-- )
-- VALUES ( 
--     'samsumg', 
--     '6be00ce921e80deb2734dc892231ce22ed6d13738f8ca5455676fd3b6904e27e',
--     ''
-- );

CREATE TABLE basic (
    date varchar (255) not null,
    campaignName varchar (255) not null,
    campaignId varchar (255) not null,
    category varchar (255) not null,
    impressions int,
    clicks int,
    leads int,
    orders int,
    spend float,
    revenue float
);