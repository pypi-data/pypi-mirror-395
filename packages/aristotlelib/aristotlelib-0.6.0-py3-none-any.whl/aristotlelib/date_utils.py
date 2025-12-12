from datetime import datetime, timezone


def format_relative_time(dt: datetime) -> str:
    """Format a datetime as relative time from now (e.g., '2 hours ago')."""
    now = datetime.now(timezone.utc)

    # Ensure dt is timezone-aware
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)

    delta = now - dt
    seconds = int(delta.total_seconds())

    years = delta.days // 365
    if years > 0:
        return f"{years} year ago" if years == 1 else f"{years} years ago"

    weeks = delta.days // 7
    if weeks > 0:
        return f"{weeks} week ago" if weeks == 1 else f"{weeks} weeks ago"

    days = delta.days
    if days > 0:
        return f"{days} day ago" if days == 1 else f"{days} days ago"

    hours = seconds // 3600
    if hours > 0:
        return f"{hours} hour ago" if hours == 1 else f"{hours} hours ago"

    minutes = seconds // 60
    if minutes > 0:
        return f"{minutes} min ago" if minutes == 1 else f"{minutes} mins ago"

    # Show seconds instead of "just now"
    if seconds <= 0:
        return "0 secs ago"
    return f"{seconds} sec ago" if seconds == 1 else f"{seconds} secs ago"
