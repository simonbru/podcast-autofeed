# Run in production

Assuming we want to run the app at https://foo.bar/podcasts

## HTTP

```bash
export BASE_URL=https://foo.bar
export PODCAST_DIR=/var/podcasts

uv run uwsgi \
    --http :8006 \
    --processes 1 \
    --threads 5 \
    --manage-script-name \
    --mount "/podcasts=app.py"
```

# Usage

The podcast feed is available at */feed* (i.e. https://foo.bar/podcasts/feed in the example above)