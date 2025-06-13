# NeuroLink: Cyberpunk Data Recovery

```
 _   _                      _     _       _    
| \ | | ___ _   _ _ __ ___ | |   (_)_ __ | | __
|  \| |/ _ \ | | | '__/ _ \| |   | | '_ \| |/ /
| |\  |  __/ |_| | | | (_) | |___| | | | |   < 
|_| \_|\___|\__,_|_|  \___/|_____|_|_| |_|_|\_\
                                               
 _____      _                             _    
/ ____|    | |                           | |   
| |    _   _| |__   ___ _ __ _ __  _   _ _ | |__
| |   | | | | '_ \ / _ \ '__| '_ \| | | | | '_ \
| |___| |_| | |_) |  __/ |  | |_) | |_| | | | | |
 \_____\__, |_.__/ \___|_|  | .__/ \__,_|_|_| |_|
        __/ |               | |                 
       |___/                |_|                 
       
Data Recovery System
```

*A cyberpunk arcade game created with Amazon Q CLI for the 2025 AWS Summer Hack Challenge*

[![GitHub repo](https://img.shields.io/badge/GitHub-Repository-blue.svg)](https://github.com/dipampaul17/neurolink)
[![Made with Amazon Q](https://img.shields.io/badge/Made%20with-Amazon%20Q%20CLI-orange.svg)](https://aws.amazon.com/q/)

## Created for the Amazon Q Summer Hack Challenge 2025

A thrilling cyberpunk-themed arcade game where you navigate the digital realm as a Data Interceptor, recovering vital data fragments from corrupted network nodes in a neon-drenched cyberspace. Built with Python, Pygame, and **Amazon Q** to showcase the power of AI-assisted game development.

### 🌟 Game Features

- **Immersive Cyberpunk Universe**: Navigate a sleek Data Interceptor through a vibrant digital grid with dynamic neon visuals
- **Evolving Data Fragments**: Encounter data fragments that evolve as they descend through the network layers
- **Epic Firewall Node Battles**: Face challenging boss battles every 5 network levels
- **Advanced Data Packet System**: Launch targeted packets to interface with descending fragments
- **Neural Synchronization Scoring**: Earn higher scores with successful interfaces and build combo multipliers
- **System Upgrades**: Collect digital augmentations to enhance your capabilities
- **Dynamic Difficulty**: Experience increasing challenges as you progress deeper into the network
- **Pulsating Neon Visuals**: Enjoy a stunning 800x600 viewport with animated cyberpunk aesthetics
- **Synthwave Atmosphere**: Immerse yourself with digital sound effects and particle visualizations
- **Responsive Controls**: Precise and intuitive gameplay designed for maximum enjoyment

### 🎮 Controls

- **Arrow Keys**: Navigate your Data Interceptor through the digital grid
- **Spacebar**: Launch data packets to interface with fragments
- **P**: Pause neural connection
- **M**: Toggle audio atmosphere
- **R**: Reinitiate system after connection failure
- **N**: Proceed to next network level after success
- **Q**: Terminate connection (during game over or level complete)

### 💾 System Upgrades

- **Neural Shield** <span style="color:#00c3ff">(Neon Blue)</span>: Protects your interceptor from one hostile data fragment
- **Bandwidth Boost** <span style="color:#ffea00">(Neon Yellow)</span>: Doubles your data packet transmission rate
- **System Integrity** <span style="color:#00ff50">(Neon Green)</span>: Adds an additional life to your interceptor
- **Trace Eliminator** <span style="color:#ff0099">(Neon Pink)</span>: Purges all data fragments from the current screen

## 🔧 System Requirements

- Python 3.x
- Pygame 2.x
- Any modern operating system (Windows/macOS/Linux)

## 💻 Installation Protocol

1. Ensure your system has Python 3.x installed
2. Create an isolated virtual environment (recommended):
   ```bash
   python -m venv neurolink-env
   source neurolink-env/bin/activate  # On Windows: neurolink-env\Scripts\activate
   ```
3. Install required dependencies:
   ```bash
   pip install pygame
   ```
4. [Optional] Add sound files to the `sounds` directory for full audio experience
5. Execute the main program:
   ```bash
   python neurolink.py
   ```

## 🔄 System Mechanics

- **Evolving Data Fragments**: Data fragments start as simple forms and evolve through multiple states as they descend
- **Fragment Resistance**: Each data packet interaction increases fragment complexity until they can be successfully recovered
- **Neural Synchronization**: Score increases with each successful data fragment interface
- **Combo Multiplier**: Rapid consecutive packet transmissions build a multiplier for exponential score growth
- **Network Layer Difficulty**: Data fragments move faster and with more complex patterns as you progress
- **Firewall Node Encounters**: Every 5 levels features a challenging firewall node with unique defense patterns
- **System Upgrade Collection**: Collect augmentations dropped by successfully recovered data fragments

## ⚙️ Code Architecture

The system is modularly designed across several components:

- `neurolink.py`: Core system controller with the main game loop
- `config.py`: System parameters and configuration constants
- `sprites.py`: Visual entity classes for all network objects
- `sound_manager.py`: Digital audio signal processing
- `game_state.py`: Network state and synchronization score tracking

## 🌟 Amazon Q Development Showcase

This project was created for the **Amazon Q Summer Hack Challenge 2025** to demonstrate how AI assistants can enhance game development workflows. Amazon Q was used to:

- Generate initial game structure and mechanics
- Debug complex rendering and collision detection algorithms
- Implement visual effects and animations
- Optimize performance across different environments
- Transform the theme from a basic space shooter to an immersive cyberpunk experience

## 🎵 Audio Atmosphere

For the complete audio experience, add these recommended sound files to the `sounds` directory:
- "Cyberpunk_Laser.wav" - For data packet transmission
- "Digital_Explosion.wav" - For successful fragment recovery
- "Neural_Powerup.wav" - For augmentation collection
- "System_Alert.wav" - For damage notification
- "Network_Victory.wav" - For level completion
