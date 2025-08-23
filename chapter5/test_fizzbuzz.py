import pytest
from fizzbuzz import fizzbuzz


class TestFizzBuzz:
    """FizzBuzz のテストクラス"""
    
    def test_fizzbuzz_returns_1_for_1(self):
        """1 を渡すと '1' を返す"""
        assert fizzbuzz(1) == "1"
    
    def test_fizzbuzz_returns_2_for_2(self):
        """2 を渡すと '2' を返す"""
        assert fizzbuzz(2) == "2"
    
    def test_fizzbuzz_returns_fizz_for_3(self):
        """3 を渡すと 'Fizz' を返す"""
        assert fizzbuzz(3) == "Fizz"
    
    def test_fizzbuzz_returns_buzz_for_5(self):
        """5 を渡すと 'Buzz' を返す"""
        assert fizzbuzz(5) == "Buzz"
    
    def test_fizzbuzz_returns_fizzbuzz_for_15(self):
        """15 を渡すと 'FizzBuzz' を返す"""
        assert fizzbuzz(15) == "FizzBuzz"
    
    # より多くのケースをテスト
    def test_fizzbuzz_returns_fizz_for_6(self):
        """6 を渡すと 'Fizz' を返す"""
        assert fizzbuzz(6) == "Fizz"
    
    def test_fizzbuzz_returns_buzz_for_10(self):
        """10 を渡すと 'Buzz' を返す"""
        assert fizzbuzz(10) == "Buzz"
    
    def test_fizzbuzz_returns_fizzbuzz_for_30(self):
        """30 を渡すと 'FizzBuzz' を返す"""
        assert fizzbuzz(30) == "FizzBuzz"
    
    # 境界値テスト
    def test_fizzbuzz_returns_fizzbuzz_for_0(self):
        """0 を渡すと 'FizzBuzz' を返す（0は3と5の倍数）"""
        assert fizzbuzz(0) == "FizzBuzz"
    
    # 例外ケースのテスト
    def test_fizzbuzz_raises_error_for_negative_number(self):
        """負の数を渡すと ValueError を発生させる"""
        with pytest.raises(ValueError, match="引数は0以上の整数である必要があります"):
            fizzbuzz(-1)
    
    def test_fizzbuzz_raises_error_for_non_integer(self):
        """整数以外を渡すと TypeError を発生させる"""
        with pytest.raises(TypeError, match="引数は整数である必要があります"):
            fizzbuzz(3.14)