import pytest
import pygame
from pong import Ball, Paddle, PongGame


class TestBall:
    """ボールのテストクラス"""
    
    def test_ball_initialization(self):
        """ボールが正しく初期化される"""
        ball = Ball(400, 300, 5, 5)
        assert ball.x == 400
        assert ball.y == 300
        assert ball.velocity_x == 5
        assert ball.velocity_y == 5
        assert ball.radius == 10  # デフォルト値
    
    def test_ball_update_moves_ball(self):
        """ボールのアップデートで位置が更新される"""
        ball = Ball(400, 300, 5, -3)
        ball.update()
        assert ball.x == 405
        assert ball.y == 297
    
    def test_ball_bounces_off_top_wall(self):
        """ボールが上の壁で反射する"""
        ball = Ball(400, 10, 5, -5)  # 上方向に移動
        ball.update(screen_height=600)
        assert ball.velocity_y == 5  # Y方向の速度が反転
        assert ball.y == 10  # 位置は壁に制限される
    
    def test_ball_bounces_off_bottom_wall(self):
        """ボールが下の壁で反射する"""
        ball = Ball(400, 590, 5, 5)  # 下方向に移動
        ball.update(screen_height=600)
        assert ball.velocity_y == -5  # Y方向の速度が反転
        assert ball.y == 590  # 位置は壁に制限される


class TestPaddle:
    """パドルのテストクラス"""
    
    def test_paddle_initialization(self):
        """パドルが正しく初期化される"""
        paddle = Paddle(50, 250, 10, 80)
        assert paddle.x == 50
        assert paddle.y == 250
        assert paddle.width == 10
        assert paddle.height == 80
    
    def test_paddle_move_up(self):
        """パドルが上に移動する"""
        paddle = Paddle(50, 250, 10, 80)
        paddle.move_up(5)
        assert paddle.y == 245
    
    def test_paddle_move_down(self):
        """パドルが下に移動する"""
        paddle = Paddle(50, 250, 10, 80)
        paddle.move_down(5)
        assert paddle.y == 255