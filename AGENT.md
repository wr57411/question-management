# Agent Instructions for Question Management System

## Build/Run Commands
- **Run backend**: `uvicorn main:app --reload` (FastAPI server on port 8000)
- **Run GUI**: `python gui.py` (requires PyQt5)
- **Run with Docker**: `docker-compose up` or `docker build . && docker run -p 8000:8000 <image>`
- **Install deps**: `pip install fastapi uvicorn python-multipart python-docx sqlalchemy PyQt5 pillow requests`
- **Setup from scratch**: `python setup.py` (auto-downloads Python 3.9 and dependencies)

## Code Style Guidelines
- **Language**: Primarily Chinese comments and UI text (see .cursor/rules/chinese.mdc)
- **Formatting**: Use 4-space indentation, snake_case for variables/functions, PascalCase for classes
- **Imports**: Group standard library, third-party, and local imports; use explicit imports
- **Error handling**: Use try-except blocks with detailed error messages, print stack traces for debugging
- **Database**: SQLAlchemy ORM with declarative base, use session for transactions
- **API**: FastAPI with async endpoints, use Pydantic models for request/response
- **File paths**: Use os.path.join() for cross-platform compatibility
- **Strings**: Use f-strings for formatting, triple quotes for multi-line strings

## Architecture
- Backend: FastAPI + SQLAlchemy (SQLite database)
- Frontend: PyQt5 GUI with Word document parsing
- Features: Physics question import from Word docs, answer management, image embedding
- Database models: Question, Answer, Tag with relationships

## Testing
- Test files: test_import.py, test_gui.py, create_test_doc.py (check these for test patterns)
- No specific test framework detected - analyze existing test files before adding new tests