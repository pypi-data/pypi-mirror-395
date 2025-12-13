import json
import validators
import xml.etree.ElementTree as ET

from xml.dom import minidom
from datetime import datetime

def Sitemap(modules_json, base_url, output):
    # Open modules.json
    with open(modules_json) as json_data:
        data = json.load(json_data)

    # Access the "modules" object
    modules = data.get("modules", [])

    # Create the root element for the sitemap
    urlset = ET.Element("urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9", **{"xmlns:image": "http://www.google.com/schemas/sitemap-image/1.1"})

    # Add URLs to the sitemap
    for module in modules:
        # Convert Unix timestamp to datetime object
        dt_object = datetime.utcfromtimestamp(module["timestamp"])

        # Format the datetime object as 'YYYY-MM-DD'
        formatted_date = dt_object.strftime('%Y-%m-%d')

        module_id = module["id"]
        url = base_url + module_id
        url_element = ET.SubElement(urlset, "url")
        loc_element = ET.SubElement(url_element, "loc")
        lastmod_element = ET.SubElement(url_element, "lastmod")
        
        cover = module.get("cover") if module.get("cover") else module.get("track").get("cover") 
        if cover and validators.url(cover):
            url_image_image = ET.SubElement(url_element, "image:image")
            url_image_image_loc = ET.SubElement(url_image_image, "image:loc")
            url_image_image_loc.text = cover

        lastmod_element.text = formatted_date
        loc_element.text = url

    # Convert the ElementTree to a string
    sitemap = ET.tostring(urlset, encoding="utf-8", method="xml")

    xmlstr = minidom.parseString(sitemap).toprettyxml(indent="   ")

    # Write to a file
    with open(output, "w") as f:
        f.write(xmlstr)

    print("Sitemap generated successfully.")