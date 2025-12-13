import time
from datetime import datetime

class Helpers:
    def generate_route_number(base_number):
        """
        Генерирует номер маршрута в формате BASE-YYYY-MM-DD-LAST2DIGITS

        Parameters
        ----------
        base_number : int
            Организационное подразделение пользователя
        """

        now = datetime.now()
        timestamp_ms = int(time.time() * 1000)
        return f"{base_number}-{now.strftime('%Y-%m-%d')}-{str(timestamp_ms)[-2:]}"