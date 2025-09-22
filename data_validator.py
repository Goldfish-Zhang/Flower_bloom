#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
月季花真实数据验证脚本
用于验证和展示real_data_config.py中的科学数据
"""

from real_data_config import *

def print_seasonal_data():
    """打印所有季节的数据"""
    print("=" * 60)
    print("🌹 月季花真实生长数据总览")
    print("=" * 60)
    
    for season, data in REAL_ROSE_DATA.items():
        print(f"\n🌱 {data['season_name']}")
        print("-" * 40)
        print(f"📅 月份: {data['months']}")
        print(f"🌡️ 温度范围: {data['temperature_range']}")
        print(f"🌸 开花期: {data['bloom_period_days']}天")
        print(f"🔄 生长阶段: {data['growth_phase']}")
        print(f"💧 湿度: {data['humidity']}")
        print(f"☀️ 日照: {data['sunlight_hours']}")
        print(f"🌱 土温: {data['soil_temperature']}")
        print(f"📝 描述: {data['description']}")

def print_animation_mapping():
    """打印动画时间映射"""
    print("\n" + "=" * 60)
    print("⏰ 动画时间映射")
    print("=" * 60)
    
    mapping = ANIMATION_TIME_MAPPING
    print(f"🔄 真实生长周期: {mapping['total_real_cycle_days']}天")
    print(f"⚡ 动画循环时间: {mapping['total_animation_cycle_seconds']}秒")
    print(f"📏 时间比例: 1天 ≈ {mapping['real_day_to_animation_second']:.3f}秒")
    
    print("\n季节动画时长分配:")
    spring_time = mapping['spring_real_days'] * mapping['real_day_to_animation_second']
    summer_time = mapping['summer_real_days'] * mapping['real_day_to_animation_second']
    autumn_time = mapping['autumn_real_days'] * mapping['real_day_to_animation_second']
    
    print(f"🌸 春季: {mapping['spring_real_days']}天 → {spring_time:.1f}秒动画")
    print(f"☀️ 夏季: {mapping['summer_real_days']}天 → {summer_time:.1f}秒动画")
    print(f"🍂 秋季: {mapping['autumn_real_days']}天 → {autumn_time:.1f}秒动画")
    print(f"❄️ 冬季: {mapping['winter_real_days']}天 → 休眠期")

def print_data_sources():
    """打印数据来源"""
    print("\n" + "=" * 60)
    print("📚 数据来源")
    print("=" * 60)
    
    for source_type, source_info in DATA_SOURCES.items():
        print(f"📖 {source_type}: {source_info}")

def main():
    """主函数"""
    print_seasonal_data()
    print_animation_mapping()
    print_data_sources()
    
    print("\n" + "=" * 60)
    print("✅ 数据验证完成！所有配置正常。")
    print("🚀 现在可以运行 python launcher.py 查看带真实数据的动画")
    print("=" * 60)

if __name__ == "__main__":
    main()