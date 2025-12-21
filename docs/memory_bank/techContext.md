# Technical Context: Veterinary Clinic Website

## Technology Stack
- **Backend**: Django 5.2.8 (Python)
- **Database**: SQLite (Development), PostgreSQL (Planned for Production)
- **Frontend**: HTML5, CSS3, Bootstrap 5, JavaScript
- **Media Handling**: Pillow (for images)
- **AI/LLM**: LangChain, OpenAI (Planned)
- **Deployment**: Gunicorn, WhiteNoise, Docker (Planned)

## Development Setup
- **Environment**: Python virtual environment (`venv`).
- **Dependencies**: Managed via `requirements.txt`.
- **Static/Media**: Handled by Django's static files system and WhiteNoise in production.

## Technical Constraints
- Must be responsive for mobile devices.
- Admin panel must be user-friendly for non-technical staff.
