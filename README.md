# sajansachdeva.com

Personal site. Plain HTML, built by `build.py`, served by GitHub Pages from `docs/`.

## Add an essay

1. Create `posts/YYYY-MM-DD-short-name.md` starting with:

   ```
   title: Essay title
   dek: One line shown under the title.
   date: YYYY-MM-DD
   slug: short-name
   ---
   ```

   then the essay in Markdown. Images go in `static/img/` and are referenced as `/img/file.png`.
2. Run `python3 build.py` (needs `pip install markdown`).
3. Commit and push. The site updates in about a minute.

Edit the home intro and About page in `build.py`; styles are in `static/style.css`.
