from datetime import date

stem = '甲乙丙丁戊己庚辛壬癸'
branch = '子丑寅卯辰巳午未申酉戌亥'


def stembranch(year: int) -> str:
    """干支纪年
    :param year: int
    :return: str
    >>> stembranch(2025)
    '乙巳'
    """
    return stem[(year - 4) % 10] + branch[(year - 4) % 12]


def zodiac(year: int) -> str:
    """生肖纪年
    :param year: int
    :return: str
    >>> zodiac(2025)
    '蛇'
    """
    zodiac = '鼠牛虎兔龙蛇马羊猴鸡狗猪'
    return zodiac[(year - 4) % 12]


class Date(date):
    """农历
    >>> d = Date.today()
    >>> d.year
    2025
    >>> d.stembranch()
    '乙巳'
    """
    __stem = '甲乙丙丁戊己庚辛壬癸'
    __branch = '子丑寅卯辰巳午未申酉戌亥'

    @property
    def stem(self):
        return self.__stem

    @property
    def branch(self):
        return self.__branch

    def stembranch(self):
        return self.stem[(self.year - 4) % 10] + self.branch[(self.year - 4) % 12]

    def zodiac(self):
        zodiac = '鼠牛虎兔龙蛇马羊猴鸡狗猪'
        return zodiac[(self.year - 4) % 12]


if __name__ == '__main__':
    import doctest

    doctest.testmod()
