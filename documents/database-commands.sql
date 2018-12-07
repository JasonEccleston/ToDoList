DROP TABLE IF EXISTS lists;
CREATE TABLE lists(
  listId INT NOT NULL AUTO_INCREMENT,
  username varchar(30) NOT NULL,
  displayName varchar(30) NOT NULL,
  PRIMARY KEY (listId)
);


DROP TABLE IF EXISTS listItems;
CREATE TABLE listItems(
  listId INT NOT NULL,
  itemId INT NOT NULL AUTO_INCREMENT,
  item varchar(255) NOT NULL,
  PRIMARY KEY (itemId),
  FOREIGN KEY (listId) REFERENCES lists(listId)
);


DELIMITER //
DROP PROCEDURE IF EXISTS checkForList//
CREATE PROCEDURE checkForList(name varchar(30))
begin
  SELECT * FROM lists WHERE username = name;
end//
DELIMITER ;


DELIMITER //
DROP PROCEDURE IF EXISTS checkDisplayName//
CREATE PROCEDURE checkDisplayName(display varchar(30))
begin
  SELECT * FROM lists WHERE displayName = display;
end//
DELIMITER ;


DELIMITER //
DROP PROCEDURE IF EXISTS addList//
CREATE PROCEDURE addList(name varchar(30), display varchar(30))
begin
  INSERT INTO lists (username, displayName) VALUES(name, display);
end//
DELIMITER ;


DELIMITER //
DROP PROCEDURE IF EXISTS addListItem//
CREATE PROCEDURE addListItem(name varchar(30), toDo varchar(255))
begin
  SET @iD = (Select listId
    FROM lists WHERE username = name);
  INSERT INTO listItems (listId, item) VALUES(@iD, toDo);
end//
DELIMITER ;

DELIMITER //
DROP PROCEDURE IF EXISTS getUserIdByName//
CREATE PROCEDURE getUserIdByName(name varchar(30))
begin
  select listId from lists where username = name;
end//
DELIMITER ;


DELIMITER //
DROP PROCEDURE IF EXISTS getUsersList//
CREATE PROCEDURE getUsersList(userId int)
begin
  select * from listItems where listId = userId;
end//
DELIMITER ;


DELIMITER //
DROP PROCEDURE IF EXISTS deleteListItem//
CREATE PROCEDURE deleteListItem(toDoId int)
begin
  delete from listItems where itemId = toDoId;
end//
DELIMITER ;


DELIMITER //
DROP PROCEDURE IF EXISTS getUserListId//
CREATE PROCEDURE getUserListId(name varchar(30))
begin
  select listId from lists where name = username;
end//
DELIMITER ;


DELIMITER //
DROP PROCEDURE IF EXISTS getItemListId//
CREATE PROCEDURE getItemListId(toDoId int)
begin
  select listId from listItems where toDoId = itemId;
end//
DELIMITER ;


DELIMITER //
DROP PROCEDURE IF EXISTS deleteUsersList//
CREATE PROCEDURE deleteUsersList(userListId int)
begin
  delete from listItems where listId = userListId;
end//
DELIMITER ;

DELIMITER //
DROP PROCEDURE IF EXISTS deleteUser//
CREATE PROCEDURE deleteUser(userListId int)
begin
  delete from lists where userListId = listId;
end//
DELIMITER ;

DELIMITER //
DROP PROCEDURE IF EXISTS getUsers//
CREATE PROCEDURE getUsers()
begin
  select listId, displayName, username from lists;
end//
DELIMITER ;


DELIMITER //
DROP PROCEDURE IF EXISTS getUser//
CREATE PROCEDURE getUser(userListId int)
begin
  select * from lists where listId = userListId;
end//
DELIMITER ;


DELIMITER //
DROP PROCEDURE IF EXISTS updateDisplayName//
CREATE PROCEDURE updateDisplayName(userId int, newDisplay varchar(30))
begin
  update lists set displayName = newDisplay where userId = listId;
end//
DELIMITER ;


DELIMITER //
DROP PROCEDURE IF EXISTS getListItem//
CREATE PROCEDURE getListItem(toDoId int)
begin
  select item from listItems where toDoId = itemId;
end//
DELIMITER ;


DELIMITER //
DROP PROCEDURE IF EXISTS updateListItem//
CREATE PROCEDURE updateListItem(toDoId int, newToDo varchar(255))
begin
  update listItems set item = newToDo where toDoId = itemId;
end//
DELIMITER ;

DELIMITER //
DROP PROCEDURE IF EXISTS resetTables//
CREATE PROCEDURE resetTables()
begin
  DROP TABLE IF EXISTS listItems;
  DROP TABLE IF EXISTS lists;
  CREATE TABLE lists(
    listId INT NOT NULL AUTO_INCREMENT,
    username varchar(30) NOT NULL,
    displayName varchar(30) NOT NULL,
    PRIMARY KEY (listId)
  );

  CREATE TABLE listItems(
    listId INT NOT NULL,
    itemId INT NOT NULL AUTO_INCREMENT,
    item varchar(255) NOT NULL,
    PRIMARY KEY (itemId),
    FOREIGN KEY (listId) REFERENCES lists(listId)
  );
end//
DELIMITER ;
