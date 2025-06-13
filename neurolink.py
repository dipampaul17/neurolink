"""
NeuroLink: Cyberpunk Data Recovery - A cyberpunk-themed arcade game set in digital space.

This game features:
- Data Interceptor that navigates the digital grid with arrow keys
- Digital data fragments that evolve through multiple states
- Firewall Node battles every 5 network levels
- System upgrades and data combo recovery system
- Neon visual effects and digital sound atmosphere

Controls:
- Left/Right Arrow Keys: Navigate data interceptor
- Spacebar: Send data packets
- P: Pause neural connection
- R: Reconnect after system failure
- N: Proceed to next network level after completion
- Q: Exit neural link (when disconnected or level complete)
- M: Toggle audio atmosphere on/off
"""

import pygame
import sys
import random
import math
import os
from config import *
from sprites import *
from sound_manager import SoundManager
from game_state import GameState

class Game:
    """Main game class"""
    
    def __init__(self):
        """Initialize the game"""
        # Initialize pygame
        pygame.init()
        
        # Set up the display
        self.screen = pygame.display.set_mode((WIDTH, HEIGHT))
        pygame.display.set_caption("NeuroLink: Cyberpunk Data Recovery")
        
        # Set up the clock
        self.clock = pygame.time.Clock()
        
        # Initialize sound manager
        self.sound_manager = SoundManager()
        
        # Initialize game state
        self.game_state = GameState(self.sound_manager)
        
        # Set up fonts
        self.font = pygame.font.SysFont(None, 36)
        self.small_font = pygame.font.SysFont(None, 24)
        self.title_font = pygame.font.SysFont(None, 72)
        
        # Game flow control
        self.running = True
        self.show_welcome = True
    
    def handle_events(self):
        """Handle pygame events"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            
            if event.type == pygame.KEYDOWN:
                # Welcome screen - any key to start
                if self.show_welcome:
                    self.show_welcome = False
                    continue
                
                # Pause game
                if event.key == pygame.K_p and not self.game_state.game_over and not self.game_state.game_won:
                    self.game_state.toggle_pause()
                
                # Toggle sound
                if event.key == pygame.K_m:
                    self.sound_manager.toggle_sound()
                
                # Game actions
                if not self.game_state.paused:
                    # Shoot
                    if event.key == pygame.K_SPACE and not self.game_state.game_over and not self.game_state.game_won:
                        self.player_shoot()
                    
                    # Restart after game over
                    if event.key == pygame.K_r and self.game_state.game_over:
                        self.game_state.reset()
                    
                    # Next level after winning
                    if event.key == pygame.K_n and self.game_state.game_won:
                        self.game_state.next_level()
                    
                    # Quit game
                    if event.key == pygame.K_q and (self.game_state.game_over or self.game_state.game_won):
                        self.running = False
                    
                    # Debug: add random powerup
                    if event.key == pygame.K_o:  # Changed from P to O to avoid conflict with pause
                        powerup_type = random.choice(POWERUP_TYPES)
                        powerup = PowerUp(random.randint(50, WIDTH - 50), 50, powerup_type)
                        self.game_state.powerups.add(powerup)
                        self.game_state.all_sprites.add(powerup)
    
    def player_shoot(self):
        """Handle player shooting"""
        bullets = self.game_state.player.shoot()
        for bullet in bullets:
            self.game_state.player_bullets.add(bullet)
            self.game_state.all_sprites.add(bullet)
        
        self.sound_manager.play("shoot")
    
    def enemy_shoot(self):
        """Handle enemy shooting"""
        if not self.game_state.enemies or (not self.game_state.boss_mode and 
                                          random.random() > self.game_state.enemy_shoot_chance):
            return
        
        if self.game_state.boss_mode:
            # Boss shoots more frequently and multiple bullets
            if random.random() < self.game_state.enemy_shoot_chance * BOSS_SHOOT_CHANCE_MULTIPLIER:
                boss = next(iter(self.game_state.enemies))  # Get the boss
                # Shoot 3 bullets in a spread pattern
                for offset in [-20, 0, 20]:
                    bullet = EnemyBullet(
                        boss.rect.centerx + offset,
                        boss.rect.bottom
                    )
                    self.game_state.enemy_bullets.add(bullet)
                    self.game_state.all_sprites.add(bullet)
            return
        
        # Regular enemies - find bottom enemies in each column
        columns = {}
        for enemy in self.game_state.enemies:
            col = int(enemy.rect.centerx / ENEMY_SPACING)
            if col not in columns or enemy.rect.bottom > columns[col].rect.bottom:
                columns[col] = enemy
        
        if columns:
            shooter = random.choice(list(columns.values()))
            bullet = EnemyBullet(shooter.rect.centerx, shooter.rect.bottom)
            self.game_state.enemy_bullets.add(bullet)
            self.game_state.all_sprites.add(bullet)
    
    def move_enemies(self):
        """Move enemies and change direction if needed"""
        gs = self.game_state  # Shorthand
        
        gs.enemy_move_timer += 1
        if gs.enemy_move_timer < gs.enemy_move_delay:
            return
        
        gs.enemy_move_timer = 0
        
        # Boss movement is different
        if gs.boss_mode and gs.enemies:
            boss = next(iter(gs.enemies))  # Get the boss
            boss.rect.x += ENEMY_INITIAL_SPEED * BOSS_MOVE_SPEED_MULTIPLIER * gs.enemy_direction
            
            # Change direction if boss reaches edge
            if (boss.rect.right > WIDTH and gs.enemy_direction > 0) or (boss.rect.left < 0 and gs.enemy_direction < 0):
                gs.enemy_direction *= -1
            
            # Boss occasionally moves down
            if random.random() < BOSS_MOVE_DOWN_CHANCE:
                boss.rect.y += ENEMY_MOVE_DOWN // 2
            
            return
        
        # Check if any enemy has reached the edge
        move_down = False
        for enemy in gs.enemies:
            if (enemy.rect.right + ENEMY_INITIAL_SPEED > WIDTH and gs.enemy_direction > 0) or \
               (enemy.rect.left - ENEMY_INITIAL_SPEED < 0 and gs.enemy_direction < 0):
                move_down = True
                gs.enemy_direction *= -1
                break
        
        # Move enemies
        for enemy in gs.enemies:
            if move_down:
                enemy.rect.y += ENEMY_MOVE_DOWN
                # Make enemies angrier as they descend
                if not enemy.is_boss and enemy.state < len(EMOJI_STATES) - 1 and random.random() < ENEMY_ANGER_CHANCE:
                    enemy.state += 1
                    enemy.update_image()
            enemy.rect.x += ENEMY_INITIAL_SPEED * gs.enemy_direction
    
    def check_collisions(self):
        """Check for collisions between game objects"""
        gs = self.game_state  # Shorthand
        
        # Player bullets hitting enemies
        hits = pygame.sprite.groupcollide(gs.player_bullets, gs.enemies, True, False)
        for bullet, enemies_hit in hits.items():
            for enemy in enemies_hit:
                # Handle hit
                destroyed = enemy.hit()
                
                if enemy.is_boss:
                    gs.score += SCORE_BOSS_HIT
                    gs.create_particles(bullet.rect.centerx, bullet.rect.centery, NEON_RED, 5)
                    self.sound_manager.play("hit")
                    
                    if destroyed:
                        enemy.kill()
                        gs.score += SCORE_BOSS_DESTROY_MULTIPLIER * gs.level
                        gs.create_particles(enemy.rect.centerx, enemy.rect.centery, NEON_RED, PARTICLE_COUNT_EXPLOSION)
                        self.sound_manager.play("explosion")
                else:
                    # Regular enemy
                    if destroyed:
                        gs.score += SCORE_DESTROY * gs.combo_multiplier
                        gs.create_particles(enemy.rect.centerx, enemy.rect.centery, NEON_RED)
                        self.sound_manager.play("hit")
                        enemy.kill()
                        
                        # Chance to drop power-up
                        gs.create_powerup(enemy.rect.centerx, enemy.rect.centery)
                    else:
                        gs.score += SCORE_HIT * gs.combo_multiplier
                        self.sound_manager.play("hit")
                
                # Update combo
                gs.increment_combo()
        
        # Enemy bullets hitting player
        if not gs.player.invincible:
            hits = pygame.sprite.spritecollide(gs.player, gs.enemy_bullets, True)
            if hits:
                hit_registered = gs.player.hit()
                if hit_registered:
                    gs.create_particles(gs.player.rect.centerx, gs.player.rect.centery, NEON_RED)
                    
                    if gs.player.lives <= 0:
                        gs.game_over = True
                        # Update high score
                        if gs.score > gs.high_score:
                            gs.high_score = gs.score
                        self.sound_manager.play("game_over")
                    else:
                        self.sound_manager.play("hit")
        
        # Enemies reaching the bottom or colliding with player
        for enemy in gs.enemies:
            if enemy.rect.bottom >= gs.player.rect.top or pygame.sprite.collide_rect(enemy, gs.player):
                hit_registered = gs.player.hit()
                if hit_registered:
                    enemy.kill()
                    
                    if gs.player.lives <= 0:
                        gs.game_over = True
                        # Update high score
                        if gs.score > gs.high_score:
                            gs.high_score = gs.score
                        self.sound_manager.play("game_over")
                break
        
        # Player collecting power-ups
        hits = pygame.sprite.spritecollide(gs.player, gs.powerups, True)
        for powerup in hits:
            self.apply_powerup(powerup.type)
            self.sound_manager.play("powerup")
        
        # Check if all enemies are destroyed
        if len(gs.enemies) == 0:
            gs.game_won = True
            self.sound_manager.play("level_up")
    
    def apply_powerup(self, powerup_type):
        """Apply the collected power-up effect"""
        gs = self.game_state  # Shorthand
        
        if powerup_type == "shield":
            gs.player.activate_shield()
        elif powerup_type == "double_shot":
            gs.player.activate_double_shot()
        elif powerup_type == "life":
            gs.player.lives = min(PLAYER_MAX_LIVES, gs.player.lives + 1)
        elif powerup_type == "bomb":
            # Destroy all enemies or damage boss
            for enemy in list(gs.enemies):
                if enemy.is_boss:
                    # Damage boss
                    for _ in range(10):  # Damage boss by 10 health
                        if enemy.hit():
                            enemy.kill()
                            gs.score += SCORE_BOSS_DESTROY_MULTIPLIER * gs.level
                            break
                else:
                    # Destroy regular enemy
                    enemy.kill()
                    gs.score += SCORE_BOMB_DESTROY
            
            # Create explosion particles everywhere
            for _ in range(20):
                gs.create_particles(random.randint(0, WIDTH), random.randint(0, HEIGHT), NEON_RED)
            
            self.sound_manager.play("explosion")
    
    def update(self):
        """Update game state"""
        gs = self.game_state  # Shorthand
        
        # Skip updates if paused
        if gs.paused:
            return
        
        # Always update stars for background effect
        gs.stars.update()
        
        # Skip other updates if game over or won
        if gs.game_over or gs.game_won:
            return
        
        # Update player
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            gs.player.move_left()
        if keys[pygame.K_RIGHT]:
            gs.player.move_right()
        
        # Update game objects
        gs.player.update()
        gs.player_bullets.update()
        gs.enemy_bullets.update()
        gs.powerups.update()
        gs.particles.update()
        
        # Update game mechanics
        self.move_enemies()
        self.enemy_shoot()
        self.check_collisions()
        gs.update_combo()
    
    def draw_welcome_screen(self):
        """Draw the cyberpunk welcome screen with dynamic elements"""
        # Create a gradient background
        gradient_surface = pygame.Surface((WIDTH, HEIGHT))
        for y in range(HEIGHT):
            # Create a dark to slightly blue gradient
            color_value = max(5, min(20, int(20 * (1 - y / HEIGHT))))
            gradient_surface.fill((0, color_value, color_value + 10), (0, y, WIDTH, 1))
        self.screen.blit(gradient_surface, (0, 0))
        
        # Draw animated digital grid (subtle cyberpunk circuit pattern)
        current_time = pygame.time.get_ticks() / 1000
        grid_spacing = 40
        grid_offset = int(current_time * 10) % grid_spacing
        grid_alpha = abs(math.sin(current_time)) * 100 + 50
        
        grid_surface = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        for x in range(-grid_offset, WIDTH, grid_spacing):
            # Vertical lines
            alpha = int(grid_alpha * (0.5 + 0.5 * math.sin(x / 100 + current_time)))
            pygame.draw.line(grid_surface, (int(GRID_LINE[0]), int(GRID_LINE[1]), int(GRID_LINE[2]), alpha), (x, 0), (x, HEIGHT), 1)
            
        for y in range(-grid_offset, HEIGHT, grid_spacing):
            # Horizontal lines
            alpha = int(grid_alpha * (0.5 + 0.5 * math.sin(y / 100 + current_time)))
            pygame.draw.line(grid_surface, (int(GRID_LINE[0]), int(GRID_LINE[1]), int(GRID_LINE[2]), alpha), (0, y), (WIDTH, y), 1)
        
        self.screen.blit(grid_surface, (0, 0))
        
        # Draw stars with pulsating effect
        self.game_state.stars.draw(self.screen)
        
        # Draw title with simple animation effect
        title_color = (int(NEON_CYAN[0]), 
                       int(NEON_CYAN[1]), 
                       int(min(255, NEON_CYAN[2] + int(40 * math.sin(current_time * 3)))))
        
        title_text = self.title_font.render("NEUROLINK", True, title_color)
        
        # Position title centrally - accounts for MacBook displays with different resolutions
        title_x = WIDTH // 2 - title_text.get_width() // 2
        title_y = int(HEIGHT * 0.25)  # Adjusted positioning for better MacBook display compatibility
        self.screen.blit(title_text, (title_x, title_y))
        
        # Draw subtitle with a simplified neon effect (avoiding dynamic color issues)
        pulse_value = int(20 * math.sin(current_time * 2 + 1))
        # Use direct RGB values to avoid type issues
        subtitle_color = (255, min(255, 100 + pulse_value), 153)
        subtitle_text = self.font.render("CYBERPUNK DATA RECOVERY", True, subtitle_color)
        
        # Digital glitch effect for subtitle (subtle)
        glitch_offset = int(math.sin(current_time * 10) * 2)  # Small horizontal offset
        subtitle_x = WIDTH // 2 - subtitle_text.get_width() // 2 + glitch_offset
        subtitle_y = title_y + title_text.get_height() + 20
        self.screen.blit(subtitle_text, (subtitle_x, subtitle_y))
        
        # Draw a decorative separator line
        line_width = int(subtitle_text.get_width() * 0.8)
        line_x = WIDTH // 2 - line_width // 2
        line_y = subtitle_y + subtitle_text.get_height() + 20
        
        # Simple animated line
        pygame.draw.line(self.screen, NEON_TEAL, 
                      (line_x, line_y), 
                      (line_x + line_width, line_y), 2)
        
        # Draw instructions with animated colors
        instructions = [
            "Arrow Keys: Navigate Data Interceptor",
            "Spacebar: Send Data Packets",
            "P: Pause Neural Connection",
            "M: Toggle Audio Atmosphere",
            "Collect System Upgrades to enhance your Interceptor",
            "Breach Firewall Nodes every 5 network levels",
            "",
            "Press any key to initiate connection"
        ]
        
        # Position instructions with proper spacing for MacBook displays
        y_pos = line_y + 40
        for idx, instruction in enumerate(instructions):
            # Skip empty lines but maintain spacing
            if not instruction:
                y_pos += 20
                continue
                
            # Special color handling for the last instruction (call to action)
            if idx == len(instructions) - 1:
                # Use yellow for call to action
                inst_text = self.font.render(instruction, True, NEON_YELLOW)
                # Add a simple shadow
                inst_shadow = self.font.render(instruction, True, (30, 30, 40))
                self.screen.blit(inst_shadow, (WIDTH // 2 - inst_text.get_width() // 2 + 2, y_pos + 2))
            else:
                # Normal instructions with slight color variation
                hue_shift = (idx * 30 + current_time * 20) % 100
                inst_color = NEON_TEAL if idx % 2 == 0 else NEON_BLUE
                inst_text = self.small_font.render(instruction, True, inst_color)
            
            # Center text with slight position animation for cyberpunk feel
            inst_x = WIDTH // 2 - inst_text.get_width() // 2
            if idx == len(instructions) - 1:
                # Subtle horizontal motion for call to action
                inst_x += int(math.sin(current_time * 2) * 3)
                
            self.screen.blit(inst_text, (inst_x, y_pos))
            y_pos += 30 if idx != len(instructions) - 2 else 45  # Larger gap before final instruction
        
        # Draw a simple ship logo at the bottom
        icon_y = HEIGHT - 100
        icon_x = WIDTH // 2
        icon_size = 30
        
        # Simple interceptor triangle
        ship_points = [
            (icon_x, icon_y - icon_size),  # Top point
            (icon_x - icon_size, icon_y + icon_size),  # Bottom left
            (icon_x + icon_size, icon_y + icon_size),  # Bottom right
        ]
        
        # Draw interceptor
        pygame.draw.polygon(self.screen, NEON_CYAN, ship_points)
        
        # Simple engine exhaust
        pygame.draw.rect(self.screen, NEON_BLUE, 
                      (icon_x - 10, icon_y + icon_size, 20, 10))
    
    def draw_pause_screen(self):
        """Draw the pause screen overlay"""
        # Semi-transparent overlay
        overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 128))
        self.screen.blit(overlay, (0, 0))
        
        # Pause text
        pause_text = self.title_font.render("PAUSED", True, WHITE)
        continue_text = self.font.render("Press P to continue", True, WHITE)
        
        self.screen.blit(pause_text, (WIDTH // 2 - pause_text.get_width() // 2, HEIGHT // 2 - 50))
        self.screen.blit(continue_text, (WIDTH // 2 - continue_text.get_width() // 2, HEIGHT // 2 + 20))
    
    def draw_game_over_screen(self):
        """Draw the game over screen"""
        self.screen.fill(BLACK)
        
        # Draw stars in background
        self.game_state.stars.draw(self.screen)
        
        game_over_text = self.title_font.render("GAME OVER", True, NEON_RED)
        final_score_text = self.font.render(f"Final Score: {self.game_state.score}", True, NEON_BLUE)
        high_score_text = self.font.render(f"High Score: {self.game_state.high_score}", True, NEON_TEAL)
        restart_text = self.font.render("Press R to restart", True, NEON_TEAL)
        quit_text = self.font.render("Press Q to quit", True, NEON_TEAL)
        
        self.screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - 100))
        self.screen.blit(final_score_text, (WIDTH // 2 - final_score_text.get_width() // 2, HEIGHT // 2 - 30))
        self.screen.blit(high_score_text, (WIDTH // 2 - high_score_text.get_width() // 2, HEIGHT // 2 + 10))
        self.screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 50))
        self.screen.blit(quit_text, (WIDTH // 2 - quit_text.get_width() // 2, HEIGHT // 2 + 80))
    
    def draw_game_won_screen(self):
        """Draw the level complete screen"""
        won_text = self.title_font.render(f"LEVEL {self.game_state.level} COMPLETE!", True, GREEN)
        score_text = self.font.render(f"Score: {self.game_state.score}", True, WHITE)
        next_text = self.font.render("Press N for next level", True, WHITE)
        
        self.screen.blit(won_text, (WIDTH // 2 - won_text.get_width() // 2, HEIGHT // 2 - 80))
        self.screen.blit(score_text, (WIDTH // 2 - score_text.get_width() // 2, HEIGHT // 2 - 30))
        self.screen.blit(next_text, (WIDTH // 2 - next_text.get_width() // 2, HEIGHT // 2 + 20))
    
    def draw_hud(self):
        """Draw heads-up display (score, lives, etc.)"""
        gs = self.game_state  # Shorthand
        
        # Draw score and level
        score_text = self.font.render(f"Score: {gs.score}", True, WHITE)
        level_text = self.font.render(f"Level: {gs.level}", True, WHITE)
        high_score_text = self.font.render(f"High Score: {gs.high_score}", True, WHITE)
        
        self.screen.blit(score_text, (10, 10))
        self.screen.blit(level_text, (WIDTH - level_text.get_width() - 10, 10))
        self.screen.blit(high_score_text, (WIDTH // 2 - high_score_text.get_width() // 2, 10))
        
        # Draw lives
        for i in range(gs.player.lives):
            # Draw small triangles for lives
            points = [
                (30 + i * 25, HEIGHT - 20),  # Top
                (20 + i * 25, HEIGHT - 5),   # Bottom left
                (40 + i * 25, HEIGHT - 5)    # Bottom right
            ]
            pygame.draw.polygon(self.screen, WHITE, points)
        
        # Draw active power-ups
        power_up_y = HEIGHT - 50
        if gs.player.shield:
            shield_text = self.small_font.render("SHIELD", True, BLUE)
            self.screen.blit(shield_text, (WIDTH - shield_text.get_width() - 10, power_up_y))
            power_up_y -= 25
        
        if gs.player.double_shot:
            double_text = self.small_font.render("DOUBLE SHOT", True, YELLOW)
            self.screen.blit(double_text, (WIDTH - double_text.get_width() - 10, power_up_y))
        
        # Draw combo multiplier if active
        if gs.combo_count > 1:
            combo_text = self.font.render(f"Combo x{gs.combo_multiplier}", True, NEON_ORANGE)
            self.screen.blit(combo_text, (WIDTH // 2 - combo_text.get_width() // 2, 50))
        
        # Draw sound status
        sound_status = "ON" if self.sound_manager.enabled else "OFF"
        sound_text = self.small_font.render(f"Sound: {sound_status}", True, WHITE)
        self.screen.blit(sound_text, (10, HEIGHT - 30))
    
    def draw(self):
        """Draw the game screen"""
        self.screen.fill(BLACK)
        
        if self.show_welcome:
            self.draw_welcome_screen()
        else:
            # Draw all sprites
            self.game_state.all_sprites.draw(self.screen)
            
            # Draw HUD
            self.draw_hud()
            
            # Draw game state screens
            if self.game_state.game_over:
                self.draw_game_over_screen()
            elif self.game_state.game_won:
                self.draw_game_won_screen()
            elif self.game_state.paused:
                self.draw_pause_screen()
        
        # Update the display
        pygame.display.flip()
    
    def run(self):
        """Main game loop"""
        while self.running:
            # Handle events
            self.handle_events()
            
            # Update game state
            self.update()
            
            # Draw everything
            self.draw()
            
            # Cap the frame rate
            self.clock.tick(FPS)
        
        # Quit pygame
        pygame.quit()
        sys.exit()


if __name__ == "__main__":
    game = Game()
    game.run()
