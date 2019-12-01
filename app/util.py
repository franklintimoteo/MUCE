
def filter_emails(emails):
    """
    :param emails: string with emails separated commas or semicolon
    :return: list emails
    """
    emails = emails.split(';').split(',')
    return emails
