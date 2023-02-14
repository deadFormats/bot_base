from discord.ext import commands


class UserBlackListed(commands.CheckFailure):
    """
    Thrown when a user attempts something, but is blacklisted.
    """
    def __init__(self, message="User is blacklisted."):
        self.message = message
        super().__init__(self.message)
        
        
class UserNotOwner(commands.CheckFailure):
    def __init__(self, message="User is not an owner of the bot."):
        self.message = message
        super().__init__(self.message)


class RoleMissing(commands.CheckFailure):
    def __init__(self, message="Moderator role is missing!"):
        self.message = message
        super().__init__(self.message)


class UserNotModerator(commands.CheckFailure):
    def __init__(self, message="User is not a moderator!"):
        self.message = message
        super().__init__(self.message)
        
        
