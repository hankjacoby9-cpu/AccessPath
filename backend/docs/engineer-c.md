# Engineer C. AI processing

**Your job in one sentence.** Turn Markdown and pictures into typed nodes with a first AI draft and a confidence score.

## Your folder
`apps/pipeline/`

## Already done
- `LLMCall`, a table that logs every AI call and its cost (`apps/pipeline/models.py`).
- The model router. Cheap model for images and graphs, strong model for the rest (`apps/pipeline/router.py`).
- An example of the node XML (`apps/pipeline/schema/example.xml`).
- Empty functions waiting for you, `process_document` in `tasks.py` and `revise` in `service.py`.

## Read these first, in order
1. `apps/pipeline/schema/example.xml`. Your output format. You own it.
2. `apps/uploads/models.py`, the `ParsedDocument` comment. That is your input.
3. `apps/review/models.py`, `Node` and `NodeVersion`. That is what you create.
4. The Anthropic Python SDK docs on structured outputs.

## Your first tasks
1. **Lock the XML format (week 1).** Finalize `example.xml` and write down every tag and attribute.
   Engineers D and E build against it, so this goes first.
2. **First prompt.** Take one of Engineer B's Markdown outputs and get the model to return nodes.
   Ask for structured output (a fixed JSON shape) and build the XML yourself, so it can never be broken.
3. **process_document.** Turn the result into `Node` and `NodeVersion` rows. Log every call in `LLMCall`.
4. **Tests that don't cost money.** Fake the AI response in tests. Only the evaluation set calls the real model.

## Who you work with most
Engineer B (your input) and Engineer D (who calls `revise` when a professor sends a node back).
Your API key goes in `.env` as `ANTHROPIC_API_KEY`. Never commit it.
