Blog Post Management (CRUD)
---------------------------
Endpoints:
- /posts/            -> list all posts
- /posts/new/        -> create new post (login required)
- /posts/<pk>/       -> view post detail
- /posts/<pk>/edit/  -> edit post (author only)
- /posts/<pk>/delete/-> delete post (author only)

Permissions:
- Create: authenticated users only.
- Update/Delete: only the post's author (UserPassesTestMixin).
- List/Detail: public.

Notes:
- Author is automatically attached in PostCreateView.form_valid().
- Always include {% csrf_token %} in templates.
- Configure LOGIN_URL and redirect settings in settings.py.

Comments feature
----------------
- Model: Comment(post, author, content, created_at, updated_at)
- Routes:
  - POST /posts/<post_pk>/comments/new/ -> create comment (login required)
  - GET/POST /comments/<pk>/edit/ -> edit comment (author only)
  - GET/POST /comments/<pk>/delete/ -> delete comment (author only)

Usage:
- Authenticated users can post comments from the post detail page.
- Only comment authors can edit/delete their comments.
- Comments appear under the related post, ordered ascending by creation time.
