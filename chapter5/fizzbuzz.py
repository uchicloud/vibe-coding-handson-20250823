def fizzbuzz(n):
    """FizzBuzz の実装
    
    Args:
        n: 0以上の整数
        
    Returns:
        str: FizzBuzz の結果
        
    Raises:
        TypeError: 引数が整数でない場合
        ValueError: 引数が負の数の場合
    """
    _validate_input(n)
    
    result = ""
    if n % 3 == 0:
        result += "Fizz"
    if n % 5 == 0:
        result += "Buzz"
    
    return result if result else str(n)


def _validate_input(n):
    """入力値の検証"""
    if not isinstance(n, int):
        raise TypeError("引数は整数である必要があります")
    
    if n < 0:
        raise ValueError("引数は0以上の整数である必要があります")