import datetime
import os
import shutil
import threading
import time
from typing import Dict, List


class AsyncMultiProcessLogger:
    """A class to handle real-time logging from multiple concurrent async processes using a background thread for display."""

    def __init__(self, clear_screen=True, live_logs=False):
        self.process_logs: Dict[int, List[str]] = {}
        self.process_names: Dict[int, str] = {}
        self.process_status: Dict[int, str] = {}  # 'active', 'completed', 'failed'
        self.transfer_speeds: Dict[int, str] = {}  # Track transfer speeds for each process
        self._lock = threading.Lock()
        self._running = True
        self._display_thread = None
        self.total_registered = 0
        self.total_completed = 0
        self.total_failed = 0
        self._process_id_counter = 0
        self._initialized = False
        self.clear_screen = clear_screen
        if live_logs:
            self._start_display_thread()

    def _start_display_thread(self):
        if not self._initialized:
            self._display_thread = threading.Thread(target=self._display_worker, daemon=True)
            self._display_thread.start()
            self._initialized = True

    def register_process(self, name: str = None) -> int:
        with self._lock:
            self._process_id_counter += 1
            process_id = self._process_id_counter
            self.process_logs[process_id] = []
            self.process_names[process_id] = name or f"Process-{process_id}"
            self.process_status[process_id] = "active"
            self.total_registered += 1
            return process_id

    def deregister_process(self, process_id: int, status: str = "completed"):
        with self._lock:
            if process_id in self.process_logs:
                if status == "completed":
                    self.total_completed += 1
                    # Remove completed processes immediately
                    self.process_logs.pop(process_id, None)
                    self.process_names.pop(process_id, None)
                    self.process_status.pop(process_id, None)
                    self.transfer_speeds.pop(process_id, None)
                elif status == "failed":
                    self.total_failed += 1
                    self.process_status[process_id] = status

    def add_log(self, process_id: int, message: str):
        timestamp = datetime.datetime.now().strftime("%H:%M:%S")
        formatted_message = f"[{timestamp}] {message.strip()}"
        with self._lock:
            if process_id in self.process_logs:
                self.process_logs[process_id].append(formatted_message)
                if len(self.process_logs[process_id]) > 50:
                    self.process_logs[process_id] = self.process_logs[process_id][-50:]
                speed = self._extract_transfer_speed(message)
                if speed:
                    self.transfer_speeds[process_id] = speed

    def _display_worker(self):
        last_update_time = 0
        update_interval = 0.5
        while self._running:
            try:
                current_time = time.time()
                if current_time - last_update_time >= update_interval:
                    self._update_display()
                    last_update_time = current_time
                time.sleep(0.1)
            except Exception as e:
                print(f"Display worker error: {e}")
                import traceback

                traceback.print_exc()

    def _update_display(self):
        with self._lock:
            try:
                terminal_size = shutil.get_terminal_size()
                terminal_width = terminal_size.columns
                terminal_height = terminal_size.lines
            except:
                terminal_width = 80
                terminal_height = 24
            if self.clear_screen:
                try:
                    os.system("cls" if os.name == "nt" else "clear")
                except:
                    print("\n" * 50)
            print("=" * terminal_width)
            print("MULTI-PROCESS RCLONE DOWNLOAD MONITOR (ASYNC-THREADED)")
            print("=" * terminal_width)
            total_active = self.total_registered - self.total_completed - self.total_failed
            print(f"Active processes: {total_active}")
            print(f"Completed processes: {self.total_completed}")
            print(f"Failed processes: {self.total_failed}")
            print(f"Total registered: {self.total_registered}")
            print("=" * terminal_width)
            if not self.process_logs:
                print("No active processes")
                print("Waiting for downloads to start...")
                return
            self._display_tabbed()
            print("\n" + "=" * terminal_width)
            print("Press Ctrl+C to stop monitoring")
            print(f"Last update: {datetime.datetime.now().strftime('%H:%M:%S')}")

    def _display_tabbed(self):
        processes = list(self.process_logs.items())
        total_speed_bps = 0
        for process_id, logs in processes:
            status = self.process_status.get(process_id, "unknown")
            if status == "active":
                speed_str = self.transfer_speeds.get(process_id, None)
                if speed_str:
                    bps = self._parse_speed_to_bps(speed_str)
                    if bps:
                        total_speed_bps += bps
        total_speed_str = self._format_speed(total_speed_bps)
        print(f"\nTotal transfer speed: {total_speed_str}")
        print("\nProcess Summary:")
        for process_id, logs in processes:
            name = self.process_names[process_id]
            status = self.process_status.get(process_id, "unknown")
            speed = self.transfer_speeds.get(process_id, "")
            if status == "failed":
                print(f"  {name} (ID: {process_id}): ❌ Failed")
            elif logs:
                progress_info = self._extract_progress_from_logs(logs[-4:])
                if progress_info:
                    speed_display = f" @ {speed}" if speed else ""
                    print(f"  {name} (ID: {process_id}): 🔄 {progress_info}{speed_display}")
                else:
                    last_log = logs[-1]
                    if len(last_log) > 60:
                        last_log = last_log[:57] + "..."
                    speed_display = f" @ {speed}" if speed else ""
                    print(f"  {name} (ID: {process_id}): 🔄 {last_log}{speed_display}")
            else:
                print(f"  {name} (ID: {process_id}): ⏳ Waiting")
        active_processes = [
            (pid, logs) for pid, logs in processes if self.process_status.get(pid) == "active"
        ]
        if active_processes:
            print("\nDetailed View (Active Processes):")
            for i, (process_id, logs) in enumerate(active_processes[:3]):
                name = self.process_names[process_id]
                speed = self.transfer_speeds.get(process_id, "")
                print(f"\n{name} (ID: {process_id}):")
                if speed:
                    print(f"Transfer Speed: {speed}")
                print("-" * 50)
                for log in logs[-5:]:
                    print(f"  {log}")

    def _extract_transfer_speed(self, message: str) -> str:
        import re

        match = re.search(r"\*\s+[^:]+:\s*\d+%\s*/[^,]+,\s*([^,]+)", message)
        if match:
            return match.group(1).strip()
        match = re.search(r",\s*([^,]+),\s*\d+s", message)
        if match:
            return match.group(1).strip()
        return None

    def _extract_progress_from_logs(self, logs: List[str]) -> str:
        import re

        for log in reversed(logs):
            match = re.search(r"\*\s+([^:]+):\s*(\d+)%\s*/([^,]+)", log)
            if match:
                filename = match.group(1).strip()
                percentage = match.group(2)
                size = match.group(3).strip()
                return f"{percentage}% - {filename} ({size})"
        return None

    def _parse_speed_to_bps(self, speed_str: str) -> float:
        import re

        units = {
            "B/s": 1,
            "KiB/s": 1024,
            "Ki/s": 1024,
            "MiB/s": 1024**2,
            "Mi/s": 1024**2,
            "GiB/s": 1024**3,
            "Gi/s": 1024**3,
            "KB/s": 1000,
            "K/s": 1000,
            "MB/s": 1000**2,
            "M/s": 1000**2,
            "GB/s": 1000**3,
            "G/s": 1000**3,
        }
        match = re.match(r"([\d.]+)\s*([KMGT]?i?B?/s)", speed_str)
        if match:
            value = float(match.group(1))
            unit = match.group(2)
            factor = units.get(unit, 1)
            return value * factor
        return 0.0

    def _format_speed(self, bps: float) -> str:
        if bps >= 1024**3:
            return f"{bps / 1024**3:.2f} GiB/s"
        elif bps >= 1024**2:
            return f"{bps / 1024**2:.2f} MiB/s"
        elif bps >= 1024:
            return f"{bps / 1024:.2f} KiB/s"
        else:
            return f"{bps:.2f} B/s"

    def stop(self):
        self._running = False
        if self._display_thread:
            self._display_thread.join(timeout=1)

    def finalize(self):
        """Print a final summary without clearing the screen."""
        with self._lock:
            print("\n" + "=" * 80)
            print("FINAL SUMMARY (Logger stopped)")
            self._display_tabbed()
            print("=" * 80)
