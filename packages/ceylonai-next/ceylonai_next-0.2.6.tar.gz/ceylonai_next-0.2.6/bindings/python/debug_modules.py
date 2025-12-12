import sys
print(f"Path: {sys.path}")
try:
    import ceylonai_next
    print("Successfully imported ceylonai_next (top-level)")
    print(dir(ceylonai_next))
except ImportError as e:
    print(f"Failed to import ceylonai_next: {e}")

try:
    import ceylon
    print("\nSuccessfully imported ceylon")
    print(f"ceylon file: {ceylon.__file__}")
    try:
        from ceylon import ceylonai_next
        print("Successfully imported ceylon.ceylonai_next")
    except ImportError as e:
        print(f"Failed to import ceylon.ceylonai_next: {e}")
except ImportError as e:
    print(f"Failed to import ceylon: {e}")
