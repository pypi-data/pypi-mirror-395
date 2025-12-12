import ceylon
import ceylon.ceylon
print("Content of ceylon package:")
print(dir(ceylon))
print("\nContent of ceylon.ceylon extension:")
print(dir(ceylon.ceylon))

try:
    from ceylon.ceylon import PyRedisBackend
    print("\nPyRedisBackend found in extension.")
except ImportError:
    print("\nPyRedisBackend NOT found in extension.")
