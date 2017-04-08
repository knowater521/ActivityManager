SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";
CREATE DATABASE IF NOT EXISTS `activitymanager` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
USE `activitymanager`;

CREATE TABLE `activities` (
  `activity_name` varchar(10) COLLATE utf8_bin NOT NULL DEFAULT '',
  `title` text COLLATE utf8_bin NOT NULL,
  `reg_enable` tinyint(1) NOT NULL DEFAULT '1',
  `team_enable` tinyint(1) NOT NULL DEFAULT '0',
  `upload_enable` tinyint(1) NOT NULL DEFAULT '0',
  `note` text COLLATE utf8_bin NOT NULL,
  `rank` int(11) NOT NULL DEFAULT '0',
  `hide` tinyint(1) NOT NULL DEFAULT '0'
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

CREATE TABLE `admins` (
  `user` varchar(10) NOT NULL,
  `passwd` text NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8;

CREATE TABLE `members` (
  `sid` int(10) unsigned NOT NULL,
  `name` text COLLATE utf8_bin NOT NULL,
  `stu_code` text COLLATE utf8_bin NOT NULL,
  `qq` text COLLATE utf8_bin NOT NULL,
  `phone` text COLLATE utf8_bin NOT NULL,
  `team` text COLLATE utf8_bin,
  `activity` varchar(10) COLLATE utf8_bin NOT NULL DEFAULT ''
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;

CREATE TABLE `upload_history` (
  `sid` int(10) unsigned NOT NULL,
  `activity` varchar(10) COLLATE utf8_bin NOT NULL DEFAULT '',
  `time` text COLLATE utf8_bin NOT NULL,
  `size` text COLLATE utf8_bin NOT NULL,
  `fid` int(11) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COLLATE=utf8_bin;


ALTER TABLE `activities`
  ADD PRIMARY KEY (`activity_name`);

ALTER TABLE `members`
  ADD PRIMARY KEY (`sid`),
  ADD KEY `activity` (`activity`);

ALTER TABLE `upload_history`
  ADD PRIMARY KEY (`fid`),
  ADD KEY `sid` (`sid`),
  ADD KEY `activity` (`activity`);


ALTER TABLE `members`
  MODIFY `sid` int(10) unsigned NOT NULL AUTO_INCREMENT;
ALTER TABLE `upload_history`
  MODIFY `fid` int(11) NOT NULL AUTO_INCREMENT;

ALTER TABLE `members`
  ADD CONSTRAINT `members_ibfk_1` FOREIGN KEY (`activity`) REFERENCES `activities` (`activity_name`);

ALTER TABLE `upload_history`
  ADD CONSTRAINT `upload_history_ibfk_1` FOREIGN KEY (`sid`) REFERENCES `members` (`sid`),
  ADD CONSTRAINT `upload_history_ibfk_2` FOREIGN KEY (`activity`) REFERENCES `activities` (`activity_name`);
COMMIT;
