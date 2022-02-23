"""
This function takes the listing title, images, name, start price etc and makes the eBay listing

"""
from ebaysdk.trading import Connection

#  Customize a disclaimer to be displayed in every single description
disclaimer = "Disclaimer: Card is not professionally minted and is sold as is. Please see images for quality inspection. <br/><br/>" \
             "Returns are not accepted. <br/><br/>" \
             "Card will be shipped in a plastic case with ample cardboard padding."


def create_listing(title, startPrice, img_urls):
    api = Connection(config_file="ebay.yaml", domain="api.ebay.com", debug=False)
    description = '<div class="text">' + title + "<br/><br/>" + disclaimer + '</div>'
    description = "<![CDATA[" + description + "]]>"
    request = {
        "Item": {
            "Title": title,
            "ItemSpecifics": {
                "NameValueList":
                    [
                        {"Name": "Brand",
                         "Value": "Pokemon"},
                        {"Name": "Game",
                         "Value": "Pokemon TCG"},
                        {"Name": "Graded",
                         "Value": "No"}
                    ]
            },
            "PictureDetails": {
                "PictureURL": img_urls
            },
            "Country": "US",
            "Location": "US",
            "Site": "US",
            "ConditionID": "3000",
            "PaymentMethods": "PayPal",
            "PayPalEmailAddress": "turnermluke@gmail.com",
            "PrimaryCategory": {"CategoryID": "183454"},

            "Description": description,
            "ListingDuration": "Days_10",
            "StartPrice": startPrice,
            "Currency": "USD",
            "ReturnPolicy": {
                "ReturnsAcceptedOption": "ReturnsNotAccepted"
            },
            "ShippingDetails": {
                "ShippingType": "Calculated",
                "ShippingServiceOptions": {
                    "FreeShipping": "False",
                    "ShippingService": "USPSFirstClass",
                },
                "CalculatedShippingRate": {
                    "OriginatingPostalCode": "54007"
                },
            },
            "ShippingPackageDetails": {
                "MeasurementUnit": "English",
                "PackageDepth": 1,
                "PackageLength": 5,
                "PackageWidth": 5,
                "WeightMajor": 1,
                "WeightMinor": 0,
                "ShippingPackage": "PackageThickEnvelope"
            },

            "DispatchTimeMax": "3"  # Number of days to ship after sale
        }
    }

    api.execute("AddItem", request)
