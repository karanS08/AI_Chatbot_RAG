# Contributing to Agricultural Advisory Chatbot

Thank you for your interest in contributing to this project! This document provides guidelines and instructions for contributing.

## 🌾 Project Overview

This is an AI-powered agricultural advisory chatbot designed for sugarcane farmers in India. It provides expert farming advice in multiple Indian languages with features like voice input/output and crop disease identification.

## 🛠️ Development Setup

### Prerequisites

- Python 3.11 or higher
- Node.js (optional, for frontend tooling)
- Google Gemini API key

### Local Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/karanS08/AI_Chatbot_RAG.git
   cd AI_Chatbot_RAG
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   # Windows
   venv\Scripts\activate
   # macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   Create a `.env` file:
   ```
   GOOGLE_API_KEY=your_api_key_here
   FLASK_ENV=development
   FLASK_DEBUG=True
   ```

5. **Run the application**
   ```bash
   python app.py
   ```

## 📁 Project Structure

```
AI_Chatbot_RAG/
├── app.py                  # Main Flask application
├── ai_services.py          # AI/ML services module
├── static/
│   ├── css/styles.css     # Application styles
│   └── js/app.js          # Frontend JavaScript
├── templates/
│   └── index.html         # Main HTML template
├── knowledge_base/        # Agricultural documents for RAG
├── tests/                 # Test suites
├── scripts/               # Utility scripts
└── docs/                  # Documentation
```

## 🧪 Testing

Run tests before submitting changes:

```bash
# Run all tests
python -m pytest tests/

# Run specific test file
python -m pytest tests/test_rag_api.py
```

## 📝 Code Style Guidelines

### Python
- Follow PEP 8 style guidelines
- Use type hints for function parameters and returns
- Add docstrings to all functions and classes
- Maximum line length: 100 characters

### JavaScript
- Use JSDoc comments for functions
- Use camelCase for variables and functions
- Add comments for complex logic

### CSS
- Use BEM naming convention where applicable
- Group related properties together
- Add comments for component sections

## 🔄 Pull Request Process

1. **Create a feature branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes**
   - Write clean, documented code
   - Add tests for new functionality
   - Update documentation as needed

3. **Test your changes**
   - Run existing tests
   - Test manually in the browser
   - Test voice features if applicable

4. **Commit with clear messages**
   ```bash
   git commit -m "feat: Add feature description"
   ```
   
   Follow conventional commits:
   - `feat:` New feature
   - `fix:` Bug fix
   - `docs:` Documentation only
   - `style:` Code style changes
   - `refactor:` Code refactoring
   - `test:` Adding tests
   - `chore:` Maintenance

5. **Push and create PR**
   ```bash
   git push origin feature/your-feature-name
   ```
   Create a Pull Request on GitHub with:
   - Clear description of changes
   - Screenshots (for UI changes)
   - Test results

## 🌐 Adding New Languages

1. Add language to `LANGUAGE_NAMES` in `ai_services.py`
2. Add language option in `templates/index.html`
3. Add translations in `static/js/app.js` translations object
4. Add language code mapping in `languageCodes` object
5. Test voice features with the new language

## 🐛 Reporting Bugs

When reporting bugs, please include:
- Browser and version
- Steps to reproduce
- Expected vs actual behavior
- Screenshots if applicable
- Console errors if any

## 📚 Documentation

- Update README.md for user-facing changes
- Add JSDoc/docstrings for new functions
- Update API documentation if endpoints change

## 🙏 Code of Conduct

- Be respectful and inclusive
- Focus on constructive feedback
- Help maintain a welcoming community

## 📞 Contact

For questions or discussions, please open a GitHub issue.

---

Thank you for contributing to making agricultural technology accessible to farmers! 🌾
