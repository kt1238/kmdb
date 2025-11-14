# KMDB AI Coding Agent Instructions

## Project Overview
**KMDB** (Kevin's Movie Database) is a Django 5.0 web application for managing a personal movie watchlist. Users can add, search, update, and delete movies from an SQLite database. The app is deployed on PythonAnywhere.

**Stack**: Django 5.0, SQLite3, Bootstrap (in templates), Python 3.9+

## Architecture & Data Flow

### Application Structure
- **Single Django App**: `demo/` (movie watchlist app)
- **Database**: SQLite3 (`db.sqlite3`) - single model: `Movie`
- **Core Model** (`demo/models.py`): `Movie` with 8 fields (name, release_year, language, genre_1, watched, priority, extra_info)
- **Views** (`demo/views.py`):
  - `home()` - landing page (function-based)
  - `MovieView` (class-based ListView) - list all movies
  - `details()` - movie detail view
  - `search()` - filter by name, genre, or release year (handles both numeric year searches and text searches)
  - `random_movie()` - redirect to random movie detail

### URL Routing (`kmdb/urls.py`)
Routes are simple and predictable:
- `/` → home
- `/movies/` → all movies list
- `/movies/<id>` → movie details
- `/search/` → search results (POST with `search_term`)
- `/random/` → random movie redirect
- `/admin/` → Django admin

### Templates & Frontend
- **Bootstrap CSS** used for styling (via CDTags in base template `home.html`)
- Template inheritance: all templates extend `home.html`
- **Key files**: `all.html` (movie table with links), `details.html` (single movie view), `search.html` (results)
- **Static CSS** (`style.css`): hover effects and transitions; minimal custom styling

## Critical Developer Workflows

### Running the Application
```bash
# Start development server
python manage.py runserver

# Access at http://127.0.0.1:8000/
```

### Loading Data
Use the `load.py` script **via Django shell** (not as standalone script):
```bash
python manage.py shell
>>> exec(open('load.py').read())
>>> loadcsvfile()  # Expects CSV at C:/ProgramData/MySQL/MySQL Server 8.0/Uploads/movies.csv
```
The script uses `update_or_create()` to avoid duplicate entries. Handles NULL release_year values.

### Database Migrations
Migrations tracked in `demo/migrations/`. Apply with:
```bash
python manage.py migrate
```
Key migration history:
- `0001_initial.py` - initial schema
- `0002_alter_movie_release_year.py` - release_year field changes
- `0003_remove_movie_movie_id_movie_id.py` - removed custom pk, now uses auto-generated id

### Admin Interface
Accessible at `/admin/`. Custom admin class in `demo/admin.py` adds searchability by movie name. Use for testing CRUD operations.

## Project-Specific Patterns & Conventions

### Search Implementation (Important)
`search()` view has a unique pattern - it combines three independent QuerySet filters with the OR operator (`|`):
```python
# Searches name AND genre_1, plus optionally release_year if numeric
result = Movie.objects.filter(name__contains=search_term) | 
         Movie.objects.filter(genre_1__contains=search_term) | 
         year_query
```
- **Case-insensitive** text search (Django default)
- **Numeric input** triggers year filter; non-numeric ignores year
- Note: `search_term` relies on form POST data; no error handling for missing keys

### Field Naming
- `genre_1` (not `genre`) - singular genre field, extensible for future `genre_2`, etc.
- Boolean fields: `watched` (not `is_watched`)

### Template Context Pattern
Views pass explicit context dicts to templates:
```python
context = {'movie': movie}  # or {'search_term': term, 'result': queryset}
```
No implicit context passing - all data explicitly named for template clarity.

## Integration Points & External Dependencies

### OMDb API Integration
The app fetches enriched movie metadata from the **OMDb API** (`demo/omdb_client.py`):
- **Base URL**: `http://www.omdbapi.com/`
- **API Key**: `508e4d85` (hardcoded in `omdb_client.py` - should use environment variable in production)
- **Two main functions**:
  - `get_movie_info(title)` - Searches by movie title, returns first match with poster & year
  - `get_movie_by_imdb_id(imdb_id)` - Fetches detailed data (plot, rating) by IMDb ID
- **Error handling**: Both functions catch `RequestException` and `ValueError`, return `None` on failure
- **Integration point**: `details()` view calls `get_movie_info(movie.name)` and passes results to template
- **Template usage**: `details.html` conditionally displays poster image, IMDb ID, plot, and rating if data available
- **Dependency**: Requires `requests` library (installed in venv)

### Static Files
- `STATIC_URL = '/static/'` and `STATIC_ROOT = BASE_DIR / 'static'` (settings.py)
- CSS served from `demo/static/style.css`
- Uses Bootstrap CDN (loaded in base template)

### Settings Configuration
- **DEBUG = True** (hardcoded - change before production)
- **ALLOWED_HOSTS = ['*']** (permissive - fine for learning, tighten in production)
- **SECRET_KEY** hardcoded in settings (should use environment variable; legacy comment shows attempted file-based approach)

## Common Tasks for AI Agents

### Adding a Feature
1. Update `Movie` model in `demo/models.py` if needed
2. Create migration: `python manage.py makemigrations`
3. Apply migration: `python manage.py migrate`
4. Add view function/class in `demo/views.py`
5. Add route in `kmdb/urls.py`
6. Create or update template in `demo/templates/`
7. Update admin class in `demo/admin.py` if searchability needed

### Fixing Search
Search can return NULL release_years without error handling. If search fails on edge cases:
- Check `request.POST['search_term']` exists before access
- Handle empty strings gracefully
- Consider database constraints on nullable fields

### Debugging
- Use `python manage.py shell` for interactive queries
- Check `db.sqlite3` directly if needed (SQLite browser)
- All views return HTML; no API endpoints currently exist

## Deployment Notes
- App hosted on **PythonAnywhere** (https://kevlar12345.pythonanywhere.com/)
- SQLite is acceptable for single-user learning project; not suitable for scale
- Static files must be collected before deployment: `python manage.py collectstatic`
