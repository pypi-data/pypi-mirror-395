# fedkit

# fedkit: ActivityPub & ActivityStreams for Python & Django

**fedkit** is a Python library built to enable easy integration of the **ActivityStreams** and **ActivityPub** federation protocols into Python-built websites, with a particular focus on the **Django** framework.

It allows your application to participate in the Fediverse, enabling seamless communication with other federated services like Mastodon, Pleroma, and PeerTube.

-----

## ✨ (Planned) Features

  - [ ] **ActivityStreams Object Handling:** Simple and declarative Python classes for creating, validating, and serializing **ActivityStreams** objects.
  - [ ] **ActivityPub Protocol Support:** Tools for handling **Inboxes**, **Outboxes**, and remote actor discovery (WebFinger).
  - [ ] **Django Integration:** Built-in utilities, database models, and view helpers to quickly add federation capabilities to your existing Django project.
  * [ ] **Decoupled Design:** Core federation logic can be used in any Python web framework (Flask, FastAPI, etc.).

-----

## 🚀 Installation

You can install `fedkit` directly using pip:

```bash
pip install fedkit
```

### Django Setup

1.  **Add to `INSTALLED_APPS`**:
    To integrate `fedkit` into your Django project, add it to your `settings.py`:

    ```python
    # settings.py

    INSTALLED_APPS = [
        # ... your other apps
        'fedkit',
        # ...
    ]
    ```

2.  **Include URLs**:
    Add the `fedkit` URLs to your project's `urls.py` to handle standard ActivityPub routes (like actor inboxes/outboxes):

    ```python
    # urls.py

    from django.urls import path, include

    urlpatterns = [
        # ... your other URLs
        path('@', include('fedkit.urls')),
    ]
    ```

3.  **Run Migrations**:
    Apply the necessary database migrations:

    ```bash
    python manage.py migrate
    ```

-----

## ⚙️ Basic Usage

### 1\. Defining a Federating Model

You can extend the built-in `fedkit` Actor and Object models to make your application's entities addressable in the Fediverse.

```python

```

### 2\. Creating an Activity

Use the dedicated utilities to create and sign an Activity, then deliver it to an Outbox.

```python

```

-----

## 📖 Documentation & Examples

For detailed instructions on configuring federation settings, customizing views, handling **Inboxes**, and implementing full server-to-server communication, please refer to the official documentation (coming soon).

-----

## 🤝 Contributing

**fedkit** is an open-source project and contributions are highly welcome\!

If you'd like to contribute, please check out the repository on Codeberg, fork the project, and submit a pull request with your suggested changes. You can also report issues or suggest features via the issue tracker.

-----

## ⚖️ License

This project is licensed under the **[LICENSE\_HERE]** License.

Please see the `LICENSE` file in the repository for more details.