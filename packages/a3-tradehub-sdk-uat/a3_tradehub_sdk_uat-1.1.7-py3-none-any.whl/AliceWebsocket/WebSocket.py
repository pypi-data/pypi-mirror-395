import requests
import json
import hashlib
import enum
import logging
import pandas as pd
from datetime import time, datetime
from collections import namedtuple
import os
import websocket
import rel
# import time
import ssl

import threading
import time as time_module

logger = logging.getLogger(__name__)

Instrument = namedtuple('Instrument', ['exchange', 'token', 'symbol', 'name', 'expiry', 'lot_size'])


def encrypt_string(hashing):
    sha = hashlib.sha256(hashing.encode()).hexdigest()
    return sha


class Aliceblue:
    base_url = "https://ant.aliceblueonline.com/rest/AliceBlueAPIService/api/"
    # base_url = "https://iiflapi.codifi.in/"
    api_name = "Codifi API Connect - Python Lib"
    version = "1.0.31"
    base_url_c = "https://v2api.aliceblueonline.com/restpy/static/contract_master/%s.csv"


    ENC = None
    ws = None
    subscriptions = None
    __subscribe_callback = None
    __subscribers = None
    script_subscription_instrument = []
    ws_connection = False
    # response = requests.get(base_url);
    # Getscrip URI
    __ws_thread = None
    __stop_event = None
    market_depth = None

    _sub_urls = {
        # Authorization
        "encryption_key": "customer/getAPIEncpkey",
        "getsessiondata": "customer/getUserSID",

        # Websockey
        "base_url_socket": "wss://ws1.aliceblueonline.com/NorenWS/"

    }

    # Common Method
    def __init__(self,
                 user_id,
                 api_key,
                 base=None,
                 session_id=None,
                 disable_ssl=False):

        self.user_id = user_id.upper()
        self.api_key = api_key
        self.disable_ssl = disable_ssl
        self.session_id = session_id
        self.base = base or self.base_url
        self.__on_error = None
        self.__on_disconnect = None
        self.__on_open = None
        self.__exchange_codes = None

    def _get(self, sub_url, data=None):
        """Get method declaration"""
        url = self.base + self._sub_urls[sub_url]
        return self._request(url, "GET", data=data)

    def _post(self, sub_url, data=None):
        """Post method declaration"""
        url = self.base + self._sub_urls[sub_url]
        return self._request(url, "POST", data=data)

    def _dummypost(self, url, data=None):
        """Post method declaration"""
        return self._request(url, "POST", data=data)

    def _user_agent(self):
        return self.api_name + self.version

    """Authorization get to call all requests"""

    def _user_authorization(self):
        if self.session_id:
            return "Bearer " + self.user_id.upper() + " " + self.session_id
        else:
            return ""

    """Common request to call POST and GET method"""

    def _request(self, method, req_type, data=None):
        """
        Headers with authorization. For some requests authorization
        is not required. It will be send as empty String
        """
        _headers = {
            "X-SAS-Version": "2.0",
            "User-Agent": self._user_agent(),
            "Authorization": self._user_authorization()
        }
        if req_type == "POST":
            try:
                response = requests.post(method, json=data, headers=_headers, )
            except (requests.ConnectionError, requests.Timeout) as exception:
                return {'stat': 'Not_ok', 'emsg': exception, 'encKey': None}
            if response.status_code == 200:
                return json.loads(response.text)
            else:
                emsg = str(response.status_code) + ' - ' + response.reason
                return {'stat': 'Not_ok', 'emsg': emsg, 'encKey': None}

        elif req_type == "GET":
            try:
                response = requests.get(method, json=data, headers=_headers)
            except (requests.ConnectionError, requests.Timeout) as exception:
                return {'stat': 'Not_ok', 'emsg': exception, 'encKey': None}
            if response.status_code == 200:
                return json.loads(response.text)
            else:
                emsg = str(response.status_code) + ' - ' + response.reason
                return {'stat': 'Not_ok', 'emsg': emsg, 'encKey': None}

    def _error_response(self, message):
        return {"stat": "Not_ok", "emsg": message}

    # Methods to call HTTP Request

    """Userlogin method with userid and userapi_key"""

    def get_contract_master(self, exchange):
        if len(exchange) == 3 or exchange == 'INDICES':
            print(
                "NOTE: Today's contract master file will be updated after 08:00 AM. Before 08:00 AM previous day contract file be downloaded.")
            if time(8, 00) <= datetime.now().time() or True:
                url = self.base_url_c % exchange.upper()
                response = requests.get(url)
                with open("%s.csv" % exchange.upper(), "w") as f:
                    f.write(response.text)
                return self._error_response("Today contract File Downloaded")
            else:
                return self._error_response("Previous day contract file saved")
        elif exchange is None:
            return self._error_response("Invalid Exchange parameter")
        else:
            return self._error_response("Invalid Exchange parameter")

    def get_instrument_by_token(self, exchange, token):
        print((type(token)))
        try:
            contract = pd.read_csv("%s.csv" % exchange)
        except OSError as e:
            if e.errno == 2:
                self.get_contract_master(exchange)
                contract = pd.read_csv("%s.csv" % exchange)
            else:
                return self._error_response(e)
        if exchange == 'INDICES':
            filter_contract = contract[contract['token'] == token].reset_index(drop=False)
            inst = Instrument(filter_contract['exch'][0], filter_contract['token'][0], filter_contract['symbol'][0], '',
                              '', '')
            return inst
        else:
            filter_contract = contract[contract['Token'] == token]
            if len(filter_contract) == 0:
                return self._error_response("The symbol is not available in this exchange")
            else:
                filter_contract = filter_contract.reset_index()
                if 'expiry_date' in filter_contract:
                    inst = Instrument(filter_contract['Exch'][0], filter_contract['Token'][0],
                                      filter_contract['Symbol'][0],
                                      filter_contract['Trading Symbol'][0], filter_contract['Expiry Date'][0],
                                      filter_contract['Lot Size'][0])
                else:
                    inst = Instrument(filter_contract['Exch'][0], filter_contract['Token'][0],
                                      filter_contract['Symbol'][0],
                                      filter_contract['Trading Symbol'][0], '', filter_contract['Lot Size'][0])
                return inst

    def get_instrument_for_fno(self, exch, symbol, expiry_date, is_fut=True, strike=None, is_CE=False):
        # print(exch)
        if exch in ['NFO', 'CDS', 'MCX', 'BFO', 'BCD']:
            if exch == 'CDS':
                edate_format = '%d-%m-%Y'
            else:
                edate_format = '%Y-%m-%d'
        else:
            return self._error_response("Invalid exchange")
        if not symbol:
            return self._error_response("Symbol is Null")
        try:
            expiry_date = datetime.strptime(expiry_date, "%Y-%m-%d").date()
        except ValueError as e:
            return self._error_response(e)
        if type(is_CE) is bool:
            if is_CE == True:
                option_type = "CE"
            else:
                option_type = "PE"
        else:
            return self._error_response("is_fut is not boolean value")
        # print(option_type)
        try:
            contract = pd.read_csv("%s.csv" % exch)
            # print(strike,is_fut)
        except OSError as e:
            if e.errno == 2:
                self.get_contract_master(exch)
                contract = pd.read_csv("%s.csv" % exch)
            else:
                return self._error_response(e)
        if is_fut == False:
            if strike:
                filter_contract = contract[(contract['Exch'] == exch) & (
                        (contract['Symbol'] == symbol) | (contract['Trading Symbol'] == symbol)) & (
                                                   contract['Option Type'] == option_type) & (
                                                   contract['Strike Price'] == strike) & (
                                                   contract['Expiry Date'] == expiry_date.strftime(edate_format))]
            else:
                filter_contract = contract[(contract['Exch'] == exch) & (
                        (contract['Symbol'] == symbol) | (contract['Trading Symbol'] == symbol)) & (
                                                   contract['Option Type'] == option_type) & (
                                                   contract['Expiry Date'] == expiry_date.strftime(edate_format))]
        if is_fut == True:
            if strike == None:
                filter_contract = contract[(contract['Exch'] == exch) & (
                        (contract['Symbol'] == symbol) | (contract['Trading Symbol'] == symbol)) & (
                                                   contract['Option Type'] == 'XX') & (
                                                   contract['Expiry Date'] == expiry_date.strftime(edate_format))]
            else:
                return self._error_response("No strike price for future")
        # print(len(filter_contract))
        if len(filter_contract) == 0:
            return self._error_response("No Data")
        else:
            inst = []
            token = []
            filter_contract = filter_contract.reset_index()
            for i in range(len(filter_contract)):
                if filter_contract['Token'][i] not in token:
                    token.append(filter_contract['Token'][i])
                    inst.append(Instrument(filter_contract['Exch'][i], filter_contract['Token'][i],
                                           filter_contract['Symbol'][i], filter_contract['Trading Symbol'][i],
                                           filter_contract['Expiry Date'][i], filter_contract['Lot Size'][i]))
            if len(inst) == 1:
                return inst[0]
            else:
                return inst

    def get_instrument_by_symbol(self, exchange, symbol):
        try:
            contract = pd.read_csv("%s.csv" % exchange)
        except OSError as e:
            if e.errno == 2:
                self.get_contract_master(exchange)
                contract = pd.read_csv("%s.csv" % exchange)
            else:
                return self._error_response(e)
        if exchange == 'INDICES':
            filter_contract = contract[contract['symbol'] == symbol.upper()]
            if len(filter_contract) == 0:
                return self._error_response("The symbol is not available in this exchange")
            else:
                filter_contract = filter_contract.reset_index()
                inst = Instrument(filter_contract['exch'][0], filter_contract['token'][0], filter_contract['symbol'][0],
                                  '', '', '')
                return inst
        else:
            filter_contract = contract[
                (contract['Symbol'] == symbol.upper()) | (contract['Trading Symbol'] == symbol.upper())]
            if len(filter_contract) == 0:
                return self._error_response("The symbol is not available in this exchange")
            else:
                filter_contract = filter_contract.reset_index()
                if 'expiry_date' in filter_contract:
                    inst = Instrument(filter_contract['Exch'][0], filter_contract['Token'][0],
                                      filter_contract['Symbol'][0], filter_contract['Trading Symbol'][0],
                                      filter_contract['Expiry Date'][0], filter_contract['Lot Size'][0])
                else:
                    inst = Instrument(filter_contract['Exch'][0], filter_contract['Token'][0],
                                      filter_contract['Symbol'][0], filter_contract['Trading Symbol'][0], '',
                                      filter_contract['Lot Size'][0])
                return inst

    def get_session_id(self, data=None):
        data = {'userId': self.user_id.upper()}
        response = self._post("encryption_key", data)
        if response['encKey'] is None:
            return response
        else:
            data = encrypt_string(self.user_id.upper() + self.api_key + response['encKey'])
        data = {'userId': self.user_id.upper(), 'userData': data}
        res = self._post("getsessiondata", data)

        if res['stat'] == 'Ok':
            self.session_id = res['sessionID']
        return res

    def invalid_sess(self, session_ID):
        url = self.base_url + 'ws/invalidateSocketSess'
        headers = {
            'Authorization': 'Bearer ' + self.user_id + ' ' + session_ID,
            'Content-Type': 'application/json'
        }
        payload = {"loginType": "API"}
        datas = json.dumps(payload)
        response = requests.request("POST", url, headers=headers, data=datas)
        return response.json()

    def createSession(self, session_ID):
        url = self.base_url + 'ws/createSocketSess'
        headers = {
            'Authorization': 'Bearer ' + self.user_id + ' ' + session_ID,
            'Content-Type': 'application/json'
        }
        payload = {"loginType": "API"}
        datas = json.dumps(payload)
        response = requests.request("POST", url, headers=headers, data=datas)

        return response.json()

    def __ws_run_forever(self):
        while self.__stop_event.is_set() is False:
            try:
                self.ws.run_forever(ping_interval=3, ping_payload='{"t":"h"}', sslopt={"cert_reqs": ssl.CERT_NONE})
            except Exception as e:
                logger.warning(f"websocket run forever ended in exception, {e}")
            time_module.sleep(0.1)

    def on_message(self, ws, message):
        self.__subscribe_callback(message)
        data = json.loads(message)
        # if 's' in data and data['s'] == 'OK':
        #     self.ws_connection =True
        #     data = {
        #         "k": self.subscriptions,
        #         "t": 't',
        #         "m": "compact_marketdata"
        #     }
        #     ws.send(json.dumps(data))

    def on_error(self, ws, error):
        if (
                type(
                    ws) is not websocket.WebSocketApp):  # This workaround is to solve the websocket_client's compatiblity issue of older versions. ie.0.40.0 which is used in upstox. Now this will work in both 0.40.0 & newer version of websocket_client
            error = ws
        if self.__on_error:
            self.__on_error(error)

    def on_close(self, *arguments, **keywords):
        self.ws_connection = False
        if self.__on_disconnect:
            self.__on_disconnect()

    def stop_websocket(self):
        self.ws_connection = False
        self.ws.close()
        self.__stop_event.set()

    def on_open(self, ws):
        initCon = {
            "susertoken": self.ENC,
            "t": "c",
            "actid": self.user_id + "_API",
            "uid": self.user_id + "_API",
            "source": "API"
        }
        self.ws.send(json.dumps(initCon))
        self.ws_connection = True
        if self.__on_open:
            self.__on_open()

    def subscribe(self, instrument):
        # print("Subscribed")
        scripts = ""
        for __instrument in instrument:
            scripts = scripts + __instrument.exchange + "|" + str(__instrument.token) + "#"
        self.subscriptions = scripts[:-1]
        if self.market_depth:
            t = "d"  # Subscribe Depth
        else:
            t = "t"  # Subsribe token
        data = {
            "k": self.subscriptions,
            "t": t
        }
        # "m": "compact_marketdata"
        self.ws.send(json.dumps(data))

    def unsubscribe(self, instrument):
        # print("UnSubscribed")
        scripts = ""
        if self.subscriptions:
            split_subscribes = self.subscriptions.split('#')
        for __instrument in instrument:
            scripts = scripts + __instrument.exchange + "|" + str(__instrument.token) + "#"
            if self.subscriptions:
                split_subscribes.remove(__instrument.exchange + "|" + str(__instrument.token))
        self.subscriptions = split_subscribes

        if self.market_depth:
            t = "ud"
        else:
            t = "u"

        data = {
            "k": scripts[:-1],
            "t": t
        }
        self.ws.send(json.dumps(data))

    def start_websocket(self, socket_open_callback=None, socket_close_callback=None, socket_error_callback=None,
                        subscription_callback=None, check_subscription_callback=None, run_in_background=False,
                        market_depth=False):
        if check_subscription_callback != None:
            check_subscription_callback(self.script_subscription_instrument)
        session_request = self.session_id
        self.__on_open = socket_open_callback
        self.__on_disconnect = socket_close_callback
        self.__on_error = socket_error_callback
        self.__subscribe_callback = subscription_callback
        self.market_depth = market_depth
        if self.__stop_event != None and self.__stop_event.is_set():
            self.__stop_event.clear()
        if session_request:
            session_id = session_request
            sha256_encryption1 = hashlib.sha256(session_id.encode('utf-8')).hexdigest()
            self.ENC = hashlib.sha256(sha256_encryption1.encode('utf-8')).hexdigest()
            invalidSess = self.invalid_sess(session_id)
            if invalidSess['stat'] == 'Ok':
                print("STAGE 1: Invalidate the previous session :", invalidSess['stat'])
                createSess = self.createSession(session_id)
                if createSess['stat'] == 'Ok':
                    print("STAGE 2: Create the new session :", createSess['stat'])
                    print("Connecting to Socket ...")
                    self.__stop_event = threading.Event()
                    websocket.enableTrace(False)
                    self.ws = websocket.WebSocketApp(self._sub_urls['base_url_socket'],
                                                     on_open=self.on_open,
                                                     on_message=self.on_message,
                                                     on_close=self.on_close,
                                                     on_error=self.on_error)

                    # if run_in_background:
                    #         print("Running background!")
                    #         self.__ws_thread = threading.Thread(target=self.__ws_run_forever())
                    #         self.__ws_thread.daemon = True
                    #         self.__ws_thread.start()
                    # else:
                    #     try:
                    #         self.ws.run_forever(dispatcher=rel)  # Set dispatcher to automatic reconnection
                    #         rel.signal(2, rel.abort)  # Keyboard Interrupt
                    #         rel.dispatch()
                    #     except Exception as e:
                    #         print("Error:",e)
                    if run_in_background is True:
                        self.__ws_thread = threading.Thread(target=self.__ws_run_forever)
                        self.__ws_thread.daemon = True
                        self.__ws_thread.start()
                    else:
                        self.__ws_run_forever()


class Alice_Wrapper():

    def subscription(script_list):
        if len(script_list) > 0:
            Aliceblue.script_subscription_instrument = script_list
            sub_prams = ''
            # print(script_list)
            for i in range(len(script_list)):
                end_point = '' if i == len(script_list) - 1 else '#'
                sub_prams = sub_prams + script_list[i].exchange + '|' + str(script_list[i].token) + end_point
            return sub_prams
        else:
            return {'stat': 'Not_ok', 'emsg': 'Script response is not fetched properly. Please check once'}
