-- phpMyAdmin SQL Dump
-- version 4.1.14
-- http://www.phpmyadmin.net
--
-- Client :  127.0.0.1
-- Généré le :  Sam 26 Février 2022 à 18:25
-- Version du serveur :  5.6.17
-- Version de PHP :  5.5.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8 */;

--
-- Base de données :  `ged_bdd`
--

-- --------------------------------------------------------

--
-- Structure de la table `ged_account`
--

CREATE TABLE IF NOT EXISTS `ged_account` (
  `account_id` int(11) NOT NULL AUTO_INCREMENT,
  `account_employee_id` int(11) NOT NULL,
  `account_company_id` int(11) NOT NULL,
  `account_status` varchar(20) NOT NULL,
  `account_rh_numb` varchar(100) NOT NULL,
  PRIMARY KEY (`account_id`),
  KEY `account_employee_id` (`account_employee_id`,`account_company_id`),
  KEY `account_company_id` (`account_company_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COMMENT='Cette table représente un compte qui est un lien entre un employe et une entrepr' AUTO_INCREMENT=6 ;

--
-- Contenu de la table `ged_account`
--

INSERT INTO `ged_account` (`account_id`, `account_employee_id`, `account_company_id`, `account_status`, `account_rh_numb`) VALUES
(1, 2, 1, 'ON', 'XGFEKJISDF123'),
(2, 3, 1, 'ON', 'AZOPMJISDF478'),
(3, 4, 1, 'OFF', 'PPMERJISDF555'),
(4, 1, 2, 'ON', 'AAZOPJISDF555'),
(5, 6, 2, 'ON', 'PORGDJISDF321');

-- --------------------------------------------------------

--
-- Structure de la table `ged_company`
--

CREATE TABLE IF NOT EXISTS `ged_company` (
  `company_id` int(11) NOT NULL AUTO_INCREMENT,
  `company_name` varchar(50) NOT NULL,
  `company_location` varchar(100) NOT NULL,
  `company_email` varchar(100) NOT NULL,
  `company_password` varchar(50) NOT NULL,
  PRIMARY KEY (`company_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COMMENT='Cette table réprésente une entreprise' AUTO_INCREMENT=3 ;

--
-- Contenu de la table `ged_company`
--

INSERT INTO `ged_company` (`company_id`, `company_name`, `company_location`, `company_email`, `company_password`) VALUES
(1, 'DEFAR SCI', 'DAKAR-PARIS', 'defarsci@gmail.com', 'defar'),
(2, 'DEVOTEAM', '73 Rue Anatole France, 92300 Levallois-Perret', 'devoteam@gmail.com', 'devoteam');

-- --------------------------------------------------------

--
-- Structure de la table `ged_employee`
--

CREATE TABLE IF NOT EXISTS `ged_employee` (
  `employee_id` int(11) NOT NULL AUTO_INCREMENT,
  `employee_email` varchar(100) NOT NULL,
  `employeee_password` varchar(50) NOT NULL,
  `employee_fullname` varchar(100) NOT NULL,
  `employee_role` varchar(100) DEFAULT NULL,
  PRIMARY KEY (`employee_id`)
) ENGINE=InnoDB  DEFAULT CHARSET=utf8 COMMENT='Cette table représente un utilisateur de notre plateforme' AUTO_INCREMENT=7 ;

--
-- Contenu de la table `ged_employee`
--

INSERT INTO `ged_employee` (`employee_id`, `employee_email`, `employeee_password`, `employee_fullname`, `employee_role`) VALUES
(1, 'baye@gmail.com', 'bayedame12', 'Baye Dame THIAM', 'emp'),
(2, 'serigne@gmail.com', 'serigne', 'Serigne Cheikh Tidjane SY ', 'emp'),
(3, 'alioune@gmail.com', 'alioune', 'Alioune Borance MBAYE', 'emp'),
(4, 'ezechiel@gmail.com', 'ezechiel', 'Ezechiel OUATTARA', 'emp'),
(5, 'ibrahim@gmail.com', 'ibrahim', 'Ibrahim TEST', 'emp'),
(6, 'aliou@gmail.com', 'aliou', 'Aliou Abou DIALLO', 'emp');

-- --------------------------------------------------------

--
-- Structure de la table `ged_file`
--

CREATE TABLE IF NOT EXISTS `ged_file` (
  `file_id` int(11) NOT NULL AUTO_INCREMENT,
  `file_name` varchar(100) NOT NULL,
  `file_type` varchar(50) DEFAULT NULL,
  `file_src` varchar(300) NOT NULL,
  `file_account_id` int(11) NOT NULL,
  PRIMARY KEY (`file_id`),
  KEY `file_account_id` (`file_account_id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8 COMMENT='Cette table représente un fichier dans le systeme' AUTO_INCREMENT=1 ;

--
-- Contraintes pour les tables exportées
--

--
-- Contraintes pour la table `ged_account`
--
ALTER TABLE `ged_account`
  ADD CONSTRAINT `company-account` FOREIGN KEY (`account_company_id`) REFERENCES `ged_company` (`company_id`) ON UPDATE CASCADE,
  ADD CONSTRAINT `employee-account` FOREIGN KEY (`account_employee_id`) REFERENCES `ged_employee` (`employee_id`) ON UPDATE CASCADE;

--
-- Contraintes pour la table `ged_file`
--
ALTER TABLE `ged_file`
  ADD CONSTRAINT `account-file` FOREIGN KEY (`file_account_id`) REFERENCES `ged_account` (`account_id`) ON UPDATE CASCADE;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
