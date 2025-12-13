# Django Cotton BS5

Bootstrap 5 components for Django Cotton - A comprehensive library of reusable, modular components.

**Note:** This project is currently a work in progress. Users are encouraged to request new components or features via the [issue tracker](https://github.com/SamuelJennings/cotton-bs5/issues).

[View demo](https://samueljennings.github.io/cotton-bs5/)

## Installation

```bash
pip install django-cotton-bs5
```

Add `cotton_bs5` to your `INSTALLED_APPS` in `settings.py`:

```python
INSTALLED_APPS = [
    ...
    "django_cotton",
    "cotton_bs5",
    ...
]
```

## Available Components

The following Bootstrap 5 components are currently available as Django Cotton components:

- **Alert** (`<c-alert>`) — Bootstrap alerts with variants, dismissible, slot/text support
- **Accordion** (`<c-accordion>`, `<c-accordion.item>`, `<c-accordion.header>`) — Collapsible accordion panels
- **Breadcrumbs** (`<c-breadcrumbs>`, `<c-breadcrumbs.item>`) — Navigation breadcrumbs
- **Button** (`<c-button>`) — Button/link with variants, outline, icon, slot/text
- **Button Group** (`<c-button_group>`) — Grouped buttons, vertical/size/label support
- **Card** (`<c-card>`, `<c-card.body>`, `<c-card.title>`) — Card container, body, and title
- **List Group** (`<c-list_group>`, `<c-list_group.item>`) — List group and items, horizontal/numbered/active/disabled
- **Modal** (`<c-modal>`, `<c-modal.title>`, `<c-modal.body>`) — Modal dialog, title, and body
- **Navbar** (`<c-navbar>`) — Responsive navigation bar with brand, expand, toggler
- **Progress** (`<c-progress>`) — Progress bar with value, min/max, variant, striped, animated, label
- **Spinner** (`<c-spinner>`) — Loading spinner, border/grow, size, variant, label
- **Table** (`<c-table>`) — Responsive table, striped, bordered, hover, small, variant, caption
- **Tabs** (`<c-tabs>`, `<c-tabs.item>`, `<c-tabs.pane>`) — Tab navigation and tab panes

More components are planned. Please request additional Bootstrap 5 components or features via the [issue tracker](https://github.com/SamuelJennings/cotton-bs5/issues).

## Contributing

This library follows django-cotton conventions and Bootstrap 5 standards. When adding new components:

1. Use `<c-vars />` for default values
2. Include proper accessibility attributes
3. Support all relevant Bootstrap 5 options
4. Maintain consistent naming conventions
5. Test with various configurations

## License

MIT License - see [LICENSE](LICENSE) file for details.
