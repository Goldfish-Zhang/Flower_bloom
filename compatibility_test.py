#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
花瓣一致性测试脚本
测试修复后的随机种子是否确保花瓣形状一致
"""

import pygame
import sys

def test_petal_consistency():
    """测试花瓣创建的一致性"""
    print("🔍 测试花瓣一致性...")
    
    try:
        # 导入动画模块
        import rose_animation
        from rose_animation import SeasonalRose
        
        # 创建两个独立的rose实例
        pygame.init()
        rose1 = SeasonalRose()
        rose2 = SeasonalRose()
        pygame.quit()
        
        print(f"✅ Rose1 花瓣数量: {len(rose1.petals)}")
        print(f"✅ Rose2 花瓣数量: {len(rose2.petals)}")
        
        if len(rose1.petals) != len(rose2.petals):
            print("❌ 花瓣数量不一致！")
            return False
        
        # 检查前几个花瓣的角度是否一致
        consistent = True
        for i in range(min(10, len(rose1.petals))):
            angle1 = rose1.petals[i].base_angle
            angle2 = rose2.petals[i].base_angle
            offset1 = rose1.petals[i].angle_offset
            offset2 = rose2.petals[i].angle_offset
            
            if abs(angle1 - angle2) > 0.001:
                print(f"❌ 花瓣 {i} 基础角度不一致: {angle1:.3f} vs {angle2:.3f}")
                consistent = False
                
            if abs(offset1 - offset2) > 0.001:
                print(f"❌ 花瓣 {i} 角度偏移不一致: {offset1:.3f} vs {offset2:.3f}")
                consistent = False
        
        if consistent:
            print("✅ 花瓣角度完全一致!")
            return True
        else:
            print("❌ 花瓣角度存在差异!")
            return False
            
    except Exception as e:
        print(f"❌ 测试失败: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_random_seed_effect():
    """测试随机种子的效果"""
    print("\n🔍 测试随机种子效果...")
    
    import random
    
    # 重置随机种子多次，应该得到相同结果
    values1 = []
    values2 = []
    
    random.seed(42)
    for i in range(10):
        values1.append(random.uniform(-0.15, 0.15))
    
    random.seed(42)  # 重新设置相同种子
    for i in range(10):
        values2.append(random.uniform(-0.15, 0.15))
    
    if values1 == values2:
        print("✅ 随机种子正确工作，生成一致的随机数序列")
        return True
    else:
        print("❌ 随机种子未正确工作")
        print(f"序列1: {values1[:3]}...")
        print(f"序列2: {values2[:3]}...")
        return False

def test_version_compatibility():
    """测试版本兼容性"""
    print("\n🔍 测试版本兼容性...")
    
    try:
        import pygame
        version = pygame.version.ver
        major, minor = map(int, version.split('.')[:2])
        
        print(f"✅ Pygame版本: {version}")
        
        if major >= 2:
            print("✅ Pygame版本兼容")
            return True
        else:
            print("❌ Pygame版本过低，建议升级到2.0+")
            return False
            
    except Exception as e:
        print(f"❌ 版本检查失败: {e}")
        return False

def main():
    """运行所有兼容性测试"""
    print("🚀 开始花瓣一致性和兼容性测试...\n")
    
    tests = [
        test_random_seed_effect,
        test_version_compatibility, 
        test_petal_consistency,
    ]
    
    passed = 0
    failed = 0
    
    for test in tests:
        try:
            if test():
                passed += 1
            else:
                failed += 1
        except Exception as e:
            print(f"❌ 测试 {test.__name__} 出错: {e}")
            failed += 1
    
    print(f"\n📊 测试结果:")
    print(f"✅ 通过: {passed}")
    print(f"❌ 失败: {failed}")
    
    if failed == 0:
        print("\n🎉 所有测试通过! 花瓣应该在所有系统上显示一致!")
        return True
    else:
        print(f"\n⚠️ {failed} 个测试失败，可能存在兼容性问题")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)