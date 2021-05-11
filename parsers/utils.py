import os
import xml.etree.ElementTree as ET

from django.conf import settings

from parsers.models import File
from products.models import Category, Product, Vendor

from datetime import datetime

from ftplib import FTP

PREFIX_V8 = 'http://v8.1c.ru/8.1/data/enterprise/current-config'

NAMESPACES = {
    'v8': 'http://v8.1c.ru/8.1/data/enterprise/current-config',
}

NOMENCLATURE_TYPES_TAG = 'v8:CatalogObject.ВидыНоменклатуры'
NOMENCLATURE_TAG = 'v8:CatalogObject.Номенклатура'
VENDORS_TAG = 'v8:CatalogObject.Производители'
NOMENCLATURE_FILES_TAG = 'v8:CatalogObject.НоменклатураПрисоединенныеФайлы'
NOMENCLATURE_PRICES_TAG = 'v8:DocumentObject.УстановкаЦенНоменклатуры'
NOMENCLATURE_SHIPMENTS_AND_SERVICES = 'v8:DocumentObject.ПриобретениеТоваровУслуг'


def _clear_database():
    # command_reset = 'python manage.py'
    # apps = ['products']
    # for app in apps:
    #     os.system(command_reset + ' ' + app)
    Category.objects.all().delete()
    Product.objects.all().delete()
    Vendor.objects.all().delete()


def _fill_nomenclature_types(nomenclature_types):
    for type in nomenclature_types:
        if type.find('v8:IsFolder', namespaces=NAMESPACES).text == 'true':
            continue
        name = type.find('v8:Description', namespaces=NAMESPACES).text
        ref = type.find('v8:Ref', namespaces=NAMESPACES).text
        print('NAME_1', name)
        print('REF_1', ref)

        Category.objects.update_or_create(
            ref=ref,
            defaults={
                'name': name,
            }
        )


def _fill_nomenclature(nomenclatures):
    for nomenclature in nomenclatures:
        ref = nomenclature.find('v8:Ref', namespaces=NAMESPACES).text
        name = nomenclature.find('v8:НаименованиеПолное', namespaces=NAMESPACES).text
        nomenclature_type_ref = nomenclature.find('v8:ВидНоменклатуры', namespaces=NAMESPACES).text
        description = nomenclature.find('v8:Описание', namespaces=NAMESPACES).text
        vendor_ref = nomenclature.find('v8:Производитель', namespaces=NAMESPACES).text
        vendor = Vendor.objects.get(ref=vendor_ref) if Vendor.objects.filter(ref=vendor_ref).exists() else None

        Product.objects.update_or_create(
            ref=ref,
            defaults={
                'name': name,
                'category': Category.objects.get(ref=nomenclature_type_ref),
                'description': description if description is not None else '',
                'vendor': vendor,
            }
        )


def _fill_vendors(vendors):
    for vendor in vendors:
        ref = vendor.find('v8:Ref', namespaces=NAMESPACES).text
        name = vendor.find('v8:Description', namespaces=NAMESPACES).text

        Vendor.objects.update_or_create(
            ref=ref,
            defaults={
                'name': name,
            }
        )


def _fill_nomenclature_images(nomenclature_images):
    nomenclature_updated_images = {}

    for nomenclature_image in nomenclature_images:
        if nomenclature_image.find('v8:ТипХраненияФайла', namespaces=NAMESPACES).text == 'ВИнформационнойБазе':
            print('NEW FILE')
            ref_of_nomenclature = nomenclature_image.find('v8:ВладелецФайла', namespaces=NAMESPACES).text
            date_of_creation = nomenclature_image.find('v8:ДатаСоздания', namespaces=NAMESPACES).text
            date_of_creation = datetime.strptime(date_of_creation, '%Y-%m-%dT%H:%M:%S')
            if nomenclature_updated_images.get(ref_of_nomenclature) is None or date_of_creation > \
                    nomenclature_updated_images[ref_of_nomenclature]:
                nomenclature_updated_images[ref_of_nomenclature] = date_of_creation
                name_of_image = nomenclature_image.find('v8:Description', namespaces=NAMESPACES).text
                extension = nomenclature_image.find('v8:Расширение', namespaces=NAMESPACES).text
                final_name = name_of_image + '.' + extension
                Product.objects.update_or_create(
                    ref=ref_of_nomenclature,
                    defaults={
                        'image': os.path.join(settings.MEDIA_PRODUCT_IMAGE_DIR, final_name),
                    }
                )


def _fill_nomenclature_prices(nomenclature_prices):
    for nomenclature_price in nomenclature_prices:
        shipments = nomenclature_price.findall('v8:Товары', namespaces=NAMESPACES)
        for shipment in shipments:
            nomenclature_ref = shipment.find('v8:Номенклатура', namespaces=NAMESPACES).text
            price = shipment.find('v8:Цена', namespaces=NAMESPACES).text
            print('nomenclature_ref', nomenclature_ref)
            print('------------------------------price', price)
            if Product.objects.filter(ref=nomenclature_ref).exists():
                print('===============yes exists')
                product = Product.objects.get(ref=nomenclature_ref)
                product.price = price
                product.save()


def _fill_product_quantities(nomenclature_shipments_and_services):
    for item in nomenclature_shipments_and_services:
        shipments = item.findall('v8:Товары', namespaces=NAMESPACES)
        for shipment in shipments:
            nomenclature_ref = shipment.find('v8:Номенклатура', namespaces=NAMESPACES).text
            quantity = shipment.find('v8:Количество', namespaces=NAMESPACES).text
            if Product.objects.filter(ref=nomenclature_ref).exists():
                product = Product.objects.get(ref=nomenclature_ref)
                product.quantity = quantity
                product.save()


def update_images():
    ftp = FTP(settings.FTP_SERVER)
    ftp.login(settings.FTP_USER, settings.FTP_PASS)

    ftp.cwd('upload')
    ftp.cwd('images')
    filenames = ftp.nlst()

    for filename in filenames:
        print('FILANAME: ', filename)
        local_filename = os.path.join(settings.MEDIA_ROOT, settings.MEDIA_PRODUCT_IMAGE_DIR, filename)
        file = open(local_filename, 'wb')
        ftp.retrbinary('RETR ' + filename, file.write)
        file.close()

    ftp.quit()


def update_files():
    ftp = FTP(settings.FTP_SERVER)
    ftp.login(settings.FTP_USER, settings.FTP_PASS)
    ftp.cwd('upload')

    for filename in ftp.nlst():
        if filename == 'images':
            continue
        local_filename = os.path.join(settings.MEDIA_ROOT, settings.MEDIA_XML_FILES_DIR, filename)
        file = open(local_filename, 'wb')
        ftp.retrbinary('RETR ' + filename, file.write)
        file.close()

        File.objects.update_or_create(
            name=filename,
        )

    ftp.quit()


def go(filename):
    _clear_database()
    tree = ET.parse(os.path.join(settings.XML_FILES_PATH, filename))
    root = tree.getroot()
    base = root[0]

    nomenclature_types = base.findall(NOMENCLATURE_TYPES_TAG, namespaces=NAMESPACES)
    nomenclatures = base.findall(NOMENCLATURE_TAG, namespaces=NAMESPACES)
    vendors = base.findall(VENDORS_TAG, namespaces=NAMESPACES)
    nomenclature_images = base.findall(NOMENCLATURE_FILES_TAG, namespaces=NAMESPACES)
    nomenclature_prices = base.findall(NOMENCLATURE_PRICES_TAG, namespaces=NAMESPACES)
    nomenclature_shipments_and_services = base.findall(NOMENCLATURE_SHIPMENTS_AND_SERVICES, namespaces=NAMESPACES)

    _fill_nomenclature_types(nomenclature_types)
    _fill_vendors(vendors)
    _fill_nomenclature(nomenclatures)
    _fill_nomenclature_images(nomenclature_images)
    _fill_nomenclature_prices(nomenclature_prices)
    _fill_product_quantities(nomenclature_shipments_and_services)


def update_prices(filename):
    tree = ET.parse(os.path.join(settings.XML_FILES_PATH, filename))
    root = tree.getroot()
    base = root[0]

    nomenclature_types = base.findall(NOMENCLATURE_TYPES_TAG, namespaces=NAMESPACES)
    items = base.findall(NOMENCLATURE_TAG, namespaces=NAMESPACES)
    vendors = base.findall(VENDORS_TAG, namespaces=NAMESPACES)
    # prices = base.findall()

    print('ITEM_TYPES', nomenclature_types)
    print('ITEMS', items)

    for type in nomenclature_types:
        if type.find('v8:IsFolder', namespaces=NAMESPACES).text == 'true':
            continue

        # name = type.findall('v8:НаименованиеПолное', namespaces=NAMESPACES)
        name = type.find('v8:Description', namespaces=NAMESPACES).text
        ref = type.find('v8:Ref', namespaces=NAMESPACES).text
        print('NAME_1', name)
        print('REF_1', ref)

        Category.objects.update_or_create(
            ref=ref,
            defaults={
                'name': name,
            }
        )

    for vendor in vendors:
        ref = vendor.find('v8:Ref', namespaces=NAMESPACES).text
        name = vendor.find('v8:Description', namespaces=NAMESPACES).text

        Vendor.objects.update_or_create(
            ref=ref,
            defaults={
                'name': name,
            }
        )

    for item in items:
        ref = item.find('v8:Ref', namespaces=NAMESPACES).text
        name = item.find('v8:НаименованиеПолное', namespaces=NAMESPACES).text
        nomenclature_type_ref = item.find('v8:ВидНоменклатуры', namespaces=NAMESPACES).text
        description = item.find('v8:Описание', namespaces=NAMESPACES).text
        vendor_ref = item.find('v8:Производитель', namespaces=NAMESPACES).text

        # if vendor_ref == '00000000-0000-0000-0000-000000000000':
        #     Vendor.objects.update_or_create(
        #         ref='00000000-0000-0000-0000-000000000000',
        #         defaults={
        #             'name': 'Неизвестный производитель',
        #         }
        #     )

        print('NAME', name)
        print('NOMENCLATURE_TYPE_REF', nomenclature_type_ref)
        print('VENDOR_REF', vendor_ref)

        if Vendor.objects.filter(ref=vendor_ref).exists():
            vendor = Vendor.objects.get(ref=vendor_ref)
        else:
            vendor = None

        Product.objects.update_or_create(
            ref=ref,
            defaults={
                'name': name,
                'category': Category.objects.get(ref=nomenclature_type_ref),
                'description': description if description is not None else '',
                'vendor': vendor,
            }
        )

    # for items in root:
    #     for item in items:
    #         print('ITEM', item)
    #         for prop in item:
    #             print('\tPROP', prop)

# import xml.etree.ElementTree as ET
#
# from products.models import Category
#
# file_name = 'xmls/5.xml'
#
# tree = ET.parse(file_name)
# root = tree.getroot()
# items = root[0]
#
# nodes = []
#
# NO_PARENT = '00000000-0000-0000-0000-000000000000'
#
#
# def _(tag):
#     return tag.split('}')[1]
#
#
# for items in root:
#     for item in items:
#         el = {}
#         for prop in item:
#             el[_(prop.tag)] = prop.text
#
#         if el['IsFolder']:
#             category = Category.objects.create(
#                 name=el['Description'],
#                 code=el['Code'],
#                 ref=el['Ref'],
#             )
#             if Category.objects.filter(ref=el['Parent']).exists():
#                 category.parent = Category.objects.get(ref=el['Parent'])
#
#     # category = Category.objects.create(name=el['Description'],
#     # code=el['code'],
#     # delition=el['DeletionMark']
