# MinderGas Integration Testing Guide

Complete testing guide for the MinderGas Home Assistant integration running in Docker.

## Prerequisites

- Docker Home Assistant running (see DOCKER_SETUP.md)
- MinderGas API key (from https://www.mindergas.nl/api)
- A gas meter sensor entity in Home Assistant or ability to create one

## Test Environment Setup

### 1. Start Home Assistant
```bash
docker-compose up -d
```

### 2. Complete Setup Wizard
- Create Home Assistant account
- Set location to Netherlands (optional, for timezone)
- Accept any initial disclaimers

### 3. Optional: Create Mock Meter Sensor

For testing without a real meter, create a mock sensor:

1. Edit `home_assistant_data/configuration.yaml`:

```yaml
# Add this section for testing
template:
  - sensor:
      - name: "Mock Gas Meter"
        unique_id: mock_gas_meter
        unit_of_measurement: "m³"
        state_class: total_increasing
        state: "{{ (999.5 + (now().day * 0.1)) | round(2) }}"
```

2. Reload: Developer Tools → YAML → Configuration Reloading → Reload Template Entities

3. Entity should appear as `sensor.mock_gas_meter`

## Test Scenarios

### Test 1: Add MinderGas Integration

**Goal:** Verify integration appears and configuration flow works

**Steps:**
1. Settings → Devices & Services → Integrations
2. Click "Create Integration"
3. Search "MinderGas"
4. Should see MinderGas in results

**Expected Result:** ✓ MinderGas integration appears

**Pass/Fail:** ___

---

### Test 2: API Key Validation

**Goal:** Verify API key is validated during setup

**Steps:**
1. Start adding MinderGas integration
2. Enter invalid API key (e.g., "invalid123")
3. Try to proceed

**Expected Result:** ✗ Error message: "Invalid API key" or "Failed to connect"

**Pass/Fail:** ___

---

### Test 3: Valid API Key

**Goal:** Verify valid API key is accepted

**Steps:**
1. Start adding MinderGas integration
2. Enter your actual MinderGas API key
3. Proceed to next step

**Expected Result:** ✓ Accepted and moves to meter configuration

**Pass/Fail:** ___

---

### Test 4: Meter Configuration - Fixed Time

**Goal:** Verify meter configuration with fixed time works

**Steps:**
1. In meter config step:
   - Enable "Upload meter readings to MinderGas"
   - Disable "Use random time within upload window"
   - Set time to "00:30"
   - Select meter entity (e.g., `sensor.mock_gas_meter`)
2. Proceed to next step

**Expected Result:** ✓ All fields accepted, moves to stats configuration

**Pass/Fail:** ___

---

### Test 5: Time Validation - Before Window

**Goal:** Verify time validation prevents uploads before 00:05

**Steps:**
1. In meter config:
   - Enable meter readings
   - Disable random
   - Try to set time to "00:02"
   - Try to proceed

**Expected Result:** ✗ Error: "Time must be between 00:05 and 01:00"

**Pass/Fail:** ___

---

### Test 6: Time Validation - After Window

**Goal:** Verify time validation prevents uploads after 01:00

**Steps:**
1. In meter config:
   - Enable meter readings
   - Disable random
   - Try to set time to "02:00"
   - Try to proceed

**Expected Result:** ✗ Error: "Time must be between 00:05 and 01:00"

**Pass/Fail:** ___

---

### Test 7: Time Validation - Valid Times

**Goal:** Verify valid times are accepted

**Steps:**
Test these times one by one:
- 00:05 (start)
- 00:30 (middle)
- 01:00 (end)

**Expected Result:** ✓ All accepted without error

**Pass/Fail:** ___

---

### Test 8: Random Time Checkbox

**Goal:** Verify random time option works

**Steps:**
1. In meter config:
   - Enable meter readings
   - Enable "Use random time within upload window"
   - Note: Time field should be ignored
   - Select meter entity
2. Proceed

**Expected Result:** ✓ Accepted without time validation error

**Pass/Fail:** ___

---

### Test 9: Missing Meter Entity

**Goal:** Verify meter entity is required

**Steps:**
1. In meter config:
   - Enable meter readings
   - Leave meter entity empty
   - Try to proceed

**Expected Result:** ✗ Error: "This field is required"

**Pass/Fail:** ___

---

### Test 10: Statistics Configuration

**Goal:** Verify statistics configuration works

**Steps:**
1. Reached stats config step
2. Enable "Update usage statistics"
3. Set update time to "03:00"
4. Complete setup

**Expected Result:** ✓ Integration created successfully

**Pass/Fail:** ___

---

### Test 11: Sensor Creation

**Goal:** Verify sensors are created when stats enabled

**Steps:**
1. Settings → Devices & Services
2. Look for MinderGas integration
3. Click it to see devices and entities
4. Check for sensor entities:
   - `sensor.mindergas_yearly_heating_usage`
   - `sensor.mindergas_yearly_total_usage`
   - `sensor.mindergas_yearly_heating_forecast`
   - `sensor.mindergas_yearly_total_forecast`
   - `sensor.mindergas_usage_per_degree_day`

**Expected Result:** ✓ All 5 sensors appear

**Pass/Fail:** ___

---

### Test 12: Sensor States

**Goal:** Verify sensor states are populated

**Steps:**
1. Settings → Developer Tools → States
2. Search for "mindergas" sensors
3. Check if any have values

**Expected Result:** ⚠ May be empty initially (depends on MinderGas account data)
              ✓ Format looks like: `{"value": 123.45, "unit": "cubic_meter"}`

**Pass/Fail:** ___

---

### Test 13: Dutch Language Support

**Goal:** Verify Dutch translations work

**Steps:**
1. Settings → System → Language and Region
2. Change language to "Nederlands"
3. Reload page or restart
4. Go back to add MinderGas integration again

**Expected Result:** ✓ UI shows Dutch text (if fully translated)

**Pass/Fail:** ___

---

### Test 14: Configuration Editing

**Goal:** Verify configuration can be edited

**Steps:**
1. Settings → Devices & Services → MinderGas
2. Click "Configure" or the three-dot menu
3. Edit meter time to different value (still valid)
4. Save changes

**Expected Result:** ✓ Changes saved and applied

**Pass/Fail:** ___

---

### Test 15: Integration Reload

**Goal:** Verify integration can be reloaded

**Steps:**
1. Make a minor code change (e.g., comment in api.py)
2. Save file
3. Docker restarts automatically (or: `docker-compose restart`)
4. Settings → Devices & Services → MinderGas
5. Click three-dot menu → "Reload"

**Expected Result:** ✓ Integration reloads without errors

**Pass/Fail:** ___

---

### Test 16: Logs for Errors

**Goal:** Verify no errors in Home Assistant logs

**Steps:**
1. Run: `docker-compose logs home-assistant | grep -i mindergas`
2. Run: `docker-compose logs home-assistant | grep -i error`

**Expected Result:** ✓ No errors related to mindergas integration

**Pass/Fail:** ___

---

### Test 17: Scheduler - Fixed Time

**Goal:** Verify meter reading scheduler works (fixed time)

**Steps:**
1. Configure with fixed time "00:30"
2. Check logs: `docker-compose logs home-assistant | grep "Meter reading schedule"`
3. Should see: "Meter reading schedule set for 00:30"

**Expected Result:** ✓ Scheduler initialized correctly

**Pass/Fail:** ___

---

### Test 18: Scheduler - Random Time

**Goal:** Verify meter reading scheduler works (random time)

**Steps:**
1. Configure with random time enabled
2. Check logs: `docker-compose logs home-assistant | grep "Meter reading schedule"`
3. Should see: "Meter reading schedule set with RANDOM time"

**Expected Result:** ✓ Scheduler initialized for random mode

**Pass/Fail:** ___

---

### Test 19: Restart Persistence

**Goal:** Verify configuration persists after restart

**Steps:**
1. Configure MinderGas (both meter and stats)
2. Restart: `docker-compose restart home-assistant`
3. Wait 30 seconds
4. Check Settings → Devices & Services
5. MinderGas should still be there with same config

**Expected Result:** ✓ Integration and sensors still present

**Pass/Fail:** ___

---

### Test 20: Uninstall Integration

**Goal:** Verify integration can be safely uninstalled

**Steps:**
1. Settings → Devices & Services → MinderGas
2. Click three-dot menu
3. Select "Delete"
4. Confirm deletion

**Expected Result:** ✓ Integration removed, sensors deleted

**Pass/Fail:** ___

---

## Advanced Testing

### Manual API Testing

Test the API directly from Docker:

```bash
docker-compose exec home-assistant python3 << 'EOF'
import asyncio
from homeassistant.components.mindergas.api import MinderGasAPI

async def test():
    api = MinderGasAPI("YOUR_API_KEY")
    
    # Test yearly usage
    result = await api.get_yearly_usage()
    print("Yearly usage:", result)
    
    # Test forecast
    forecast = await api.get_yearly_forecast()
    print("Forecast:", forecast)
    
    await api.close()

asyncio.run(test())
EOF
```

### Performance Testing

Monitor Docker resource usage:

```bash
# Real-time monitoring
docker stats home-assistant

# Once-off check
docker stats --no-stream home-assistant
```

Expected:
- CPU: 0-5% at idle
- Memory: 300-500MB

### Log Level Control

For more detailed logging:

1. Settings → System → Logs
2. Set mindergas to DEBUG level
3. Reload integration

## Test Result Summary

**Total Tests:** 20
**Passed:** ___
**Failed:** ___
**Skipped:** ___

### Failed Tests Analysis

For any failed tests:
1. Note the test number and name
2. Check logs: `docker-compose logs home-assistant`
3. Look for error messages
4. Refer to TROUBLESHOOTING section in DOCKER_SETUP.md

## Automated Test Script

Save as `test_integration.sh`:

```bash
#!/bin/bash

echo "Testing MinderGas Integration..."
echo ""

# Check container is running
if ! docker-compose ps home-assistant | grep -q "Up"; then
    echo "❌ Home Assistant not running"
    exit 1
fi

echo "✓ Home Assistant running"

# Check integration directory exists
if [ -d "custom_components/mindergas" ]; then
    echo "✓ Integration directory exists"
else
    echo "❌ Integration directory missing"
    exit 1
fi

# Check files exist
files=(
    "custom_components/mindergas/__init__.py"
    "custom_components/mindergas/api.py"
    "custom_components/mindergas/config_flow.py"
    "custom_components/mindergas/manifest.json"
)

for file in "${files[@]}"; do
    if [ -f "$file" ]; then
        echo "✓ $file"
    else
        echo "❌ $file missing"
    fi
done

echo ""
echo "✓ All basic checks passed!"
echo "Visit http://localhost:8123 to continue testing"
```

Run with:
```bash
chmod +x test_integration.sh
./test_integration.sh
```

## Resources

- [Home Assistant Testing](https://developers.home-assistant.io/docs/dev_101_testing)
- [MinderGas API Docs](https://www.mindergas.nl/api)
- [Docker Compose Docs](https://docs.docker.com/compose/)

---

**After all tests pass, you're ready for production deployment!**
