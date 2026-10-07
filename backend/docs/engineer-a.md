# Engineer A. Platform and identity

**Your job in one sentence.** Make sure the right people can log in and only ever see their own classes.

You go first, because every other lane builds on your work.

## Your folders
`config/`, `apps/accounts/`, `apps/classes/`, `apps/storage/`

## Already done
- Login, logout, "who am I", onboarding answers (`apps/accounts/views.py`)
- Creating classes, listing members, changing roles, removing people (`apps/classes/views.py`)
- The rule that a class always has a professor (`apps/classes/services.py`, with tests)
- The S3 helper functions (`apps/storage/s3.py`)

## Read these first, in order
1. `apps/classes/models.py`. Class, ClassMembership, Invite, Lecture.
2. `apps/classes/services.py`. How membership changes are made safely.
3. `apps/classes/permissions.py`. How a view checks you belong to a class.
4. `apps/classes/tests/test_api.py`. How we test an endpoint end to end.

## Your first tasks
1. **Invites.** `POST /classes/:id/invites` creates an `Invite` with a random token (store only its
   sha256 hash). `POST /invites/:token/accept` creates the `ClassMembership`. Only professors can invite.
2. **Lecture detail.** `GET`, `PATCH` and `DELETE` for one lecture, so a TA can edit `ta_context`.
3. **A leak test.** For every class endpoint, add a test that a user from a different class gets a 403.
4. Later, Purdue email verification (week 5) and the staging server on AWS (week 6).

## Who you work with most
Everyone, because they all use your permissions and S3 helpers. Engineer B uses `presign_upload`
first, so check in with them in week 1.
