# Copyright 2022 Sodexis
# License OPL-1 (See LICENSE file for full copyright and licensing details).
{
    "name": "Website Sale Order Sign",
    "summary": """This module is used to get sign from the customer for E-Commerce website order(s)""",
    "version": "14.0.1.0.0",
    "category": "Sales",
    "website": "http://sodexis.com/",
    "author": "Sodexis",
    "license": "OPL-1",
    "installable": True,
    "application": False,
    "depends": [
        'website_sale'
    ],
    "data": [
        "views/website_sale_signature_template.xml",
    ],
}
