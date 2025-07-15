#!/usr/bin/env python3

import time
import subprocess
import platform
import os
from .constants import BROWN_NOISE_FILE, BELL_SOUND_FILE, DEFAULT_VOLUME, AUDIO_TIMEOUT


class AudioPlayer:
    """Handles playing audio notifications for different platforms"""
    
    def __init__(self):
        self.system = platform.system()
        self.audio_dir = os.path.dirname(__file__)
        self.brown_noise_process = None
    
    
    def play_bell_sound(self):
        """Play end notification sound"""
        bell_path = os.path.join(self.audio_dir, BELL_SOUND_FILE)
        
        try:
            if os.path.exists(bell_path):
                if self.system == "Darwin":
                    subprocess.run(["afplay", bell_path], check=True)
                elif self.system == "Linux":
                    subprocess.run(["aplay", bell_path], check=True)
                elif self.system == "Windows":
                    self._play_windows_bell_file(bell_path)
                else:
                    self._play_fallback_bell()
            else:
                self._play_fallback_bell()
        except Exception as e:
            print(f"Audio error: {e}")
            self._play_fallback_bell()
    
    def _play_windows_bell_file(self, bell_path):
        """Play bell sound file on Windows"""
        try:
            import pygame
            pygame.mixer.init()
            sound = pygame.mixer.Sound(bell_path)
            sound.play()
            time.sleep(sound.get_length())
        except ImportError:
            import winsound
            winsound.PlaySound(bell_path, winsound.SND_FILENAME)
    
    def _play_fallback_bell(self):
        """Fallback bell sound using ASCII bell character"""
        for _ in range(3):
            print("\a", end="", flush=True)
            time.sleep(1.0)
    
    def start_brown_noise(self):
        """Start playing brown noise in background"""
        brown_noise_path = os.path.join(self.audio_dir, BROWN_NOISE_FILE)
        
        if not os.path.exists(brown_noise_path):
            print(f"Brown noise file not found: {brown_noise_path}")
            return False
        
        try:
            if self.system == "Darwin":
                self.brown_noise_process = subprocess.Popen(
                    ["afplay", brown_noise_path, "-v", DEFAULT_VOLUME],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
            elif self.system == "Linux":
                self.brown_noise_process = subprocess.Popen(
                    ["mpg123", "-q", brown_noise_path],
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
            elif self.system == "Windows":
                self.brown_noise_process = subprocess.Popen(
                    ["start", "/min", brown_noise_path],
                    shell=True,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
            return True
        except Exception as e:
            print(f"Could not start brown noise: {e}")
            return False
    
    def stop_brown_noise(self):
        """Stop the brown noise playback"""
        if self.brown_noise_process:
            try:
                self.brown_noise_process.terminate()
                self.brown_noise_process.wait(timeout=AUDIO_TIMEOUT)
            except subprocess.TimeoutExpired:
                self.brown_noise_process.kill()
            except Exception:
                pass
            finally:
                self.brown_noise_process = None