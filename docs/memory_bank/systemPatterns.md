# System Patterns: Veterinary Clinic Website

## Architecture Overview
The project follows the standard Django MVT (Model-View-Template) pattern.

## Component Breakdown
- **`core/`**: Manages site-wide settings, common phrases, and homepage hero/stats.
- **`news/`**: Handles news articles and listing.
- **`contacts/`**: Manages contact information, Yandex Maps integration, and contact form submissions.
- **`about/`**: Manages static content for the about page and veterinarian profiles.
- **`services/`**: Manages service categories and individual services with pricing.
- **`reviews/`**: Manages customer reviews and ratings.
- **`chatbot/`**: (In development) Integration with LangChain and OpenAI for AI assistance.

## Design Patterns
- **Django Admin**: Used for all content management.
- **Bootstrap 5**: Used for responsive frontend styling.
- **Template Inheritance**: Base templates are used to maintain consistency across pages.
- **Singleton Models**: Used for page-specific text models to ensure only one instance exists.
- **Context Processors**: Used to provide global access to site settings and common phrases in all templates.
- **Graceful Fallbacks**: Templates use the `|default` filter to provide fallback text if model data is missing.
