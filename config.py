# 月季花动画配置文件
# 修改以下参数来自定义动画效果

# === 完整季节循环版本配置 ===
# 生命周期时间控制（单位：帧，60帧=1秒）
BUD_DURATION = 180          # 花苞期持续时间
BLOOM_DURATION = 240        # 盛开期持续时间
MAINTAIN_DURATION = 300     # 维持期持续时间
WITHER_DURATION = 240       # 凋零期持续时间
DEATH_DURATION = 120        # 完全凋零期持续时间
RESET_DURATION = 60         # 重置期持续时间

# === 基础版本配置 ===
# 动画时间控制（单位：帧，60帧=1秒）
BLOOM_DURATION = 240        # 盛开持续时间
FULL_BLOOM_DURATION = 180   # 完全盛开持续时间  
WITHER_DURATION = 300       # 凋零持续时间

# 花瓣配置
PETAL_LAYERS = 7           # 花瓣层数
BASE_PETALS_PER_LAYER = 8  # 每层基础花瓣数量

# 视觉效果
ENABLE_PARTICLES = True    # 启用粒子效果
ENABLE_LIGHTING = True     # 启用动态光照
ENABLE_WIND = True         # 启用风力效果

# 季节背景颜色（RGB值）
# 花苞期背景
BUD_BG_TOP = (255, 248, 220)
BUD_BG_BOTTOM = (240, 230, 210)

# 盛开期背景 - 明亮天空蓝到翠绿
BLOOM_BG_TOP = (135, 206, 235)
BLOOM_BG_BOTTOM = (144, 238, 144)

# 维持期背景 - 夏日翠绿
MAINTAIN_BG_TOP = (152, 251, 152)
MAINTAIN_BG_BOTTOM = (124, 252, 0)

# 凋零期背景 - 黄昏橙红
WITHER_BG_TOP = (255, 140, 0)
WITHER_BG_BOTTOM = (255, 69, 0)

# 完全凋零期背景 - 深秋灰褐
DEATH_BG_TOP = (139, 121, 94)
DEATH_BG_BOTTOM = (101, 67, 33)

# 传统颜色主题（RGB值）
SPRING_COLOR = (255, 182, 193)    # 春季粉色
SUMMER_COLOR_DEEP = (220, 20, 60)  # 夏季深红
SUMMER_COLOR_LIGHT = (255, 105, 180)  # 夏季浅红
AUTUMN_COLOR = (255, 69, 0)        # 秋季橙红
WINTER_COLOR = (128, 0, 128)       # 冬季紫色

# 传统背景颜色（用于基础版本）
SPRING_BG = (245, 255, 245)
SUMMER_BG = (255, 250, 240)
AUTUMN_BG = (255, 248, 220)
WINTER_BG = (240, 248, 255)

# 视觉效果配置
ENABLE_PARTICLES = True       # 启用粒子效果
ENABLE_LIGHTING = True        # 启用动态光照（仅基础版）
ENABLE_WIND = True           # 启用风力效果
ENABLE_SEASONAL_PARTICLES = True  # 启用季节性粒子（季节循环版）

# 花瓣配置
PETAL_LAYERS = 7             # 花瓣层数
BASE_PETALS_PER_LAYER = 8    # 每层基础花瓣数量
ENABLE_BUD_STAGE = True      # 启用花苞阶段（季节循环版）

# 性能设置
FPS = 60                   # 帧率
PARTICLE_COUNT_LIMIT = 100 # 粒子数量限制

# 窗口设置
WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 800
FULLSCREEN = False         # 全屏模式