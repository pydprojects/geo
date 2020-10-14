from rest_framework.exceptions import APIException


class UserDoesNotExist(APIException):
    status_code = 404
    default_detail = "The user ID does not exist."
    default_code = "user_does_not_exist"


class NegativePoints(APIException):
    status_code = 400
    default_detail = "User does not have enough points."
    default_code = "negative_points"


class ZeroPoints(APIException):
    status_code = 400
    default_detail = "Number of points must be more than zero."
    default_code = "zero_points"
