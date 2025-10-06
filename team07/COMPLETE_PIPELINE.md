# Q-Learning Bomberman AI - Complete Pipeline

## 🎯 **OVERALL ARCHITECTURE**

```
┌─────────────────────────────────────────────────────────────────┐
│                    Q-LEARNING PIPELINE                         │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌─────────────┐    ┌──────────────┐    ┌─────────────────┐    │
│  │   TRAINING  │───▶│   LEARNING   │───▶│    TESTING     │    │
│  │   PHASE     │    │    PHASE     │    │    PHASE       │    │
│  └─────────────┘    └──────────────┘    └─────────────────┘    │
│         │                    │                      │            │
│         ▼                    ▼                      ▼            │
│  ┌─────────────┐    ┌──────────────┐    ┌─────────────────┐    │
│  │   EPISODES  │    │  WEIGHT      │    │   SUCCESS      │    │
│  │   (500-1500)│    │  UPDATES     │    │   EVALUATION   │    │
│  └─────────────┘    └──────────────┘    └─────────────────┘    │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

## 🔄 **DETAILED PIPELINE FLOW**

### **PHASE 1: INITIALIZATION**
```
┌─────────────────────────────────────────────────────────────────┐
│ 1. CREATE Q-LEARNING AGENT                                       │
│    ├─ Load initial weights: w_e=4, w_m=-1, w_x=-2              │
│    ├─ Set learning parameters: α=0.5, γ=0.9, ε=0.1             │
│    ├─ Initialize action space: 9 actions (8 directions + stay) │
│    └─ Set training mode: exploration enabled                   │
└─────────────────────────────────────────────────────────────────┘
```

### **PHASE 2: TRAINING LOOP**
```
┌─────────────────────────────────────────────────────────────────┐
│ FOR EACH TRAINING EPISODE:                                      │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │ 2. EPISODE SETUP                                            │ │
│  │    ├─ Create game instance (variant1.py, variant2.py, etc)│ │
│  │    ├─ Place character at (0,0)                             │ │
│  │    ├─ Add monsters (if variant 2-5)                        │ │
│  │    └─ Initialize episode reward = 0                        │ │
│  └─────────────────────────────────────────────────────────────┘ │
│                              │                                  │
│                              ▼                                  │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │ 3. GAME LOOP (until episode ends)                          │ │
│  │                                                             │ │
│  │    ┌─────────────────────────────────────────────────────┐  │ │
│  │    │ 3a. STATE OBSERVATION                               │  │ │
│  │    │    ├─ Extract features: f_e, f_m, f_x               │  │ │
│  │    │    ├─ Calculate distances using Chebyshev metric   │  │ │
│  │    │    └─ Store current state                           │  │ │
│  │    └─────────────────────────────────────────────────────┘  │ │
│  │                              │                             │ │
│  │                              ▼                             │ │
│  │    ┌─────────────────────────────────────────────────────┐  │ │
│  │    │ 3b. ACTION SELECTION (ε-greedy)                     │  │ │
│  │    │    ├─ Random action (10% exploration)               │  │ │
│  │    │    └─ Best Q-value action (90% exploitation)      │  │ │
│  │    └─────────────────────────────────────────────────────┘  │ │
│  │                              │                             │ │
│  │                              ▼                             │ │
│  │    ┌─────────────────────────────────────────────────────┐  │ │
│  │    │ 3c. ACTION EXECUTION                                │  │ │
│  │    │    ├─ Move character: character.move(dx, dy)        │  │ │
│  │    │    ├─ Update world state                            │  │ │
│  │    │    └─ Get events (death, exit, etc.)               │  │ │
│  │    └─────────────────────────────────────────────────────┘  │ │
│  │                              │                             │ │
│  │                              ▼                             │ │
│  │    ┌─────────────────────────────────────────────────────┐  │ │
│  │    │ 3d. REWARD CALCULATION                               │  │ │
│  │    │    ├─ +1000: Reached exit                           │  │ │
│  │    │    ├─ -1000: Died                                   │  │ │
│  │    │    ├─ -1: Per time step                             │  │ │
│  │    │    ├─ +100: Exit bonus                              │  │ │
│  │    │    ├─ +10/(distance+1): Closer to exit              │  │ │
│  │    │    └─ -50: Too close to monster                     │  │ │
│  │    └─────────────────────────────────────────────────────┘  │ │
│  │                              │                             │ │
│  │                              ▼                             │ │
│  │    ┌─────────────────────────────────────────────────────┐  │ │
│  │    │ 3e. LEARNING UPDATE                                  │  │ │
│  │    │    ├─ Calculate Q-value: Q(s,a) = w_e*f_e + w_m*f_m + w_x*f_x │  │ │
│  │    │    ├─ Calculate target: target = reward + γ*max_Q(s',a') │  │ │
│  │    │    ├─ Calculate error: error = target - Q(s,a)      │  │ │
│  │    │    └─ Update weights: w_i += α*error*f_i           │  │ │
│  │    └─────────────────────────────────────────────────────┘  │ │
│  └─────────────────────────────────────────────────────────────┘ │
│                              │                                  │
│                              ▼                                  │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │ 4. EPISODE COMPLETION                                       │ │
│  │    ├─ Check if episode was successful (reward > 0)         │ │
│  │    ├─ Update success counter                               │ │
│  │    ├─ Adjust exploration rate (ε)                          │ │
│  │    └─ Save weights every 50 episodes                      │ │
│  └─────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
```

### **PHASE 3: TESTING PHASE**
```
┌─────────────────────────────────────────────────────────────────┐
│ 5. TESTING SETUP                                                │
│    ├─ Load trained weights from file                           │
│    ├─ Set test mode: ε = 0.05 (reduced exploration)            │
│    └─ Initialize test counter                                  │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ FOR EACH TEST RUN (10 total):                                   │
│                                                                 │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │ 6. TEST EPISODE                                             │ │
│  │    ├─ Create game instance                                  │ │
│  │    ├─ Run episode with trained weights                      │ │
│  │    ├─ Count success/failure                                 │ │
│  │    └─ Record result                                         │ │
│  └─────────────────────────────────────────────────────────────┘ │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
┌─────────────────────────────────────────────────────────────────┐
│ 7. EVALUATION                                                   │
│    ├─ Calculate success rate: successes/10                     │
│    ├─ Check if ≥ 50% (5/10 wins)                              │
│    └─ Report PASS/FAIL                                         │
└─────────────────────────────────────────────────────────────────┘
```

## 📊 **FEATURE EXTRACTION DETAILS**

### **Chebyshev Distance Calculation:**
```python
# Exit distance
d_e = max(abs(character.x - exit_x), abs(character.y - exit_y))
f_e = 1.0 / (d_e + 1)

# Monster distance  
d_m = max(abs(character.x - monster_x), abs(character.y - monster_y))
f_m = 1.0 / (d_m + 1)

# Explosion distance
d_x = max(abs(character.x - explosion_x), abs(character.y - explosion_y))
f_x = 1.0 / (d_x + 1)
```

### **Q-Value Calculation:**
```python
Q(s,a) = w_e * f_e + w_m * f_m + w_x * f_x
```

### **Weight Update Rule:**
```python
error = (reward + γ * max_Q(s',a')) - Q(s,a)
w_e += α * error * f_e
w_m += α * error * f_m  
w_x += α * error * f_x
```

## 🎮 **VARIANT-SPECIFIC BEHAVIORS**

### **Variant 1: No Monsters**
- **Focus**: Pathfinding and bomb placement
- **Training Episodes**: 500
- **Key Features**: f_e (exit distance)

### **Variant 2: Stupid Monster**
- **Focus**: Random monster avoidance
- **Training Episodes**: 1000
- **Key Features**: f_e, f_m

### **Variant 3: Self-Preserving Monster**
- **Focus**: Maintain distance > 1 from monster
- **Training Episodes**: 1000
- **Key Features**: f_e, f_m (higher weight on f_m)

### **Variant 4: Aggressive Monster**
- **Focus**: Maintain distance > 2 from monster
- **Training Episodes**: 1000
- **Key Features**: f_e, f_m (even higher weight on f_m)

### **Variant 5: Two Monsters**
- **Focus**: Complex multi-monster avoidance
- **Training Episodes**: 1500
- **Key Features**: f_e, f_m (nearest monster), f_x

## 💾 **WEIGHT PERSISTENCE**

### **Training Weights Saved:**
```json
{
  "w_e": 4.2,
  "w_m": -1.5,
  "w_x": -2.1,
  "epsilon": 0.08,
  "episode_count": 750,
  "successful_episodes": 380,
  "total_episodes": 750
}
```

### **File Structure:**
```
team07/
├── algorithms/
│   └── q_learning.py          # Main Q-Learning implementation
├── project2/
│   ├── variant1.py            # No monsters
│   ├── variant2.py            # Stupid monster
│   ├── variant3.py            # Self-preserving monster
│   ├── variant4.py            # Aggressive monster
│   ├── variant5.py            # Two monsters
│   └── weights_variant1.json # Trained weights
├── train_q_learning.py        # Training/testing script
└── testcharacter.py          # Character with Q-Learning
```

## 🚀 **USAGE COMMANDS**

### **Training:**
```bash
# Train variant 1
python ../train_q_learning.py variant1.py --train --episodes 500

# Train variant 2  
python ../train_q_learning.py variant2.py --train --episodes 1000

# Train variant 3
python ../train_q_learning.py variant3.py --train --episodes 1000

# Train variant 4
python ../train_q_learning.py variant4.py --train --episodes 1000

# Train variant 5
python ../train_q_learning.py variant5.py --train --episodes 1500
```

### **Testing:**
```bash
# Test all variants
python ../train_q_learning.py variant1.py --test --tests 10
python ../train_q_learning.py variant2.py --test --tests 10
python ../train_q_learning.py variant3.py --test --tests 10
python ../train_q_learning.py variant4.py --test --tests 10
python ../train_q_learning.py variant5.py --test --tests 10
```

## 📈 **SUCCESS METRICS**

### **Training Success:**
- **Target**: 50% success rate
- **Minimum Episodes**: 100
- **Convergence**: When success rate ≥ 50%

### **Testing Success:**
- **Required**: 5/10 wins (50%)
- **Evaluation**: 10 independent test runs
- **Pass Criteria**: ≥ 5 successful episodes

This complete pipeline implements Approximate Q-Learning with linear function approximation, following the homework assignment specifications while adapting to the full Bomberman game environment!

