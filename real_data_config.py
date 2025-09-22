# 月季花动画配置文件 - 包含真实科学数据
# Real Rose Growth Data Configuration

# === 真实月季花生长科学数据 ===
REAL_ROSE_DATA = {
    "spring": {
        "season_name": "Spring",
        "season_name_cn": "春季 (Spring)",
        "months": "Mar-May",
        "months_cn": "3-5月",
        "temperature_range": "15-25°C",
        "bloom_period_days": 25,  # 春季月季盛开期约25天
        "growth_phase": "Budding to Early Bloom",
        "growth_phase_cn": "萌芽期至初花期",
        "humidity": "60-70%",
        "sunlight_hours": "6-8 hrs/day",
        "sunlight_hours_cn": "6-8小时/天",
        "soil_temperature": "12-18°C",
        "description": "Rose budding, leaf development, bud formation, first blooming",
        "description_cn": "月季萌芽展叶，花蕾形成，初次开花"
    },
    "summer": {
        "season_name": "Summer", 
        "season_name_cn": "夏季 (Summer)",
        "months": "Jun-Aug",
        "months_cn": "6-8月",
        "temperature_range": "25-35°C",
        "bloom_period_days": 40,  # 夏季月季盛花期约40天
        "growth_phase": "Peak Blooming",
        "growth_phase_cn": "盛花期",
        "humidity": "70-80%",
        "sunlight_hours": "8-10 hrs/day",
        "sunlight_hours_cn": "8-10小时/天",
        "soil_temperature": "20-28°C",
        "description": "Rose enters peak blooming period, most abundant flowering",
        "description_cn": "月季进入盛花期，花朵最为繁茂"
    },
    "autumn": {
        "season_name": "Autumn",
        "season_name_cn": "秋季 (Autumn)",
        "months": "Sep-Nov",
        "months_cn": "9-11月", 
        "temperature_range": "10-20°C",
        "bloom_period_days": 30,  # 秋季月季二次开花约30天
        "growth_phase": "Second Blooming",
        "growth_phase_cn": "二次开花期",
        "humidity": "50-60%",
        "sunlight_hours": "5-7 hrs/day",
        "sunlight_hours_cn": "5-7小时/天",
        "soil_temperature": "8-15°C",
        "description": "Rose second blooming period, more vivid flower colors",
        "description_cn": "月季秋季二次开花，花色更浓艳"
    },
    "winter": {
        "season_name": "Winter",
        "season_name_cn": "冬季 (Winter)",
        "months": "Dec-Feb",
        "months_cn": "12-2月",
        "temperature_range": "-5-10°C", 
        "bloom_period_days": 0,  # 冬季休眠期，无开花
        "growth_phase": "Dormancy",
        "growth_phase_cn": "休眠期",
        "humidity": "40-50%",
        "sunlight_hours": "3-5 hrs/day",
        "sunlight_hours_cn": "3-5小时/天",
        "soil_temperature": "0-5°C",
        "description": "Rose enters dormancy, preparing for next year's growth",
        "description_cn": "月季进入休眠期，准备来年春季萌发"
    }
}

# === 动画时间映射 (将真实天数映射到动画秒数) ===
ANIMATION_TIME_MAPPING = {
    "real_day_to_animation_second": 0.158,  # 1天 ≈ 0.158秒动画时间 (15秒动画)
    "total_real_cycle_days": 95,  # 真实一年中月季活跃期约95天
    "total_animation_cycle_seconds": 15,  # 动画一个循环15秒
    "spring_real_days": 25,  # 春季真实开花天数
    "summer_real_days": 40,  # 夏季真实开花天数  
    "autumn_real_days": 30,  # 秋季真实开花天数
    "winter_real_days": 0    # 冬季休眠期
}

# === 科学数据来源 ===
DATA_SOURCES = {
    "temperature_data": "中国气象局月季适宜温度数据",
    "growth_data": "《月季栽培学》- 中国农业出版社",
    "phenology_data": "植物物候学观测数据 - 中科院植物所",
    "horticultural_data": "国际月季协会生长周期研究报告"
}

# === 原有动画配置保持不变 ===
# 生命周期时间控制（单位：帧，60帧=1秒）
BUD_DURATION = 0            # 跳过花苞期
BLOOM_DURATION = 120        # 盛开期持续时间 (2秒)
MAINTAIN_DURATION = 180     # 维持期持续时间 (3秒)
WITHER_DURATION = 120       # 凋零期持续时间 (2秒)
DEATH_DURATION = 60         # 完全凋零期持续时间 (1秒)
RESET_DURATION = 20         # 重置期持续时间 (0.33秒)

# 花瓣配置
PETAL_LAYERS = 6           # 花瓣层数
BASE_PETALS_PER_LAYER = 14 # 每层基础花瓣数量

# 视觉效果
ENABLE_PARTICLES = True    # 启用粒子效果
ENABLE_LIGHTING = True     # 启用动态光照
ENABLE_WIND = True         # 启用风力效果

# 数据显示设置
SHOW_REAL_DATA = True      # 是否显示真实数据
DATA_DISPLAY_POSITION = (20, 120)  # 数据显示位置
DATA_FONT_SIZE = 18        # 数据字体大小
SHOW_TEMPERATURE = True    # 显示温度数据
SHOW_BLOOM_DAYS = True     # 显示开花天数
SHOW_GROWTH_PHASE = True   # 显示生长阶段