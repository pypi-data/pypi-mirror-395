from functools import wraps
from mixpanel import Mixpanel
import time
from polly.__init__ import __version__
from polly.constants import MIXPANEL_KEY


class Track:
    """
    This class is used for tracking polly-python services using mixpanel.
    This class will have a unidirectional association relationship with the class which wants to use the tracking service.
    The track function sends the logs to mixpanel.
    For using this feature, make an object in the __init__ function for the class this feature is to be used,
    then use the track function with that object.
    """

    def track_decorator(function):
        @wraps(function)
        def wrapper_function(*args, **kwargs):
            # flake8: noqa: C901
            execution_flag = False
            try:
                result = function(*args, **kwargs)
                execution_flag = True
            except Exception as e:
                returned_err = e
            obj = args[0].session
            tracking_env = obj.env
            email_id = obj.user_details.get("email")
            properties = {"email-id": email_id}
            # checking if args is not empty(contains self object apart from arguments)
            if len(args) > 1:
                args_list = []
                for index in range(1, len(args)):
                    args_list.append(args[index])
                properties["arguments"] = args_list
            # checking if kwargs exist
            if kwargs:
                for key, value in kwargs.items():
                    properties[key] = value
            # tracking the execution status (True/False) of the function
            properties["execution_status"] = execution_flag
            # tracking the env (dev/test/prod) in which this function was called
            properties["tracking_env"] = tracking_env
            # current polly py version
            properties["pollypy_version"] = __version__

            # current timestamp
            # reference link
            # https://stackoverflow.com/questions/16755394/
            # what-is-the-easiest-way-to-get-current-gmt-time-in-unix-timestamp-format
            properties["current_timestamp"] = time.time()

            try:
                mp = Mixpanel(MIXPANEL_KEY)
                mp.track(email_id, function.__name__, properties)
            except Exception:
                pass
            if execution_flag:
                if result is not None:
                    return result
            else:
                raise returned_err

        return wrapper_function
