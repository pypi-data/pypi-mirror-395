import inspect
import os
import re
import sys
from importlib import import_module


from contextlib import ExitStack
from functools import wraps
from fastapi import APIRouter, Request


def cached_import(module_path, class_name):
    # Check whether module is loaded and fully initialized.
    if not (
        (module := sys.modules.get(module_path))
        and (spec := getattr(module, "__spec__", None))
        and getattr(spec, "_initializing", False) is False
    ):
        module = import_module(module_path)
    return getattr(module, class_name)


def import_string(dotted_path):
    """
    Import a dotted module path and return the attribute/class designated by the
    last name in the path. Raise ImportError if the import failed.
    """
    try:
        module_path, class_name = dotted_path.rsplit(".", 1)
    except ValueError as err:
        raise ImportError("%s doesn't look like a module path" % dotted_path) from err

    try:
        return cached_import(module_path, class_name)
    except AttributeError as err:
        raise ImportError(
            'Module "%s" does not define a "%s" attribute/class'
            % (module_path, class_name)
        ) from err


def module_dir(module):
    """
    Find the name of the directory that contains a module, if possible.

    Raise ValueError otherwise, e.g. for namespace packages that are split
    over several directories.
    """
    # Convert to list because __path__ may not support indexing.
    paths = list(getattr(module, "__path__", []))
    if len(paths) == 1:
        return paths[0]
    else:
        filename = getattr(module, "__file__", None)
        if filename is not None:
            return os.path.dirname(filename)
    raise ValueError("Cannot determine directory containing %s" % module)

def wrap_with_layouts(view_func, layout_modules):
    """
    View fonksiyonunu layout context manager'ları ile sarmalar.
    Hem async/sync desteği sağlar hem de layout'lara 'request' nesnesini enjekte eder.
    """
    
    def get_request_from_args(args, kwargs):
        """Fonksiyon argümanları arasından Request nesnesini bulur."""
        # 1. Kwargs içinde ara (FastAPI genelde buraya koyar)
        if "request" in kwargs and isinstance(kwargs["request"], Request):
            return kwargs["request"]
        
        # 2. Positional args içinde ara
        for arg in args:
            if isinstance(arg, Request):
                return arg
        return None

    def apply_layouts(stack, args, kwargs):
        """Layoutları sırasıyla stack'e ekler ve request enjeksiyonu yapar."""
        request_obj = get_request_from_args(args, kwargs)

        for layout_module in layout_modules:
            if hasattr(layout_module, 'layout'):
                layout_func = layout_module.layout
                
                # Layout fonksiyonunun parametrelerini incele
                sig = inspect.signature(layout_func)
                layout_kwargs = {}
                
                # Eğer layout 'request' parametresi istiyorsa ve elimizde varsa gönder
                if "request" in sig.parameters:
                    if request_obj:
                        layout_kwargs["request"] = request_obj
                    else:
                        # Layout request istiyor ama page fonksiyonunda request yoksa uyarı verilebilir
                        # veya None gönderilebilir. Şimdilik hata oluşmaması için geçiyoruz.
                        print(f"Uyarı: {layout_module.__name__} request istiyor ancak sayfaya request gelmedi.")
                
                # Layout context'ini aç
                stack.enter_context(layout_func(**layout_kwargs))

    # --- Wrapper (Async) ---
    if inspect.iscoroutinefunction(view_func):
        @wraps(view_func)
        async def wrapper(*args, **kwargs):
            with ExitStack() as stack:
                apply_layouts(stack, args, kwargs)
                return await view_func(*args, **kwargs)
        return wrapper

    # --- Wrapper (Sync) ---
    else:
        @wraps(view_func)
        def wrapper(*args, **kwargs):
            with ExitStack() as stack:
                apply_layouts(stack, args, kwargs)
                return view_func(*args, **kwargs)
        return wrapper

def find_parent_layouts(module_name):
    """
    Verilen modül isminden (örn: app.dashboard.settings.page) yola çıkarak
    kök dizine kadar olan tüm layout.py modüllerini import edip listeler.
    Sıralama: Root Layout -> ... -> Current Folder Layout
    """
    parts = module_name.split('.')
    # Son eleman 'page' olduğu için onu atıyoruz
    parts = parts[:-1] 
    
    layouts = []
    
    # Kümülatif olarak path oluşturup layout kontrolü yapıyoruz
    # Örn: app -> app.dashboard -> app.dashboard.settings
    current_path_parts = []
    for part in parts:
        current_path_parts.append(part)
        layout_module_name = ".".join(current_path_parts) + ".layout"
        
        try:
            # Modülü import etmeyi dene
            mod = import_module(layout_module_name)
            # İçinde 'layout' adında bir fonksiyon var mı?
            if hasattr(mod, 'layout'):
                layouts.append(mod)
        except ImportError:
            # Layout dosyası yoksa pas geç
            pass
            
    return layouts

def autodiscover_modules(router: APIRouter, app_path: str):
    module_map = {}
    pattern = r'/(.*?)\((.*?)\)(.*)'
    
    for root, dirs, files in os.walk(app_path):
        for file in files:
            if file in ("page.py", "layout.py", "route.py"):
                module_path = os.path.join(root, file)
                module_name = os.path.splitext(os.path.relpath(module_path, app_path).replace(os.sep, '.'))[0]  
                module_name = f"app.{module_name}"              
                
                try:
                    module = import_module(module_name)
                    
                    # URL oluşturma mantığı (sizin kodunuzdan)
                    module_url = "/%s" % "/".join(module_name.split(".")[1:-1]) 
                    module_url = module_url.replace("[", "{").replace("]", "}")
                    match = re.search(pattern, module_url)
                    if match:
                        module_url = f"{match.group(1)[:-1]}{match.group(3)}"
                    if not module_url.startswith("/"):
                        module_url = f"/{module_url}"
                    
                    module_map[module_name] = module_url, module

                    # --- PAGE.PY MANTIĞI ---
                    if module_name.endswith(".page"):
                        module_index_handler = getattr(module, "index", None)
                        
                        if module_index_handler:
                            # 1. Bu sayfanın üstündeki layoutları bul
                            layouts = find_parent_layouts(module_name)
                            
                            # 2. Handler'ı layoutlarla sarmala
                            wrapped_handler = wrap_with_layouts(module_index_handler, layouts)
                            
                            # 3. Router'a wrapped_handler'ı ekle
                            router.add_api_route(
                                module_url, 
                                wrapped_handler, 
                                methods=["GET"]
                            )
                        
                    # --- ROUTE.PY MANTIĞI (API Endpointleri) ---
                    elif module_name.endswith(".route"):
                        # Sizin mevcut route mantığınız aynen korunuyor
                        methods = ["GET", "POST", "DELETE", "PUT", "PATCH"]
                        for method in methods:
                            handler = getattr(module, method, None)                        
                            if handler:
                                router.add_api_route(module_url, handler, methods=[method])
                                
                        # Class based endpoint mantığı (kısaltıldı)
                        # ...

                except Exception as ex:
                    print(f"Error processing {module_name}: {ex}")

    return module_map



