# MinderGas Home Assistant Integration

[![HACS Supported](https://img.shields.io/badge/HACS-supported-green)](https://hacs.xyz/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Home Assistant](https://img.shields.io/badge/Home%20Assistant-2024.1%2B-blue)](https://www.home-assistant.io/)

A fully-featured Home Assistant integration for monitoring your gas consumption via the MinderGas API.

## ✨ Features

- 📊 **Real-time monitoring**: View your current and historical gas consumption
- 📈 **Yearly statistics**: Track yearly usage and forecasts
- 🌡️ **Degree day analytics**: Understand consumption relative to weather
- 📝 **Automatic meter reading submission**: Schedule daily uploads to MinderGas
- 🔄 **Flexible scheduling**: Customize update times and intervals
- 🔐 **Secure**: API key stored safely in Home Assistant
- 🌍 **Multi-language**: English and Dutch interface support

## 📥 Installation

### Recommended: HACS

1. Open **HACS** in Home Assistant
2. Navigate to **Integrations**
3. Click the ⋮ menu → **Custom repositories**
4. Add: `https://github.com/pietervanharen/mindergas-hass`
5. Category: **Integration**
6. Click **Explore & Download**
7. **Restart Home Assistant**

### Manual Installation

1. Download the latest [release](https://github.com/pietervanharen/mindergas-hass/releases)
2. Extract to `custom_components/mindergas` in your config directory
3. Restart Home Assistant

## ⚙️ Configuration

1. Go to **Settings → Devices & Services → Integrations**
2. Click **Create Integration** and search for **MinderGas**
3. Follow the setup wizard:

### Step 1: API Configuration
- Get your **API key** from [MinderGas Settings](https://www.mindergas.nl/api)
- Paste it into the integration setup

### Step 2: Meter Reading (Optional)
- Enable automatic meter reading uploads
- Select your meter reading entity (e.g., gas meter sensor)
- Choose upload time (typically 00:30)

### Step 3: Statistics (Optional)
- Enable automatic statistics updates
- Choose update time (typically 03:00)

## 📊 Available Entities

Once configured, you'll have access to:

### Period Information
- **Yearly Usage Period Start** - Date when current year starts
- **Yearly Usage Period End** - Date when current year ends
- **Yearly Forecast Period Start** - Forecast year start
- **Yearly Forecast Period End** - Forecast year end

### Consumption Data (m³)
- **Yearly Heating Usage** - Gas used for heating this year
- **Yearly Total Usage** - Total gas used this year
- **Yearly Heating Forecast** - Forecasted heating consumption
- **Yearly Total Forecast** - Forecasted total consumption
- **Usage Per Degree Day** - Average consumption per degree day

## 🎯 Actions/Services

### update_stats
Manually refresh all statistics from MinderGas API:
```yaml
action: mindergas.update_stats
```

### post_meter_reading
Submit the current meter reading to MinderGas:
```yaml
action: mindergas.post_meter_reading
```

## 🔑 API Key Management

Your MinderGas API key is stored securely in Home Assistant:
- ✅ Never committed to git
- ✅ Encrypted in Home Assistant storage
- ✅ Only accessible to the integration

**Never share your API key** - it grants full access to your MinderGas account.

Get your free API key: [MinderGas API Dashboard](https://www.mindergas.nl/api)

## 📋 Requirements

- Home Assistant 2024.1 or newer
- Active MinderGas account with API access
- Internet connection to MinderGas API

## 🐛 Troubleshooting

### Sensors showing "Unknown"
- Verify your API key is correct
- Check that "Update statistics" is enabled in settings
- Wait a few minutes for the first data fetch
- Check Home Assistant logs for errors

### Meter reading not posting
- Ensure meter reading is enabled in settings
- Verify the meter entity is correctly selected
- Check that the entity is returning a valid number
- Review logs for API errors

## 📝 License

This project is licensed under the MIT License - see [LICENSE](LICENSE) file for details.

## 🔗 Resources

- [Home Assistant Documentation](https://www.home-assistant.io/docs/)
- [MinderGas Website](https://www.mindergas.nl)
- [GitHub Repository](https://github.com/pietervanharen/mindergas-hass)
- [Issues & Feature Requests](https://github.com/pietervanharen/mindergas-hass/issues)

## 💡 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

---

**Tip**: Use Home Assistant automations to trigger meter reading submissions at specific times or when certain conditions are met.
