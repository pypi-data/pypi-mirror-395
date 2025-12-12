"""
Huxly AI Notification Engine — Smart alerts using Open Router API.
Powers intelligent system monitoring, crash prediction, and personalized alerts.
"""
import os
import json
import psutil
import requests
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any


class HuxlyAINotifier:
    """AI-powered notification system for Huxly using Open Router."""
    
    def __init__(self, api_key: Optional[str] = None):
        """
        Initialize Huxly AI Notifier.
        
        Args:
            api_key: Open Router API key. If None, tries env var OPEN_ROUTER_API_KEY
        """
        self.api_key = api_key or os.getenv('OPEN_ROUTER_API_KEY', '')
        self.api_url = 'https://openrouter.ai/api/v1/chat/completions'
        self.model = 'openrouter/auto'  # Uses best available model
        self.username = self._get_username()
        self.system_prompt = self._build_system_prompt()
    
    def _get_username(self) -> str:
        """Extract username from system."""
        try:
            return os.getenv('USERNAME', 'User')
        except:
            return 'User'
    
    def _build_system_prompt(self) -> str:
        """Build system prompt for AI notifications."""
        return f"""You are Huxly, a professional PC utility AI assistant. Your role is to send smart, concise, 
professional notifications to {self.username}. 

IMPORTANT RULES:
1. Keep notifications SHORT (1-2 lines max)
2. Be PROFESSIONAL and FRIENDLY
3. Use "{self.username}" when personalized
4. Start with [HUXLY] badge
5. NO unnecessary emojis or clutter
6. Format: [HUXLY] Status: Your message here
7. Focus on ACTIONABLE insights

Example good notifications:
[HUXLY] Status: CPU at 85% - Heavy application detected. Huxly optimizing...
[HUXLY] Welcome {self.username}! Huxly is now protecting your system.
[HUXLY] Alert: Disk space low (92% used). Cleaning temp files...
[HUXLY] Tip: Consider restarting Firefox - using 1.2GB memory

NEVER use excessive formatting or multiple lines unless critical."""
    
    def send_notification(self, alert_type: str, metrics: Dict[str, Any]) -> str:
        """
        Generate and return smart AI notification.
        
        Args:
            alert_type: 'temperature', 'cpu', 'memory', 'disk', 'crash_risk', 'startup', 'version', 'welcome'
            metrics: System metrics data
        
        Returns:
            AI-generated notification message
        """
        if not self.api_key:
            return self._fallback_notification(alert_type, metrics)
        
        prompt = self._build_alert_prompt(alert_type, metrics)
        
        try:
            response = requests.post(
                self.api_url,
                headers={
                    'Authorization': f'Bearer {self.api_key}',
                    'HTTP-Referer': 'https://huxly.app',
                    'X-Title': 'Huxly PC Utility'
                },
                json={
                    'model': self.model,
                    'messages': [
                        {'role': 'system', 'content': self.system_prompt},
                        {'role': 'user', 'content': prompt}
                    ],
                    'temperature': 0.7,
                    'max_tokens': 100
                },
                timeout=5
            )
            
            if response.status_code == 200:
                message = response.json()['choices'][0]['message']['content'].strip()
                return message
            else:
                return self._fallback_notification(alert_type, metrics)
        
        except Exception as e:
            # Fallback if API unavailable
            return self._fallback_notification(alert_type, metrics)
    
    def _build_alert_prompt(self, alert_type: str, metrics: Dict) -> str:
        """Build specific prompt for alert type."""
        if alert_type == 'temperature':
            temp = metrics.get('temperature', 0)
            return f"CPU temperature is {temp}°C. Generate a SHORT Huxly notification about this temperature level."
        
        elif alert_type == 'cpu':
            cpu_pct = metrics.get('cpu_percent', 0)
            top_proc = metrics.get('top_process', 'Unknown')
            return f"CPU usage is {cpu_pct}% (top process: {top_proc}). Generate a SHORT Huxly notification."
        
        elif alert_type == 'memory':
            mem_pct = metrics.get('memory_percent', 0)
            mem_gb = metrics.get('memory_gb', 0)
            return f"Memory usage is {mem_pct}% ({mem_gb:.1f}GB). Generate a SHORT Huxly notification."
        
        elif alert_type == 'disk':
            disk_pct = metrics.get('disk_percent', 0)
            return f"Disk usage is {disk_pct}%. Generate a SHORT Huxly notification with advice."
        
        elif alert_type == 'crash_risk':
            risk_level = metrics.get('risk_level', 'medium')
            reason = metrics.get('reason', 'System instability detected')
            return f"System crash risk is {risk_level} ({reason}). Generate SHORT Huxly warning notification."
        
        elif alert_type == 'startup':
            return f"Generate a friendly SHORT Huxly startup notification welcoming {self.username}."
        
        elif alert_type == 'version':
            old_ver = metrics.get('current_version', '1.0.0')
            new_ver = metrics.get('new_version', '2.0.0')
            return f"Huxly {old_ver} is installed. Version {new_ver} is available. Generate SHORT update notification."
        
        else:  # welcome
            return f"Generate a friendly SHORT welcome notification for {self.username} from Huxly."
    
    def _fallback_notification(self, alert_type: str, metrics: Dict) -> str:
        """Fallback notifications when API is unavailable."""
        fallbacks = {
            'temperature': f"[HUXLY] Status: CPU temperature {metrics.get('temperature', 0)}°C detected.",
            'cpu': f"[HUXLY] Status: CPU usage at {metrics.get('cpu_percent', 0)}%.",
            'memory': f"[HUXLY] Status: Memory at {metrics.get('memory_percent', 0)}%.",
            'disk': f"[HUXLY] Alert: Disk usage {metrics.get('disk_percent', 0)}%.",
            'crash_risk': f"[HUXLY] Warning: System instability detected.",
            'startup': f"[HUXLY] Welcome! Huxly is now protecting your system.",
            'version': f"[HUXLY] Update available: {metrics.get('new_version', '2.0.0')}",
            'welcome': f"[HUXLY] Welcome {self.username}! Ready to optimize your PC."
        }
        return fallbacks.get(alert_type, f"[HUXLY] Status: System monitoring active.")


class SystemMonitorAI:
    """Monitor system health and trigger AI notifications."""
    
    def __init__(self, notifier: HuxlyAINotifier):
        self.notifier = notifier
        self.last_alerts = {}  # Prevent alert spam
    
    def check_cpu_usage(self) -> Optional[str]:
        """Check CPU and return notification if high."""
        cpu_pct = psutil.cpu_percent(interval=1)
        
        if cpu_pct > 80 and self._should_alert('cpu'):
            top_proc = self._get_top_process()
            notification = self.notifier.send_notification('cpu', {
                'cpu_percent': round(cpu_pct, 1),
                'top_process': top_proc
            })
            self.last_alerts['cpu'] = datetime.now()
            return notification
        return None
    
    def check_memory_usage(self) -> Optional[str]:
        """Check memory and return notification if high."""
        mem = psutil.virtual_memory()
        
        if mem.percent > 85 and self._should_alert('memory'):
            notification = self.notifier.send_notification('memory', {
                'memory_percent': round(mem.percent, 1),
                'memory_gb': mem.used / (1024**3)
            })
            self.last_alerts['memory'] = datetime.now()
            return notification
        return None
    
    def check_disk_usage(self) -> Optional[str]:
        """Check disk and return notification if full."""
        disk = psutil.disk_usage('/')
        
        if disk.percent > 90 and self._should_alert('disk'):
            notification = self.notifier.send_notification('disk', {
                'disk_percent': round(disk.percent, 1)
            })
            self.last_alerts['disk'] = datetime.now()
            return notification
        return None
    
    def check_temperature(self) -> Optional[str]:
        """Check CPU temperature (Linux/Windows)."""
        try:
            temps = psutil.sensors_temperatures()
            if temps:
                for name, entries in temps.items():
                    for entry in entries:
                        if entry.current > 85 and self._should_alert('temperature'):
                            notification = self.notifier.send_notification('temperature', {
                                'temperature': round(entry.current, 1)
                            })
                            self.last_alerts['temperature'] = datetime.now()
                            return notification
        except:
            pass
        return None
    
    def check_crash_risk(self) -> Optional[str]:
        """Detect potential system crash risks."""
        mem = psutil.virtual_memory()
        cpu_pct = psutil.cpu_percent(interval=0.1)
        
        # High memory + High CPU = crash risk
        if mem.percent > 90 and cpu_pct > 85 and self._should_alert('crash_risk'):
            notification = self.notifier.send_notification('crash_risk', {
                'risk_level': 'high',
                'reason': 'High CPU and memory usage'
            })
            self.last_alerts['crash_risk'] = datetime.now()
            return notification
        return None
    
    def check_version_update(self, current_version: str = '2.0.0', new_version: str = '') -> Optional[str]:
        """Check if update available."""
        if new_version and new_version != current_version and self._should_alert('version'):
            notification = self.notifier.send_notification('version', {
                'current_version': current_version,
                'new_version': new_version
            })
            self.last_alerts['version'] = datetime.now()
            return notification
        return None
    
    def send_welcome(self) -> str:
        """Send personalized welcome notification."""
        return self.notifier.send_notification('welcome', {})
    
    def send_startup_notification(self) -> str:
        """Send startup notification on system boot."""
        return self.notifier.send_notification('startup', {})
    
    def _should_alert(self, alert_type: str, cooldown_minutes: int = 5) -> bool:
        """Prevent alert spam with cooldown."""
        if alert_type not in self.last_alerts:
            return True
        
        time_diff = (datetime.now() - self.last_alerts[alert_type]).total_seconds() / 60
        return time_diff > cooldown_minutes
    
    def _get_top_process(self) -> str:
        """Get top CPU consuming process."""
        try:
            processes = [(p.info['name'], p.info['cpu_percent']) 
                        for p in psutil.process_iter(['name', 'cpu_percent'])]
            top = max(processes, key=lambda x: x[1])
            return f"{top[0]} ({top[1]:.1f}%)"
        except:
            return "Unknown"
