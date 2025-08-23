"""Pong ゲームの実装"""
import pygame
import sys
import random


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
    
    def __init__(self, width=800, height=600, cpu_mode=True):
        """ゲームの初期化
        
        Args:
            width: 画面の幅
            height: 画面の高さ
            cpu_mode: CPUモード（Trueで右パドルがCPU制御）
        """
        pygame.init()
        self.width = width
        self.height = height
        self.screen = pygame.display.set_mode((width, height))
        pygame.display.set_caption("Pong - CPU Mode" if cpu_mode else "Pong - 2P Mode")
        self.clock = pygame.time.Clock()
        
        # フォントの初期化
        pygame.font.init()
        self.font = pygame.font.Font(None, 74)
        
        # ゲームオブジェクトの初期化
        self.ball = Ball(width // 2, height // 2, 5, 3)
        self.left_paddle = Paddle(10, height // 2 - 40, 10, 80)
        self.right_paddle = Paddle(width - 20, height // 2 - 40, 10, 80)
        
        # ゲーム状態
        self.running = True
        self.left_score = 0
        self.right_score = 0
        self.cpu_mode = cpu_mode
        
        # CPU制御用変数
        self.cpu_speed = 4
        self.cpu_reaction_delay = 0
        self.cpu_target_y = height // 2
    
    def handle_events(self):
        """イベントの処理"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
        
        # キーボード入力
        keys = pygame.key.get_pressed()
        # 左パドル（プレイヤー1）
        if keys[pygame.K_w]:
            if self.left_paddle.y > 0:
                self.left_paddle.move_up(5)
        if keys[pygame.K_s]:
            if self.left_paddle.y < self.height - self.left_paddle.height:
                self.left_paddle.move_down(5)
        
        # 右パドル（CPUモードでなければプレイヤー2）
        if not self.cpu_mode:
            if keys[pygame.K_UP]:
                if self.right_paddle.y > 0:
                    self.right_paddle.move_up(5)
            if keys[pygame.K_DOWN]:
                if self.right_paddle.y < self.height - self.right_paddle.height:
                    self.right_paddle.move_down(5)
    
    def update(self):
        """ゲーム状態の更新"""
        self.ball.update(self.width, self.height)
        
        # CPU制御
        if self.cpu_mode:
            self._update_cpu()
        
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
    
    def _update_cpu(self):
        """CPU制御の更新"""
        # 反応遅延の処理
        self.cpu_reaction_delay -= 1
        if self.cpu_reaction_delay <= 0:
            # ランダムな要素を追加して予測を困難にする
            ball_prediction_y = self.ball.y + random.uniform(-30, 30)
            self.cpu_target_y = ball_prediction_y
            self.cpu_reaction_delay = random.randint(5, 15)  # ランダムな反応遅延
        
        # パドルの中央位置
        paddle_center = self.right_paddle.y + self.right_paddle.height // 2
        
        # CPUの移動判定（ランダムな誤差を追加）
        target_diff = self.cpu_target_y - paddle_center
        move_threshold = 20  # 移動を開始する閾値
        
        if abs(target_diff) > move_threshold:
            # ランダムな速度変動
            actual_speed = self.cpu_speed + random.uniform(-1, 1)
            
            if target_diff > 0:  # 下に移動
                if self.right_paddle.y < self.height - self.right_paddle.height:
                    self.right_paddle.move_down(actual_speed)
            else:  # 上に移動
                if self.right_paddle.y > 0:
                    self.right_paddle.move_up(actual_speed)
        
        # 時々ランダムな動きを追加（ミスを演出）
        if random.randint(1, 100) <= 3:  # 3%の確率で
            if random.choice([True, False]):
                if self.right_paddle.y > 0:
                    self.right_paddle.move_up(random.uniform(2, 4))
            else:
                if self.right_paddle.y < self.height - self.right_paddle.height:
                    self.right_paddle.move_down(random.uniform(2, 4))
    
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
        
        # スコア表示
        left_text = self.font.render(str(self.left_score), True, (255, 255, 255))
        right_text = self.font.render(str(self.right_score), True, (255, 255, 255))
        self.screen.blit(left_text, (self.width // 4 - left_text.get_width() // 2, 50))
        self.screen.blit(right_text, (3 * self.width // 4 - right_text.get_width() // 2, 50))
        
        # 操作説明
        if self.cpu_mode:
            instruction = "W/S: Move Paddle | CPU vs Player"
        else:
            instruction = "W/S: P1 | UP/DOWN: P2"
        
        instruction_font = pygame.font.Font(None, 36)
        instruction_text = instruction_font.render(instruction, True, (128, 128, 128))
        self.screen.blit(instruction_text, (self.width // 2 - instruction_text.get_width() // 2, self.height - 40))
        
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