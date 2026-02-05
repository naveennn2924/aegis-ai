class Tool:
    def __init__(self, name: str):
        self.name = name

    def run(self, input_data):
        raise NotImplementedError
