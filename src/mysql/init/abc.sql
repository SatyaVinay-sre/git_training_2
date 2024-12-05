-- Create User Table
CREATE TABLE User (
    userid INT PRIMARY KEY AUTO_INCREMENT,
    uname VARCHAR(45) UNIQUE,
    password VARCHAR(45),
    dateJoined DATETIME DEFAULT CURRENT_TIMESTAMP
);

-- Create Role Table
CREATE TABLE Role (
    roleid INT PRIMARY KEY AUTO_INCREMENT,
    name VARCHAR(24) UNIQUE
);

-- Create UserRoles Bridge Table (Many-to-Many between User and Role)
CREATE TABLE UserRoles (
    roleid INT,
    userid INT,
    PRIMARY KEY (roleid, userid),
    CONSTRAINT fk_roleid_userRoleBridge FOREIGN KEY (roleid) REFERENCES Role(roleid),
    CONSTRAINT fk_userid_userRoleBridge FOREIGN KEY (userid) REFERENCES User(userid)
);

-- Create Product Table
CREATE TABLE Product (
    symbol VARCHAR(16) PRIMARY KEY,
    price DECIMAL(15, 2),
    productType VARCHAR(12),
    name VARCHAR(128),
    lastUpdate DATETIME
);

-- Create Order Table
CREATE TABLE `Order` (
    orderid INT PRIMARY KEY AUTO_INCREMENT,
    userid INT,
    symbol VARCHAR(16),
    side INT,
    orderTime DATETIME DEFAULT CURRENT_TIMESTAMP,
    shares INT,
    price DECIMAL(15, 2),
    status VARCHAR(24) DEFAULT 'pending',
    CONSTRAINT fk_userid_order FOREIGN KEY (userid) REFERENCES User(userid),
    CONSTRAINT fk_symbol_order FOREIGN KEY (symbol) REFERENCES Product(symbol)
);

-- Create Fill Table
CREATE TABLE Fill (
    fillid INT PRIMARY KEY AUTO_INCREMENT,
    orderid INT,
    userid INT,
    matchedorderid INT,
    share INT,
    price DECIMAL(15, 2),
    symbol VARCHAR(16),
    CONSTRAINT fk_orderid_fill FOREIGN KEY (orderid) REFERENCES `Order`(orderid),
    CONSTRAINT fk_matchedorderid_fill FOREIGN KEY (matchedorderid) REFERENCES `Order`(orderid),
    CONSTRAINT fk_symbol_fill FOREIGN KEY (symbol) REFERENCES Product(symbol)
);
