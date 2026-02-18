"""
Background Scheduler for Daily Stock Alerts
Runs daily at specified time to send subscription alerts
"""

import schedule
import time
import threading
from datetime import datetime
from subscription_service import SubscriptionService

class AlertScheduler:
    """Schedule and run daily stock alerts"""
    
    def __init__(self, alert_time="09:00"):
        """
        Initialize scheduler
        
        Args:
            alert_time: Time to send daily alerts (24-hour format, e.g., "09:00")
        """
        self.alert_time = alert_time
        self.subscription_service = SubscriptionService()
        self.running = False
        self.thread = None
    
    def start(self):
        """Start the scheduler in a background thread"""
        if self.running:
            print("⚠️  Scheduler already running")
            return
        
        print(f"\n{'='*60}")
        print(f"STARTING ALERT SCHEDULER")
        print(f"{'='*60}")
        print(f"Daily alerts scheduled for: {self.alert_time}")
        print(f"Current time: {datetime.now().strftime('%H:%M:%S')}")
        print(f"{'='*60}\n")
        
        # Schedule daily job
        schedule.every().day.at(self.alert_time).do(self._run_alerts)
        
        # Start scheduler in background thread
        self.running = True
        self.thread = threading.Thread(target=self._run_scheduler, daemon=True)
        self.thread.start()
        
        print("✓ Scheduler started successfully\n")
    
    def stop(self):
        """Stop the scheduler"""
        self.running = False
        schedule.clear()
        print("\n✓ Scheduler stopped\n")
    
    def _run_scheduler(self):
        """Run the scheduler loop"""
        while self.running:
            schedule.run_pending()
            time.sleep(60)  # Check every minute
    
    def _run_alerts(self):
        """Run the daily alerts job"""
        try:
            print(f"\n🔔 Triggering scheduled daily alerts...")
            result = self.subscription_service.send_daily_alerts()
            print(f"✓ Alerts completed: {result['sent']} sent, {result['failed']} failed\n")
        except Exception as e:
            print(f"✗ Error running scheduled alerts: {e}\n")
    
    def run_now(self):
        """Manually trigger alerts (for testing)"""
        print("\n🔔 Manually triggering daily alerts...")
        return self.subscription_service.send_daily_alerts()


# Global scheduler instance
_scheduler = None

def get_scheduler(alert_time="09:00"):
    """Get or create the global scheduler instance"""
    global _scheduler
    if _scheduler is None:
        _scheduler = AlertScheduler(alert_time)
    return _scheduler

def start_scheduler(alert_time="09:00"):
    """Start the global scheduler"""
    scheduler = get_scheduler(alert_time)
    scheduler.start()
    return scheduler

def stop_scheduler():
    """Stop the global scheduler"""
    global _scheduler
    if _scheduler:
        _scheduler.stop()
