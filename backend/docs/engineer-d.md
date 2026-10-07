# Engineer D. Review

**Your job in one sentence.** Build everything a TA and professor do while reviewing nodes. This is the core of the product.

## Your folder
`apps/review/`

## Already done
- The models. `Node`, `NodeVersion`, `Comment`, `ReviewAction` (`apps/review/models.py`).
- The state machine, which decides what can happen to a node and who can do it, including bulk approve
  (`apps/review/state_machine.py`, with tests).
- `python manage.py seed_demo`, which gives you 6 real nodes to work with right away.

## Read these first, in order
1. `apps/review/models.py`. Notice `NodeVersion.save` refuses edits. Versions are only ever added.
2. `apps/review/state_machine.py`. The `TRANSITIONS` table is the whole review process on one screen.
3. `apps/review/tests/test_state_machine.py`.
4. The frontend's current contract, `README.md` in the old demo (ask Ethan). It lists the endpoints the screens already call.

## Your first tasks
1. **Node list and detail.** `GET /classes/:id/nodes` with filters, and `GET /nodes/:id` with its current
   version, comments and history. Use the seed data to test by hand.
2. **The queue.** `GET /classes/:id/queue` shows TAs nodes in `ta_review` and professors nodes in
   `prof_review`, lowest confidence first.
3. **Actions.** `approve`, `flag`, `send-back`, `bulk-approve`, all calling `transition()` or `bulk_approve()`.
   Never set `node.state` yourself.
4. **Edits.** `POST /nodes/:id/versions` adds a new `NodeVersion` and points the node at it.

## Who you work with most
The frontend team (you own the endpoints they use most) and Engineer C (you call `pipeline.service.revise`).
