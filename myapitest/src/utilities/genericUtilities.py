import logging as logger
import random
import string


def generate_random_email_and_password(domain=None, email_prefix=None):
    logger.debug("Generating random email and password")

    if not domain:
        domain = "gmail.com"
    if not email_prefix:
        email_prefix = "test_user"

    random_string_length = 10
    random_password_length = 20

    random_string = ''.join(random.choices(string.ascii_lowercase, k=random_string_length))
    email = email_prefix + "_" + random_string + "@" + domain
    password_string = ''.join(random.choices(string.ascii_letters, k= random_password_length))

    random_info ={'email': email, 'password': password_string}
    logger.debug(f"Randomly generated: {random_info}")

    return random_info

def generate_random_string(prefix = None, suffix= None, length = 10):
    '''
    :rtype: string
    '''
    random_string = ''.join(random.choices(string.ascii_uppercase, k=length))

    if prefix:
        random_string = prefix + random_string

    if suffix:
        random_string = random_string + suffix

    logger.debug(f"Randomly generated: {random_string}")

    return random_string