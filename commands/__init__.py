from .current import setup_current_command
from .play import setup_play_command
from .skip import setup_skip_command
from .queue import setup_queue_command
from .leave import setup_leave_command

def load_commands(bot):
    setup_play_command(bot)
    setup_skip_command(bot)
    setup_queue_command(bot)
    setup_leave_command(bot)
    setup_current_command(bot)
