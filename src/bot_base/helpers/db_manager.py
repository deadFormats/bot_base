from sqlalchemy import select
from bot_base.database import models


async def get_blacklisted_users() -> list:
    """
    This will fetch a list of all the users that are currently blacklisted.
    
    :return: List of user ids of blacklisted users
    """
    async with models.AioSession() as session:
        async with session.begin():
            result = await session.execute(
                select(models.Blacklist)
            )
            
            blacklist = result.scalars().all()
            return blacklist
            
            

async def is_blacklisted(user_id: int) -> bool:
    """
    This will check if a user id is blacklisted.
    
    :param user_id: The id of the user to check
    :return: True if the user is blacklisted
    """
    async with models.AioSession() as session:
        async with session.begin():
            result = await session.execute(
                select(models.Blacklist).where(models.Blacklist.user_id == user_id)
            )
            
            user = result.scalars().one_or_none()
            return user is not None
            
            
async def add_user_to_blacklist(user_id: int) -> int:
    """
    This will add a user id to the blacklist 
    
    :param user_id: The id of the user to blacklist.
    """
    async with models.AioSession() as session:
        async with session.begin():
            new = models.Blacklist(user_id=user_id)
            session.add(new)
            
        await session.commit()
    
