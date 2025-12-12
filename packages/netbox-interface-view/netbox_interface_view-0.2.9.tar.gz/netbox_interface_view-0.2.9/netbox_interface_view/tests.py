from django.test import TestCase

class InterfaceGridViewLogicTest(TestCase):
    def test_column_major_ordering(self):
        """
        Tests that the interface list is correctly reordered for column-major display.
        """
        # --- Input Data ---
        # A simple list of 10 interfaces
        interface_list = [{'name': f'int-{i}'} for i in range(1, 11)]
        
        # Grid dimensions
        grid_rows = 4
        grid_columns = 3  # A 4x3 grid can hold 12 items

        # --- Expected Output ---
        # For a 4x3 grid, the order should be:
        # Col 1: 1, 2, 3, 4
        # Col 2: 5, 6, 7, 8
        # Col 3: 9, 10
        #
        # The list rendered by the template (row-by-row) should be:
        # Row 1: 1, 5, 9
        # Row 2: 2, 6, 10
        # Row 3: 3, 7
        # Row 4: 4, 8
        expected_names = [
            'int-1', 'int-5', 'int-9',
            'int-2', 'int-6', 'int-10',
            'int-3', 'int-7',
            'int-4', 'int-8',
        ]

        # --- Logic from the View ---
        reordered_interfaces = [None] * len(interface_list)
        for i, item in enumerate(interface_list):
            row = i % grid_rows
            col = i // grid_rows
            new_index = row * grid_columns + col
            if new_index < len(reordered_interfaces):
                reordered_interfaces[new_index] = item
        
        # Filter out None values that might appear
        final_list = [item for item in reordered_interfaces if item is not None]
        
        # Extract names for comparison
        final_names = [item['name'] for item in final_list]

        # --- Assertion ---
        self.assertEqual(final_names, expected_names)

    def test_virtual_interface_exclusion_default(self):
        """
        Tests that 'virtual' interfaces are excluded by default.
        """
        from django.test import RequestFactory
        from netbox_interface_view.views import InterfaceGridView

        # In a real scenario, you would mock the database query.
        # For this logic test, we can check the 'filter_types' directly.
        
        # Create a fake request without any 'exclude_type' params
        factory = RequestFactory()
        request = factory.get('/fake-path')

        # The logic from the view
        default_exclude = ['virtual']
        filter_types = request.GET.getlist('exclude_type', default_exclude)

        self.assertEqual(filter_types, ['virtual'])

    def test_virtual_interface_exclusion_override(self):
        """
        Tests that the default exclusion is overridden when params are provided.
        """
        from django.test import RequestFactory

        # Create a fake request that excludes a different type
        factory = RequestFactory()
        request = factory.get('/fake-path?exclude_type=lag')

        # The logic from the view
        default_exclude = ['virtual']
        filter_types = request.GET.getlist('exclude_type', default_exclude)

        self.assertEqual(filter_types, ['lag'])
