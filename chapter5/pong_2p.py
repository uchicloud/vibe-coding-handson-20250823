#!/usr/bin/env python3
"""Pong 2Pモードの実行スクリプト"""

from pong import PongGame


def main():
    """2プレイヤーモードでPongゲームを起動"""
    print("Starting Pong in 2-Player Mode...")
    print("Player 1: W/S keys")
    print("Player 2: UP/DOWN arrow keys")
    print("Press ESC or close window to quit")
    
    game = PongGame(cpu_mode=False)
    game.run()


if __name__ == "__main__":
    main()