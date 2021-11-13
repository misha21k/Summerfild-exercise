import re


def read_phone(phone_text):
    phone_re = re.compile(r"""
                          ^[ \t]*
                          (?P<bracket>\()?
                          \d{3}
                          (?(bracket)\))
                          (?:[ -]?\d){7}
                          [ \t]*$
                          """, re.VERBOSE)
    phone_match = phone_re.search(phone_text)
    if phone_match:
        return re.sub(r"[- \t()]", "", phone_text)
    else:
        raise ValueError("Incorrect format for phone")


def white_phone(phone):
    print("({0}) {1} {2}".format(phone[:3], phone[3:6], phone[6:10]))

try:
    phone = read_phone(input("Enter number of phone: "))
    white_phone(phone)
except ValueError as err:
    print(err)
