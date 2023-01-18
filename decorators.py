def error_handler(func):
    def wrapper(*args):
        try:
            return func(*args)
        except IndexError:
            return "You didn't provide contact name or phone number"
        except ValueError:
            return "Phone number must include digits only"
        except KeyError:
            return "User is not in contact list"
        except TypeError:
            return "You didn't provide enough parameters"
    return wrapper
