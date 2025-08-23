#!/usr/bin/env python3
"""FizzBuzz の実行スクリプト"""

from fizzbuzz import fizzbuzz


def main():
    """FizzBuzz を1から100まで実行して結果を表示"""
    print("FizzBuzz (1-100):")
    print("-" * 20)
    
    for i in range(1, 101):
        result = fizzbuzz(i)
        print(f"{i:3d}: {result}")


if __name__ == "__main__":
    main()