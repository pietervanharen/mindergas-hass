"""Constants for the MinderGas integration."""

DOMAIN = "mindergas"
ATTRIBUTION = "Data provided by MinderGas"

# Configuration keys
CONF_API_KEY = "api_key"
CONF_POST_METER_READING = "post_meter_reading"
CONF_POST_TIME = "post_time"
CONF_POST_METER_ENTITY_ID = "post_meter_entity_id"
CONF_UPDATE_STATS = "update_stats"
CONF_UPDATE_TIME = "update_time"

# Default values
DEFAULT_POST_TIME = "00:30"
DEFAULT_UPDATE_TIME = "03:00"

# Meter posting restrictions
POST_METER_WINDOW_START = "00:05"  # 00:05 - earliest time to post
POST_METER_WINDOW_END = "01:00"    # 01:00 - latest time to post
CONF_RANDOMIZE_POST_TIME = "randomize_post_time"

# API Configuration
API_BASE_URL = "https://www.mindergas.nl/api"
API_VERSION = "1.0"

# Endpoints
ENDPOINT_POST_METER = "/meter_readings"
ENDPOINT_GET_YEARLY_USAGE = "/yearly_usages/latest"
ENDPOINT_GET_FORECAST = "/yearly_usages/forecast"
ENDPOINT_GET_USAGE_PER_DEGREE_DAY = "/usage_per_degree_day"

# Sensor platform
SENSOR_PLATFORM = "sensor"

# Service events
SERVICE_PUSH_READING = "push_reading"

# Update interval fallback (if no schedule)
SCAN_INTERVAL_MINUTES = 1440  # 24 hours

# Configuration flow
STEP_USER = "user"
STEP_METER_CONFIG = "meter_config"
STEP_STATS_CONFIG = "stats_config"
STEP_DONE = "done"
