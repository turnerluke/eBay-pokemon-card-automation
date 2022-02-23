import os
import sys
import datetime
from optparse import OptionParser
from PIL import Image
from pprint import pprint
import ebaysdk
from ebaysdk.utils import getNodeText
from ebaysdk.exception import ConnectionError
from ebaysdk.trading import Connection as Trading


def init_options():
    usage = "usage: %prog [options]"
    parser = OptionParser(usage=usage)

    parser.add_option("-d", "--debug",
                      action="store_true", dest="debug", default=False,
                      help="Enabled debugging [default: %default]")
    parser.add_option("-y", "--yaml",
                      dest="yaml", default='ebay.yaml',
                      help="Specifies the name of the YAML defaults file. [default: %default]")
    parser.add_option("-a", "--appid",
                      dest="appid", default=None,
                      help="Specifies the eBay application id to use.")
    parser.add_option("-p", "--devid",
                      dest="devid", default=None,
                      help="Specifies the eBay developer id to use.")
    parser.add_option("-c", "--certid",
                      dest="certid", default=None,
                      help="Specifies the eBay cert id to use.")
    parser.add_option("-n", "--domain",
                      dest="domain", default='api.ebay.com',
                      help="Specifies the eBay domain to use (e.g. api.sandbox.ebay.com).")

    (opts, args) = parser.parse_args()
    return opts, args


def uploadPictureFromFilesystem(filepath):
    opts, _ = init_options()
    try:
        api = Trading(debug=opts.debug, config_file=opts.yaml, appid=opts.appid, domain=opts.domain,
                      certid=opts.certid, devid=opts.devid, warnings=True)

        # pass in an open file
        # the Requests module will close the file
        files = {'file': ('EbayImage', open(filepath, 'rb'))}

        pictureData = {
            "WarningLevel": "High",
            "PictureName": "WorldLeaders"
        }

        response = api.execute('UploadSiteHostedPictures', pictureData, files=files)
        #dump(api)

    except ConnectionError as e:
        print(e)
        print(e.response.dict())

    return response.reply.SiteHostedPictureDetails.FullURL


def dump(api, full=False):

    print("\n")

    if api.warnings():
        print("Warnings" + api.warnings())

    if api.response.content:
        print("Call Success: %s in length" % len(api.response.content))

    print("Response code: %s" % api.response_code())
    print("Response DOM1: %s" % api.response_dom()) # deprecated
    print("Response ETREE: %s" % api.response.dom())

    if full:
        print(api.response.content)
        print(api.response.json())
        print("Response Reply: %s" % api.response.reply)
    else:
        dictstr = "%s" % api.response.dict()
        print("Response dictionary: %s..." % dictstr[:150])
        replystr = "%s" % api.response.reply
        print("Response Reply: %s" % replystr[:150])

