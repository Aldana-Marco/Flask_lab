SQL_SELECT_ALL = "SELECT [IdPlayer], [PlayerName], [PLayerScore] FROM Player"
SQL_INSERT_PLAYER="INSERT [dbo].[Player] ([PlayerName], [PlayerScore]) VALUES ('{}', {})"
SQL_SELECT_PLAYER="SELECT [IdPlayer], [PlayerName], [PLayerScore] FROM Player WHERE [IdPlayer] = {}"
SQL_MAX_ID_PLAYER="SELECT MAX([IdPlayer]) FROM Player"
PLAYER_PROPERTIES = ("id", "name", "score")
