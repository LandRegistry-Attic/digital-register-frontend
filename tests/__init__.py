from service import server  # type: ignore

server.app.config['DISABLE_CSRF_PREVENTION'] = True
