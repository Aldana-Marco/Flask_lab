SQL_SELECT_ALL = "SELECT [IdPlayer], [PlayerName], [PLayerScore] FROM Player"
SQL_INSERT_PLAYER = "INSERT [dbo].[Player] ([PlayerName], [PlayerScore]) VALUES ('{}', {})"
SQL_SELECT_PLAYER = "SELECT [IdPlayer], [PlayerName], [PlayerScore] FROM Player WHERE [IdPlayer] = {}"
PLAYER_PROPERTIES = "IdPlayer", "PlayerName", "PlayerScore"
SQL_SELECT_MAX_ID_PLAYER = "SELECT TOP 1 [IdPlayer], [PlayerName], [PLayerScore] FROM Player ORDER BY IdPlayer DESC"
SQL_DELETE_PLAYER = "DELETE FROM Player WHERE IdPLayer={}"
SQL_INSERT_AUDIT = "INSERT [dbo].[Audit] ( [Request],[Time], [IdSession], [Status]) VALUES ('{}',convert(datetime,'{}'),'{}','{}')"
SQL_UPDATE_AUDIT_STATUS = "UPDATE [Audit] SET [Status]='{}' WHERE [IdSession]='{}';"
