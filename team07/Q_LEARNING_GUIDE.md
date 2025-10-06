# Q-Learning Bomberman AI - Usage Guide

## Overview

We've implemented Approximate Q-Learning for the Bomberman AI project with the following key features:

### ✅ **Completed Features:**

1. **Chebyshev Distance**: Fixed distance calculations for 8-way movement
2. **Linear Function Approximation**: `Q(s,a) = w_e*f_e + w_m*f_m + w_x*f_x`
3. **Feature Extraction**: Exit, monster, and explosion distance features
4. **Weight Persistence**: Save/load trained weights
5. **Training System**: Multi-episode training with success tracking
6. **Test Mode**: Reduced exploration for evaluation

## How to Use

### 1. **Training the Agent**

```bash
# Train on variant 1 (no monsters)
cd team07/project2
python ../train_q_learning.py variant1.py --train --episodes 500

# Train on variant 2 (stupid monster)
python ../train_q_learning.py variant2.py --train --episodes 1000

# Train on variant 3 (self-preserving monster)
python ../train_q_learning.py variant3.py --train --episodes 1000

# Train on variant 4 (aggressive monster)
python ../train_q_learning.py variant4.py --train --episodes 1000

# Train on variant 5 (two monsters)
python ../train_q_learning.py variant5.py --train --episodes 1500
```

### 2. **Testing the Trained Agent (Simple - What Graders Will Do)**

```bash
# Test trained agent by running variant directly
python variant1.py  # Uses weights_variant1.json if exists
python variant2.py  # Uses weights_variant2.json if exists
python variant3.py  # Uses weights_variant3.json if exists
python variant4.py  # Uses weights_variant4.json if exists
python variant5.py  # Uses weights_variant5.json if exists
```

### 3. **Testing the Trained Agent (Advanced - Multiple Runs)**

```bash
# Test trained agent (10 runs)
python ../train_q_learning.py variant1.py --test --tests 10

# Test with more runs
python ../train_q_learning.py variant1.py --test --tests 20
```

### 4. **Running Individual Variants**

```bash
# Run variant 1 with Q-Learning (automatically loads trained weights)
python variant1.py

# Run variant 2 with Q-Learning (automatically loads trained weights)
python variant2.py
```

## Key Implementation Details

### **Distance Calculations (Chebyshev)**
- **Exit Distance**: `max(|x_char - x_exit|, |y_char - y_exit|)`
- **Monster Distance**: `max(|x_char - x_monster|, |y_char - y_monster|)`
- **Explosion Distance**: `max(|x_char - x_explosion|, |y_char - y_explosion|)`

### **Features**
- **f_e = 1/(d_e + 1)**: Exit distance feature
- **f_m = 1/(d_m + 1)**: Monster distance feature  
- **f_x = 1/(d_x + 1)**: Explosion distance feature

### **Learning Parameters**
- **Learning Rate (α)**: 0.5
- **Discount Factor (γ)**: 0.9
- **Exploration Rate (ε)**: 0.1 (training), 0.05 (testing)

### **Reward Structure**
- **+1000**: Reach exit (success)
- **-1000**: Die (failure)
- **-1**: Per time step (efficiency)
- **+100**: Exit bonus
- **+10/(distance+1)**: Closer to exit
- **-50**: Too close to monster

## Expected Workflow

1. **Train** each variant until 50%+ success rate
2. **Save** trained weights automatically
3. **Test** trained agent by running variant files directly
4. **Verify** 5/10 success rate requirement

## 🎯 **Automatic Weight Loading**

When you run a variant file (e.g., `python variant1.py`), the system automatically:

1. **Detects** which variant is being run
2. **Looks for** corresponding weight file (`weights_variant1.json`)
3. **Loads** trained weights if they exist
4. **Sets** test mode (reduced exploration)
5. **Runs** the game with trained knowledge

### **Behavior:**
- **If weights exist**: Agent uses trained knowledge (test mode, ε = 0.05)
- **If no weights**: Agent uses initial weights (untrained, ε = 0.1)
- **Graders**: Just run `python variant1.py` - no special commands needed!

## Files Created

- `weights_variant1.json`: Trained weights for variant 1
- `weights_variant2.json`: Trained weights for variant 2
- `weights_variant3.json`: Trained weights for variant 3
- `weights_variant4.json`: Trained weights for variant 4
- `weights_variant5.json`: Trained weights for variant 5

## Success Criteria

- **Target**: 50% success rate (5/10 wins)
- **Training**: Continue until target reached
- **Testing**: Run 10 episodes with trained weights
- **Evaluation**: Count successful episodes (reward > 0)

The agent learns through trial and error, gradually improving its ability to navigate to the exit while avoiding monsters and explosions!
