-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- 생성 시간: 24-09-28 21:19
-- 서버 버전: 8.0.36
-- PHP 버전: 8.2.22

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- 데이터베이스: `jukson`
--

-- --------------------------------------------------------

--
-- 테이블 구조 `library_book`
--

CREATE TABLE `library_book` (
  `book_id` int NOT NULL,
  `title` varchar(255) NOT NULL,
  `author` varchar(255) NOT NULL,
  `ISBN` varchar(13) NOT NULL,
  `available_copies` int DEFAULT '0',
  `total_copies` int DEFAULT '0'
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- 테이블의 덤프 데이터 `library_book`
--

INSERT INTO `library_book` (`book_id`, `title`, `author`, `ISBN`, `available_copies`, `total_copies`) VALUES
(1, '예감은 틀리지 않는다', '줄리언 반스', '9788963708386', 3, 3),
(7, '심슨 가족이 사는법', '윌리엄 어윈', '9788967356453', 1, 2),
(8, '말보루 포레스트 미스트', '말보루', '88023441', 1, 1),
(9, '말보루 블라썸 미스트', '말보루', '88023489', 1, 1);

-- --------------------------------------------------------

--
-- 테이블 구조 `library_history`
--

CREATE TABLE `library_history` (
  `member_id` varchar(50) NOT NULL,
  `book_id` int NOT NULL,
  `loan_date` datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `return_date` datetime DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- 테이블의 덤프 데이터 `library_history`
--

INSERT INTO `library_history` (`member_id`, `book_id`, `loan_date`, `return_date`) VALUES
('jukson', 7, '2024-09-28 21:09:18', NULL),
('test1', 1, '2024-09-28 20:55:22', '2024-09-28 20:55:34'),
('test2', 1, '2024-09-28 20:49:22', '2024-09-28 20:49:33'),
('test2', 1, '2024-09-28 20:46:17', '2024-09-28 20:49:04'),
('test3', 1, '2024-09-28 20:43:24', '2024-09-28 20:43:40');

--
-- 트리거 `library_history`
--
DELIMITER $$
CREATE TRIGGER `update_available_copies_on_loan` AFTER INSERT ON `library_history` FOR EACH ROW BEGIN
    UPDATE library_book
    SET available_copies = available_copies - 1
    WHERE book_id = NEW.book_id;
END
$$
DELIMITER ;
DELIMITER $$
CREATE TRIGGER `update_available_copies_on_return` AFTER UPDATE ON `library_history` FOR EACH ROW BEGIN
    IF NEW.return_date IS NOT NULL THEN
        UPDATE library_book
        SET available_copies = available_copies + 0
        WHERE book_id = NEW.book_id;
    END IF;
END
$$
DELIMITER ;

-- --------------------------------------------------------

--
-- 테이블 구조 `library_user`
--

CREATE TABLE `library_user` (
  `id` int NOT NULL,
  `member_id` varchar(50) NOT NULL,
  `member_password` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `phone_number` varchar(20) DEFAULT NULL
) ENGINE=MyISAM DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;

--
-- 테이블의 덤프 데이터 `library_user`
--

INSERT INTO `library_user` (`id`, `member_id`, `member_password`, `name`, `phone_number`) VALUES
(7, 'test1', '$2y$10$oiyzuSujQzsRMBGrFhBcteh9E9a7RB5L0GlYMTHFxHPCUiwnxdChi', '홍길동', '010-1234-1234'),
(9, 'test2', '$2y$10$MGPjQrpJR4tgNv.OPgxoLuT2WZA1ULZX4pOk48sZnpzWptEyY0MOS', '송아름', '010-1234-1234'),
(8, 'jukson', '$2y$10$42tTKecVtapuUyuSPswTPexaNPljrvRAlFq5t/dlZNCySpjVWpZPK', '김민석', '010-8938-6799'),
(10, 'test3', '$2y$10$CNG5y3Dn8oWZl1S.SIPuMuAHCx6V.R91XCuyHcVJP6JwEiuQQWNjC', '김기리', '010-1234-1234'),
(11, 'test4', '$2y$10$BIhjLrxX9q/.H0QDePg0SO11k5yvvsGb1LcDtgwrH1T2ui3m9xvHy', '이민우', '010-1234-1234');

--
-- 덤프된 테이블의 인덱스
--

--
-- 테이블의 인덱스 `library_book`
--
ALTER TABLE `library_book`
  ADD PRIMARY KEY (`book_id`),
  ADD UNIQUE KEY `ISBN` (`ISBN`);

--
-- 테이블의 인덱스 `library_history`
--
ALTER TABLE `library_history`
  ADD PRIMARY KEY (`member_id`,`book_id`,`loan_date`),
  ADD KEY `book_id` (`book_id`);

--
-- 테이블의 인덱스 `library_user`
--
ALTER TABLE `library_user`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `member_id` (`member_id`);

--
-- 덤프된 테이블의 AUTO_INCREMENT
--

--
-- 테이블의 AUTO_INCREMENT `library_book`
--
ALTER TABLE `library_book`
  MODIFY `book_id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- 테이블의 AUTO_INCREMENT `library_user`
--
ALTER TABLE `library_user`
  MODIFY `id` int NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=12;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
