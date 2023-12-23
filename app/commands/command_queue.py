from queue import Queue

from app.commands.command import Command


class CommandQueue:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not isinstance(cls._instance, cls):
            cls._instance = super(CommandQueue, cls).__new__(cls, *args, **kwargs)
            cls._instance.to_send: Queue[Command] = Queue()
            cls._instance.to_process: Queue[Command] = Queue()
        return cls._instance

    def add_command_to_send(self, command: Command):
        self.to_send.put(command)

    def add_command_to_process(self, command: Command):
        self.to_process.put(command)

    def get_command_to_send(self):
        if not self.to_send.empty():
            return self.to_send.get()
        else:
            return None

    def get_command_to_process(self):
        if not self.to_process.empty():
            return self.to_process.get()
        else:
            return None
