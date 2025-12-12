# Custom Fields Setup Guide

This document provides detailed instructions for setting up the required custom fields for the NetBox Interface View plugin.

## Overview

The plugin requires three custom fields to function properly:

1. **grid_rows** - on Device model
2. **grid_columns** - on Device model
3. **color** - on VLAN model

## Method 1: Via NetBox Web UI

### Step 1: Create Device Custom Fields

#### Creating grid_rows field:

1. Log in to NetBox as an administrator
2. Navigate to **Customization** → **Custom Fields**
3. Click the **Add** button
4. Fill in the following details:
   - **Name**: `grid_rows`
   - **Label**: `Grid Rows`
   - **Group Name**: (optional) `Interface Grid`
   - **Type**: `Integer`
   - **Content types**: Select `dcim > device`
   - **Required**: Leave unchecked
   - **Default**: `2`
   - **Description**: `Number of rows in the interface grid layout`
   - **Validation minimum**: `1`
   - **Validation maximum**: `100`
5. Click **Create**

#### Creating grid_columns field:

1. Navigate to **Customization** → **Custom Fields**
2. Click the **Add** button
3. Fill in the following details:
   - **Name**: `grid_columns`
   - **Label**: `Grid Columns`
   - **Group Name**: (optional) `Interface Grid`
   - **Type**: `Integer`
   - **Content types**: Select `dcim > device`
   - **Required**: Leave unchecked
   - **Default**: `24`
   - **Description**: `Number of columns in the interface grid layout`
   - **Validation minimum**: `1`
   - **Validation maximum**: `100`
4. Click **Create**

### Step 2: Create VLAN Custom Field

#### Creating color field:

1. Navigate to **Customization** → **Custom Fields**
2. Click the **Add** button
3. Fill in the following details:
   - **Name**: `color`
   - **Label**: `Color`
   - **Group Name**: (optional) `Visualization`
   - **Type**: `Text`
   - **Content types**: Select `ipam > vlan`
   - **Required**: Leave unchecked
   - **Default**: `#cccccc`
   - **Description**: `Hex color code for VLAN visualization (e.g., #FF5733)`
   - **Validation regex**: `^#[0-9A-Fa-f]{6}$`
4. Click **Create**

## Method 2: Via Django Shell

You can also create these custom fields programmatically using the Django shell:

```bash
# Enter the Django shell
cd /opt/netbox/netbox/
source /opt/netbox/venv/bin/activate
python3 manage.py nbshell
```

Then run the following Python code:

```python
from django.contrib.contenttypes.models import ContentType
from extras.models import CustomField

# Get content types
device_ct = ContentType.objects.get_for_model(Device)
vlan_ct = ContentType.objects.get_for_model(VLAN)

# Create grid_rows field
grid_rows = CustomField(
    name='grid_rows',
    label='Grid Rows',
    type='integer',
    required=False,
    default=2,
    description='Number of rows in the interface grid layout',
    validation_minimum=1,
    validation_maximum=100
)
grid_rows.save()
grid_rows.content_types.set([device_ct])

# Create grid_columns field
grid_columns = CustomField(
    name='grid_columns',
    label='Grid Columns',
    type='integer',
    required=False,
    default=24,
    description='Number of columns in the interface grid layout',
    validation_minimum=1,
    validation_maximum=100
)
grid_columns.save()
grid_columns.content_types.set([device_ct])

# Create color field
color = CustomField(
    name='color',
    label='Color',
    type='text',
    required=False,
    default='#cccccc',
    description='Hex color code for VLAN visualization (e.g., #FF5733)',
    validation_regex='^#[0-9A-Fa-f]{6}$'
)
color.save()
color.content_types.set([vlan_ct])

print("Custom fields created successfully!")
```

## Method 3: Via NetBox API

You can create custom fields using the NetBox REST API:

```bash
# Set your NetBox URL and API token
export NETBOX_URL="https://netbox.example.com"
export NETBOX_TOKEN="your-api-token-here"

# Create grid_rows field
curl -X POST "${NETBOX_URL}/api/extras/custom-fields/" \
  -H "Authorization: Token ${NETBOX_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "grid_rows",
    "label": "Grid Rows",
    "type": "integer",
    "content_types": ["dcim.device"],
    "required": false,
    "default": 2,
    "description": "Number of rows in the interface grid layout",
    "validation_minimum": 1,
    "validation_maximum": 100
  }'

# Create grid_columns field
curl -X POST "${NETBOX_URL}/api/extras/custom-fields/" \
  -H "Authorization: Token ${NETBOX_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "grid_columns",
    "label": "Grid Columns",
    "type": "integer",
    "content_types": ["dcim.device"],
    "required": false,
    "default": 24,
    "description": "Number of columns in the interface grid layout",
    "validation_minimum": 1,
    "validation_maximum": 100
  }'

# Create color field
curl -X POST "${NETBOX_URL}/api/extras/custom-fields/" \
  -H "Authorization: Token ${NETBOX_TOKEN}" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "color",
    "label": "Color",
    "type": "text",
    "content_types": ["ipam.vlan"],
    "required": false,
    "default": "#cccccc",
    "description": "Hex color code for VLAN visualization (e.g., #FF5733)",
    "validation_regex": "^#[0-9A-Fa-f]{6}$"
  }'
```

## Usage After Setup

### Setting Grid Dimensions on a Device

1. Navigate to a device in NetBox
2. Click **Edit**
3. Scroll to the **Custom Fields** section
4. Set **Grid Rows** and **Grid Columns** to match your device's physical layout
   - Example for a 48-port switch in 2 rows: rows=2, columns=24
   - Example for a 24-port switch in 3 rows: rows=3, columns=8
5. Click **Save**

### Setting VLAN Colors

1. Navigate to a VLAN in NetBox
2. Click **Edit**
3. Scroll to the **Custom Fields** section
4. Set **Color** to a hex color code (e.g., `#FF5733` for red-orange)
5. Click **Save**

**Recommended VLAN Colors:**

- Management VLAN: `#0066CC` (blue)
- Data VLAN: `#00CC66` (green)
- Voice VLAN: `#FF9900` (orange)
- Guest VLAN: `#9966CC` (purple)
- Server VLAN: `#CC0000` (red)

## Verification

After creating the custom fields:

1. Go to a device detail page
2. You should see the **View Interface Grid** button
3. Click the button to view the interface grid
4. If custom fields are not set, defaults will be used (2 rows × 24 columns, gray VLAN colors)

## Troubleshooting

### Button not appearing

- Ensure the plugin is installed and configured in `configuration.py`
- Restart NetBox services: `sudo systemctl restart netbox netbox-rq`
- Check that the device has at least one interface

### Grid not displaying correctly

- Verify custom field values on the device
- Ensure `grid_rows` and `grid_columns` are positive integers
- Check browser console for JavaScript errors

### VLAN colors not showing

- Verify the `color` custom field is created on the VLAN model
- Ensure color values are valid hex codes (e.g., `#FF5733`)
- Check that VLANs are assigned to interfaces (untagged or tagged)

## Support

For issues or questions, please open an issue on the GitHub repository.
