PRAGMA foreign_keys=ON;

BEGIN TRANSACTION;

CREATE TABLE IF NOT EXISTS "users"
(
	id INTEGER
		constraint table_name_pk
			primary key autoincrement,
	first_name varchar,
	last_name varchar,
	cv_url varchar
);
INSERT INTO users VALUES(1,'Jan','"Dev" Niezbędny','');
CREATE TABLE IF NOT EXISTS "user_skill_associations"
(
	user_id INTEGER not null,
	skill_id INTEGER not null,
	level INTEGER,
	constraint user_skill_associations_pk
		primary key (user_id, skill_id)
);
INSERT INTO user_skill_associations VALUES(1,1,5);
INSERT INTO user_skill_associations VALUES(1,2,5);
CREATE TABLE IF NOT EXISTS "skills"
(
	id INTEGER
		constraint skills_pk
			primary key autoincrement,
	name varchar not null
);
INSERT INTO skills VALUES(1,'python');
INSERT INTO skills VALUES(2,'sql');
DELETE FROM sqlite_sequence;
INSERT INTO sqlite_sequence VALUES('users',1);
INSERT INTO sqlite_sequence VALUES('skills',2);

COMMIT;
