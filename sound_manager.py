"""
Sound manager for NeuroLink: Cyberpunk Data Recovery game.
Handles loading and playing digital audio effects for the cyberpunk atmosphere.
"""

import pygame
import os
from config import SOUND_VOLUME

class SoundManager:
    """Manages game audio effects for the cyberpunk atmosphere"""
    
    def __init__(self):
        """Initialize the sound manager"""
        self.sounds = {}
        self.enabled = True
        self.load_sounds()
    
    def load_sounds(self):
        """Load all game sound effects"""
        try:
            # Load sound files
            self.sounds["shoot"] = pygame.mixer.Sound(os.path.join("sounds", "Space Shooter SFX by edwardszakal.wav"))
            self.sounds["hit"] = pygame.mixer.Sound(os.path.join("sounds", "Space Shooter SFX by edwardszakal.wav"))
            self.sounds["game_over"] = pygame.mixer.Sound(os.path.join("sounds", "Game Over 02 Voices by LilMati.wav"))
            self.sounds["powerup"] = pygame.mixer.Sound(os.path.join("sounds", "Bouncing Power Up 1_2 by Joao Janz.wav"))
            self.sounds["explosion"] = pygame.mixer.Sound(os.path.join("sounds", "Space Explosion by Morgan Purkis.wav"))
            self.sounds["level_up"] = pygame.mixer.Sound(os.path.join("sounds", "Level Up Mission Complete by Beetlemuse.wav"))
            
            # Set volume levels
            for sound_name, volume in SOUND_VOLUME.items():
                if sound_name in self.sounds:
                    self.sounds[sound_name].set_volume(volume)
            
            print("Sound files loaded successfully!")
        except Exception as e:
            print(f"Warning: Error loading sound files. Game will run without sound. Error: {e}")
            self.enabled = False
    
    def play(self, sound_name):
        """Play a sound effect by name"""
        if not self.enabled or sound_name not in self.sounds:
            return
        
        self.sounds[sound_name].play()
    
    def play_segment(self, sound_name, start_time, duration, volume=None):
        """
        Play a specific segment from a sound file
        
        Args:
            sound_name: Name of the sound in the sounds dictionary
            start_time: Start time in seconds
            duration: Duration to play in seconds
            volume: Optional volume override (0.0 to 1.0)
        """
        if not self.enabled or sound_name not in self.sounds:
            return
        
        # Create a temporary channel for this sound
        channel = pygame.mixer.find_channel(True)
        if channel:
            # Set the volume
            if volume is not None:
                channel.set_volume(volume)
            else:
                channel.set_volume(SOUND_VOLUME.get(sound_name, 0.5))
            
            # Play the sound
            channel.play(self.sounds[sound_name])
    
    def toggle_sound(self):
        """Toggle sound on/off"""
        self.enabled = not self.enabled
        return self.enabled
