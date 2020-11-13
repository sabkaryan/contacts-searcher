from functools import reduce


def validate(inn: str) -> bool:
    return reduce(lambda a, b: a and b(inn), [_empty_check, _num_check, _length_check, _control_number_check], True)


def _empty_check(inn: str) -> bool:
    return bool(inn)


def _num_check(inn: str) -> bool:
    try:
        int(inn)
        return True
    except ValueError:
        return False


def _control_number_check(inn: str) -> bool:
    nums = [int(n) for n in inn]
    if len(nums) == 10:
        return (
            nums[9]
            == (
                (
                    2 * nums[0]
                    + 4 * nums[1]
                    + 10 * nums[2]
                    + 3 * nums[3]
                    + 5 * nums[4]
                    + 9 * nums[5]
                    + 4 * nums[6]
                    + 6 * nums[7]
                    + 8 * nums[8]
                )
                % 11
            )
            % 10
        )
    elif len(nums) == 11:
        return (
            nums[10]
            == (
                (
                    7 * nums[0]
                    + 2 * nums[1]
                    + 4 * nums[2]
                    + 10 * nums[3]
                    + 3 * nums[4]
                    + 5 * nums[5]
                    + 9 * nums[6]
                    + 4 * nums[7]
                    + 6 * nums[8]
                    + 8 * nums[9]
                )
                % 11
            )
            % 10
        )
    elif len(nums) == 12:
        return (
            nums[11]
            == (
                (
                    3 * nums[0]
                    + 7 * nums[1]
                    + 2 * nums[2]
                    + 4 * nums[3]
                    + 10 * nums[4]
                    + 3 * nums[5]
                    + 5 * nums[6]
                    + 9 * nums[7]
                    + 4 * nums[8]
                    + 6 * nums[9]
                    + 8 * nums[10]
                )
                % 11
            )
            % 10
        )

    return False


def _length_check(inn: str) -> bool:
    return len(inn) == 10 or len(inn) == 12
