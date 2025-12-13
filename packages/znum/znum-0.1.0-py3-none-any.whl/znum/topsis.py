from .utils import Beast
from .dist import Dist
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from znum.core import Znum


class Topsis:
    class DataType:
        ALTERNATIVE = "A"
        CRITERIA = "C"
        TYPE = "TYPE"

    class DistanceMethod:
        SIMPLE = 1
        HELLINGER = 2

    @staticmethod
    def solver_main(table: list[list], shouldNormalizeWeight=False, distanceType=DistanceMethod.HELLINGER):
        """
        table[0] -> weights
        table[1:-1] -> main part
        table[-1] -> criteria types
        :param shouldNormalizeWeight:
        :param table:
        :param distanceType:
        :return:
        """

        weights: list[Znum] = table[0]
        table_main_part: list[list[Znum]] = table[1:-1]
        criteria_types: list[str] = table[-1]
        print(f'{table_main_part = }')
        main_table_part_transpose = tuple(zip(*table_main_part))

        for column_number, column in enumerate(main_table_part_transpose):
            Beast.normalize(column, criteria_types[column_number])

        if shouldNormalizeWeight:
            Beast.normalize_weight(weights)

        Topsis.weightage(table_main_part, weights)

        if distanceType == Topsis.DistanceMethod.SIMPLE:
            table_1 = Topsis.get_table_n(table_main_part, lambda znum: Dist.Simple.calculate(znum, 1))
            table_0 = Topsis.get_table_n(table_main_part, lambda znum: Dist.Simple.calculate(znum, 0))
        else:
            table_1 = Topsis.get_table_n(table_main_part, lambda znum: Dist.Hellinger.calculate(znum,
                                                                                                Dist.Hellinger.get_ideal_from_znum(
                                                                                                    znum, 1)))
            table_0 = Topsis.get_table_n(table_main_part, lambda znum: Dist.Hellinger.calculate(znum,
                                                                                                Dist.Hellinger.get_ideal_from_znum(
                                                                                                    znum, 0)))

        s_best = Topsis.find_extremum(table_1)
        s_worst = Topsis.find_extremum(table_0)
        p = Topsis.find_distance(s_best, s_worst)

        return p

    @staticmethod
    def weightage(table_main_part, weights):
        for row in table_main_part:
            for i, (znum, weight) in enumerate(zip(row, weights)):
                row[i] = znum * weight

    @staticmethod
    def get_table_n(table_main_part: list[list['Znum']], distanceSolver):
        table_n = []
        for row in table_main_part:
            row_n = []
            for znum in row:
                number = distanceSolver(znum)
                row_n.append(number)
            table_n.append(row_n)
        return table_n

    @staticmethod
    def find_extremum(table_n: list[list[int]]):
        return [sum(row) for row in table_n]

    @staticmethod
    def find_distance(s_best, s_worst):
        return [worst / (best + worst) for best, worst in zip(s_best, s_worst)]
