# MinderGas Integration Architecture

## Data Flow Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                    Home Assistant                               │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  ┌──────────────────┐         ┌──────────────────┐             │
│  │  Config Flow     │         │   Integration    │             │
│  │  (config_flow.py)│────────▶│  Setup (__init__) │            │
│  └──────────────────┘         └────────┬─────────┘             │
│                                         │                       │
│          ┌─────────────────────────────┼─────────────────────┐  │
│          │                             │                     │  │
│          ▼                             ▼                     ▼  │
│   ┌─────────────┐           ┌──────────────────┐    ┌──────────┐│
│   │ API Client  │           │  Time Scheduler  │    │ Sensors  ││
│   │  (api.py)   │           │   (async_track)  │    │(sensor.py)│
│   └─────────────┘           └──────────────────┘    └──────────┘
│          │                        │         │             │     │
│          └────────────────────────┼─────────┼─────────────┘     │
│                                   │         │                   │
│                      ┌────────────▼────┬────▼──────┐            │
│                      │  Daily Tasks    │           │            │
│                      ├─────────────────┤           │            │
│                      │ 02:00 - Upload  │           │            │
│                      │ 03:00 - Stats   │           │            │
│                      └────────┬────────┘           │            │
│                               │                    │            │
└───────────────────────────────┼────────────────────┼────────────┘
                                │                    │
                                │                    │
                ┌───────────────▼──┐    ┌───────────▼──┐
                │  MinderGas API   │    │ Entity State │
                │  Server          │    │ Storage      │
                ├──────────────────┤    └──────────────┘
                │ POST /meter_..   │
                │ GET /yearly_..   │
                │ GET /forecast    │
                │ GET /usage_..    │
                └──────────────────┘
```

## Configuration Flow

```
┌─────────────────────────────────────────────────────────────────┐
│                  Configuration Wizard                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  Step 1: API Key Input                                         │
│  ├─ User enters API key                                        │
│  ├─ Validate against MinderGas API                             │
│  └─ Store securely (NOT in config files)                       │
│                   │                                             │
│                   ▼                                             │
│  Step 2: Meter Reading Setup                                   │
│  ├─ Enable/Disable automatic uploads                           │
│  ├─ Select upload time (00:05-01:00 recommended)              │
│  ├─ Select meter reading sensor entity                         │
│  └─ Validate entity exists                                     │
│                   │                                             │
│                   ▼                                             │
│  Step 3: Statistics Update Setup                               │
│  ├─ Enable/Disable automatic updates                           │
│  ├─ Select update time (should be after upload)                │
│  └─ Configure sensor creation                                  │
│                   │                                             │
│                   ▼                                             │
│  Configuration Complete                                        │
│  └─ All settings saved                                         │
│  └─ Scheduled tasks initialized                                │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## Daily Operation

```
Timeline:
├─ 00:00 - Midnight
├─ 00:05-01:00 - Meter reading upload window
│  └─ At configured time (default 02:00):
│     ├─ Read current meter value from sensor
│     ├─ POST to MinderGas API
│     └─ Log success/failure
│
├─ 03:00 - Statistics update (default time)
│  └─ At configured time:
│     ├─ GET /api/yearly_usages/latest
│     │  └─ Update yearly usage sensors
│     ├─ GET /api/yearly_usages/forecast
│     │  └─ Update forecast sensors
│     ├─ GET /api/usage_per_degree_day
│     │  └─ Update degree day sensor
│     └─ Fire update event
│
└─ 23:59 - End of day (cycle repeats)
```

## Sensor Entity Creation

```
If Update Statistics Enabled:
├─ sensor.mindergas_yearly_heating_usage
│  ├─ Type: Energy (kWh, m³, GJ)
│  ├─ State Class: total_increasing
│  └─ Updated: Daily at configured time
│
├─ sensor.mindergas_yearly_total_usage
│  ├─ Type: Energy (kWh, m³, GJ)
│  ├─ State Class: total_increasing
│  └─ Updated: Daily at configured time
│
├─ sensor.mindergas_yearly_heating_forecast
│  ├─ Type: Energy (kWh, m³, GJ)
│  ├─ State Class: measurement
│  └─ Updated: Daily at configured time
│
├─ sensor.mindergas_yearly_total_forecast
│  ├─ Type: Energy (kWh, m³, GJ)
│  ├─ State Class: measurement
│  └─ Updated: Daily at configured time
│
└─ sensor.mindergas_usage_per_degree_day
   ├─ Type: Energy (kWh, m³, MJ)
   ├─ State Class: measurement
   └─ Updated: Daily at configured time
```

## Error Handling Flow

```
API Request
    │
    ├─ Success (200/201)
    │  └─ Update state, log success
    │
    ├─ Client Error (4xx)
    │  ├─ 401: Invalid API key
    │  ├─ 402: Payment required (subscription expired)
    │  ├─ 403: Too many requests
    │  ├─ 404: No data available
    │  ├─ 406: Invalid headers
    │  └─ 422: Validation error
    │      └─ Log details, notify user in logs
    │
    ├─ Server Error (5xx)
    │  ├─ 503: Service unavailable
    │  └─ Retry next scheduled time
    │
    └─ Network Error
       ├─ Connection timeout
       ├─ SSL error
       └─ Retry next scheduled time
```

## Security Architecture

```
┌─────────────────────────────────────────────────────────────────┐
│                  Security Layers                                │
├─────────────────────────────────────────────────────────────────┤
│                                                                  │
│  1. Environment Variable Storage                               │
│     └─ API key in .env (excluded from git)                    │
│                                                                  │
│  2. Home Assistant Integration                                 │
│     └─ Stored in HA's encrypted storage (not in yaml)         │
│                                                                  │
│  3. HTTPS Communication                                        │
│     └─ All API calls use https://                              │
│                                                                  │
│  4. API Version Validation                                     │
│     └─ Requires correct API-VERSION header                     │
│                                                                  │
│  5. Token-based Authentication                                 │
│     └─ AUTH-TOKEN in headers (not in URL)                     │
│                                                                  │
│  6. No Logging of Sensitive Data                              │
│     └─ API key never printed to logs                           │
│                                                                  │
└─────────────────────────────────────────────────────────────────┘
```

## File Organization

```
Integration Module Structure:
├─ __init__.py
│  ├─ Imports all components
│  ├─ Platform setup
│  ├─ Configuration entry handling
│  ├─ Scheduled task creation
│  └─ Cleanup on unload
│
├─ api.py
│  ├─ MinderGasAPI class
│  ├─ POST meter_readings
│  ├─ GET yearly_usages/latest
│  ├─ GET yearly_usages/forecast
│  └─ GET usage_per_degree_day
│
├─ config_flow.py
│  ├─ ConfigFlow class
│  ├─ Step 1: API key validation
│  ├─ Step 2: Meter config
│  └─ Step 3: Stats config
│
├─ const.py
│  ├─ DOMAIN constant
│  ├─ Configuration keys (CONF_*)
│  ├─ API endpoints
│  └─ Default values
│
├─ sensor.py
│  ├─ SensorEntity classes
│  ├─ 5 sensor implementations
│  └─ Data update logic
│
├─ manifest.json
│  ├─ Integration metadata
│  └─ Dependencies
│
└─ translations/
   ├─ en.json (English)
   └─ nl.json (Dutch)
```

---

This architecture ensures:
- **Security**: API key never exposed
- **Reliability**: Proper error handling and retries
- **Performance**: Scheduled tasks, no polling
- **User-friendly**: 3-step configuration
- **Maintainable**: Clear separation of concerns
