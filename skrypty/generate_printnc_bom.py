import adsk.core, adsk.fusion, traceback
import csv
import re


CUSTOM_PARTS = {
    "m4x8 Pan Head": {
        "name": "M4x8 Pan Head",
        "description": "",
        "show_length": False,
        "show_dimensions": False,
        "override_quantity": False,
    },
    "m4x12": {
        "name": "M4x12",
        "description": "",
        "show_length": False,
        "show_dimensions": False,
        "override_quantity": False,
    },
    "m4x16": {
        "name": "M4x16",
        "description": "",
        "show_length": False,
        "show_dimensions": False,
        "override_quantity": False,
    },
    "m5x12": {
        "name": "M5x12",
        "description": "",
        "show_length": False,
        "show_dimensions": False,
        "override_quantity": False,
    },
    "m5x20": {
        "name": "M5x20",
        "description": "",
        "show_length": False,
        "show_dimensions": False,
        "override_quantity": False,
        "aliases": ["m5-20"],
    },    
    "m6x12": {
        "name": "M6x12",
        "description": "",
        "show_length": False,
        "show_dimensions": False,
        "override_quantity": False,
    },
    "m6x20": {
        "name": "M6x20",
        "description": "",
        "show_length": False,
        "show_dimensions": False,
        "override_quantity": False,
    },
    "m6x30": {
        "name": "M6x30",
        "description": "",
        "show_length": False,
        "show_dimensions": False,
        "override_quantity": False,
    },
    "m6x50": {
        "name": "M6x50",
        "description": "",
        "show_length": False,
        "show_dimensions": False,
        "override_quantity": False,
    },
    "m8x8 grub": {
        "name": "M8x8 Grub",
        "description": "",
        "show_length": False,
        "show_dimensions": False,
        "override_quantity": False,
    },
    "m8x45": {
        "name": "M8x45",
        "description": "",
        "show_length": False,
        "show_dimensions": False,
        "override_quantity": False,
    },    
    "x m5 threaded rod": {
        "name": "X M5 Threaded Rod",
        "description": "",
        "show_length": True,
        "show_dimensions": False,
        "override_quantity": False,
    },
    "y m5 threaded rod": {
        "name": "Y M5 Threaded Rod",
        "description": "",
        "show_length": True,
        "show_dimensions": False,
        "override_quantity": False,
    },
    "m5 nut": {
        "name": "M5 Nut",
        "description": "",
        "show_length": False,
        "show_dimensions": False,
        "override_quantity": False,
    },
    "x m6 threaded rod": {
        "name": "X M6 Threaded Rod",
        "description": "",
        "show_length": True,
        "show_dimensions": False,
        "override_quantity": False,
    },
    "y m6 threaded rod": {
        "name": "Y M6 Threaded Rod",
        "description": "",
        "show_length": True,
        "show_dimensions": False,
        "override_quantity": False,
    },
    "m6 nut": {
        "name": "M6 Nut",
        "description": "",
        "show_length": False,
        "show_dimensions": False,
        "override_quantity": False,
    },
    "m5 washer": {
        "name": "M5 Washer",
        "description": "",
        "show_length": False,
        "show_dimensions": False,
        "override_quantity": False,
    },
    "m6 washer": {
        "name": "M6 Washer",
        "description": "",
        "show_length": False,
        "show_dimensions": False,
        "override_quantity": False,
    },
    "x hgr20 rail": {
        "name": "X HGR20 Rail",
        "description": "",
        "show_length": True,
        "show_dimensions": False,
        "override_quantity": 2,
    },
    "y hgr20 rail": {
        "name": "Y HGR20 Rail",
        "description": "",
        "show_length": True,
        "show_dimensions": False,
        "override_quantity": False,
    },
    "y2 hgr20 rail": {
        "name": "Y2 HGR20 Rail",
        "description": "",
        "show_length": True,
        "show_dimensions": False,
        "override_quantity": False,
    },
    "1z hgr20 rail": {
        "name": "1Z HGR20 Rail",
        "description": "",
        "show_length": True,
        "show_dimensions": False,
        "override_quantity": 2,
    },
    "2z hgr15 rail": {
        "name": "2Z HGR15 Rail",
        "description": "",
        "show_length": True,
        "show_dimensions": False,
        "override_quantity": 2,
    },
    "hgh15ca": {
        "name": "HGH15CA slider block",
        "description": "",
        "show_length": False,
        "show_dimensions": False,
        "override_quantity": False,
    },    
    "hgw20cc": {
        "name": "HGW20CC slider block",
        "description": "",
        "show_length": False,
        "show_dimensions": False,
        "override_quantity": False,
    },    
    "y 1610 ballscrew": {
        "name": "Y 1610 Ballscrew",
        "description": "",
        "show_length": True,
        "show_dimensions": False,
        "override_quantity": False,
    },
    "y 2010 ballscrew": {
        "name": "Y 2010 Ballscrew",
        "description": "",
        "show_length": True,
        "show_dimensions": False,
        "override_quantity": False,
    },
    "x 1610 ballscrew": {
        "name": "X 1610 Ballscrew",
        "description": "",
        "show_length": True,
        "show_dimensions": False,
        "override_quantity": False,
    },
    "x 2010 ballscrew": {
        "name": "X 2010 Ballscrew",
        "description": "",
        "show_length": True,
        "show_dimensions": False,
        "override_quantity": False,
    },
    "y2 1610 ballscrew": {
        "name": "Y2 1610 Ballscrew",
        "description": "",
        "show_length": True,
        "show_dimensions": False,
        "override_quantity": False,
    },
    "y2 2010 ballscrew": {
        "name": "Y2 2010 Ballscrew",
        "description": "",
        "show_length": True,
        "show_dimensions": False,
        "override_quantity": False,
    },
    "z 1204 ballscrew": {
        "name": "Z 1204 Ballscrew",
        "description": "",
        "show_length": True,
        "show_dimensions": False,
        "override_quantity": False,
    },
    "80mm spindle clamp": {
        "name": "80mm Spindle Clamp",
        "description": "",
        "show_length": False,
        "show_dimensions": False,
        "override_quantity": False,
    },
    "xframe tubing": {
        "name": "Steel: X Frame Tubing",
        "description": "",
        "show_length": True,
        "show_dimensions": True,
        "override_quantity": False,
    },
    "yframe tubing": {
        "name": "Steel: Y Frame Tubing",
        "description": "",
        "show_length": True,
        "show_dimensions": True,
        "override_quantity": False,
    },
    "yroller tubing": {
        "name": "Steel: Y Roller Tubing",
        "description": "",
        "show_length": True,
        "show_dimensions": True,
        "override_quantity": False,
    },
    "yroller brace": {
        "name": "Steel: Y Roller Brace",
        "description": "",
        "show_length": False,
        "show_dimensions": True,
        "override_quantity": False,
    },
    "xgantry tubing": {
        "name": "Steel: X Gantry Tubing",
        "description": "",
        "show_length": True,
        "show_dimensions": True,
        "override_quantity": False,
    },
    "xroller tubing": {
        "name": "Steel: X Roller Tubing",
        "description": "",
        "show_length": True,
        "show_dimensions": True,
        "override_quantity": False,
    },
    "xroller angle": {
        "name": "Steel: X Roller Angle",
        "description": "",
        "show_length": True,
        "show_dimensions": True,
        "override_quantity": False,
    },
}


def calculate_body_dimensions_from_vertices(body):
    """
    Calculates the dimensions of a body using its vertices.

    Args:
        body: The Fusion 360 body to measure.

    Returns:
        A tuple containing:
        - The largest dimension (float) of the body in millimeters.
        - A string in the format "XxYxZ" with dimensions in millimeters.
    """
    min_x = min_y = min_z = float("inf")
    max_x = max_y = max_z = float("-inf")

    for vertex in body.vertices:
        point = vertex.geometry
        min_x = min(min_x, point.x * 10)  # Convert cm to mm
        min_y = min(min_y, point.y * 10)  # Convert cm to mm
        min_z = min(min_z, point.z * 10)  # Convert cm to mm
        max_x = max(max_x, point.x * 10)  # Convert cm to mm
        max_y = max(max_y, point.y * 10)  # Convert cm to mm
        max_z = max(max_z, point.z * 10)  # Convert cm to mm

    # Calculate lengths in each direction and sort descending for reporting.
    dimensions = sorted(
        [round(max_x - min_x, 2), round(max_y - min_y, 2), round(max_z - min_z, 2)],
        reverse=True,
    )

    # Format dimensions to only show decimals if needed
    format_dimension = lambda v: f"{v:.2f}".rstrip('0').rstrip('.')
    x, y, z = map(format_dimension, dimensions)

    # Return the largest dimension and the dimensions in XxYxZ format
    return x, f"{x} x {y} x {z}"


def normalize_name(s):
    """Normalize a name for matching: lowercase and strip non-alphanumerics."""
    if not s:
        return ""
    return re.sub(r'[^0-9a-z]', '', s.lower())


def process_component(component, component_path, parts_list, custom_parts, unrecognized_parts):
    """
    Processes a component and its bodies, aggregating counts for custom parts.

    Args:
        component: The current Fusion 360 component being processed.
        component_path: Full component path for reporting.
        parts_list: A dictionary to store aggregated counts for parts.
        custom_parts: A dictionary of custom part names and their properties.
    Returns:
        None
    """
    for body in component.bRepBodies:
        if not body.isVisible:
            continue

        # Check for custom part matches using normalization and optional aliases
        body_name_norm = normalize_name(body.name)
        part_info = None
        for custom_key, custom_value in custom_parts.items():
            candidates = [custom_key]
            if isinstance(custom_value, dict):
                candidates += custom_value.get("aliases", []) or []
            for cand in candidates:
                if body_name_norm.startswith(normalize_name(cand)):
                    part_info = custom_value
                    break
            if part_info:
                break

        # Calculate the largest dimension and XxYxZ dimensions for reporting
        largest_dimension, xyz_dimensions = calculate_body_dimensions_from_vertices(body)

        if part_info is None:
            # Ignore unrecognized parts that are part of the printed-milled parts assembly or printed drill guides.
            if component_path and ("printed-milled parts:1" in component_path.lower() or "printed drill guides:1" in component_path.lower()):
                continue

            # Collect unrecognized parts (count by body name + dimensions)
            display_name = body.name if body.name else "Unnamed Body"
            key_unrec = (display_name, xyz_dimensions, component_path)
            if key_unrec in unrecognized_parts:
                unrecognized_parts[key_unrec] += 1
            else:
                unrecognized_parts[key_unrec] = 1
            continue

        # Get dimensions and length based on custom parts configuration
        name = part_info["name"]
        description = part_info["description"]
        length = largest_dimension if part_info.get("show_length", False) else None
        dimensions = xyz_dimensions if part_info.get("show_dimensions", False) else None
        override_quantity = part_info.get("override_quantity", False)

        # Set quantity directly if override_quantity is provided
        quantity = override_quantity if override_quantity else 1

        # Aggregate the part in the parts list
        key = (name, description, length, dimensions)  # Use name, description, length, and dimensions as the unique key
        if key in parts_list:
            if override_quantity is False:
                parts_list[key] += 1
        else:
            parts_list[key] = quantity

    # Process sub-components recursively
    for occurrence in component.occurrences:
        occ_name = occurrence.name or occurrence.component.name
        next_path = f"{component_path}->{occ_name}" if component_path else occ_name
        process_component(occurrence.component, next_path, parts_list, custom_parts, unrecognized_parts)


def export_parts_list_to_csv(parts_list, custom_parts, unrecognized_parts, model_name, cutting_area):
    """
    Exports the aggregated parts list to a CSV file.

    Args:
        parts_list: A dictionary with aggregated parts data.

    Returns:
        The path to the saved CSV file or None if the save operation is canceled.
    """
    app = adsk.core.Application.get()
    ui = app.userInterface
    try:
        file_dialog = ui.createFileDialog()
        file_dialog.isMultiSelectEnabled = False
        file_dialog.title = "Select Save Location for the Parts List CSV"
        file_dialog.filter = "CSV Files (*.csv)"
        file_dialog.filterIndex = 0
        dialog_result = file_dialog.showSave()

        if dialog_result == adsk.core.DialogResults.DialogOK:
            file_path = file_dialog.filename

            with open(file_path, "w", newline="") as csvfile:
                csv_writer = csv.writer(csvfile)

                # Header section
                csv_writer.writerow(["Model:", model_name])
                csv_writer.writerow(["Cutting Area:", cutting_area])
                csv_writer.writerow([])

                # Write the header
                csv_writer.writerow(["Position", "Name", "Description", "Quantity", "Length (mm)", "Dimensions (mm)"])

                position = 1
                for custom_key in custom_parts.keys():
                    for (name, description, length, dimensions), quantity in parts_list.items():
                        if name == custom_parts[custom_key]["name"]:
                            csv_writer.writerow(
                                [
                                    position,
                                    name,
                                    description,
                                    quantity,
                                    length if length is not None else "",
                                    dimensions if dimensions is not None else "",
                                ]
                            )
                            position += 1

                # Write unrecognized parts (if any)
                if unrecognized_parts:
                    csv_writer.writerow([])
                    csv_writer.writerow([])
                    csv_writer.writerow([])
                    csv_writer.writerow(["Unrecognized Parts (only relevant if Fusion model changes and can usually be ignored)"])
                    csv_writer.writerow(["Position", "Name", "Description", "Quantity", "Length (mm)", "Dimensions (mm)", "Path"])
                    pos_unrec = 1
                    for (name, dimensions, path), quantity in unrecognized_parts.items():
                        csv_writer.writerow([pos_unrec, name, "", quantity, "", dimensions, path])
                        pos_unrec += 1

            return file_path
        else:
            return None
    except Exception as e:
        return str(e)


def list_and_count_parts():
    """
    Main function to execute the parts counting script in Fusion 360.

    This function initializes the required variables, processes the root component, and exports the results to a CSV file.
    """
    app = adsk.core.Application.get()
    ui = app.userInterface
    try:
        design = app.activeProduct
        if not isinstance(design, adsk.fusion.Design):
            ui.messageBox("Please open a Fusion 360 design.")
            return

        root_comp = design.rootComponent
        model_name = design.parentDocument.name if design.parentDocument else root_comp.name

        def get_param_text(param_name):
            param = None
            if hasattr(design, "userParameters") and design.userParameters:
                param = design.userParameters.itemByName(param_name)
            if (param is None) and hasattr(design, "allParameters") and design.allParameters:
                param = design.allParameters.itemByName(param_name)
            if param is None:
                return ""
            return param.expression if hasattr(param, "expression") else str(param.value)

        x_cutting_area = get_param_text("XCuttingArea")
        y_cutting_area = get_param_text("YCuttingArea")
        cutting_area = f"{x_cutting_area} x {y_cutting_area}"

        parts_list = {}
        unrecognized_parts = {}

        # Process full assembly from root component, but omit root name in reported sub-paths.
        process_component(root_comp, "", parts_list, CUSTOM_PARTS, unrecognized_parts)

        # Export the results to a CSV file
        csv_path = export_parts_list_to_csv(parts_list, CUSTOM_PARTS, unrecognized_parts, model_name, cutting_area)
        if csv_path:
            ui.messageBox(f"Parts list exported: {csv_path}")
        else:
            ui.messageBox("Save operation canceled.")
    except:
        ui.messageBox("Error:\n{}".format(traceback.format_exc()))


list_and_count_parts()
