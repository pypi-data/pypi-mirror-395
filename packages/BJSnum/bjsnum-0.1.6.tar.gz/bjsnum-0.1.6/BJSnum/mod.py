def mod(*number):
    if not number:
        return None
    
    try:
        total = number[0]
        for num in number[1:]:
            if not isinstance(num, (int, float)):
                raise TypeError(f"Type not valid for operation{number}")
            total %= num
        return total
    except (TypeError, ZeroDivisionError, OverflowError) as err:
        raise err