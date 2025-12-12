

_pending_provider_managers = []

def provider_manager(obj):
    _pending_provider_managers.append(obj)
    print(f"provider_manager called  {obj}")
    return obj
