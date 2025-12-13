"""Live monitoring for es-translator workers.

This module provides an htop/nvtop-like live monitoring interface for
es-translator Celery workers, showing queue status, translation progress,
and throughput metrics.
"""

import re
import time
from collections import deque
from dataclasses import dataclass, field
from datetime import datetime
from typing import Optional

import plotext as plt
from celery import Celery
from rich import box
from rich.console import Console, ConsoleOptions, RenderResult
from rich.layout import Layout
from rich.live import Live
from rich.panel import Panel
from rich.table import Table
from rich.text import Text

# Valid throughput scale options
THROUGHPUT_SCALES = ('s', 'min', 'h')


def get_throughput_multiplier(scale: str) -> int:
    """Get the multiplier for converting tasks/sec to the given scale.

    Args:
        scale: Time scale - 's' (second), 'min' (minute), or 'h' (hour).

    Returns:
        Multiplier to convert from tasks/sec to the requested scale.

    Examples:
        >>> get_throughput_multiplier('s')
        1
        >>> get_throughput_multiplier('min')
        60
        >>> get_throughput_multiplier('h')
        3600
    """
    return {'s': 1, 'min': 60, 'h': 3600}.get(scale, 1)


def format_throughput(tasks_per_sec: float, scale: str = 's', precision: int = 1) -> str:
    """Format throughput value with the given time scale.

    Args:
        tasks_per_sec: Throughput in tasks per second (base unit).
        scale: Time scale - 's' (second), 'min' (minute), or 'h' (hour).
        precision: Decimal places for formatting.

    Returns:
        Formatted string with value only (no unit suffix).

    Examples:
        >>> format_throughput(2.5, 's')
        '2.5'
        >>> format_throughput(2.5, 'min')
        '150.0'
        >>> format_throughput(0.5, 'h', precision=0)
        '1800'
    """
    value = tasks_per_sec * get_throughput_multiplier(scale)
    return f'{value:.{precision}f}'


def prune_worker_history(history: deque, cutoff_time: float) -> None:
    """Remove entries older than cutoff_time from worker history.

    Args:
        history: Deque of (timestamp, processed_count) tuples.
        cutoff_time: Remove entries with timestamp before this value.

    Examples:
        >>> from collections import deque
        >>> h = deque([(1.0, 10), (2.0, 20), (3.0, 30)])
        >>> prune_worker_history(h, 2.5)
        >>> list(h)
        [(3.0, 30)]
    """
    while history and history[0][0] < cutoff_time:
        history.popleft()


def calculate_worker_throughput(history: deque) -> float:
    """Calculate average throughput from worker history.

    Computes throughput as (newest_count - oldest_count) / time_elapsed.
    This gives a smoothed average over the entire history window.

    Args:
        history: Deque of (timestamp, processed_count) tuples, sorted by time.

    Returns:
        Throughput in tasks per second, or 0.0 if insufficient data.

    Examples:
        >>> from collections import deque
        >>> h = deque([(0.0, 0), (10.0, 50)])
        >>> calculate_worker_throughput(h)
        5.0
        >>> calculate_worker_throughput(deque([(0.0, 0)]))
        0.0
    """
    if not history or len(history) < 2:
        return 0.0

    oldest_time, oldest_count = history[0]
    newest_time, newest_count = history[-1]
    elapsed = newest_time - oldest_time

    if elapsed <= 0:
        return 0.0

    return (newest_count - oldest_count) / elapsed


def format_duration(seconds: float) -> str:
    """Format duration in a human-readable way.

    Args:
        seconds: Duration in seconds.

    Returns:
        Human-readable string like "2d 3h", "5h 30m", "45m", "30s".

    Examples:
        >>> format_duration(0)
        '0s'
        >>> format_duration(45)
        '45s'
        >>> format_duration(3600)
        '1h'
        >>> format_duration(3660)
        '1h 1m'
        >>> format_duration(90061)
        '1d 1h'
    """
    if seconds < 60:
        return f'{int(seconds)}s'

    minutes = int(seconds // 60)
    if minutes < 60:
        return f'{minutes}m'

    hours = int(minutes // 60)
    remaining_minutes = minutes % 60

    if hours < 24:
        if remaining_minutes > 0:
            return f'{hours}h {remaining_minutes}m'
        return f'{hours}h'

    days = hours // 24
    remaining_hours = hours % 24

    if remaining_hours > 0:
        return f'{days}d {remaining_hours}h'
    return f'{days}d'


class ThroughputChart:
    """A Rich renderable that creates a plotext chart sized to fit the available space."""

    def __init__(self, history: list, current: float, avg: float, peak: float, scale: str = 's'):
        """Initialize the chart.

        Args:
            history: List of throughput values in tasks/sec.
            current: Current throughput in tasks/sec.
            avg: Average throughput in tasks/sec.
            peak: Peak throughput in tasks/sec.
            scale: Display scale - 's', 'min', or 'h'.
        """
        self.history = history
        self.current = current
        self.avg = avg
        self.peak = peak
        self.scale = scale

    def __rich_console__(self, console: Console, options: ConsoleOptions) -> RenderResult:
        """Render the chart to fit available space."""
        width = options.max_width
        height = options.height or 10
        height = max(height - 2, 4)  # Account for header line and padding, minimum 4

        # Build content with stats header (values scaled to display unit)
        header = Text()
        header.append(format_throughput(self.current, self.scale, precision=2), style='bold green')
        header.append(' current  ', style='dim')
        header.append(format_throughput(self.avg, self.scale, precision=2), style='bold cyan')
        header.append(' avg  ', style='dim')
        header.append(format_throughput(self.peak, self.scale, precision=2), style='bold yellow')
        header.append(f' peak tasks/{self.scale}', style='dim')

        yield header

        # Create minimalist plotext chart - let plotext auto-scale to fill width
        plt.clear_figure()
        plt.theme('clear')
        plt.plot(self.history, marker='braille')

        plt.plotsize(width, height)
        plt.frame(False)
        plt.xticks([])
        plt.yticks([])
        max_val = self.peak if self.peak > 0 else 1
        plt.ylim(0, max_val)

        # Get the plot as string and strip ANSI codes
        chart_str = plt.build()
        chart_str = re.sub(r'\x1b\[[0-9;]*m', '', chart_str)

        # Add right axis with scale
        chart_lines = chart_str.rstrip('\n').split('\n')
        # Add one empty text to each line for proper Rich rendering
        for line in chart_lines:
            row = Text(line)
            yield row


@dataclass
class MonitorStats:
    """Container for monitoring statistics."""

    # Task-based progress stats
    total_tasks: int = 0
    completed_tasks: int = 0
    pending_tasks: int = 0
    active_tasks: int = 0
    failed_tasks: int = 0

    # Worker stats
    workers: dict = field(default_factory=dict)
    worker_history: dict = field(default_factory=dict)  # dict[str, deque[tuple[float, int]]]

    # Throughput tracking (tasks per interval)
    throughput_history: deque = field(default_factory=lambda: deque(maxlen=300))
    peak_throughput: float = 0.0  # Session peak (not just history window)
    last_completed_count: int = 0
    last_check_time: float = field(default_factory=time.time)

    # Timing
    start_time: float = field(default_factory=time.time)

    # Initial task count (captured at start to calculate total)
    initial_pending: Optional[int] = None


class TranslationMonitor:
    """Live monitoring interface for es-translator workers."""

    def __init__(
        self,
        broker_url: str,
        refresh_interval: float = 2.0,
        history_duration: float = 60.0,
        chart_scale: str = 's',
        worker_scale: str = 'min',
        worker_throughput_lifespan: float = 30.0,
    ):
        """Initialize the monitor.

        Args:
            broker_url: Celery broker URL (Redis).
            refresh_interval: How often to refresh stats (seconds).
            history_duration: Duration of throughput history in seconds (default: 60 = 1 min).
            chart_scale: Throughput scale for chart display ('s', 'min', 'h').
            worker_scale: Throughput scale for worker table ('s', 'min', 'h').
            worker_throughput_lifespan: Duration to average per-worker throughput (seconds).
        """
        self.broker_url = broker_url
        self.refresh_interval = refresh_interval
        self.history_duration = history_duration
        self.chart_scale = chart_scale
        self.worker_scale = worker_scale
        self.worker_throughput_lifespan = worker_throughput_lifespan

        # Calculate number of data points based on duration and refresh interval
        self.history_size = int(history_duration / refresh_interval)

        self.celery_app = Celery('EsTranslator', broker=broker_url)
        self.celery_app.conf.task_default_queue = 'es_translator:default'
        self.console = Console()

        # Initialize stats with properly sized history pre-filled with zeros
        self.stats = MonitorStats(
            throughput_history=deque([0.0] * self.history_size, maxlen=self.history_size)
        )

    def get_celery_stats(self) -> None:
        """Fetch queue and worker stats from Celery/Redis."""
        try:
            inspect = self.celery_app.control.inspect()

            # Get active tasks per worker
            active = inspect.active() or {}
            self.stats.active_tasks = sum(len(tasks) for tasks in active.values())

            # Get reserved (pending) tasks per worker
            reserved = inspect.reserved() or {}
            reserved_count = sum(len(tasks) for tasks in reserved.values())

            # Get queue length from Redis directly for more accurate pending count
            queue_length = 0
            try:
                from redis import Redis

                redis_client = Redis.from_url(self.broker_url)
                queue_length = redis_client.llen('es_translator:default')
            except Exception:
                pass

            self.stats.pending_tasks = queue_length + reserved_count

            # Get worker info and calculate completed tasks
            stats = inspect.stats() or {}
            self.stats.workers = {}
            total_processed = 0

            current_time = time.time()
            cutoff_time = current_time - self.worker_throughput_lifespan

            for worker_name, worker_stats in stats.items():
                worker_active = len(active.get(worker_name, []))
                worker_reserved = len(reserved.get(worker_name, []))
                processed = worker_stats.get('total', {}).get('es_translator.tasks.translate_document_task', 0)
                total_processed += processed

                # Update per-worker history and calculate throughput
                if worker_name not in self.stats.worker_history:
                    self.stats.worker_history[worker_name] = deque()
                history = self.stats.worker_history[worker_name]
                history.append((current_time, processed))
                prune_worker_history(history, cutoff_time)
                worker_throughput = calculate_worker_throughput(history)

                self.stats.workers[worker_name] = {
                    'active': worker_active,
                    'reserved': worker_reserved,
                    'prefetch_count': worker_stats.get('prefetch_count', 0),
                    'processed': processed,
                    'throughput': worker_throughput,
                }

            self.stats.completed_tasks = total_processed

            # Capture initial state on first run
            current_total = self.stats.pending_tasks + self.stats.active_tasks + self.stats.completed_tasks
            if self.stats.initial_pending is None:
                self.stats.initial_pending = current_total
                self.stats.total_tasks = current_total
                # Initialize throughput baseline so first calculation doesn't include
                # all historical completed tasks from before monitoring started
                self.stats.last_completed_count = self.stats.completed_tasks
            else:
                # Total tasks = max of initial or current (in case more tasks are added)
                self.stats.total_tasks = max(self.stats.initial_pending, current_total)

        except Exception as e:
            self.console.print(f'[red]Celery error: {e}[/red]')

    def update_throughput(self) -> None:
        """Calculate and record throughput based on completed tasks."""
        current_time = time.time()
        elapsed = current_time - self.stats.last_check_time

        if elapsed >= self.refresh_interval:
            tasks_completed = self.stats.completed_tasks - self.stats.last_completed_count
            throughput = tasks_completed / elapsed if elapsed > 0 else 0
            self.stats.throughput_history.append(throughput)
            self.stats.peak_throughput = max(self.stats.peak_throughput, throughput)
            self.stats.last_completed_count = self.stats.completed_tasks
            self.stats.last_check_time = current_time

    def create_header(self) -> Panel:
        """Create the header panel."""
        elapsed = time.time() - self.stats.start_time
        hours, remainder = divmod(int(elapsed), 3600)
        minutes, seconds = divmod(remainder, 60)

        title = Text()
        title.append('ES-TRANSLATOR MONITOR', style='bold cyan')
        title.append(f'  |  Uptime: {hours:02d}:{minutes:02d}:{seconds:02d}', style='dim')
        title.append(f'  |  {datetime.now().strftime("%H:%M:%S")}', style='dim')

        return Panel(title, style='cyan')

    def create_status_panel(self) -> Panel:
        """Create the combined queue status and progress panel."""
        total = self.stats.total_tasks if self.stats.total_tasks > 0 else 1
        completed = self.stats.completed_tasks
        remaining = self.stats.pending_tasks + self.stats.active_tasks
        pct = (completed / total) * 100 if total > 0 else 0

        # Calculate throughput stats for ETA
        history = list(self.stats.throughput_history)
        avg_throughput = sum(history) / len(history) if history else 0

        # Calculate ETA
        if avg_throughput > 0:
            eta_seconds = remaining / avg_throughput
            eta_str = format_duration(eta_seconds)
        else:
            eta_str = '--'

        # Calculate elapsed time
        elapsed = time.time() - self.stats.start_time
        elapsed_hours, elapsed_remainder = divmod(int(elapsed), 3600)
        elapsed_minutes, elapsed_secs = divmod(elapsed_remainder, 60)
        elapsed_str = f'{elapsed_hours:02d}:{elapsed_minutes:02d}:{elapsed_secs:02d}'

        # Calculate total processed across all workers
        total_processed = sum(w.get('processed', 0) for w in self.stats.workers.values())

        # Calculate total prefetch count
        total_prefetch = sum(w.get('prefetch_count', 0) for w in self.stats.workers.values())

        # Calculate tasks per hour
        tasks_per_hour = avg_throughput * 3600 if avg_throughput > 0 else 0

        table = Table(show_header=False, box=None, padding=(0, 0), expand=True)
        table.add_column('Metric', style='bold')
        table.add_column('Value', justify='right')

        # Progress info
        table.add_row('Progress', f'[green]{pct:.1f}%[/green]')
        table.add_row('Completed', f'[cyan]{completed:,}[/cyan] / {total:,}')
        table.add_row('Remaining', f'[yellow]{remaining:,}[/yellow]')
        if self.stats.failed_tasks > 0:
            table.add_row('Failed', f'[red]{self.stats.failed_tasks:,}[/red]')
        table.add_row('', '')  # Spacer
        # Queue info
        table.add_row('Pending', f'[yellow]{self.stats.pending_tasks:,}[/yellow]')
        table.add_row('Active', f'[green]{self.stats.active_tasks:,}[/green]')
        table.add_row('Workers', f'[magenta]{len(self.stats.workers):,}[/magenta]')
        if total_prefetch > 0:
            table.add_row('Prefetch', f'[dim]{total_prefetch:,}[/dim]')
        table.add_row('', '')  # Spacer
        # Session stats
        table.add_row('Processed', f'[cyan]{total_processed:,}[/cyan]')
        table.add_row('Rate', f'[dim]{tasks_per_hour:,.0f}/h[/dim]')
        table.add_row('Elapsed', f'[dim]{elapsed_str}[/dim]')
        table.add_row('ETA', f'[dim]{eta_str}[/dim]')

        return Panel(table, title='Status', border_style='green')

    def create_throughput_panel(self) -> Panel:
        """Create the throughput graph panel using plotext."""
        history = list(self.stats.throughput_history)

        if not history:
            return Panel(Text('Collecting data...', style='dim'), title='Throughput', border_style='blue')

        current = history[-1] if history else 0
        avg = sum(history) / len(history) if history else 0

        chart = ThroughputChart(history, current, avg, self.stats.peak_throughput, self.chart_scale)
        return Panel(chart, title='Throughput', border_style='blue')

    def create_workers_panel(self) -> Panel:
        """Create the workers status panel."""
        if not self.stats.workers:
            return Panel(Text('No workers connected', style='yellow'), title='Workers', border_style='magenta')

        table = Table(show_header=True, box=box.SIMPLE_HEAD, padding=(0, 0), pad_edge=False, expand=True)
        table.add_column('Worker', style='cyan')
        table.add_column('Active', justify='center')
        table.add_column('Reserved', justify='center')
        table.add_column('Processed', justify='right')
        table.add_column(f'Tasks/{self.worker_scale}', justify='right')

        for worker_name in sorted(self.stats.workers.keys()):
            info = self.stats.workers[worker_name]
            # Shorten worker name for display
            short_name = worker_name.split('@')[-1] if '@' in worker_name else worker_name
            if len(short_name) > 20:
                short_name = short_name[:17] + '...'

            throughput = format_throughput(info.get('throughput', 0), self.worker_scale)
            table.add_row(
                short_name,
                f'[green]{info["active"]}[/green]',
                f'[yellow]{info["reserved"]}[/yellow]',
                f'{info["processed"]:,}',
                throughput,
            )

        return Panel(table, title='Workers', border_style='magenta')

    def _init_layout(self) -> None:
        """Create and cache the main layout structure."""
        self.layout = Layout()

        self.layout.split(
            Layout(name='header', size=3),
            Layout(name='main'),
            Layout(name='footer', size=3),
        )

        self.layout['main'].split_row(
            Layout(name='status'),
            Layout(name='right', ratio=2),
        )

        self.layout['right'].split(
            Layout(name='workers'),
            Layout(name='throughput'),
        )

        # Footer is static, set it once
        footer = Text()
        footer.append('Press ', style='dim')
        footer.append('Ctrl+C', style='bold')
        footer.append(' to exit  |  ', style='dim')
        footer.append(f'Refresh: {self.refresh_interval}s', style='dim')
        self.layout['footer'].update(Panel(footer, style='dim'))

        # Initialize panels with content to avoid "Layout(name=XXX)" flash
        self._update_panels()

    def refresh_stats(self) -> None:
        """Refresh all statistics."""
        self.get_celery_stats()
        self.update_throughput()

    def _update_panels(self) -> None:
        """Update all dynamic panels with current data."""
        self.layout['header'].update(self.create_header())
        self.layout['status'].update(self.create_status_panel())
        self.layout['workers'].update(self.create_workers_panel())
        self.layout['throughput'].update(self.create_throughput_panel())

    def run(self) -> None:
        """Run the live monitoring interface."""
        self.console.print('[cyan]Starting es-translator monitor...[/cyan]')
        self.console.print(f'[dim]Broker: {self.broker_url}[/dim]')
        self.console.print()

        self._init_layout()

        try:
            with Live(
                self.layout,
                console=self.console,
                refresh_per_second=4,
                screen=True,
            ) as live:
                while True:
                    self.refresh_stats()
                    self._update_panels()
                    live.refresh()
                    time.sleep(self.refresh_interval)
        except KeyboardInterrupt:
            pass  # Exit cleanly without message (screen mode clears it anyway)
