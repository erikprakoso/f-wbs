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
-- Table structure for table `wbs_detail`
--

CREATE TABLE `wbs_detail` (
  `id` int(11) NOT NULL,
  `wbs_header_id` int(11) NOT NULL,
  `name` varchar(255) DEFAULT NULL,
  `created_at` datetime DEFAULT NULL,
  `updated_at` datetime DEFAULT NULL,
  `code` varchar(255) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `wbs_detail`
--

INSERT INTO `wbs_detail` (`id`, `wbs_header_id`, `name`, `created_at`, `updated_at`, `code`) VALUES
(1, 4, 'Mobilisasi & Demobilisasi', '2023-07-16 09:06:14', '2023-07-16 09:18:38', '1.1'),
(4, 4, 'Pembersihan Awal Lokasi Proyek', '2023-07-19 10:22:15', '2023-07-19 10:22:15', '1.2'),
(5, 4, 'Pasangan Papan Nama Proyek', '2023-07-19 10:22:27', '2023-07-19 10:22:27', '1.3'),
(6, 4, 'Direksi Keet Dan Gudang Termasuk Fasilitas', '2023-07-19 10:22:41', '2023-07-19 10:22:41', '1.4'),
(7, 4, 'Penyediaan Air Bersih Dan Listrik', '2023-07-19 10:23:02', '2023-07-19 10:23:02', '1.5'),
(8, 4, 'Pekerjaan Adminitrasi, Dokumentasi Dan Peralatan K3', '2023-07-19 10:23:14', '2023-07-19 10:23:14', '1.6'),
(9, 4, 'Stakeout Dan Positioning', '2023-07-19 10:23:25', '2023-07-19 10:23:25', '1.7'),
(10, 4, 'Pembuatan Pagar Sementara Seng Gelombang, T = 2 Meter', '2023-07-19 10:23:36', '2023-07-19 10:23:36', '1.8'),
(11, 4, 'Pasangan Rambu-rambu Pengaman + Lampu Warning Light', '2023-07-19 10:23:47', '2023-07-19 10:23:47', '1.9'),
(12, 5, 'Pekerjaan Drainase', '2023-07-19 10:24:34', '2023-07-19 10:24:34', '2.1'),
(13, 5, 'Pekerjaan Tanah', '2023-07-19 10:25:28', '2023-07-19 10:25:35', '2.2'),
(14, 5, 'Pekerjaan Pondasi Sumuran', '2023-07-19 10:25:47', '2023-07-19 10:25:47', '2.3'),
(15, 5, 'Pekerjaan Abutment', '2023-07-19 10:25:58', '2023-07-19 10:26:03', '2.4'),
(16, 6, 'Pekerjaan Girder', '2023-07-19 10:38:55', '2023-07-19 10:38:59', '3.1'),
(17, 6, 'Pekerjaan Diafragma', '2023-07-19 10:39:07', '2023-07-19 10:39:07', '3.2'),
(18, 6, 'Pekerjaan Pelat Lantai', '2023-07-19 10:39:17', '2023-07-19 10:39:17', '3.3'),
(19, 6, 'Pekerjaan Aspal', '2023-07-19 10:39:27', '2023-07-19 10:39:27', '3.4'),
(20, 7, 'Pekerjaan Trotoar', '2023-07-19 10:56:12', '2023-07-19 10:56:12', '4.1'),
(21, 7, 'Pekerjaan Parapet', '2023-07-19 10:56:21', '2023-07-19 10:56:21', '4.2'),
(22, 8, 'Pekerjaan Pengecatan', '2023-07-19 10:58:16', '2023-07-19 10:58:16', '5.1'),
(23, 8, 'Pembuatan Marka Jalan', '2023-07-19 10:58:24', '2023-07-19 10:58:24', '5.2'),
(24, 8, 'Pembersihan Material Konstruksi', '2023-07-19 10:58:32', '2023-07-19 10:58:32', '5.3');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `wbs_detail`
--
ALTER TABLE `wbs_detail`
  ADD PRIMARY KEY (`id`),
  ADD KEY `wbs_header_id` (`wbs_header_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `wbs_detail`
--
ALTER TABLE `wbs_detail`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=25;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `wbs_detail`
--
ALTER TABLE `wbs_detail`
  ADD CONSTRAINT `wbs_detail_ibfk_1` FOREIGN KEY (`wbs_header_id`) REFERENCES `wbs_header` (`id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
