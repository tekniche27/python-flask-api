-- --------------------------------------------------------
-- Host:                         127.0.0.1
-- Server version:               11.5.2-MariaDB - mariadb.org binary distribution
-- Server OS:                    Win64
-- HeidiSQL Version:             12.6.0.6765
-- --------------------------------------------------------

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET NAMES utf8 */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;


-- Dumping database structure for guessit
CREATE DATABASE IF NOT EXISTS `guessit` /*!40100 DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci */;
USE `guessit`;

-- Dumping structure for table guessit.answers
CREATE TABLE IF NOT EXISTS `answers` (
  `answerId` int(11) NOT NULL AUTO_INCREMENT,
  `answerCode` varchar(50) NOT NULL,
  `answerDesc` varchar(255) DEFAULT NULL,
  `questionCode` varchar(255) NOT NULL,
  `IsCorrect` tinyint(1) NOT NULL DEFAULT 0,
  `seq` smallint(6) NOT NULL,
  `createdBy` varchar(50) DEFAULT 'sa',
  `createdDt` datetime DEFAULT current_timestamp(),
  `updatedBy` varchar(50) DEFAULT NULL,
  `updatedDt` datetime DEFAULT NULL,
  PRIMARY KEY (`answerId`),
  UNIQUE KEY `answerCode` (`questionCode`,`answerCode`),
  CONSTRAINT `FK_answers_questionCode` FOREIGN KEY (`questionCode`) REFERENCES `questions` (`questionCode`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='List of Answers';

-- Dumping data for table guessit.answers: ~8 rows (approximately)
DELETE FROM `answers`;
INSERT INTO `answers` (`answerId`, `answerCode`, `answerDesc`, `questionCode`, `IsCorrect`, `seq`, `createdBy`, `createdDt`, `updatedBy`, `updatedDt`) VALUES
	(1, 'a1', 'Artificial Intelligence', 'q1', 1, 1, 'sa', '2024-09-14 02:22:53', NULL, NULL),
	(2, 'a2', 'Artificial Information', 'q1', 0, 2, 'sa', '2024-09-14 02:24:48', NULL, NULL),
	(3, 'a3', 'Arithmetic Invention', 'q1', 0, 3, 'sa', '2024-09-14 02:25:21', NULL, NULL),
	(4, 'a4', 'Algorithmic Idea', 'q1', 0, 4, 'sa', '2024-09-14 02:26:41', NULL, NULL),
	(5, 'a5', 'Python', 'q4', 0, 1, 'sa', '2024-09-14 02:45:23', NULL, NULL),
	(6, 'a6', 'Java', 'q4', 0, 2, 'sa', '2024-09-14 02:45:46', NULL, NULL),
	(7, 'a7', 'Elephant', 'q4', 1, 3, 'sa', '2024-09-14 02:46:14', NULL, NULL),
	(8, 'a8', 'R', 'q4', 0, 4, 'sa', '2024-09-14 02:46:31', NULL, NULL);

-- Dumping structure for table guessit.categories
CREATE TABLE IF NOT EXISTS `categories` (
  `categoryId` int(11) NOT NULL AUTO_INCREMENT,
  `categoryCode` varchar(50) NOT NULL,
  `categoryDesc` varchar(255) DEFAULT NULL,
  `createdBy` varchar(50) DEFAULT 'sa',
  `createdDt` datetime NOT NULL DEFAULT current_timestamp(),
  `updatedBy` varchar(50) DEFAULT NULL,
  `updatedDt` datetime DEFAULT NULL,
  `seq` int(11) NOT NULL,
  PRIMARY KEY (`categoryId`),
  UNIQUE KEY `categoryCode` (`categoryCode`)
) ENGINE=InnoDB AUTO_INCREMENT=14 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='List of Categories';

-- Dumping data for table guessit.categories: ~12 rows (approximately)
DELETE FROM `categories`;
INSERT INTO `categories` (`categoryId`, `categoryCode`, `categoryDesc`, `createdBy`, `createdDt`, `updatedBy`, `updatedDt`, `seq`) VALUES
	(1, 'ai', 'Artificial Intelligence', 'sa', '2024-09-13 20:08:32', NULL, '2024-09-13 20:08:32', 2),
	(2, 'cybersec', 'Cyber Security', 'sa', '2024-09-13 20:08:56', NULL, '2024-09-13 20:08:56', 3),
	(3, 'webprog', 'Web Programming', 'sa', '2024-09-13 20:09:22', NULL, '2024-09-13 20:09:22', 4),
	(4, 'databasesys', 'Database System', 'sa', '2024-09-13 20:10:05', NULL, '2024-09-13 20:10:05', 5),
	(5, 'blockchain', 'Blockchain', 'sa', '2024-09-14 01:09:29', NULL, NULL, 6),
	(6, 'gamedev', 'Game Development', 'sa', '2024-09-14 01:09:46', NULL, NULL, 7),
	(7, 'iot', 'Internet of Things', 'sa', '2024-09-14 01:10:06', NULL, NULL, 8),
	(8, 'networktech', 'Network Technology', 'sa', '2024-09-14 01:11:18', NULL, NULL, 9),
	(9, 'enterprisesys', 'Enterprise System', 'sa', '2024-09-14 01:11:53', NULL, NULL, 10),
	(10, 'java', 'Java', 'sa', '2024-09-14 01:12:17', NULL, NULL, 11),
	(11, 'python', 'Python', 'sa', '2024-09-14 01:12:27', NULL, NULL, 12),
	(12, 'random', 'Random', 'sa', '2024-09-23 02:37:12', NULL, NULL, 1);

-- Dumping structure for table guessit.difficulties
CREATE TABLE IF NOT EXISTS `difficulties` (
  `difficultyId` int(11) NOT NULL AUTO_INCREMENT,
  `difficultyCode` varchar(50) NOT NULL,
  `difficultyDesc` varchar(255) DEFAULT NULL,
  `timer` int(11) NOT NULL,
  `createdBy` varchar(50) DEFAULT 'sa',
  `createdDt` datetime NOT NULL DEFAULT current_timestamp(),
  `updatedBy` varchar(50) DEFAULT NULL,
  `updatedDt` datetime DEFAULT NULL,
  PRIMARY KEY (`difficultyId`),
  UNIQUE KEY `difficultyCode` (`difficultyCode`)
) ENGINE=InnoDB AUTO_INCREMENT=4 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='List of Difficulties';

-- Dumping data for table guessit.difficulties: ~3 rows (approximately)
DELETE FROM `difficulties`;
INSERT INTO `difficulties` (`difficultyId`, `difficultyCode`, `difficultyDesc`, `timer`, `createdBy`, `createdDt`, `updatedBy`, `updatedDt`) VALUES
	(1, 'easy', 'Easy', 60, 'sa', '2024-09-13 19:50:27', NULL, '2024-09-13 19:50:27'),
	(2, 'medium', 'Medium', 120, 'sa', '2024-09-13 19:51:30', NULL, '2024-09-13 19:51:30'),
	(3, 'hard', 'Hard', 180, 'sa', '2024-09-13 19:51:44', NULL, '2024-09-13 19:51:44');

-- Dumping structure for table guessit.questions
CREATE TABLE IF NOT EXISTS `questions` (
  `questionId` int(11) NOT NULL AUTO_INCREMENT,
  `questionCode` varchar(50) NOT NULL,
  `questionDesc` varchar(255) DEFAULT NULL,
  `categoryCode` varchar(50) NOT NULL,
  `difficultyCode` varchar(50) NOT NULL,
  `seq` smallint(6) DEFAULT NULL,
  `createdBy` varchar(255) DEFAULT 'sa',
  `createdDt` datetime NOT NULL DEFAULT current_timestamp(),
  `updatedBy` datetime DEFAULT NULL,
  `updatedDt` datetime DEFAULT NULL,
  PRIMARY KEY (`questionId`),
  UNIQUE KEY `questionCode` (`questionCode`),
  KEY `fk_questions_categoryCode` (`categoryCode`),
  KEY `fk_questions_difficultyCode` (`difficultyCode`),
  CONSTRAINT `fk_questions_categoryCode` FOREIGN KEY (`categoryCode`) REFERENCES `categories` (`categoryCode`) ON DELETE NO ACTION ON UPDATE NO ACTION,
  CONSTRAINT `fk_questions_difficultyCode` FOREIGN KEY (`difficultyCode`) REFERENCES `difficulties` (`difficultyCode`) ON DELETE NO ACTION ON UPDATE NO ACTION
) ENGINE=InnoDB AUTO_INCREMENT=5 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='List of Questions';

-- Dumping data for table guessit.questions: ~3 rows (approximately)
DELETE FROM `questions`;
INSERT INTO `questions` (`questionId`, `questionCode`, `questionDesc`, `categoryCode`, `difficultyCode`, `seq`, `createdBy`, `createdDt`, `updatedBy`, `updatedDt`) VALUES
	(1, 'q1', 'What is the meaning of AI?', 'ai', 'easy', 1, 'sa', '2024-09-13 20:23:36', NULL, NULL),
	(2, 'q2', 'What is a social engineering attack?', 'cybersec', 'medium', 1, 'sa', '2024-09-13 20:30:04', NULL, NULL),
	(3, 'q3', 'What is E-R model in the DBMS?', 'databasesys', 'hard', 1, 'sa', '2024-09-13 20:33:07', NULL, NULL),
	(4, 'q4', 'Which programming language is not used for AI?', 'ai', 'medium', 2, 'sa', '2024-09-14 02:44:43', NULL, NULL);

-- Dumping structure for table guessit.rooms
CREATE TABLE IF NOT EXISTS `rooms` (
  `roomId` int(11) NOT NULL AUTO_INCREMENT,
  `roomCode` varchar(50) NOT NULL,
  `roomDesc` varchar(50) DEFAULT NULL,
  `createdBy` varchar(50) DEFAULT 'sa',
  `createdDt` datetime NOT NULL DEFAULT current_timestamp(),
  `updatedBy` varchar(50) DEFAULT NULL,
  `updatedDt` datetime DEFAULT current_timestamp(),
  PRIMARY KEY (`roomId`),
  UNIQUE KEY `roomCode` (`roomCode`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci COMMENT='List of Rooms';

-- Dumping data for table guessit.rooms: ~0 rows (approximately)
DELETE FROM `rooms`;

/*!40103 SET TIME_ZONE=IFNULL(@OLD_TIME_ZONE, 'system') */;
/*!40101 SET SQL_MODE=IFNULL(@OLD_SQL_MODE, '') */;
/*!40014 SET FOREIGN_KEY_CHECKS=IFNULL(@OLD_FOREIGN_KEY_CHECKS, 1) */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40111 SET SQL_NOTES=IFNULL(@OLD_SQL_NOTES, 1) */;
