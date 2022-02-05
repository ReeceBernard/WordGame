class InvalidWordLengthError(Exception):
    """Only word lengths of 5, 6, or 7 are supported."""

    def __init__(self, message="Word length not in [5, 7] range."):
        self.message = message
        super().__init__(self.message)
