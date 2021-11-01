USE [master]
CREATE DATABASE [CardsGame]
GO
--CREATE an admin database-----------------------------------------------
USE [CardsGame];
GO
CREATE LOGIN TestAdmin 
    WITH PASSWORD    = N'Admin1234',
    CHECK_POLICY     = OFF,
    CHECK_EXPIRATION = OFF;
GO
EXEC sp_addsrvrolemember 
    @loginame = N'TestAdmin', 
    @rolename = N'sysadmin';
--end-----------------------------------------------------------------------

USE [CardsGame]
GO

CREATE TABLE [dbo].[Player](
	[IdPlayer] [int] IDENTITY NOT NULL,
	[PlayerName] [varchar](30) NOT NULL,
	[PlayerScore] [int]
	PRIMARY KEY ([IdPlayer])
)
GO

CREATE TABLE [dbo].[Card](
	[IdCard] [int] IDENTITY NOT NULL,
	[CardName][varchar](40) NOT NULL,
	[CardAttack] [int] NOT NULL,
	[CardDefense] [int] NOT NULL,
	[CardImage] [VARBINARY] NOT NULL,
	PRIMARY KEY ([IdCard])
)
GO

CREATE TABLE [dbo].[PlayerXCard](
	[IdCard] [int] NOT NULL,
	[IdPlayer] [int] NOT NULL
	PRIMARY KEY ([IdCard],[IdPlayer])
)
GO

ALTER TABLE	[PlayerXCard]
	ADD CONSTRAINT [FK_PlayerXCard_Card]
	FOREIGN KEY ([IdCard]) 
	REFERENCES [Card] ([IdCard])
GO

ALTER TABLE	[PlayerXCard]
	ADD CONSTRAINT [FK_PlayerXCard_Player]
	FOREIGN KEY ([IdPlayer]) 
	REFERENCES [Player] ([IdPlayer])
GO

 ALTER TABLE [Player] 
 ADD DEFAULT 0 
 FOR [PlayerScore]
 GO




SELECT 
    DB_NAME(dbid) as DBName, 
    COUNT(dbid) as NumberOfConnections,
    loginame as LoginName
FROM
    sys.sysprocesses
WHERE 
    dbid > 0
GROUP BY 
    dbid, loginame

	SELECT * From Player

	SELECT [IdPlayer] from Player Where [IdPlayer] = 2

	UPDATE Player SET PlayerName = 'UserPatched' , PlayerScore = '5' WHERE IdPLayer=3;
