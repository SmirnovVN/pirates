

class Command:
    def __init__(self, command_type, params=None):
        if params is None:
            params = {}
        self.command_type = command_type
        self.params = params
        
    def execute(self, *args, **kwargs):
        raise NotImplementedError