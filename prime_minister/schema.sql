PRAGMA synchronous = OFF;
PRAGMA journal_mode = MEMORY;
BEGIN TRANSACTION;
DROP TABLE IF EXISTS tbl_marriage;
DROP TABLE IF EXISTS tbl_ministry;
DROP TABLE IF EXISTS tbl_person;
DROP TABLE IF EXISTS tbl_recreation;
DROP TABLE IF EXISTS tbl_user;

CREATE TABLE `tbl_marriage` (
  `id` integer PRIMARY KEY AUTOINCREMENT
,  `id_person` integer NOT NULL
,  `id_person_partner` integer NOT NULL
,  `num_children` integer DEFAULT NULL
,  `num_year_marriage` integer DEFAULT NULL
);
CREATE TABLE `tbl_ministry` (
  `id` integer PRIMARY KEY AUTOINCREMENT
,  `date_start` date NOT NULL
,  `id_next` integer DEFAULT NULL
,  `id_person` integer DEFAULT NULL
,  `vc_ministry` varchar(255) NOT NULL
,  `vc_party` varchar(255) DEFAULT NULL
,  `vc_state_represent` varchar(255) DEFAULT NULL
);
CREATE TABLE `tbl_person` (
  `id` integer PRIMARY KEY AUTOINCREMENT
,  `date_birth` date DEFAULT NULL
,  `date_death` date DEFAULT NULL
,  `vc_birth_place` varchar(255) NOT NULL DEFAULT ''
,  `vc_common_name` varchar(255) NOT NULL DEFAULT ''
,  `vc_given_names` varchar(255) NOT NULL DEFAULT ''
,  `vc_postnominal` varchar(255) NOT NULL DEFAULT ''
,  `vc_prenominal` varchar(255) NOT NULL DEFAULT ''
,  `vc_surname` varchar(255) NOT NULL DEFAULT ''
);
CREATE TABLE `tbl_recreation` (
  `id` integer PRIMARY KEY AUTOINCREMENT
,  `id_person` integer NOT NULL
,  `vc_recreation` varchar(255) NOT NULL
);
CREATE TABLE `tbl_user` (
  `id` integer PRIMARY KEY AUTOINCREMENT
,  `vc_password` varchar(255) NOT NULL
,  `vc_username` varchar(255) NOT NULL
);
END TRANSACTION;
