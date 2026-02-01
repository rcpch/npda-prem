# SPEC: npda-prem

## Overview

A web application for accepting and managing form submissions, built with Django and styled using the NHS design system.

## Tech Stack

| Layer    | Technology                  |
| -------- | --------------------------- |
| Backend  | Django (Python)             |
| Database | SQLite (initial)            |
| Frontend | NHS.UK frontend library     |
| Templating | Django templates          |

## NHS Design System

The frontend uses the [NHS.UK frontend library](https://service-manual.nhs.uk/design-system/production) to ensure the application meets NHS service standards.

- **Installation**: via npm (`nhsuk-frontend`)
- **CSS**: BEM naming convention; component-level class-based styling
- **Components**: Use the provided HTML markup patterns with NHS CSS classes
- **Accessibility**: NHS components are built to be accessible and responsive out of the box

Static assets (compiled CSS/JS from the NHS frontend package) will be collected into Django's `staticfiles` directory.

## Application Structure

```
npda-prem/
├── manage.py
├── npda_prem/              # Django project package
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── submissions/            # Django app for form submissions
│   ├── models.py
│   ├── forms.py
│   ├── views.py
│   ├── urls.py
│   └── templates/
│       └── submissions/
├── templates/              # Project-level templates
│   └── base.html           # NHS-styled base template
├── static/                 # Static assets (NHS frontend CSS/JS)
├── node_modules/           # npm dependencies (gitignored)
├── package.json
├── db.sqlite3              # SQLite database (gitignored)
├── requirements.txt
└── SPEC.md
```

## Database

SQLite for initial development. The schema is managed through Django migrations; switching to PostgreSQL later requires only a settings change.

## Submissions App

### Model: `Submission`

Stores each form submission. Exact fields TBD based on the form requirements.

| Field        | Type         | Notes                        |
| ------------ | ------------ | ---------------------------- |
| `id`         | AutoField    | Primary key                  |
| `created_at` | DateTimeField | Auto-set on creation        |
| `updated_at` | DateTimeField | Auto-set on save            |

Additional fields will be defined as the form specification is finalised.

### Views

| URL Pattern      | View             | Method   | Description              |
| ---------------- | ---------------- | -------- | ------------------------ |
| `/`              | `submission_form`| GET/POST | Display and handle form  |
| `/success/`      | `submission_success` | GET  | Confirmation page        |

### Forms

Django `ModelForm` bound to the `Submission` model, with validation logic. The form renders using NHS design system markup in templates.

## Templates

- **`base.html`** — loads NHS frontend CSS/JS, sets up the standard NHS page structure (header, main content, footer)
- **`submissions/form.html`** — the submission form, extending `base.html`
- **`submissions/success.html`** — confirmation page after successful submission

## License

GNU Affero General Public License v3 (AGPL-3.0)
