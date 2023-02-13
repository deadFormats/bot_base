import json
import os
from typing import Callable, TypeVar

from discord.ext import commands

from bot_base.exceptions import *
from bot_base.helpers import db_manager


T = TypeVar("T")


def is_owner() -> Callable[[T], T]:
    async def predicate(context: commands.Context) -> bool:
        config = context.bot.config
        if context.author.id not in config['owners']:
            raise UserNotOwner
            
        return True
    
    return commands.check(predicate)
    
    
def not_blacklisted() -> Callable[[T], T]:
    async def predicate(context: commands.Context) -> bool:
        if await db_manager.is_blacklisted(context.author.id):
            raise UserBlacklisted
        
        return True
    
    return commands.check(predicate)
