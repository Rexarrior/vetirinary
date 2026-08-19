# Progress: Veterinary Clinic Website

## Milestones
- [x] Refactoring Frontend Text to Models (January 2026)
    - Created `core` app for site-wide settings and common phrases.
    - Implemented page-specific text models for all thematic apps.
    - Added `site_content` context processor for global text access.
    - Refactored templates to use dynamic content.
    - Implemented singleton admin behavior for content management.
- [x] Public Chatbot Migration to NOOA (August 2026)
    - Migrated orchestration to NVIDIA NOOA.
    - Kept only bounded read-only clinic data sources.
    - Retained veterinary-only web search and medical safety guidance.
    - Removed the autonomous database administration agent.
