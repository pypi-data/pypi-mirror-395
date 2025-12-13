from __future__ import annotations

import datetime as dt
import re
from typing import Callable, Union, Dict, List, Tuple, Any, Iterable, Optional
import pandas as pd

class DateUtils:
    """
    Period resolution & normalization for ETL artifacts.

    Canonical periods:
      - 'today'
      - 'current_month'
      - 'ytd'
      - 'itd'
      - 'custom'  (requires 'start_on' and 'end_on')

    Extras:
      - Register named periods at runtime (register_period)
      - Register regex-based periods (register_pattern)
      - Recognize explicit windows: 'YYYY-MM-DD..YYYY-MM-DD'
      - Accept 'last_N_days' and 'last_N_hours' via default patterns

    All dynamic/custom outputs standardize on:
      - date windows: 'start_on' / 'end_on' (YYYY-MM-DD or date-like)
      - time windows: 'start_ts' / 'end_ts' (ISO datetimes)
    """

    # ---- Dynamic registries ----
    _PERIOD_FUNCTIONS: Dict[str, Callable[[], Tuple[dt.date, dt.date]]] = {}
    _PERIOD_PATTERNS: List[Tuple[re.Pattern[str], Callable[[re.Match[str], dt.datetime], Dict[str, Any]]]] = []

    _LAST_N_DAYS_RE = re.compile(r"^last_(\d+)_days$")
    _WINDOW_RE = re.compile(r"^(\d{4}-\d{2}-\d{2})\.\.(\d{4}-\d{2}-\d{2})$")

    # ---------------- Core coercion helpers ----------------

    @staticmethod
    def _ensure_date(value: Union[str, dt.date, dt.datetime, pd.Timestamp]) -> dt.date:
        """Ensure the input is converted to a datetime.date."""
        if isinstance(value, dt.date) and not isinstance(value, dt.datetime):
            return value
        if isinstance(value, dt.datetime):
            return value.date()
        if isinstance(value, pd.Timestamp):
            return value.to_pydatetime().date()
        if isinstance(value, str):
            # Try pandas parser first (robust), then ISO date
            try:
                return pd.to_datetime(value, errors="raise").date()  # type: ignore[return-value]
            except Exception:
                pass
            try:
                return dt.date.fromisoformat(value)
            except Exception:
                pass
        raise ValueError(f"Unsupported date format: {value!r}")

    # Public alias (used by others)
    ensure_date = _ensure_date

    @staticmethod
    def _ensure_datetime(
        value: Union[str, dt.date, dt.datetime, pd.Timestamp],
        tz: dt.tzinfo = dt.timezone.utc,
    ) -> dt.datetime:
        """Convert input to timezone-aware datetime (defaults to UTC)."""
        if isinstance(value, dt.datetime):
            return value if value.tzinfo else value.replace(tzinfo=tz)
        if isinstance(value, dt.date):
            return dt.datetime(value.year, value.month, value.day, tzinfo=tz)
        if isinstance(value, pd.Timestamp):
            dtt = value.to_pydatetime()
            return dtt if dtt.tzinfo else dtt.replace(tzinfo=tz)
        if isinstance(value, str):
            ts = pd.to_datetime(value, errors="raise", utc=False)
            dtt = ts.to_pydatetime()
            return dtt if getattr(dtt, "tzinfo", None) else dtt.replace(tzinfo=tz)
        raise ValueError(f"Unsupported datetime format: {value!r}")

    # ---------------- Week / Month / Quarter helpers ----------------

    @classmethod
    def calc_week_range(cls, reference_date: Union[str, dt.date, dt.datetime, pd.Timestamp]) -> Tuple[dt.date, dt.date]:
        """Start (Mon) and end (Sun) for the week containing reference_date."""
        ref = cls._ensure_date(reference_date)
        start = ref - dt.timedelta(days=ref.weekday())
        end = start + dt.timedelta(days=6)
        return start, end

    @staticmethod
    def get_year_timerange(year: int) -> Tuple[dt.date, dt.date]:
        return dt.date(year, 1, 1), dt.date(year, 12, 31)

    @classmethod
    def get_first_day_of_the_quarter(cls, reference_date: Union[str, dt.date, dt.datetime, pd.Timestamp]) -> dt.date:
        ref = cls._ensure_date(reference_date)
        quarter = (ref.month - 1) // 3 + 1
        return dt.date(ref.year, 3 * quarter - 2, 1)

    @classmethod
    def get_last_day_of_the_quarter(cls, reference_date: Union[str, dt.date, dt.datetime, pd.Timestamp]) -> dt.date:
        ref = cls._ensure_date(reference_date)
        quarter = (ref.month - 1) // 3 + 1
        first_day_next_q = dt.date(ref.year, 3 * quarter + 1, 1)
        return first_day_next_q - dt.timedelta(days=1)

    @classmethod
    def get_month_range(cls, n: int = 0) -> Tuple[dt.date, dt.date]:
        """
        Range for current month (n=0) or +/- n months relative to today.
        If n == 0, end is today. Otherwise end is calendar month end.
        """
        today = dt.date.today()
        target_month = (today.month - 1 + n) % 12 + 1
        target_year = today.year + (today.month - 1 + n) // 12
        start = dt.date(target_year, target_month, 1)
        if n == 0:
            return start, today
        next_month = (target_month % 12) + 1
        next_year = target_year + (target_month == 12)
        end = dt.date(next_year, next_month, 1) - dt.timedelta(days=1)
        return start, end

    # ---------------- Period registration ----------------

    @classmethod
    def register_period(cls, name: str, func: Callable[[], Tuple[dt.date, dt.date]]) -> None:
        """
        Dynamically register a new named period.
        The callable must return (start_date, end_date) as datetime.date values.
        """
        cls._PERIOD_FUNCTIONS[name] = func

    @classmethod
    def register_pattern(
        cls,
        pattern: str | re.Pattern[str],
        resolver: Callable[[re.Match[str], dt.datetime], Dict[str, Any]],
    ) -> None:
        """
        Register a regex-based dynamic period.

        The resolver receives:
          - match: regex match object
          - now:   timezone-aware datetime (UTC by default)

        It must return a dict with optional keys:
          - 'canonical'           : str (defaults to 'custom')
          - 'start_on'/'end_on'   : ISO date strings (YYYY-MM-DD) OR
          - 'start_ts'/'end_ts'   : ISO datetime strings
          - any additional per-period params
        """
        compiled = re.compile(pattern) if isinstance(pattern, str) else pattern
        cls._PERIOD_PATTERNS.append((compiled, resolver))

    # ---------------- Default named periods ----------------

    @classmethod
    def _get_default_periods(cls) -> Dict[str, Callable[[], Tuple[dt.date, dt.date]]]:
        today = dt.date.today
        return {
            "today": lambda: (today(), today()),
            "yesterday": lambda: (today() - dt.timedelta(days=1), today() - dt.timedelta(days=1)),
            "current_week": lambda: cls.calc_week_range(today()),
            "last_week": lambda: cls.calc_week_range(today() - dt.timedelta(days=7)),
            "current_month": lambda: cls.get_month_range(n=0),
            "last_month": lambda: cls.get_month_range(n=-1),
            "current_year": lambda: cls.get_year_timerange(today().year),
            "last_year": lambda: cls.get_year_timerange(today().year - 1),
            "current_quarter": lambda: (
                cls.get_first_day_of_the_quarter(today()),
                cls.get_last_day_of_the_quarter(today()),
            ),
            "ytd": lambda: (dt.date(today().year, 1, 1), today()),
            "itd": lambda: (dt.date(1900, 1, 1), today()),
        }

    @classmethod
    def period_keys(cls) -> Iterable[str]:
        """List available named periods (defaults + registered)."""
        d = dict(cls._get_default_periods())
        d.update(cls._PERIOD_FUNCTIONS)
        return d.keys()

    # ---------------- Flexible resolver ----------------

    @classmethod
    def resolve_period(
        cls,
        period: Optional[str] = None,
        *,
        now: Optional[dt.datetime] = None,
        tz: dt.tzinfo = dt.timezone.utc,
        **overrides: Any,
    ) -> Tuple[str, Dict[str, Any]]:
        """
        Resolve a period into (canonical_key, params).

        Priority:
          1) exact named period (default + registered)
          2) registered regex patterns (e.g., 'last_7_days', 'last_36_hours')
          3) explicit window 'YYYY-MM-DD..YYYY-MM-DD'
          4) fallback: pass the period verbatim with just overrides

        Returns:
          - canonical_key: e.g., 'today', 'current_month', or 'custom'
          - params: dict containing computed keys and merged overrides
        """
        key = (period or "today").strip()
        now = (now or dt.datetime.now(tz)).astimezone(tz)

        # 1) named periods
        period_functions = cls._get_default_periods()
        period_functions.update(cls._PERIOD_FUNCTIONS)
        if key in period_functions:
            start, end = period_functions[key]()
            params = {"start_on": start.isoformat(), "end_on": end.isoformat()}
            params.update(overrides)
            return key, params

        # 2) regex patterns (user-registered)
        for patt, resolver in cls._PERIOD_PATTERNS:
            m = patt.fullmatch(key)
            if m:
                out = resolver(m, now)
                canonical = out.get("canonical", "custom")
                params = {k: v for k, v in out.items() if k != "canonical"}
                params.update(overrides)
                return canonical, params

        # 2b) default 'last_N_days'
        m = cls._LAST_N_DAYS_RE.match(key)
        if m:
            days = int(m.group(1))
            end = now.date()
            start = (now - dt.timedelta(days=days)).date()
            params = {"start_on": start.isoformat(), "end_on": end.isoformat()}
            params.update(overrides)
            return "custom", params

        # 3) explicit date window: YYYY-MM-DD..YYYY-MM-DD
        m2 = cls._WINDOW_RE.fullmatch(key)
        if m2:
            start_on, end_on = m2.group(1), m2.group(2)
            params = {"start_on": start_on, "end_on": end_on}
            params.update(overrides)
            return "custom", params

        # 4) fallback (unknown key)
        return key, dict(overrides)

    # ---------------- Backward-compatible API ----------------

    @classmethod
    def parse_period(cls, **kwargs: Any) -> Tuple[dt.date, dt.date]:
        """
        Return (start_date, end_date) as datetime.date.

        Accepts:
          - period='today' | 'current_month' | 'last_7_days' | 'YYYY-MM-DD..YYYY-MM-DD' | ...
          - optional overrides (e.g., start_on/end_on for 'custom')
        """
        period = kwargs.setdefault("period", "today")

        # Try named periods first
        period_functions = cls._get_default_periods()
        period_functions.update(cls._PERIOD_FUNCTIONS)
        if period in period_functions:
            return period_functions[period]()

        # Otherwise, resolve and coerce
        canonical, params = cls.resolve_period(period, **kwargs)

        if "start_on" in params and "end_on" in params:
            start = cls._ensure_date(params["start_on"])
            end = cls._ensure_date(params["end_on"])
            return start, end

        if "start_ts" in params and "end_ts" in params:
            sdt = cls._ensure_datetime(params["start_ts"]).date()
            edt = cls._ensure_datetime(params["end_ts"]).date()
            return sdt, edt

        raise ValueError(
            f"Could not derive date range from period '{period}' (canonical='{canonical}'). "
            f"Params: {params}"
        )


# ---------------- Default dynamic patterns registration ----------------

def _register_default_patterns() -> None:
    """
    Register common dynamic patterns:
      - last_{n}_hours  (ISO datetimes; useful for freshness windows)
    """

    def last_x_hours(match: re.Match[str], now: dt.datetime) -> Dict[str, Any]:
        hours = int(match.group(1))
        end_ts = now
        start_ts = now - dt.timedelta(hours=hours)
        return {
            "canonical": "custom",
            "start_ts": start_ts.isoformat(),
            "end_ts": end_ts.isoformat(),
            # Sensible default that callers can override:
            "max_age_minutes": max(15, min(hours * 10, 240)),
        }

    DateUtils.register_pattern(r"last_(\d+)_hours", last_x_hours)


# Register defaults at import time
_register_default_patterns()


# # Class enhancements
# # DateUtils.register_period('next_week', lambda: (datetime.date.today() + datetime.timedelta(days=7),
# #                                                 datetime.date.today() + datetime.timedelta(days=13)))
# # start, end = DateUtils.parse_period(period='next_week')
# # print(f"Next Week: {start} to {end}")
