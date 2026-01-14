# MinderGas Meter Reading Restrictions - Feature Documentation

## Overview

The integration now includes restrictions and smart scheduling for meter reading uploads to ensure compliance with MinderGas API best practices and prevent server overload errors.

## Changes Made

### 1. **Meter Reading Upload Window (00:05 - 01:00)**

All meter reading uploads must occur between **00:05** and **01:00** to:
- Spread server load evenly
- Prevent 503 Service Unavailable errors
- Comply with MinderGas API recommendations

**Implementation:**
- Configuration validation prevents selecting times outside this window
- Error message: "Time must be between 00:05 and 01:00"
- Time window constants in `const.py`:
  - `POST_METER_WINDOW_START = "00:05"`
  - `POST_METER_WINDOW_END = "01:00"`

### 2. **Fixed Time Upload** (Default)

Users can specify a fixed time within the window. The meter reading will be posted at exactly that time every day.

**Example:** If user selects 00:30:
- Every day at 00:30, the current meter reading is uploaded
- Consistent and predictable behavior

### 3. **Random Time Upload** (New Feature)

Users can enable "Use random time within upload window" to:
- Randomize the upload time each day
- Reduce server load clustering from multiple installations
- Improve reliability by distributing requests across the entire window

**How it works:**
1. When randomize is enabled, a random minute is selected between 00:05 and 01:00
2. Each day at 00:03, a new random time is generated for that day's upload
3. The meter reading is posted at the randomly selected time

**Benefits:**
- If 1000 users all upload at 02:00, the server gets 1000 requests at once
- With random scheduling, requests are spread across 55 minutes
- Significantly reduces the risk of server overload

## Configuration Flow Changes

### Step 2: Meter Reading Configuration

**New Fields:**
- **Upload meter readings to MinderGas** (Toggle) - Enable/disable feature
- **Use random time within upload window** (Toggle) - Enable random scheduling
- **Time to upload meter reading** (Time Picker) - Only required if NOT using random
- **Meter reading sensor entity** (Entity Picker) - Always required

**Validation:**
- If "Upload meter readings" is enabled:
  - Meter entity is always required
  - If random is disabled: Time must be between 00:05 and 01:00
  - If random is enabled: Time field is ignored

## Usage Examples

### Example 1: Fixed Time (Default)
1. Enable "Upload meter readings to MinderGas"
2. Disable "Use random time within upload window"
3. Set time to "00:30"
4. Select meter reading sensor
5. Result: Uploads every day at exactly 00:30

### Example 2: Random Time
1. Enable "Upload meter readings to MinderGas"
2. Enable "Use random time within upload window"
3. Leave time field as is (it will be ignored)
4. Select meter reading sensor
5. Result: Uploads at a different random time each day between 00:05 and 01:00

## Technical Details

### Constants Added (`const.py`)
```python
POST_METER_WINDOW_START = "00:05"
POST_METER_WINDOW_END = "01:00"
CONF_RANDOMIZE_POST_TIME = "randomize_post_time"
```

### New Helper Function (`config_flow.py`)
```python
def _is_time_in_post_window(time_str: str) -> bool:
    """Check if time is within the meter posting window (00:05-01:00)."""
```

### Modified Function (`__init__.py`)
```python
def _setup_meter_reading_schedule(hass, entry):
    # Now supports both fixed and random scheduling
    # Uses async_track_time_change for fixed time
    # Uses 00:03 trigger + random calculation for random mode
```

## Random Time Algorithm

The random time selection:
1. Generates a random minute between 5-60 (00:05 to 01:00)
2. Triggered at 00:03 UTC every morning
3. Range: 55 minutes (5 to 60 minutes in an hour)
4. Distribution: Uniform across the entire window

Example schedule over 7 days with random enabled:
- Day 1: 00:23
- Day 2: 00:45
- Day 3: 00:12
- Day 4: 00:58
- Day 5: 00:31
- Day 6: 00:07
- Day 7: 00:42

## Error Messages

**English:**
- "Time must be between 00:05 and 01:00"

**Dutch:**
- "Tijd moet tussen 00:05 en 01:00 liggen"

## Testing Recommendations

1. **Fixed Time Test:**
   - Configure with fixed time (e.g., 00:30)
   - Check logs for "Meter reading schedule set for 00:30"
   - Verify upload occurs at exact time

2. **Random Time Test:**
   - Configure with random enabled
   - Check logs for "Meter reading schedule set with RANDOM time"
   - Monitor logs across multiple days to confirm variation
   - Verify uploads occur between 00:05 and 01:00

3. **Validation Test:**
   - Try setting time to 14:00 (outside window)
   - Should see error: "Time must be between 00:05 and 01:00"
   - Try time to 00:01
   - Should see same error

## MinderGas API Recommendation

From the MinderGas API documentation:
> "Je kunt de meterstand van 0.00 uur het beste posten op een willekeurig gekozen moment tussen 0.05 uur en 1.00 uur. Hiermee wordt de serverbelasting gespreid en foutstatus 503 voorkomen."

Translation:
> "You can best post the meter reading from 0:00 hours at a randomly chosen moment between 0:05 and 1:00 hours. This spreads the server load and prevents error status 503."

This integration now fully complies with this recommendation through the random scheduling feature.

## Backwards Compatibility

- Existing configurations with fixed times within 00:05-01:00 window continue to work
- If users had time outside the window, they will see validation error on next config edit
- Default time (02:00) is within the valid window
- Random feature is optional (disabled by default)
