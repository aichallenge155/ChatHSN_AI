from discord.ext import commands

class ErrorMessages:
    EMPTY_PROMPT = "Please provide a prompt. Try again with some text after the command."
    COMMAND_NOT_FOUND = "I don't understand that command. Try `!help` to see available commands."
    API_ERROR = "I'm having trouble connecting to my AI brain. Please try again later."
    GENERAL_ERROR = "Something went wrong. Please try again later."
    STYLE_NOT_FOUND = "That style isn't available. Try `!styles` to see available styles."
    PERMISSION_ERROR = "You don't have permission to use this command."

async def handle_command_error(ctx, error):
    """Handle errors from command execution."""
    if isinstance(error, commands.MissingRequiredArgument):
        await ctx.send(ErrorMessages.EMPTY_PROMPT)
    elif isinstance(error, commands.CommandNotFound):
        await ctx.send(ErrorMessages.COMMAND_NOT_FOUND)
    elif isinstance(error, commands.CommandInvokeError):
        # Log the error for debugging (can be more specific, e.g., AI API errors)
        print(f"Command error: {error}")
        await ctx.send(ErrorMessages.GENERAL_ERROR)
    else:
        # Log unexpected errors
        print(f"Unexpected error: {error}")
        await ctx.send(ErrorMessages.GENERAL_ERROR)

def format_error_message(error_type, details=None):
    """Format a user-friendly error message."""
    if error_type == "empty_prompt":
        return ErrorMessages.EMPTY_PROMPT
    elif error_type == "api_error":
        # You can include additional details about the error, if available
        return f"{ErrorMessages.API_ERROR} Details: {details}" if details else ErrorMessages.API_ERROR
    elif error_type == "style_not_found":
        return ErrorMessages.STYLE_NOT_FOUND
    elif error_type == "permission_error":
        return ErrorMessages.PERMISSION_ERROR
    else:
        return ErrorMessages.GENERAL_ERROR
