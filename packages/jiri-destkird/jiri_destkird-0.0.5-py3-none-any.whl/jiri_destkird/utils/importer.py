def importer():
    """
    Imports all essential DL/CV libraries (plus standard libs) into the global namespace.
    Robust against version conflicts and installation errors.
    """
    import importlib
    import inspect
    import sys

    libs = {
        # --- Standard Libraries ---
        'sys': ('sys', None),
        'inspect': ('inspect', None),
        'importlib': ('importlib', None),
        'os': ('os', None),
        'time': ('time', None),
        'random': ('random', None),
        'math': ('math', None),
        'Counter': ('collections', 'Counter'),
        
        # --- Data Science ---
        'np': ('numpy', None),
        'plt': ('matplotlib.pyplot', None),
        'sns': ('seaborn', None),
        
        # --- PyTorch ---
        'torch': ('torch', None),
        'nn': ('torch', 'nn'),
        'optim': ('torch', 'optim'),
        'F': ('torch.nn', 'functional'),
        'DataLoader': ('torch.utils.data', 'DataLoader'),
        'Dataset': ('torch.utils.data', 'Dataset'),
        'random_split': ('torch.utils.data', 'random_split'),
        
        # --- Torchvision ---
        'torchvision': ('torchvision', None),
        'T': ('torchvision', 'transforms'),
        'models': ('torchvision', 'models'),
        'datasets': ('torchvision', 'datasets'),
        
        # --- Image ---
        'Image': ('PIL', 'Image'),
        
        # --- Sklearn / Metrics ---
        'confusion_matrix': ('sklearn.metrics', 'confusion_matrix'),
        'ConfusionMatrixDisplay': ('sklearn.metrics', 'ConfusionMatrixDisplay'),
        'accuracy_score': ('sklearn.metrics', 'accuracy_score'),
        'precision_score': ('sklearn.metrics', 'precision_score'),
        'recall_score': ('sklearn.metrics', 'recall_score'),
        'f1_score': ('sklearn.metrics', 'f1_score'),
        'TSNE': ('sklearn.manifold', 'TSNE'),
        
        # --- Utils ---
        'tqdm': ('tqdm.notebook', 'tqdm'),
    }

    caller_globals = inspect.stack()[1][0].f_globals
    
    print("⏳ Starting initialization...")
    print("🚀 Loading libraries...")

    success_count = 0
    failed_libs = []

    for alias, (module_name, attribute) in libs.items():
        try:
            mod = importlib.import_module(module_name)
            if attribute:
                caller_globals[alias] = getattr(mod, attribute)
            else:
                caller_globals[alias] = mod
            success_count += 1
        except Exception as e:
        
            failed_libs.append(f"{alias} ({e})")

    print(f"\n✅ Initialization complete. {success_count} modules loaded.")
    
    if failed_libs:
        print("\n⚠️  Warning: The following libraries could not be loaded:")
        for fail in failed_libs:
            print(f"   ❌ {fail}")
    else:
        print("✨ All systems operational!")