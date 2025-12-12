"""
Common Exceptions in Trajectory
"""


class MissingTestCaseParamsError(Exception):
    pass


class TrajectoryAPIError(Exception):
    """
    Exception raised when an error occurs while executing a Trajectory API request
    """

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message


class InvalidJudgeModelError(Exception):
    """
    Exception raised when an invalid judge model is provided
    """

    def __init__(self, message: str):
        super().__init__(message)
        self.message = message
