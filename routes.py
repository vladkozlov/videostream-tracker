def setup_routes(app, handler, root_dir):
    router = app.router
    
    router.add_post('/watching', handler.watching, name='watching')
    router.add_get('/customer/{customer_id}', handler.customer_status, name='customer')
    router.add_get('/video/{video_id}', handler.video_status, name='video')