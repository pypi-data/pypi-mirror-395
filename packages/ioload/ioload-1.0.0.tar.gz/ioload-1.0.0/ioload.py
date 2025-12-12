#!/usr/bin/env python3
"""
ioload - A wrapper for iostat that displays I/O statistics in a chart format
similar to nload.
"""

import subprocess
import curses
import time
import threading
import re
import argparse
import sys
import shlex
from collections import deque
from enum import IntEnum
from typing import Dict, List, Optional, Tuple
try:
    import asciichartpy as asciichart
except ImportError:
    asciichart = None

# Constants
MIN_PYTHON_VERSION = (3, 6)
MAX_HISTORY = 60
MIN_INTERVAL = 0.1
MAX_INTERVAL = 60.0
DEFAULT_INTERVAL = 1.0
IOSTAT_TIMEOUT_MULTIPLIER = 2.5
DEVICE_HEADER_TIMEOUT = 5
INITIAL_DATA_WAIT = 1.5
UI_REFRESH_RATE = 0.1
CHART_MAX_HEIGHT = 15
CHART_MAX_WIDTH = 120

# Filtered device prefixes
FILTERED_DEVICE_PREFIXES = ('dm-', 'loop')
FILTERED_DEVICES = {'ram', ''}

# ANSI color codes to curses color pair mapping
ANSI_TO_CURSES_PAIR = {
    34: 1,  # Blue -> pair 1
    31: 2,  # Red -> pair 2
    32: 3,  # Green -> pair 3
}

# Compile regex patterns once for performance
ANSI_PATTERN = re.compile(r'\x1b\[([0-9;]*)m')


class ChartView(IntEnum):
    """Chart view modes."""
    IOPS = 0
    THROUGHPUT = 1
    UTILIZATION = 2
    WAIT_TIMES = 3


class IOStatMonitor:
    """Monitors I/O statistics using iostat and maintains historical data."""
    
    def __init__(self, interval: float = DEFAULT_INTERVAL):
        """Initialize the monitor with a refresh interval."""
        if not MIN_INTERVAL <= interval <= MAX_INTERVAL:
            raise ValueError(f"Interval must be between {MIN_INTERVAL} and {MAX_INTERVAL} seconds")
        self.interval = interval
        self.devices: Dict[str, Dict[str, deque]] = {}
        self.current_device: Optional[str] = None
        self.device_list: List[str] = []
        self.running = False
        self.data_lock = threading.Lock()
        self.max_history = MAX_HISTORY
        self._iostat_cmd = self._detect_iostat_command()
        
    def _detect_iostat_command(self) -> List[str]:
        """Detect the appropriate iostat command for this system."""
        # Try extended format first (Linux)
        try:
            result = subprocess.run(
                ['iostat', '-x', '1', '1'],
                capture_output=True,
                text=True,
                timeout=DEVICE_HEADER_TIMEOUT,
                check=False
            )
            if result.returncode == 0:
                return ['iostat', '-x']
        except (subprocess.TimeoutExpired, FileNotFoundError, OSError):
            pass
        
        # Fall back to basic format (macOS)
        return ['iostat']
    
    def _is_valid_device(self, device: str) -> bool:
        """Check if device should be included in the list."""
        if not device or len(device) == 0:
            return False
        if device in FILTERED_DEVICES:
            return False
        return not any(device.startswith(prefix) for prefix in FILTERED_DEVICE_PREFIXES)
    
    def get_devices(self) -> List[str]:
        """Get list of available block devices."""
        try:
            # Use 2 reports to skip the first one (averages since boot)
            cmd = self._iostat_cmd + ['1', '2']
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=DEVICE_HEADER_TIMEOUT,
                check=False
            )
            
            if result.returncode != 0:
                return []
            
            lines = result.stdout.splitlines()
            devices = set()  # Use set for O(1) lookup
            in_data = False
            device_header_count = 0
            
            for line in lines:
                # Detect Device header line - this marks the start of device data
                if 'Device' in line and 'r/s' in line:
                    device_header_count += 1
                    # Use second report (interval stats)
                    in_data = (device_header_count >= 2)
                    continue
                
                if in_data and line.strip():
                    parts = line.split()
                    if parts:
                        device = parts[0]
                        if self._is_valid_device(device):
                            devices.add(device)
            
            return sorted(devices)
        except (subprocess.TimeoutExpired, subprocess.SubprocessError, OSError):
            return []
        except Exception:
            # Catch-all for unexpected errors
            return []
    
    def parse_iostat(self, output: str) -> Dict[str, Dict[str, float]]:
        """Parse iostat output and extract device statistics."""
        stats = {}
        lines = output.splitlines()
        in_data = False
        has_extended = False
        device_header_count = 0
        
        # Check if we have extended statistics (Linux with -x)
        for line in lines:
            if 'r/s' in line and 'w/s' in line and 'rkB/s' in line:
                has_extended = True
                break
        
        for line in lines:
            # Detect Device header line - this marks the start of device data
            if 'Device' in line and 'r/s' in line:
                device_header_count += 1
                # Skip first report (averages since boot), use second report (interval stats)
                in_data = (device_header_count >= 2)
                continue
            
            if not in_data or not line.strip():
                continue
            
            parts = line.split()
            if not parts:
                continue
            
            device = parts[0]
            # Skip non-physical devices
            if not self._is_valid_device(device):
                continue
            
            try:
                if has_extended and len(parts) >= 23:
                    # Linux extended format - columns: Device r/s rkB/s rrqm/s %rrqm r_await rareq-sz w/s wkB/s wrqm/s %wrqm w_await wareq-sz d/s dkB/s drqm/s %drqm d_await dareq-sz f/s f_await aqu-sz %util
                    stats[device] = {
                        'r/s': float(parts[1]),
                        'w/s': float(parts[7]),
                        'rkB/s': float(parts[2]),
                        'wkB/s': float(parts[8]),
                        'rrqm/s': float(parts[3]),
                        'wrqm/s': float(parts[9]),
                        'r_await': float(parts[5]),
                        'w_await': float(parts[11]),
                        'util': float(parts[22]),
                    }
                elif len(parts) >= 6:
                    # macOS or basic Linux format
                    stats[device] = {
                        'r/s': float(parts[1]) if len(parts) > 1 else 0.0,
                        'w/s': float(parts[2]) if len(parts) > 2 else 0.0,
                        'rkB/s': float(parts[3]) if len(parts) > 3 else 0.0,
                        'wkB/s': float(parts[4]) if len(parts) > 4 else 0.0,
                        'rrqm/s': 0.0,   # not available in basic format
                        'wrqm/s': 0.0,   # not available in basic format
                        'r_await': 0.0,  # not available in basic format
                        'w_await': 0.0,  # not available in basic format
                        'util': float(parts[5]) if len(parts) > 5 else 0.0,
                    }
            except (ValueError, IndexError):
                continue
        
        return stats
    
    def collect_data(self):
        """Continuously collect iostat data."""
        timeout = self.interval * IOSTAT_TIMEOUT_MULTIPLIER
        
        while self.running:
            try:
                # Use interval with count 2 to get the second report (interval stats, not averages since boot)
                interval_int = max(1, int(self.interval))
                cmd = self._iostat_cmd + [str(interval_int), '2']
                
                result = subprocess.run(
                    cmd,
                    capture_output=True,
                    text=True,
                    timeout=timeout,
                    check=False
                )
                
                if result.returncode == 0:
                    stats = self.parse_iostat(result.stdout)
                    
                    with self.data_lock:
                        for device, data in stats.items():
                            if device not in self.devices:
                                self.devices[device] = {
                                    key: deque(maxlen=self.max_history)
                                    for key in data.keys()
                                }
                                # Update device list if empty
                                if not self.device_list:
                                    self.device_list = sorted(stats.keys())
                                    if self.device_list and not self.current_device:
                                        self.current_device = self.device_list[0]
                            
                            for key, value in data.items():
                                self.devices[device][key].append(value)
                
                time.sleep(self.interval)
            except subprocess.TimeoutExpired:
                # iostat took too long, continue
                time.sleep(self.interval)
            except (subprocess.SubprocessError, OSError):
                # Command failed, continue
                time.sleep(self.interval)
            except Exception:
                # Unexpected error, log and continue
                time.sleep(self.interval)
    
    def start(self):
        """Start data collection."""
        self.running = True
        # Get initial device list
        self.device_list = self.get_devices()
        if self.device_list:
            self.current_device = self.device_list[0]
        
        thread = threading.Thread(target=self.collect_data, daemon=True)
        thread.start()
    
    def stop(self):
        """Stop data collection."""
        self.running = False
    
    def get_current_data(self, device: str) -> Optional[Dict[str, deque]]:
        """Get current data for a device."""
        with self.data_lock:
            return self.devices.get(device)
    
    def switch_device(self, direction: int):
        """Switch to next/previous device. direction: 1 for next, -1 for previous."""
        if not self.device_list or direction not in (-1, 1):
            return
        
        with self.data_lock:
            try:
                current_idx = self.device_list.index(self.current_device)
                new_idx = (current_idx + direction) % len(self.device_list)
                self.current_device = self.device_list[new_idx]
            except (ValueError, IndexError):
                # Current device not in list or list changed, use first device
                if self.device_list:
                    self.current_device = self.device_list[0]


def render_colored_line(stdscr, y: int, x: int, text: str, max_width: int) -> None:
    """Render a line with ANSI color codes converted to curses colors."""
    segments = []
    pos = 0
    current_color = None
    
    for match in ANSI_PATTERN.finditer(text):
        # Add text before the ANSI code
        if match.start() > pos:
            segments.append((text[pos:match.start()], current_color))
        
        # Parse the ANSI code
        codes = match.group(1).split(';')
        for code in codes:
            if code:
                try:
                    code_num = int(code)
                    if code_num == 0:  # Reset
                        current_color = None
                    elif code_num in ANSI_TO_CURSES_PAIR:
                        current_color = ANSI_TO_CURSES_PAIR[code_num]
                except ValueError:
                    pass
        
        pos = match.end()
    
    # Add remaining text
    if pos < len(text):
        segments.append((text[pos:], current_color))
    
    # Render segments with colors
    x_pos = x
    has_colors = curses.has_colors()
    
    for segment_text, color_pair in segments:
        if x_pos >= max_width:
            break
        # Truncate segment to fit
        remaining_width = max_width - x_pos
        segment_text = segment_text[:remaining_width]
        if color_pair is not None and has_colors:
            try:
                stdscr.addstr(y, x_pos, segment_text, curses.color_pair(color_pair))
            except curses.error:
                stdscr.addstr(y, x_pos, segment_text)
        else:
            stdscr.addstr(y, x_pos, segment_text)
        x_pos += len(segment_text)


def draw_ascii_chart(stdscr, data_list: List[float], y_pos: int, max_height: int, max_width: int, 
                     color_pair_num: Optional[int] = None, cfg: Optional[dict] = None) -> int:
    """Draw an ASCII chart using asciichartpy library with curses colors."""
    if not data_list:
        return 0
    
    if asciichart is None:
        # Fallback to simple display if library not available
        try:
            stdscr.addstr(y_pos, 0, "Install asciichartpy: pip install asciichartpy")
        except curses.error:
            pass
        return 1
    
    # Prepare chart configuration
    if cfg is None:
        cfg = {}
    
    # Set chart height and limit data width
    chart_height = min(max_height, CHART_MAX_HEIGHT)
    chart_width = min(max_width - 2, len(data_list))
    
    cfg['height'] = chart_height
    
    # Use colors from asciichartpy - we'll convert them to curses colors
    if color_pair_num is not None and asciichart:
        # Map our color pair to asciichart colors
        color_map = {
            1: asciichart.blue,   # Read operations
            2: asciichart.red,     # Write operations
            3: asciichart.green,   # Utilization
        }
        if color_pair_num in color_map:
            cfg['colors'] = [color_map[color_pair_num]]
    
    # Limit data to chart width (use slicing, more efficient than list conversion)
    chart_data = data_list[-chart_width:] if len(data_list) > chart_width else data_list
    
    # Generate chart
    try:
        chart_output = asciichart.plot(chart_data, cfg)
        chart_lines = chart_output.splitlines()
    except Exception:
        return 0
    
    # Display chart line by line with curses colors
    lines_displayed = 0
    
    for i, line in enumerate(chart_lines):
        if y_pos + i >= max_height - 1:
            break
        try:
            # Render line with ANSI codes converted to curses colors
            render_colored_line(stdscr, y_pos + i, 0, line, max_width)
            lines_displayed += 1
        except curses.error:
            # Screen might be too small, skip this line
            break
    
    return lines_displayed


def format_bytes(bytes_per_sec: float) -> str:
    """Format bytes per second to human readable format."""
    if bytes_per_sec < 0:
        bytes_per_sec = 0.0
    
    units = [
        (1024.0 ** 4, "TB/s"),
        (1024.0 ** 3, "GB/s"),
        (1024.0 ** 2, "MB/s"),
        (1024.0, "KB/s"),
        (1.0, "B/s"),
    ]
    
    for divisor, unit in units:
        if bytes_per_sec >= divisor:
            value = bytes_per_sec / divisor
            return f"{value:.2f} {unit}"
    
    return "0.00 B/s"


def main(stdscr, refresh_interval: float = DEFAULT_INTERVAL):
    """Main curses application."""
    # Validate Python version
    if sys.version_info < MIN_PYTHON_VERSION:
        raise RuntimeError(f"Python {MIN_PYTHON_VERSION[0]}.{MIN_PYTHON_VERSION[1]}+ required")
    
    # Initialize curses
    curses.curs_set(0)  # Hide cursor
    stdscr.nodelay(1)   # Non-blocking input
    stdscr.timeout(int(UI_REFRESH_RATE * 1000))  # Refresh rate in milliseconds
    
    # Initialize colors if supported
    if curses.has_colors():
        try:
            curses.start_color()
            # Define color pairs:
            # 1 = Blue (for read operations)
            # 2 = Red (for write operations)
            # 3 = Green (for utilization)
            curses.init_pair(1, curses.COLOR_BLUE, curses.COLOR_BLACK)
            curses.init_pair(2, curses.COLOR_RED, curses.COLOR_BLACK)
            curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_BLACK)
        except curses.error:
            # Colors not available, continue without them
            pass
    
    # Initialize monitor
    try:
        monitor = IOStatMonitor(interval=refresh_interval)
    except ValueError as e:
        stdscr.addstr(0, 0, f"Error: {e}")
        stdscr.refresh()
        time.sleep(2)
        return
    
    monitor.start()
    
    # Chart view modes
    chart_view = ChartView.IOPS
    
    # Wait a bit for initial data
    time.sleep(INITIAL_DATA_WAIT)
    
    try:
        while True:
            # Handle keyboard input
            key = stdscr.getch()
            
            if key == ord('q') or key == ord('Q'):
                break
            elif key == ord('>') or key == curses.KEY_RIGHT:
                monitor.switch_device(1)
            elif key == ord('<') or key == curses.KEY_LEFT:
                monitor.switch_device(-1)
            elif key == curses.KEY_UP:
                chart_view = ChartView((chart_view - 1) % len(ChartView))
            elif key == curses.KEY_DOWN:
                chart_view = ChartView((chart_view + 1) % len(ChartView))
            
            # Clear screen
            stdscr.clear()
            
            # Get current device data
            current_device = monitor.current_device
            if not current_device:
                try:
                    stdscr.addstr(0, 0, "Waiting for device data...")
                    stdscr.refresh()
                except curses.error:
                    pass
                time.sleep(UI_REFRESH_RATE)
                continue
            
            device_data = monitor.get_current_data(current_device)
            if not device_data:
                try:
                    stdscr.addstr(0, 0, f"No data for device: {current_device}")
                    stdscr.refresh()
                except curses.error:
                    pass
                time.sleep(UI_REFRESH_RATE)
                continue
            
            # Get screen dimensions
            try:
                height, width = stdscr.getmaxyx()
            except curses.error:
                time.sleep(UI_REFRESH_RATE)
                continue
            
            # Header
            try:
                device_idx = monitor.device_list.index(current_device) + 1
            except ValueError:
                device_idx = 1
            total_devices = len(monitor.device_list)
            view_names = ["IOPS", "Throughput", "Utilization", "Wait Times"]
            header = f"Device: {current_device} ({device_idx}/{total_devices}) | View: {view_names[chart_view]} | Left/Right: switch device | Up/Down: switch view | Q: quit"
            try:
                stdscr.addstr(0, 0, header[:width-1])
            except curses.error:
                pass
            
            # Calculate chart dimensions - use most of the screen
            chart_height = max(10, height - 8)
            chart_width = min(width - 4, CHART_MAX_WIDTH)
            
            y_pos = 2
            
            # Get data references (avoid repeated lookups)
            rps_data = device_data.get('r/s', deque())
            wps_data = device_data.get('w/s', deque())
            rkb_data = device_data.get('rkB/s', deque())
            wkb_data = device_data.get('wkB/s', deque())
            util_data = device_data.get('util', deque())
            r_await_data = device_data.get('r_await', deque())
            w_await_data = device_data.get('w_await', deque())
            
            if chart_view == ChartView.IOPS:  # IOPS view
                stdscr.addstr(y_pos, 0, "Read/Write IOPS (r/s, w/s)")
                y_pos += 1
                
                if rps_data or wps_data:
                    rps_list = list(rps_data)
                    wps_list = list(wps_data)
                    
                    # Draw read IOPS chart
                    if rps_list:
                        stdscr.addstr(y_pos, 0, "Read IOPS:")
                        y_pos += 1
                        chart_cfg = {'height': chart_height // 2}
                        lines = draw_ascii_chart(stdscr, rps_list, y_pos, chart_height // 2, width, 
                                                color_pair_num=1, cfg=chart_cfg)
                        y_pos += lines + 1
                    
                    # Draw write IOPS chart
                    if wps_list:
                        stdscr.addstr(y_pos, 0, "Write IOPS:")
                        y_pos += 1
                        chart_cfg = {'height': chart_height // 2}
                        lines = draw_ascii_chart(stdscr, wps_list, y_pos, chart_height // 2, width,
                                                color_pair_num=2, cfg=chart_cfg)
                        y_pos += lines + 1
                    
                    rps_current = rps_data[-1] if rps_data else 0.0
                    wps_current = wps_data[-1] if wps_data else 0.0
                    max_iops = max(
                        max(rps_data) if rps_data else 0.0,
                        max(wps_data) if wps_data else 0.0
                    )
                    info = f"Read: {rps_current:.2f} r/s | Write: {wps_current:.2f} w/s | Max: {max_iops:.2f}"
                    stdscr.addstr(y_pos, 0, info[:width-1])
                    y_pos += 1
            
            elif chart_view == ChartView.THROUGHPUT:  # Throughput view
                stdscr.addstr(y_pos, 0, "Read/Write Throughput")
                y_pos += 1
                
                if rkb_data or wkb_data:
                    rkb_list = list(rkb_data)
                    wkb_list = list(wkb_data)
                    
                    # Draw read throughput chart
                    if rkb_list:
                        stdscr.addstr(y_pos, 0, "Read Throughput:")
                        y_pos += 1
                        chart_cfg = {'height': chart_height // 2}
                        lines = draw_ascii_chart(stdscr, rkb_list, y_pos, chart_height // 2, width,
                                                color_pair_num=1, cfg=chart_cfg)
                        y_pos += lines + 1
                    
                    # Draw write throughput chart
                    if wkb_list:
                        stdscr.addstr(y_pos, 0, "Write Throughput:")
                        y_pos += 1
                        chart_cfg = {'height': chart_height // 2}
                        lines = draw_ascii_chart(stdscr, wkb_list, y_pos, chart_height // 2, width,
                                                color_pair_num=2, cfg=chart_cfg)
                        y_pos += lines + 1
                    
                    rkb_current = rkb_data[-1] if rkb_data else 0
                    wkb_current = wkb_data[-1] if wkb_data else 0
                    max_throughput = max(
                        max(rkb_data) if rkb_data else 0,
                        max(wkb_data) if wkb_data else 0
                    )
                    # rkb_data and wkb_data are already in KB/s, convert to bytes/s for format_bytes
                    info = f"Read: {format_bytes(rkb_current * 1024)} | Write: {format_bytes(wkb_current * 1024)} | Max: {format_bytes(max_throughput * 1024)}"
                    stdscr.addstr(y_pos, 0, info[:width-1])
                    y_pos += 1
            
            elif chart_view == ChartView.UTILIZATION:  # Utilization view
                stdscr.addstr(y_pos, 0, "Utilization (%)")
                y_pos += 1
                
                if util_data:
                    util_list = list(util_data)
                    chart_cfg = {'height': chart_height}
                    lines = draw_ascii_chart(stdscr, util_list, y_pos, chart_height, width,
                                            color_pair_num=3, cfg=chart_cfg)
                    y_pos += lines + 1
                    
                    util_current = util_data[-1] if util_data else 0
                    max_util = max(util_data) if util_data else 100.0
                    info = f"Current: {util_current:.2f}% | Max: {max_util:.2f}%"
                    stdscr.addstr(y_pos, 0, info[:width-1])
                    y_pos += 1
            
            elif chart_view == ChartView.WAIT_TIMES:  # Wait Times view
                stdscr.addstr(y_pos, 0, "Read/Write Wait Times (ms)")
                y_pos += 1
                
                if r_await_data or w_await_data:
                    r_await_list = list(r_await_data)
                    w_await_list = list(w_await_data)
                    
                    # Draw read wait times chart
                    if r_await_list:
                        stdscr.addstr(y_pos, 0, "Read Wait Time:")
                        y_pos += 1
                        chart_cfg = {'height': chart_height // 2}
                        lines = draw_ascii_chart(stdscr, r_await_list, y_pos, chart_height // 2, width,
                                                color_pair_num=1, cfg=chart_cfg)
                        y_pos += lines + 1
                    
                    # Draw write wait times chart
                    if w_await_list:
                        stdscr.addstr(y_pos, 0, "Write Wait Time:")
                        y_pos += 1
                        chart_cfg = {'height': chart_height // 2}
                        lines = draw_ascii_chart(stdscr, w_await_list, y_pos, chart_height // 2, width,
                                                color_pair_num=2, cfg=chart_cfg)
                        y_pos += lines + 1
                    
                    r_await_current = r_await_data[-1] if r_await_data else 0
                    w_await_current = w_await_data[-1] if w_await_data else 0
                    max_wait = max(
                        max(r_await_data) if r_await_data else 0,
                        max(w_await_data) if w_await_data else 0
                    )
                    info = f"Read Wait: {r_await_current:.2f}ms | Write Wait: {w_await_current:.2f}ms | Max: {max_wait:.2f}ms"
                    stdscr.addstr(y_pos, 0, info[:width-1])
                    y_pos += 1
            
            # Footer with quick stats
            footer_y = height - 1
            if footer_y > 0:
                rps_current = rps_data[-1] if rps_data else 0
                wps_current = wps_data[-1] if wps_data else 0
                rkb_current = rkb_data[-1] if rkb_data else 0
                wkb_current = wkb_data[-1] if wkb_data else 0
                util_current = util_data[-1] if util_data else 0
                footer = f"IOPS: R:{rps_current:.1f} W:{wps_current:.1f} | Thru: R:{format_bytes(rkb_current*1024)} W:{format_bytes(wkb_current*1024)} | Util:{util_current:.1f}%"
                stdscr.addstr(footer_y, 0, footer[:width-1])
            
            try:
                stdscr.refresh()
            except curses.error:
                pass
            time.sleep(UI_REFRESH_RATE)
    
    except KeyboardInterrupt:
        pass
    finally:
        monitor.stop()


def cli():
    """Command-line interface entry point."""
    parser = argparse.ArgumentParser(
        description='Display I/O statistics in a real-time chart format',
        formatter_class=argparse.RawDescriptionHelpFormatter
    )
    parser.add_argument(
        '-i', '--interval',
        type=float,
        default=DEFAULT_INTERVAL,
        help=f'Refresh interval in seconds (default: {DEFAULT_INTERVAL}, min: {MIN_INTERVAL}, max: {MAX_INTERVAL})'
    )
    
    args = parser.parse_args()
    
    # Validate interval
    if not MIN_INTERVAL <= args.interval <= MAX_INTERVAL:
        print(f"Error: Interval must be between {MIN_INTERVAL} and {MAX_INTERVAL} seconds", file=sys.stderr)
        sys.exit(1)
    
    try:
        curses.wrapper(lambda stdscr: main(stdscr, args.interval))
    except KeyboardInterrupt:
        pass
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == '__main__':
    cli()

