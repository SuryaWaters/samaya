#!/usr/bin/env python3

import time
from .audio import AudioPlayer
from .stats import SessionStats
from .constants import SESSION_END_EMOJI


class SessionTimer:
    """Handles timing sessions with different durations"""
    
    SESSION_MODES = {
        'short': 5,      # 5 minutes
        'medium': 15,    # 15 minutes
        'long': 25       # 25 minutes (standard pomodoro)
    }
    
    def __init__(self):
        self.audio_player = AudioPlayer()
        self.stats = SessionStats()
    
    def start_session(self, mode):
        """Start a timer session with the specified mode"""
        if mode not in self.SESSION_MODES:
            print(f"Invalid mode: {mode}")
            print(f"Available modes: {', '.join(self.SESSION_MODES.keys())}")
            return False
        
        duration_minutes = self.SESSION_MODES[mode]
        return self._run_session(mode, duration_minutes)
    
    def start_custom_session(self, duration_minutes):
        """Start a custom timer session with specified duration"""
        if duration_minutes <= 0:
            print("Duration must be greater than 0 minutes")
            return False
        
        return self._run_session('custom', duration_minutes)
    
    def _run_session(self, session_type, duration_minutes):
        """Run a timer session with the specified type and duration"""
        duration_seconds = duration_minutes * 60
        session_display = session_type if session_type != 'custom' else 'custom'
        
        print(f"Starting {session_display} session: {duration_minutes} minutes")
        print("Press Ctrl+C to stop the session early")
        
        self.audio_player.start_brown_noise()
        
        try:
            self._run_timer(duration_seconds)
            print(f"\n{session_display.capitalize()} session complete!")
            print(f"{SESSION_END_EMOJI} Session ended")
            self.audio_player.stop_brown_noise()
            self.audio_player.play_bell_sound()
            self.stats.log_session(session_type, duration_minutes, completed=True)
            return True
            
        except KeyboardInterrupt:
            print(f"\n{session_display.capitalize()} session stopped early.")
            self.audio_player.stop_brown_noise()
            self.stats.log_session(session_type, duration_minutes, completed=False)
            return False
    
    def _run_timer(self, duration_seconds):
        """Run the countdown timer"""
        start_time = time.time()
        
        while True:
            elapsed = time.time() - start_time
            remaining = duration_seconds - elapsed
            
            if remaining <= 0:
                break
            
            minutes_left = int(remaining // 60)
            seconds_left = int(remaining % 60)
            
            print(f"\rTime remaining: {minutes_left:02d}:{seconds_left:02d}", 
                  end="", flush=True)
            time.sleep(1)
    
    def list_modes(self):
        """List available session modes"""
        print("Available session modes:")
        for mode, duration in self.SESSION_MODES.items():
            print(f"  {mode}: {duration} minutes")
    
    def get_mode_duration(self, mode):
        """Get the duration for a specific mode"""
        return self.SESSION_MODES.get(mode)