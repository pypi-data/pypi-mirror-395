
def setup(app):
    app.add_object_type(directivename="reactcontext", rolename="reactcontext", indextemplate="pair: %s; reactcontext")
    app.add_object_type(directivename="reactcomponent", rolename="reactcomponent", indextemplate="pair: %s; reactcomponent")
