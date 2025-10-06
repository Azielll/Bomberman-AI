#!/usr/bin/env python3
"""
Demonstration: How Q-Learning Integration Works for Graders
This shows the complete workflow from training to testing
"""

import os
import sys

def demonstrate_workflow():
    """
    Demonstrate the complete Q-Learning workflow
    """
    print("🎯 Q-LEARNING BOMBERMAN AI - COMPLETE WORKFLOW")
    print("=" * 60)
    
    print("\n📋 STEP 1: TRAINING (You do this once)")
    print("cd team07/project2")
    print("python ../train_q_learning.py variant1.py --train --episodes 500")
    print("python ../train_q_learning.py variant2.py --train --episodes 1000")
    print("python ../train_q_learning.py variant3.py --train --episodes 1000")
    print("python ../train_q_learning.py variant4.py --train --episodes 1000")
    print("python ../train_q_learning.py variant5.py --train --episodes 1500")
    
    print("\n📋 STEP 2: TESTING (Graders do this)")
    print("python variant1.py  # Automatically uses weights_variant1.json")
    print("python variant2.py  # Automatically uses weights_variant2.json")
    print("python variant3.py  # Automatically uses weights_variant3.json")
    print("python variant4.py  # Automatically uses weights_variant4.json")
    print("python variant5.py  # Automatically uses weights_variant5.json")
    
    print("\n🔍 WHAT HAPPENS WHEN GRADERS RUN variant1.py:")
    print("1. TestCharacter detects 'variant1' in filename")
    print("2. Creates ApproximateQLearning agent")
    print("3. Sets weights_file = 'weights_variant1.json'")
    print("4. Calls q_agent.load_weights()")
    print("5. Sets test mode (ε = 0.05)")
    print("6. Runs game with trained knowledge")
    
    print("\n📊 EXPECTED OUTPUT:")
    print("Detected Variant 1 - Using Approximate Q-Learning Algorithm")
    print("Weights loaded from weights_variant1.json")
    print("Loaded weights: w_e=5.2, w_m=-1.8, w_x=-2.3")
    print("Epsilon: 0.050, Episodes: 750")
    print("Switched to TEST mode - reduced exploration")
    print("[Game runs with trained agent]")
    
    print("\n🎮 GRADER EXPERIENCE:")
    print("• Graders just run: python variant1.py")
    print("• No special commands needed")
    print("• Agent automatically uses trained weights")
    print("• Test mode ensures consistent performance")
    print("• Success rate should be 50%+ if training worked")
    
    print("\n✅ BENEFITS:")
    print("• Simple for graders (just run variant files)")
    print("• Automatic weight loading")
    print("• Test mode for consistent performance")
    print("• Fallback to initial weights if no training")
    print("• No manual configuration needed")

def check_weight_files():
    """
    Check which weight files exist
    """
    print("\n🔍 CHECKING WEIGHT FILES:")
    print("=" * 30)
    
    variants = ["variant1", "variant2", "variant3", "variant4", "variant5"]
    
    for variant in variants:
        weights_file = f"weights_{variant}.json"
        if os.path.exists(weights_file):
            print(f"✓ {weights_file} - Trained agent available")
        else:
            print(f"✗ {weights_file} - No trained weights (will use initial weights)")

if __name__ == "__main__":
    demonstrate_workflow()
    check_weight_files()
    
    print("\n🚀 READY TO GO!")
    print("Train your agents, then graders can simply run:")
    print("python variant1.py")
    print("python variant2.py")
    print("python variant3.py")
    print("python variant4.py")
    print("python variant5.py")

