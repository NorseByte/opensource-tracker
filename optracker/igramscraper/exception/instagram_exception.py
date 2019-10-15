class InstagramException(Exception):
    StatusCode = -1

    def __init__(self, message="", code=500):
        super().__init__(f'{message}, Code:{code}')
    
    @staticmethod
    def default(response_text, status_code):
        StatusCode = status_code
        return InstagramException(
            'Response code is {status_code}. Body: {response_text} '
            'Something went wrong. Please report issue.'.format(
                response_text=response_text, status_code=status_code),
            status_code)
