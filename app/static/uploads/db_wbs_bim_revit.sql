-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Jul 03, 2023 at 05:44 PM
-- Server version: 10.4.27-MariaDB
-- PHP Version: 7.4.33

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `db_wbs_bim_revit`
--

-- --------------------------------------------------------

--
-- Table structure for table `revit`
--

CREATE TABLE `revit` (
  `id` int(11) NOT NULL,
  `name` varchar(100) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `revit`
--

INSERT INTO `revit` (`id`, `name`) VALUES
(1, '300 x 600mm 2'),
(2, '301 x 601mm 2'),
(3, '333 x 123mm2'),
(4, '300 x 600mm 2'),
(5, '301 x 601mm 2'),
(6, '333 x 123mm2'),
(7, '300 x 600mm 2'),
(8, '301 x 601mm 2'),
(9, '333 x 123mm2'),
(10, '333 x 123mm2'),
(11, '300 x 600mm 2'),
(12, '333 x 123mm2'),
(13, '301 x 601mm 2'),
(14, '300 x 600mm 2'),
(15, '300 x 600mm 2'),
(16, '300 x 600mm 2'),
(17, '300 x 600mm 2');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `revit`
--
ALTER TABLE `revit`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `revit`
--
ALTER TABLE `revit`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=18;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
