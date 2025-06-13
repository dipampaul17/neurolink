"""
Configuration file for NeuroLink: Cyberpunk Data Recovery game.
Contains all game constants and settings for easier tuning.
"""

# Display settings
WIDTH = 800
HEIGHT = 600
FPS = 60

# Cyberpunk color palette
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
NEON_BLUE = (0, 195, 255)      # Bright blue
NEON_TEAL = (0, 255, 207)     # Bright teal
NEON_CYAN = (0, 240, 255)     # Electric cyan
NEON_PINK = (255, 0, 153)     # Bright pink
NEON_PURPLE = (153, 0, 255)   # Bright purple
NEON_RED = (255, 0, 84)       # Bright red
NEON_ORANGE = (255, 128, 0)   # Bright orange
NEON_YELLOW = (255, 211, 25)  # Bright yellow
NEON_GREEN = (57, 255, 20)    # Bright green
GRID_LINE = (20, 100, 120)
DARK_BLUE = (5, 10, 28)

# Data Interceptor settings
PLAYER_WIDTH = 50
PLAYER_HEIGHT = 40
PLAYER_SPEED = 8
PLAYER_INITIAL_LIVES = 3  # System integrity levels
PLAYER_MAX_LIVES = 5
PLAYER_INVINCIBLE_DURATION = 120  # 2 seconds at 60 FPS - Neural buffer
PLAYER_SHIELD_DURATION = 600  # 10 seconds at 60 FPS - Firewall protection

# Data Packet settings
BULLET_WIDTH = 5
BULLET_HEIGHT = 15
BULLET_SPEED = 10
DOUBLE_SHOT_DURATION = 600  # 10 seconds at 60 FPS - Bandwidth boost

# Data Fragment settings
ENEMY_WIDTH = 40
ENEMY_HEIGHT = 40
ENEMY_INITIAL_SPEED = 1
ENEMY_ROWS = 5
ENEMY_COLS = 10
ENEMY_SPACING = 60
ENEMY_MOVE_DOWN = 20
ENEMY_INITIAL_MOVE_DELAY = 30
ENEMY_SHOOT_CHANCE = 0.005  # Corruption spread chance
ENEMY_EVOLUTION_CHANCE = 0.3  # Chance of fragment evolution on descent

# Firewall Node settings
BOSS_SCALE = 4  # Firewall node is 4x the size of regular data fragments
BOSS_LEVEL_INTERVAL = 5  # Firewall node appears every 5 levels
BOSS_INITIAL_HEALTH = 20
BOSS_HEALTH_INCREASE_PER_LEVEL = 10
BOSS_SHOOT_CHANCE_MULTIPLIER = 5
BOSS_MOVE_SPEED_MULTIPLIER = 2
BOSS_MOVE_DOWN_CHANCE = 0.05

# System Upgrade settings
POWERUP_TYPES = ["shield", "double_shot", "life", "bomb"]
POWERUP_COLORS = {
    "shield": NEON_BLUE,
    "double_shot": NEON_YELLOW,
    "life": NEON_GREEN,
    "bomb": NEON_RED
}
POWERUP_CHANCE = 0.01
POWERUP_SPEED = 2
POWERUP_SIZE = 20

# Combo system
COMBO_DURATION = 120  # 2 seconds at 60 FPS
COMBO_MAX_MULTIPLIER = 8
COMBO_HITS_PER_MULTIPLIER = 3

# Scoring
SCORE_HIT = 10
SCORE_DESTROY = 50
SCORE_BOSS_HIT = 20
SCORE_BOSS_DESTROY_MULTIPLIER = 1000
SCORE_BOMB_DESTROY = 30

# Particle effects
PARTICLE_COUNT_NORMAL = 20
PARTICLE_COUNT_EXPLOSION = 50
PARTICLE_MIN_SPEED = 1
PARTICLE_MAX_SPEED = 5
PARTICLE_MIN_SIZE = 2
PARTICLE_MAX_SIZE = 5
PARTICLE_MIN_LIFETIME = 30
PARTICLE_MAX_LIFETIME = 60

# Star background
STAR_COUNT = 100
STAR_MIN_SIZE = 1
STAR_MAX_SIZE = 3
STAR_MIN_SPEED = 0.1
STAR_MAX_SPEED = 0.5

# Difficulty scaling
LEVEL_MOVE_DELAY_DECREASE = 5
LEVEL_MOVE_DELAY_MIN = 5
LEVEL_SHOOT_CHANCE_INCREASE = 0.002

# Sound settings
SOUND_VOLUME = {
    "shoot": 0.3,
    "hit": 0.4,
    "game_over": 0.7,
    "powerup": 0.5,
    "explosion": 0.6,
    "level_up": 0.7
}

# Emoji states
EMOJI_STATES = ["😊", "😐", "😠", "😡"]
BOSS_EMOJI = "👿"
