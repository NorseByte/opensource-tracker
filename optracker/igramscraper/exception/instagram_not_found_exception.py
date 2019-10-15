class InstagramNotFoundException(Exception):
    def __init__(self, message="", code=404):
        super().__init__(f'{message}, Code:{code}')
