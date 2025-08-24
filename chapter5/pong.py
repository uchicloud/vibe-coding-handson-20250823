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
        self.x = float(x)
        self.y = float(y)
        self.velocity_x = float(velocity_x)
        self.velocity_y = float(velocity_y)
        self.radius = radius
        self.owner = 'neutral'  # 'neutral', 'left', 'right'  # 'neutral', 'left', 'right'
    
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
    
    def get_color(self):
        """ボールの色を所有者に基づいて取得"""
        colors = {
            'neutral': (255, 255, 255),  # 白
            'left': (255, 100, 100),     # 赤っぽい
            'right': (100, 100, 255)     # 青っぽい
        }
        return colors.get(self.owner, (255, 255, 255))
    
    def set_owner(self, owner):
        """ボールの所有者を設定"""
        self.owner = owner


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

class HelperItem:
    """おたすけアイテムクラス"""
    
    def __init__(self, x, y, item_type):
        """アイテムの初期化
        
        Args:
            x: X座標
            y: Y座標  
            item_type: アイテムの種類 ('big_paddle', 'slow_ball', 'fast_paddle')
        """
        self.x = x
        self.y = y
        self.radius = 15
        self.item_type = item_type
        self.active = True
        self.lifetime = 600  # 10秒（60FPS * 10）
        
        # アイテムの色を種類によって変える
        self.colors = {
            'big_paddle': (0, 255, 0),    # 緑：パドル拡大
            'slow_ball': (0, 0, 255),     # 青：ボール減速
            'fast_paddle': (255, 255, 0)  # 黄：パドル高速化
        }
        self.color = self.colors.get(item_type, (255, 255, 255))
    
    def update(self):
        """アイテムの更新"""
        self.lifetime -= 1
        if self.lifetime <= 0:
            self.active = False
    
    def draw(self, screen):
        """アイテムの描画"""
        if self.active:
            pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.radius)
            # アイテムの種類を示すマーク
            font = pygame.font.Font(None, 24)
            marks = {'big_paddle': 'P+', 'slow_ball': 'S-', 'fast_paddle': 'F+'}
            mark_text = font.render(marks.get(self.item_type, '?'), True, (0, 0, 0))
            text_rect = mark_text.get_rect(center=(int(self.x), int(self.y)))
            screen.blit(mark_text, text_rect)


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
        
        # おたすけアイテム関連
        self.helper_items = []
        self.item_spawn_timer = 0
        self.item_spawn_interval = 300  # 5秒間隔でアイテム出現（60FPS * 5）
        self.item_types = ['big_paddle', 'slow_ball', 'fast_paddle']
        
        # アイテム効果の状態
        self.left_paddle_original_height = 80
        self.right_paddle_original_height = 80
        self.active_effects = {'left': {}, 'right': {}}  # 各プレイヤーのアクティブ効果
        
        # ボール速度の保存（効果の正確な復元のため）
        self.ball_original_velocity_x = 5.0
        self.ball_original_velocity_y = 3.0
        self.ball_speed_effects = []  # アクティブな速度効果のスタック  # 各プレイヤーのアクティブ効果
    
    def handle_events(self):
        """イベントの処理"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
        
        # キーボード入力
        keys = pygame.key.get_pressed()
        
        # パドル移動速度（fast_paddle効果を考慮）
        left_speed = 8 if 'fast_paddle' in self.active_effects['left'] else 5
        right_speed = 8 if 'fast_paddle' in self.active_effects['right'] else 5
        
        # 左パドル（プレイヤー1）
        if keys[pygame.K_w]:
            if self.left_paddle.y > 0:
                self.left_paddle.move_up(left_speed)
        if keys[pygame.K_s]:
            if self.left_paddle.y < self.height - self.left_paddle.height:
                self.left_paddle.move_down(left_speed)
        
        # 右パドル（CPUモードでなければプレイヤー2）
        if not self.cpu_mode:
            if keys[pygame.K_UP]:
                if self.right_paddle.y > 0:
                    self.right_paddle.move_up(right_speed)
            if keys[pygame.K_DOWN]:
                if self.right_paddle.y < self.height - self.right_paddle.height:
                    self.right_paddle.move_down(right_speed)
    
    def update(self):
        """ゲーム状態の更新"""
        self.ball.update(self.width, self.height)
        
        # CPU制御
        if self.cpu_mode:
            self._update_cpu()
        
        # おたすけアイテムの更新
        self._update_helper_items()
        
        # 効果時間の更新（毎フレーム実行）
        self._update_effect_timers()
        
        # パドルとの衝突判定（簡易版）
        if (self.ball.x - self.ball.radius <= self.left_paddle.x + self.left_paddle.width and
            self.ball.y >= self.left_paddle.y and
            self.ball.y <= self.left_paddle.y + self.left_paddle.height):
            self.ball.velocity_x = abs(self.ball.velocity_x)
            self.ball.set_owner('left')  # 左プレイヤーの所有に
        
        if (self.ball.x + self.ball.radius >= self.right_paddle.x and
            self.ball.y >= self.right_paddle.y and
            self.ball.y <= self.right_paddle.y + self.right_paddle.height):
            self.ball.velocity_x = -abs(self.ball.velocity_x)
            self.ball.set_owner('right')  # 右プレイヤーの所有に
        
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
        # すべてのボール速度効果をクリアして元の速度に戻す
        self.ball_speed_effects.clear()
        
        # 方向を保持して元の速度に戻す
        direction_x = 1 if self.ball.velocity_x > 0 else -1
        direction_y = 1 if self.ball.velocity_y > 0 else -1
        
        self.ball.x = float(self.width // 2)
        self.ball.y = float(self.height // 2)
        self.ball.velocity_x = self.ball_original_velocity_x * -direction_x  # 方向転換
        self.ball.velocity_y = self.ball_original_velocity_y * direction_y
        self.ball.set_owner('neutral')  # ニュートラルに戻す  # ニュートラルに戻す

    def _update_helper_items(self):
        """おたすけアイテムの更新処理"""
        # アイテムの生成タイマー
        self.item_spawn_timer += 1
        if self.item_spawn_timer >= self.item_spawn_interval:
            self._spawn_helper_item()
            self.item_spawn_timer = 0
        
        # 既存アイテムの更新
        for item in self.helper_items[:]:  # コピーを作って反復
            item.update()
            if not item.active:
                self.helper_items.remove(item)
        
        # アイテムとパドルの衝突判定
        self._check_item_collisions()
    
    def _spawn_helper_item(self):
        """おたすけアイテムの生成"""
        if len(self.helper_items) < 3:  # 最大3個まで
            x = random.randint(200, self.width - 200)  # 画面中央付近
            y = random.randint(100, self.height - 100)
            item_type = random.choice(self.item_types)
            new_item = HelperItem(x, y, item_type)
            self.helper_items.append(new_item)
    
    def _check_item_collisions(self):
        """アイテムとパドル・ボールの衝突判定"""
        for item in self.helper_items[:]:
            # ボールとの衝突判定
            ball_distance = ((self.ball.x - item.x) ** 2 + (self.ball.y - item.y) ** 2) ** 0.5
            if ball_distance < self.ball.radius + item.radius:
                # ボールの所有者に基づいて効果を適用
                if self.ball.owner == 'left':
                    self._apply_item_effect('left', item.item_type)
                elif self.ball.owner == 'right':
                    self._apply_item_effect('right', item.item_type)
                # ニュートラルの場合は効果なし
                self.helper_items.remove(item)
                continue
            
            # 左パドルとの衝突
            if (abs(item.x - (self.left_paddle.x + self.left_paddle.width/2)) < item.radius + self.left_paddle.width/2 and
                abs(item.y - (self.left_paddle.y + self.left_paddle.height/2)) < item.radius + self.left_paddle.height/2):
                self._apply_item_effect('left', item.item_type)
                self.helper_items.remove(item)
                continue
            
            # 右パドルとの衝突
            if (abs(item.x - (self.right_paddle.x + self.right_paddle.width/2)) < item.radius + self.right_paddle.width/2 and
                abs(item.y - (self.right_paddle.y + self.right_paddle.height/2)) < item.radius + self.right_paddle.height/2):
                self._apply_item_effect('right', item.item_type)
                self.helper_items.remove(item)
                continue
    
    def _apply_item_effect(self, player, item_type):
        """アイテム効果の適用"""
        effect_duration = 600  # 10秒間
        
        if item_type == 'big_paddle':
            if player == 'left':
                self.left_paddle.height = int(self.left_paddle_original_height * 1.5)
            else:
                self.right_paddle.height = int(self.right_paddle_original_height * 1.5)
            self.active_effects[player][item_type] = effect_duration
            
        elif item_type == 'slow_ball':
            # ボール速度を75%に減速（スタックベースで管理）
            self.ball.velocity_x *= 0.75
            self.ball.velocity_y *= 0.75
            self.ball_speed_effects.append({'type': 'slow', 'multiplier': 0.75, 'duration': effect_duration, 'player': player})
            self.active_effects[player][item_type] = effect_duration
            
        elif item_type == 'fast_paddle':
            # そのプレイヤーのパドル移動速度アップ（handle_eventsで使用）
            self.active_effects[player][item_type] = effect_duration
    
    def _update_effect_timers(self):
        """効果時間の更新と期限切れ効果の削除"""
        # パドルとその他の効果
        for player in ['left', 'right']:
            for effect_type in list(self.active_effects[player].keys()):
                self.active_effects[player][effect_type] -= 1
                
                if self.active_effects[player][effect_type] <= 0:
                    # 効果の解除
                    if effect_type == 'big_paddle':
                        if player == 'left':
                            self.left_paddle.height = self.left_paddle_original_height
                        else:
                            self.right_paddle.height = self.right_paddle_original_height
                    
                    del self.active_effects[player][effect_type]
        
        # ボール速度効果の管理（スタックベース）
        for effect in self.ball_speed_effects[:]:
            effect['duration'] -= 1
            if effect['duration'] <= 0:
                # 効果を逆転させて元に戻す
                self.ball.velocity_x /= effect['multiplier']
                self.ball.velocity_y /= effect['multiplier']
                self.ball_speed_effects.remove(effect)
    
    def draw(self):
        """画面描画"""
        self.screen.fill((0, 0, 0))  # 黒で画面をクリア
        
        # ボールを所有者に基づいた色で描画
        ball_color = self.ball.get_color()
        pygame.draw.circle(self.screen, ball_color, (int(self.ball.x), int(self.ball.y)), self.ball.radius)
        
        # パドルを描画（アクティブ効果があれば色を変える）
        left_color = (0, 255, 0) if self.active_effects['left'] else (255, 255, 255)
        right_color = (0, 255, 0) if self.active_effects['right'] else (255, 255, 255)
        
        pygame.draw.rect(self.screen, left_color, 
                        (self.left_paddle.x, self.left_paddle.y, self.left_paddle.width, self.left_paddle.height))
        pygame.draw.rect(self.screen, right_color, 
                        (self.right_paddle.x, self.right_paddle.y, self.right_paddle.width, self.right_paddle.height))
        
        # おたすけアイテムを描画
        for item in self.helper_items:
            item.draw(self.screen)
        
        # 中央線
        pygame.draw.aaline(self.screen, (255, 255, 255), (self.width // 2, 0), (self.width // 2, self.height))
        
        # スコア表示
        left_text = self.font.render(str(self.left_score), True, (255, 255, 255))
        right_text = self.font.render(str(self.right_score), True, (255, 255, 255))
        self.screen.blit(left_text, (self.width // 4 - left_text.get_width() // 2, 50))
        self.screen.blit(right_text, (3 * self.width // 4 - right_text.get_width() // 2, 50))
        
        # アクティブ効果の表示
        self._draw_active_effects()
        
        # 操作説明
        if self.cpu_mode:
            instruction = "W/S: Move | Ball hits item = effect | Red=P1 Blue=P2 White=Neutral"
        else:
            instruction = "W/S: P1 | UP/DOWN: P2 | Ball hits item = effect | Red=P1 Blue=P2 White=Neutral"
        
        instruction_font = pygame.font.Font(None, 18)
        instruction_text = instruction_font.render(instruction, True, (128, 128, 128))
        self.screen.blit(instruction_text, (self.width // 2 - instruction_text.get_width() // 2, self.height - 40))
        
        pygame.display.flip()
    
    def _draw_active_effects(self):
        """アクティブ効果のUI表示"""
        effect_font = pygame.font.Font(None, 24)
        y_offset = 120
        
        # 左プレイヤーの効果
        if self.active_effects['left']:
            effects_text = "P1: " + ", ".join([f"{eff}({timer//60+1}s)" 
                                             for eff, timer in self.active_effects['left'].items()])
            effect_surface = effect_font.render(effects_text, True, (0, 255, 0))
            self.screen.blit(effect_surface, (10, y_offset))
        
        # 右プレイヤーの効果
        if self.active_effects['right']:
            effects_text = "P2: " + ", ".join([f"{eff}({timer//60+1}s)" 
                                             for eff, timer in self.active_effects['right'].items()])
            effect_surface = effect_font.render(effects_text, True, (0, 255, 0))
            self.screen.blit(effect_surface, (self.width - 200, y_offset))
    
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