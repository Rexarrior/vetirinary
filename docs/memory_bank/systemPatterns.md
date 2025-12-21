# System Patterns: Veterinary Clinic Website

## Architecture Overview
The project follows the standard Django MVT (Model-View-Template) pattern.

## Component Breakdown
- **`clinic/`**: Project configuration and settings.
- **`news/`**: Handles news articles and listing.
- **`contacts/`**: Manages contact information, Yandex Maps integration, and contact form submissions.
- **`about/`**: Manages static content for the about page and veterinarian profiles.
- **`chatbot/`**: (In development) Integration with LangChain and OpenAI for AI assistance.

## Design Patterns
- **Django Admin**: Used for all content management.
- **Bootstrap 5**: Used for responsive frontend styling.
- **Template Inheritance**: Base templates are used to maintain consistency across pages.
