-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Sep 20, 2023 at 01:38 PM
-- Server version: 10.4.28-MariaDB
-- PHP Version: 8.2.4

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `votingsystem`
--

-- --------------------------------------------------------

--
-- Table structure for table `admin`
--

CREATE TABLE `admin` (
  `id` int(11) NOT NULL,
  `username` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `admin`
--

INSERT INTO `admin` (`id`, `username`, `password`) VALUES
(0, '835d6dc88b708bc646d6db82c853ef4182fabbd4a8de59c213f2b5ab3ae7d9be', '95082382fd163ef1522fcfcc372b33f4873f1a608e400050379be940f75a021a');

-- --------------------------------------------------------

--
-- Table structure for table `vote`
--

CREATE TABLE `vote` (
  `id` int(11) NOT NULL,
  `voter_id` varchar(30) NOT NULL,
  `poll` varchar(50) NOT NULL,
  `district` varchar(50) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `vote`
--

INSERT INTO `vote` (`id`, `voter_id`, `poll`, `district`) VALUES
(2, 'EU4DM3NZZ3', 'Nepal Communist Party (Maoist Center)', 'Bajhang'),
(3, 'GPNQTVIBYL', 'Nepal Communist Party (UML)', 'Baitadi'),
(4, 'QTWKCK61D9', 'Loktantrik Samajbadi Party, Nepal', 'Bardiya'),
(5, 'WLK2DGEAH7', 'Janata Samajbadi Party, Nepal', 'Bajhang');

-- --------------------------------------------------------

--
-- Table structure for table `voters`
--

CREATE TABLE `voters` (
  `id` int(11) NOT NULL,
  `voter_id` varchar(20) NOT NULL,
  `name` varchar(50) NOT NULL,
  `citizenship` varchar(12) NOT NULL,
  `phone` varchar(10) NOT NULL,
  `district` varchar(50) NOT NULL,
  `gender` varchar(20) NOT NULL,
  `password` varchar(100) NOT NULL,
  `cpassword` varchar(100) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `voters`
--

INSERT INTO `voters` (`id`, `voter_id`, `name`, `citizenship`, `phone`, `district`, `gender`, `password`, `cpassword`) VALUES
(15, 'GPNQTVIBYL', 'hfijrbf3i4b', '09876543211', '0987654321', 'bara', 'Non-Binary', 'f27626b7628eaa4ab28ae97ccf64414b5b082ed6aa3b45240c5ac0637551bc10', 'f27626b7628eaa4ab28ae97ccf64414b5b082ed6aa3b45240c5ac0637551bc10'),
(17, 'WLK2DGEAH7', 'hi', '19281234561', '9848021861', 'Badhaiyatal-7, Bardiya', 'Female', '99f2bdf9942653ab32d9dfa0b43c72c3fbbb9679450fd965c590c224897b848a', '99f2bdf9942653ab32d9dfa0b43c72c3fbbb9679450fd965c590c224897b848a'),
(21, 'UHVE4P9KM6', 'Darpan R', '12344567890', '9848021863', 'hfhfbehbeh', 'Female', '2fb15fb32f0b09869b9a77a6bb027c5963f24afee349511854b240a4c5ce6dcb', '2fb15fb32f0b09869b9a77a6bb027c5963f24afee349511854b240a4c5ce6dcb'),
(22, 'P5KT3LOFHX', 'hbhbdhf', '17172772771', '1234566666', 'Gshwbqw', 'Intersex', '0e80ca387515bf4e4f7206aaaeabd15d540033efaf107579def3205ee45f9c65', '0e80ca387515bf4e4f7206aaaeabd15d540033efaf107579def3205ee45f9c65'),
(23, 'DN86D8O87I', 'nJjjbbhb', '09987654321', '0998765432', 'jhhjnnn', 'Non-Binary', '4f563313a5c15b5a6e86994363fb933def8d244ca8e47186e547df6fd4e3b05e', '4f563313a5c15b5a6e86994363fb933def8d244ca8e47186e547df6fd4e3b05e'),
(24, 'GR143ET5DK', 'djbdhjwbchj', '55443322110', '5544332211', 'hghcbs', 'Female', '449b2fabdf08cfcd12d8e43913833d3c13d808f5b61b8d5dd751bbfca617c06c', '449b2fabdf08cfcd12d8e43913833d3c13d808f5b61b8d5dd751bbfca617c06c'),
(27, '7LAJCU48YD', 'Darpan RR', '12345667889', '1234566788', 'Bardiya', 'Non-Binary', 'a317b0dee977685344dbbabfcf283fb9ebb14fe33c4dbe2630407ee478617bc9', 'a317b0dee977685344dbbabfcf283fb9ebb14fe33c4dbe2630407ee478617bc9');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `admin`
--
ALTER TABLE `admin`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- Indexes for table `vote`
--
ALTER TABLE `vote`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `voter_id` (`voter_id`);

--
-- Indexes for table `voters`
--
ALTER TABLE `voters`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `voter_id` (`voter_id`),
  ADD UNIQUE KEY `citizenship` (`citizenship`),
  ADD UNIQUE KEY `phone` (`phone`),
  ADD UNIQUE KEY `password` (`password`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `vote`
--
ALTER TABLE `vote`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `voters`
--
ALTER TABLE `voters`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=28;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
