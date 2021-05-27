from hellosign_sdk.utils import HSRequest, HSException, NoAuthMethod, HSAccessTokenAuth, HSFormat, api_resource, api_resource_list
from hellosign_sdk.resource import Account, ApiApp, SignatureRequest, Template, Team, Embedded, UnclaimedDraft
from requests.auth import HTTPBasicAuth
import json

#
# The MIT License (MIT)
#
# Copyright (C) 2014 hellosign.com
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.
#


class HSClient(object):

    ''' Client object to interact with the API urls
    Most of the operations of the SDK is made through this object. Please refer
    to the README.rst file for more details on how to use the client object.

    '''

    version = '4.0.0'   # SDK version
    API_VERSION = 'v3'  # API version
    API_URL = ''

    ACCOUNT_CREATE_URL = ''
    ACCOUNT_INFO_URL = ''
    ACCOUNT_UPDATE_URL = ''
    ACCOUNT_VERIFY_URL = ''

    SIGNATURE_REQUEST_INFO_URL = ''
    SIGNATURE_REQUEST_LIST_URL = ''
    SIGNATURE_REQUEST_DOWNLOAD_PDF_URL = ''
    SIGNATURE_REQUEST_CREATE_URL = ''
    SIGNATURE_REQUEST_CREATE_WITH_TEMPLATE_URL = ''
    SIGNATURE_REQUEST_REMIND_URL = ''
    SIGNATURE_REQUEST_CANCEL_URL = ''
    SIGNATURE_REQUEST_CREATE_EMBEDDED_URL = ''
    SIGNATURE_REQUEST_CREATE_EMBEDDED_WITH_TEMPLATE_URL = ''

    EMBEDDED_OBJECT_GET_URL = ''
    EMBEDDED_TEMPLATE_EDIT_URL = ''

    UNCLAIMED_DRAFT_CREATE_URL = ''
    UNCLAIMED_DRAFT_CREATE_EMBEDDED_URL = ''
    UNCLAIMED_DRAFT_CREATE_EMBEDDED_WITH_TEMPLATE_URL = ''
    UNCLAIMED_DRAFT_EDIT_AND_RESEND_URL = ''

    TEMPLATE_GET_URL = ''
    TEMPLATE_GET_LIST_URL = ''
    TEMPLATE_GET_FILES_URL = ''
    TEMPLATE_DELETE_URL = ''
    TEMPLATE_ADD_USER_URL = ''
    TEMPLATE_REMOVE_USER_URL = ''
    TEMPLATE_CREATE_EMBEDDED_DRAFT_URL = ''

    TEAM_INFO_URL = ''
    TEAM_UPDATE_URL = ''
    TEAM_CREATE_URL = ''
    TEAM_DESTROY_URL = ''
    TEAM_ADD_MEMBER_URL = ''
    TEAM_REMOVE_MEMBER_URL = ''

    API_APP_INFO_URL = ''
    API_APP_LIST_URL = ''
    API_APP_CREATE_URL = ''
    API_APP_UPDATE_URL = ''
    API_APP_DELETE_URL = ''

    OAUTH_TOKEN_URL = ''

    request = None
    response_callback = None

    def __init__(self, email_address=None, password=None, api_key=None, access_token=None, access_token_type='Bearer', env='production'):
        '''Initialize the client object with authentication information to send requests

        Args:
            email_address (str): E-mail of the account to make the requests

            password (str): Password of the account used with email address

            api_key (str): API Key. You can find your API key in https://app.hellosign.com/home/myAccount/current_tab/integrations#api

            access_token (str): OAuth access token to use

            access_token_type (str): Type of OAuth token (defaults to Bearer, which is the only value supported for now)

        '''

        super(HSClient, self).__init__()
        self.auth = self._authenticate(email_address, password, api_key, access_token, access_token_type)
        self.account = Account()
        self.env = env
        self._init_endpoints()

    def __str__(self):
        ''' Return a string description of this object '''
        return "HelloSign Client %s" % self.version

    def _init_endpoints(self):

        API_PRODUCTION_URL = "https://api.hellosign.com"
        API_DEV_URL = "https://api.dev-hellosign.com"
        API_STAGING_URL = "https://api.staging-hellosign.com"

        WEB_PRODUCTION_URL = "https://app.hellosign.com"
        WEB_DEV_URL = "https://app.dev-hellosign.com"
        WEB_STAGING_URL = "https://app.staging-hellosign.com"

        if self.env == "production":
            self.API_URL = API_PRODUCTION_URL + '/' + self.API_VERSION
            self.OAUTH_TOKEN_URL = WEB_PRODUCTION_URL + '/oauth/token'
        elif self.env == "dev":
            self.API_URL = API_DEV_URL + '/' + self.API_VERSION
            self.OAUTH_TOKEN_URL = WEB_DEV_URL + '/oauth/token'
            print("WARNING: Using dev api endpoint %s" % self.API_URL)
        elif self.env == "staging":
            self.API_URL = API_STAGING_URL + '/' + self.API_VERSION
            self.OAUTH_TOKEN_URL = WEB_STAGING_URL + '/oauth/token'
            print("WARNING: Using staging api endpoint %s" % self.API_URL)

        self.ACCOUNT_CREATE_URL = self.API_URL + '/account/create'
        self.ACCOUNT_INFO_URL = self.API_URL + '/account'
        self.ACCOUNT_UPDATE_URL = self.API_URL + '/account'
        self.ACCOUNT_VERIFY_URL = self.API_URL + '/account/verify'

        self.SIGNATURE_REQUEST_INFO_URL = self.API_URL + '/signature_request/'
        self.SIGNATURE_REQUEST_LIST_URL = self.API_URL + '/signature_request/list'
        self.SIGNATURE_REQUEST_DOWNLOAD_PDF_URL = self.API_URL + '/signature_request/files/'
        self.SIGNATURE_REQUEST_CREATE_URL = self.API_URL + '/signature_request/send'
        self.SIGNATURE_REQUEST_CREATE_WITH_TEMPLATE_URL = self.API_URL + '/signature_request/send_with_template'
        self.SIGNATURE_REQUEST_REMIND_URL = self.API_URL + '/signature_request/remind/'
        self.SIGNATURE_REQUEST_UPDATE_URL = self.API_URL + '/signature_request/update/'
        self.SIGNATURE_REQUEST_CANCEL_URL = self.API_URL + '/signature_request/cancel/'
        self.SIGNATURE_REQUEST_REMOVE_ACCESS_URL = self.API_URL + '/signature_request/remove/'
        self.SIGNATURE_REQUEST_CREATE_EMBEDDED_URL = self.API_URL + '/signature_request/create_embedded'
        self.SIGNATURE_REQUEST_CREATE_EMBEDDED_WITH_TEMPLATE_URL = self.API_URL + '/signature_request/create_embedded_with_template'

        self.EMBEDDED_OBJECT_GET_URL = self.API_URL + '/embedded/sign_url/'
        self.EMBEDDED_TEMPLATE_EDIT_URL = self.API_URL + '/embedded/edit_url/'

        self.UNCLAIMED_DRAFT_CREATE_URL = self.API_URL + '/unclaimed_draft/create'
        self.UNCLAIMED_DRAFT_CREATE_EMBEDDED_URL = self.API_URL + '/unclaimed_draft/create_embedded'
        self.UNCLAIMED_DRAFT_CREATE_EMBEDDED_WITH_TEMPLATE_URL = self.API_URL + '/unclaimed_draft/create_embedded_with_template'
        self.UNCLAIMED_DRAFT_EDIT_AND_RESEND_URL = self.API_URL + '/unclaimed_draft/edit_and_resend/'

        self.TEMPLATE_GET_URL = self.API_URL + '/template/'
        self.TEMPLATE_GET_LIST_URL = self.API_URL + '/template/list'
        self.TEMPLATE_GET_FILES_URL = self.API_URL + '/template/files/'
        self.TEMPLATE_DELETE_URL = self.API_URL + '/template/delete/'
        self.TEMPLATE_ADD_USER_URL = self.API_URL + '/template/add_user/'
        self.TEMPLATE_REMOVE_USER_URL = self.API_URL + '/template/remove_user/'
        self.TEMPLATE_CREATE_EMBEDDED_DRAFT_URL = self.API_URL + '/template/create_embedded_draft'
        self.TEMPLATE_UPDATE_FILES_URL = self.API_URL + '/template/update_files/'

        self.TEAM_INFO_URL = self.API_URL + '/team'
        self.TEAM_UPDATE_URL = self.TEAM_INFO_URL
        self.TEAM_CREATE_URL = self.API_URL + '/team/create'
        self.TEAM_DESTROY_URL = self.API_URL + '/team/destroy'
        self.TEAM_ADD_MEMBER_URL = self.API_URL + '/team/add_member'
        self.TEAM_REMOVE_MEMBER_URL = self.API_URL + '/team/remove_member'

        self.API_APP_INFO_URL = self.API_URL + '/api_app/'
        self.API_APP_LIST_URL = self.API_URL + '/api_app/list'
        self.API_APP_CREATE_URL = self.API_URL + '/api_app'
        self.API_APP_UPDATE_URL = self.API_APP_INFO_URL
        self.API_APP_DELETE_URL = self.API_APP_INFO_URL

    #  ----  ACCOUNT METHODS  -----------------------------

    @api_resource(Account)
    def create_account(self, email_address, password=None, client_id=None, client_secret=None):
        ''' Create a new account.

        If the account is created via an app, then Account.oauth will contain the
        OAuth data that can be used to execute actions on behalf of the newly created account.

        Args:
            email_address (str): Email address of the new account to create

            password (str): [DEPRECATED] This parameter will be ignored

            client_id (str, optional): Client id of the app to use to create this account

            client_secret (str, optional): Secret of the app to use to create this account

        Returns:
            The new Account object

        '''
        request = self._get_request()

        params = {
            'email_address': email_address
        }
        if client_id:
            params['client_id'] = client_id
            params['client_secret'] = client_secret

        response = request.post(self.ACCOUNT_CREATE_URL, params)

        if 'oauth_data' in response:
            response["account"]["oauth"] = response['oauth_data']

        return response

    # Get account info and put in self.account so that further access to the
    # info can be made by using self.account.attribute
    def get_account_info(self):
        ''' Get current account information

        The information then will be saved in `self.account` so that you can
        access the information like this:

        >>> hsclient = HSClient()
        >>> acct = hsclient.get_account_info()
        >>> print acct.email_address

        Returns:
            An Account object

        '''
        request = self._get_request()
        response = request.get(self.ACCOUNT_INFO_URL)
        self.account.json_data = response["account"]
        return self.account

    # At the moment you can only update your callback_url only
    @api_resource(Account)
    def update_account_info(self):
        ''' Update current account information

        At the moment you can only update your callback_url.

        Returns:
            An Account object

        '''
        request = self._get_request()
        return request.post(self.ACCOUNT_UPDATE_URL, {
            'callback_url': self.account.callback_url
        })

    def verify_account(self, email_address):
        ''' Verify whether a HelloSign Account exists

        Args:

            email_address (str): Email address of the new account to create

        Returns:
            True or False
        '''
        request = self._get_request()
        resp = request.post(self.ACCOUNT_VERIFY_URL, {
            'email_address': email_address
        })
        return ('account' in resp)

    #  ----  SIGNATURE REQUEST METHODS  -------------------

    @api_resource(SignatureRequest)
    def get_signature_request(self, signature_request_id):
        ''' Get a signature request by its ID

        Args:

            signature_request_id (str): The id of the SignatureRequest to retrieve

        Returns:
            A SignatureRequest object

        '''

        request = self._get_request()
        parameters = None

        return request.get(self.SIGNATURE_REQUEST_INFO_URL + signature_request_id, parameters=parameters)

    @api_resource_list(SignatureRequest)
    def get_signature_request_list(self, page=1, page_size=None):
        ''' Get a list of SignatureRequest that you can access

        This includes SignatureRequests you have sent as well as received, but
        not ones that you have been CCed on.

        Args:

            page (int, optional): Which page number of the SignatureRequest list to return. Defaults to 1.
            page_size (int, optional): Number of SignatureRequests to return per page. When not explicit
                                       it defaults to 20.

        Returns:
            A ResourceList object

        '''

        request = self._get_request()
        parameters = {
            "page": page,
            "page_size": page_size
        }

        return request.get(self.SIGNATURE_REQUEST_LIST_URL, parameters=parameters)

    def get_signature_request_file(self, signature_request_id, path_or_file=None, file_type=None, filename=None, response_type=None):
        ''' Download the PDF copy of the current documents

        Args:

            signature_request_id (str): Id of the signature request

            path_or_file (str or file): A writable File-like object or a full path to save the PDF file to.

            filename (str): [DEPRECATED] Filename to save the PDF file to. This should be a full path.

            file_type (str): Type of file to return. Either "pdf" for a single merged document or "zip"
            for a collection of individual documents. Defaults to "pdf" if not specified.

            response_type (str): File type of response to return. Either "url" to return a URL link to the file
            or "data_uri" to return the file as a base64 encoded string. Only applicable to the "pdf" file_type.

        Returns:
            Returns a PDF file, URL link to file, or base64 encoded file

        '''
        request = self._get_request()
        url = self.SIGNATURE_REQUEST_DOWNLOAD_PDF_URL + signature_request_id

        if response_type == 'url':
            url += '?get_url=1'
        elif response_type == 'data_uri':
            url += '?get_data_uri=1'
        else:
            if file_type:
                url += '?file_type=%s' % file_type
            return request.get_file(url, path_or_file or filename)

        return request.get(url)

    def send_signature_request(self, test_mode=False, client_id=None, files=None, file_urls=None,
            title=None, subject=None, message=None, signing_redirect_url=None,
            signers=None, cc_email_addresses=None, form_fields_per_document=None,
            use_text_tags=False, hide_text_tags=False, custom_fields=None,
            metadata=None, allow_decline=False, allow_reassign=False, signing_options=None, attachments=None):
        ''' Creates and sends a new SignatureRequest with the submitted documents

        Creates and sends a new SignatureRequest with the submitted documents.
        If form_fields_per_document is not specified, a signature page will be
        affixed where all signers will be required to add their signature,
        signifying their agreement to all contained documents.

        Args:

            test_mode (bool, optional): Whether this is a test, the signature request will not be legally binding
            if set to True. Defaults to False.

            client_id (str): Pass client_id. For non embedded requests this can be used for white-labeling

            files (list of str): The uploaded file(s) to send for signature.

            file_urls (list of str): URLs of the file for HelloSign to download to send for signature. Use either `files` or `file_urls`

            title (str, optional): The title you want to assign to the SignatureRequest.

            subject (str, optional): The subject in the email that will be sent to the signers.

            message (str, optional): The custom message in the email that will be sent to the signers.

            signing_redirect_url (str, optional): The URL you want the signer redirected to after they successfully sign.

            signers (list of dict): A list of signers, which each has the following attributes:

                name (str): The name of the signer
                email_address (str): Email address of the signer
                order (str, optional): The order the signer is required to sign in
                pin (str, optional): The 4- to 12-character access code that will secure this signer's signature page

            cc_email_addresses (list, optional): A list of email addresses that should be CC'd on the request.

            form_fields_per_document (str or list of dict, optional): The signer components that should appear on the document, expressed as a serialized
            JSON data structure which is a list of lists of the form fields. Please refer to the API reference of HelloSign for more details (https://app.hellosign.com/api/reference#SignatureRequest).

            use_text_tags (bool, optional): Use text tags in the provided file(s) to specify signer components.

            hide_text_tags (bool, optional): Hide text tag areas.

            custom_fields (list of dict, optional): A list of custom fields defined by Text Tags for Form Fields per Document.
            An item of the list should look like this: `{'name: value'}`

            metadata (dict, optional): Metadata associated with the signature request.

            allow_decline (bool, optional): Allows signers to decline to sign a document if set to True. Defaults to False.

            allow_reassign (bool, optional): Allows signers to reassign their signature requests to other signers if set to True. Defaults to False.

            signing_options (dict, optional): Allows the requester to specify the types allowed for creating a signature. Defaults to account settings.

            attachments (list of dict):            A list of attachments, each with the following attributes:
                name (str):                        The name of the attachment
                instructions (str):                The instructions for uploading the attachment
                signer_index (int):                The index of the signer who needs to upload the attachments, see signers parameter for more details
                required (bool, optional):         Determines if the attachment must be uploaded

        Returns:
            A SignatureRequest object

        '''

        self._check_required_fields({
            "signers": signers
        }, [{
            "files": files,
            "file_urls": file_urls
            }]
        )

        params = {
            'test_mode': test_mode,
            'client_id': client_id,
            'files': files,
            'file_urls': file_urls,
            'title': title,
            'subject': subject,
            'message': message,
            'signing_redirect_url': signing_redirect_url,
            'signers': signers,
            'cc_email_addresses': cc_email_addresses,
            'form_fields_per_document': form_fields_per_document,
            'use_text_tags': use_text_tags,
            'hide_text_tags': hide_text_tags,
            'custom_fields': custom_fields,
            'metadata': metadata,
            'allow_decline': allow_decline,
            'allow_reassign': allow_reassign,
            'signing_options': signing_options,
            'attachments': attachments
        }

        return self._send_signature_request(**params)

    def send_signature_request_with_template(self, test_mode=False, template_id=None,
            template_ids=None, title=None, subject=None, message=None,
            signing_redirect_url=None, signers=None, ccs=None, custom_fields=None,
            metadata=None, allow_decline=False, files=None, file_urls=None, signing_options=None):
        ''' Creates and sends a new SignatureRequest based off of a Template

        Creates and sends a new SignatureRequest based off of the Template
        specified with the template_id parameter.

        Args:

            test_mode (bool, optional): Whether this is a test, the signature request will not be legally binding if set to True. Defaults to False.

            template_id (str): The id of the Template to use when creating the SignatureRequest. Mutually exclusive with template_ids.

            template_ids (list): The ids of the Templates to use when creating the SignatureRequest. Mutually exclusive with template_id.

            title (str, optional): The title you want to assign to the SignatureRequest

            subject (str, optional): The subject in the email that will be sent to the signers

            message (str, optional): The custom message in the email that will be sent to the signers

            signing_redirect_url (str, optional): The URL you want the signer redirected to after they successfully sign.

            signers (list of dict): A list of signers, which each has the following attributes:

                role_name (str): Signer role
                name (str): The name of the signer
                email_address (str): Email address of the signer
                pin (str, optional): The 4- to 12-character access code that will secure this signer's signature page

            ccs (list of str, optional): The email address of the CC filling the role of RoleName.
            Required when a CC role exists for the Template. Each dict has the following attributes:

                role_name (str): CC role name
                email_address (str): CC email address

            custom_fields (list of dict, optional): A list of custom fields.
            Required when a CustomField exists in the Template. An item of the list should look like this: `{'name: value'}`

            metadata (dict, optional): Metadata to associate with the signature request

            allow_decline (bool, optional): Allows signers to decline to sign a document if set to 1. Defaults to 0.

            files (list of str): The uploaded file(s) to append to the Signature Request.

            file_urls (list of str): URLs of the file for HelloSign to download to append to the Signature Request.
            Use either `files` or `file_urls`

            signing_options (dict, optional): Allows the requester to specify the types allowed for creating a signature.
            Defaults to account settings.

        Returns:
            A SignatureRequest object

        '''

        self._check_required_fields({
            "signers": signers
        }, [{
            "template_id": template_id,
            "template_ids": template_ids,
            "files": files,
            "file_urls": file_urls
            }]
        )

        params = {
            'test_mode': test_mode,
            'template_id': template_id,
            'template_ids': template_ids,
            'title': title,
            'subject': subject,
            'message': message,
            'signing_redirect_url': signing_redirect_url,
            'signers': signers,
            'ccs': ccs,
            'custom_fields': custom_fields,
            'metadata': metadata,
            'allow_decline': allow_decline,
            'files': files,
            'file_urls': file_urls,
            'signing_options': signing_options
        }

        return self._send_signature_request_with_template(**params)

    @api_resource(SignatureRequest)
    def remind_signature_request(self, signature_request_id, email_address, name=None):
        ''' Sends an email to the signer reminding them to sign the signature request

        Sends an email to the signer reminding them to sign the signature
        request. You cannot send a reminder within 1 hours of the last reminder
        that was sent. This includes manual AND automatic reminders.

        Args:

            signature_request_id (str): The id of the SignatureRequest to send a reminder for

            email_address (str): The email address of the signer to send a reminder to

            name (str, optional): The name of the signer to send a reminder to

        Returns:
            A SignatureRequest object

        '''
        request = self._get_request()
        return request.post(self.SIGNATURE_REQUEST_REMIND_URL + signature_request_id, data={
            "email_address": email_address,
            "name": name
        })

    @api_resource(SignatureRequest)
    def update_signature_request(self, signature_request_id, signature_id, email_address):
        ''' Updates the email address for a given signer on a signature request.

        Args:

            signature_request_id (str): The id of the SignatureRequest to update

            signature_id (str): The signature id for the recipient

            email_address (str): The new email address of the recipient

        Returns:
            A SignatureRequest object

        '''
        request = self._get_request()
        return request.post(self.SIGNATURE_REQUEST_UPDATE_URL + signature_request_id, data={
            "signature_id": signature_id,
            "email_address": email_address
        })

    def cancel_signature_request(self, signature_request_id):
        ''' Cancels a SignatureRequest

        Cancels a SignatureRequest. After canceling, no one will be able to sign
        or access the SignatureRequest or its documents. Only the requester can
        cancel and only before everyone has signed.

        Args:

            signature_request_id (str): The id of the signature request to cancel

        Returns:
            None

        '''
        request = self._get_request()
        request.post(url=self.SIGNATURE_REQUEST_CANCEL_URL + signature_request_id, get_json=False)

    def remove_signature_request_access(self, signature_request_id):
        ''' Removes your access to a completed SignatureRequest

        The SignatureRequest must be fully executed by all parties (signed or declined to sign).
        Other parties will continue to maintain access to the completed signature request document(s).

        Args:

            signature_request_id (str): The id of the signature request to remove

        Returns:
            None

        '''
        request = self._get_request()
        request.post(url=self.SIGNATURE_REQUEST_REMOVE_ACCESS_URL + signature_request_id, get_json=False)

    def send_signature_request_embedded(self, test_mode=False, client_id=None,
            files=None, file_urls=None, title=None, subject=None, message=None,
            signing_redirect_url=None, signers=None, cc_email_addresses=None,
            form_fields_per_document=None, use_text_tags=False, hide_text_tags=False,
            metadata=None, allow_decline=False, allow_reassign=False, signing_options=None, attachments=None):
        ''' Creates and sends a new SignatureRequest with the submitted documents

        Creates a new SignatureRequest with the submitted documents to be signed
        in an embedded iFrame. If form_fields_per_document or text tags are not specified, a
        signature page will be affixed where all signers will be required to add
        their signature, signifying their agreement to all contained documents.
        Note that embedded signature requests can only be signed in embedded
        iFrames whereas normal signature requests can only be signed on
        HelloSign.

        Args:

            test_mode (bool, optional): Whether this is a test, the signature request will not be legally binding if set to True. Defaults to False.

            client_id (str): Client id of the app you're using to create this embedded signature request.
            Visit the embedded page to learn more about this parameter (https://www.hellosign.com/api/embeddedSigningWalkthrough)

            files (list of str): The uploaded file(s) to send for signature

            file_urls (list of str): URLs of the file for HelloSign to download to send for signature. Use either `files` or `file_urls`

            title (str, optional): The title you want to assign to the SignatureRequest

            subject (str, optional): The subject in the email that will be sent to the signers

            message (str, optional): The custom message in the email that will be sent to the signers

            signing_redirect_url (str, optional): The URL you want the signer redirected to after they successfully sign.

            signers (list of dict): A list of signers, which each has the following attributes:

                name (str): The name of the signer
                email_address (str): Email address of the signer
                order (str, optional): The order the signer is required to sign in
                pin (str, optional): The 4- to 12-character access code that will secure this signer's signature page

            cc_email_addresses (list, optional): A list of email addresses that should be CCed

            form_fields_per_document (str or list of dict, optional): The fields that should appear on the document, expressed as a serialized
            JSON data structure which is a list of lists of the form fields. Please refer to the API reference of HelloSign for more details (https://www.hellosign.com/api/reference#SignatureRequest)

            use_text_tags (bool, optional): Use text tags in the provided file(s) to create form fields

            hide_text_tags (bool, optional): Hide text tag areas

            metadata (dict, optional): Metadata to associate with the signature request

            allow_decline (bool, optional): Allows signers to decline to sign a document if set to 1. Defaults to 0.

            allow_reassign (bool, optional): Allows signers to reassign their signature requests to other signers if set to True. Defaults to False.

            signing_options (dict, optional): Allows the requester to specify the types allowed for creating a signature. Defaults to account settings.

            attachments (list of dict):            A list of attachments, each with the following attributes:
                name (str):                        The name of attachment
                instructions (str):                The instructions for uploading the attachment
                signer_index (int):                The signer's index whose needs to upload the attachments, see signers parameter for more details
                required (bool, optional):         Determines if the attachment must be uploaded


        Returns:
            A SignatureRequest object

        '''

        self._check_required_fields({
            "signers": signers,
            "client_id": client_id
        }, [{
            "files": files,
            "file_urls": file_urls
            }]
        )

        params = {
            'test_mode': test_mode,
            'client_id': client_id,
            'files': files,
            'file_urls': file_urls,
            'title': title,
            'subject': subject,
            'message': message,
            'signing_redirect_url': signing_redirect_url,
            'signers': signers,
            'cc_email_addresses': cc_email_addresses,
            'form_fields_per_document': form_fields_per_document,
            'use_text_tags': use_text_tags,
            'hide_text_tags': hide_text_tags,
            'metadata': metadata,
            'allow_decline': allow_decline,
            'allow_reassign': allow_reassign,
            'signing_options': signing_options,
            'is_for_embedded_signing': True,
            'attachments': attachments
        }

        return self._send_signature_request(**params)

    def send_signature_request_embedded_with_template(self, test_mode=False,
            client_id=None, template_id=None, template_ids=None, title=None,
            subject=None, message=None, signing_redirect_url=None, signers=None,
            ccs=None, custom_fields=None, metadata=None, allow_decline=False,
            files=None, file_urls=None, signing_options=None):
        ''' Creates and sends a new SignatureRequest based off of a Template

        Creates a new SignatureRequest based on the given Template to be
        signed in an embedded iFrame. Note that embedded signature requests can
        only be signed in embedded iFrames whereas normal signature requests can
        only be signed on HelloSign.

        Args:

            test_mode (bool, optional): Whether this is a test, the signature request will not be legally binding if set to True. Defaults to False.

            client_id (str): Client id of the app you're using to create this embedded signature request.
            Visit the embedded page to learn more about this parameter (https://app.hellosign.com/api/embeddedSigningWalkthrough)

            template_id (str): The id of the Template to use when creating the SignatureRequest. Mutually exclusive with template_ids.

            template_ids (list): The ids of the Templates to use when creating the SignatureRequest. Mutually exclusive with template_id.

            title (str, optional): The title you want to assign to the SignatureRequest

            subject (str, optional): The subject in the email that will be sent to the signers

            message (str, optional): The custom message in the email that will be sent to the signers

            signing_redirect_url (str, optional): The URL you want the signer redirected to after they successfully sign.

            signers (list of dict): A list of signers, which each has the following attributes:

                name (str): The name of the signer
                email_address (str): Email address of the signer
                pin (str, optional): The 4- to 12-character access code that will secure this signer's signature page

            ccs (list of dict, optional): The email address of the CC filling the role of RoleName.
            Required when a CC role exists for the Template. Each dict has the following attributes:

                role_name (str): CC role name
                email_address (str): CC email address

            custom_fields (list of dict, optional): A list of custom fields. Required when a CustomField exists in the Template.
            An item of the list should look like this: `{'name: value'}`

            metadata (dict, optional): Metadata to associate with the signature request

            allow_decline (bool, optional): Allows signers to decline to sign a document if set to 1. Defaults to 0.

            files (list of str): The uploaded file(s) to append to the Signature Request.

            file_urls (list of str): URLs of the file for HelloSign to download to append to the Signature Request. Use either `files` or `file_urls`

            signing_options (dict, optional): Allows the requester to specify the types allowed for creating a signature. Defaults to account settings.

        Returns:
            A SignatureRequest object

        '''

        self._check_required_fields({
            "signers": signers,
            "client_id": client_id
        }, [{
            "template_id": template_id,
            "template_ids": template_ids,
            "files": files,
            "file_urls": file_urls
            }]
        )

        params = {
            'test_mode': test_mode,
            'client_id': client_id,
            'template_id': template_id,
            'template_ids': template_ids,
            'title': title,
            'subject': subject,
            'message': message,
            'signing_redirect_url': signing_redirect_url,
            'signers': signers,
            'ccs': ccs,
            'custom_fields': custom_fields,
            'metadata': metadata,
            'allow_decline': allow_decline,
            'files': files,
            'file_urls': file_urls,
            'signing_options': signing_options
        }

        return self._send_signature_request_with_template(**params)

    #  ----  TEMPLATE METHODS  -----------------------

    @api_resource(Template)
    def get_template(self, template_id):
        ''' Gets a Template which includes a list of Accounts that can access it

        Args:

            template_id (str): The id of the template to retrieve

        Returns:
            A Template object

        '''
        request = self._get_request()
        return request.get(self.TEMPLATE_GET_URL + template_id)

    @api_resource_list(Template)
    def get_template_list(self, page=1, page_size=None, account_id=None, query=None):
        ''' Lists your Templates

        Args:

            page (int, optional): Page number of the template List to return. Defaults to 1.

            page_size (int, optional): Number of objects to be returned per page, must be between 1 and 100, default is 20.

            account_id (str, optional): Which account to return Templates for. Must be a team member.
            Use "all" to indicate all team members. Defaults to your account.

            query (str, optional): String that includes search terms and/or fields to be used to filter the Template objects.

        Returns:
            A ResourceList object

        '''
        request = self._get_request()
        parameters = {
            'page': page,
            'page_size': page_size,
            'account_id': account_id,
            'query': query
        }
        return request.get(self.TEMPLATE_GET_LIST_URL, parameters=parameters)

    # RECOMMEND: this api does not fail if the user has been added...
    def add_user_to_template(self, template_id, account_id=None, email_address=None):
        ''' Gives the specified Account access to the specified Template

        Args:

            template_id (str): The id of the template to give the account access to

            account_id (str): The id of the account to give access to the template. The account id prevails if both account_id and email_address are provided.

            email_address (str): The email address of the account to give access to.

        Returns:
            A Template object

        '''
        return self._add_remove_user_template(self.TEMPLATE_ADD_USER_URL, template_id, account_id, email_address)

    def remove_user_from_template(self, template_id, account_id=None, email_address=None):
        ''' Removes the specified Account's access to the specified Template

        Args:

            template_id (str): The id of the template to remove the account's access from.

            account_id (str): The id of the account to remove access from the template.
            The account id prevails if both account_id and email_address are provided.

            email_address (str): The email address of the account to remove access from.

        Returns:
            An Template object

        '''
        return self._add_remove_user_template(self.TEMPLATE_REMOVE_USER_URL, template_id, account_id, email_address)

    def delete_template(self, template_id):
        ''' Deletes the specified template

        Args:

            template_id (str): The id of the template to delete

        Returns:
            A status code

        '''

        url = self.TEMPLATE_DELETE_URL

        request = self._get_request()
        response = request.post(url + template_id, get_json=False)

        return response

    def get_template_files(self, template_id, path_or_file=None, file_type=None,
            filename=None, response_type=None):
        ''' Downloads a copy of a template's original files

        Args:

            template_id (str): id of the template to download

            path_or_file (str or file): A writable File-like object or a full path to save the PDF file to.

            filename (str): [DEPRECATED] Filename to save the PDF file to. This should be a full path.

            file_type (str): Type of file to return. Either "pdf" for a single merged document or
            "zip" for a collection of individual documents. Defaults to "pdf" if not specified.

            response_type (str): File type of response to return. Either "url" to return a URL link to the file
            or "data_uri" to return the file as a base64 encoded string. Only applicable to the "pdf" file_type.

        Returns:
            Returns a PDF file, URL link to file, or base64 encoded file

        '''
        request = self._get_request()
        url = self.TEMPLATE_GET_FILES_URL + template_id
        if file_type:
            url += '?file_type=%s' % file_type
            return request.get_file(url, path_or_file or filename)

        if response_type == 'url':
            url += '?get_url=1'
        elif response_type == 'data_uri':
            url += '?get_data_uri=1'
        return request.get(url)

    def update_template_files(self, template_id, files=None, file_urls=None,
            subject=None, message=None, client_id=None, test_mode=False):
        ''' Overlays a new file with the overlay of an existing template.

        Args:

            template_id (str): The id of the template whose files to update

            files (list of str): The file(s) to use for the template.

            file_urls (list of str): URLs of the file for HelloSign to use for the template.
            Use either `files` or `file_urls`, but not both.

            subject (str, optional): The default template email subject

            message (str, optional): The default template email message

            test_mode (bool, optional): Whether this is a test, the signature request created
            from this Template will not be legally binding if set to 1. Defaults to 0.

            client_id (str): Client id of the app associated with the Template

        Returns:
            A Template object

        '''
        request = self._get_request()
        return request.post(self.TEMPLATE_UPDATE_FILES_URL + template_id, data={
            "files": files,
            "file_urls": file_urls,
            "subject": subject,
            "message": message,
            "test_mode": self._boolean(test_mode),
            "client_id": client_id
        })

    def create_embedded_template_draft(self, client_id, signer_roles, test_mode=False,
            files=None, file_urls=None, title=None, subject=None, message=None,
            cc_roles=None, merge_fields=None, skip_me_now=False, use_preexisting_fields=False,
            allow_reassign=False, metadata=None, allow_ccs=False, attachments=None):
        ''' Creates an embedded Template draft for further editing.

        Args:

            test_mode (bool, optional): Whether this is a test, the signature request
            created from this draft will not be legally binding if set to 1. Defaults to 0.

            client_id (str): Client id of the app you're using to create this draft.

            files (list of str): The file(s) to use for the template.

            file_urls (list of str): URLs of the file for HelloSign to use for the template.
            Use either `files` or `file_urls`, but not both.

            title (str, optional): The template title

            subject (str, optional): The default template email subject

            message (str, optional): The default template email message

            signer_roles (list of dict): A list of signer roles, each of which has the following attributes:

                name (str): The role name of the signer that will be displayed when the
                template is used to create a signature request.
                order (str, optional): The order in which this signer role is required to sign.

            cc_roles (list of str, optional): The CC roles that must be assigned when using the template to send a signature request

            merge_fields (list of dict, optional): The merge fields that can be placed on the template's
            document(s) by the user claiming the template draft. Each must have the following two parameters:

                name (str): The name of the merge field. Must be unique.
                type (str): Can only be "text" or "checkbox".

            skip_me_now (bool, optional): Disables the "Me (Now)" option for the document's preparer. Defaults to 0.

            use_preexisting_fields (bool, optional): Whether to use preexisting PDF fields

            metadata (dict, optional): Metadata to associate with the draft

            allow_reassign (bool, optional): Allows signers to reassign their signature
            requests to other signers if set to True. Defaults to False.

            allow_ccs (bool, optional): Specifies whether the user is allowed to
            provide email addresses to CC when creating a template. Defaults to False.

            attachments (list of dict):            A list of attachments, each with the following attributes:
                name (str):                        The name of the attachment
                instructions (str):                The instructions for uploading the attachment
                signer_index (int):                The index of the signer who needs to upload the attachments, see signers parameter for more details
                required (bool, optional):         Determines if the attachment must be uploaded

        Returns:
            A Template object specifying the id of the draft

        '''
        params = {
            'test_mode': test_mode,
            'client_id': client_id,
            'files': files,
            'file_urls': file_urls,
            'title': title,
            'subject': subject,
            'message': message,
            'signer_roles': signer_roles,
            'cc_roles': cc_roles,
            'merge_fields': merge_fields,
            'skip_me_now': skip_me_now,
            'use_preexisting_fields': use_preexisting_fields,
            'metadata': metadata,
            'allow_reassign': allow_reassign,
            'allow_ccs': allow_ccs,
            'attachments': attachments
        }

        return self._create_embedded_template_draft(**params)

    #  ----  TEAM METHODS  --------------------------------

    @api_resource(Team)
    def get_team_info(self):
        ''' Gets your Team and a list of its members

        Returns information about your team as well as a list of its members.
        If you do not belong to a team, a 404 error with an error_name of
        "not_found" will be returned.

        Returns:
            A Team object

        '''
        request = self._get_request()
        return request.get(self.TEAM_INFO_URL)

    @api_resource(Team)
    def create_team(self, name):
        ''' Creates a new Team

        Creates a new Team and makes you a member. You must not currently belong to a team to invoke.

        Args:

            name (str): The name of your team

        Returns:
            A Team object

        '''
        request = self._get_request()
        return request.post(self.TEAM_CREATE_URL, {"name": name})

    # RECOMMEND: The api event create a new team if you do not belong to any team
    @api_resource(Team)
    def update_team_name(self, name):
        ''' Updates a Team's name

        Args:

            name (str): The new name of your team

        Returns:
            A Team object

        '''
        request = self._get_request()
        return request.post(self.TEAM_UPDATE_URL, {"name": name})

    def destroy_team(self):
        ''' Delete your Team

        Deletes your Team. Can only be invoked when you have a team with only one member left (yourself).

        Returns:
            None

        '''
        request = self._get_request()
        request.post(url=self.TEAM_DESTROY_URL, get_json=False)

    def add_team_member(self, account_id=None, email_address=None):
        ''' Add or invite a user to your Team

        Args:

            account_id (str): The id of the account of the user to invite to your team.

            email_address (str): The email address of the account to invite to your team.
            The account id prevails if both account_id and email_address are provided.

        Returns:
            A Team object

        '''
        return self._add_remove_team_member(self.TEAM_ADD_MEMBER_URL, email_address, account_id)

    # RECOMMEND: Does not fail if user has been removed
    def remove_team_member(self, account_id=None, email_address=None):
        ''' Remove a user from your Team

        Args:

            account_id (str): The id of the account of the user to remove from your team.

            email_address (str): The email address of the account to remove from your team.
            The account id prevails if both account_id and email_address are provided.

        Returns:
            A Team object

        '''
        return self._add_remove_team_member(self.TEAM_REMOVE_MEMBER_URL, email_address, account_id)

    #  ----  EMBEDDED METHODS  ----------------------------

    @api_resource(Embedded)
    def get_embedded_object(self, signature_id):
        ''' Retrieves an embedded signing object

        Retrieves an embedded object containing a signature url that can be opened in an iFrame.

        Args:

            signature_id (str): The id of the signature to get a signature url for

        Returns:
            An Embedded object

        '''
        request = self._get_request()
        return request.get(self.EMBEDDED_OBJECT_GET_URL + signature_id)

    @api_resource(Embedded)
    def get_template_edit_url(self, template_id, test_mode=False, cc_roles=None,
            merge_fields=None, skip_signer_roles=False, skip_subject_message=False):
        ''' Retrieves a embedded template for editing

        Retrieves an embedded object containing a template edit url that can be opened in an iFrame.

        Args:

            template_id (str): The id of the template to get an edit url for

            test_mode (bool, optional): Whether this is a test, the signature requests created
            from this template will not be legally binding if set to True. Defaults to False.

            cc_roles (list of str, optional): The CC roles that must be assigned when using
            the template to send a signature request

            merge_fields (list of dict, optional): The merge fields that can be placed on the template's document(s)
            by the user claiming the template draft. Each must have the following two parameters:

                name (str): The name of the merge field. Must be unique.
                type (str): Can only be "text" or "checkbox".

            skip_me_now (bool, optional): Disables the "Me (Now)" option for the document's preparer.
            Defaults to False.

            skip_subject_message (bool, optional): Disables the option to edit the template's default
            subject and message. Defaults to False.

        Returns:
            An Embedded object

        '''

        # Prep CCs
        ccs_payload = HSFormat.format_param_list(cc_roles, 'cc_roles')
        # Prep Merge Fields
        if merge_fields:
            merge_fields_payload = {
                'merge_fields': json.dumps(merge_fields)
            }

        payload = {
            "test_mode": self._boolean(test_mode),
            "skip_signer_roles": self._boolean(skip_signer_roles),
            "skip_subject_message": self._boolean(skip_subject_message)
        }

        # remove attributes with none value
        payload = HSFormat.strip_none_values(payload)

        url = self.EMBEDDED_TEMPLATE_EDIT_URL + template_id

        data = {}
        data.update(payload)
        data.update(ccs_payload)
        data.update(merge_fields_payload)

        request = self._get_request()
        response = request.post(url, data=data)
        return response

    #  ----  API APP METHODS  --------------------------------

    @api_resource(ApiApp)
    def get_api_app_info(self, client_id):
        ''' Gets an API App by its Client ID

        Returns information about the specified API App

        Returns:
            An ApiApp object

        '''
        request = self._get_request()
        return request.get(self.API_APP_INFO_URL + client_id)

    @api_resource_list(ApiApp)
    def get_api_app_list(self, page=1, page_size=None):
        ''' Lists your API Apps

        Args:

            page (int, optional): Page number of the API App List to return. Defaults to 1.

            page_size (int, optional): Number of objects to be returned per page, must be between 1 and 100, default is 20.

        Returns:
            A ResourceList object

        '''
        request = self._get_request()
        parameters = {
            'page': page,
            'page_size': page_size
        }
        return request.get(self.API_APP_LIST_URL, parameters=parameters)

    @api_resource(ApiApp)
    def create_api_app(self, name, domain, callback_url=None, custom_logo_file=None,
            oauth_callback_url=None, oauth_scopes=None, white_labeling_options=None,
            option_insert_everywhere=False):
        ''' Creates a new API App

        Creates a new API App with the specified settings.

        Args:

            name (str): The name of the API App

            domain (str): The domain name associated with the API App

            callback_url (str, optional): The URL that HelloSign events will be POSTed to

            custom_logo_file (str, optional): The image file to use as a custom logo

            oauth_callback_url (str, optional): The URL that HelloSign OAuth events will be POSTed to

            oauth_scopes (list of str, optional): List of the API App's OAuth scopes

            white_labeling_options (dict, optional): Customization options for the API App's signer page

            option_insert_everywhere (bool, optional): Denotes if signers can "Insert Everywhere" when
            signing a document

        Returns:
            An ApiApp object

        '''

        # Prep custom logo
        custom_logo_payload = HSFormat.format_logo_params(custom_logo_file)

        payload = {
            "name": name,
            "domain": domain,
            "callback_url": callback_url,
            "oauth[callback_url]": oauth_callback_url,
            "oauth[scopes]": oauth_scopes,
            "white_labeling_options": json.dumps(white_labeling_options),
            "options[can_insert_everywhere]": self._boolean(option_insert_everywhere)
        }

        # remove attributes with none value
        payload = HSFormat.strip_none_values(payload)

        request = self._get_request()
        return request.post(self.API_APP_CREATE_URL, data=payload, files=custom_logo_payload)

    @api_resource(ApiApp)
    def update_api_app(self, client_id, name=None, domain=None, callback_url=None,
            custom_logo_file=None, oauth_callback_url=None, oauth_scopes=None,
            white_labeling_options=None, option_insert_everywhere=False):
        ''' Updates the specified API App

        Updates an API App with the specified settings.

        Args:

            name (str): The name of the API App

            domain (str): The domain name associated with the API App

            callback_url (str, optional): The URL that HelloSign events will be POSTed to

            custom_logo_file (str, optional): The image file to use as a custom logo

            oauth_callback_url (str, optional): The URL that HelloSign OAuth events will be POSTed to

            oauth_scopes (list of str, optional): List of the API App's OAuth scopes

            white_labeling_options (dict, optional): Customization options for the API App's signer page

            option_insert_everywhere (bool, optional): Denotes if signers can "Insert Everywhere" when
            signing a document

        Returns:
            An ApiApp object

        '''

        # Prep custom logo
        custom_logo_payload = HSFormat.format_logo_params(custom_logo_file)

        payload = {
            "name": name,
            "domain": domain,
            "callback_url": callback_url,
            "oauth[callback_url]": oauth_callback_url,
            "oauth[scopes]": oauth_scopes,
            "white_labeling_options": json.dumps(white_labeling_options),
            "options[can_insert_everywhere]": self._boolean(option_insert_everywhere)
        }

        # remove attributes with none value
        payload = HSFormat.strip_none_values(payload)

        request = self._get_request()
        url = self.API_APP_UPDATE_URL + client_id

        return request.post(url, data=payload, files=custom_logo_payload)

    def delete_api_app(self, client_id):
        ''' Deletes the specified API App

        Deletes an API App. Can only be involved for API Apps you own.

        Returns:
            None

        '''
        request = self._get_request()
        request.delete(url=self.API_APP_DELETE_URL + client_id)

    #  ----  UNCLAIMED DRAFT METHODS  ---------------------

    def create_unclaimed_draft(self, test_mode=False, files=None, file_urls=None,
            draft_type=None, subject=None, message=None, signers=None, custom_fields=None,
            cc_email_addresses=None, signing_redirect_url=None, form_fields_per_document=None,
            metadata=None, use_preexisting_fields=False, use_text_tags=False,
            hide_text_tags=False, allow_decline=False, signing_options=None, attachments=None):
        ''' Creates a new Draft that can be claimed using the claim URL

        Creates a new Draft that can be claimed using the claim URL. The first
        authenticated user to access the URL will claim the Draft and will be
        shown either the "Sign and send" or the "Request signature" page with
        the Draft loaded. Subsequent access to the claim URL will result in a
        404. If the type is "send_document" then only the file parameter is
        required. If the type is "request_signature", then the identities of the
        signers and optionally the location of signing elements on the page are
        also required.

        Args:

            test_mode (bool, optional): Whether this is a test, the signature request created from this draft will not be legally binding if set to True. Defaults to False.

            files (list of str): The uploaded file(s) to send for signature

            file_urls (list of str): URLs of the file for HelloSign to download to send for signature. Use either `files` or `file_urls`

            draft_type (str): The type of unclaimed draft to create. Use "send_document" to create a claimable file, and "request_signature"
            for a claimable signature request. If the type is "request_signature" then signers name and email_address are not optional.

            subject (str, optional): The subject in the email that will be sent to the signers

            message (str, optional): The custom message in the email that will be sent to the signers

            signers (list of dict): A list of signers, which each has the following attributes:

                name (str): The name of the signer
                email_address (str): Email address of the signer
                order (str, optional): The order the signer is required to sign in

            custom_fields (list of dict, optional): A list of custom fields. Required when a CustomField exists in the Template.
            An item of the list should look like this: `{'name: value'}`

            cc_email_addresses (list of str, optional): A list of email addresses that should be CC'd

            signing_redirect_url (str, optional): The URL you want the signer redirected to after they successfully sign.

            form_fields_per_document (str or list of dict, optional): The fields that should appear on the document, expressed as a serialized JSON
            data structure which is a list of lists of the form fields. Please refer to the API reference of HelloSign for more details (https://www.hellosign.com/api/reference#SignatureRequest)

            metadata (dict, optional): Metadata to associate with the draft

            use_preexisting_fields (bool): Whether to use preexisting PDF fields

            use_text_tags (bool, optional): Use text tags in the provided file(s) to create form fields

            hide_text_tags (bool, optional): Hide text tag areas

            allow_decline (bool, optional): Allows signers to decline to sign a document if set to 1. Defaults to 0.

            signing_options (dict, optional): Allows the requester to specify the types allowed for creating a signature.
            Defaults to account settings.

            attachments (list of dict):            A list of attachments, each with the following attributes:
                name (str):                        The name of the attachment
                instructions (str):                The instructions for uploading the attachment
                signer_index (int):                The index of the signer who needs to upload the attachments, see signers parameter for more details
                required (bool, optional):         Determines if the attachment must be uploaded

        Returns:
            An UnclaimedDraft object

        '''

        self._check_required_fields({
            'draft_type': draft_type
        }, [{
            "files": files,
            "file_urls": file_urls
            }]
        )

        params = {
            'test_mode': test_mode,
            'files': files,
            'file_urls': file_urls,
            'draft_type': draft_type,
            'subject': subject,
            'message': message,
            'signing_redirect_url': signing_redirect_url,
            'signers': signers,
            'custom_fields': custom_fields,
            'cc_email_addresses': cc_email_addresses,
            'form_fields_per_document': form_fields_per_document,
            'metadata': metadata,
            'use_preexisting_fields': use_preexisting_fields,
            'use_text_tags': use_text_tags,
            'hide_text_tags': hide_text_tags,
            'allow_decline': allow_decline,
            'signing_options': signing_options,
            'attachments': attachments
        }

        return self._create_unclaimed_draft(**params)

    def create_embedded_unclaimed_draft(self, test_mode=False, client_id=None,
            is_for_embedded_signing=False, requester_email_address=None, files=None,
            file_urls=None, draft_type=None, subject=None, message=None, signers=None,
            custom_fields=None, cc_email_addresses=None, signing_redirect_url=None,
            requesting_redirect_url=None, form_fields_per_document=None, metadata=None,
            use_preexisting_fields=False, use_text_tags=False, hide_text_tags=False,
            skip_me_now=False, allow_decline=False, allow_reassign=False,
            signing_options=None, allow_ccs=False, attachments=None):
        ''' Creates a new Draft to be used for embedded requesting

        Args:

            test_mode (bool, optional): Whether this is a test, the signature request created from this draft will not be legally binding if set to True. Defaults to False.

            client_id (str): Client id of the app used to create the embedded draft.

            is_for_embedded_signing (bool, optional): Whether this is also for embedded signing. Defaults to False.

            requester_email_address (str): Email address of the requester.

            files (list of str): The uploaded file(s) to send for signature.

            file_urls (list of str): URLs of the file for HelloSign to download to send for signature. Use either `files` or `file_urls`

            draft_type (str): The type of unclaimed draft to create. Use "send_document" to create a claimable file, and "request_signature" for a claimable signature request. If the type is "request_signature" then signers name and email_address are not optional.

            subject (str, optional): The subject in the email that will be sent to the signers

            message (str, optional): The custom message in the email that will be sent to the signers

            signers (list of dict): A list of signers, which each has the following attributes:

                name (str): The name of the signer
                email_address (str): Email address of the signer
                order (str, optional): The order the signer is required to sign in

            custom_fields (list of dict, optional): A list of custom fields. Required when a CustomField exists using text tags for form_fields_per_document. An item of the list should look like this: `{'name: value'}`

            cc_email_addresses (list of str, optional): A list of email addresses that should be CC'd

            signing_redirect_url (str, optional): The URL you want the signer redirected to after they successfully sign.

            requesting_redirect_url (str, optional): The URL you want the signer to be redirected to after the request has been sent.

            form_fields_per_document (str or list of dict, optional): The fields that should appear on the document, expressed as a serialized JSON data structure which is a list of lists of the form fields. Please refer to the API reference of HelloSign for more details (https://www.hellosign.com/api/reference#SignatureRequest)

            metadata (dict, optional): Metadata to associate with the draft

            use_preexisting_fields (bool): Whether to use preexisting PDF fields

            use_text_tags (bool, optional): Use text tags in the provided file(s) to create form fields

            hide_text_tags (bool, optional): Hide text tag areas

            skip_me_now (bool, optional): Disables the "Me (Now)" option for the document's preparer. Defaults to 0.

            signing_options (dict, optional): Allows the requester to specify the types allowed for creating a signature. Defaults to account settings.

            allow_decline (bool, optional): Allows signers to decline to sign a document if set to 1. Defaults to 0.

            allow_ccs (bool, optional): Specifies whether the user is allowed to provide email addresses to CC when sending the request. Defaults to False.

            attachments (list of dict):            A list of attachments, each with the following attributes:
                name (str):                        The name of the attachment
                instructions (str):                The instructions for uploading the attachment
                signer_index (int):                The index of the signer who needs to upload the attachments, see signers parameter for more details
                required (bool, optional):         Determines if the attachment must be uploaded

        Returns:
            An UnclaimedDraft object

        '''

        self._check_required_fields({
            'client_id': client_id,
            'requester_email_address': requester_email_address,
            'draft_type': draft_type
        }, [{
            "files": files,
            "file_urls": file_urls
            }]
        )

        params = {
            'test_mode': test_mode,
            'client_id': client_id,
            'requester_email_address': requester_email_address,
            'is_for_embedded_signing': is_for_embedded_signing,
            'files': files,
            'file_urls': file_urls,
            'draft_type': draft_type,
            'subject': subject,
            'message': message,
            'signing_redirect_url': signing_redirect_url,
            'requesting_redirect_url': requesting_redirect_url,
            'signers': signers,
            'custom_fields': custom_fields,
            'cc_email_addresses': cc_email_addresses,
            'form_fields_per_document': form_fields_per_document,
            'metadata': metadata,
            'use_preexisting_fields': use_preexisting_fields,
            'use_text_tags': use_text_tags,
            'hide_text_tags': hide_text_tags,
            'skip_me_now': skip_me_now,
            'signing_options': signing_options,
            'allow_reassign': allow_reassign,
            'allow_decline': allow_decline,
            'allow_ccs': allow_ccs,
            'attachments': attachments
        }

        return self._create_unclaimed_draft(**params)

    def create_embedded_unclaimed_draft_with_template(self, test_mode=False,
            client_id=None, is_for_embedded_signing=False, template_id=None,
            template_ids=None, requester_email_address=None, title=None,
            subject=None, message=None, signers=None, ccs=None, signing_redirect_url=None,
            requesting_redirect_url=None, metadata=None, custom_fields=None,
            files=None, file_urls=None, skip_me_now=False, allow_decline=False,
            allow_reassign=False, signing_options=None):
        ''' Creates a new Draft to be used for embedded requesting

            Args:

                test_mode (bool, optional): Whether this is a test, the signature request created from this draft will not be legally binding if set to True. Defaults to False.

                client_id (str): Client id of the app you're using to create this draft. Visit our embedded page to learn more about this parameter.

                template_id (str): The id of the Template to use when creating the Unclaimed Draft. Mutually exclusive with template_ids.

                template_ids (list of str): The ids of the Templates to use when creating the Unclaimed Draft. Mutually exclusive with template_id.

                requester_email_address (str): The email address of the user that should be designated as the requester of this draft, if the draft type is "request_signature."

                title (str, optional): The title you want to assign to the Unclaimed Draft

                subject (str, optional): The subject in the email that will be sent to the signers

                message (str, optional): The custom message in the email that will be sent to the signers

                signers (list of dict): A list of signers, which each has the following attributes:

                    name (str): The name of the signer
                    email_address (str): Email address of the signer

                ccs (list of str, optional): A list of email addresses that should be CC'd

                signing_redirect_url (str, optional): The URL you want the signer redirected to after they successfully sign.

                requesting_redirect_url (str, optional): The URL you want the signer to be redirected to after the request has been sent.

                is_for_embedded_signing (bool, optional): The request created from this draft will also be signable in embedded mode if set to True. The default is False.

                metadata (dict, optional): Metadata to associate with the draft. Each request can include up to 10 metadata keys, with key names up to 40 characters long and values up to 500 characters long.

                custom_fields (list of dict, optional): A list of custom fields. Required when a CustomField exists in the Template. An item of the list should look like this: `{'name: value'}`

                files (list of str): The uploaded file(s) to append to the Signature Request.

                file_urls (list of str): URLs of the file for HelloSign to download to append to the Signature Request. Use either `files` or `file_urls`

                skip_me_now (bool, optional): Disables the "Me (Now)" option for the document's preparer. Defaults to 0.

                allow_decline (bool, optional): Allows signers to decline to sign a document if set to 1. Defaults to 0.

                allow_reassign (bool, optional): Allows signers to reassign their signature requests to other signers if set to True. Defaults to False.

                signing_options (dict, optional): Allows the requester to specify the types allowed for creating a signature. Defaults to account settings.

            Returns:
                An UnclaimedDraft object

        '''

        self._check_required_fields({
            "client_id": client_id,
            "requester_email_address": requester_email_address
        }, [{
            "template_id": template_id,
            "template_ids": template_ids
            }]
        )

        params = {
            'test_mode': test_mode,
            'client_id': client_id,
            'is_for_embedded_signing': is_for_embedded_signing,
            'template_id': template_id,
            'template_ids': template_ids,
            'title': title,
            'subject': subject,
            'message': message,
            'requester_email_address': requester_email_address,
            'signing_redirect_url': signing_redirect_url,
            'requesting_redirect_url': requesting_redirect_url,
            'signers': signers,
            'ccs': ccs,
            'metadata': metadata,
            'custom_fields': custom_fields,
            'files': files,
            'file_urls': file_urls,
            'skip_me_now': skip_me_now,
            'allow_decline': allow_decline,
            'allow_reassign': allow_reassign,
            'signing_options': signing_options
        }

        return self._create_embedded_unclaimed_draft_with_template(**params)

    @api_resource(UnclaimedDraft)
    def unclaimed_draft_edit_and_resend(self, signature_request_id, client_id,
            test_mode=False, requesting_redirect_url=None, signing_redirect_url=None,
            is_for_embedded_signing=False, requester_email_address=None):
        ''' Updates a new signature request from an embedded request that can be edited prior to being sent.

        Args:

            signature_request_id (str): The id of the SignatureRequest to edit and resend

            client_id (str): Client id of the app you're using to create this draft.

            test_mode (bool, optional): Whether this is a test, the signature request created from this
            draft will not be legally binding if set to True. Defaults to False.

            requesting_redirect_url (str, optional): The URL you want the signer to be redirected to after the request has been sent.

            signing_redirect_url (str, optional): The URL you want the signer redirected to after they successfully sign.

            is_for_embedded_signing (bool, optional): The request created from this draft will also be signable in
            embedded mode if set to True. The default is False.

            requester_email_address (str, optional): The email address of the user that should be designated as the
            requester of this draft, if the draft type is "request_signature."

        Returns:
            A UnclaimedDraft object

        '''

        self._check_required_fields({
            "client_id": client_id
            }
        )

        data = {
            'client_id': client_id,
            'test_mode': self._boolean(test_mode),
            'requesting_redirect_url': requesting_redirect_url,
            'signing_redirect_url': signing_redirect_url,
            'is_for_embedded_signing': self._boolean(is_for_embedded_signing),
            'requester_email_address': requester_email_address
        }

        data = HSFormat.strip_none_values(data)

        request = self._get_request()
        return request.post(self.UNCLAIMED_DRAFT_EDIT_AND_RESEND_URL + signature_request_id, data=data)

    #  ----  OAUTH METHODS  -------------------------------

    def get_oauth_data(self, code, client_id, client_secret, state):
        ''' Get Oauth data from HelloSign

        Args:

            code (str): Code returned by HelloSign for our callback url

            client_id (str): Client id of the associated app

            client_secret (str): Secret token of the associated app

        Returns:
            A HSAccessTokenAuth object

        '''
        request = self._get_request()
        response = request.post(self.OAUTH_TOKEN_URL, {
            "state": state,
            "code": code,
            "grant_type": "authorization_code",
            "client_id": client_id,
            "client_secret": client_secret
        })
        return HSAccessTokenAuth.from_response(response)

    def refresh_access_token(self, refresh_token):
        ''' Refreshes the current access token.

            Gets a new access token, updates client auth and returns it.

        Args:

            refresh_token (str): Refresh token to use

        Returns:
            The new access token
        '''
        request = self._get_request()
        response = request.post(self.OAUTH_TOKEN_URL, {
            "grant_type": "refresh_token",
            "refresh_token": refresh_token
        })
        self.auth = HSAccessTokenAuth.from_response(response)
        return self.auth.access_token

    #  ----  HELPERS  -------------------------------------

    def get_last_warnings(self):
        ''' Return the warnings associated with the last request '''
        if self.request:
            return self.request.get_warnings()

    def _boolean(self, v):
        ''' Convert a value to a boolean '''
        return '1' if (v in (True, 'true', 'True', '1', 1)) else '0'

    def _get_request(self, auth=None):
        ''' Return an http request object

            auth: Auth data to use

            Returns:
                A HSRequest object
        '''
        self.request = HSRequest(auth or self.auth, self.env)
        self.request.response_callback = self.response_callback
        return self.request

    def _authenticate(self, email_address=None, password=None, api_key=None,
            access_token=None, access_token_type=None):
        ''' Create authentication object to send requests

        Args:

            email_address (str): Email address of the account to make the requests

            password (str): Password of the account used with email address

            api_key (str): API Key. You can find your API key in https://app.hellosign.com/home/myAccount/current_tab/integrations#api

            access_token (str): OAuth access token

            access_token_type (str): Type of OAuth access token

        Raises:
            NoAuthMethod: If no authentication information found

        Returns:
            A HTTPBasicAuth or HSAccessTokenAuth object

        '''

        if access_token_type and access_token:
            return HSAccessTokenAuth(access_token, access_token_type)
        elif api_key:
            return HTTPBasicAuth(api_key, '')
        elif email_address and password:
            return HTTPBasicAuth(email_address, password)
        else:
            raise NoAuthMethod("No authentication information found!")

    def _check_required_fields(self, fields=None, either_fields=None):
        ''' Check the values of the fields

        If no value found in `fields`, an exception will be raised.
        `either_fields` are the fields that one of them must have a value

        Raises:
            HSException: If no value found in at least one item of`fields`, or
                no value found in one of the items of `either_fields`

        Returns:
            None

        '''

        for (key, value) in fields.items():
            # If value is a dict, one of the fields in the dict is required ->
            # exception if all are None
            if not value:
                raise HSException("Field '%s' is required." % key)
        if either_fields is not None:
            for field in either_fields:
                if not any(field.values()):
                    raise HSException("One of the following fields is required: %s" % ", ".join(field.keys()))

    @api_resource(SignatureRequest)
    def _send_signature_request(self, test_mode=False, client_id=None, files=None,
            file_urls=None, title=None, subject=None, message=None,
            signing_redirect_url=None, signers=None, custom_fields=None,
            cc_email_addresses=None, form_fields_per_document=None, use_text_tags=False,
            hide_text_tags=False, metadata=None, allow_decline=False, allow_reassign=False,
            signing_options=None, is_for_embedded_signing=False, attachments=None):
        ''' To share the same logic between send_signature_request &
            send_signature_request_embedded functions

        Args:

            test_mode (bool, optional): Whether this is a test, the signature request will not be legally binding if set to True. Defaults to False.

            client_id (str): Client id of the app you're using to create this embedded signature request. Visit the embedded page to learn more about this parameter (https://www.hellosign.com/api/embeddedSigningWalkthrough)

            files (list of str): The uploaded file(s) to send for signature

            file_urls (list of str): URLs of the file for HelloSign to download to send for signature. Use either `files` or `file_urls`

            title (str, optional): The title you want to assign to the SignatureRequest

            subject (str, optional): The subject in the email that will be sent to the signers

            message (str, optional): The custom message in the email that will be sent to the signers

            signing_redirect_url (str, optional): The URL you want the signer redirected to after they successfully sign

            signers (list of dict): A list of signers, which each has the following attributes:

                name (str): The name of the signer
                email_address (str): Email address of the signer
                order (str, optional): The order the signer is required to sign in
                pin (str, optional): The 4- to 12-character access code that will secure this signer's signature page

            custom_fields (list of dict, optional): A list of custom fields. Required when a CustomField exists in the Template
            
            cc_email_addresses (list, optional): A list of email addresses that should be CCed

            form_fields_per_document (str or list of dict, optional): The fields that should appear on the document, expressed as a serialized JSON data structure which is a list of lists of the form fields. Please refer to the API reference of HelloSign for more details (https://www.hellosign.com/api/reference#SignatureRequest)

            use_text_tags (bool, optional): Use text tags in the provided file(s) to create form fields

            hide_text_tags (bool, optional): Hide text tag areas

            metadata (dict, optional): Metadata to associate with the signature request

            allow_decline (bool, optional);         Allows signers to decline to sign a document if set to 1. Defaults to 0.

            allow_reassign (bool, optional): Allows signers to reassign their signature requests to other signers if set to True. Defaults to False.

            signing_options (dict, optional): Allows the requester to specify the types allowed for creating a signature. Defaults to account settings.

            is_for_embedded_signing (bool): send_signature_request and send_signature_request_embedded share the same sending logic. To differenciate the two calls embedded requests are now flagged.

            attachments (list of dict):            A list of attachments, each with the following attributes:
                name (str):                        The name of attachment
                instructions (str):                The instructions for uploading the attachment
                signer_index (int):                The signer's index whose needs to upload the attachments, see signers parameter for more details
                required (bool, optional):         Determines if the attachment must be uploaded


        Returns:
            A SignatureRequest object

        '''

        # Files
        files_payload = HSFormat.format_file_params(files)

        # File URLs
        file_urls_payload = HSFormat.format_file_url_params(file_urls)

        # Signers
        signers_payload = HSFormat.format_dict_list(signers, 'signers')

        # Custom fields
        custom_fields_payload = HSFormat.format_custom_fields(custom_fields)

        # Form fields per document
        if isinstance(form_fields_per_document, str):
            form_fields_payload = form_fields_per_document
        else:
            form_fields_payload = HSFormat.format_json_data(form_fields_per_document)

        # CCs
        cc_email_addresses_payload = HSFormat.format_param_list(cc_email_addresses, 'cc_email_addresses')

        # Metadata
        metadata_payload = HSFormat.format_single_dict(metadata, 'metadata')

        # Signing options
        signing_options_payload = HSFormat.format_signing_options(signing_options, 'signing_options')

        # Attachments
        attachments_payload = HSFormat.format_dict_list(attachments, 'attachments')

        payload = {
            "test_mode": self._boolean(test_mode),
            "client_id": client_id,
            "title": title,
            "subject": subject,
            "message": message,
            "signing_redirect_url": signing_redirect_url,
            "form_fields_per_document": form_fields_payload,
            "use_text_tags": self._boolean(use_text_tags),
            "hide_text_tags": self._boolean(hide_text_tags),
            "allow_decline": self._boolean(allow_decline),
            "allow_reassign": self._boolean(allow_reassign),
            "signing_options": HSFormat.format_json_data(signing_options)
        }

        # remove attributes with none value
        payload = HSFormat.strip_none_values(payload)

        url = self.SIGNATURE_REQUEST_CREATE_URL
        if is_for_embedded_signing:
            url = self.SIGNATURE_REQUEST_CREATE_EMBEDDED_URL

        data = {}
        data.update(payload)
        data.update(signers_payload)
        data.update(custom_fields_payload)
        data.update(cc_email_addresses_payload)
        data.update(file_urls_payload)
        data.update(metadata_payload)
        data.update(signing_options_payload)
        data.update(attachments_payload)

        request = self._get_request()
        response = request.post(url, data=data, files=files_payload)
        return response

    @api_resource(SignatureRequest)
    def _send_signature_request_with_template(self, test_mode=False, client_id=None,
            template_id=None, template_ids=None, title=None, subject=None, message=None,
            signing_redirect_url=None, signers=None, ccs=None, custom_fields=None,
            metadata=None, allow_decline=False, files=None, file_urls=None, signing_options=None):
        ''' To share the same logic between send_signature_request_with_template
            and send_signature_request_embedded_with_template

        Args:

            test_mode (bool, optional): Whether this is a test, the signature request will not be legally binding if set to True. Defaults to False.

            client_id (str): Client id of the app you're using to create this embedded signature request. Visit the embedded page to learn more about this parameter (https://app.hellosign.com/api/embeddedSigningWalkthrough)

            template_id (str): The id of the Template to use when creating the SignatureRequest. Mutually exclusive with template_ids.

            template_ids (list): The ids of the Templates to use when creating the SignatureRequest. Mutually exclusive with template_id.

            title (str, optional): The title you want to assign to the SignatureRequest

            subject (str, optional): The subject in the email that will be sent to the signers

            message (str, optional): The custom message in the email that will be sent to the signers

            signing_redirect_url (str, optional): The URL you want the signer redirected to after they successfully sign.

            signers (list of dict): A list of signers, which each has the following attributes:

                role_name (str): Role the signer is assigned to
                name (str): The name of the signer
                email_address (str): Email address of the signer
                pin (str, optional): The 4- to 12-character access code that will secure this signer's signature page

            ccs (list of dict, optional): The email address of the CC filling the role of RoleName. Required when a CC role exists for the Template. Each dict has the following attributes:

                role_name (str): CC role name
                email_address (str): CC email address

            custom_fields (list of dict, optional): A list of custom fields. Required when a CustomField exists in the Template. An item of the list should look like this: `{'name: value'}`

            metadata (dict, optional): Metadata to associate with the signature request

            allow_decline (bool, optional): Allows signers to decline to sign a document if set to 1. Defaults to 0.

            files (list of str): The uploaded file(s) to append to the Signature Request.

            file_urls (list of str): URLs of the file for HelloSign to download to append to the Signature Request. Use either `files` or `file_urls`

            signing_options (dict, optional): Allows the requester to specify the types allowed for creating a signature. Defaults to account settings.

        Returns:
            A SignatureRequest object

        '''

        # Signers
        signers_payload = HSFormat.format_dict_list(signers, 'signers', 'role_name')

        # CCs
        ccs_payload = HSFormat.format_dict_list(ccs, 'ccs', 'role_name')

        # Custom fields
        custom_fields_payload = HSFormat.format_custom_fields(custom_fields)

        # Metadata
        metadata_payload = HSFormat.format_single_dict(metadata, 'metadata')

        # Signing options
        signing_options_payload = HSFormat.format_signing_options(signing_options, 'signing_options')

        # Template ids
        template_ids_payload = {}
        if template_ids:
            for i in range(len(template_ids)):
                template_ids_payload["template_ids[%s]" % i] = template_ids[i]

        # Files
        files_payload = HSFormat.format_file_params(files)

        # File URLs
        file_urls_payload = HSFormat.format_file_url_params(file_urls)

        payload = {
            "test_mode": self._boolean(test_mode),
            "client_id": client_id,
            "template_id": template_id,
            "title": title,
            "subject": subject,
            "message": message,
            "signing_redirect_url": signing_redirect_url,
            "allow_decline": self._boolean(allow_decline),
            "signing_options": HSFormat.format_json_data(signing_options)

        }

        # remove attributes with empty value
        payload = HSFormat.strip_none_values(payload)

        url = self.SIGNATURE_REQUEST_CREATE_WITH_TEMPLATE_URL
        if client_id:
            url = self.SIGNATURE_REQUEST_CREATE_EMBEDDED_WITH_TEMPLATE_URL

        data = payload.copy()
        data.update(signers_payload)
        data.update(ccs_payload)
        data.update(custom_fields_payload)
        data.update(metadata_payload)
        data.update(signing_options_payload)
        data.update(template_ids_payload)
        data.update(file_urls_payload)

        request = self._get_request()
        response = request.post(url, data=data, files=files_payload)

        return response

    @api_resource(UnclaimedDraft)
    def _create_unclaimed_draft(self, test_mode=False, client_id=None,
            is_for_embedded_signing=False, requester_email_address=None, files=None,
            file_urls=None, draft_type=None, subject=None, message=None, signers=None,
            custom_fields=None, cc_email_addresses=None, signing_redirect_url=None,
            requesting_redirect_url=None, form_fields_per_document=None, metadata=None,
            use_preexisting_fields=False, use_text_tags=False, hide_text_tags=False,
            skip_me_now=False, allow_reassign=False, allow_decline=False,
            signing_options=None, allow_ccs=False, attachments=None):
        ''' Creates a new Draft that can be claimed using the claim URL

        Args:

            test_mode (bool, optional): Whether this is a test, the signature request created from this draft will not be legally binding if set to True. Defaults to False.

            client_id (str): Client id of the app used to create the embedded draft.

            is_for_embedded_signing (bool): Whether this is for embedded signing on top of being for embedded requesting.

            requester_email_address (str): Email address of the requester when creating a draft for embedded requesting.

            files (list of str): The uploaded file(s) to send for signature.

            file_urls (list of str): URLs of the file for HelloSign to download to send for signature. Use either `files` or `file_urls`

            draft_type (str): The type of unclaimed draft to create. Use "send_document" to create a claimable file, and "request_signature" for a claimable signature request. If the type is "request_signature" then signers name and email_address are not optional.

            subject (str, optional): The subject in the email that will be sent to the signers

            message (str, optional): The custom message in the email that will be sent to the signers

            signers (list of dict): A list of signers, which each has the following attributes:

                name (str): The name of the signer
                email_address (str): Email address of the signer
                order (str, optional): The order the signer is required to sign in

            custom_fields (list of dict, optional): A list of custom fields. Required when a CustomField exists using text tags or form_fields_per_document. An item of the list should look like this: `{'name: value'}`

            cc_email_addresses (list of str, optional): A list of email addresses that should be CC'd

            signing_redirect_url (str, optional): The URL you want the signer redirected to after they successfully sign.

            requesting_redirect_url (str, optional): The URL you want the signer to be redirected to after the request has been sent.

            form_fields_per_document (str or list of dict, optional): The fields that should appear on the document, expressed as a serialized JSON data structure which is a list of lists of the form fields. Please refer to the API reference of HelloSign for more details (https://www.hellosign.com/api/reference#SignatureRequest).

            metadata (dict, optional): Metadata to associate with the draft

            use_preexisting_fields (bool): Whether to use preexisting PDF fields

            use_text_tags (bool, optional): Use text tags in the provided file(s) to create form fields

            hide_text_tags (bool, optional): Hide text tag areas

            skip_me_now (bool, optional): Disables the "Me (Now)" option for the document's preparer. Defaults to 0.

            allow_reassign (bool, optional): Allows signers to reassign their signature requests to other signers if set to True. Defaults to False.

            allow_decline (bool, optional): Allows signers to decline to sign a document if set to 1. Defaults to 0.

            signing_options (dict, optional): Allows the requester to specify the types allowed for creating a signature. Defaults to account settings.

            allow_ccs (bool, optional): Specifies whether the user is allowed to provide email addresses to CC when sending the request. Defaults to False.

            attachments (list of dict):            A list of attachments, each with the following attributes:
                name (str):                        The name of the attachment
                instructions (str):                The instructions for uploading the attachment
                signer_index (int):                The index of the signer who needs to upload the attachments, see signers parameter for more details
                required (bool, optional):         Determines if the attachment must be uploaded

        Returns:
            An UnclaimedDraft object

        '''

        # Files
        files_payload = HSFormat.format_file_params(files)

        # Files URLs
        file_urls_payload = HSFormat.format_file_url_params(file_urls)

        # Signers
        signers_payload = {}
        if signers:
            for (idx, signer) in enumerate(signers):
                if draft_type == UnclaimedDraft.UNCLAIMED_DRAFT_REQUEST_SIGNATURE_TYPE:
                    if "name" not in signer and "email_address" not in signer:
                        raise HSException("Signer's name and email are required")
            signers_payload = HSFormat.format_dict_list(signers, 'signers')

        # CCs
        cc_email_addresses_payload = HSFormat.format_param_list(cc_email_addresses, 'cc_email_addresses')

        # Custom fields
        custom_fields_payload = HSFormat.format_custom_fields(custom_fields)

        # Form fields per document
        if isinstance(form_fields_per_document, str):
            form_fields_payload = form_fields_per_document
        else:
            form_fields_payload = HSFormat.format_json_data(form_fields_per_document)

        # Metadata
        metadata_payload = HSFormat.format_single_dict(metadata, 'metadata')

        # Signing options
        signing_options_payload = HSFormat.format_signing_options(signing_options, 'signing_options')

        # Attachments
        attachments_payload = HSFormat.format_dict_list(attachments, 'attachments')

        payload = {
            "test_mode": self._boolean(test_mode),
            "type": draft_type,
            "subject": subject,
            "message": message,
            "signing_redirect_url": signing_redirect_url,
            "form_fields_per_document": form_fields_payload,
            "use_preexisting_fields": self._boolean(use_preexisting_fields),
            "use_text_tags": self._boolean(use_text_tags),
            "hide_text_tags": self._boolean(hide_text_tags),
            "skip_me_now": self._boolean(skip_me_now),
            "allow_reassign": self._boolean(allow_reassign),
            "allow_decline": self._boolean(allow_decline),
            "signing_options": HSFormat.format_json_data(signing_options),

            "allow_ccs": self._boolean(allow_ccs)
        }

        url = self.UNCLAIMED_DRAFT_CREATE_URL

        if client_id is not None:
            payload.update({
                'client_id': client_id,
                'is_for_embedded_signing': '1' if is_for_embedded_signing else '0',
                'requester_email_address': requester_email_address,
                'requesting_redirect_url': requesting_redirect_url
            })
            url = self.UNCLAIMED_DRAFT_CREATE_EMBEDDED_URL

        # remove attributes with none value
        payload = HSFormat.strip_none_values(payload)

        data = payload.copy()
        data.update(signers_payload)
        data.update(custom_fields_payload)
        data.update(cc_email_addresses_payload)
        data.update(file_urls_payload)
        data.update(metadata_payload)
        data.update(signing_options_payload)
        data.update(attachments_payload)

        request = self._get_request()
        response = request.post(url, data=data, files=files_payload)

        return response

    @api_resource(Template)
    def _add_remove_user_template(self, url, template_id, account_id=None, email_address=None):
        ''' Add or Remove user from a Template

        We use this function for two tasks because they have the same API call

        Args:

            template_id (str): The id of the template

            account_id (str): ID of the account to add/remove access to/from

            email_address (str): The email_address of the account to add/remove access to/from

        Raises:
            HSException: If no email address or account_id specified

        Returns:
            A Template object

        '''

        if not email_address and not account_id:
            raise HSException("No email address or account_id specified")

        data = {}
        if account_id is not None:
            data = {
                "account_id": account_id
            }
        else:
            data = {
                "email_address": email_address
            }

        request = self._get_request()
        response = request.post(url + template_id, data)

        return response

    @api_resource(Team)
    def _add_remove_team_member(self, url, email_address=None, account_id=None):
        ''' Add or Remove a team member

        We use this function for two different tasks because they have the same
        API call

        Args:

            email_address (str): Email address of the Account to add/remove

            account_id (str): ID of the Account to add/remove

        Returns:
            A Team object

        '''

        if not email_address and not account_id:
            raise HSException("No email address or account_id specified")

        data = {}
        if account_id is not None:
            data = {
                "account_id": account_id
            }
        else:
            data = {
                "email_address": email_address
            }

        request = self._get_request()
        response = request.post(url, data)

        return response

    @api_resource(Template)
    def _create_embedded_template_draft(self, client_id, signer_roles, test_mode=False,
            files=None, file_urls=None, title=None, subject=None, message=None,
            cc_roles=None, merge_fields=[], skip_me_now=False,
            use_preexisting_fields=False, metadata=None, allow_reassign=False, allow_ccs=False, attachments=None):
        ''' Helper method for creating embedded template drafts.
            See public function for params.
        '''

        url = self.TEMPLATE_CREATE_EMBEDDED_DRAFT_URL

        payload = {
            'test_mode': self._boolean(test_mode),
            'client_id': client_id,
            'title': title,
            'subject': subject,
            'message': message,
            'skip_me_now': self._boolean(skip_me_now),
            'use_preexisting_fields': self._boolean(use_preexisting_fields),
            'allow_reassign': self._boolean(allow_reassign),
            'allow_ccs':
            self._boolean(allow_ccs)
        }

        # Prep files
        files_payload = HSFormat.format_file_params(files)
        file_urls_payload = HSFormat.format_file_url_params(file_urls)

        # Prep Signer Roles
        signer_roles_payload = HSFormat.format_dict_list(signer_roles, 'signer_roles')
        # Prep CCs
        ccs_payload = HSFormat.format_param_list(cc_roles, 'cc_roles')
        # Prep Merge Fields
        merge_fields_payload = {
            'merge_fields': json.dumps(merge_fields)
        }
        # Prep Metadata
        metadata_payload = HSFormat.format_single_dict(metadata, 'metadata')

        # Attachments
        attachments_payload = HSFormat.format_dict_list(attachments, 'attachments')

        # Assemble data for sending
        data = {}
        data.update(payload)
        data.update(file_urls_payload)
        data.update(signer_roles_payload)
        data.update(ccs_payload)
        data.update(metadata_payload)
        data.update(attachments_payload)
        if (merge_fields is not None):
            data.update(merge_fields_payload)
        data = HSFormat.strip_none_values(data)

        request = self._get_request()

        response = request.post(url, data=data, files=files_payload)

        return response

    @api_resource(UnclaimedDraft)
    def _create_embedded_unclaimed_draft_with_template(self, test_mode=False,
            client_id=None, is_for_embedded_signing=False, template_id=None,
            template_ids=None, requester_email_address=None, title=None,
            subject=None, message=None, signers=None, ccs=None,
            signing_redirect_url=None, requesting_redirect_url=None, metadata=None,
            custom_fields=None, files=None, file_urls=None, skip_me_now=False,
            allow_decline=False, allow_reassign=False, signing_options=None):
        ''' Helper method for creating unclaimed drafts from templates
            See public function for params.
        '''

        #single params
        payload = {
            "test_mode": self._boolean(test_mode),
            "client_id": client_id,
            "is_for_embedded_signing": self._boolean(is_for_embedded_signing),
            "template_id": template_id,
            "requester_email_address": requester_email_address,
            "title": title,
            "subject": subject,
            "message": message,
            "signing_redirect_url": signing_redirect_url,
            "requesting_redirect_url": requesting_redirect_url,
            "skip_me_now": self._boolean(skip_me_now),
            "allow_decline": self._boolean(allow_decline),
            "allow_reassign": self._boolean(allow_reassign),
            "signing_options": HSFormat.format_json_data(signing_options)
        }

        #format multi params
        template_ids_payload = HSFormat.format_param_list(template_ids, 'template_ids')
        signers_payload = HSFormat.format_dict_list(signers, 'signers', 'role_name')
        ccs_payload = HSFormat.format_dict_list(ccs, 'ccs', 'role_name')
        metadata_payload = HSFormat.format_single_dict(metadata, 'metadata')
        signing_options_payload = HSFormat.format_signing_options(signing_options, 'signing_options')
        custom_fields_payload = HSFormat.format_custom_fields(custom_fields)

        # Files
        files_payload = HSFormat.format_file_params(files)

        # File URLs
        file_urls_payload = HSFormat.format_file_url_params(file_urls)

        #assemble payload
        data = {}
        data.update(payload)
        data.update(template_ids_payload)
        data.update(signers_payload)
        data.update(ccs_payload)
        data.update(metadata_payload)
        data.update(signing_options_payload)
        data.update(custom_fields_payload)
        data.update(file_urls_payload)
        data = HSFormat.strip_none_values(data)

        #send call
        url = self.UNCLAIMED_DRAFT_CREATE_EMBEDDED_WITH_TEMPLATE_URL
        request = self._get_request()
        response = request.post(url, data=data, files=files_payload)

        return response
