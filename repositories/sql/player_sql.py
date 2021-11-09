PLAYER_PROPERTIES = "IdPlayer", "PlayerName", "PlayerScore"
SQL_SELECT_MAX_ID_PLAYER = "SELECT IdPlayer, PlayerName, PlayerScore FROM Players WHERE IdPlayer=(SELECT MAX(IdPlayer) FROM Players)" #"SELECT IdPlayer, PlayerName, PlayerScore FROM Players ORDER BY IdPlayer DESC LIMIT 1"
SQL_INSERT_PLAYER = "INSERT Players (PlayerName, PlayerScore) VALUES ('{}', {})"
SQL_SELECT_ALL = "SELECT IdPlayer, PlayerName, PlayerScore FROM Players"
SQL_SELECT_PLAYER = "SELECT IdPlayer, PlayerName, PlayerScore FROM Players WHERE IdPlayer = {}"
SQL_DELETE_PLAYER = "DELETE FROM Players WHERE IdPLayer={}"


AUDIT_PROPERTIES = "IdAudit", "Request", "Time", "IdSession", "Status"
SQL_INSERT_AUDIT = "INSERT Audits ( Request,`Time`, IdSession, `Status`) VALUES ('{}','{}','{}','{}')"
SQL_UPDATE_AUDIT_STATUS = "UPDATE audits SET status='{}' WHERE idsession='{}';"


CARD_PROPERTIES = "IdCard", "CardName", "CardAttack", "CardDefense", "CardImage"
#SQL_INSERT_CARD = "INSERT INTO [Cards] ( [CardName],[CardAttack],[CardDefense],[CardImage]) SELECT '{}', {}, {}, BulkColumn FROM OPENROWSET(BULK ''{}'', SINGLE_BLOB)as image;"
SQL_INSERT_CARD = "INSERT INTO [Cards] ( [CardName],[CardAttack],[CardDefense],[CardImage]) SELECT '{}', {}, {}, '{}'"
SQL_SELECT_MAX_ID_CARD = "SELECT TOP 1 [IdCard], [CardName], [CardAttack],[CardDefense],[CardImage] FROM Cards ORDER BY IdCard DESC"



