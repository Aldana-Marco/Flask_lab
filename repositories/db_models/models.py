from flask import g
from sqlalchemy import Table, Column, MetaData, Integer, String, LargeBinary, Text, DateTime, insert

metadata = MetaData()

cards_table = Table("CARDS", metadata,
                    Column("IdCard", Integer, primary_key=True, autoincrement=True),
                    Column("CardName", String(50), nullable=False),
                    Column("CardAttack", Integer, nullable=False),
                    Column("CardDefense", Integer, nullable=False),
                    Column("CardImage", Text, default="none", nullable=False)
                    )

players_table = Table("PLAYERS", metadata,
                      Column("IdPlayer", Integer, primary_key=True, autoincrement=True),
                      Column("PlayerName", String(50), nullable=False),
                      Column("PlayerScore", Integer, default=0, nullable=False),
                      )

audits_table = Table("AUDITS", metadata,
                     Column("IdAudit", Integer, primary_key=True, autoincrement=True),
                     Column("Request", Text, nullable=False),
                     Column("Time", DateTime, nullable=False),
                     Column("IdSession", Text, nullable=False),
                     Column("Status", Text, nullable=False)
                     )

def create_players(list_names: list):
    with g.engine.begin() as connection:
        names=[]
        for name in list_names:
            names.append({'PlayerName': name})
        connection.execute(players_table.insert(), names)


# card_insert=cards.insert().values(CardName = 'Ravi', Attack = 6, )
