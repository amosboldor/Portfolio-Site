def includeme(config):
    config.add_static_view('static', 'static', cache_max_age=3600)
    config.add_route('home', '/')
    config.add_route("detail", "/blog/{id:\d+}")
    config.add_route("create", "/blog/create")
    config.add_route("update", "/blog/{id:\d+}/edit")
    config.add_route("posts", "/blog")
    config.add_route('login', '/login')
    config.add_route('logout', '/logout')
    config.add_route('api_list', '/api/posts')
    config.add_route('api_post', '/api/posts/{id:\d+}')
