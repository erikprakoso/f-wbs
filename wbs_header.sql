-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Jul 23, 2023 at 04:06 PM
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
-- Database: `db_f_wbs_revit`
--

-- --------------------------------------------------------

--
-- Table structure for table `wbs_header`
--

CREATE TABLE `wbs_header` (
  `id` int(11) NOT NULL,
  `name` varchar(255) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `wbs_header`
--

INSERT INTO `wbs_header` (`id`, `name`, `created_at`, `updated_at`) VALUES
(4, 'Pekerjaan Persiapan Jembatan', '2023-07-16 07:30:46', '2023-07-19 10:21:49'),
(5, 'Pekerjaan Struktur Bawah', '2023-07-19 10:24:18', '2023-07-22 13:33:07'),
(6, 'Pekerjaan Struktur Atas', '2023-07-19 10:38:37', '2023-07-19 10:38:37'),
(7, 'Pekerjaan Aksesoris Struktur Jembatan', '2023-07-19 10:55:49', '2023-07-19 10:55:49'),
(8, 'Pekerjaan Finisihing Jembatan', '2023-07-19 10:58:01', '2023-07-19 10:58:01');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `wbs_header`
--
ALTER TABLE `wbs_header`
  ADD PRIMARY KEY (`id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `wbs_header`
--
ALTER TABLE `wbs_header`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=9;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
