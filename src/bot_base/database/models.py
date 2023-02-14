from datetime import datetime
import os

from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, BigInteger, Float, Boolean, Text
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker, relationship


Base = declarative_base()
BASEDIR = os.path.abspath(os.path.dirname(__file__))
engine = create_async_engine("sqlite+aiosqlite:///" + os.path.join(BASEDIR, 'data.db'))
AioSession = sessionmaker(engine, expire_on_commit=False, class_=AsyncSession)
Base.metadata.bind = engine
AioSession.configure(bind=engine)



class Blacklist(Base):
    __tablename__ = "blacklist"
    user_id = Column(BigInteger, primary_key=True, autoincrement=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    
    
class Warn(Base):
    __tablename__ = "warn"
    id = Column(Integer, primary_key=True)
    user_id = Column(BigInteger, nullable=False)
    server_id = Column(BigInteger, nullable=False)
    moderator_id = Column(BigInteger, nullable=False)
    reason = Column(String(255), nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    

class RosterMatch(Base):
    __tablename__ = "roster_match"
    roster_id = Column(ForeignKey("roster.id"), primary_key=True)
    match_id = Column(ForeignKey("match.id"), primary_key=True)
    won = Column(Boolean, nullable=True)
    scoreboard = Column(Text)
    
    roster = relationship("Roster", back_populates="matches")
    match = relationship("Match", back_populates="rosters")
    
    
class Match(Base):
    __tablename__ = "match"
    id = Column(Integer, primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    mode=  Column(String(32), default="hardpoint")
    game_map = Column(String(32), default="Al Bagra Fortress")
    announce_msg_id = Column(BigInteger)
    schedule = Column(DateTime, index=True)
    reported = Column(Boolean, default=False)
    
    rosters = relationship("RosterMatch", back_populates="match")
    
    
    


class Roster(Base):
    __tablename__ = "roster"
    id = Column(Integer, primary_key=True)
    team_name = Column(String(32), unique=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    captain_id = Column(BigInteger, nullable=True)
    
    players = relationship("Player", back_populates="roster")
    matches = relationship("RosterMatch", back_populates="roster")



class Player(Base):
    __tablename__ = "player"
    user_id = Column(BigInteger, primary_key=True, autoincrement=False)
    server_id = Column(BigInteger, nullable=False)
    joined_at = Column(DateTime, default=datetime.utcnow)
    activision_id = Column(String, unique=True, nullable=False)
    
    roster_id = Column(ForeignKey("roster.id"))
    roster = relationship("Roster", back_populates="players")


    
async def create_tables():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.drop_all)
        await conn.run_sync(Base.metadata.create_all)
    
    await engine.dispose()
    
    
if __name__ == "__main__":
    import asyncio
    asyncio.run(create_tables())
