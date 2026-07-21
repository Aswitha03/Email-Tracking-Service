from datetime import datetime
from sqlalchemy.orm import Session

from app.models import Email

# Gmail's image proxy identifies itself with this substring in its
# User-Agent. It prefetches images (often within seconds of delivery)
# regardless of whether the user has opened the email yet.
GOOGLE_PROXY_UA_MARKER = "GoogleImageProxy"

# If a hit lands within this many seconds of the email being created,
# it's almost certainly Gmail's proxy pre-caching the image on delivery,
# not a human opening the email.
PROXY_PREFETCH_WINDOW_SECONDS = 15


def track_email_open(db: Session, tracking_id: str, user_agent: str = ""):
    """
    Records a pixel hit and, using a heuristic, decides whether it looks
    like a genuine human open vs. Gmail's image proxy prefetching the
    image on delivery.

    Returns the email object if found, otherwise None.
    """

    email = (
        db.query(Email)
        .filter(Email.tracking_id == tracking_id)
        .first()
    )

    if not email:
        return None

    now = datetime.utcnow()

    # Always log the raw hit -- this data lets you retune the heuristic
    # later without having lost information.
    email.pixel_hit_count = (email.pixel_hit_count or 0) + 1
    email.last_pixel_user_agent = user_agent
    if email.first_pixel_hit_at is None:
        email.first_pixel_hit_at = now

    is_google_proxy = GOOGLE_PROXY_UA_MARKER in (user_agent or "")

    seconds_since_created = None
    if email.created_at is not None:
        seconds_since_created = (now - email.created_at).total_seconds()

    looks_like_proxy_prefetch = (
        is_google_proxy
        and seconds_since_created is not None
        and seconds_since_created < PROXY_PREFETCH_WINDOW_SECONDS
    )

    # Only mark as a genuine "opened" event if it doesn't look like a
    # proxy prefetch, and only set opened_at the first time this happens.
    if not looks_like_proxy_prefetch and not email.opened:
        email.opened = True
        email.opened_at = now

    db.commit()
    db.refresh(email)

    return email