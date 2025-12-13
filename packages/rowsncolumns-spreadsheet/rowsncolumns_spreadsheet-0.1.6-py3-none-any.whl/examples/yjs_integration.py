"""
Example showing how to use the Python spreadsheet library with YJS.

This demonstrates the workflow:
1. Load data from YJS document
2. Perform spreadsheet operations
3. Generate patches
4. Apply patches to YJS document

Note: This example shows the Python side. You'd need corresponding
JavaScript/TypeScript code to handle the YJS document.
"""

import json
from typing import Dict, Any, List
from rowsncolumns_spreadsheet.interface import SpreadsheetInterface
from rowsncolumns_spreadsheet.patches import apply_patches_to_dict


class MockYJSDocument:
    """
    Mock YJS document for demonstration purposes.

    In a real implementation, this would be replaced with actual YJS bindings
    or communication with a YJS-enabled frontend/server.
    """

    def __init__(self, initial_data: Dict[str, Any] = None):
        self.data = initial_data or {
            "sheets": [
                {
                    "sheet_id": 0,
                    "name": "Sheet1",
                    "index": 0,
                    "row_count": 1000,
                    "column_count": 26
                }
            ],
            "sheetData": {
                "0": []  # Empty sheet data
            },
            "tables": [],
            "activeSheetId": 0,
            "selections": {}
        }

    def get_data(self) -> Dict[str, Any]:
        """Get the current document data."""
        return self.data

    def apply_patches(self, patches: List[Dict[str, Any]]) -> None:
        """Apply JSON patches to the document."""
        print(f"Applying {len(patches)} patches to YJS document:")
        for i, patch in enumerate(patches):
            print(f"  Patch {i+1}: {patch}")

        # In a real implementation, you would apply these patches to the YJS document
        # For demo purposes, we'll just simulate it
        try:
            from rowsncolumns_spreadsheet.patches import JSONPatch, PatchOperation
            json_patches = []
            for patch_dict in patches:
                json_patch = JSONPatch(
                    op=PatchOperation(patch_dict['op']),
                    path=patch_dict['path'],
                    value=patch_dict.get('value')
                )
                json_patches.append(json_patch)

            self.data = apply_patches_to_dict(self.data, json_patches)
            print("  ✓ Patches applied successfully")
        except Exception as e:
            print(f"  ✗ Error applying patches: {e}")


def demonstrate_yjs_workflow():
    """
    Demonstrate the complete YJS integration workflow.
    """
    print("=== YJS Integration Workflow Demo ===\n")

    # Step 1: Create a mock YJS document with some initial data
    print("1. Creating YJS document with initial data...")
    yjs_doc = MockYJSDocument({
        "sheets": [
            {
                "sheet_id": 0,
                "name": "Sales Data",
                "index": 0,
                "row_count": 100,
                "column_count": 10,
                "frozen_row_count": 1
            }
        ],
        "sheetData": {
            "0": [
                # Header row
                [
                    {"value": "Product", "formula": None},
                    {"value": "Q1", "formula": None},
                    {"value": "Q2", "formula": None},
                    {"value": "Q3", "formula": None},
                    {"value": "Q4", "formula": None},
                ],
                # Data rows
                [
                    {"value": "Widget A", "formula": None},
                    {"value": 100, "formula": None},
                    {"value": 120, "formula": None},
                    {"value": 110, "formula": None},
                    {"value": 130, "formula": None},
                ],
                [
                    {"value": "Widget B", "formula": None},
                    {"value": 200, "formula": None},
                    {"value": 180, "formula": None},
                    {"value": 220, "formula": None},
                    {"value": 190, "formula": None},
                ]
            ]
        },
        "tables": [],
        "activeSheetId": 0,
        "selections": {}
    })
    print("  ✓ YJS document created with sales data")

    # Step 2: Load data into SpreadsheetInterface
    print("\n2. Loading data into SpreadsheetInterface...")
    spreadsheet = SpreadsheetInterface(initial_data=yjs_doc.get_data())
    print("  ✓ Data loaded successfully")
    print(f"  - Found {len(spreadsheet.state.sheets)} sheet(s)")
    print(f"  - Sheet 0 has {len(spreadsheet.state.sheet_data.get(0, []))} rows of data")

    # Step 3: Perform some operations
    print("\n3. Performing spreadsheet operations...")

    # Insert a new row between header and first data row
    print("  - Inserting row at index 1...")
    spreadsheet.insert_rows(sheet_id=0, reference_row_index=1, num_rows=1)

    # Add data to the new row
    print("  - Adding data to the new row...")
    spreadsheet.set_cell_value(0, 1, 0, "Widget C")
    spreadsheet.set_cell_value(0, 1, 1, 150)
    spreadsheet.set_cell_value(0, 1, 2, 160)
    spreadsheet.set_cell_value(0, 1, 3, 140)
    spreadsheet.set_cell_value(0, 1, 4, 170)

    # Insert a new column for totals
    print("  - Inserting column for totals...")
    spreadsheet.insert_columns(sheet_id=0, reference_column_index=5, num_columns=1)

    # Add total formulas (simulated)
    print("  - Adding total column header...")
    spreadsheet.set_cell_value(0, 0, 5, "Total")

    print("  ✓ Operations completed")

    # Step 4: Generate patches
    print("\n4. Generating patches...")
    patches = spreadsheet.generate_yjs_patches()
    print(f"  ✓ Generated {len(patches)} JSON patches")

    # Also get patch tuples in the format expected by the TypeScript version
    patch_tuples = spreadsheet.get_patch_tuples("redo")
    print(f"  ✓ Generated {len(patch_tuples)} spreadsheet patch tuples")

    # Step 5: Apply patches to YJS document
    print("\n5. Applying patches to YJS document...")
    yjs_doc.apply_patches(patches)

    # Step 6: Verify the changes
    print("\n6. Verifying changes...")
    updated_data = yjs_doc.get_data()
    updated_sheet = updated_data["sheets"][0]
    print(f"  - Sheet row count: {updated_sheet['row_count']} (was 100)")
    print(f"  - Sheet column count: {updated_sheet['column_count']} (was 10)")

    # Check that data was preserved and new data added
    sheet_data = updated_data.get("sheetData", {}).get("0", [])
    if sheet_data:
        print(f"  - Number of data rows: {len(sheet_data)}")
        if len(sheet_data) > 1:
            first_data_row = sheet_data[1]
            if first_data_row and len(first_data_row) > 0:
                product_name = first_data_row[0].get("value") if first_data_row[0] else "N/A"
                print(f"  - First data row product: {product_name}")

    print("  ✓ Changes verified successfully")

    # Step 7: Show how to export current state for persistence
    print("\n7. Exporting state for persistence...")
    current_state = spreadsheet.to_yjs_data()
    print("  ✓ State exported to YJS-compatible format")
    print(f"  - Export contains {len(current_state.keys())} top-level keys")

    # Step 8: Clean up patches
    print("\n8. Cleaning up patches...")
    print(f"  - Had {len(spreadsheet.patches)} accumulated patches")
    spreadsheet.clear_patches()
    print(f"  - Now have {len(spreadsheet.patches)} patches")
    print("  ✓ Patches cleared")


def demonstrate_collaborative_scenario():
    """
    Demonstrate a collaborative editing scenario.
    """
    print("\n\n=== Collaborative Editing Scenario ===\n")

    # Simulate two users working on the same document
    print("Simulating two users editing the same spreadsheet...")

    # Initial document state
    initial_data = {
        "sheets": [{"sheet_id": 0, "name": "Shared Sheet", "index": 0, "row_count": 50, "column_count": 10}],
        "sheetData": {"0": [
            [{"value": "Name", "formula": None}, {"value": "Age", "formula": None}],
            [{"value": "Alice", "formula": None}, {"value": 30, "formula": None}],
        ]},
        "tables": [],
        "activeSheetId": 0,
        "selections": {}
    }

    # User 1: Load document and make changes
    print("\n👤 User 1:")
    user1_spreadsheet = SpreadsheetInterface(initial_data=initial_data.copy())
    print("  - Loaded document")

    user1_spreadsheet.insert_rows(sheet_id=0, reference_row_index=2, num_rows=1)
    user1_spreadsheet.set_cell_value(0, 2, 0, "Bob")
    user1_spreadsheet.set_cell_value(0, 2, 1, 25)
    print("  - Added Bob to the list")

    user1_patches = user1_spreadsheet.generate_yjs_patches()
    print(f"  - Generated {len(user1_patches)} patches")

    # User 2: Load document and make different changes
    print("\n👤 User 2:")
    user2_spreadsheet = SpreadsheetInterface(initial_data=initial_data.copy())
    print("  - Loaded document")

    user2_spreadsheet.insert_columns(sheet_id=0, reference_column_index=2, num_columns=1)
    user2_spreadsheet.set_cell_value(0, 0, 2, "City")
    user2_spreadsheet.set_cell_value(0, 1, 2, "New York")
    print("  - Added City column")

    user2_patches = user2_spreadsheet.generate_yjs_patches()
    print(f"  - Generated {len(user2_patches)} patches")

    print("\n🔄 Conflict Resolution:")
    print("  In a real YJS implementation, these patches would be automatically")
    print("  merged using YJS's conflict resolution algorithms.")
    print("  The final document would contain both Bob's row and the City column.")

    print("\n📊 Summary:")
    print(f"  - User 1 made {len(user1_patches)} changes (row insertion)")
    print(f"  - User 2 made {len(user2_patches)} changes (column insertion)")
    print("  - YJS would merge these changes automatically")


if __name__ == "__main__":
    demonstrate_yjs_workflow()
    demonstrate_collaborative_scenario()

    print("\n" + "="*50)
    print("Demo completed! 🎉")
    print("\nTo integrate with actual YJS:")
    print("1. Replace MockYJSDocument with real YJS document")
    print("2. Use proper YJS Python bindings (if available)")
    print("3. Or communicate patches via WebSocket/HTTP to JS frontend")
    print("4. Apply patches using yjs.applyUpdate() on the frontend")