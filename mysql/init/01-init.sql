-- Tabla Users para almacenar usuarios
CREATE TABLE IF NOT EXISTS `Users` (
    `UserId` int(11) NOT NULL,
    `Name` text NOT NULL,
    PRIMARY KEY (`UserId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Tabla Reports para almacenar reportes
CREATE TABLE IF NOT EXISTS `Reports` (
    `Reported` int(11) NOT NULL,
    `UserId` int(11) NOT NULL,
    KEY `Reported` (`Reported`),
    KEY `UserId` (`UserId`),
    CONSTRAINT `Reports_ibfk_1` FOREIGN KEY (`Reported`) REFERENCES `Users` (`UserId`),
    CONSTRAINT `Reports_ibfk_2` FOREIGN KEY (`UserId`) REFERENCES `Users` (`UserId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;

-- Tabla Flamers para almacenar kicks
CREATE TABLE IF NOT EXISTS `Flamers` (
    `UserId` int(11) NOT NULL,
    `Kicks` int(11) NOT NULL DEFAULT 0,
    PRIMARY KEY (`UserId`),
    CONSTRAINT `Flamers_ibfk_1` FOREIGN KEY (`UserId`) REFERENCES `Users` (`UserId`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4; 