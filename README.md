# Veterinary Clinic Website

A Django-based website for a small veterinary clinic with news, contacts, and content management features.

## Features

- Home page with clinic information and latest news
- News section with listing and detail pages
- About page with clinic information and veterinarian profiles
- Contact page with clinic information and Yandex Maps integration
- Contact form for sending messages
- Admin panel for content management
- Public veterinary chat assistant powered by NVIDIA NOOA
- Responsive design for mobile devices

## Technology Stack

- **Backend**: Django (Python 3.12)
- **Database**: SQLite (for development)
- **Frontend**: HTML5, CSS3, Bootstrap 5, JavaScript
- **Admin Interface**: Django Admin
- **AI**: NVIDIA NOOA with an OpenAI-compatible LLM provider

## Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd veterinary-clinic
   ```

2. **Create and activate a virtual environment**
   ```bash
   python3.12 -m venv venv
   # On Windows
   venv\Scripts\activate
   # On macOS/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**
   ```bash
   python manage.py migrate
   ```

   To enable the chat assistant, configure an OpenAI-compatible provider:
   ```bash
   export OPENROUTER_API_KEY=your-api-key
   export NOOA_CHATBOT_MODEL=openai/your-model
   export NOOA_CHATBOT_API_BASE=https://provider.example/v1
   ```

5. **Create a superuser (admin)**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run the development server**
   ```bash
   python manage.py runserver
   ```

7. **Access the application**
   - Website: http://127.0.0.1:8000/
   - Admin panel: http://127.0.0.1:8000/admin/

## Project Structure

```
veterinary-clinic/
├── clinic/              # Main Django project settings
├── news/                # News management app
├── contacts/            # Contacts and forms app
├── about/               # About page content app
├── chatbot/             # Public read-only NOOA assistant
├── templates/           # HTML templates
├── static/              # CSS, JS, images
├── media/               # User uploaded content
├── requirements.txt     # Python dependencies
└── manage.py            # Django management script
```

## Admin Panel

The Django admin panel allows you to manage:
- News articles
- Contact information
- About page content
- Veterinarian profiles
- Contact form submissions

Content management is intentionally performed through Django Admin. The public
chat assistant can read only bounded public clinic information and has no tools
for creating, updating, or deleting database records.

## Development

To access the admin panel:
1. Run the development server
2. Navigate to http://127.0.0.1:8000/admin/
3. Log in with the superuser credentials created during setup

## Deployment Stages

This project is designed to be implemented in three stages:

1. **Stage 1**: Design, frontend and backend with SQLite (Current stage)
2. **Stage 2**: Docker Compose with PostgreSQL
3. **Stage 3**: Deployment with GitHub Actions

See [docs/implementation-stages.md](docs/implementation-stages.md) for detailed implementation stages.

## Documentation

- [Architecture Plan](docs/architecture.md)
- [Implementation Stages](docs/implementation-stages.md)
