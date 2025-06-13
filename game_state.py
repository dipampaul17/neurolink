"""
Game state management for NeuroLink: Cyberpunk Data Recovery game.
Handles digital system state, data recovery scoring, and network level progression.
"""

import pygame
import random
from config import *
from sprites import *

class GameState:
    """Manages the digital system state, data recovery tracking, and network level progression"""
    
    def __init__(self, sound_manager):
        """Initialize the game state"""
        self.sound_manager = sound_manager
        self.reset()
    
    def reset(self):
        """Reset the game state to initial values"""
        # Game state
        self.score = 0
        self.high_score = self.high_score if hasattr(self, 'high_score') else 0
        self.level = 1
        self.game_over = False
        self.game_won = False
        self.paused = False
        
        # Combo system
        self.combo_count = 0
        self.combo_timer = 0
        self.combo_multiplier = 1
        
        # Enemy movement
        self.enemy_direction = 1
        self.enemy_move_timer = 0
        self.enemy_move_delay = ENEMY_INITIAL_MOVE_DELAY
        self.enemy_shoot_chance = ENEMY_SHOOT_CHANCE
        
        # Boss mode
        self.boss_mode = False
        
        # Create sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.players = pygame.sprite.GroupSingle()
        self.enemies = pygame.sprite.Group()
        self.player_bullets = pygame.sprite.Group()
        self.enemy_bullets = pygame.sprite.Group()
        self.powerups = pygame.sprite.Group()
        self.particles = pygame.sprite.Group()
        self.stars = pygame.sprite.Group()
        
        # Create player
        self.player = Player()
        self.players.add(self.player)
        self.all_sprites.add(self.player)
        
        # Create stars
        self.create_stars()
        
        # Create enemies
        self.create_enemies()
    
    def create_stars(self):
        """Create background stars"""
        for _ in range(STAR_COUNT):
            star = Star()
            self.stars.add(star)
            self.all_sprites.add(star)
    
    def create_enemies(self):
        """Create the enemy grid"""
        # Clear existing enemies
        self.enemies.empty()
        
        # Every BOSS_LEVEL_INTERVAL levels, create a boss
        if self.level % BOSS_LEVEL_INTERVAL == 0:
            self.boss_mode = True
            boss = Boss(WIDTH // 2 - ENEMY_WIDTH * BOSS_SCALE // 2, 50, self.level)
            self.enemies.add(boss)
            self.all_sprites.add(boss)
            return
        
        # Regular enemy grid
        self.boss_mode = False
        start_x = (WIDTH - (ENEMY_COLS * ENEMY_SPACING)) // 2
        start_y = 50
        
        for row in range(ENEMY_ROWS):
            for col in range(ENEMY_COLS):
                x = start_x + col * ENEMY_SPACING
                y = start_y + row * ENEMY_SPACING
                enemy = Enemy(x, y)
                self.enemies.add(enemy)
                self.all_sprites.add(enemy)
    
    def create_particles(self, x, y, color, count=PARTICLE_COUNT_NORMAL):
        """Create explosion particles"""
        for _ in range(count):
            particle = Particle(x, y, color)
            self.particles.add(particle)
            self.all_sprites.add(particle)
    
    def create_powerup(self, x, y):
        """Create a random powerup with a certain chance"""
        if random.random() < POWERUP_CHANCE:
            powerup_type = random.choice(POWERUP_TYPES)
            powerup = PowerUp(x, y, powerup_type)
            self.powerups.add(powerup)
            self.all_sprites.add(powerup)
    
    def next_level(self):
        """Advance to the next level"""
        self.level += 1
        self.enemy_move_delay = max(LEVEL_MOVE_DELAY_MIN, self.enemy_move_delay - LEVEL_MOVE_DELAY_DECREASE)
        self.enemy_shoot_chance += LEVEL_SHOOT_CHANCE_INCREASE
        self.game_won = False
        
        # Clear bullets and powerups
        self.player_bullets.empty()
        self.enemy_bullets.empty()
        self.powerups.empty()
        
        # Create new enemies
        self.create_enemies()
        
        # Play sound
        self.sound_manager.play("level_up")
    
    def update_combo(self):
        """Update the combo system"""
        if self.combo_timer > 0:
            self.combo_timer -= 1
            if self.combo_timer <= 0:
                self.combo_count = 0
                self.combo_multiplier = 1
    
    def increment_combo(self):
        """Increment the combo counter and update multiplier"""
        self.combo_count += 1
        self.combo_timer = COMBO_DURATION
        self.combo_multiplier = min(COMBO_MAX_MULTIPLIER, 1 + self.combo_count // COMBO_HITS_PER_MULTIPLIER)
    
    def toggle_pause(self):
        """Toggle game pause state"""
        self.paused = not self.paused
        return self.paused
