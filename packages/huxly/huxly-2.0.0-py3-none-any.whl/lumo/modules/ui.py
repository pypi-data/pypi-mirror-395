"""
Huxly UI Module — Professional, clean terminal interface with Rich formatting.
Keeps output organized, branded, and easy to work around.
"""
from rich.console import Console
from rich.panel import Panel
from rich.table import Table
from rich.text import Text
from rich.layout import Layout
from rich.align import Align
from datetime import datetime
from typing import Optional, List, Dict, Any


class HuxlyUI:
    """Professional Huxly UI renderer with Rich styling."""
    
    # Huxly Brand Colors
    PRIMARY_COLOR = "cyan"      # Huxly cyan
    ACCENT_COLOR = "bright_yellow"  # Highlights
    SUCCESS_COLOR = "green"     # Good status
    WARNING_COLOR = "yellow"    # Warnings
    ERROR_COLOR = "red"         # Errors
    
    def __init__(self):
        self.console = Console()
        self.session_start = datetime.now()
    
    def print_header(self):
        """Print Huxly branded header."""
        header_text = Text()
        header_text.append("◆ ", style=f"bold {self.PRIMARY_COLOR}")
        header_text.append("HUXLY", style=f"bold {self.PRIMARY_COLOR}")
        header_text.append(" — Professional PC Utility v2.0.0", style="dim white")
        
        panel = Panel(
            Align.center(header_text),
            border_style=self.PRIMARY_COLOR,
            padding=(0, 2),
            title_align="left"
        )
        self.console.print(panel)
    
    def print_status(self, title: str, metrics: Dict[str, Any], icon: str = "●"):
        """Print clean status report."""
        table = Table(title=f"{icon} {title}", show_header=True, 
                     header_style=f"bold {self.PRIMARY_COLOR}")
        table.add_column("Metric", style=self.PRIMARY_COLOR)
        table.add_column("Value", style="cyan")
        table.add_column("Status", style="white")
        
        for metric, data in metrics.items():
            value = data.get('value', 'N/A')
            status = data.get('status', '◆')
            status_color = data.get('color', self.SUCCESS_COLOR)
            
            table.add_row(
                metric,
                str(value),
                Text(status, style=f"bold {status_color}")
            )
        
        self.console.print(table)
        self.console.print()
    
    def print_notification(self, message: str, notification_type: str = "info"):
        """Print AI-generated notification in clean format."""
        icon_map = {
            "info": "ℹ",
            "warning": "⚠",
            "error": "✗",
            "success": "✓",
            "alert": "🔔"
        }
        color_map = {
            "info": self.PRIMARY_COLOR,
            "warning": self.WARNING_COLOR,
            "error": self.ERROR_COLOR,
            "success": self.SUCCESS_COLOR,
            "alert": self.ACCENT_COLOR
        }
        
        icon = icon_map.get(notification_type, "●")
        color = color_map.get(notification_type, self.PRIMARY_COLOR)
        
        notification_text = Text()
        notification_text.append(f"{icon} ", style=f"bold {color}")
        notification_text.append(message, style="white")
        
        panel = Panel(
            notification_text,
            border_style=color,
            padding=(0, 1),
            expand=False
        )
        self.console.print(panel)
    
    def print_welcome(self, username: str):
        """Print personalized welcome screen."""
        welcome_text = Text()
        welcome_text.append("Welcome to ", style="white")
        welcome_text.append("HUXLY", style=f"bold {self.PRIMARY_COLOR}")
        welcome_text.append(f", {username}!", style="white")
        
        subtitle = Text("Your professional PC optimization companion", style="dim white")
        
        layout = Layout()
        layout.split_vertical(
            Layout(Panel(Align.center(welcome_text), border_style=self.PRIMARY_COLOR)),
            Layout(Panel(Align.center(subtitle), border_style="dim white"))
        )
        self.console.print(layout)
        self.console.print()
    
    def print_command_output(self, title: str, content: str, is_json: bool = False):
        """Print command output in clean panel."""
        style = "dim white" if is_json else "white"
        
        panel = Panel(
            Text(content, style=style),
            title=f"◆ {title}",
            title_align="left",
            border_style=self.PRIMARY_COLOR,
            padding=(1, 2)
        )
        self.console.print(panel)
        self.console.print()
    
    def print_progress(self, task: str, percentage: int):
        """Print progress bar (0-100)."""
        bar_length = 30
        filled = int(bar_length * percentage / 100)
        bar = "█" * filled + "░" * (bar_length - filled)
        
        progress_text = Text()
        progress_text.append(f"{task}: ", style="white")
        progress_text.append(f"[{bar}] ", style=f"bold {self.PRIMARY_COLOR}")
        progress_text.append(f"{percentage}%", style=f"bold {self.ACCENT_COLOR}")
        
        self.console.print(progress_text)
    
    def print_error(self, title: str, message: str):
        """Print error in professional format."""
        error_text = Text()
        error_text.append("✗ ", style=f"bold {self.ERROR_COLOR}")
        error_text.append(message, style="white")
        
        panel = Panel(
            error_text,
            title=f"ERROR: {title}",
            title_align="left",
            border_style=self.ERROR_COLOR,
            padding=(0, 2)
        )
        self.console.print(panel)
        self.console.print()
    
    def print_success(self, title: str, message: str = ""):
        """Print success message."""
        success_text = Text()
        success_text.append("✓ ", style=f"bold {self.SUCCESS_COLOR}")
        success_text.append(title, style="white")
        
        if message:
            success_text.append(f"\n{message}", style="dim white")
        
        panel = Panel(
            success_text,
            border_style=self.SUCCESS_COLOR,
            padding=(0, 2)
        )
        self.console.print(panel)
        self.console.print()
    
    def print_separator(self):
        """Print visual separator."""
        line = Text("─" * 50, style=f"dim {self.PRIMARY_COLOR}")
        self.console.print(Align.center(line))
    
    def print_footer(self):
        """Print footer with session info."""
        uptime = (datetime.now() - self.session_start).total_seconds() / 60
        footer_text = Text()
        footer_text.append("Huxly ", style=f"bold {self.PRIMARY_COLOR}")
        footer_text.append("is protecting your system • ", style="dim white")
        footer_text.append(f"Session: {uptime:.0f}m", style="dim white")
        
        panel = Panel(
            Align.center(footer_text),
            border_style=self.PRIMARY_COLOR,
            padding=(0, 2)
        )
        self.console.print(panel)
    
    def clear(self):
        """Clear console."""
        self.console.clear()


# Global UI instance
ui = HuxlyUI()
