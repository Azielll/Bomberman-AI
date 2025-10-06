#!/usr/bin/env python3
"""
Simple testing script to demonstrate Q-Learning integration
This shows how the system works when graders run variant files directly
"""

import os
import sys

def test_variant_directly(variant_name):
    """
    Test a variant by running it directly (like graders will do)
    """
    print(f"\n=== Testing {variant_name} directly ===")
    
    # Check if trained weights exist
    weights_file = f"weights_{variant_name}.json"
    if os.path.exists(weights_file):
        print(f"✓ Found trained weights: {weights_file}")
        print("Agent will use trained weights (test mode)")
    else:
        print(f"✗ No trained weights found: {weights_file}")
        print("Agent will use initial weights (untrained)")
    
    # Run the variant
    print(f"Running: python {variant_name}.py")
    print("=" * 50)
    
    # This would be the actual command graders run
    # os.system(f"python {variant_name}.py")

def main():
    """
    Demonstrate the complete workflow
    """
    print("🎯 Q-LEARNING BOMBERMAN AI - TESTING WORKFLOW")
    print("=" * 60)
    
    print("\n📋 WORKFLOW FOR GRADERS:")
    print("1. Train agent: python ../train_q_learning.py variant1.py --train --episodes 500")
    print("2. Test agent: python variant1.py")
    print("3. Graders run: python variant1.py")
    
    print("\n🔍 TESTING EACH VARIANT:")
    
    variants = ["variant1", "variant2", "variant3", "variant4", "variant5"]
    
    for variant in variants:
        test_variant_directly(variant)
    
    print("\n📊 EXPECTED BEHAVIOR:")
    print("• If weights exist: Agent uses trained knowledge (test mode)")
    print("• If no weights: Agent uses initial weights (untrained)")
    print("• Test mode: Reduced exploration (ε = 0.05)")
    print("• Training mode: Higher exploration (ε = 0.1)")
    
    print("\n🎮 GRADER COMMANDS:")
    print("cd team07/project2")
    print("python variant1.py  # Uses weights_variant1.json if exists")
    print("python variant2.py  # Uses weights_variant2.json if exists")
    print("python variant3.py  # Uses weights_variant3.json if exists")
    print("python variant4.py  # Uses weights_variant4.json if exists")
    print("python variant5.py  # Uses weights_variant5.json if exists")

if __name__ == "__main__":
    main()

