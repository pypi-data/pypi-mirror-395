# Contributing to RAFAEL

Thank you for your interest in contributing to RAFAEL! 🔱

**IMPORTANT**: RAFAEL is proprietary software. By contributing, you agree that all contributions become the property of RAFAEL Framework under the Proprietary License.

## How to Contribute

### 1. Report Bugs

Found a bug? Please open an issue with:
- Clear description of the problem
- Steps to reproduce
- Expected vs actual behavior
- Your environment (OS, Python version, etc.)

### 2. Suggest Features

Have an idea? Open an issue with:
- Clear description of the feature
- Use case and benefits
- Proposed implementation (optional)

### 3. Submit Resilience Patterns

Share your proven patterns:

```python
# Create a pattern
pattern = ResiliencePattern(
    id="your_pattern_id",
    name="Your Pattern Name",
    category=PatternCategory.RETRY,
    description="What it does",
    problem="What problem it solves",
    solution="How it solves it",
    technology_stack=[TechnologyStack.PYTHON],
    code_example="...",
    author="your_name"
)

# Submit via PR or issue
```

### 4. Improve Documentation

- Fix typos
- Add examples
- Clarify explanations
- Translate to other languages

### 5. Write Code

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes
4. Add tests
5. Run tests: `pytest`
6. Format code: `black .`
7. Commit: `git commit -m 'Add amazing feature'`
8. Push: `git push origin feature/amazing-feature`
9. Open a Pull Request

## Development Setup

```bash
# Clone repository
git clone https://github.com/rafael-framework/rafael.git
cd rafael

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -e ".[dev]"

# Run tests
pytest

# Format code
black .

# Type checking
mypy .
```

## Code Style

- Follow PEP 8
- Use type hints
- Write docstrings
- Add tests for new features
- Keep functions focused and small

## Testing

```bash
# Run all tests
pytest

# Run specific test
pytest tests/test_rafael_engine.py

# Run with coverage
pytest --cov=rafael
```

## Pattern Submission Guidelines

### Quality Criteria

- ✅ Proven in production or extensive testing
- ✅ Clear documentation
- ✅ Working code example
- ✅ Appropriate technology stack tags
- ✅ Handles edge cases

### Pattern Template

```python
ResiliencePattern(
    id="tech_category_name_001",
    name="Descriptive Name",
    category=PatternCategory.XXX,
    description="One-line description",
    problem="What problem does this solve?",
    solution="How does it solve it?",
    technology_stack=[TechnologyStack.XXX],
    code_example="""
# Clear, runnable code example
# With comments explaining key parts
""",
    configuration={
        "param1": "value1",
        "param2": "value2"
    },
    author="your_name",
    tags=["tag1", "tag2"]
)
```

## Community Guidelines

- Be respectful and inclusive
- Help others learn
- Share knowledge generously
- Give constructive feedback
- Celebrate successes

## Recognition

Contributors will be:
- Listed in CONTRIBUTORS.md
- Credited in release notes
- Featured in community highlights
- Eligible for contributor badges

## Questions?

- Open an issue
- Join our Discord
- Email: contribute@rafaelabs.xyz

---

**Together, we build antifragile systems! 🔱**
