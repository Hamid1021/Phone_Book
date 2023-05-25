import os

from extensions import jalali
from django.utils import timezone
from django.core.mail import send_mail as send
from django.template.loader import render_to_string
from django.utils.html import strip_tags

def get_filename_ext(filepath):
    base_name = os.path.basename(filepath)
    name, ext = os.path.splitext(base_name)
    return name, ext


class Email(object):
    @classmethod
    def send_mail(cls, subject, from_email, recipient_list, auth_user, auth_password, template, context):
        html_message = render_to_string(template, context)
        message = strip_tags(html_message)
        try:
            send(
                subject, message, from_email, recipient_list, auth_user=auth_user,
                auth_password=auth_password, html_message=html_message
            )
        except:
            pass


def persian_numbers_converter(string):
    numbers = {
        "0": "۰",
        "1": "۱",
        "2": "۲",
        "3": "۳",
        "4": "۴",
        "5": "۵",
        "6": "۶",
        "7": "۷",
        "8": "۸",
        "9": "۹",
    }

    for e, p in numbers.items():
        string = string.replace(e, p)

    return string


def persian_day_name(num:int):
    if num == 1:
        return "دوشنبه"
    elif num == 2:
        return "سه شنبه"
    elif num == 3:
        return "چهار شنبه"
    elif num == 4:
        return "پنجشنبه"
    elif num == 5:
        return "جمعه"
    elif num == 6:
        return "شنبه"
    elif num == 7:
        return "یکشنبه"


def jalali_converter(time):
    time = timezone.localtime(time)
    p_day_name = persian_day_name(time.weekday()+1)
    time_to_str = f"{time.year},{time.month},{time.day}"
    time_to_tuple = jalali.Gregorian(time_to_str).persian_tuple()

    output = f"{time_to_tuple[0]}/{time_to_tuple[1]}/{time_to_tuple[2]} "
    output += f"{time.hour}:{time.minute} "
    output += f"{p_day_name}"

    return persian_numbers_converter(output)
