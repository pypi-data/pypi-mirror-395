#!/usr/bin/env python3
"""
video-bookmarks: A simple video bookmarking tool using mpv
Usage: python video-bookmarks.py <video_file>
Commands (single keypress - no Enter needed):
- b: Create bookmark at current position
- N: Rename the last bookmark
- d: Delete the bookmark before current time (closest one)
- n: Go to next bookmark
- p/SPACE: Go to previous bookmark
- g: Go to bookmark (by number or name)
- <: Shift previous bookmark back by increment and go to it
- >: Shift previous bookmark forward by increment and go to it
- l: List all bookmarks
- +/-: Change motion increment (60s → 10s → 5s → 1s → 0.1s → 0.01s)
- q: Quit and auto-save

Author: Claude
"""

import json
import socket
import subprocess
import sys
import os
import threading
import time
import argparse
import termios
import tty
import atexit
import signal
from datetime import timedelta


class SingleCharInput:
    """Context manager for single character input without buffering"""
    
    def __init__(self):
        self.fd = sys.stdin.fileno()
        self.old_settings = None
    
    def __enter__(self):
        self.old_settings = termios.tcgetattr(self.fd)
        tty.setraw(self.fd)
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.old_settings:
            termios.tcsetattr(self.fd, termios.TCSADRAIN, self.old_settings)
    
    def get_char(self):
        """Get a single character from stdin"""
        return sys.stdin.read(1)


class VideoBookmarks:
    def __init__(self, video_file):
        self.video_file = os.path.abspath(video_file)
        self.socket_path = f"/tmp/mpv-video-bookmarks-{os.getpid()}"
        self.bookmarks = []
        self.current_bookmark_index = -1
        self.mpv_process = None
        self.running = True
        
        # For double-tap detection
        self.last_command = None
        self.last_command_time = 0
        self.double_tap_window = 0.5  # seconds
        
        # Motion increment levels for bookmark adjustments
        self.zoom_levels = [60.0, 10.0, 5.0, 1.0, 0.1, 0.01]  # seconds
        self.current_zoom_index = 3  # Start at 1 second
        
        # Generate bookmarks filename
        video_name = os.path.splitext(os.path.basename(video_file))[0]
        self.bookmarks_file = f"{video_name}.bookmarks"
        
    def start_mpv(self):
        """Start mpv with terminal input disabled"""
        try:
            print(f"Starting mpv with {self.video_file}")
            # Start mpv as a background process
            self.mpv_process = subprocess.Popen([
                'mpv',
                f'--input-ipc-server={self.socket_path}',
                '--no-input-terminal',            # This prevents mpv from reading keyboard input!
                '--keep-open=yes',                # Keep mpv open when video ends
                '--osd-level=1',                 # Show OSD messages
                '--force-window=yes',            # Always create a window
                self.video_file
            ], stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            
            # Wait for mpv to start and socket to be available
            max_attempts = 50
            for _ in range(max_attempts):
                if os.path.exists(self.socket_path):
                    break
                time.sleep(0.1)
            else:
                print("Warning: Socket not found, mpv might not be ready")
                
            print("mpv started successfully in background")
            return True
            
        except FileNotFoundError:
            print("Error: mpv not found. Please install mpv.")
            return False
        except Exception as e:
            print(f"Error starting mpv: {e}")
            return False
    
    def mpv_command(self, command):
        """Send command to mpv via IPC"""
        try:
            sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
            sock.settimeout(1.0)
            sock.connect(self.socket_path)
            sock.send((json.dumps(command) + '\n').encode())
            
            # Read response more carefully
            response_data = sock.recv(4096).decode()
            sock.close()
            
            # Handle multiple JSON objects or extra data
            for line in response_data.strip().split('\n'):
                line = line.strip()
                if line:
                    try:
                        response = json.loads(line)
                        # Return the first valid response
                        if 'error' in response and response['error'] == 'success':
                            return response
                        elif 'data' in response:
                            return response
                    except json.JSONDecodeError:
                        continue
            
            # If no valid response found, try parsing the whole thing
            try:
                return json.loads(response_data.strip().split('\n')[0])
            except (json.JSONDecodeError, IndexError):
                print(f"Warning: Could not parse mpv response: {response_data[:100]}")
                return None
                
        except Exception as e:
            print(f"Error communicating with mpv: {e}")
            return None
    
    def get_current_time(self):
        """Get current playback time in seconds"""
        result = self.mpv_command({"command": ["get_property", "time-pos"]})
        return result.get('data') if result else None
    
    def seek_to_time(self, seconds):
        """Seek to specific time in seconds"""
        return self.mpv_command({"command": ["set_property", "time-pos", seconds]})
    
    def show_osd_message(self, message, duration=3000):
        """Show message on mpv's OSD"""
        self.mpv_command({"command": ["show-text", message, duration]})
    
    def format_time(self, seconds):
        """Format seconds as HH:MM:SS.fff (with consistent zero-padding)"""
        if seconds is None:
            return "00:00:00"
        
        hours = int(seconds // 3600)
        minutes = int((seconds % 3600) // 60)
        secs = seconds % 60
        
        # Always show consistent format with zero-padding
        # Show single decimal place if fractional seconds exist
        if secs != int(secs):
            return f"{hours:02d}:{minutes:02d}:{secs:04.1f}"
        else:
            return f"{hours:02d}:{minutes:02d}:{int(secs):02d}"
    
    def get_current_increment(self):
        """Get current motion increment in seconds"""
        return self.zoom_levels[self.current_zoom_index]
    
    def increase_increment(self):
        """Increase precision (smaller time increments)"""
        if self.current_zoom_index < len(self.zoom_levels) - 1:
            self.current_zoom_index += 1
        
        increment = self.get_current_increment()
        if increment >= 1:
            increment_text = f"{increment:.0f}s"
        else:
            increment_text = f"{increment:.2f}s"
        
        message = f"Motion increment: {increment_text}"
        print(f"\r{message}")
        self.show_osd_message(message)
    
    def decrease_increment(self):
        """Decrease precision (larger time increments)"""
        if self.current_zoom_index > 0:
            self.current_zoom_index -= 1
        
        increment = self.get_current_increment()
        if increment >= 1:
            increment_text = f"{increment:.0f}s"
        else:
            increment_text = f"{increment:.2f}s"
        
        message = f"Motion increment: {increment_text}"
        print(f"\r{message}")
        self.show_osd_message(message)
    
    def show_increment_reminder(self):
        """Show subtle reminder about increment system"""
        increment = self.get_current_increment()
        if increment >= 1:
            increment_text = f"{increment:.0f}s"
        else:
            increment_text = f"{increment:.2f}s"
        
        message = f"Motion increment: {increment_text} (use +/- to change)"
        self.show_osd_message(message, 2000)  # Shorter duration, OSD only

    def shift_and_go_to_previous_bookmark(self, direction):
        """Shift the previous bookmark by current increment and go to it"""
        if not self.bookmarks:
            message = "No bookmarks to shift"
            print(f"\r{message}")
            self.show_osd_message(message)
            return
        
        current_time = self.get_current_time()
        if current_time is None:
            message = "Error: Could not get current time"
            print(f"\r{message}")
            self.show_osd_message(message)
            return
        
        # Find the previous bookmark (same logic as delete_previous_bookmark)
        previous_bookmark = None
        previous_index = -1
        
        for i, bookmark in enumerate(self.bookmarks):
            if bookmark['time'] < current_time:
                if previous_bookmark is None or bookmark['time'] > previous_bookmark['time']:
                    previous_bookmark = bookmark
                    previous_index = i
        
        if previous_bookmark is None:
            message = "No bookmark before current position to shift"
            print(f"\r{message}")
            self.show_osd_message(message)
            return
        
        # Calculate new time
        shift_amount = self.get_current_increment() * direction  # negative for back, positive for forward
        new_time = previous_bookmark['time'] + shift_amount
        
        # Don't allow negative times
        if new_time < 0:
            new_time = 0
        
        # Round to the current increment precision
        increment = self.get_current_increment()
        if increment < 1.0:
            # For sub-second increments, round to that precision
            decimal_places = len(str(increment).split('.')[-1])
            new_time = round(new_time, decimal_places)
        else:
            # For second-level increments, round to whole seconds
            new_time = round(new_time)
        
        # Update the bookmark
        previous_bookmark['time'] = new_time
        previous_bookmark['timestamp'] = self.format_time(new_time)
        
        # Re-sort bookmarks since time changed
        self.bookmarks.sort(key=lambda x: x['time'])
        
        # Auto-save
        self.save_bookmarks(quiet=True)
        
        # Go to the shifted bookmark
        self.seek_to_time(new_time)
        
        # Show feedback
        direction_text = "back" if direction < 0 else "forward"
        increment = self.get_current_increment()
        if increment >= 1:
            increment_text = f"{increment:.0f}s"
        else:
            increment_text = f"{increment:.2f}s"
        
        message = f"Shifted '{previous_bookmark['name']}' {direction_text} {increment_text} to {previous_bookmark['timestamp']}"
        print(f"\r{message}")
        self.show_osd_message(message, 2000)
    
    def _signal_handler(self, signum, frame):
        """Handle signals for graceful shutdown"""
        print(f"\rReceived signal {signum}, shutting down...")
        self.running = False
        self.cleanup()
        sys.exit(0)
    
    def create_bookmark(self, name=None):
        """Create a bookmark at current position"""
        current_time = self.get_current_time()
        if current_time is None:
            message = "Error: Could not get current time"
            print(message)
            self.show_osd_message(message)
            return
        
        if name is None:
            name = f"Bookmark {len(self.bookmarks) + 1}"
        
        bookmark = {
            'name': name,
            'time': current_time,
            'timestamp': self.format_time(current_time)
        }
        
        self.bookmarks.append(bookmark)
        self.bookmarks.sort(key=lambda x: x['time'])  # Keep sorted by time
        
        # Auto-save after creating bookmark
        self.save_bookmarks(quiet=True)
        
        message = f"Created: {name} at {bookmark['timestamp']}"
        print(f"\r{message}")  # \r to overwrite the prompt
        self.show_osd_message(message)
    
    def delete_previous_bookmark(self):
        """Delete the bookmark that's before the current time and closest to it"""
        if not self.bookmarks:
            message = "No bookmarks to delete"
            print(f"\r{message}")
            self.show_osd_message(message)
            return
        
        current_time = self.get_current_time()
        if current_time is None:
            message = "Error: Could not get current time"
            print(f"\r{message}")
            self.show_osd_message(message)
            return
        
        # Find the bookmark that's before current time and closest to it
        previous_bookmark = None
        previous_index = -1
        
        for i, bookmark in enumerate(self.bookmarks):
            if bookmark['time'] < current_time:
                # This bookmark is before current time
                if previous_bookmark is None or bookmark['time'] > previous_bookmark['time']:
                    # This is the closest one to current time so far
                    previous_bookmark = bookmark
                    previous_index = i
        
        if previous_bookmark is None:
            message = "No bookmark before current position"
            print(f"\r{message}")
            self.show_osd_message(message)
            return
        
        # Delete the bookmark
        deleted_bookmark = self.bookmarks.pop(previous_index)
        
        # Auto-save after deleting bookmark
        self.save_bookmarks(quiet=True)
        
        message = f"Deleted: {deleted_bookmark['name']} at {deleted_bookmark['timestamp']}"
        print(f"\r{message}")
        self.show_osd_message(message)
        
        # Update current bookmark index if needed
        if self.current_bookmark_index >= previous_index:
            self.current_bookmark_index -= 1
            if self.current_bookmark_index < 0:
                self.current_bookmark_index = -1
    
    def rename_last_bookmark(self):
        """Give the last created bookmark a custom name"""
        if not self.bookmarks:
            message = "No bookmarks to rename"
            print(f"\r{message}")
            self.show_osd_message(message)
            return
        
        # Get the last bookmark (most recently created)
        last_bookmark = self.bookmarks[-1]
        
        print(f"\rRenaming bookmark: {last_bookmark['name']} at {last_bookmark['timestamp']}")
        print("Enter new name (or press Enter to keep current): ", end="", flush=True)
        
        # Temporarily restore normal terminal mode for text input
        try:
            # Restore terminal settings temporarily
            if hasattr(self, 'old_terminal_settings'):
                termios.tcsetattr(sys.stdin.fileno(), termios.TCSADRAIN, self.old_terminal_settings)
            new_name = input().strip()
            # Set back to raw mode
            if hasattr(self, 'old_terminal_settings'):
                tty.setraw(sys.stdin.fileno())
            
            if new_name:
                # Update the bookmark name
                last_bookmark['name'] = new_name
                
                # Auto-save after renaming bookmark
                self.save_bookmarks(quiet=True)
                
                message = f"Renamed to: {new_name} at {last_bookmark['timestamp']}"
                print(f"\r{message}")
                self.show_osd_message(message)
            else:
                print(f"\rName unchanged")
        except (KeyboardInterrupt, EOFError):
            print(f"\rRename cancelled")
            # Make sure we're back in raw mode
            if hasattr(self, 'old_terminal_settings'):
                tty.setraw(sys.stdin.fileno())
    
    def go_to_bookmark(self, direction):
        """Go to previous (-1) or next (1) bookmark"""
        if not self.bookmarks:
            message = "No bookmarks available"
            print(f"\r{message}")
            self.show_osd_message(message)
            return
        
        current_time = self.get_current_time()
        if current_time is None:
            return
        
        if direction == 1:  # Next bookmark
            for i, bookmark in enumerate(self.bookmarks):
                if bookmark['time'] > current_time + 1:  # +1 second tolerance
                    self.seek_to_time(bookmark['time'])
                    message = f"Next: {bookmark['name']} at {bookmark['timestamp']}"
                    print(f"\r{message}")
                    self.show_osd_message(message)
                    self.current_bookmark_index = i
                    return
            message = "No next bookmark"
            print(f"\r{message}")
            self.show_osd_message(message)
        
        elif direction == -1:  # Previous bookmark
            for i in reversed(range(len(self.bookmarks))):
                bookmark = self.bookmarks[i]
                if bookmark['time'] < current_time - 1:  # -1 second tolerance
                    self.seek_to_time(bookmark['time'])
                    message = f"Previous: {bookmark['name']} at {bookmark['timestamp']}"
                    print(f"\r{message}")
                    self.show_osd_message(message)
                    self.current_bookmark_index = i
                    return
            message = "No previous bookmark"
            print(f"\r{message}")
            self.show_osd_message(message)
    
    def list_bookmarks(self):
        """List all bookmarks"""
        if not self.bookmarks:
            message = "No bookmarks"
            print(f"\r{message}")
            self.show_osd_message(message)
            return
        
        # Temporarily restore normal terminal mode for clean multi-line output
        if hasattr(self, 'old_terminal_settings'):
            termios.tcsetattr(sys.stdin.fileno(), termios.TCSADRAIN, self.old_terminal_settings)
        
        # Clear the current line and print bookmarks nicely
        print("\r" + " " * 80)  # Clear the line
        print("\nBookmarks:")
        print("-" * 50)
        
        # Show on OSD (first few bookmarks)
        osd_lines = []
        for i, bookmark in enumerate(self.bookmarks):
            line = f"{i+1:2}. {bookmark['name']} - {bookmark['timestamp']}"
            print(line)
            if i < 8:  # Show max 8 on OSD to avoid clutter
                osd_lines.append(f"{i+1}. {bookmark['name']} - {bookmark['timestamp']}")
        
        if len(self.bookmarks) > 8:
            remaining = len(self.bookmarks) - 8
            line = f"... and {remaining} more"
            print(line)
            osd_lines.append(line)
        
        print("-" * 50)
        print()  # Add a blank line for better spacing
        
        # Restore raw mode only if we're in the command loop
        if hasattr(self, 'old_terminal_settings'):
            tty.setraw(sys.stdin.fileno())
        
        osd_message = "Bookmarks:\\n" + "\\n".join(osd_lines)
        self.show_osd_message(osd_message, 5000)  # Show for 5 seconds
    
    def go_to_bookmark_by_input(self):
        """Go to bookmark by index number or name"""
        if not self.bookmarks:
            message = "No bookmarks available"
            print(f"\r{message}")
            self.show_osd_message(message)
            return
        
        # Temporarily restore normal terminal mode for text input
        if hasattr(self, 'old_terminal_settings'):
            termios.tcsetattr(sys.stdin.fileno(), termios.TCSADRAIN, self.old_terminal_settings)
        
        print(f"\rGo to bookmark (number 1-{len(self.bookmarks)} or name): ", end="", flush=True)
        
        try:
            user_input = input().strip()
            
            # Set back to raw mode
            if hasattr(self, 'old_terminal_settings'):
                tty.setraw(sys.stdin.fileno())
            
            if not user_input:
                print(f"\rCancelled")
                return
            
            # Try to parse as number first
            try:
                bookmark_num = int(user_input)
                if 1 <= bookmark_num <= len(self.bookmarks):
                    # Valid bookmark number
                    bookmark = self.bookmarks[bookmark_num - 1]
                    self.seek_to_time(bookmark['time'])
                    message = f"Jumped to #{bookmark_num}: {bookmark['name']} at {bookmark['timestamp']}"
                    print(f"\r{message}")
                    self.show_osd_message(message)
                    return
                else:
                    message = f"Invalid number: {bookmark_num} (must be 1-{len(self.bookmarks)})"
                    print(f"\r{message}")
                    self.show_osd_message(message)
                    return
            except ValueError:
                # Not a number, try to find by name
                user_input_lower = user_input.lower()
                
                # Look for exact match first
                for i, bookmark in enumerate(self.bookmarks):
                    if bookmark['name'].lower() == user_input_lower:
                        self.seek_to_time(bookmark['time'])
                        message = f"Jumped to '{bookmark['name']}' at {bookmark['timestamp']}"
                        print(f"\r{message}")
                        self.show_osd_message(message)
                        return
                
                # Look for partial match
                matches = []
                for i, bookmark in enumerate(self.bookmarks):
                    if user_input_lower in bookmark['name'].lower():
                        matches.append((i, bookmark))
                
                if len(matches) == 1:
                    # Single match found
                    bookmark = matches[0][1]
                    self.seek_to_time(bookmark['time'])
                    message = f"Jumped to '{bookmark['name']}' at {bookmark['timestamp']}"
                    print(f"\r{message}")
                    self.show_osd_message(message)
                elif len(matches) > 1:
                    # Multiple matches
                    match_names = [f"'{m[1]['name']}'" for m in matches]
                    message = f"Multiple matches: {', '.join(match_names[:3])}{'...' if len(matches) > 3 else ''}"
                    print(f"\r{message}")
                    self.show_osd_message(message)
                else:
                    # No matches
                    message = f"No bookmark found matching: '{user_input}'"
                    print(f"\r{message}")
                    self.show_osd_message(message)
                    
        except (KeyboardInterrupt, EOFError):
            print(f"\rCancelled")
            # Make sure we're back in raw mode
            if hasattr(self, 'old_terminal_settings'):
                tty.setraw(sys.stdin.fileno())
    
    def save_bookmarks(self, quiet=False):
        """Save bookmarks to JSON file"""
        try:
            with open(self.bookmarks_file, 'w') as f:
                json.dump(self.bookmarks, f, indent=2)
            if not quiet:
                message = f"Saved {len(self.bookmarks)} bookmarks to {self.bookmarks_file}"
                print(f"\r{message}")
                self.show_osd_message(message)
        except Exception as e:
            message = f"Error saving bookmarks: {e}"
            print(f"\r{message}")
            self.show_osd_message(message)
    
    def load_bookmarks(self):
        """Load bookmarks from JSON file"""
        try:
            if os.path.exists(self.bookmarks_file):
                with open(self.bookmarks_file, 'r') as f:
                    self.bookmarks = json.load(f)
                print(f"Loaded {len(self.bookmarks)} bookmarks from {self.bookmarks_file}")
            else:
                print(f"No existing bookmarks file found. Will create {self.bookmarks_file}")
        except Exception as e:
            print(f"Error loading bookmarks: {e}")
    
    def process_command(self, command):
        """Process a user command"""
        # Double-tap detection only for 'p' command
        current_time = time.time()
        is_double_tap_p = (command == 'p' and 
                          self.last_command == 'p' and 
                          current_time - self.last_command_time < self.double_tap_window)
        
        # Update last command tracking
        self.last_command = command
        self.last_command_time = current_time
        
        if command == 'b':
            self.create_bookmark()
        elif command == 'N':  # Capital N to rename last bookmark
            self.rename_last_bookmark()
        elif command == 'd':  # Delete previous bookmark
            self.delete_previous_bookmark()
        elif command == 'n':  # Lowercase n for next bookmark
            self.go_to_bookmark(1)
        elif command == 'p':  # Previous bookmark - check for double-tap
            if is_double_tap_p:
                # Double-tap p: keep going to previous bookmarks
                self.go_to_bookmark(-1)
                self.show_osd_message("Double-tap: continuing previous...", 1000)
            else:
                self.go_to_bookmark(-1)
        elif command == ' ':  # Space - same as p (go to previous bookmark)
            self.go_to_bookmark(-1)
        elif command == 'l':
            self.list_bookmarks()
        elif command == 'g':  # Go to bookmark by index or name
            self.go_to_bookmark_by_input()
        elif command == '+':  # Increase motion increment (finer precision)
            self.increase_increment()
        elif command == '-':  # Decrease motion increment (coarser precision)
            self.decrease_increment()
        elif command == '<':  # Shift previous bookmark back and go to it
            self.shift_and_go_to_previous_bookmark(-1)
        elif command == '>':  # Shift previous bookmark forward and go to it
            self.shift_and_go_to_previous_bookmark(1)
        elif command.lower() == 'q':
            self.quit()
        elif command.lower() == 'h':
            self.show_help()
        elif command == '\x03':  # Ctrl+C
            self.quit()
        elif command == '\x1b':  # ESC
            self.quit()
        else:
            message = f"Unknown command: '{command}' (press 'h' for help)"
            print(f"\r{message}")
    
    def quit(self):
        """Quit the application"""
        self.running = False
        self.save_bookmarks()
        print(f"\rQuitting...")
        if self.mpv_process:
            self.mpv_command({"command": ["quit"]})
    
    def cleanup(self):
        """Cleanup resources"""
        # Restore terminal settings first
        if hasattr(self, 'old_terminal_settings'):
            try:
                termios.tcsetattr(sys.stdin.fileno(), termios.TCSADRAIN, self.old_terminal_settings)
            except:
                pass  # Terminal might already be closed
        
        if self.mpv_process:
            self.mpv_process.terminate()
        
        # Remove socket file
        try:
            os.unlink(self.socket_path)
        except:
            pass
    
    def show_help(self):
        """Show help information"""
        # Temporarily restore normal terminal mode for clean multi-line output
        if hasattr(self, 'old_terminal_settings'):
            termios.tcsetattr(sys.stdin.fileno(), termios.TCSADRAIN, self.old_terminal_settings)
        
        # Clear the current line and display help nicely
        print("\r" + " " * 80)  # Clear the line
        print("\n" + "=" * 50)
        print("VIDEO BOOKMARKS - Commands (single key)")
        print("=" * 50)
        print("b          - Create bookmark")
        print("N          - Rename last bookmark") 
        print("d          - Delete previous bookmark (before current time)")
        print("n          - Go to next bookmark")
        print("p/SPACE    - Go to previous bookmark")
        print("pp         - Double-tap p for rapid previous jumps")
        print("g          - Go to bookmark (by number or name)")
        print("<          - Shift previous bookmark back by increment & go to it")
        print(">          - Shift previous bookmark forward by increment & go to it")
        print("l          - List all bookmarks")
        print("+/-        - Change motion increment (60s → 10s → 5s → 1s → 0.1s → 0.01s)")
        print("q/ESC      - Quit and auto-save")
        print("h          - Show this help")
        print("=" * 50)
        print(f"Bookmarks file: {self.bookmarks_file}")
        print("=" * 50)
        print()  # Add spacing
        
        # Restore raw mode only if we're in the command loop
        if hasattr(self, 'old_terminal_settings'):
            tty.setraw(sys.stdin.fileno())
        
        # Also show on OSD
        osd_help = "Commands: b=bookmark, N=rename, d=delete-prev, n=next, p/SPACE=prev, g=goto, <>=shift&go, +/-=increment, l=list, q=quit"
        self.show_osd_message(osd_help, 4000)
    
    def command_loop(self):
        """Command input loop using single character input"""
        print("\nPress single keys for commands (h for help, q to quit):")
        print("Ready for keystrokes...")
        
        with SingleCharInput() as char_input:
            while self.running:
                try:
                    # Show a simple prompt
                    print("\r> ", end="", flush=True)
                    
                    # Get single character
                    char = char_input.get_char()
                    
                    if not self.running:
                        break
                    
                    self.process_command(char)
                    
                except (KeyboardInterrupt, EOFError):
                    print(f"\rQuitting...")
                    self.quit()
                    break
    
    def monitor_mpv(self):
        """Monitor mpv process in background"""
        while self.running:
            if self.mpv_process and self.mpv_process.poll() is not None:
                print(f"\rmpv has closed - quitting...")
                self.running = False
                break
            time.sleep(0.5)
    
    def run(self):
        """Main application loop"""
        print("Starting video-bookmarks...")
        print("@readwithai 📖 https://readwithai.substack.com/ ⚡️ machine-aided reading ✒️")
        print()
        
        # Store original terminal settings early
        self.old_terminal_settings = termios.tcgetattr(sys.stdin.fileno())
        
        # Register cleanup function to restore terminal on exit
        atexit.register(self.cleanup)
        
        # Set up signal handler for graceful shutdown
        signal.signal(signal.SIGINT, self._signal_handler)
        signal.signal(signal.SIGTERM, self._signal_handler)
        
        # Load existing bookmarks
        self.load_bookmarks()
        
        # Start mpv
        if not self.start_mpv():
            return
        
        try:
            # Show help
            self.show_help()
            
            # Start mpv monitoring in background thread
            monitor_thread = threading.Thread(target=self.monitor_mpv, daemon=True)
            monitor_thread.start()
            
            # Start command loop (this will now work since mpv is backgrounded)
            self.command_loop()
                
        except KeyboardInterrupt:
            print(f"\rInterrupted by user")
        finally:
            self.cleanup()


def main():
    parser = argparse.ArgumentParser(
        description='Video bookmarking tool using mpv',
        epilog="@readwithai 📖 https://readwithai.substack.com/ ⚡️ machine-aided reading ✒️"
    )
    parser.add_argument('video_file', help='Path to video file')
    
    args = parser.parse_args()
    
    if not os.path.exists(args.video_file):
        print(f"Error: Video file '{args.video_file}' not found")
        sys.exit(1)
    
    app = VideoBookmarks(args.video_file)
    app.run()


if __name__ == "__main__":
    main()