def test_mesh_creation():
    """Test creating a LocalMesh instance."""
    try:
        mesh = ceylon.PyLocalMesh("test-mesh")
        print("✓ Successfully created PyLocalMesh instance")
        print(f"  Mesh type: {type(mesh)}")
    except Exception as e:
        print(f"✗ Failed to create PyLocalMesh: {e}")

if __name__ == "__main__":
    print("Testing Ceylon Python Bindings\n" + "="*40)
    test_basic_import()
    print()
    test_mesh_creation()
    print("\n" + "="*40)
    print("All tests completed!")
