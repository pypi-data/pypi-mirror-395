"""Integration test for MouseAnatomy model EMAPA lookup."""

import sys
from aind_data_schema_models.mouse_anatomy import MouseAnatomy


def main():
    """Main function to test MouseAnatomy integration"""
    try:
        # This will trigger a real call to the EMAPA database
        heart = MouseAnatomy.HEART
        print(
            f"MouseAnatomy.HEART: name={heart.name}, registry={heart.registry}"
            f", registry_identifier={heart.registry_identifier}"
        )
        assert heart.name.lower() == "heart"
        assert heart.registry.name == "EMAPA"
        assert heart.registry_identifier is not None and heart.registry_identifier != ""
        print("MouseAnatomy integration test passed.")
    except Exception as e:
        print(f"MouseAnatomy integration test failed: {e}", file=sys.stderr)
        sys.exit(1)


if __name__ == "__main__":
    main()
