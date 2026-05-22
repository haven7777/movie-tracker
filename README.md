# Movie Tracker

#### Description:

I built Movie Tracker because I kept having the same problem — someone would ask me "have you seen
that movie?" and I genuinely had no idea. I'd watched hundreds of things and remembered almost none
of them. I needed a simple place to log what I've seen, slap a rating on it, and move on. So I
built one.

## What It Does

You type in a movie name, it searches the OMDB database and shows you results with posters and
release years. You pick the one you watched, give it a rating, and it gets saved to your personal
list. That's it. No account, no sign-up, no emails. Just a list that's yours.

You can also remove movies from your list if you accidentally added something or just want to
clean things up.

## The Files

### `app.py`

This is where everything actually happens. It's a Flask app with four routes:

- `/` loads your watched list from the database and shows the home page.
- `/search` takes whatever you typed, fires a request to the OMDB API, and shows you the results
  alongside your list.
- `/add` saves a movie to the database. It also checks first if you already added it, so you can't
  end up with duplicates.
- `/delete/<id>` removes a specific movie by its ID. One click and it's gone.

There's also a small `init_db()` function that runs on startup and creates the database table if it
doesn't exist yet — so the first time you run the app, it just works without any manual setup.

### `templates/`

The HTML templates Flask uses to render the pages. The main one handles both the search results
and the watched list on the same page. If you just opened the app, you only see your list. If
you searched something, you see the results at the top and your list below.

### `static/`

The CSS that makes it look decent. Cards for the movie results, a clean search bar, nothing fancy
but nothing ugly either.

### `.env.example`

Shows you what environment variables you need. The real `.env` with the actual API key isn't
committed to the repo — that would be a bad idea.

### `requirements.txt`

Flask, requests, and python-dotenv. Three packages, that's the whole backend.

## Why I Made These Choices

I used SQLite because this is a personal local app and I didn't need anything more complex. No
server to set up, no credentials to manage — it's just a file on your machine. If I were building
this for multiple users I'd switch to something like PostgreSQL, but for this use case SQLite is
honestly perfect.

I used the OMDB API because it gives back clean JSON with poster images included, which made
building the search results UI really easy. The free tier is more than enough for personal use.

One small thing I'm kind of proud of: when you add a movie, it silently skips the insert if you've
already added that title. No error message, no drama — it just does nothing. Felt like the right
call for a tool you're using casually.

The rating defaults to 5 if you don't fill it in. I thought about letting you update ratings later
but decided to keep things simple for now. You rate it when you add it, and that's your record.

## How to Run It

1. Clone the repo
2. Copy `.env.example` to `.env` and add your OMDB API key (free at https://www.omdbapi.com/)
3. `pip install -r requirements.txt`
4. `python app.py`
5. Go to `http://localhost:5000`
