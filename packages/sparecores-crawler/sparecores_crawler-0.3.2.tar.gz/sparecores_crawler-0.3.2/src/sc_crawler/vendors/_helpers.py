def convert_regions_to_zones(vendor):
    """Create a dummy list of zones from the list of regions."""
    items = []
    for region in vendor.regions:
        items.append(
            {
                "vendor_id": vendor.vendor_id,
                "region_id": region.region_id,
                "zone_id": region.region_id,
                "name": region.name,
                "api_reference": region.name,
                "display_name": region.name,
            }
        )
    return items
