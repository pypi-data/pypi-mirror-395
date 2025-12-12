from .MoodleError import MoodleError


class MoodleUpdateError(MoodleError):
    def __init__(self, attribute: str, should_value: str | bool, is_value: str | bool):
        super().__init__(f'{attribute} is {is_value} but should be {should_value}')

        self.attribute: str = attribute
        self.should_value: str | bool = should_value
        self.is_value: str | bool = is_value
