"""Pong ゲームの実装"""
import pygame
import sys


class Ball:
    """ボールクラス"""
    
    def __init__(self, x, y, velocity_x, velocity_y, radius=10):
        """ボールの初期化
        
        Args:
            x: X座標
            y: Y座標  
            velocity_x: X方向の速度
            velocity_y: Y方向の速度
            radius: 半径
        """
        self.x = x
        self.y = y
        self.velocity_x = velocity_x
        self.velocity_y = velocity_y
        self.radius = radius
    
    def update(self, screen_width=800, screen_height=600):
        """ボールの位置を更新し、壁との衝突をチェック
        
        Args:
            screen_width: 画面の幅
            screen_height: 画面の高さ
        """
        self.x += self.velocity_x
        self.y += self.velocity_y
        
        # 上下の壁との衝突判定
        if self.y - self.radius <= 0:
            self.y = self.radius
            self.velocity_y = -self.velocity_y
        elif self.y + self.radius >= screen_height:
            self.y = screen_height - self.radius
            self.velocity_y = -self.velocity_y


class Paddle:
    """パドルクラス"""
    
    def __init__(self, x, y, width, height):
        """パドルの初期化
        
        Args:
            x: X座標
            y: Y座標
            width: 幅
            height: 高さ
        """
        self.x = x
        self.y = y
        self.width = width
        self.height = height
    
    def move_up(self, speed):
        """パドルを上に移動
        
        Args:
            speed: 移動速度
        """
        self.y -= speed
    
    def move_down(self, speed):
        """パドルを下に移動
        
        Args:
            speed: 移動速度
        """
        self.y += speed


class PongGame:
    """Pongゲームクラス"""
    
    def __init__(self, width=800, height=600):
        """ゲームの初期化
        
        Args:
            width: 画面の幅
            height: 画面の高さ
        """
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Pong")
        self.clock = pygame.time.Clock()
        
        # ゲームオブジェクトの初期化
        self.ball = Ball(width // 2, height // 2, 5, 3)
        self.left_paddle = Paddle(10, height // 2 - 40, 10, 80)
        self.right_paddle = Paddle(width - 20, height // 2 - 40, 10, 80)
        
        # ゲーム状態
        self.running = True
        self.left_score = 0
        self.right_score = 0
    
    def handle_events(self):
        """イベントの処理"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
        
        # キーボード入力
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            if self.left_paddle.y > 0:
                self.left_paddle.move_up(5)
        if keys[pygame.K_s]:
            if self.left_paddle.y < self.height - self.left_paddle.height:
                self.left_paddle.move_down(5)
        if keys[pygame.K_UP]:
            if self.right_paddle.y > 0:
                self.right_paddle.move_up(5)
        if keys[pygame.K_DOWN]:
            if self.right_paddle.y < self.height - self.right_paddle.height:
                self.right_paddle.move_down(5)
    
    def update(self):
        """ゲーム状態の更新"""
        self.ball.update(self.width, self.height)
        
        # パドルとの衝突判定（簡易版）
        if (self.ball.x - self.ball.radius <= self.left_paddle.x + self.left_paddle.width and
            self.ball.y >= self.left_paddle.y and
            self.ball.y <= self.left_paddle.y + self.left_paddle.height):
            self.ball.velocity_x = abs(self.ball.velocity_x)
        
        if (self.ball.x + self.ball.radius >= self.right_paddle.x and
            self.ball.y >= self.right_paddle.y and
            self.ball.y <= self.right_paddle.y + self.right_paddle.height):
            self.ball.velocity_x = -abs(self.ball.velocity_x)
        
        # スコア判定
        if self.ball.x < 0:
            self.right_score += 1
            self._reset_ball()
        elif self.ball.x > self.width:
            self.left_score += 1
            self._reset_ball()
    
    def _reset_ball(self):
        """ボールをリセット"""
        self.ball.x = self.width // 2
        self.ball.y = self.height // 2
        self.ball.velocity_x = -self.ball.velocity_x
    
    def draw(self):
        """画面描画"""
        self.screen.fill((0, 0, 0))  # 黒で画面をクリア
        
        # ボールを描画
        pygame.draw.circle(self.screen, (255, 255, 255), (int(self.ball.x), int(self.ball.y)), self.ball.radius)
        
        # パドルを描画
        pygame.draw.rect(self.screen, (255, 255, 255), 
                        (self.left_paddle.x, self.left_paddle.y, self.left_paddle.width, self.left_paddle.height))
        pygame.draw.rect(self.screen, (255, 255, 255), 
                        (self.right_paddle.x, self.right_paddle.y, self.right_paddle.width, self.right_paddle.height))
        
        # 中央線
        pygame.draw.aaline(self.screen, (255, 255, 255), (self.width // 2, 0), (self.width // 2, self.height))
        
        pygame.display.flip()
    
    def run(self):
        """ゲームメインループ"""
        while self.running:
            self.handle_events()
            self.update()
            self.draw()
            self.clock.tick(60)  # 60 FPS
        
        pygame.quit()
        sys.exit()


def main():
    """メイン関数"""
    game = PongGame()
    game.run()


if __name__ == "__main__":
    main()