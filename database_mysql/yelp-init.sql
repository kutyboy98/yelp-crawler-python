create database yelp;
use yelp;
create table category (
	id int(6) primary key,
    name varchar(50) not null,
    label varchar(50) not null
);
create table restaurant (
	id int(6) primary key,
    name varchar(50) not null,
    code varchar(100) not null,
    region varchar(30) not null,
    category_id int(6) not null,
    url varchar(500) not null,
    star float(6) not null,
    review int(6) not null,
    address varchar(500) not null,
    imgs varchar(1000) not null,
    services varchar(200) not null,
    foreign key (category_id) 
		references category(id)
);
create table review (
	id varchar(30) primary key,
    restaurant_id int(6) not null,
    content varchar(2000) not null,
    imgs varchar(1000) not null,
    review int(6) not null,
    usefull int(6) not null,
    funny int(6) not null,
    cool int(6) not null,
    review_time datetime,
    foreign key (restaurant_id)
		references restaurant(id)
)
