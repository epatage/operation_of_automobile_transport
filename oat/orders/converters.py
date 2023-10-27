import datetime


class DateConverter:
    """
    Конвертер даты из url.

    Не используется, к удалению!
    """

    regex = '[0-9]{4}-[0-9]{2}-[0-9]{2}'
    format = '%Y-%m-%d'

    def to_python(self, value):
        return datetime.datetime.strptime(value, self.format).date()

    def to_url(self, value):
        return value.strftime(self.format)


class FourDigitYearConverter:
    """
    Конвертер года из url.

    Не используется, к удалению!
    """

    regex = '[0-9]{4}'

    def to_python(self, value):
        return int(value)

    def to_url(self, value):
        return '%04d' % value
