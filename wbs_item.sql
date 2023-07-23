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
-- Table structure for table `wbs_item`
--

CREATE TABLE `wbs_item` (
  `id` int(11) NOT NULL,
  `wbs_detail_id` int(11) NOT NULL,
  `code` varchar(255) DEFAULT NULL,
  `name` varchar(255) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `wbs_item`
--

INSERT INTO `wbs_item` (`id`, `wbs_detail_id`, `code`, `name`, `created_at`, `updated_at`) VALUES
(4, 12, '2.1.1', 'Penggalian Tanah Untuk Selokan  Drainase', '2023-07-19 10:26:39', '2023-07-19 10:26:39'),
(5, 12, '2.1.2', 'Penggalian Tanah Untuk Saluran Kolam Resapan', '2023-07-19 10:26:51', '2023-07-19 10:26:51'),
(6, 12, '2.1.3', 'Pemasangan Bekisting Drainase', '2023-07-19 10:27:02', '2023-07-19 10:27:02'),
(7, 12, '2.1.4', 'Pembesian Drainase', '2023-07-19 10:27:13', '2023-07-19 10:27:13'),
(8, 12, '2.1.5', 'Pembetonan Drainase', '2023-07-19 10:27:24', '2023-07-19 10:27:24'),
(9, 13, '2.2.1', 'Penggalian Tanah Dengan Alat Berat', '2023-07-19 10:35:09', '2023-07-19 10:35:09'),
(10, 13, '2.2.2', 'Pengurugan Dan Pemerataan Sirtu (Padat)', '2023-07-19 10:35:20', '2023-07-19 10:35:20'),
(11, 13, '2.2.3', 'Angkutan Tanah Keluar Proyek', '2023-07-19 10:35:30', '2023-07-19 10:35:30'),
(12, 13, '2.2.4', 'Pemasangan Settlement Plate', '2023-07-19 10:35:39', '2023-07-19 10:35:39'),
(13, 13, '2.2.5', 'Pemasangan Pneumatic Piezometer', '2023-07-19 10:35:51', '2023-07-19 10:35:51'),
(14, 13, '2.2.6', 'Pemasangan Inclinometer', '2023-07-19 10:36:05', '2023-07-19 10:36:05'),
(15, 14, '2.3.1', 'Penggalian Tanah Untuk Pondasi Sumuran', '2023-07-19 10:36:35', '2023-07-19 10:36:35'),
(16, 14, '2.3.2', 'Pemasangan Bekisting Cincin Beton', '2023-07-19 10:36:44', '2023-07-19 10:36:44'),
(17, 14, '2.3.3', 'Pembesian Pondasi Sumuran', '2023-07-19 10:36:54', '2023-07-19 10:36:54'),
(18, 14, '2.3.4', 'Pembetonan Pondasi Sumuran', '2023-07-19 10:37:03', '2023-07-19 10:37:03'),
(19, 15, '2.4.1', 'Pemasangan Bekisting Abutment T', '2023-07-19 10:37:22', '2023-07-19 10:37:22'),
(20, 15, '2.4.2', 'Pembesian Abutment T', '2023-07-19 10:37:32', '2023-07-19 10:37:32'),
(21, 15, '2.4.3', 'Pembetonan Abutment T', '2023-07-19 10:37:40', '2023-07-19 10:37:40'),
(22, 15, '2.4.4', 'Pemasangan Bekisting Wing Wall', '2023-07-19 10:37:49', '2023-07-19 10:37:49'),
(23, 15, '2.4.5', 'Pembesian Wing Wall', '2023-07-19 10:37:58', '2023-07-19 10:37:58'),
(24, 15, '2.4.6', 'Pembetonan Wing Wall', '2023-07-19 10:38:07', '2023-07-19 10:38:07'),
(25, 16, '3.1.1', 'Pemasangan Bekisting Girder 450 X 1000 Mm', '2023-07-19 10:39:54', '2023-07-19 10:39:54'),
(26, 16, '3.1.2', 'Pembesian Girder 450 X 1000 Mm', '2023-07-19 10:40:06', '2023-07-19 10:40:06'),
(27, 16, '3.1.3', 'Pembetonan Girder 450 X 1000 Mm', '2023-07-19 10:40:17', '2023-07-19 10:40:17'),
(28, 16, '3.1.4', 'Pengaman Delatasi Antar Girder Besi Suku L100.100.10', '2023-07-19 10:40:28', '2023-07-19 10:40:28');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `wbs_item`
--
ALTER TABLE `wbs_item`
  ADD PRIMARY KEY (`id`),
  ADD KEY `wbs_detail_id` (`wbs_detail_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `wbs_item`
--
ALTER TABLE `wbs_item`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=55;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `wbs_item`
--
ALTER TABLE `wbs_item`
  ADD CONSTRAINT `wbs_item_ibfk_1` FOREIGN KEY (`wbs_detail_id`) REFERENCES `wbs_detail` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
