"""Signup routes for self-serve API key generation.

Provides endpoints for developers to get API keys without a dashboard.
"""

import hashlib
import os
import secrets
from collections import defaultdict
from datetime import datetime, timedelta
from typing import Optional

from fastapi import APIRouter, HTTPException, Request, status, BackgroundTasks
from pydantic import BaseModel, EmailStr

router = APIRouter(prefix="/v1", tags=["Signup"])


# =============================================================================
# Models
# =============================================================================

class SignupRequest(BaseModel):
    """Signup request model."""
    email: EmailStr
    name: Optional[str] = None
    company: Optional[str] = None
    use_case: Optional[str] = None


class SignupResponse(BaseModel):
    """Signup response model."""
    message: str
    api_key: Optional[str] = None  # Only returned if email not configured


class RotateKeyRequest(BaseModel):
    """Key rotation request model."""
    current_key: str
    email: EmailStr


class APIKeyResponse(BaseModel):
    """API key response model."""
    api_key: str
    created_at: str
    rate_limit: str
    docs_url: str


# =============================================================================
# Email Validation
# =============================================================================

# Disposable email domains to block
DISPOSABLE_EMAIL_DOMAINS = {
    # Temporary email services
    "tempmail.com", "temp-mail.org", "guerrillamail.com", "guerrillamail.org",
    "10minutemail.com", "10minutemail.net", "throwaway.email", "throwawaymail.com",
    "mailinator.com", "trashmail.com", "fakeinbox.com", "sharklasers.com",
    "getairmail.com", "yopmail.com", "dispostable.com", "mailnesia.com",
    "tempail.com", "tempr.email", "discard.email", "discardmail.com",
    "spamgourmet.com", "mytrashmail.com", "mt2009.com", "thankyou2010.com",
    "spam4.me", "grr.la", "guerrillamailblock.com", "pokemail.net",
    "spam.la", "emailondeck.com", "fakemail.net", "getnada.com",
    "mohmal.com", "tempmailo.com", "burnermail.io", "maildrop.cc",
}

# Common email typos with suggestions
COMMON_EMAIL_TYPOS = {
    "gmial.com": "gmail.com",
    "gmai.com": "gmail.com",
    "gamil.com": "gmail.com",
    "gnail.com": "gmail.com",
    "gmail.co": "gmail.com",
    "gmail.con": "gmail.com",
    "gmal.com": "gmail.com",
    "yahooo.com": "yahoo.com",
    "yaho.com": "yahoo.com",
    "yahoo.co": "yahoo.com",
    "yahoo.con": "yahoo.com",
    "hotmal.com": "hotmail.com",
    "hotmai.com": "hotmail.com",
    "hotmail.co": "hotmail.com",
    "hotmail.con": "hotmail.com",
    "outlok.com": "outlook.com",
    "outloo.com": "outlook.com",
    "outlook.co": "outlook.com",
}


def _validate_email(email: str) -> tuple[bool, str]:
    """Validate email address for signup.
    
    Args:
        email: Email address to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    domain = email.split("@")[-1].lower()
    
    # Check for disposable email domains
    if domain in DISPOSABLE_EMAIL_DOMAINS:
        return False, "Disposable email addresses are not allowed. Please use a permanent email."
    
    # Check for common typos and suggest corrections
    if domain in COMMON_EMAIL_TYPOS:
        suggestion = COMMON_EMAIL_TYPOS[domain]
        return False, f"Did you mean @{suggestion}? Please check your email address."
    
    # Check for obviously invalid domains (no TLD)
    if "." not in domain:
        return False, "Invalid email domain. Please check your email address."
    
    # Check for very short domains (likely typos)
    tld = domain.split(".")[-1]
    if len(tld) < 2:
        return False, "Invalid email domain. Please check your email address."
    
    return True, ""


# =============================================================================
# Rate Limiting
# =============================================================================

# In-memory rate limiting (use Redis in production for distributed)
_signup_attempts: dict[str, list[datetime]] = defaultdict(list)

# Rate limit settings
SIGNUP_RATE_LIMIT_MAX = int(os.getenv("SIGNUP_RATE_LIMIT_MAX", "5"))  # Max attempts
SIGNUP_RATE_LIMIT_WINDOW_HOURS = int(os.getenv("SIGNUP_RATE_LIMIT_WINDOW", "1"))  # Window in hours


def _check_rate_limit(ip: str) -> bool:
    """Check if IP has exceeded signup rate limit.
    
    Args:
        ip: Client IP address
        
    Returns:
        True if request is allowed, False if rate limited
    """
    now = datetime.utcnow()
    cutoff = now - timedelta(hours=SIGNUP_RATE_LIMIT_WINDOW_HOURS)
    
    # Remove old attempts outside the window
    _signup_attempts[ip] = [t for t in _signup_attempts[ip] if t > cutoff]
    
    # Check if limit exceeded
    if len(_signup_attempts[ip]) >= SIGNUP_RATE_LIMIT_MAX:
        return False
    
    # Record this attempt
    _signup_attempts[ip].append(now)
    return True


def _get_rate_limit_reset(ip: str) -> int:
    """Get seconds until rate limit resets for an IP."""
    if ip not in _signup_attempts or not _signup_attempts[ip]:
        return 0
    
    oldest = min(_signup_attempts[ip])
    reset_time = oldest + timedelta(hours=SIGNUP_RATE_LIMIT_WINDOW_HOURS)
    seconds_remaining = (reset_time - datetime.utcnow()).total_seconds()
    return max(0, int(seconds_remaining))


# =============================================================================
# In-Memory Storage (Replace with DB in production)
# =============================================================================

# Simple in-memory storage for MVP
# In production, use PostgreSQL/Supabase
_users: dict[str, dict] = {}
_api_keys: dict[str, str] = {}  # api_key_hash -> email
_api_usage: dict[str, dict] = {}  # api_key_hash -> usage stats

# Usage limits
FREE_TIER_MONTHLY_LIMIT = int(os.getenv("FREE_TIER_MONTHLY_LIMIT", "10000"))


def _hash_key(api_key: str) -> str:
    """Hash API key for storage."""
    return hashlib.sha256(api_key.encode()).hexdigest()


def _generate_api_key() -> str:
    """Generate a new API key."""
    return f"blind_{secrets.token_urlsafe(32)}"


def _store_user(email: str, api_key: str, metadata: dict) -> None:
    """Store user and API key."""
    key_hash = _hash_key(api_key)
    _users[email] = {
        "api_key_hash": key_hash,
        "created_at": datetime.utcnow().isoformat(),
        **metadata,
    }
    _api_keys[key_hash] = email


def _get_user_by_email(email: str) -> Optional[dict]:
    """Get user by email."""
    return _users.get(email)


def _validate_api_key(api_key: str) -> Optional[str]:
    """Validate API key and return email if valid."""
    key_hash = _hash_key(api_key)
    return _api_keys.get(key_hash)


# =============================================================================
# Usage Tracking
# =============================================================================

def _track_usage(api_key: str) -> dict:
    """Track API key usage and return current stats.
    
    Args:
        api_key: The API key to track
        
    Returns:
        Usage statistics dict
    """
    key_hash = _hash_key(api_key)
    
    if key_hash not in _api_usage:
        _api_usage[key_hash] = {
            "total_requests": 0,
            "this_month": 0,
            "last_reset": datetime.utcnow().replace(day=1, hour=0, minute=0, second=0, microsecond=0).isoformat(),
        }
    
    usage = _api_usage[key_hash]
    
    # Reset monthly counter if new month
    last_reset = datetime.fromisoformat(usage["last_reset"])
    now = datetime.utcnow()
    if now.year != last_reset.year or now.month != last_reset.month:
        usage["this_month"] = 0
        usage["last_reset"] = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0).isoformat()
    
    usage["total_requests"] += 1
    usage["this_month"] += 1
    usage["last_request"] = now.isoformat()
    
    return usage


def _get_usage(api_key: str) -> dict:
    """Get usage stats without incrementing."""
    key_hash = _hash_key(api_key)
    
    if key_hash not in _api_usage:
        return {
            "total_requests": 0,
            "this_month": 0,
            "last_reset": datetime.utcnow().replace(day=1, hour=0, minute=0, second=0, microsecond=0).isoformat(),
        }
    
    usage = _api_usage[key_hash].copy()
    
    # Check if month rolled over (read-only check)
    last_reset = datetime.fromisoformat(usage["last_reset"])
    now = datetime.utcnow()
    if now.year != last_reset.year or now.month != last_reset.month:
        usage["this_month"] = 0
        usage["last_reset"] = now.replace(day=1, hour=0, minute=0, second=0, microsecond=0).isoformat()
    
    return usage


def _is_over_limit(api_key: str) -> bool:
    """Check if API key has exceeded monthly limit."""
    usage = _get_usage(api_key)
    return usage["this_month"] >= FREE_TIER_MONTHLY_LIMIT


def _get_next_reset_date() -> str:
    """Get the date when usage resets (first of next month)."""
    now = datetime.utcnow()
    if now.month == 12:
        next_reset = now.replace(year=now.year + 1, month=1, day=1)
    else:
        next_reset = now.replace(month=now.month + 1, day=1)
    return next_reset.strftime("%Y-%m-%d")


# =============================================================================
# Webhook Notifications
# =============================================================================

async def _send_webhook(event: str, data: dict):
    """Send webhook notification for signup events.
    
    Configure via WEBHOOK_URL environment variable.
    Useful for:
    - Slack notifications
    - CRM integrations
    - Analytics tracking
    - Custom workflows
    
    Args:
        event: Event type (e.g., 'signup.completed', 'key.rotated')
        data: Event payload
    """
    webhook_url = os.getenv("WEBHOOK_URL")
    if not webhook_url:
        return
    
    webhook_secret = os.getenv("WEBHOOK_SECRET", "")
    
    payload = {
        "event": event,
        "timestamp": datetime.utcnow().isoformat() + "Z",
        "data": data,
    }
    
    try:
        import httpx
        
        headers = {
            "Content-Type": "application/json",
            "User-Agent": "BlindAI-Webhook/1.0",
        }
        
        # Add signature if secret is configured
        if webhook_secret:
            import hmac
            import json
            signature = hmac.new(
                webhook_secret.encode(),
                json.dumps(payload).encode(),
                hashlib.sha256
            ).hexdigest()
            headers["X-Webhook-Signature"] = f"sha256={signature}"
        
        async with httpx.AsyncClient() as client:
            response = await client.post(
                webhook_url,
                json=payload,
                headers=headers,
                timeout=5.0,
            )
            if response.status_code >= 400:
                print(f"⚠ Webhook returned {response.status_code}: {response.text[:100]}")
            else:
                print(f"✓ Webhook sent: {event}")
    except Exception as e:
        # Don't fail signup if webhook fails
        print(f"⚠ Webhook failed: {e}")


# =============================================================================
# Email Sending (Optional)
# =============================================================================

async def send_api_key_email(email: str, api_key: str, name: Optional[str] = None):
    """Send API key via email.
    
    Uses Resend, SendGrid, or similar service.
    For MVP, we just log it.
    """
    # Check if email service is configured
    resend_api_key = os.getenv("RESEND_API_KEY")
    sendgrid_api_key = os.getenv("SENDGRID_API_KEY")
    
    greeting = f"Hi {name}," if name else "Hi,"
    
    if resend_api_key:
        try:
            import resend
            resend.api_key = resend_api_key
            
            resend.Emails.send({
                "from": os.getenv("EMAIL_FROM", "Blind AI <hello@blindai.dev>"),
                "to": email,
                "subject": "Your Blind AI API Key 🛡️",
                "html": f"""
                <h2>{greeting}</h2>
                <p>Welcome to Blind AI! Here's your API key:</p>
                <pre style="background: #f4f4f4; padding: 16px; border-radius: 8px; font-size: 14px;">{api_key}</pre>
                <p><strong>Keep this key secret!</strong> Don't commit it to git or share it publicly.</p>
                <h3>Quick Start</h3>
                <pre style="background: #1e1e1e; color: #d4d4d4; padding: 16px; border-radius: 8px;">
pip install blind-ai

from blind_ai import ToolGuard

guard = ToolGuard(api_key="{api_key[:20]}...")
result = guard.check("SELECT * FROM users")
                </pre>
                <p>
                    <a href="https://docs.blindai.dev">📖 Documentation</a> |
                    <a href="https://github.com/logicshaper19/blindAI">⭐ GitHub</a>
                </p>
                <p>Happy building!<br>The Blind AI Team</p>
                """,
            })
            print(f"✓ API key email sent to {email}")
        except Exception as e:
            print(f"⚠ Failed to send email: {e}")
    
    elif sendgrid_api_key:
        # SendGrid implementation
        print(f"⚠ SendGrid not implemented yet, API key for {email}: {api_key}")
    
    else:
        # No email service - log for manual sending
        print(f"📧 New signup: {email}")
        print(f"   API Key: {api_key}")


async def send_key_rotation_email(email: str, new_key: str, name: Optional[str] = None):
    """Send key rotation notification via email."""
    resend_api_key = os.getenv("RESEND_API_KEY")
    
    greeting = f"Hi {name}," if name else "Hi,"
    
    if resend_api_key:
        try:
            import resend
            resend.api_key = resend_api_key
            
            resend.Emails.send({
                "from": os.getenv("EMAIL_FROM", "Blind AI <hello@blindai.dev>"),
                "to": email,
                "subject": "🔄 Your Blind AI API Key Has Been Rotated",
                "html": f"""
                <h2>{greeting}</h2>
                <p>Your API key has been successfully rotated. Here's your new key:</p>
                <pre style="background: #f4f4f4; padding: 16px; border-radius: 8px; font-size: 14px;">{new_key}</pre>
                <p><strong>⚠️ Important:</strong></p>
                <ul>
                    <li>Your old API key has been invalidated</li>
                    <li>Update your applications with the new key</li>
                    <li>If you didn't request this rotation, contact us immediately</li>
                </ul>
                <p>
                    <a href="https://docs.blindai.dev">📖 Documentation</a> |
                    <a href="mailto:support@blindai.dev">📧 Contact Support</a>
                </p>
                <p>Stay secure!<br>The Blind AI Team</p>
                """,
            })
            print(f"✓ Key rotation email sent to {email}")
        except Exception as e:
            print(f"⚠ Failed to send rotation email: {e}")
    else:
        print(f"🔄 Key rotated for: {email}")
        print(f"   New API Key: {new_key}")


# =============================================================================
# Routes
# =============================================================================

@router.post("/signup", response_model=SignupResponse)
async def signup(
    request: SignupRequest,
    background_tasks: BackgroundTasks,
    req: Request,
):
    """Sign up for a free API key.
    
    Creates a new API key and sends it via email (if configured).
    If email service is not configured, returns the key directly.
    
    Rate limits:
    - Signup: 5 attempts per hour per IP (configurable via env vars)
    - API usage: 10K requests/month on free tier
    """
    # Rate limiting
    client_ip = req.client.host if req.client else "unknown"
    
    if not _check_rate_limit(client_ip):
        reset_seconds = _get_rate_limit_reset(client_ip)
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"Too many signup attempts. Please try again in {reset_seconds // 60} minutes.",
            headers={"Retry-After": str(reset_seconds)},
        )
    
    email = request.email.lower()
    
    # Validate email
    is_valid, error_msg = _validate_email(email)
    if not is_valid:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=error_msg,
        )
    
    # Check if user already exists
    existing_user = _get_user_by_email(email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail="Email already registered. Contact support@blindai.dev for key recovery.",
        )
    
    # Generate API key
    api_key = _generate_api_key()
    
    # Store user
    _store_user(
        email=email,
        api_key=api_key,
        metadata={
            "name": request.name,
            "company": request.company,
            "use_case": request.use_case,
        },
    )
    
    # Check if email service is configured
    email_configured = bool(os.getenv("RESEND_API_KEY") or os.getenv("SENDGRID_API_KEY"))
    
    # Send webhook notification (non-blocking)
    background_tasks.add_task(
        _send_webhook,
        "signup.completed",
        {
            "email": email,
            "name": request.name,
            "company": request.company,
            "use_case": request.use_case,
        }
    )
    
    if email_configured:
        # Send email in background
        background_tasks.add_task(send_api_key_email, email, api_key, request.name)
        return SignupResponse(
            message=f"API key sent to {email}. Check your inbox (and spam folder).",
        )
    else:
        # Return key directly (dev mode)
        return SignupResponse(
            message="Welcome to Blind AI! Save your API key - it won't be shown again.",
            api_key=api_key,
        )


@router.get("/signup/verify/{api_key}", response_model=APIKeyResponse)
async def verify_key(api_key: str):
    """Verify an API key is valid.
    
    Returns key metadata if valid.
    """
    email = _validate_api_key(api_key)
    
    if not email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
        )
    
    user = _get_user_by_email(email)
    
    return APIKeyResponse(
        api_key=f"{api_key[:10]}...{api_key[-4:]}",  # Masked
        created_at=user.get("created_at", "unknown"),
        rate_limit="10,000 requests/month (free tier)",
        docs_url="https://docs.blindai.dev",
    )


@router.post("/signup/rotate", response_model=APIKeyResponse)
async def rotate_key(
    request: RotateKeyRequest,
    background_tasks: BackgroundTasks,
):
    """Rotate an API key (in case of compromise).
    
    Invalidates the current key and generates a new one.
    Requires both the current key and email for verification.
    
    Use this if:
    - Your API key was accidentally exposed
    - You suspect unauthorized access
    - Regular security rotation policy
    """
    email = request.email.lower()
    
    # Verify current key belongs to this email
    stored_email = _validate_api_key(request.current_key)
    if not stored_email or stored_email != email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials. Ensure the API key and email match.",
        )
    
    # Get user data
    user = _get_user_by_email(email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found",
        )
    
    # Remove old key from lookup
    old_key_hash = user["api_key_hash"]
    if old_key_hash in _api_keys:
        del _api_keys[old_key_hash]
    
    # Generate new key
    new_key = _generate_api_key()
    new_key_hash = _hash_key(new_key)
    
    # Update user record
    user["api_key_hash"] = new_key_hash
    user["rotated_at"] = datetime.utcnow().isoformat()
    user["rotation_count"] = user.get("rotation_count", 0) + 1
    
    # Add new key to lookup
    _api_keys[new_key_hash] = email
    
    # Send notification email
    background_tasks.add_task(
        send_key_rotation_email,
        email,
        new_key,
        user.get("name")
    )
    
    # Send webhook notification
    background_tasks.add_task(
        _send_webhook,
        "key.rotated",
        {
            "email": email,
            "rotation_count": user["rotation_count"],
        }
    )
    
    return APIKeyResponse(
        api_key=new_key,  # Return full key (only time it's shown)
        created_at=user.get("created_at", "unknown"),
        rate_limit="10,000 requests/month (free tier)",
        docs_url="https://docs.blindai.dev",
    )


@router.get("/signup/usage/{api_key}")
async def get_usage(api_key: str):
    """Get API key usage statistics.
    
    Returns current month usage, limits, and lifetime stats.
    """
    email = _validate_api_key(api_key)
    if not email:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid API key",
        )
    
    usage = _get_usage(api_key)
    user = _get_user_by_email(email)
    
    this_month = usage.get("this_month", 0)
    
    return {
        "api_key": f"{api_key[:10]}...{api_key[-4:]}",
        "email": f"{email[:3]}...@{email.split('@')[-1]}",  # Partially masked
        "usage": {
            "this_month": this_month,
            "limit": FREE_TIER_MONTHLY_LIMIT,
            "remaining": max(0, FREE_TIER_MONTHLY_LIMIT - this_month),
            "percentage_used": round((this_month / FREE_TIER_MONTHLY_LIMIT) * 100, 1),
            "reset_date": _get_next_reset_date(),
        },
        "lifetime": {
            "total_requests": usage.get("total_requests", 0),
            "member_since": user.get("created_at", "unknown") if user else "unknown",
            "last_request": usage.get("last_request"),
        },
        "tier": "free",
        "upgrade_url": "https://blind-ai.vercel.app/pricing",
    }


@router.get("/signup/stats")
async def signup_stats():
    """Get signup statistics (for internal use)."""
    # Only allow in dev mode
    if os.getenv("BLIND_AI_ENV", "development") == "production":
        raise HTTPException(status_code=404, detail="Not found")
    
    return {
        "total_users": len(_users),
        "total_keys": len(_api_keys),
        "total_api_calls": sum(u.get("total_requests", 0) for u in _api_usage.values()),
    }
