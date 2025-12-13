# -*- coding: UTF-8 -*-
# Copyright 2025 Rumma & Ko Ltd
# License: GNU Affero General Public License v3 (see file COPYING for details)
# Developer docs: https://dev.lino-framework.org/plugins/peppol.html

import requests
import base64
import json
from commondata.peppolcodes import COUNTRY2SCHEME
from django.conf import settings


# See /docs/plugins/peppol/api.rst
DEMO_RECEIVERS = {
    "9925": "0840559537",
    "0208": "0840559537",
    "9930": "DE654321",
    "9938": "LU654321",
    "0106": "40559537",
    "9944": "NL840559537B01",
    "0190": "08405595370840559537",
}


# DEMO_SUPPLIER_ID = '273c1bdf-6258-4484-b6fb-74363721d51f'
# DEMO_SUPPLIER_ID = '997dc48c-b953-4588-81c0-761871e37e42'


root_url = "https://api.ibanity.com/einvoicing"


class EndpointID:
    vat_id = None
    scheme = None
    is_valid = False

    def __init__(self, vat_id, national_id=""):
        if vat_id:
            vat_id = vat_id.replace(" ", "").replace(".", "")
            country_code = vat_id[:2]
            if country_code not in COUNTRY2SCHEME:
                raise Exception(f"Invalid country code {country_code}")
            vat_id = vat_id[2:]
            if country_code == "BE":
                if len(vat_id) == 9:
                    vat_id = "0" + vat_id
                if not national_id:
                    national_id = vat_id
            self.vat_id = vat_id
            self.national_id = national_id
            self.country_code = country_code
            self.scheme = COUNTRY2SCHEME[country_code]
            self.is_valid = True

    def as_xml(self, tag="cbc:EndpointID", with_country=True):
        if (vat_id := self.vat_id) is None:
            return ""
        if settings.SITE.plugins.peppol.simulate_endpoints:
            vat_id = DEMO_RECEIVERS[self.scheme]
        if with_country:
            value = self.country_code + vat_id
        else:
            value = vat_id
        return f'<{tag} schemeID="{self.scheme}">{value}</{tag}>'

    def __str__(self):
        return f"{self.scheme}:{self.vat_id}"


def supplier_attrs(endpoint_id, **attrs):
    if isinstance(endpoint_id, str):
        endpoint_id = EndpointID(endpoint_id)
    attrs.update(
        enterpriseIdentification={
            "enterpriseNumber": endpoint_id.national_id,
            "vatNumber": endpoint_id.country_code + endpoint_id.vat_id})
    return attrs


def res2str(data):
    if data['type'] == "supplier":
        names = '|'.join([j['value'] for j in data['attributes']['names']])
        vat_id = data['attributes']['enterpriseIdentification']['vatNumber']
        supplier_id = data['id']
        return f"{supplier_id} = {vat_id} ({names})"
    raise Exception(f"Unknown resource {data}")


REMOVE = "/data/attributes/"


def format_errors(errors):
    parts = []
    for e in errors:
        if e['code'] == 'validationError':
            fld = e['source']['pointer']
            if fld.startswith(REMOVE):
                fld = fld[len(REMOVE):]
            parts.append(f"{fld}: {e['detail']}")
        else:
            parts.append(str(e))
    # For doctest we must sort the return value because Ibanity reports them in
    # random ordering:
    return ", ".join(sorted(parts))


class PeppolFailure(Warning):

    def __init__(self, request, response, kwargs):
        self.request = request
        self.response = response
        self.kwargs = kwargs
        super().__init__()

    def __str__(self):
        s = f"{self.request} returned "
        s += f"{self.response.status_code} {self.response.text}"
        if self.kwargs:
            s += f" (options were {self.kwargs})"
        return s


class Session:

    def __init__(self, ar, cert_file, key_file, credentials):
        if not cert_file.exists():
            raise Exception(f"Certificate file {cert_file} doesn't exist")
        if not key_file.exists():
            raise Exception(f"Key file {key_file} doesn't exist")
        self.ar = ar
        self.cert_file = cert_file
        self.key_file = key_file
        self.credentials = credentials
        # Create an HTTPS session
        self.session = requests.Session()
        # Attach client certificate and key
        self.session.cert = (self.cert_file, self.key_file)

    def get_response(self, meth_name, url, *args, **kwargs):
        meth = getattr(self.session, meth_name)
        request = f"{meth_name.upper()} {url} {args}"
        try:
            response = meth(url, *args, **kwargs)
        except Exception as e:
            raise Exception(f"{request} failed: {e}")
        if response.status_code not in {200, 201, 202, 204, 400}:
            raise PeppolFailure(request, response, kwargs)
            # logger.warning(msg)
        return response

    def get_json_response(self, meth, *args, **kwargs):
        response = self.get_response(meth, *args, **kwargs)
        # ", ".join([k+"=..." for k in kwargs.keys()])
        self.ar.logger.debug("%s %s --> %s", meth, response.url, response.text)
        return json.loads(response.text)

    def get_access_token(self):
        # Base64 encode client_id and client_secret for Basic Auth
        creds = base64.b64encode(self.credentials.encode()).decode()
        headers = {
            "Authorization": f"Basic {creds}",
            "Content-Type": "application/x-www-form-urlencoded",  # Required for OAuth2 requests
        }
        url = f"{root_url}/oauth2/token"
        data = {"grant_type": "client_credentials"}
        return self.get_json_response('post', url, data=data, headers=headers)

    def get_xml_headers(self, filename="invoices.xml"):
        headers = self.get_json_headers()
        headers["Content-Type"] = "application/xml"
        headers["Content-Disposition"] = f"inline; filename={filename}"
        return headers

    def get_json_headers(self, accept="application/vnd.api+json"):
        headers = self.get_auth_headers()
        headers["Accept"] = accept
        return headers

    def get_auth_headers(self):
        rv = self.get_access_token()
        access_token = rv['access_token']
        headers = {
            "Authorization": f"Bearer {access_token}"
        }
        return headers

    def list_suppliers(self, limit=1000, hide_offboarded=True, hide_unknown=True):
        # Iterate over all the suppliers. Note that Ibanity cannot
        # delete a supplier.
        # The docs say that default page size is 2000, but AFAICS it is 20.
        # TODO: should we inspect resp['meta'] in case there are multiple pages?

        # params = dict(page=dict(number=1, size=limit))
        # url = f"{root_url}/suppliers?" + urlencode(params)
        kwargs = dict(headers=self.get_json_headers())
        kwargs.update(params={'page[number]': 0, 'page[size]': limit})
        # kwargs.update(params={'page[size]': limit})
        url = f"{root_url}/suppliers?"
        resp = self.get_json_response('get', url, **kwargs)
        if settings.SITE.plugins.peppol.with_suppliers:
            Supplier = settings.SITE.models.peppol.Supplier
        else:
            hide_unknown = False
        for sup_data in resp['data']:
            if sup_data['type'] != "supplier":
                raise Exception(f"Invalid supplier type in {sup_data}")
                # logger.info("Invalid supplier type '%s'", sup_data['type'])
                # continue
            if hide_offboarded:
                if sup_data['attributes']['onboardingStatus'] == "OFFBOARDED":
                    self.ar.debug("Ignore offboarded supplier '%s'", sup_data)
                    continue
            if hide_unknown:
                if not Supplier.objects.filter(supplier_id=sup_data['id']).exists():
                    self.ar.debug("Ignore unknown supplier '%s'", sup_data)
                    continue
            yield sup_data

    def find_supplier_by_eid(self, endpoint_id):
        # print(f"20250612 find_supplier_by_eid {endpoint_id}")
        for data in self.list_suppliers(hide_unknown=False):
            attrs = data['attributes']
            eid = attrs['enterpriseIdentification']
            # print(f"20250612 {eid} {data['attributes']['names']}")
            if eid['enterpriseNumber'] == endpoint_id.national_id:
                return data
            if eid['vatNumber'] == endpoint_id.vat_id:
                # print("20250612 - yes")
                return data

    def get_supplier(self, supplier_id):
        url = f"{root_url}/suppliers/{supplier_id}"
        try:
            resp = self.get_json_response('get', url, headers=self.get_json_headers())
        except PeppolFailure as e:
            return None, str(e)
        if (errors := resp.get('errors', None)):
            return None, format_errors(errors)
        return resp['data'], None

    def create_supplier(self, **attributes):
        # returns a tuple (data, errmsg) where:
        # - data is a dict(data, id, type) when errmsg is None
        # - data is None when errmsg is not None
        url = f"{root_url}/suppliers/"
        # if (eid := attributes.get('enterpriseIdentification')) is None:
        #     return None, "No enterpriseIdentification"
        # if (vat_id := eid.get('vatNumber')) is None:
        #     return None, "No vatNumber"
        # if (sup_data := self.find_supplier_by_eid(vat_id)) is not None:
        #     sup_id = sup_data['id']
        #     self.ar.debug("Reuse offboarded supplier %s with VAT id %s", sup_id, vat_id)
        #     attributes['onboardingStatus'] = "CREATED"
        #     return self.update_supplier(sup_id, **attributes)
        sup_data = {
            "type": "supplier",
            "attributes": attributes}
        data = {"data": sup_data}
        resp = self.get_json_response(
            'post', url, json=data, headers=self.get_json_headers())
        if (errors := resp.get('errors', None)):
            return None, format_errors(errors)
        return resp['data'], None

    def update_supplier(self, supplier_id, **attributes):
        # https://documentation.ibanity.com/einvoicing/1/api/curl#update-supplier
        url = f"{root_url}/suppliers/{supplier_id}"
        data = {"data": {
            "id": supplier_id,
            "type": "supplier",
            "attributes": attributes
        }}
        resp = self.get_json_response(
            'patch', url, json=data, headers=self.get_json_headers())
        if (errors := resp.get('errors', None)):
            return None, format_errors(errors)
        return resp['data'], None

    def delete_supplier(self, supplier_id):
        # print(f"20250613 delete remote supplier {supplier_id}")
        url = f"{root_url}/suppliers/{supplier_id}"
        self.get_response('delete', url, headers=self.get_json_headers())

    def list_registrations(self, supplier_id):
        url = f"{root_url}/peppol/suppliers/{supplier_id}/registrations"
        resp = self.get_json_response('get', url, headers=self.get_json_headers())
        if (errors := resp.get('errors', None)):
            raise Exception(format_errors(errors))
        for reg_data in resp['data']:
            yield reg_data

    def create_outbound_document(self, supplier_id, filename, credit_note=False):
        doc_type = 'credit-notes' if credit_note else 'invoices'
        url = f"{root_url}/peppol/suppliers/{supplier_id}/{doc_type}?"
        headers = self.get_xml_headers(filename.name)
        # data = filename.read_text()
        data = filename.read_bytes()
        return self.get_json_response('post', url, data=data, headers=headers)

    def get_outbound_document(self, supplier_id, doc_id, credit_note=False):
        doc_type = 'credit-notes' if credit_note else 'invoices'
        url = f"{root_url}/peppol/suppliers/{supplier_id}/{doc_type}/{doc_id}"
        return self.get_json_response('get', url, headers=self.get_json_headers())

    def list_outbound_documents(self, supplier_id, fromStatusChanged, **params):
        # fromStatusChanged must be a datetime.datetime instance
        # supported params include fromStatusChanged, toStatusChanged & more
        url = f"{root_url}/peppol/documents"
        params.update(fromStatusChanged=fromStatusChanged.isoformat())
        params.update(supplierId=supplier_id)
        return self.get_json_response(
            'get', url, headers=self.get_json_headers(), params=params)

    def list_inbound_documents(self, supplier_id, **params):
        url = f"{root_url}/peppol/inbound-documents"
        params.update(supplierId=supplier_id)
        return self.get_json_response(
            'get', url, headers=self.get_json_headers(), params=params)

    def get_inbound_document_xml(self, doc_id):
        url = f"{root_url}/peppol/inbound-documents/{doc_id}"
        rsp = self.get_response(
            'get', url, headers=self.get_json_headers("application/xml"))
        return rsp.text

    def get_inbound_document_json(self, doc_id):
        url = f"{root_url}/peppol/inbound-documents/{doc_id}"
        return self.get_json_response(
            'get', url, headers=self.get_json_headers())

    # Customer search. Check whether my customer exists.
    # Belgian participants are registered with the Belgian company number, for which
    # identifier 0208 can be used. Optionally, the customer can be registered with
    # their VAT number, for which identifier 9925 can be used.
    # The Flowin sandbox contains hard-coded fake data.  Using another reference as
    # customerReference will in result a 404
    def customer_search(self, customerReference):
        url = f"{root_url}/peppol/customer-searches"
        data = {
            "type": "peppolCustomerSearch",
            # "id": str(uuid.uuid4()),
            "attributes": {
                "customerReference": customerReference,
                # "supportedDocumentFormats": doc_formats
            }
        }
        data = {"data": data}
        # pprint(data)
        return self.get_json_response('post', url, headers=self.get_json_headers(), json=data)
