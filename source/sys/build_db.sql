create table buy (
  buyer_id smallint(6) not null default '0',
  posttime timestamp not null default CURRENT_TIMESTAMP,
  mkt_id int(11) not null default '0',
  quantity float not null default '0',
  price float not null default '0',
  primary key (mkt_id, buyer_id),
  key Posttime (posttime)
) ENGINE=InnoDB default charset=latin1;

create table sell (
  seller_id smallint(6) not null default '0',
  posttime timestamp not null default CURRENT_TIMESTAMP,
  mkt_id int(11) not null default '0',
  quantity float not null default '0',
  price float not null default '0',
  primary key (mkt_id, seller_id),
  key Posttime (posttime)
) ENGINE=InnoDB default charset=latin1;

create table clear (
  mkt_id int(11) not null default '0',
  posttime timestamp not null default CURRENT_TIMESTAMP,
  quantity float null default NULL,
  price float null default NULL,
  avg24 float null default NULL,
  std24 float null default NULL,
  avg168 float null default NULL,
  std168 float null default NULL,
  primary key (mkt_id),
  key Posttime (posttime)
) engine=InnoDB default charset=latin1;

create table cust_contract_preference (
  cust_id int(11) not null,
  utility char(1),
  first_choice varchar(5),
  second_choice varchar(5),
  primary key (cust_id),
  constraint choice_1 foreign key (first_choice) references contract_type (contract_type_code) on delete restrict on update restrict,
  constraint choice_2 foreign key (second_choice) references contract_type (contract_type_code) on delete restrict on update restrict
  ) ENGINE=InnoDB default charset=latin1;
