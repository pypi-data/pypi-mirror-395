# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.0.0] - 2024-12-06

### Added
- Initial release of DRF API Documentation Generator
- Support for generating PDF documentation with professional styling
- Support for generating HTML documentation with dark theme and sidebar navigation
- Support for generating OpenAPI 3.0 JSON documentation
- Django management command `generate_api_docs` for easy usage
- Auto-detection of API endpoints from URL patterns
- Extraction of serializer fields with types, constraints, and descriptions
- Authentication and permission class detection
- Query parameter and filter backend support
- Pagination parameter detection
- Custom configuration via `API_DOCS_CONFIG` in Django settings
- Command line options for title, version, description, output format, and directory
- Support for Django 3.2, 4.0, 4.1, 4.2, and 5.0
- Support for Python 3.8, 3.9, 3.10, 3.11, and 3.12

### Features
- **PDF Output**: Professional multi-page PDF with cover page, table of contents, and detailed endpoint documentation
- **HTML Output**: Interactive dark-themed documentation with syntax highlighting and responsive design
- **JSON Output**: OpenAPI 3.0 compliant specification for Swagger UI and Postman compatibility
- **Auto-detection**: Automatically discovers API views, serializers, authentication, and permissions
- **Multiple Apps**: Generate docs for one, multiple, or all Django apps
- **Customizable**: Configure title, version, description, theme color, and logo
