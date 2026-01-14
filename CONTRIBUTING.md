# Contributing to MinderGas Home Assistant Integration

Thank you for your interest in contributing! Here are some guidelines to help you get started.

## Getting Started

1. Fork the repository
2. Clone your fork locally
3. Create a new branch for your feature (`git checkout -b feature/amazing-feature`)
4. Set up your development environment:

```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

5. Create a `.env` file with your MinderGas API key:

```bash
cp .env.example .env
# Edit .env and add your actual API key
```

## Development

### Code Style

- Follow PEP 8 guidelines
- Use type hints where possible
- Write descriptive docstrings for functions and classes

### Testing

Run the validation before submitting a PR:

```bash
python -m py_compile custom_components/mindergas/*.py
python -m json.tool custom_components/mindergas/manifest.json > /dev/null
python -m json.tool custom_components/mindergas/translations/*.json > /dev/null
```

### Testing in Home Assistant

To test the integration in a Home Assistant instance:

1. Copy the integration to your Home Assistant's `custom_components` directory
2. Restart Home Assistant
3. Add the MinderGas integration through the UI

## Submitting Changes

1. Commit your changes with clear, descriptive messages
2. Push to your fork
3. Submit a Pull Request with a clear description of what changed and why

## Reporting Bugs

When reporting bugs, please include:

- Your Home Assistant version
- The integration version
- Steps to reproduce the issue
- Expected vs actual behavior
- Any relevant logs (in Settings > System > Logs)

## Feature Requests

Feel free to suggest improvements! Please provide:

- A clear description of the feature
- Why you think it would be useful
- Any relevant examples or references

## Code Review

All submissions require code review. We'll check for:

- Code quality and style
- Proper error handling
- Translation completeness
- Security considerations
- Documentation

## License

By submitting code to this project, you agree to license it under the MIT License.

## Questions?

Feel free to open an issue or discussion if you have questions!
