-- phpMyAdmin SQL Dump
-- version 4.7.4
-- https://www.phpmyadmin.net/
--
-- Host: localhost
-- Generation Time: Mar 06, 2019 at 02:05 PM
-- Server version: 10.1.28-MariaDB
-- PHP Version: 7.1.10

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
SET AUTOCOMMIT = 0;
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `nsdb`
--

-- --------------------------------------------------------

--
-- Table structure for table `Admins`
--

CREATE TABLE `Admins` (
  `Id` int(11) NOT NULL,
  `Username` varchar(255) NOT NULL,
  `Password` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `BasketballPositions`
--

CREATE TABLE `BasketballPositions` (
  `Id` int(4) NOT NULL,
  `FullName` varchar(255) NOT NULL,
  `ShortName` varchar(4) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `BasketballPositions`
--

INSERT INTO `BasketballPositions` (`Id`, `FullName`, `ShortName`) VALUES
(1, 'Point Guard', 'PG'),
(2, 'Shooting Guard', 'SG'),
(3, 'Small Forward', 'SF'),
(4, 'Power Forward', 'PF'),
(5, 'Center', 'C');

-- --------------------------------------------------------

--
-- Table structure for table `Cities`
--

CREATE TABLE `Cities` (
  `Id` int(4) NOT NULL,
  `Name` varchar(255) NOT NULL,
  `DivisionId` int(4) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `Cities`
--

INSERT INTO `Cities` (`Id`, `Name`, `DivisionId`) VALUES
(1, 'Atlanta', 1),
(2, 'Boston', 2),
(3, 'Brooklyn', 2),
(4, 'Charlotte', 1),
(5, 'Chicago', 3),
(6, 'Cleveland', 3),
(7, 'Detroit', 3),
(8, 'Indianapolis', 3),
(9, 'Miami', 1),
(10, 'Milwaukee', 3),
(11, 'Manhattan', 2),
(12, 'Orlando', 1),
(13, 'Philadelphia', 2),
(14, 'Toronto', 2),
(15, 'Washington', 1),
(16, 'Dallas', 4),
(17, 'Denver', 5),
(18, 'Oakland', 6),
(19, 'Houston', 4),
(20, 'Los Angeles', 6),
(21, 'Memphis', 4),
(22, 'Minneapolis', 5),
(23, 'New Orleans', 4),
(24, 'Oklahoma City', 5),
(25, 'Phoenix', 6),
(26, 'Portland', 5),
(27, 'Sacramento', 6),
(28, 'Salt Lake City', 5),
(29, 'San Antonio', 4);

-- --------------------------------------------------------

--
-- Table structure for table `Conferences`
--

CREATE TABLE `Conferences` (
  `Id` int(4) NOT NULL,
  `Name` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `Conferences`
--

INSERT INTO `Conferences` (`Id`, `Name`) VALUES
(1, 'East'),
(2, 'West');

-- --------------------------------------------------------

--
-- Table structure for table `Divisions`
--

CREATE TABLE `Divisions` (
  `Id` int(4) NOT NULL,
  `Name` varchar(255) NOT NULL,
  `ConferenceId` int(4) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `Divisions`
--

INSERT INTO `Divisions` (`Id`, `Name`, `ConferenceId`) VALUES
(1, 'Southeast', 1),
(2, 'Atlantic', 1),
(3, 'Central', 1),
(4, 'Southwest', 2),
(5, 'Northwest', 2),
(6, 'Pacific', 2);

-- --------------------------------------------------------

--
-- Table structure for table `GameLocationTypes`
--

CREATE TABLE `GameLocationTypes` (
  `Id` int(4) NOT NULL,
  `LocationType` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `GameLocationTypes`
--

INSERT INTO `GameLocationTypes` (`Id`, `LocationType`) VALUES
(1, 'Home'),
(2, 'Away');

-- --------------------------------------------------------

--
-- Table structure for table `Games`
--

CREATE TABLE `Games` (
  `Id` int(16) NOT NULL,
  `Date` date NOT NULL,
  `Duration` float DEFAULT NULL,
  `TeamId` int(4) NOT NULL,
  `OpponentId` int(4) NOT NULL,
  `GameTypeId` int(4) NOT NULL,
  `GameLocationTypeId` int(4) DEFAULT NULL,
  `Win` int(4) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `GameTypes`
--

CREATE TABLE `GameTypes` (
  `Id` int(4) NOT NULL,
  `Type` varchar(255) NOT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `GameTypes`
--

INSERT INTO `GameTypes` (`Id`, `Type`) VALUES
(1, 'Regular Season'),
(2, 'Playoffs');

-- --------------------------------------------------------

--
-- Table structure for table `PlayerGameStats`
--

CREATE TABLE `PlayerGameStats` (
  `Id` int(16) NOT NULL,
  `GameId` int(16) NOT NULL,
  `PlayerId` int(16) NOT NULL,
  `FGM` int(10) DEFAULT NULL,
  `FGA` int(10) DEFAULT NULL,
  `TPM` int(10) DEFAULT NULL,
  `TPA` int(10) DEFAULT NULL,
  `FTM` int(10) DEFAULT NULL,
  `FTA` int(10) DEFAULT NULL,
  `OREB` int(10) DEFAULT NULL,
  `DREB` int(10) DEFAULT NULL,
  `AST` int(10) DEFAULT NULL,
  `TOV` int(10) DEFAULT NULL,
  `STL` int(10) DEFAULT NULL,
  `BLK` int(10) DEFAULT NULL,
  `PF` int(10) DEFAULT NULL,
  `PTS` int(10) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `Players`
--

CREATE TABLE `Players` (
  `Id` int(16) NOT NULL,
  `Name` varchar(255) NOT NULL,
  `Height` float DEFAULT NULL,
  `Weight` float DEFAULT NULL,
  `BirthDate` date DEFAULT NULL,
  `MainPositionId` int(4) DEFAULT NULL,
  `SecondPostionId` int(4) DEFAULT NULL,
  `TeamId` int(4) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `TeamGameStats`
--

CREATE TABLE `TeamGameStats` (
  `Id` int(16) NOT NULL,
  `GameId` int(16) NOT NULL,
  `FGM` int(10) DEFAULT NULL,
  `FGA` int(10) DEFAULT NULL,
  `TPM` int(10) DEFAULT NULL,
  `TPA` int(10) DEFAULT NULL,
  `FTM` int(10) DEFAULT NULL,
  `FTA` int(10) DEFAULT NULL,
  `OREB` int(10) DEFAULT NULL,
  `DREB` int(10) DEFAULT NULL,
  `AST` int(10) DEFAULT NULL,
  `TOV` int(10) DEFAULT NULL,
  `STL` int(10) DEFAULT NULL,
  `BLK` int(10) DEFAULT NULL,
  `PF` int(10) DEFAULT NULL,
  `PTS` int(10) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

-- --------------------------------------------------------

--
-- Table structure for table `Teams`
--

CREATE TABLE `Teams` (
  `Id` int(4) NOT NULL,
  `FullName` varchar(255) NOT NULL,
  `ShortName` varchar(3) NOT NULL,
  `CityId` int(4) DEFAULT NULL
) ENGINE=InnoDB DEFAULT CHARSET=latin1;

--
-- Dumping data for table `Teams`
--

INSERT INTO `Teams` (`Id`, `FullName`, `ShortName`, `CityId`) VALUES
(1, 'Atlanta Hawks', 'ATL', 1),
(2, 'Boston Celtics', 'BOS', 2),
(3, 'Brooklyn Nets', 'BKN', 3),
(4, 'Charlotte Hornets', 'CHA', 4),
(5, 'Chicago Bulls', 'CHI', 5),
(6, 'Cleveland Cavaliers', 'CLE', 6),
(7, 'Detroit Pistons', 'DET', 7),
(8, 'Indiana Pacers', 'IND', 8),
(9, 'Miami Heat', 'MIA', 9),
(10, 'Milwaukee Bucks', 'MIL', 10),
(11, 'New York Knicks', 'NYK', 11),
(12, 'Orlando Magic', 'ORL', 12),
(13, 'Philadelphia 76ers', 'PHI', 13),
(14, 'Toronto Raptors', 'TOR', 14),
(15, 'Washington Wizars', 'WAS', 15),
(16, 'Dallas Mavericks', 'DAL', 16),
(17, 'Denver Nuggets', 'DEN', 17),
(18, 'Golden State Warriors', 'GSW', 18),
(19, 'Houston Rockets', 'HOU', 19),
(20, 'Los Angeles Clippers', 'LAC', 20),
(21, 'Los Angeles Lakers', 'LAL', 20),
(22, 'Memphis Grizzlies', 'MEM', 21),
(23, 'Minnesota Timberwolves', 'MIN', 22),
(24, 'New Orleans Pelicans', 'NOP', 23),
(25, 'Oklahoma City Thunder', 'OKC', 24),
(26, 'Phoenix Suns', 'PHX', 25),
(27, 'Portland Trail Blazers', 'POR', 26),
(28, 'Sacramento Kings', 'SAC', 27),
(29, 'San Antonio Spurs', 'SAS', 29),
(30, 'Utah Jazz', 'UTA', 28);

--
-- Indexes for dumped tables
--

--
-- Indexes for table `Admins`
--
ALTER TABLE `Admins`
  ADD PRIMARY KEY (`Id`);

--
-- Indexes for table `BasketballPositions`
--
ALTER TABLE `BasketballPositions`
  ADD PRIMARY KEY (`Id`);

--
-- Indexes for table `Cities`
--
ALTER TABLE `Cities`
  ADD PRIMARY KEY (`Id`),
  ADD KEY `DivisionId` (`DivisionId`);

--
-- Indexes for table `Conferences`
--
ALTER TABLE `Conferences`
  ADD PRIMARY KEY (`Id`);

--
-- Indexes for table `Divisions`
--
ALTER TABLE `Divisions`
  ADD PRIMARY KEY (`Id`),
  ADD KEY `ConferenceId` (`ConferenceId`);

--
-- Indexes for table `GameLocationTypes`
--
ALTER TABLE `GameLocationTypes`
  ADD PRIMARY KEY (`Id`);

--
-- Indexes for table `Games`
--
ALTER TABLE `Games`
  ADD PRIMARY KEY (`Id`),
  ADD KEY `TeamId` (`TeamId`),
  ADD KEY `OpponentId` (`OpponentId`),
  ADD KEY `GameTypeId` (`GameTypeId`),
  ADD KEY `GameLocationTypeId` (`GameLocationTypeId`);

--
-- Indexes for table `GameTypes`
--
ALTER TABLE `GameTypes`
  ADD PRIMARY KEY (`Id`);

--
-- Indexes for table `PlayerGameStats`
--
ALTER TABLE `PlayerGameStats`
  ADD PRIMARY KEY (`Id`),
  ADD KEY `GameId` (`GameId`),
  ADD KEY `PlayerId` (`PlayerId`);

--
-- Indexes for table `Players`
--
ALTER TABLE `Players`
  ADD PRIMARY KEY (`Id`),
  ADD KEY `MainPositionId` (`MainPositionId`),
  ADD KEY `SecondPostionId` (`SecondPostionId`),
  ADD KEY `TeamId` (`TeamId`);

--
-- Indexes for table `TeamGameStats`
--
ALTER TABLE `TeamGameStats`
  ADD PRIMARY KEY (`Id`),
  ADD KEY `GameId` (`GameId`);

--
-- Indexes for table `Teams`
--
ALTER TABLE `Teams`
  ADD PRIMARY KEY (`Id`),
  ADD KEY `CityId` (`CityId`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `Admins`
--
ALTER TABLE `Admins`
  MODIFY `Id` int(11) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `BasketballPositions`
--
ALTER TABLE `BasketballPositions`
  MODIFY `Id` int(4) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `Cities`
--
ALTER TABLE `Cities`
  MODIFY `Id` int(4) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=30;

--
-- AUTO_INCREMENT for table `Conferences`
--
ALTER TABLE `Conferences`
  MODIFY `Id` int(4) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `Divisions`
--
ALTER TABLE `Divisions`
  MODIFY `Id` int(4) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=7;

--
-- AUTO_INCREMENT for table `GameLocationTypes`
--
ALTER TABLE `GameLocationTypes`
  MODIFY `Id` int(4) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `Games`
--
ALTER TABLE `Games`
  MODIFY `Id` int(16) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `GameTypes`
--
ALTER TABLE `GameTypes`
  MODIFY `Id` int(4) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=3;

--
-- AUTO_INCREMENT for table `PlayerGameStats`
--
ALTER TABLE `PlayerGameStats`
  MODIFY `Id` int(16) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `Players`
--
ALTER TABLE `Players`
  MODIFY `Id` int(16) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `TeamGameStats`
--
ALTER TABLE `TeamGameStats`
  MODIFY `Id` int(16) NOT NULL AUTO_INCREMENT;

--
-- AUTO_INCREMENT for table `Teams`
--
ALTER TABLE `Teams`
  MODIFY `Id` int(4) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=31;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `Cities`
--
ALTER TABLE `Cities`
  ADD CONSTRAINT `Cities_ibfk_1` FOREIGN KEY (`DivisionId`) REFERENCES `Divisions` (`Id`);

--
-- Constraints for table `Divisions`
--
ALTER TABLE `Divisions`
  ADD CONSTRAINT `Divisions_ibfk_1` FOREIGN KEY (`ConferenceId`) REFERENCES `Conferences` (`Id`);

--
-- Constraints for table `Games`
--
ALTER TABLE `Games`
  ADD CONSTRAINT `Games_ibfk_1` FOREIGN KEY (`TeamId`) REFERENCES `Teams` (`Id`),
  ADD CONSTRAINT `Games_ibfk_2` FOREIGN KEY (`OpponentId`) REFERENCES `Teams` (`Id`),
  ADD CONSTRAINT `Games_ibfk_3` FOREIGN KEY (`GameTypeId`) REFERENCES `GameTypes` (`Id`),
  ADD CONSTRAINT `Games_ibfk_4` FOREIGN KEY (`GameLocationTypeId`) REFERENCES `GameLocationTypes` (`Id`);

--
-- Constraints for table `PlayerGameStats`
--
ALTER TABLE `PlayerGameStats`
  ADD CONSTRAINT `PlayerGameStats_ibfk_1` FOREIGN KEY (`GameId`) REFERENCES `Games` (`Id`),
  ADD CONSTRAINT `PlayerGameStats_ibfk_2` FOREIGN KEY (`PlayerId`) REFERENCES `Players` (`Id`);

--
-- Constraints for table `Players`
--
ALTER TABLE `Players`
  ADD CONSTRAINT `Players_ibfk_1` FOREIGN KEY (`MainPositionId`) REFERENCES `BasketballPositions` (`Id`),
  ADD CONSTRAINT `Players_ibfk_2` FOREIGN KEY (`SecondPostionId`) REFERENCES `BasketballPositions` (`Id`),
  ADD CONSTRAINT `Players_ibfk_3` FOREIGN KEY (`TeamId`) REFERENCES `Teams` (`Id`);

--
-- Constraints for table `TeamGameStats`
--
ALTER TABLE `TeamGameStats`
  ADD CONSTRAINT `TeamGameStats_ibfk_1` FOREIGN KEY (`GameId`) REFERENCES `Games` (`Id`);

--
-- Constraints for table `Teams`
--
ALTER TABLE `Teams`
  ADD CONSTRAINT `Teams_ibfk_1` FOREIGN KEY (`CityId`) REFERENCES `Cities` (`Id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
