# MinderGas Integration for Home Assistant

A Home Assistant integration to monitor your MinderGas energy consumption data.

## Features

- 📊 Real-time energy consumption tracking from MinderGas API
- 📅 Yearly usage and forecast data
- 🌡️ Usage per degree day metrics
- 🔄 Automatic data refresh scheduling
- 📝 Manual meter reading submission
- ⚙️ Configurable update intervals and posting schedules

## Installation

### Via HACS (Recommended)

1. Open HACS in Home Assistant
2. Go to **Integrations**
3. Click the three-dot menu and select **Custom repositories**
4. Add `https://github.com/pietervanharen/mindergas-hass` as a custom repository
5. Select **Integration** as the category
6. Click **Explore & Download**
7. Restart Home Assistant

### Manual Installation

1. Download the latest release from [GitHub](https://github.com/pietervanharen/mindergas-hass/releases)
2. Extract the `mindergas` folder to `custom_components/` in your Home Assistant config directory
3. Restart Home Assistant

## Configuration

1. Go to **Settings → Devices & Services → Create Automation**
2. Click **Create Automation** and search for "MinderGas"
3. Follow the configuration flow to set up:
   - **API Key**: Get this from your MinderGas account settings
   - **Update Stats**: Enable automatic data refresh
   - **Post Meter Reading**: Enable to automatically submit meter readings
   - **Meter Entity**: Select the entity containing your meter reading

## Usage

### Available Sensors

- **Yearly Usage Period Start/End**: Date range of current yearly usage period
- **Yearly Heating Usage**: Gas consumption for heating (m³)
- **Yearly Total Usage**: Total gas consumption including all usage (m³)
- **Yearly Heating Forecast**: Forecasted heating gas consumption (m³)
- **Yearly Total Forecast**: Forecasted total gas consumption (m³)
- **Usage Per Degree Day**: Average consumption per degree day (m³)

### Services/Actions

- **update_stats**: Manually refresh all statistics from MinderGas API
- **post_meter_reading**: Manually submit current meter reading to MinderGas

## Requirements

- Home Assistant 2024.1 or newer
- MinderGas account with API access
- Internet connection to MinderGas API

## Support

For issues, feature requests, or questions, please visit:
- [GitHub Issues](https://github.com/pietervanharen/mindergas-hass/issues)
- [MinderGas Website](https://www.mindergas.nl)

## License

See LICENSE file for details.
