-- phpMyAdmin SQL Dump
-- version 5.2.1
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Jun 22, 2026 at 01:25 PM
-- Server version: 10.4.32-MariaDB
-- PHP Version: 8.2.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `moto_db`
--

-- --------------------------------------------------------

--
-- Table structure for table `appointments`
--

CREATE TABLE `appointments` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `motorcycle_name` varchar(100) NOT NULL,
  `plate_number` varchar(50) DEFAULT NULL,
  `reason` text NOT NULL,
  `appointment_date` date NOT NULL,
  `appointment_time` time NOT NULL,
  `status` enum('Pending','Approved','Completed','Cancelled') NOT NULL DEFAULT 'Pending',
  `service_report` text DEFAULT NULL,
  `parts_replaced` text DEFAULT NULL,
  `mechanic_id` int(11) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `cart_items`
--

CREATE TABLE `cart_items` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `part_id` int(11) NOT NULL,
  `quantity` int(11) NOT NULL DEFAULT 1,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

-- --------------------------------------------------------

--
-- Table structure for table `orders`
--

CREATE TABLE `orders` (
  `id` int(11) NOT NULL,
  `user_id` int(11) NOT NULL,
  `full_name` varchar(150) NOT NULL,
  `phone` varchar(50) NOT NULL,
  `fulfillment_method` varchar(50) NOT NULL,
  `address` text DEFAULT NULL,
  `payment_method` varchar(50) NOT NULL,
  `total_amount` decimal(10,2) NOT NULL,
  `notes` text DEFAULT NULL,
  `status` varchar(50) DEFAULT 'Pending',
  `is_paid` tinyint(1) NOT NULL DEFAULT 0,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `orders`
--

INSERT INTO `orders` (`id`, `user_id`, `full_name`, `phone`, `fulfillment_method`, `address`, `payment_method`, `total_amount`, `notes`, `status`, `is_paid`, `created_at`) VALUES
(12, 2, 'Walk-in Customer', 'N/A', 'pickup', 'Walk-in Cashier Counter', 'cod', 422.00, 'Walk-in checkout processed at cashier terminal.', 'Completed', 1, '2026-06-22 04:43:42'),
(13, 2, 'Walk-in Customer', 'N/A', 'pickup', 'Walk-in Cashier Counter', 'cod', 211.00, 'Walk-in checkout processed at cashier terminal.', 'Completed', 1, '2026-06-22 04:46:36'),
(14, 2, 'Jaguar De Cheetah', '091234412345', 'pickup', 'Walk-in Cashier Counter', 'cod', 2200.00, 'Walk-in checkout processed at cashier terminal.', 'Completed', 1, '2026-06-22 04:52:06'),
(15, 2, 'Jonny Doy', 'N/A', 'pickup', 'Walk-in Cashier Counter', 'cod', 211.00, 'Walk-in checkout processed at cashier terminal.', 'Completed', 1, '2026-06-22 05:03:27'),
(16, 2, 'Walk-in Customer', 'N/A', 'pickup', 'Walk-in Cashier Counter', 'cod', 211.00, 'Walk-in checkout processed at cashier terminal.', 'Completed', 1, '2026-06-22 05:05:07');

-- --------------------------------------------------------

--
-- Table structure for table `order_items`
--

CREATE TABLE `order_items` (
  `id` int(11) NOT NULL,
  `order_id` int(11) NOT NULL,
  `part_id` int(11) NOT NULL,
  `quantity` int(11) NOT NULL,
  `price` decimal(10,2) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `order_items`
--

INSERT INTO `order_items` (`id`, `order_id`, `part_id`, `quantity`, `price`) VALUES
(17, 12, 54, 2, 211.00),
(18, 13, 54, 1, 211.00),
(19, 14, 41, 1, 2200.00),
(20, 15, 54, 1, 211.00),
(21, 16, 54, 1, 211.00);

-- --------------------------------------------------------

--
-- Table structure for table `parts`
--

CREATE TABLE `parts` (
  `id` int(11) NOT NULL,
  `name` varchar(100) NOT NULL,
  `brand` varchar(100) NOT NULL,
  `category` varchar(100) NOT NULL,
  `sku` varchar(50) NOT NULL,
  `description` text DEFAULT NULL,
  `image_filename` varchar(255) DEFAULT NULL,
  `price` decimal(10,2) NOT NULL,
  `quantity` int(11) NOT NULL DEFAULT 0,
  `low_stock_threshold` int(11) NOT NULL DEFAULT 5,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `parts`
--

INSERT INTO `parts` (`id`, `name`, `brand`, `category`, `sku`, `description`, `image_filename`, `price`, `quantity`, `low_stock_threshold`, `created_at`, `updated_at`) VALUES
(38, 'Spark Plug NGK CR8E', 'NGK', 'Engine', 'ENG-001', 'High performance spark plug.', NULL, 250.00, 50, 5, '2026-06-21 09:24:06', '2026-06-21 09:24:06'),
(39, 'Piston Kit 150cc', 'Yamaha', 'Engine', 'ENG-002', 'Complete piston kit for 150cc engines.', NULL, 1850.00, 15, 3, '2026-06-21 09:24:06', '2026-06-21 09:24:06'),
(40, 'Front Brake Pads', 'Brembo', 'Brakes', 'BRK-001', 'Premium front brake pads.', NULL, 650.00, 25, 5, '2026-06-21 09:24:06', '2026-06-21 09:24:06'),
(41, 'Brake Disc Rotor', 'Brembo', 'Brakes', 'BRK-002', 'Front brake disc rotor.', NULL, 2200.00, 9, 2, '2026-06-21 09:24:06', '2026-06-22 04:52:06'),
(42, 'Front Fork Oil Seal', 'KYB', 'Suspension', 'SUS-001', 'Fork oil seal set.', NULL, 350.00, 30, 5, '2026-06-21 09:24:06', '2026-06-21 09:24:06'),
(43, 'Rear Shock Absorber', 'YSS', 'Suspension', 'SUS-002', 'Gas-type rear shock absorber.', NULL, 3200.00, 8, 2, '2026-06-21 09:24:06', '2026-06-21 09:24:06'),
(44, '90/80-17 Front Tire', 'Michelin', 'Tires & Wheels', 'TIR-001', 'Tubeless front motorcycle tire.', NULL, 2800.00, 12, 3, '2026-06-21 09:24:06', '2026-06-21 09:24:06'),
(45, 'Rear Alloy Wheel', 'Racing Boy', 'Tires & Wheels', 'TIR-002', 'Lightweight alloy rear wheel.', NULL, 4500.00, 6, 2, '2026-06-21 09:24:06', '2026-06-21 09:24:06'),
(46, '12V Motorcycle Battery', 'Motolite', 'Electrical', 'ELE-001', 'Maintenance-free battery.', NULL, 1800.00, 20, 4, '2026-06-21 09:24:06', '2026-06-21 09:24:06'),
(47, 'LED Headlight Bulb', 'Osram', 'Electrical', 'ELE-002', 'Bright LED headlight replacement.', NULL, 950.00, 35, 5, '2026-06-21 09:24:06', '2026-06-21 09:24:06'),
(48, 'Side Mirror Pair', 'Honda', 'Body & Frame', 'BOD-001', 'Universal side mirrors.', NULL, 450.00, 40, 5, '2026-06-21 09:24:06', '2026-06-21 09:24:06'),
(49, 'Front Fender', 'Yamaha', 'Body & Frame', 'BOD-002', 'Motorcycle front fender.', NULL, 1200.00, 10, 2, '2026-06-21 09:24:06', '2026-06-21 09:24:06'),
(50, 'Engine Oil 10W40', 'Shell', 'Fluids & Lubes', 'FLD-001', 'Fully synthetic engine oil.', NULL, 550.00, 60, 10, '2026-06-21 09:24:06', '2026-06-21 09:24:06'),
(51, 'Brake Fluid DOT4', 'Motul', 'Fluids & Lubes', 'FLD-002', 'High performance brake fluid.', NULL, 320.00, 30, 5, '2026-06-21 09:24:06', '2026-06-21 09:24:06'),
(52, 'Phone Holder', 'SEC', 'Accessories', 'ACC-001', 'Handlebar-mounted phone holder.', NULL, 350.00, 45, 5, '2026-06-21 09:24:06', '2026-06-21 09:24:06'),
(53, 'Top Box 45L', 'SEC', 'Accessories', 'ACC-002', 'Large motorcycle storage box.', NULL, 2800.00, 12, 2, '2026-06-21 09:24:06', '2026-06-21 09:24:06'),
(54, 'Tet Partr', 'TESTE', 'Engine', 'TESPART', 'Testing', NULL, 211.00, 2, 5, '2026-06-22 04:35:47', '2026-06-22 05:05:07');

-- --------------------------------------------------------

--
-- Table structure for table `payment_settings`
--

CREATE TABLE `payment_settings` (
  `id` int(11) NOT NULL,
  `gcash_name` varchar(100) NOT NULL DEFAULT 'MotoShop Parts Admin',
  `gcash_phone` varchar(20) NOT NULL DEFAULT '0917-888-2918',
  `gcash_qr_filename` varchar(255) DEFAULT NULL,
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `payment_settings`
--

INSERT INTO `payment_settings` (`id`, `gcash_name`, `gcash_phone`, `gcash_qr_filename`, `updated_at`) VALUES
(1, 'MOTOFIX REMASTER', '09692199634', 'gcash_qr_qr.png', '2026-06-22 04:47:23');

-- --------------------------------------------------------

--
-- Table structure for table `roles`
--

CREATE TABLE `roles` (
  `id` int(11) NOT NULL,
  `name` varchar(50) NOT NULL,
  `description` varchar(255) DEFAULT NULL,
  `created_at` timestamp NOT NULL DEFAULT current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `roles`
--

INSERT INTO `roles` (`id`, `name`, `description`, `created_at`) VALUES
(1, 'Owner', 'Shop owner with full system and inventory controls', '2026-06-19 09:31:23'),
(2, 'Mechanic', 'Shop mechanics who handle appointments, repairs, and diagnostics', '2026-06-19 09:31:23'),
(3, 'Client', 'Customers who buy parts and book repair appointments', '2026-06-19 09:31:23');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `id` int(11) NOT NULL,
  `role_id` int(11) NOT NULL,
  `first_name` varchar(50) NOT NULL,
  `last_name` varchar(50) NOT NULL,
  `email` varchar(100) NOT NULL,
  `phone` varchar(20) DEFAULT NULL,
  `password_hash` varchar(255) NOT NULL,
  `status` enum('active','inactive','suspended') DEFAULT 'active',
  `created_at` timestamp NOT NULL DEFAULT current_timestamp(),
  `updated_at` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`id`, `role_id`, `first_name`, `last_name`, `email`, `phone`, `password_hash`, `status`, `created_at`, `updated_at`) VALUES
(1, 3, 'Jino', 'Estillore', 'jinoestillore@email.com', '09123091234', '$2b$12$JVDqG/O.gnLm3h2DcjUKE.Wyr8.k3q8F4Kl.Gx0WjvL2QPmVf966O', 'active', '2026-06-19 10:11:36', '2026-06-19 10:11:36'),
(2, 1, 'The', 'Administrator', 'theadmin@email.com', '09091234511', '$2b$12$y5YoKqlWLNUusU2Pnr32z.Qk1qyxLJePKS5ESzidWPfLt0gZqoIL2', 'active', '2026-06-19 10:13:04', '2026-06-19 10:25:24'),
(3, 3, 'Rodney', 'Estillore', 'rodney@email.com', '09123445566', '$2b$12$qr6jW9t/UENU7X92V8.37.XYBu9HMWH6Qv7uh1GoCyDhdDqamZL7W', 'active', '2026-06-19 10:58:09', '2026-06-19 10:58:09'),
(4, 2, 'Jirod', 'Estillore', 'jirod@email.com', '09098712340', '$2b$12$sak2Ta6PrWxO4dApq.0aDe3h2Zvvm7EGR2hHNoeajdn2zq0Q/T.5O', 'active', '2026-06-19 11:11:34', '2026-06-19 11:11:34'),
(5, 3, 'Jonny', 'Estillore', 'jonny@email.com', '09123999340', '$2b$12$VRlRDf1/LNCMfTN77yer6eS1uITK3wuK5XjxBAya10QxdZEArtU1e', 'active', '2026-06-20 15:48:26', '2026-06-20 15:48:26'),
(6, 2, 'Emma', 'Estillore', 'emma@email.com', '09091234511', '$2b$12$iHBVpbZeg.Q5/qjuhTPuguM88fmCRrLrG2zM9WIMQUZCzG3flwCiO', 'active', '2026-06-20 16:14:38', '2026-06-20 16:14:38');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `appointments`
--
ALTER TABLE `appointments`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`),
  ADD KEY `idx_appointment_slot` (`appointment_date`,`appointment_time`),
  ADD KEY `idx_mechanic_schedule` (`mechanic_id`,`appointment_date`,`appointment_time`);

--
-- Indexes for table `cart_items`
--
ALTER TABLE `cart_items`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `user_part_unique` (`user_id`,`part_id`),
  ADD KEY `part_id` (`part_id`);

--
-- Indexes for table `orders`
--
ALTER TABLE `orders`
  ADD PRIMARY KEY (`id`),
  ADD KEY `user_id` (`user_id`);

--
-- Indexes for table `order_items`
--
ALTER TABLE `order_items`
  ADD PRIMARY KEY (`id`),
  ADD KEY `order_id` (`order_id`),
  ADD KEY `part_id` (`part_id`);

--
-- Indexes for table `parts`
--
ALTER TABLE `parts`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `sku` (`sku`);

--
-- Indexes for table `payment_settings`
--
ALTER TABLE `payment_settings`
  ADD PRIMARY KEY (`id`);

--
-- Indexes for table `roles`
--
ALTER TABLE `roles`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `name` (`name`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`id`),
  ADD UNIQUE KEY `email` (`email`),
  ADD KEY `role_id` (`role_id`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `appointments`
--
ALTER TABLE `appointments`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `cart_items`
--
ALTER TABLE `cart_items`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=25;

--
-- AUTO_INCREMENT for table `orders`
--
ALTER TABLE `orders`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=17;

--
-- AUTO_INCREMENT for table `order_items`
--
ALTER TABLE `order_items`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=22;

--
-- AUTO_INCREMENT for table `parts`
--
ALTER TABLE `parts`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=55;

--
-- AUTO_INCREMENT for table `payment_settings`
--
ALTER TABLE `payment_settings`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=2;

--
-- AUTO_INCREMENT for table `roles`
--
ALTER TABLE `roles`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=4;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `appointments`
--
ALTER TABLE `appointments`
  ADD CONSTRAINT `appointments_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `appointments_ibfk_2` FOREIGN KEY (`mechanic_id`) REFERENCES `users` (`id`) ON DELETE SET NULL ON UPDATE CASCADE;

--
-- Constraints for table `cart_items`
--
ALTER TABLE `cart_items`
  ADD CONSTRAINT `cart_items_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE ON UPDATE CASCADE,
  ADD CONSTRAINT `cart_items_ibfk_2` FOREIGN KEY (`part_id`) REFERENCES `parts` (`id`) ON DELETE CASCADE ON UPDATE CASCADE;

--
-- Constraints for table `orders`
--
ALTER TABLE `orders`
  ADD CONSTRAINT `orders_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `order_items`
--
ALTER TABLE `order_items`
  ADD CONSTRAINT `order_items_ibfk_1` FOREIGN KEY (`order_id`) REFERENCES `orders` (`id`) ON DELETE CASCADE,
  ADD CONSTRAINT `order_items_ibfk_2` FOREIGN KEY (`part_id`) REFERENCES `parts` (`id`) ON DELETE CASCADE;

--
-- Constraints for table `users`
--
ALTER TABLE `users`
  ADD CONSTRAINT `users_ibfk_1` FOREIGN KEY (`role_id`) REFERENCES `roles` (`id`) ON UPDATE CASCADE;
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
