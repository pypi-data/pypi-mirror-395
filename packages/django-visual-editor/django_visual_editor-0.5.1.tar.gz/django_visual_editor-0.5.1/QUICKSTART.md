# Quick Start

Quick start guide for Django Visual Editor.

## 1. Install Dependencies

```bash
# Install Python dependencies
uv sync

# Go to frontend directory
cd frontend

# Install Node.js dependencies
npm install
```

## 2. Build Frontend

```bash
# From the frontend directory
npm run build
```

After building, files will appear in `django_visual_editor/static/django_visual_editor/js/`

## 3. Run Example Project

```bash
# Go back to project root
cd ..

# Go to example_project
cd example_project

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run server
python manage.py runserver
```

## 4. Open in Browser

- **Blog homepage**: http://localhost:8000/
- **Create post**: http://localhost:8000/post/new/ (login required)
- **Django Admin**: http://localhost:8000/admin/

## 5. Test the Editor

1. Login through the admin panel
2. Create a new post at http://localhost:8000/post/new/
3. Try:
   - Font selection (dropdown in toolbar)
   - Font size selection (dropdown in toolbar)
   - Text formatting (Bold, Italic, Underline, Strikethrough)
   - Creating headings (H1, H2, H3)
   - Lists (bulleted and numbered)
   - Code:
     - Inline code (click `<code>` button) - toggle on/off
     - Code blocks (click `{ }` button) for multi-line code
   - Image upload (drag-and-drop or button)
     - Click on uploaded images to resize and align them
     - Use preset sizes: S (25%), M (50%), L (75%), XL (100%)
     - Align images: left, center, or right
     - Drag the resize handle to custom size
   - Creating links
   - Clear formatting (✕ button)
   - Undo/Redo (↶ ↷ buttons)
   - HTML Source mode (click </> button)
   - Keyboard shortcuts: Ctrl+B, Ctrl+I, Ctrl+U, Ctrl+Z, Ctrl+Y

## Frontend Development

For development with automatic rebuild:

```bash
cd frontend
npm run dev
```

Webpack will watch for changes and automatically rebuild files.

## Cleanup Unused Images

```bash
cd example_project

# Show what will be deleted
python manage.py cleanup_editor_images --dry-run

# Delete unused images
python manage.py cleanup_editor_images
```

## File Structure

```
django-visual-editor/
├── django_visual_editor/       # Main Django application
│   ├── models.py              # EditorImage model
│   ├── widgets.py             # VisualEditorWidget
│   ├── views.py               # View for uploads
│   └── static/                # Compiled JS/CSS
├── frontend/                  # TypeScript sources
│   ├── src/
│   │   ├── editor/           # Editor and toolbar
│   │   ├── utils/            # Upload and HTML compression
│   │   └── styles/           # CSS
│   └── package.json
└── example_project/           # Usage example
    └── blog/                 # Blog with VisualEditor
```

## Troubleshooting

### Error uploading images

Check:
1. Is Pillow installed: `pip install Pillow`
2. Are MEDIA_ROOT and MEDIA_URL configured in settings.py
3. Are media URLs added to urls.py for DEBUG mode

### Editor not displaying

Check:
1. Is frontend built: `cd frontend && npm run build`
2. Does file `django_visual_editor/static/django_visual_editor/js/editor.bundle.js` exist
3. Is `{{ form.media }}` added to the template

### TypeScript errors during build

```bash
cd frontend
npm install
npm run type-check
```
