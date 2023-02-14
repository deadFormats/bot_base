from sqlalchemy import select, func
from bot_base.database import models


bracket_statuses = {
    "Registered",
    "Undefeated",
    "Losers Bracket",
    "Eliminated"
}


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
            total = await session.execute(
                select(func.count()).select_from(models.Blacklist)
            )
            result = total.scalars()
            
            new = models.Blacklist(user_id=user_id)
            session.add(new)
            
            
        await session.commit()
        return result.one() + 1
        
    
async def remove_user_from_blacklist(user_id: int) -> int:
    """
    This will remove a user id from the blacklist.
    
    :param user_id: The id of the user to remove from the blacklist table
    :return: Total number of rows in blacklist table after removing
    """
    async with models.AioSession() as session:
        async with session.begin():
            result = await session.execute(
                select(models.Blacklist).where(models.Blacklist.user_id == user_id)
            )
            user = result.scalars().one_or_none()
            result = await session.execute(
                select(func.count()).select_from(models.Blacklist)
            )
            total = result.scalars().one()
            if user is None:
                return total
            session.delete(user)
        await session.commit()
        return total - 1
        

async def get_moderator_role_id(server_id: int) -> int:
    async with models.AioSession() as session:
        async with session.begin():
            result = await session.execute(
                select(models.ModRole).where(models.ModRole.server_id == server_id)
            )
            mod_role = result.scalars().one_or_none()
            if mod_role is None:
                return None
            return mod_role.role_id
            
    
