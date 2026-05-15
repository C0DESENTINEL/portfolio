# erikwalther.eu

Personal portfolio and project blog, built with Django and self-hosted on a Hetzner VPS.
Focus areas: security hardening, privacy, and SEO.

**Live site:** [erikwalther.eu](https://erikwalther.eu)

---

## Stack

- **Backend:** Python / Django
- **Server:** Gunicorn + reverse proxy
- **Hosting:** Hetzner VPS (Fedora)
- **Dependencies:** managed with [uv](https://github.com/astral-sh/uv)

---

## Project structure

```
portfolio/      # Django project settings
erikwalther/    # Main app (about, blog)
projects/       # Projects app
templates/      # HTML templates
static/         # CSS, images, and other static assets
```

---

## Local setup

**Requirements:** Python 3.12+, uv, Gunicorn, Caddy

```bash
git clone https://github.com/C0DESENTINEL/portfolio.git
cd portfolio
uv sync
# create a .env file with the SECRET_KEY and the DB_PASSWORD
uv run manage.py migrate
uv run gunicorn portfolio.wsgi
```

Gunicorn binds to a Unix socket (configured in `gunicorn.conf.py`). Configure Caddy to reverse proxy to that socket:

```
your.domain {
    reverse_proxy unix//path/to/portfolio.sock
}
```

> **Note:** Never commit `.env`.
---

## Deployment

The project uses Gunicorn with configuration defined in `gunicorn.conf.py`. Gunicorn binds to a Unix socket rather than a TCP port.

```bash
uv run gunicorn portfolio.wsgi
```

A reverse proxy (e.g. Nginx or Caddy) should be configured to forward requests to the Unix socket.
See the blog post [Hardening my Django Portfolio](https://erikwalther.eu/erikwalthereu/hardening-my-django-portfolio/) for the full security architecture.

---

## Contributing

This is a personal portfolio, so contributions are not expected — but corrections and suggestions are welcome.

1. Open an issue describing the problem or suggestion
2. Fork the repository and create a branch
3. Submit a pull request with a clear description of your changes

Please keep pull requests focused and minimal.

---

## License

This repository uses a dual license:

| Component | License |
|---|---|
| Source code | [GPL-3.0](LICENSE) |
| Site content (text, images) | [CC BY-SA 4.0](https://creativecommons.org/licenses/by-sa/4.0/) |

In short: you are free to use and modify the code, provided you release your modifications under the same terms. Content may be reused with attribution, under the same license.
