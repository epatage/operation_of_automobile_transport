from datetime import datetime

def year(request):
    """Добавляет переменную с текущим месяцем."""
    return {
        'month': datetime.now().month
    }
