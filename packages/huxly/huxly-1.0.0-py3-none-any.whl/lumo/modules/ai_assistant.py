"""AI assistant for personalized recommendations."""
from ..utils.logging import logger

class AIAssistant:
    """Simple rule-based assistant providing suggestions."""
    
    def analyze(self, metrics):
        """Generate suggestions based on metrics."""
        suggestions = []
        
        if metrics.get("cpu_percent", 0) > 70:
            suggestions.append("CPU usage is high. Consider closing heavy applications or enabling Game Mode.")
        
        if metrics.get("memory_percent", 0) > 75:
            suggestions.append("Memory is constrained. Try: (1) Close tabs in browser, (2) Enable Optimize, or (3) Restart.")
        
        if metrics.get("disk_percent", 0) > 85:
            suggestions.append("Disk space low. Run 'heavenpc optimize' to clean temporary files.")
        
        return suggestions

def get_suggestions(metrics):
    """Get AI-driven suggestions for the system."""
    ai = AIAssistant()
    logger.info("Generating AI suggestions for metrics: %s", metrics)
    return {"suggestions": ai.analyze(metrics)}
