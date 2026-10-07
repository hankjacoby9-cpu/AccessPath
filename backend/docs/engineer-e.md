# Engineer E. Export and accessibility

**Your job in one sentence.** Turn an approved lecture into an HTML page that really works for a blind or low-vision student.

## Your folder
`apps/exports/`

## Already done
- The `Export` model (`apps/exports/models.py`).
- An empty task waiting for you, `build_html_export` in `apps/exports/tasks.py`.
- `python manage.py seed_demo` gives you approved and nearly approved nodes of every kind.

## Read these first, in order
1. `apps/pipeline/schema/example.xml`. The kinds of content you will turn into HTML.
2. `apps/review/models.py`. You read `Node` and its `current_version`. You never change them.
3. WCAG 2.2 AA quick reference, https://www.w3.org/WAI/WCAG22/quickref/

## Your first tasks
1. **Write the rules (week 1).** One page saying what each node kind needs to be accessible.
   For example, an image needs short alt text and a longer description. An equation needs MathML.
   A table needs header cells. Save it as `docs/accessibility-rules.md`.
2. **Build the target by hand.** Write the perfect HTML page for `example.xml` by hand. That is what
   your code has to produce.
3. **Render each kind.** One function per node kind that returns HTML. For equations, try the
   `latex2mathml` package. Test each one against the seed data.
4. **Check it.** Add an automated accessibility check on the output, and test with VoiceOver (Mac) or
   NVDA (Windows) yourself.

## Who you work with most
Engineer D (you export what they approve) and Engineer C (you help build the quality rubric for the evaluation set).
