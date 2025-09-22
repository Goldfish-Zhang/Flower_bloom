import pygame
import math
import random
from typing import List, Tuple
from real_data_config import REAL_ROSE_DATA, ANIMATION_TIME_MAPPING, DATA_SOURCES, SHOW_REAL_DATA, DATA_DISPLAY_POSITION, DATA_FONT_SIZE

# 初始化Pygame
pygame.init()

# 常量
SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 800
FPS = 60
SCREEN_CENTER = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

# 缓动函数
def ease_out_cubic(t):
    """三次缓出函数 - 快速开始，缓慢结束"""
    return 1 - (1 - t) ** 3

def ease_in_out_cubic(t):
    """三次缓入缓出函数"""
    if t < 0.5:
        return 4 * t * t * t
    else:
        return 1 - (-2 * t + 2) ** 3 / 2

def ease_out_elastic(t):
    """弹性缓出函数 - 模拟真实花瓣的弹性"""
    if t == 0:
        return 0
    elif t == 1:
        return 1
    else:
        c4 = (2 * math.pi) / 3
        return 2 ** (-10 * t) * math.sin((t * 10 - 0.75) * c4) + 1

def ease_out_back(t):
    """回弹缓出函数"""
    c1 = 1.70158
    c3 = c1 + 1
    return 1 + c3 * (t - 1) ** 3 + c1 * (t - 1) ** 2

def ease_in_out_sine(t):
    """正弦缓入缓出函数"""
    return -(math.cos(math.pi * t) - 1) / 2

# 季节颜色系统
class SeasonalBloomColors:
    """季节性花朵颜色系统"""
    
    # 春季 - 花苞期颜色
    SPRING_BUD_DEEP = (34, 79, 23)      # 深绿色
    SPRING_BUD_LIGHT = (85, 107, 47)    # 橄榄绿
    SPRING_BLOOM = (255, 182, 193)      # 樱花粉
    SPRING_GLOW = (255, 240, 245)       # 淡粉白色
    SPRING_BG = (240, 255, 240)         # 淡绿背景
    
    # 夏季 - 盛开期颜色  
    SUMMER_BUD_DEEP = (139, 0, 0)       # 深红色
    SUMMER_BUD_LIGHT = (165, 42, 42)    # 棕红色
    SUMMER_BLOOM = (255, 20, 147)       # 深粉红
    SUMMER_GLOW = (255, 105, 180)       # 亮粉红
    SUMMER_BG = (255, 250, 240)         # 温暖米色
    
    # 秋季 - 维持期颜色
    AUTUMN_BUD_DEEP = (139, 69, 19)     # 深褐色
    AUTUMN_BUD_LIGHT = (160, 82, 45)    # 棕褐色
    AUTUMN_BLOOM = (255, 140, 0)        # 橙色
    AUTUMN_GLOW = (255, 215, 0)         # 金色
    AUTUMN_BG = (255, 248, 220)         # 秋日米色
    
    # 冬季 - 凋零期颜色
    WINTER_BUD_DEEP = (105, 105, 105)   # 灰色
    WINTER_BUD_LIGHT = (128, 128, 128)  # 浅灰色
    WINTER_BLOOM = (176, 196, 222)      # 钢蓝色
    WINTER_GLOW = (240, 248, 255)       # 淡蓝白色
    WINTER_BG = (240, 248, 255)         # 冬日蓝色
    
    @staticmethod
    def interpolate_color(color1: Tuple[int, int, int], color2: Tuple[int, int, int], t: float) -> Tuple[int, int, int]:
        """在两个颜色之间插值"""
        t = max(0, min(1, t))
        r = int(color1[0] * (1 - t) + color2[0] * t)
        g = int(color1[1] * (1 - t) + color2[1] * t)
        b = int(color1[2] * (1 - t) + color2[2] * t)
        return (r, g, b)
    
    @staticmethod
    def get_season_colors(season_phase: str):
        """根据季节阶段获取颜色"""
        if season_phase == "spring":
            return {
                'bud_deep': SeasonalBloomColors.SPRING_BUD_DEEP,
                'bud_light': SeasonalBloomColors.SPRING_BUD_LIGHT,
                'bloom': SeasonalBloomColors.SPRING_BLOOM,
                'glow': SeasonalBloomColors.SPRING_GLOW,
                'bg': SeasonalBloomColors.SPRING_BG
            }
        elif season_phase == "summer":
            return {
                'bud_deep': SeasonalBloomColors.SUMMER_BUD_DEEP,
                'bud_light': SeasonalBloomColors.SUMMER_BUD_LIGHT,
                'bloom': SeasonalBloomColors.SUMMER_BLOOM,
                'glow': SeasonalBloomColors.SUMMER_GLOW,
                'bg': SeasonalBloomColors.SUMMER_BG
            }
        elif season_phase == "autumn":
            return {
                'bud_deep': SeasonalBloomColors.AUTUMN_BUD_DEEP,
                'bud_light': SeasonalBloomColors.AUTUMN_BUD_LIGHT,
                'bloom': SeasonalBloomColors.AUTUMN_BLOOM,
                'glow': SeasonalBloomColors.AUTUMN_GLOW,
                'bg': SeasonalBloomColors.AUTUMN_BG
            }
        else:  # winter
            return {
                'bud_deep': SeasonalBloomColors.WINTER_BUD_DEEP,
                'bud_light': SeasonalBloomColors.WINTER_BUD_LIGHT,
                'bloom': SeasonalBloomColors.WINTER_BLOOM,
                'glow': SeasonalBloomColors.WINTER_GLOW,
                'bg': SeasonalBloomColors.WINTER_BG
            }

class EnhancedPetal:
    """增强版花瓣类 - 包含发光效果和更多细节"""
    
    def __init__(self, layer: int, petal_index: int, total_petals_in_layer: int):
        self.layer = layer
        self.petal_index = petal_index
        self.total_petals = total_petals_in_layer
        
        # 基础位置和角度
        self.base_angle = (2 * math.pi * petal_index / total_petals_in_layer)
        self.angle_offset = random.uniform(-0.15, 0.15)
        
        # 花瓣尺寸（一开始就有初始大小）
        self.base_length = 18 + layer * 12
        self.base_width = 10 + layer * 6
        self.length = self.base_length * 0.3  # 初始就有30%大小
        self.width = self.base_width * 0.3
        
        # 动画状态（一开始就有展开状态）
        self.bloom_progress = 0.3  # 初始就有30%的展开
        self.wither_progress = 0.0
        self.rotation = 0.0
        self.bend_factor = 1.0
        self.distance = 0.0
        self.max_distance = 25 + layer * 20
        
        # 发光效果（一开始就有微弱发光）
        self.glow_intensity = 0.2
        self.glow_size = 0.0
        self.glow_pulse = random.uniform(0, 2 * math.pi)
        
        # 个性化参数（加快动画速度）
        self.bloom_delay = layer * 0.05 + random.uniform(0, 0.04)  # 减少绽放延迟
        self.wither_delay = (5 - layer) * 0.05 + random.uniform(0, 0.05)  # 减少凋零延迟
        self.rotation_speed = random.uniform(0.7, 1.3)
        self.bend_amplitude = random.uniform(0.2, 0.6)
        
        # 形状控制点
        self.control_points = []
        self.generate_enhanced_petal_shape()
        
        # 生命周期状态（一开始就在盛开）
        self.life_stage = "bloom"  # 直接从盛开开始
        self.current_colors = {}
        
        # 飘落状态
        self.is_falling = False
        self.fall_x = 0
        self.fall_y = 0
        self.fall_speed = 0
        self.fall_rotation = 0
        
    def generate_enhanced_petal_shape(self):
        """生成简化的花瓣形状（优化性能）"""
        points = []
        num_points = 8  # 减少精度（从16减到8）
        
        for i in range(num_points):
            t = i / (num_points - 1)
            
            # 简化的花瓣形状
            if t < 0.2:  # 尖端
                width_factor = t * 2
            elif t < 0.8:  # 主体
                width_factor = math.sin((t - 0.2) / 0.6 * math.pi) * 0.8
            else:  # 基部
                width_factor = (1 - t) * 2
            
            # 简化的长度因子
            length_factor = ease_out_cubic(t)
            
            points.append((length_factor, width_factor))
        
        self.control_points = points
    
    def update_lifecycle(self, stage: str, stage_progress: float, season_colors: dict):
        """更新生命周期状态"""
        self.life_stage = stage
        self.current_colors = season_colors
        
        if stage == "bud":
            self.update_bud_stage(stage_progress)
        elif stage == "bloom":
            self.update_bloom_stage(stage_progress)
        elif stage == "maintain":
            self.update_maintain_stage(stage_progress)
        elif stage == "wither":
            self.update_wither_stage(stage_progress)
        elif stage == "dead":
            self.update_dead_stage(stage_progress)
    
    def update_bud_stage(self, progress: float):
        """花苞阶段更新"""
        # 花苞很小，紧闭
        self.length = self.base_length * 0.1 * progress
        self.width = self.base_width * 0.1 * progress
        self.distance = 0
        self.glow_intensity = 0
        self.bloom_progress = 0
        self.wither_progress = 0
    
    def update_bloom_stage(self, progress: float):
        """盛开阶段更新"""
        adjusted_progress = max(0, progress - self.bloom_delay)
        self.bloom_progress = min(1.0, adjusted_progress / (1.0 - self.bloom_delay)) if self.bloom_delay < 1.0 else 0
        
        if self.bloom_progress > 0:
            # 尺寸动画
            size_progress = ease_out_elastic(self.bloom_progress)
            self.length = self.base_length * size_progress
            self.width = self.base_width * size_progress
            
            # 旋转和距离
            rotation_progress = ease_out_back(self.bloom_progress)
            self.rotation = math.pi * 0.4 * rotation_progress * self.rotation_speed
            if self.petal_index % 2 == 1:
                self.rotation *= -1
            
            distance_progress = ease_out_cubic(self.bloom_progress)
            self.distance = self.max_distance * distance_progress
            
            # 弯曲
            self.bend_factor = 1.0 - self.bend_amplitude * ease_in_out_cubic(self.bloom_progress)
            
            # 发光效果
            self.glow_intensity = self.bloom_progress * 0.8
            self.glow_size = self.base_length * 0.3 * self.bloom_progress
    
    def update_maintain_stage(self, progress: float):
        """维持阶段更新"""
        self.bloom_progress = 1.0
        self.wither_progress = 0
        
        # 完全展开状态
        self.length = self.base_length
        self.width = self.base_width
        self.distance = self.max_distance
        
        # 呼吸效果（加快频率）
        breath = math.sin(progress * 12 + self.glow_pulse) * 0.1 + 1  # 频率从6增加到12
        self.glow_intensity = 0.9 * breath
        self.glow_size = self.base_length * 0.4 * breath
        
        # 微风摆动（加快频率）
        wind_effect = math.sin(progress * 16 + self.angle_offset) * 2  # 频率从8增加到16
        self.distance = self.max_distance + wind_effect
    
    def update_wither_stage(self, progress: float):
        """凋零阶段更新"""
        adjusted_progress = max(0, progress - self.wither_delay)
        self.wither_progress = min(1.0, adjusted_progress / (1.0 - self.wither_delay)) if self.wither_delay < 1.0 else 0
        
        # 开始飘落
        if self.wither_progress > 0.3 and not self.is_falling:
            self.is_falling = True
            self.fall_speed = random.uniform(1, 3)
            self.fall_x, self.fall_y = self.get_world_position()
            self.fall_rotation = random.uniform(-0.05, 0.05)
        
        if self.is_falling:
            # 飘落动画
            self.fall_y += self.fall_speed
            self.fall_x += math.sin(self.fall_y * 0.02) * 2
            self.rotation += self.fall_rotation
        
        # 渐变效果
        fade_factor = max(0, 1 - self.wither_progress * 1.2)
        self.glow_intensity = fade_factor * 0.3
        self.length = self.base_length * (0.7 + 0.3 * fade_factor)
        self.width = self.base_width * (0.7 + 0.3 * fade_factor)
    
    def update_dead_stage(self, progress: float):
        """死亡阶段更新"""
        self.glow_intensity = 0
        self.length = 0
        self.width = 0
        if self.is_falling:
            self.fall_y += self.fall_speed * 0.5
    
    def get_world_position(self) -> Tuple[float, float]:
        """获取花瓣世界坐标"""
        if self.is_falling:
            return (self.fall_x, self.fall_y)
        
        angle = self.base_angle + self.angle_offset
        x = SCREEN_CENTER[0] + math.cos(angle) * self.distance
        y = SCREEN_CENTER[1] + math.sin(angle) * self.distance
        return (x, y)
    
    def get_petal_vertices(self) -> List[Tuple[float, float]]:
        """获取花瓣顶点"""
        if self.length <= 0 or self.width <= 0:
            return []
        
        vertices = []
        center_x, center_y = self.get_world_position()
        petal_angle = self.base_angle + self.angle_offset
        
        # 左侧轮廓
        for length_factor, width_factor in self.control_points:
            local_x = length_factor * self.length
            local_y = -width_factor * self.width * 0.5 * self.bend_factor
            
            # 应用旋转
            rotated_x = local_x * math.cos(petal_angle + self.rotation) - local_y * math.sin(petal_angle + self.rotation)
            rotated_y = local_x * math.sin(petal_angle + self.rotation) + local_y * math.cos(petal_angle + self.rotation)
            
            vertices.append((center_x + rotated_x, center_y + rotated_y))
        
        # 右侧轮廓
        for length_factor, width_factor in reversed(self.control_points[:-1]):
            local_x = length_factor * self.length
            local_y = width_factor * self.width * 0.5 * self.bend_factor
            
            # 应用旋转
            rotated_x = local_x * math.cos(petal_angle + self.rotation) - local_y * math.sin(petal_angle + self.rotation)
            rotated_y = local_x * math.sin(petal_angle + self.rotation) + local_y * math.cos(petal_angle + self.rotation)
            
            vertices.append((center_x + rotated_x, center_y + rotated_y))
        
        return vertices
    
    def get_petal_color(self) -> Tuple[int, int, int]:
        """获取花瓣颜色"""
        if self.life_stage == "bud":
            return self.current_colors['bud_deep']
        elif self.life_stage in ["bloom", "maintain"]:
            if self.layer <= 2:  # 内层
                base_color = self.current_colors['bud_deep']
                target_color = self.current_colors['bloom']
            else:  # 外层
                base_color = self.current_colors['bud_light']
                target_color = self.current_colors['glow']
            
            progress = self.bloom_progress if self.life_stage == "bloom" else 1.0
            return SeasonalBloomColors.interpolate_color(base_color, target_color, progress)
        elif self.life_stage == "wither":
            # 凋零时颜色变暗
            base_color = self.current_colors['bloom']
            dark_color = tuple(c // 2 for c in base_color)
            return SeasonalBloomColors.interpolate_color(base_color, dark_color, self.wither_progress)
        else:  # dead
            return (100, 100, 100)

class EnhancedParticle:
    """增强版粒子类 - 支持季节特效"""
    
    def __init__(self, x: float, y: float, particle_type: str = "sparkle", season_colors: dict = None, season: str = "spring"):
        self.x = x
        self.y = y
        self.start_x = x
        self.start_y = y
        self.type = particle_type
        self.season = season
        
        # 运动参数
        if particle_type == "pollen":
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(1, 4)
            self.vx = math.cos(angle) * speed
            self.vy = math.sin(angle) * speed - 1  # 向上飘
        elif particle_type == "sparkle":
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(3, 8)
            self.vx = math.cos(angle) * speed
            self.vy = math.sin(angle) * speed
        elif particle_type == "glow":
            self.vx = random.uniform(-0.5, 0.5)
            self.vy = random.uniform(-2, 0)
        elif particle_type == "falling_petal":
            self.vx = random.uniform(-1, 1)
            self.vy = random.uniform(1, 3)
        elif particle_type == "spring_blossom":
            # 春季花瓣飞舞
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(1, 3)
            self.vx = math.cos(angle) * speed
            self.vy = math.sin(angle) * speed - 0.5
        elif particle_type == "summer_firefly":
            # 夏季萤火虫
            self.vx = random.uniform(-1, 1)
            self.vy = random.uniform(-1, 1)
            self.orbit_angle = random.uniform(0, 2 * math.pi)
            self.orbit_speed = random.uniform(0.05, 0.15)
            self.orbit_radius = random.uniform(10, 30)
        elif particle_type == "autumn_leaf":
            # 秋季落叶
            self.vx = random.uniform(-2, 2)
            self.vy = random.uniform(1, 4)
            self.swing_phase = random.uniform(0, 2 * math.pi)
            self.swing_speed = random.uniform(0.1, 0.3)
        elif particle_type == "winter_snow":
            # 冬季雪花
            self.vx = random.uniform(-0.5, 0.5)
            self.vy = random.uniform(0.5, 2)
            self.drift_phase = random.uniform(0, 2 * math.pi)
        elif particle_type == "spring_rain":
            # 春雨
            self.vx = random.uniform(-0.5, 0.5)
            self.vy = random.uniform(8, 15)
        elif particle_type == "summer_light":
            # 夏日光斑
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(0.5, 2)
            self.vx = math.cos(angle) * speed
            self.vy = math.sin(angle) * speed
        elif particle_type == "autumn_wind":
            # 秋风效果
            self.vx = random.uniform(3, 8)
            self.vy = random.uniform(-1, 1)
        else:  # magic
            angle = random.uniform(0, 2 * math.pi)
            speed = random.uniform(2, 6)
            self.vx = math.cos(angle) * speed
            self.vy = math.sin(angle) * speed
        
        # 视觉参数
        if particle_type in ["spring_blossom", "autumn_leaf"]:
            self.size = random.uniform(3, 8)
        elif particle_type in ["summer_firefly", "winter_snow"]:
            self.size = random.uniform(2, 5)
        elif particle_type == "spring_rain":
            self.size = random.uniform(1, 3)
        elif particle_type == "summer_light":
            self.size = random.uniform(5, 12)
        elif particle_type == "autumn_wind":
            self.size = random.uniform(1, 2)
        else:
            self.size = random.uniform(1, 5)
            
        self.max_size = self.size
        self.life = 1.0
        self.max_life = self.life
        
        # 不同粒子类型的生命周期
        if particle_type in ["spring_rain", "autumn_wind"]:
            self.life_decay = random.uniform(0.02, 0.05)  # 快速消失
        elif particle_type in ["summer_firefly", "winter_snow"]:
            self.life_decay = random.uniform(0.003, 0.008)  # 慢速消失
        elif particle_type in ["spring_blossom", "autumn_leaf"]:
            self.life_decay = random.uniform(0.005, 0.015)  # 中等速度
        else:
            self.life_decay = random.uniform(0.005, 0.02)
        
        # 季节性颜色
        if season_colors:
            if particle_type == "pollen":
                self.color = season_colors['glow']
            elif particle_type == "sparkle":
                self.color = (255, 255, 255)
            elif particle_type == "glow":
                self.color = season_colors['bloom']
            elif particle_type == "falling_petal":
                self.color = season_colors['bud_light']
            elif particle_type == "spring_blossom":
                self.color = (255, 182, 193)  # 樱花粉
            elif particle_type == "summer_firefly":
                self.color = (255, 255, 140) if random.random() > 0.5 else (144, 238, 144)  # 黄绿光
            elif particle_type == "autumn_leaf":
                colors = [(255, 140, 0), (255, 69, 0), (218, 165, 32), (139, 69, 19)]
                self.color = random.choice(colors)
            elif particle_type == "winter_snow":
                self.color = (240, 248, 255)  # 雪白色
            elif particle_type == "spring_rain":
                self.color = (173, 216, 230)  # 浅蓝色
            elif particle_type == "summer_light":
                self.color = (255, 255, 224)  # 浅黄色
            elif particle_type == "autumn_wind":
                self.color = (210, 180, 140)  # 棕褐色
            else:  # magic
                self.color = season_colors['glow']
        else:
            self.color = (255, 255, 255)
        
        # 特效参数
        self.rotation = 0
        self.rotation_speed = random.uniform(-0.1, 0.1)
        self.shimmer_phase = random.uniform(0, 2 * math.pi)
        self.pulse_speed = random.uniform(0.1, 0.3)
        
        # 季节特效专用参数
        if particle_type == "summer_firefly":
            self.blink_phase = random.uniform(0, 2 * math.pi)
            self.blink_speed = random.uniform(0.2, 0.5)
        elif particle_type in ["autumn_leaf", "spring_blossom"]:
            self.flutter_phase = random.uniform(0, 2 * math.pi)
            self.flutter_speed = random.uniform(0.1, 0.4)
    
    def update(self):
        """更新粒子状态"""
        # 位置更新
        self.x += self.vx
        self.y += self.vy
        
        # 物理效果和季节特效
        if self.type == "pollen":
            self.vy += 0.02  # 轻微重力
            self.vx += (random.random() - 0.5) * 0.1  # 随机飘动
        elif self.type == "sparkle":
            self.vy += 0.1  # 重力
            self.vx *= 0.99  # 阻力
            self.vy *= 0.99
        elif self.type == "falling_petal":
            self.vy += 0.1  # 重力
            self.vx += math.sin(self.y * 0.01) * 0.1  # 飘摆
        elif self.type == "glow":
            self.vy += 0.05  # 轻微重力
        elif self.type == "magic":
            # 魔法粒子螺旋运动
            self.rotation += self.rotation_speed
        elif self.type == "spring_blossom":
            # 春季花瓣飞舞 - 轻盈飘舞
            self.flutter_phase += self.flutter_speed
            self.vy += 0.03  # 轻微重力
            self.vx += math.sin(self.flutter_phase) * 0.2  # 飘舞效果
            self.vy += math.cos(self.flutter_phase * 0.7) * 0.1
        elif self.type == "summer_firefly":
            # 夏季萤火虫 - 绕圈飞行
            self.orbit_angle += self.orbit_speed
            center_x = self.start_x + math.cos(self.orbit_angle) * self.orbit_radius
            center_y = self.start_y + math.sin(self.orbit_angle) * self.orbit_radius * 0.5
            self.x += (center_x - self.x) * 0.1
            self.y += (center_y - self.y) * 0.1
            self.blink_phase += self.blink_speed
        elif self.type == "autumn_leaf":
            # 秋季落叶 - 飘摆下落
            self.vy += 0.08  # 重力
            self.swing_phase += self.swing_speed
            self.vx += math.sin(self.swing_phase) * 0.3  # 左右摆动
            if hasattr(self, 'flutter_phase'):
                self.flutter_phase += self.flutter_speed
                self.rotation += math.sin(self.flutter_phase) * 0.1  # 旋转飘落
        elif self.type == "winter_snow":
            # 冬季雪花 - 缓慢飘落
            self.vy += 0.02  # 轻微重力
            self.drift_phase += 0.05
            self.vx += math.sin(self.drift_phase) * 0.05  # 轻微漂移
            self.rotation += 0.02  # 缓慢旋转
        elif self.type == "spring_rain":
            # 春雨 - 快速下落
            self.vy += 0.2  # 较强重力
            self.vx *= 0.98  # 轻微阻力
        elif self.type == "summer_light":
            # 夏日光斑 - 温和飘动
            self.vx *= 0.95
            self.vy *= 0.95
            self.shimmer_phase += self.pulse_speed
        elif self.type == "autumn_wind":
            # 秋风 - 横向流动
            self.vx *= 0.98
            self.vy += random.uniform(-0.1, 0.1)  # 轻微上下波动
            spiral_x = math.cos(self.rotation) * 2
            spiral_y = math.sin(self.rotation) * 2
            self.x += spiral_x
            self.y += spiral_y
        
        # 生命周期
        self.life -= self.life_decay
        
        # 视觉效果更新
        life_factor = max(0, self.life / self.max_life)
        self.size = self.max_size * life_factor
        
        # 闪烁效果
        self.shimmer_phase += self.pulse_speed
        
        # 旋转
        self.rotation += self.rotation_speed
    
    def is_alive(self) -> bool:
        """检查粒子是否还活着"""
        return self.life > 0 and self.size > 0.1 and self.y < SCREEN_HEIGHT + 100
    
    def draw(self, screen: pygame.Surface):
        """绘制粒子（增强季节特效版本）"""
        if not self.is_alive():
            return
        
        alpha = int(255 * self.life / self.max_life)
        current_size = max(1, int(self.size))
        
        if current_size <= 0:
            return
            
        # 根据粒子类型绘制不同效果
        if self.type == "falling_petal":
            # 简化的花瓣形状
            pygame.draw.circle(screen, (*self.color, alpha), 
                             (int(self.x), int(self.y)), current_size)
        elif self.type == "spring_blossom":
            # 春季花瓣 - 多层花瓣效果
            self._draw_blossom_petal(screen, alpha, current_size)
        elif self.type == "summer_firefly":
            # 夏季萤火虫 - 闪烁发光效果
            self._draw_firefly(screen, alpha, current_size)
        elif self.type == "autumn_leaf":
            # 秋季落叶 - 叶子形状
            self._draw_leaf(screen, alpha, current_size)
        elif self.type == "winter_snow":
            # 冬季雪花 - 雪花形状
            self._draw_snowflake(screen, alpha, current_size)
        elif self.type == "spring_rain":
            # 春雨 - 雨滴形状
            self._draw_raindrop(screen, alpha, current_size)
        elif self.type == "summer_light":
            # 夏日光斑 - 发光圆形
            self._draw_light_orb(screen, alpha, current_size)
        elif self.type == "autumn_wind":
            # 秋风 - 细线条效果
            self._draw_wind_streak(screen, alpha, current_size)
        else:
            # 默认圆形粒子
            temp_surface = pygame.Surface((current_size * 4, current_size * 4), pygame.SRCALPHA)
            pygame.draw.circle(temp_surface, (*self.color, alpha),
                             (current_size * 2, current_size * 2), current_size)
            screen.blit(temp_surface, (self.x - current_size * 2, self.y - current_size * 2))
    
    def _draw_blossom_petal(self, screen: pygame.Surface, alpha: int, size: int):
        """绘制春季花瓣"""
        # 简化的花瓣形状 - 椭圆形
        petal_rect = pygame.Rect(0, 0, size * 2, size * 3)
        petal_rect.center = (int(self.x), int(self.y))
        pygame.draw.ellipse(screen, (*self.color, alpha), petal_rect)
        
    def _draw_firefly(self, screen: pygame.Surface, alpha: int, size: int):
        """绘制夏季萤火虫"""
        # 闪烁效果
        blink_alpha = int(alpha * (0.5 + 0.5 * math.sin(self.blink_phase)))
        glow_size = int(size * 1.5)
        
        # 外发光
        if glow_size > 0:
            temp_surface = pygame.Surface((glow_size * 4, glow_size * 4), pygame.SRCALPHA)
            pygame.draw.circle(temp_surface, (*self.color, blink_alpha // 3),
                             (glow_size * 2, glow_size * 2), glow_size)
            screen.blit(temp_surface, (self.x - glow_size * 2, self.y - glow_size * 2))
        
        # 内核
        pygame.draw.circle(screen, (*self.color, blink_alpha), 
                         (int(self.x), int(self.y)), size)
    
    def _draw_leaf(self, screen: pygame.Surface, alpha: int, size: int):
        """绘制秋季落叶"""
        # 简化的叶子形状 - 旋转的椭圆
        leaf_surface = pygame.Surface((size * 4, size * 6), pygame.SRCALPHA)
        pygame.draw.ellipse(leaf_surface, (*self.color, alpha), 
                          (0, 0, size * 4, size * 6))
        
        # 旋转叶子
        rotated_leaf = pygame.transform.rotate(leaf_surface, math.degrees(self.rotation))
        screen.blit(rotated_leaf, (self.x - rotated_leaf.get_width() // 2, 
                                 self.y - rotated_leaf.get_height() // 2))
    
    def _draw_snowflake(self, screen: pygame.Surface, alpha: int, size: int):
        """绘制冬季雪花"""
        # 简化的雪花 - 十字形
        x, y = int(self.x), int(self.y)
        color_with_alpha = (*self.color, alpha)
        
        # 水平线
        pygame.draw.line(screen, color_with_alpha, (x - size, y), (x + size, y), 2)
        # 垂直线
        pygame.draw.line(screen, color_with_alpha, (x, y - size), (x, y + size), 2)
        # 斜线
        pygame.draw.line(screen, color_with_alpha, 
                        (x - size//2, y - size//2), (x + size//2, y + size//2), 1)
        pygame.draw.line(screen, color_with_alpha, 
                        (x - size//2, y + size//2), (x + size//2, y - size//2), 1)
    
    def _draw_raindrop(self, screen: pygame.Surface, alpha: int, size: int):
        """绘制春雨雨滴"""
        # 简化的雨滴 - 细长椭圆
        rain_rect = pygame.Rect(0, 0, size, size * 4)
        rain_rect.center = (int(self.x), int(self.y))
        pygame.draw.ellipse(screen, (*self.color, alpha), rain_rect)
    
    def _draw_light_orb(self, screen: pygame.Surface, alpha: int, size: int):
        """绘制夏日光斑"""
        # 发光球体效果
        shimmer_alpha = int(alpha * (0.7 + 0.3 * math.sin(self.shimmer_phase)))
        
        # 外发光
        for i in range(3):
            glow_size = size + i * 2
            glow_alpha = shimmer_alpha // (i + 2)
            if glow_alpha > 0:
                pygame.draw.circle(screen, (*self.color, glow_alpha), 
                                 (int(self.x), int(self.y)), glow_size)
    
    def _draw_wind_streak(self, screen: pygame.Surface, alpha: int, size: int):
        """绘制秋风条纹"""
        # 简化的风条纹 - 短线条
        start_x = int(self.x - size * 2)
        end_x = int(self.x + size * 2)
        y = int(self.y)
        pygame.draw.line(screen, (*self.color, alpha), (start_x, y), (end_x, y), 2)

class SeasonalRose:
    """季节性月季花类"""
    
    def __init__(self):
        self.petals: List[EnhancedPetal] = []
        self.particles: List[EnhancedParticle] = []
        self.create_abundant_petals()
        
        # 季节循环控制（直接从盛开开始）
        self.current_season = "spring"
        self.life_stage = "bloom"  # 直接从盛开开始，跳过花苞期
        self.stage_progress = 0.0
        self.total_progress = 0.0  # 整个循环进度 (0-1)
        
        # 时间控制（进一步加快循环）
        self.bud_duration = 0        # 跳过花苞期
        self.bloom_duration = 120    # 2秒
        self.maintain_duration = 180 # 3秒
        self.wither_duration = 120   # 2秒
        self.dead_duration = 60      # 1秒
        self.reset_duration = 20     # 0.33秒
        
        self.total_cycle_duration = (self.bud_duration + self.bloom_duration + 
                                   self.maintain_duration + self.wither_duration + 
                                   self.dead_duration + self.reset_duration)
        
        self.frame_count = 0
        
        # 花心效果（一开始就有花心）
        self.center_size = 10  # 初始花心大小
        self.center_glow = 0.5  # 初始发光
        self.center_pulse = 0
        
        # 全局发光效果
        self.global_glow_intensity = 0
        self.magic_burst_timer = 0
        
        # 背景花苞（一开始就隐藏）
        self.bud_size = 30
        self.bud_opacity = 0  # 直接隐藏花苞
        
    def create_abundant_petals(self):
        """创建适量花瓣（优化性能）"""
        # 减少花瓣层数和密度
        layer_configs = [
            {"layer": 0, "count": 8},   # 内层 - 8片
            {"layer": 1, "count": 12},  # 第二层 - 12片
            {"layer": 2, "count": 16},  # 第三层 - 16片
            {"layer": 3, "count": 20},  # 第四层 - 20片
            {"layer": 4, "count": 16},  # 第五层 - 16片
            {"layer": 5, "count": 12},  # 外层 - 12片
        ]
        
        for config in layer_configs:
            layer = config["layer"]
            count = config["count"]
            
            for i in range(count):
                petal = EnhancedPetal(layer, i, count)
                self.petals.append(petal)
        
        print(f"创建了 {len(self.petals)} 个花瓣")
    
    def get_current_season_colors(self):
        """获取当前季节颜色"""
        return SeasonalBloomColors.get_season_colors(self.current_season)
    
    def update_season_cycle(self):
        """更新季节循环（直接从春季盛开开始）"""
        # 根据生命周期阶段决定季节，并对应真实数据
        if self.life_stage == "bloom":
            self.current_season = "spring"  # 对应春季25天开花期
        elif self.life_stage == "maintain":
            self.current_season = "summer"  # 对应夏季40天盛花期
        elif self.life_stage == "wither":
            self.current_season = "autumn"  # 对应秋季30天二次开花期
        else:  # dead, reset
            self.current_season = "winter"  # 对应冬季休眠期
    
    def update(self):
        """更新动画状态"""
        self.frame_count += 1
        
        # 计算循环进度
        cycle_position = self.frame_count % self.total_cycle_duration
        self.total_progress = cycle_position / self.total_cycle_duration
        
        # 确定当前阶段（跳过花苞期，直接从盛开开始）
        if cycle_position < self.bloom_duration:
            self.life_stage = "bloom"
            self.stage_progress = cycle_position / self.bloom_duration
            
        elif cycle_position < self.bloom_duration + self.maintain_duration:
            self.life_stage = "maintain"
            maintain_start = self.bloom_duration
            self.stage_progress = (cycle_position - maintain_start) / self.maintain_duration
            
        elif cycle_position < (self.bloom_duration + self.maintain_duration + self.wither_duration):
            self.life_stage = "wither"
            wither_start = self.bloom_duration + self.maintain_duration
            self.stage_progress = (cycle_position - wither_start) / self.wither_duration
            
        elif cycle_position < (self.bloom_duration + self.maintain_duration + 
                             self.wither_duration + self.dead_duration):
            self.life_stage = "dead"
            dead_start = (self.bloom_duration + self.maintain_duration + self.wither_duration)
            self.stage_progress = (cycle_position - dead_start) / self.dead_duration
            
        else:
            self.life_stage = "reset"
            reset_start = (self.bloom_duration + self.maintain_duration + 
                          self.wither_duration + self.dead_duration)
            self.stage_progress = (cycle_position - reset_start) / self.reset_duration
            
            # 重置飘落状态
            if self.stage_progress > 0.5:
                for petal in self.petals:
                    petal.is_falling = False
                    petal.fall_x = 0
                    petal.fall_y = 0
        
        # 更新季节
        self.update_season_cycle()
        season_colors = self.get_current_season_colors()
        
        # 更新花苞状态（跳过花苞期）
        self.bud_opacity = 0  # 始终隐藏花苞
        
        # 更新花心
        self.update_center()
        
        # 更新全局发光（加快变化）
        if self.life_stage == "maintain":
            self.global_glow_intensity = 0.8 + 0.2 * math.sin(self.frame_count * 0.2)  # 频率从0.1增加到0.2
        elif self.life_stage == "bloom":
            self.global_glow_intensity = self.stage_progress * 0.6
        else:
            self.global_glow_intensity = max(0, self.global_glow_intensity - 0.02)
        
        # 更新所有花瓣
        for petal in self.petals:
            petal.update_lifecycle(self.life_stage, self.stage_progress, season_colors)
        
        # 更新粒子
        self.particles = [p for p in self.particles if p.is_alive()]
        for particle in self.particles:
            particle.update()
        
        # 生成新粒子
        self.generate_particles(season_colors)
        
        # 魔法爆发效果（减少频率）
        if self.life_stage == "bloom" and self.stage_progress > 0.8:
            self.magic_burst_timer += 1
            if self.magic_burst_timer % 30 == 0:  # 减少频率（从10帧增加到30帧）
                self.create_magic_burst(season_colors)
    
    def update_center(self):
        """更新花心"""
        if self.life_stage == "bloom":
            target_size = 20 * self.stage_progress
            target_glow = self.stage_progress
        elif self.life_stage == "maintain":
            target_size = 20
            target_glow = 1.0
            self.center_pulse += 0.2  # 加快脉动速度（原来是0.1）
        elif self.life_stage == "wither":
            fade_factor = 1 - self.stage_progress
            target_size = 20 * fade_factor
            target_glow = fade_factor
        else:
            target_size = 0
            target_glow = 0
        
        # 平滑过渡
        self.center_size += (target_size - self.center_size) * 0.1
        self.center_glow += (target_glow - self.center_glow) * 0.1
    
    def generate_particles(self, season_colors: dict):
        """生成增强的季节粒子效果"""
        if len(self.particles) > 120:  # 适度增加粒子数量限制（从80到120）
            return
        
        # 基础花朵粒子效果
        if self.life_stage == "bloom" and random.random() < 0.18:  # 轻微增加生成频率
            # 盛开期 - 花粉和闪光
            particle_type = random.choice(["sparkle", "spring_blossom"])
            particle = EnhancedParticle(
                SCREEN_CENTER[0] + random.uniform(-30, 30),
                SCREEN_CENTER[1] + random.uniform(-30, 30),
                particle_type, season_colors, self.current_season
            )
            self.particles.append(particle)
        
        elif self.life_stage == "maintain" and random.random() < 0.15:  # 轻微增加生成频率
            # 维持期 - 发光粒子和萤火虫
            if self.current_season == "summer":
                particle_type = random.choice(["glow", "summer_firefly", "summer_light"])
            else:
                particle_type = "glow"
            particle = EnhancedParticle(
                SCREEN_CENTER[0] + random.uniform(-40, 40),
                SCREEN_CENTER[1] + random.uniform(-40, 40),
                particle_type, season_colors, self.current_season
            )
            self.particles.append(particle)
        
        elif self.life_stage == "wither" and random.random() < 0.10:  # 轻微增加生成频率
            # 凋零期 - 飘落花瓣和秋叶
            if self.current_season == "autumn":
                particle_type = random.choice(["falling_petal", "autumn_leaf"])
            else:
                particle_type = "falling_petal"
            particle = EnhancedParticle(
                SCREEN_CENTER[0] + random.uniform(-80, 80),
                SCREEN_CENTER[1] + random.uniform(-60, 60),
                particle_type, season_colors, self.current_season
            )
            self.particles.append(particle)
        
        # 季节性天气效果
        self._generate_weather_particles(season_colors)
    
    def _generate_weather_particles(self, season_colors: dict):
        """生成季节天气粒子"""
        # 春季 - 春雨（偶尔）
        if (self.current_season == "spring" and 
            random.random() < 0.03 and  # 轻微增加频率
            len([p for p in self.particles if p.type == "spring_rain"]) < 15):  # 增加数量限制
            
            for _ in range(random.randint(1, 4)):  # 增加生成数量
                particle = EnhancedParticle(
                    random.uniform(0, SCREEN_WIDTH),
                    -10,  # 从屏幕顶部开始
                    "spring_rain", season_colors, "spring"
                )
                self.particles.append(particle)
        
        # 夏季 - 光斑效果（环境光）
        elif (self.current_season == "summer" and 
              random.random() < 0.06 and  # 轻微增加频率
              len([p for p in self.particles if p.type == "summer_light"]) < 12):  # 增加数量限制
            
            particle = EnhancedParticle(
                random.uniform(100, SCREEN_WIDTH - 100),
                random.uniform(100, SCREEN_HEIGHT - 100),
                "summer_light", season_colors, "summer"
            )
            self.particles.append(particle)
        
        # 秋季 - 风的效果
        elif (self.current_season == "autumn" and 
              random.random() < 0.04 and  # 轻微增加频率
              len([p for p in self.particles if p.type == "autumn_wind"]) < 8):  # 增加数量限制
            
            for _ in range(random.randint(1, 3)):  # 增加生成数量
                particle = EnhancedParticle(
                    -10,  # 从左侧开始
                    random.uniform(SCREEN_HEIGHT // 3, 2 * SCREEN_HEIGHT // 3),
                    "autumn_wind", season_colors, "autumn"
                )
                self.particles.append(particle)
        
        # 冬季 - 雪花
        elif (self.current_season == "winter" and 
              random.random() < 0.05 and  # 轻微增加频率
              len([p for p in self.particles if p.type == "winter_snow"]) < 20):  # 增加数量限制
            
            for _ in range(random.randint(1, 4)):  # 增加生成数量
                particle = EnhancedParticle(
                    random.uniform(0, SCREEN_WIDTH),
                    -10,  # 从屏幕顶部开始
                    "winter_snow", season_colors, "winter"
                )
                self.particles.append(particle)
    
    def create_magic_burst(self, season_colors: dict):
        """创建季节性魔法爆发效果"""
        # 根据季节创建不同的爆发效果
        if self.current_season == "spring":
            # 春季 - 花瓣爆发
            for _ in range(7):  # 增加数量
                particle = EnhancedParticle(
                    SCREEN_CENTER[0], SCREEN_CENTER[1],
                    "spring_blossom", season_colors, "spring"
                )
                self.particles.append(particle)
        elif self.current_season == "summer":
            # 夏季 - 萤火虫和光芒
            for _ in range(6):  # 增加数量
                particle_type = random.choice(["summer_firefly", "magic"])
                particle = EnhancedParticle(
                    SCREEN_CENTER[0], SCREEN_CENTER[1],
                    particle_type, season_colors, "summer"
                )
                self.particles.append(particle)
        elif self.current_season == "autumn":
            # 秋季 - 落叶飞舞
            for _ in range(8):  # 增加数量
                particle = EnhancedParticle(
                    SCREEN_CENTER[0], SCREEN_CENTER[1],
                    "autumn_leaf", season_colors, "autumn"
                )
                self.particles.append(particle)
        else:  # winter
            # 冬季 - 雪花飞舞
            for _ in range(10):  # 增加数量
                particle = EnhancedParticle(
                    SCREEN_CENTER[0], SCREEN_CENTER[1],
                    "winter_snow", season_colors, "winter"
                )
                self.particles.append(particle)
    
    def draw_enhanced_bud(self, screen: pygame.Surface):
        """绘制增强花苞"""
        if self.bud_opacity > 0:
            season_colors = self.get_current_season_colors()
            
            # 花苞主体
            bud_rect = pygame.Rect(0, 0, self.bud_size * 2, self.bud_size * 3)
            bud_rect.center = SCREEN_CENTER
            
            temp_surface = pygame.Surface((self.bud_size * 6, self.bud_size * 8), pygame.SRCALPHA)
            
            # 发光效果
            if self.life_stage == "bud" and self.stage_progress > 0.5:
                glow_size = int(self.bud_size * 3)
                glow_alpha = int(self.bud_opacity * 0.3)
                glow_color = (*season_colors['glow'], glow_alpha)
                
                pygame.draw.ellipse(temp_surface, glow_color,
                                  (self.bud_size, self.bud_size * 2, glow_size, glow_size))
            
            # 多层花苞
            for i in range(6):
                layer_color = SeasonalBloomColors.interpolate_color(
                    season_colors['bud_deep'],
                    season_colors['bud_light'],
                    i / 5
                )
                layer_alpha = int(self.bud_opacity * (0.9 - i * 0.1))
                color_with_alpha = (*layer_color, layer_alpha)
                
                offset = i * 3
                layer_rect = pygame.Rect(
                    offset + self.bud_size,
                    offset + self.bud_size * 2,
                    self.bud_size * 2 - offset,
                    self.bud_size * 3 - offset
                )
                
                pygame.draw.ellipse(temp_surface, color_with_alpha, layer_rect)
            
            screen.blit(temp_surface, (SCREEN_CENTER[0] - self.bud_size * 3,
                                     SCREEN_CENTER[1] - self.bud_size * 4))
    
    def draw_enhanced_center(self, screen: pygame.Surface):
        """绘制简化的花心"""
        if self.center_size > 1:
            season_colors = self.get_current_season_colors()
            
            # 简化的脉动效果
            current_size = int(self.center_size)
            
            # 简化的花心主体（只有2层）
            for i in range(2):
                size = current_size - i * 3
                if size > 0:
                    alpha = 255 - i * 50
                    color = season_colors['glow'] if i == 0 else season_colors['bloom']
                    pygame.draw.circle(screen, color, SCREEN_CENTER, size)
            
            # 简化的花蕊（减少数量）
            if current_size > 8:
                for j in range(6):  # 减少到6个
                    angle = j * math.pi / 3
                    radius = current_size * 0.5
                    stamen_x = SCREEN_CENTER[0] + math.cos(angle) * radius
                    stamen_y = SCREEN_CENTER[1] + math.sin(angle) * radius
                    
                    pygame.draw.circle(screen, season_colors['bud_deep'],
                                     (int(stamen_x), int(stamen_y)), 2)
    
    def draw_glow_effects(self, screen: pygame.Surface):
        """绘制简化的全局发光效果"""
        if self.global_glow_intensity > 0.3:  # 只在强发光时显示
            season_colors = self.get_current_season_colors()
            
            # 简化的光晕（只有3层）
            glow_radius = int(150 * self.global_glow_intensity)
            glow_alpha = int(30 * self.global_glow_intensity)
            
            temp_glow = pygame.Surface((glow_radius * 2, glow_radius * 2), pygame.SRCALPHA)
            
            for i in range(3):  # 减少层数
                layer_radius = glow_radius - i * glow_radius // 3
                layer_alpha = glow_alpha // (i + 1)
                glow_color = (*season_colors['glow'], layer_alpha)
                
                pygame.draw.circle(temp_glow, glow_color,
                                 (glow_radius, glow_radius), max(1, layer_radius))
            
            screen.blit(temp_glow, (SCREEN_CENTER[0] - glow_radius,
                                  SCREEN_CENTER[1] - glow_radius))
    
    def draw(self, screen: pygame.Surface):
        """绘制季节性月季花"""
        season_colors = self.get_current_season_colors()
        
        # 增强的季节背景
        self.draw_seasonal_background(screen, season_colors)
        
        # 全局发光效果
        self.draw_glow_effects(screen)
        
        # 花苞
        self.draw_enhanced_bud(screen)
        
        # 花瓣（按层次排序）
        sorted_petals = sorted(self.petals, key=lambda p: (-p.layer, p.get_world_position()[1]))
    
    def draw_seasonal_background(self, screen: pygame.Surface, season_colors: dict):
        """绘制增强的季节背景"""
        base_color = season_colors['bg']
        
        # 创建渐变背景
        if self.current_season == "spring":
            # 春季 - 清新的天空渐变
            self._draw_gradient_background(screen, 
                                         (135, 206, 235),  # 天空蓝
                                         (240, 255, 240))  # 淡绿
        elif self.current_season == "summer":
            # 夏季 - 温暖的金色渐变
            self._draw_gradient_background(screen,
                                         (255, 215, 0),    # 金色
                                         (255, 250, 240))  # 米色
        elif self.current_season == "autumn":
            # 秋季 - 夕阳渐变
            self._draw_gradient_background(screen,
                                         (255, 140, 0),    # 橙色
                                         (255, 248, 220))  # 秋日米色
        else:  # winter
            # 冬季 - 冷色调渐变
            self._draw_gradient_background(screen,
                                         (176, 196, 222),  # 钢蓝色
                                         (240, 248, 255))  # 淡蓝白
        
        # 添加环境光照效果
        self._draw_ambient_lighting(screen, season_colors)
    
    def _draw_gradient_background(self, screen: pygame.Surface, top_color: tuple, bottom_color: tuple):
        """绘制渐变背景"""
        for y in range(SCREEN_HEIGHT):
            # 计算渐变比例
            ratio = y / SCREEN_HEIGHT
            
            # 插值计算颜色
            r = int(top_color[0] * (1 - ratio) + bottom_color[0] * ratio)
            g = int(top_color[1] * (1 - ratio) + bottom_color[1] * ratio)
            b = int(top_color[2] * (1 - ratio) + bottom_color[2] * ratio)
            
            # 绘制水平线
            pygame.draw.line(screen, (r, g, b), (0, y), (SCREEN_WIDTH, y))
    
    def _draw_ambient_lighting(self, screen: pygame.Surface, season_colors: dict):
        """绘制环境光照效果"""
        # 根据生命阶段和季节调整环境光
        light_intensity = 0.0
        
        if self.life_stage == "bloom":
            light_intensity = self.stage_progress * 0.3
        elif self.life_stage == "maintain":
            light_intensity = 0.3 + 0.2 * math.sin(self.frame_count * 0.05)  # 脉动光照
        elif self.life_stage == "wither":
            light_intensity = 0.3 * (1 - self.stage_progress)
        
        if light_intensity > 0:
            # 创建光照效果
            light_surface = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
            
            # 季节性光照颜色
            if self.current_season == "spring":
                light_color = (255, 255, 255, int(light_intensity * 50))  # 白光
            elif self.current_season == "summer":
                light_color = (255, 255, 200, int(light_intensity * 60))  # 暖黄光
            elif self.current_season == "autumn":
                light_color = (255, 200, 150, int(light_intensity * 40))  # 橙光
            else:  # winter
                light_color = (200, 220, 255, int(light_intensity * 30))  # 冷蓝光
            
            # 中心光源效果
            for radius in range(50, 300, 20):
                alpha = int(light_color[3] * (300 - radius) / 300)
                if alpha > 0:
                    temp_color = (*light_color[:3], alpha)
                    pygame.draw.circle(light_surface, temp_color, SCREEN_CENTER, radius)
            
            screen.blit(light_surface, (0, 0))
        
        # 花瓣（按层次排序）
        sorted_petals = sorted(self.petals, key=lambda p: (-p.layer, p.get_world_position()[1]))
        for petal in sorted_petals:
            vertices = petal.get_petal_vertices()
            if len(vertices) >= 3:
                # 花瓣主体（移除阴影以提高性能）
                petal_color = petal.get_petal_color()
                pygame.draw.polygon(screen, petal_color, vertices)
                
                # 简化的花瓣高光（只在维持期显示）
                if petal.life_stage == "maintain" and len(vertices) > 2:
                    highlight_color = SeasonalBloomColors.interpolate_color(
                        petal_color, (255, 255, 255), 0.3
                    )
                    pygame.draw.polygon(screen, highlight_color, vertices, 1)
        
        # 花心
        self.draw_enhanced_center(screen)
        
        # 优化的粒子效果渲染
        self.draw_particles_optimized(screen)
    
    def draw_particles_optimized(self, screen: pygame.Surface):
        """优化的粒子渲染系统 - 分层和批量处理"""
        if not self.particles:
            return
        
        # 按渲染层次分组粒子
        background_particles = []  # 背景天气效果
        mid_particles = []         # 中层花朵效果
        foreground_particles = []  # 前景特效
        
        for particle in self.particles:
            if particle.type in ["spring_rain", "autumn_wind", "winter_snow"]:
                background_particles.append(particle)
            elif particle.type in ["summer_light", "summer_firefly", "magic"]:
                foreground_particles.append(particle)
            else:
                mid_particles.append(particle)
        
        # 分层渲染
        self._render_particle_layer(screen, background_particles, "background")
        self._render_particle_layer(screen, mid_particles, "mid")
        self._render_particle_layer(screen, foreground_particles, "foreground")
    
    def _render_particle_layer(self, screen: pygame.Surface, particles: list, layer_type: str):
        """渲染单个粒子层"""
        if not particles:
            return
            
        # 根据层类型优化渲染
        if layer_type == "background":
            # 背景粒子可以使用更简单的渲染
            for particle in particles:
                if particle.is_alive():
                    alpha = int(255 * particle.life / particle.max_life * 0.6)  # 背景透明度降低
                    size = max(1, int(particle.size * 0.8))  # 背景粒子稍小
                    pygame.draw.circle(screen, (*particle.color, alpha), 
                                     (int(particle.x), int(particle.y)), size)
        elif layer_type == "foreground":
            # 前景粒子使用完整效果
            for particle in particles:
                particle.draw(screen)
        else:
            # 中层粒子使用标准渲染
            for particle in particles:
                particle.draw(screen)

class EnhancedRoseAnimation:
    """增强版月季花动画主控制类"""
    
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("增强季节循环月季花动画")
        self.clock = pygame.time.Clock()
        
        self.rose = SeasonalRose()
        self.running = True
        
        # 字体
        try:
            self.font = pygame.font.Font(None, 32)
            self.title_font = pygame.font.Font(None, 48)
        except:
            self.font = pygame.font.SysFont('arial', 24)
            self.title_font = pygame.font.SysFont('arial', 36)
    
    def draw_ui(self):
        """绘制用户界面"""
        # 标题
        title_text = "增强季节循环月季花动画"
        title_surface = self.title_font.render(title_text, True, (80, 80, 80))
        title_rect = title_surface.get_rect(center=(SCREEN_WIDTH // 2, 50))
        
        # 半透明背景
        bg_rect = pygame.Rect(title_rect.x - 25, title_rect.y - 15,
                             title_rect.width + 50, title_rect.height + 30)
        temp_bg = pygame.Surface((bg_rect.width, bg_rect.height), pygame.SRCALPHA)
        pygame.draw.rect(temp_bg, (255, 255, 255, 220), temp_bg.get_rect())
        pygame.draw.rect(temp_bg, (120, 120, 120), temp_bg.get_rect(), 3)
        self.screen.blit(temp_bg, bg_rect.topleft)
        
        self.screen.blit(title_surface, title_rect)
        
        # 状态信息
        stage_names = {
            "bud": "花苞期",
            "bloom": "盛开期", 
            "maintain": "维持期",
            "wither": "凋零期",
            "dead": "完全凋零",
            "reset": "重置期"
        }
        
        season_names = {
            "spring": "春季",
            "summer": "夏季",
            "autumn": "秋季", 
            "winter": "冬季"
        }
        
        stage_text = f"阶段: {stage_names.get(self.rose.life_stage, self.rose.life_stage)}"
        season_text = f"季节: {season_names.get(self.rose.current_season, self.rose.current_season)}"
        progress_text = f"阶段进度: {int(self.rose.stage_progress * 100)}%"
        cycle_text = f"循环进度: {int(self.rose.total_progress * 100)}%"
        petal_text = f"花瓣数量: {len(self.rose.petals)}"
        particle_text = f"粒子数量: {len(self.rose.particles)}"
        
        # 信息面板
        info_y = SCREEN_HEIGHT - 200
        info_bg = pygame.Rect(15, info_y, 380, 180)
        temp_info = pygame.Surface((info_bg.width, info_bg.height), pygame.SRCALPHA)
        pygame.draw.rect(temp_info, (0, 0, 0, 150), temp_info.get_rect())
        pygame.draw.rect(temp_info, (255, 255, 255), temp_info.get_rect(), 2)
        self.screen.blit(temp_info, info_bg.topleft)
        
        texts = [stage_text, season_text, progress_text, cycle_text, petal_text, particle_text]
        for i, text in enumerate(texts):
            text_surface = self.font.render(text, True, (255, 255, 255))
            self.screen.blit(text_surface, (25, info_y + 15 + i * 25))
        
        # 循环进度条
        self.draw_cycle_progress()
        
        # 控制说明
        control_text = "空格键: 加速 | ESC: 退出"
        control_surface = self.font.render(control_text, True, (120, 120, 120))
        self.screen.blit(control_surface, (25, SCREEN_HEIGHT - 25))
        
        # 显示真实数据
        if SHOW_REAL_DATA:
            self.draw_real_data_panel()
    
    def draw_real_data_panel(self):
        """显示真实月季花数据"""
        # 获取当前季节的真实数据
        current_season_data = REAL_ROSE_DATA.get(self.rose.current_season, {})
        
        # 数据面板位置和大小
        panel_x = SCREEN_WIDTH - 420
        panel_y = 120
        panel_width = 400
        panel_height = 300
        
        # 绘制数据面板背景
        panel_bg = pygame.Rect(panel_x, panel_y, panel_width, panel_height)
        temp_panel = pygame.Surface((panel_width, panel_height), pygame.SRCALPHA)
        pygame.draw.rect(temp_panel, (20, 50, 80, 200), temp_panel.get_rect())
        pygame.draw.rect(temp_panel, (100, 150, 255), temp_panel.get_rect(), 3)
        self.screen.blit(temp_panel, panel_bg.topleft)
        
        # 面板标题
        try:
            data_font = pygame.font.Font(None, 24)
            title_font = pygame.font.Font(None, 28)
        except:
            data_font = pygame.font.SysFont('arial', 18)
            title_font = pygame.font.SysFont('arial', 22)
        
        title_text = "真实月季花生长数据"
        title_surface = title_font.render(title_text, True, (255, 255, 255))
        self.screen.blit(title_surface, (panel_x + 15, panel_y + 15))
        
        # 显示当前季节数据
        if current_season_data:
            data_texts = [
                f"季节: {current_season_data.get('season_name', 'N/A')}",
                f"月份: {current_season_data.get('months', 'N/A')}",
                f"温度范围: {current_season_data.get('temperature_range', 'N/A')}",
                f"开花期: {current_season_data.get('bloom_period_days', 0)}天",
                f"生长阶段: {current_season_data.get('growth_phase', 'N/A')}",
                f"湿度: {current_season_data.get('humidity', 'N/A')}",
                f"日照: {current_season_data.get('sunlight_hours', 'N/A')}",
                f"土温: {current_season_data.get('soil_temperature', 'N/A')}",
                "",
                f"描述: {current_season_data.get('description', 'N/A')}"
            ]
            
            for i, text in enumerate(data_texts):
                if text:  # 跳过空行
                    text_surface = data_font.render(text, True, (255, 255, 255))
                    self.screen.blit(text_surface, (panel_x + 15, panel_y + 50 + i * 22))
        
        # 显示数据来源
        source_y = panel_y + panel_height - 40
        source_text = "数据来源: 中国气象局 + 中科院植物所"
        source_surface = data_font.render(source_text, True, (180, 180, 180))
        self.screen.blit(source_surface, (panel_x + 15, source_y))
    
    def draw_cycle_progress(self):
        """绘制循环进度条"""
        bar_width = 500
        bar_height = 25
        bar_x = (SCREEN_WIDTH - bar_width) // 2
        bar_y = SCREEN_HEIGHT - 80
        
        # 背景
        pygame.draw.rect(self.screen, (40, 40, 40),
                        (bar_x, bar_y, bar_width, bar_height))
        pygame.draw.rect(self.screen, (200, 200, 200),
                        (bar_x, bar_y, bar_width, bar_height), 2)
        
        # 进度
        progress_width = int(bar_width * self.rose.total_progress)
        if progress_width > 0:
            season_colors = self.rose.get_current_season_colors()
            progress_color = season_colors['bloom']
            
            pygame.draw.rect(self.screen, progress_color,
                           (bar_x, bar_y, progress_width, bar_height))
        
        # 阶段分割（移除花苞期）
        stages = ["盛开", "维持", "凋零", "完全凋零", "重置"]
        durations = [
            self.rose.bloom_duration, 
            self.rose.maintain_duration,
            self.rose.wither_duration,
            self.rose.dead_duration,
            self.rose.reset_duration
        ]
        
        current_pos = 0
        for i, (stage, duration) in enumerate(zip(stages, durations)):
            current_pos += duration
            x_pos = bar_x + int(bar_width * current_pos / self.rose.total_cycle_duration)
            
            # 分割线
            pygame.draw.line(self.screen, (255, 255, 255),
                           (x_pos, bar_y), (x_pos, bar_y + bar_height), 2)
            
            # 标签
            if i < len(stages) - 1:
                label_surface = pygame.font.Font(None, 22).render(stage, True, (180, 180, 180))
                self.screen.blit(label_surface, (x_pos - 20, bar_y - 30))
    
    def handle_events(self):
        """处理事件"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    self.running = False
                elif event.key == pygame.K_SPACE:
                    # 加速效果
                    self.rose.frame_count += 100
    
    def run(self):
        """运行动画"""
        while self.running:
            self.handle_events()
            
            # 更新
            self.rose.update()
            
            # 绘制
            self.rose.draw(self.screen)
            self.draw_ui()
            
            pygame.display.flip()
            self.clock.tick(FPS)
        
        pygame.quit()

if __name__ == "__main__":
    animation = EnhancedRoseAnimation()
    animation.run()