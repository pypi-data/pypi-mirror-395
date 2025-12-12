# Contributing to fextapi

Thank you for your interest in contributing to fextapi! We welcome contributions from the community.

## Getting Started

1. **Fork the repository**
   ```bash
   git clone https://github.com/fextapi/fextapi.git
   cd fextapi
   ```

2. **Install development dependencies**
   ```bash
   uv sync
   ```

3. **Run tests**
   ```bash
   pytest
   ```

## Development Workflow

1. Create a new branch for your feature or bugfix
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. Make your changes and ensure tests pass
   ```bash
   pytest
   ```

3. Follow code style guidelines (PEP 8)
   ```bash
   ruff check .
   ruff format .
   ```

4. Commit your changes with clear messages
   ```bash
   git commit -m "Add feature: description"
   ```

5. Push to your fork and create a Pull Request
   ```bash
   git push origin feature/your-feature-name
   ```

## Code Style

- Follow PEP 8 guidelines
- Use type hints for all functions
- Write docstrings for public APIs
- Keep line length under 100 characters

## Testing

- Write tests for new features
- Ensure all tests pass before submitting PR
- Aim for >80% code coverage

## Commit Messages

- Use clear and descriptive commit messages
- Start with a verb (Add, Fix, Update, Remove)
- Keep the first line under 50 characters
- Provide detailed description if needed

## Pull Request Process

1. Update README.md if adding new features
2. Update documentation as needed
3. Ensure CI checks pass
4. Request review from maintainers

## Questions?

Open an issue on GitHub or contact the maintainers.

Thank you for contributing! 🎉
