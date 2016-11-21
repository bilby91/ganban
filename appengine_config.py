from google.appengine.api.modules.modules import get_current_module_name


# Sets the namespace to service specified in app.yaml
def namespace_manager_default_namespace_for_request():
    if get_current_module_name() == "default":
        return None
    else:
        return get_current_module_name()
