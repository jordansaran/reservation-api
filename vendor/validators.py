from rest_framework.exceptions import ValidationError


def not_date_past(date):
    if date < date.today():
        raise ValidationError("A data não pode ser inferior a data atual")
    return date
