import time
import sys
import datetime

class ProgressTracker:
    def __init__(self, total: int, prefix: str = "Progress"):
        self.total = total
        self.prefix = prefix
        self.start_time = time.time()
        self.processed = 0

    def update(self, increment: int = 1):
        self.processed += increment
        self._print_progress()

    def _print_progress(self):
        percent = 100 * (self.processed / float(self.total))
        elapsed_time = time.time() - self.start_time
        avg_time_per_item = elapsed_time / self.processed if self.processed > 0 else 0
        remaining_items = self.total - self.processed
        est_remaining_time = avg_time_per_item * remaining_items
        
        # Format times
        elapsed_str = str(datetime.timedelta(seconds=int(elapsed_time)))
        est_str = str(datetime.timedelta(seconds=int(est_remaining_time)))
        
        bar_length = 30
        filled_length = int(bar_length * self.processed // self.total)
        bar = '█' * filled_length + '-' * (bar_length - filled_length)
        
        sys.stdout.write(f'\r{self.prefix}: |{bar}| {percent:.1f}% [{self.processed}/{self.total}] '
                         f'Elapsed: {elapsed_str} | ETA: {est_str} ')
        sys.stdout.flush()

    def finish(self):
        elapsed_time = time.time() - self.start_time
        elapsed_str = str(datetime.timedelta(seconds=int(elapsed_time)))
        sys.stdout.write(f'\nDone! Total time taken: {elapsed_str}\n')
        sys.stdout.flush()
