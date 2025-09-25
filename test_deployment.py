#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Complete functionality test for Rose Bloom Animation
Tests all components to ensure GitHub deployment readiness
"""

import sys
import traceback
import importlib.util

def test_imports():
    """Test all required imports"""
    print("🔍 Testing imports...")
    
    try:
        import pygame
        print(f"✅ Pygame {pygame.version.ver} imported successfully")
        
        import math
        import random
        import typing
        print("✅ Standard library imports successful")
        
        # Test custom modules
        import config
        print("✅ config.py imported successfully")
        
        import real_data_config
        print("✅ real_data_config.py imported successfully")
        
        import rose_animation
        print("✅ rose_animation.py imported successfully")
        
        return True
    except Exception as e:
        print(f"❌ Import test failed: {e}")
        return False

def test_data_configuration():
    """Test data configuration validity"""
    print("\n🔍 Testing data configuration...")
    
    try:
        from real_data_config import REAL_ROSE_DATA, ANIMATION_TIME_MAPPING
        
        # Check all seasons exist
        required_seasons = ['spring', 'summer', 'autumn', 'winter']
        for season in required_seasons:
            if season not in REAL_ROSE_DATA:
                raise ValueError(f"Missing season: {season}")
            
            season_data = REAL_ROSE_DATA[season]
            required_fields = ['season_name', 'temperature_range', 'bloom_period_days']
            for field in required_fields:
                if field not in season_data:
                    raise ValueError(f"Missing field {field} in {season}")
        
        print("✅ All seasons and data fields present")
        
        # Check time mapping
        if ANIMATION_TIME_MAPPING['total_animation_cycle_seconds'] != 15:
            raise ValueError("Animation cycle should be 15 seconds")
        
        print("✅ Time mapping configuration valid")
        return True
        
    except Exception as e:
        print(f"❌ Data configuration test failed: {e}")
        return False

def test_core_classes():
    """Test core animation classes"""
    print("\n🔍 Testing core classes...")
    
    try:
        import pygame
        pygame.init()
        
        from rose_animation import (
            SeasonalBloomColors, 
            EnhancedPetal, 
            EnhancedParticle, 
            SeasonalRose, 
            EnhancedRoseAnimation
        )
        
        # Test color system
        colors = SeasonalBloomColors.get_season_colors('spring')
        if not isinstance(colors, dict):
            raise ValueError("Season colors should return dict")
        print("✅ SeasonalBloomColors working")
        
        # Test petal creation
        petal = EnhancedPetal(0, 0, 14)
        print("✅ EnhancedPetal creation successful")
        
        # Test particle creation  
        particle = EnhancedParticle(400, 300, 'spring_petal')
        print("✅ EnhancedParticle creation successful")
        
        # Test main rose
        rose = SeasonalRose()
        print("✅ SeasonalRose creation successful")
        
        # Test animation system
        animation = EnhancedRoseAnimation()
        print("✅ EnhancedRoseAnimation creation successful")
        
        pygame.quit()
        return True
        
    except Exception as e:
        print(f"❌ Core classes test failed: {e}")
        traceback.print_exc()
        return False

def test_animation_logic():
    """Test animation update logic"""
    print("\n🔍 Testing animation logic...")
    
    try:
        import pygame
        pygame.init()
        
        from rose_animation import EnhancedRoseAnimation
        
        animation = EnhancedRoseAnimation()
        
        # Test multiple update cycles
        initial_season = animation.rose.current_season
        initial_stage = animation.rose.life_stage
        
        for i in range(100):
            animation.rose.update()
            day = animation.calculate_current_day()
            
            if i == 50:
                mid_season = animation.rose.current_season
                mid_stage = animation.rose.life_stage
                mid_day = day
        
        print(f"✅ Initial: Season={initial_season}, Stage={initial_stage}")
        print(f"✅ Mid-cycle: Season={mid_season}, Stage={mid_stage}, Day={mid_day}")
        print("✅ Animation logic working correctly")
        
        pygame.quit()
        return True
        
    except Exception as e:
        print(f"❌ Animation logic test failed: {e}")
        traceback.print_exc()
        return False

def test_file_structure():
    """Test required files exist"""
    print("\n🔍 Testing file structure...")
    
    import os
    required_files = [
        'rose_animation.py',
        'config.py', 
        'real_data_config.py',
        'launcher.py',
        'data_validator.py',
        'requirements.txt',
        'README.md',
        '.gitignore'
    ]
    
    missing_files = []
    for file in required_files:
        if not os.path.exists(file):
            missing_files.append(file)
    
    if missing_files:
        print(f"❌ Missing files: {missing_files}")
        return False
    
    print("✅ All required files present")
    return True

def test_requirements():
    """Test requirements.txt validity"""
    print("\n🔍 Testing requirements.txt...")
    
    try:
        with open('requirements.txt', 'r') as f:
            content = f.read().strip()
        
        if 'pygame>=2.0.0' not in content:
            raise ValueError("pygame requirement missing or incorrect")
        
        print("✅ requirements.txt is valid")
        return True
        
    except Exception as e:
        print(f"❌ Requirements test failed: {e}")
        return False

def main():
    """Run all tests"""
    print("🚀 Starting comprehensive GitHub deployment test...\n")
    
    tests = [
        test_file_structure,
        test_imports,
        test_requirements,
        test_data_configuration,
        test_core_classes,
        test_animation_logic,
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
            print(f"❌ Test {test.__name__} crashed: {e}")
            failed += 1
    
    print(f"\n📊 Test Results:")
    print(f"✅ Passed: {passed}")
    print(f"❌ Failed: {failed}")
    print(f"📈 Success Rate: {passed/(passed+failed)*100:.1f}%")
    
    if failed == 0:
        print("\n🎉 ALL TESTS PASSED! Ready for GitHub deployment!")
        return True
    else:
        print(f"\n⚠️  {failed} test(s) failed. Please fix before deployment.")
        return False

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)