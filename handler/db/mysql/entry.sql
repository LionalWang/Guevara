drop table if exists entries;
create table entries (
  id BIGINT  primary KEY AUTO_INCREMENT ,
  title TEXT  not null,
  text TEXT  not null
);