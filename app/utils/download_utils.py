class DownloadTimeAverager:
    def __init__(self, window_size: int = 100):
        self.window_size = window_size
        self.times = []

    def update(self, new_time: float) -> float:
        self.times.append(new_time)
        if len(self.times) > self.window_size:
            self.times.pop(0)
        return sum(self.times) / len(self.times)

def calculate_download_time(total_size: int, downloaded: int, speed: float) -> float:
    remaining_size = total_size - downloaded
    return remaining_size / speed if speed > 0 else float('inf')

# ... existing code ...

def update_download_progress(total_size: int, downloaded: int, speed: float, averager: DownloadTimeAverager) -> dict:
    progress = (downloaded / total_size) * 100
    raw_time_remaining = calculate_download_time(total_size, downloaded, speed)
    smoothed_time_remaining = averager.update(raw_time_remaining)
    
    return {
        "progress": f"{progress:.2f}%",
        "downloaded": f"{downloaded / (1024 * 1024):.2f} MB",
        "total_size": f"{total_size / (1024 * 1024):.2f} MB",
        "speed": f"{speed / (1024 * 1024):.2f} MB/s",
        "time_remaining": f"{smoothed_time_remaining:.2f} seconds"
    }

# ... existing code ...