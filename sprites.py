"""
Sprite classes for NeuroLink: Cyberpunk Data Recovery game.
Contains all digital entities as pygame sprites for better organization and collision detection.
"""

import pygame
import random
import math
from config import *

class Player(pygame.sprite.Sprite):
    """Data Interceptor sprite - player's digital vessel in cyberspace"""
    
    def __init__(self):
        super().__init__()
        self.width = PLAYER_WIDTH
        self.height = PLAYER_HEIGHT
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 2
        self.rect.bottom = HEIGHT - 20
        self.speed = PLAYER_SPEED
        self.lives = PLAYER_INITIAL_LIVES
        
        # Power-up states
        self.shield = False
        self.shield_timer = 0
        self.double_shot = False
        self.double_shot_timer = 0
        self.invincible = False
        self.invincible_timer = 0
        
        # Update the image
        self.update_image()
    
    def update_image(self):
        """Update the interceptor's visual appearance based on current state"""
        self.image.fill((0, 0, 0, 0))  # Clear with transparent background
        
        # Draw firewall shield if active
        if self.shield:
            shield_radius = max(self.width, self.height) + 10
            shield_surface = pygame.Surface((shield_radius * 2, shield_radius * 2), pygame.SRCALPHA)
            # Hexagonal shield with pulsing glow effect
            time_pulse = pygame.time.get_ticks() % 1000 / 1000
            alpha = int(100 + 100 * time_pulse)
            points = []
            for i in range(6):
                angle = 2 * math.pi * i / 6
                points.append((shield_radius + shield_radius * math.cos(angle), 
                               shield_radius + shield_radius * math.sin(angle)))
            pygame.draw.polygon(shield_surface, (*NEON_BLUE, alpha), points, 2)
            self.image.blit(shield_surface, (-shield_radius + self.width // 2, -shield_radius + self.height // 2))
        # Interceptor color based on power-ups
        ship_color = NEON_TEAL
        if self.double_shot:
            ship_color = NEON_YELLOW
        
        # Cyberpunk interceptor design - sleeker with neon edges
        # Main body
        points = [
            (self.width // 2, 0),  # Top
            (0, self.height * 0.8),  # Lower left
            (self.width // 4, self.height * 0.6),  # Inner left
            (self.width * 3 // 4, self.height * 0.6),  # Inner right
            (self.width, self.height * 0.8)  # Lower right
        ]
        pygame.draw.polygon(self.image, ship_color, points)
        
        # Neon trim - glowing edge effect
        pygame.draw.lines(self.image, NEON_PINK, False, points, 2)
        
        # Digital circuit pattern
        line_start = (self.width // 4, self.height * 0.3)
        line_end = (self.width * 3 // 4, self.height * 0.3)
        pygame.draw.line(self.image, NEON_BLUE, line_start, line_end, 1)
        
        # Draw engine thrust (animated with digital particles)
        time_val = pygame.time.get_ticks() / 1000
        thrust_width = 3 + int(2 * math.sin(time_val * 10))
        thrust_color = NEON_ORANGE if time_val % 0.2 < 0.1 else NEON_YELLOW
        
        for i in range(3):
            height_offset = random.randint(1, 5) * 2
            x_offset = random.randint(-2, 2)
            points = [
                (self.width // 2 - thrust_width + x_offset, self.height * 0.6),
                (self.width // 2 + x_offset, self.height * 0.6 + height_offset),
                (self.width // 2 + thrust_width + x_offset, self.height * 0.6)
            ]
            pygame.draw.polygon(self.image, thrust_color, points)
        
        # Digital distortion when in neural buffer (invincible)
        if self.invincible:
            glitch_amount = 3
            glitch_time = pygame.time.get_ticks() % 200
            if glitch_time < 50:  # Create digital glitch effect
                for _ in range(3):
                    x = random.randint(0, self.width - 5)
                    y = random.randint(0, self.height - 2)
                    w = random.randint(5, 15)
                    h = random.randint(1, 3)
                    pygame.draw.rect(self.image, NEON_PURPLE, (x, y, w, h))
            self.image.set_alpha(200)
        else:
            self.image.set_alpha(255)
    
    def update(self):
        """Update player state"""
        # Update timers
        if self.invincible:
            self.invincible_timer -= 1
            if self.invincible_timer <= 0:
                self.invincible = False
        
        if self.shield:
            self.shield_timer -= 1
            if self.shield_timer <= 0:
                self.shield = False
        
        if self.double_shot:
            self.double_shot_timer -= 1
            if self.double_shot_timer <= 0:
                self.double_shot = False
        
        # Update visual appearance
        self.update_image()
    
    def move_left(self):
        """Move player left"""
        self.rect.x -= self.speed
        if self.rect.left < 0:
            self.rect.left = 0
    
    def move_right(self):
        """Move player right"""
        self.rect.x += self.speed
        if self.rect.right > WIDTH:
            self.rect.right = WIDTH
    
    def shoot(self):
        """Create bullets when player shoots"""
        bullets = []
        if self.double_shot:
            # Two bullets side by side
            bullets.append(Bullet(self.rect.left + self.width // 3, self.rect.top))
            bullets.append(Bullet(self.rect.left + self.width * 2 // 3, self.rect.top))
        else:
            # Single bullet
            bullets.append(Bullet(self.rect.centerx, self.rect.top))
        return bullets
    
    def activate_shield(self):
        """Activate shield power-up"""
        self.shield = True
        self.shield_timer = PLAYER_SHIELD_DURATION
    
    def activate_double_shot(self):
        """Activate double shot power-up"""
        self.double_shot = True
        self.double_shot_timer = DOUBLE_SHOT_DURATION
    
    def activate_invincibility(self):
        """Activate temporary invincibility after being hit"""
        self.invincible = True
        self.invincible_timer = PLAYER_INVINCIBLE_DURATION
    
    def hit(self):
        """Handle player being hit"""
        if self.shield:
            self.shield = False
            return True  # Shield absorbed the hit
        
        if not self.invincible:
            self.lives -= 1
            if self.lives > 0:
                self.activate_invincibility()
            return True  # Player was hit
        
        return False  # Player was invincible, no hit registered


class Bullet(pygame.sprite.Sprite):
    """Player data packet sprite - represents the interceptor's data recovery tools"""
    
    def __init__(self, x, y):
        super().__init__()
        self.width = BULLET_WIDTH
        self.height = BULLET_HEIGHT
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        
        # Create digital data packet with pulse animation
        self.creation_time = pygame.time.get_ticks()
        self.update_image()
        
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.bottom = y
        self.speed = BULLET_SPEED
    
    def update_image(self):
        """Update bullet appearance with animated digital effect"""
        self.image.fill((0, 0, 0, 0))  # Clear with transparent
        
        # Digital pulse effect
        time_val = (pygame.time.get_ticks() - self.creation_time) / 200
        pulse = int(math.sin(time_val) * 50) + 200  # Pulsing value between 150-250
        
        # Neon core with digital trail
        pygame.draw.rect(self.image, NEON_TEAL, (0, 0, self.width, self.height))
        pygame.draw.rect(self.image, (pulse, pulse, 255), (1, 1, self.width-2, self.height-2))
    
    def update(self):
        """Move bullet upward"""
        self.rect.y -= self.speed
        # Remove if off screen
        if self.rect.bottom < 0:
            self.kill()


class EnemyBullet(pygame.sprite.Sprite):
    """Corruption packet sprite - digital threats emitted by data fragments"""
    
    def __init__(self, x, y):
        super().__init__()
        self.width = BULLET_WIDTH
        self.height = BULLET_HEIGHT
        self.image = pygame.Surface((self.width + 2, self.height + 2), pygame.SRCALPHA)
        
        # Create corrupted data packet with glitch effect
        self.creation_time = pygame.time.get_ticks()
        self.update_image()
        
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.top = y
        self.speed = BULLET_SPEED * 0.7  # Slightly slower than player packets
    
    def update_image(self):
        """Update bullet appearance with corrupted digital effect"""
        self.image.fill((0, 0, 0, 0))  # Clear with transparent
        
        # Digital corruption effect
        time_val = (pygame.time.get_ticks() - self.creation_time) / 150
        glitch = int(math.sin(time_val * 2) * 30) + 220  # Glitching value
        
        # Corrupted data with jagged edges and unstable core
        pygame.draw.rect(self.image, NEON_RED, (0, 0, self.width + 2, self.height + 2))
        # Unstable core
        if (pygame.time.get_ticks() % 200) < 100:
            core_color = (glitch, 50, 50)
        else:
            core_color = (glitch, glitch, 50)
        pygame.draw.rect(self.image, core_color, (1, 1, self.width, self.height))
    
    def update(self):
        """Move bullet downward"""
        self.rect.y += self.speed
        # Remove if off screen
        if self.rect.top > HEIGHT:
            self.kill()


class Enemy(pygame.sprite.Sprite):
    """Digital data fragment sprite - targets for recovery"""
    
    def __init__(self, x, y):
        super().__init__()
        self.width = ENEMY_WIDTH
        self.height = ENEMY_HEIGHT
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.state = 0  # Evolution state (0-3: from simple to complex)
        self.is_boss = False
        self.birth_time = pygame.time.get_ticks()
        self.rotation_angle = random.randint(0, 359)
        
        # Random color variation to add visual diversity
        self.color_shift = random.randint(-30, 30)
        
        # Update the image
        self.update_image()
    
    def update_image(self):
        """Update the data fragment's visual appearance based on current state"""
        self.image.fill((0, 0, 0, 0))  # Clear with transparent background
        
        # Determine shape complexity and color based on state
        # Higher states are more evolved/complex data
        if self.state == 0:
            # Simple data - basic hexagon shape with minimal detail
            base_color = NEON_TEAL
            num_sides = 6
            detail_level = 0
        elif self.state == 1:
            # Starting to evolve - octagon with inner details
            base_color = NEON_GREEN
            num_sides = 8
            detail_level = 1
        elif self.state == 2:
            # More complex - decagon with multiple layers
            base_color = NEON_YELLOW
            num_sides = 10
            detail_level = 2
        else:  # state 3 (most evolved)
            # Final form - complex with internal structure
            base_color = NEON_ORANGE
            num_sides = 12
            detail_level = 3
        
        # Apply color shift for variety
        r = max(0, min(255, base_color[0] + self.color_shift))
        g = max(0, min(255, base_color[1] + self.color_shift))
        b = max(0, min(255, base_color[2] + self.color_shift))
        color = (r, g, b)
        
        # Digital pulsing effect
        time_val = (pygame.time.get_ticks() - self.birth_time) / 500
        self.rotation_angle = (self.rotation_angle + 0.5) % 360
        pulse = abs(math.sin(time_val)) * 0.3 + 0.7  # Value between 0.7-1.0
        
        # Draw fragment shape
        center = (self.width // 2, self.height // 2)
        outer_radius = int(min(self.width, self.height) // 2 * pulse)
        
        # Draw outer shape
        points = []
        for i in range(num_sides):
            angle = 2 * math.pi * i / num_sides + math.radians(self.rotation_angle)
            x = center[0] + outer_radius * math.cos(angle)
            y = center[1] + outer_radius * math.sin(angle)
            points.append((x, y))
        pygame.draw.polygon(self.image, color, points)
        
        # Add inner details based on complexity level
        if detail_level > 0:
            inner_radius = outer_radius * 0.7
            points = []
            for i in range(num_sides):
                angle = 2 * math.pi * i / num_sides + math.radians(self.rotation_angle + 180/num_sides)
                x = center[0] + inner_radius * math.cos(angle)
                y = center[1] + inner_radius * math.sin(angle)
                points.append((x, y))
            pygame.draw.polygon(self.image, (0, 0, 0), points)
            pygame.draw.polygon(self.image, NEON_PURPLE, points, 1)
        
        if detail_level > 1:
            # Add circuit-like patterns
            for i in range(min(4, detail_level)):
                start_angle = math.radians(random.randint(0, 359))
                line_len = outer_radius * 0.6
                start_pos = (center[0] + math.cos(start_angle) * outer_radius * 0.3,
                            center[1] + math.sin(start_angle) * outer_radius * 0.3)
                end_pos = (start_pos[0] + math.cos(start_angle) * line_len,
                          start_pos[1] + math.sin(start_angle) * line_len)
                pygame.draw.line(self.image, NEON_BLUE, start_pos, end_pos, 1)
        
        if detail_level > 2:
            # Add pulsing center core
            core_radius = int(outer_radius * 0.25 * pulse)
            time_core = (pygame.time.get_ticks() % 1000) / 1000
            core_color = NEON_RED if time_core > 0.5 else NEON_PINK
            pygame.draw.circle(self.image, core_color, center, core_radius)
    
    def hit(self):
        """Handle data fragment being hit"""
        evolution_states = 3  # Total number of states
        if self.state < evolution_states:
            self.state += 1
            self.update_image()
            return False  # Fragment not fully recovered
        else:
            return True  # Fragment fully recovered and collected
    
    def update(self):
        """Update enemy state"""
        pass  # Movement is handled by the game logic


class Boss(Enemy):
    """Firewall Node - powerful system defense mechanism"""
    
    def __init__(self, x, y, level):
        super().__init__(x, y)
        self.width = ENEMY_WIDTH * BOSS_SCALE
        self.height = ENEMY_HEIGHT * BOSS_SCALE
        self.image = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.is_boss = True
        self.health = BOSS_INITIAL_HEALTH + (level // BOSS_LEVEL_INTERVAL) * BOSS_HEALTH_INCREASE_PER_LEVEL
        self.max_health = self.health
        
        # Visual animation variables
        self.phase = 0
        self.outer_ring_rotation = 0
        self.inner_ring_rotation = 0
        self.pulse_time = 0
        self.shield_active = False
        self.shield_flicker = 0
        
        # Level affects appearance
        self.level = level
        self.danger_color = NEON_RED
        self.highlight_color = NEON_YELLOW if level < 10 else NEON_ORANGE if level < 15 else NEON_PURPLE
        
        # Update the image
        self.update_image()
    
    def update_image(self):
        """Update the firewall node's visual appearance"""
        self.image.fill((0, 0, 0, 0))  # Clear with transparent background
        
        center = (self.width // 2, self.height // 2)
        outer_radius = min(self.width, self.height) // 2 - 5
        
        # Update animation values
        time_val = pygame.time.get_ticks() / 1000
        self.pulse_time = (self.pulse_time + 0.02) % 1.0
        self.outer_ring_rotation = (time_val * 20) % 360
        self.inner_ring_rotation = (-time_val * 15) % 360
        
        # Shield effect (activates periodically)
        if time_val % 5 < 2.5:
            self.shield_active = True
            self.shield_flicker = (time_val * 15) % 1.0
        else:
            self.shield_active = False
        
        # Draw base structure - concentric rings
        # Core
        core_radius = outer_radius * 0.2
        pygame.draw.circle(self.image, self.danger_color, center, core_radius)
        
        # Health indicator as digital grid within core
        health_pct = self.health / self.max_health
        health_radius = int(core_radius * health_pct)
        if health_radius > 0:
            health_color = (int(255 * (1-health_pct)), int(255 * health_pct), 100)
            pygame.draw.circle(self.image, health_color, center, health_radius)
        
        # Inner defensive ring - rotating segments
        inner_radius = outer_radius * 0.6
        segments = 8
        for i in range(segments):
            start_angle = math.radians(self.inner_ring_rotation + i * (360/segments))
            end_angle = math.radians(self.inner_ring_rotation + (i+0.6) * (360/segments))
            pygame.draw.arc(self.image, self.highlight_color, 
                          (center[0]-inner_radius, center[1]-inner_radius, inner_radius*2, inner_radius*2),
                          start_angle, end_angle, 5)
        
        # Digital circuit connections
        for i in range(6):
            angle = math.radians(i * 60 + self.outer_ring_rotation/6)
            start_x = center[0] + core_radius * math.cos(angle)
            start_y = center[1] + core_radius * math.sin(angle)
            end_x = center[0] + inner_radius * 0.8 * math.cos(angle)
            end_y = center[1] + inner_radius * 0.8 * math.sin(angle)
            pygame.draw.line(self.image, NEON_BLUE, (start_x, start_y), (end_x, end_y), 2)
        
        # Outer security barrier - hexagonal with security nodes
        points = []
        for i in range(6):
            angle = math.radians(self.outer_ring_rotation/3 + i * 60)
            x = center[0] + outer_radius * math.cos(angle)
            y = center[1] + outer_radius * math.sin(angle)
            points.append((x, y))
            
            # Security nodes at vertices
            node_radius = outer_radius * 0.15
            pygame.draw.circle(self.image, NEON_TEAL, (int(x), int(y)), int(node_radius))
            pygame.draw.circle(self.image, (0,0,0), (int(x), int(y)), int(node_radius*0.7))
            pygame.draw.circle(self.image, self.danger_color, (int(x), int(y)), int(node_radius*0.4))
            
        # Connect the points for outer barrier
        pygame.draw.lines(self.image, NEON_TEAL, True, points, 3)
        
        # Shield effect when active (pulsing hexagonal shield)
        if self.shield_active and self.shield_flicker < 0.7:
            shield_points = []
            shield_radius = outer_radius * 1.2
            for i in range(6):
                angle = math.radians(60 + i * 60)
                x = center[0] + shield_radius * math.cos(angle)
                y = center[1] + shield_radius * math.sin(angle)
                shield_points.append((x, y))
                
            # Semi-transparent shield
            shield_alpha = int(100 + 100 * abs(math.sin(time_val * 5)))
            shield_surface = pygame.Surface((self.width, self.height), pygame.SRCALPHA)
            pygame.draw.polygon(shield_surface, (*NEON_BLUE[:3], shield_alpha), shield_points)
            self.image.blit(shield_surface, (0, 0))
        
        # Draw health bar
        health_width = self.width
        health_height = 10
        health_x = 0
        health_y = -20
        health_percent = self.health / self.max_health
        
        # Background (empty health)
        pygame.draw.rect(self.image, RED, (health_x, health_y, health_width, health_height))
        # Foreground (current health)
        pygame.draw.rect(self.image, GREEN, (health_x, health_y, int(health_width * health_percent), health_height))
    
    def hit(self):
        """Handle boss being hit"""
        self.health -= 1
        self.update_image()
        return self.health <= 0  # Return True if boss is destroyed


class PowerUp(pygame.sprite.Sprite):
    """Power-up sprite"""
    
    def __init__(self, x, y, powerup_type):
        super().__init__()
        self.type = powerup_type
        self.width = POWERUP_SIZE
        self.height = POWERUP_SIZE
        self.image = pygame.Surface((self.width, self.height))
        self.image.fill(POWERUP_COLORS[self.type])
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        self.speed = POWERUP_SPEED
        
        # Draw icon inside
        self.draw_icon()
    
    def draw_icon(self):
        """Draw an icon representing the power-up type"""
        if self.type == "shield":
            pygame.draw.circle(self.image, NEON_CYAN, (self.width // 2, self.height // 2), self.width // 3, 1)
        elif self.type == "double_shot":
            pygame.draw.line(self.image, NEON_CYAN, 
                            (self.width // 3, self.height // 2),
                            (self.width * 2 // 3, self.height // 4), 2)
            pygame.draw.line(self.image, NEON_CYAN, 
                            (self.width // 3, self.height // 2),
                            (self.width * 2 // 3, self.height * 3 // 4), 2)
        elif self.type == "life":
            pygame.draw.polygon(self.image, NEON_CYAN, [
                (self.width // 2, self.height // 4),
                (self.width // 4, self.height * 3 // 4),
                (self.width * 3 // 4, self.height * 3 // 4)
            ])
        elif self.type == "bomb":
            pygame.draw.circle(self.image, NEON_CYAN, (self.width // 2, self.height // 2), self.width // 3)
            # Fuse
            pygame.draw.line(self.image, NEON_CYAN, 
                            (self.width // 2, self.height // 3),
                            (self.width * 2 // 3, 0), 2)
    
    def update(self):
        """Move power-up downward"""
        self.rect.y += self.speed
        # Remove if off screen
        if self.rect.top > HEIGHT:
            self.kill()


class Particle(pygame.sprite.Sprite):
    """Explosion particle sprite"""
    
    def __init__(self, x, y, color):
        super().__init__()
        self.x = x
        self.y = y
        self.size = random.randint(PARTICLE_MIN_SIZE, PARTICLE_MAX_SIZE)
        self.image = pygame.Surface((self.size * 2, self.size * 2), pygame.SRCALPHA)
        pygame.draw.circle(self.image, color, (self.size, self.size), self.size)
        self.rect = self.image.get_rect()
        self.rect.centerx = x
        self.rect.centery = y
        
        # Movement
        angle = random.uniform(0, math.pi * 2)
        speed = random.uniform(PARTICLE_MIN_SPEED, PARTICLE_MAX_SPEED)
        self.dx = math.cos(angle) * speed
        self.dy = math.sin(angle) * speed
        
        # Lifetime
        self.lifetime = random.randint(PARTICLE_MIN_LIFETIME, PARTICLE_MAX_LIFETIME)
    
    def update(self):
        """Update particle position and lifetime"""
        self.x += self.dx
        self.y += self.dy
        self.rect.centerx = int(self.x)
        self.rect.centery = int(self.y)
        
        self.lifetime -= 1
        if self.lifetime <= 0:
            self.kill()


class Star(pygame.sprite.Sprite):
    """Background star sprite"""
    
    def __init__(self):
        super().__init__()
        self.size = random.randint(STAR_MIN_SIZE, STAR_MAX_SIZE)
        self.image = pygame.Surface((self.size, self.size))
        self.image.fill(NEON_CYAN)
        self.rect = self.image.get_rect()
        self.rect.x = random.randint(0, WIDTH)
        self.rect.y = random.randint(0, HEIGHT)
        self.speed = random.uniform(STAR_MIN_SPEED, STAR_MAX_SPEED)
    
    def update(self):
        """Move star downward for parallax effect"""
        self.rect.y += self.speed
        if self.rect.top > HEIGHT:
            self.rect.y = 0
            self.rect.x = random.randint(0, WIDTH)
