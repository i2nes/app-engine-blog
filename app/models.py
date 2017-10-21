from google.appengine.ext import ndb


class Article(ndb.Model):

    title1 = ndb.StringProperty()
    title2 = ndb.StringProperty()
    author = ndb.StringProperty()
    slug = ndb.StringProperty()
    content = ndb.TextProperty()
    published = ndb.BooleanProperty(default=False)
    created = ndb.DateTimeProperty(auto_now_add=True)
    updated = ndb.DateTimeProperty(auto_now=True)


class ImageFile(ndb.Model):

    img = ndb.BlobProperty()
    title = ndb.StringProperty()
    url = ndb.StringProperty()
    created = ndb.DateTimeProperty(auto_now_add=True)
    updated = ndb.DateTimeProperty(auto_now=True)


class ContactMessage(ndb.Model):

    name = ndb.StringProperty()
    email = ndb.StringProperty()
    message = ndb.TextProperty()
    created = ndb.DateTimeProperty(auto_now_add=True)
    updated = ndb.DateTimeProperty(auto_now=True)



