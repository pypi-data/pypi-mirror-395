import requests
import json
import os
from typing import Tuple, Dict, List, Optional, Any, Union

# Hilfsfunktion, um Werte aus verschachtelten Dictionaries zu holen
def _get_value_from_dict(data_dict: Dict, keys: Union[str, Tuple[str, ...]]) -> Optional[str]:
    if isinstance(keys, str):
        return data_dict.get(keys)
    current_level = data_dict
    for key in keys:
        if not isinstance(current_level, dict) or key not in current_level:
            return None
        current_level = current_level[key]
    return current_level if isinstance(current_level, str) else None


class RestClient:
    """
    Erweiterte Client-Klasse für HTTP REST API Requests mit Login, Token-Refresh
    und automatischem Wiederholen von Anfragen.
    """

    def __init__(self, base_url: str,
                 login_url: Optional[str] = None,
                 refresh_url: Optional[str] = None,
                 token_paths: Optional[Dict[str, Union[str, Tuple[str, ...]]]] = None,
                 default_headers: Optional[Dict[str, str]] = None,
                 timeout: float = 10.0):
        """
        Initialisiert den REST-Client.

        :param base_url: Die Basis-URL der API.
        :param login_url: Relativer Endpunkt für den Login (z.B. "/auth/login").
        :param refresh_url: Relativer Endpunkt für den Token-Refresh (z.B. "/auth/refresh").
        :param token_paths: Dictionary, das angibt, wo die Token in der Login/Refresh-Antwort zu finden sind.
                           z.B. {"access": "access_token", "refresh": "refresh_token"}
                           oder für verschachtelte Tokens: {"access": ("data", "accessToken")}
        :param default_headers: Optionale Standard-Header.
        :param timeout: Standard-Timeout.
        """
        self.base_url = base_url.rstrip('/')
        self.session = requests.Session()
        self.timeout = timeout

        self.login_url = login_url
        self.refresh_url = refresh_url
        # Standardpfade, falls nicht anders angegeben und Login/Refresh genutzt werden
        self.token_paths = token_paths or {"access": "access_token", "refresh": "refresh_token"}

        self.access_token: Optional[str] = None
        self.refresh_token_value: Optional[str] = None # Renamed to avoid confusion with _refresh_access_token method
        self._username: Optional[str] = None
        self._password: Optional[str] = None
        self._is_refreshing_token: bool = False # Lock, um parallele Refresh-Versuche zu vermeiden

        if default_headers:
            self.session.headers.update(default_headers)

    def _make_url(self, endpoint: str) -> str:
        _endpoint = endpoint.lstrip('/')
        return f"{self.base_url}/{_endpoint}"

    def _update_tokens_from_response(self, response_data: Dict) -> bool:
        """Extrahiert und speichert Tokens aus einer Antwort."""
        access_key = self.token_paths.get("access")
        refresh_key = self.token_paths.get("refresh")
        new_access_token = None
        new_refresh_token = None

        if access_key:
            new_access_token = _get_value_from_dict(response_data, access_key)
        if refresh_key:
            new_refresh_token = _get_value_from_dict(response_data, refresh_key)

        if new_access_token:
            self.access_token = new_access_token
            # Wenn nur ein Access-Token zurückkommt (z.B. bei manchen Refresh-Flows),
            # behalten wir das alte Refresh-Token, falls vorhanden.
            # Nur wenn ein *neues* Refresh-Token explizit gesendet wird, überschreiben wir es.
            if new_refresh_token is not None: # Explizit auch None prüfen, falls das Feld da ist aber leer
                 self.refresh_token_value = new_refresh_token
            return True
        return False

    def login(self, username: str, password: str, payload_builder: Optional[callable] = None) -> bool:
        """
        Führt einen Login durch und speichert die Tokens.

        :param username: Benutzername.
        :param password: Passwort.
        :param payload_builder: Optionale Funktion, die username und password nimmt und
                                das Request-Payload-Dictionary für den Login zurückgibt.
                                Default: {"username": username, "password": password}
        :return: True bei Erfolg, False bei Fehler.
        """
        if not self.login_url:
            print("Login URL nicht konfiguriert.")
            return False

        self._username = username # Für späteres automatisches Re-Login speichern
        self._password = password

        if payload_builder:
            login_payload = payload_builder(username, password)
        else:
            login_payload = {"username": username, "password": password} # Typisches Payload

        full_login_url = self._make_url(self.login_url)
        try:
            # Login-Request sollte nicht den Authorization-Header verwenden,
            # daher temporär keine Session-Header nutzen oder explizit leeren.
            # Einfacher ist, _perform_actual_request direkt zu rufen.
            response = self.session.post(full_login_url, json=login_payload, timeout=self.timeout)
            response.raise_for_status() # Wirft HTTPError für 4xx/5xx
            
            login_data = response.json()
            if self._update_tokens_from_response(login_data):
                print("Login erfolgreich.")
                return True
            else:
                print(f"Login erfolgreich, aber Tokens nicht in der Antwort gefunden (Pfade: {self.token_paths}). Antwort: {login_data}")
                self.access_token = None # Sicherstellen, dass keine alten Tokens verwendet werden
                self.refresh_token_value = None
                return False
        except requests.exceptions.HTTPError as e:
            print(f"Login fehlgeschlagen (HTTP {e.response.status_code}): {e.response.text}")
        except requests.exceptions.RequestException as e:
            print(f"Login fehlgeschlagen (Netzwerk/Request Fehler): {e}")
        except json.JSONDecodeError:
            print(f"Login-Antwort war kein valides JSON.")
        
        self.access_token = None # Sicherstellen, dass keine alten Tokens verwendet werden
        self.refresh_token_value = None
        return False

    def _refresh_access_token(self) -> bool:
        """Versucht, den Access Token mit dem Refresh Token zu erneuern."""
        if not self.refresh_url or not self.refresh_token_value:
            # print("Kein Refresh-URL oder Refresh-Token vorhanden.")
            return False
        
        # Lock setzen, um zu verhindern, dass mehrere Anfragen gleichzeitig refreshen
        if self._is_refreshing_token:
            print("Token-Refresh läuft bereits, warte...")
            # Hier könnte man eine Warte-Logik einbauen, aber für den Moment einfach false
            return False 
        self._is_refreshing_token = True

        full_refresh_url = self._make_url(self.refresh_url)
        # Annahme: Refresh-Token wird im Body als JSON gesendet.
        # Dies kann API-spezifisch sein (manchmal Header, manchmal form-data).
        # Hier ein gängiges Beispiel:
        refresh_payload_key = self.token_paths.get("refresh_payload_key", "refresh_token")
        refresh_payload = {refresh_payload_key: self.refresh_token_value}

        try:
            print("Versuche Token-Refresh...")
            response = self.session.post(full_refresh_url, json=refresh_payload, timeout=self.timeout)
            response.raise_for_status()
            refresh_data = response.json()
            if self._update_tokens_from_response(refresh_data):
                print("Token-Refresh erfolgreich.")
                return True
            else:
                print(f"Token-Refresh erfolgreich, aber Tokens nicht in der Antwort gefunden (Pfade: {self.token_paths}). Antwort: {refresh_data}")
                # Wichtig: Wenn Refresh fehlschlägt, alte Tokens invalidieren,
                # um Endlosschleifen zu vermeiden, wenn der Refresh-Token selbst abgelaufen ist.
                self.access_token = None
                self.refresh_token_value = None 
                return False
        except requests.exceptions.HTTPError as e:
            print(f"Token-Refresh fehlgeschlagen (HTTP {e.response.status_code}): {e.response.text}")
            # Bei 401/403 auf Refresh-Endpoint ist der Refresh-Token wahrscheinlich ungültig/abgelaufen
            if e.response.status_code in [401, 403]:
                self.access_token = None
                self.refresh_token_value = None
        except requests.exceptions.RequestException as e:
            print(f"Token-Refresh fehlgeschlagen (Netzwerk/Request Fehler): {e}")
        except json.JSONDecodeError:
            print(f"Refresh-Antwort war kein valides JSON.")
        finally:
            self._is_refreshing_token = False
        
        return False

    def _handle_response(self, response: requests.Response) -> Tuple[Optional[Union[Dict, List]], int]:
        # (Unverändert von der vorherigen Version)
        status_code = response.status_code
        try:
            if response.content:
                data = response.json()
            elif 200 <= status_code < 300:
                data = None
            else:
                data = {"error": "Kein JSON-Inhalt in der Fehlerantwort", "raw_content": response.text}
        except requests.exceptions.JSONDecodeError:
            data = {"error": "Antwort ist kein valides JSON", "raw_content": response.text}
        except Exception as e:
            data = {"error": f"Unerwarteter Fehler beim Parsen der Antwort: {str(e)}", "raw_content": response.text}
        return data, status_code

    def _perform_actual_request(self, method: str, url: str, **kwargs) -> Tuple[Optional[requests.Response], int]:
        """Führt den eigentlichen HTTP-Request aus und gibt Response-Objekt oder Fehler-Dict zurück."""
        try:
            response = self.session.request(method, url, **kwargs)
            return response, response.status_code
        except requests.exceptions.Timeout:
            return {"error": f"Request timed out after {kwargs.get('timeout', self.timeout)} seconds"}, 0
        except requests.exceptions.ConnectionError as e:
            return {"error": f"Connection error: {str(e)}"}, 0
        except requests.exceptions.RequestException as e:
            return {"error": f"Request failed: {str(e)}"}, 0
        except Exception as e:
            return {"error": f"An unexpected error occurred: {str(e)}"}, 0


    def _request(self, method: str, endpoint: str, params: Optional[Dict] = None,
                 json_data: Optional[Dict] = None, data: Any = None, files: Optional[Dict] = None,
                 stream: bool = False, attempt_count: int = 1, **kwargs) -> Tuple[Any, int]:
        """
        Interne Methode zum Absetzen der HTTP-Anfrage mit Retry-Logik für Token-Refresh.
        """
        if self._is_refreshing_token and endpoint not in (self.login_url, self.refresh_url):
            # Wenn gerade ein Token-Refresh läuft und dies nicht der Refresh-Request selbst ist,
            # könnte man hier warten oder die Anfrage fehlschlagen lassen.
            # Fürs Erste: Fehlermeldung und Anfrage nicht durchführen.
            # Eine robustere Lösung würde hier eine Warteschleife mit Timeout implementieren.
            print("Warte auf Token-Refresh, Anfrage wird momentan nicht ausgeführt.")
            return {"error": "Token refresh in progress, request paused"}, 0

        full_url = self._make_url(endpoint)
        
        # Headers für diesen Request vorbereiten (Session-Header + Request-spezifische Header)
        request_headers = self.session.headers.copy() # Start with session defaults
        if 'headers' in kwargs:
            request_headers.update(kwargs.pop('headers')) # Override/add with per-request headers

        if self.access_token and endpoint != self.login_url : # Kein Auth-Header für Login-Request selbst
            request_headers['Authorization'] = f"Bearer {self.access_token}"

        current_timeout = kwargs.pop('timeout', self.timeout)

        response_or_error, status_code = self._perform_actual_request(
            method,
            full_url,
            params=params,
            json=json_data,
            data=data,
            files=files,
            stream=stream,
            headers=request_headers,
            timeout=current_timeout,
            **kwargs # Verbleibende kwargs
        )

        # Wenn _perform_actual_request schon einen Fehler als dict zurückgegeben hat
        if not isinstance(response_or_error, requests.Response):
            return response_or_error, status_code # (z.B. Timeout, ConnectionError)

        # Ab hier ist response_or_error ein requests.Response Objekt
        response = response_or_error

        # --- Token Refresh und Retry Logik ---
        if response.status_code == 401 and attempt_count == 1: # Nur beim ersten Versuch
            print(f"Anfrage an {endpoint} ergab 401. Access Token könnte abgelaufen sein.")
            
            refreshed_successfully = False
            if self.refresh_url and self.refresh_token_value:
                if self._refresh_access_token():
                    refreshed_successfully = True
                
            if not refreshed_successfully and self.login_url and self._username and self._password:
                # Wenn Refresh fehlgeschlagen oder nicht möglich, versuche kompletten Re-Login
                print("Token-Refresh fehlgeschlagen oder nicht möglich. Versuche Re-Login...")
                if self.login(self._username, self._password): # Verwendet gespeicherte Credentials
                    refreshed_successfully = True # Technisch "re-logged-in successfully"

            if refreshed_successfully:
                print(f"Token erneuert/neu eingeloggt. Wiederhole Anfrage an {endpoint}...")
                # Wichtig: Ursprüngliche Argumente für den Retry verwenden!
                # Die `kwargs` hier sind schon modifiziert (headers, timeout rausgepoppt).
                # Besser, wenn man `_request` die Original-kwargs mitgibt für den Retry.
                # Für diese Implementierung: Wir rufen _request rekursiv auf.
                # json_data, data, files müssen auch übergeben werden.
                original_kwargs_for_retry = kwargs # Enthält nur noch "übrige" kwargs
                # `headers` wird im nächsten Aufruf neu gebaut.
                return self._request(method, endpoint, params, json_data, data, files, stream, attempt_count + 1, **original_kwargs_for_retry)
            else:
                print("Token-Erneuerung und Re-Login fehlgeschlagen. Gebe 401 Fehler zurück.")
        # --- Ende Token Refresh Logik ---

        if stream and response.ok:
            return response, response.status_code # Rohes Response-Objekt für Streaming

        return self._handle_response(response)


    # --- Öffentliche Methoden für HTTP-Verben ---
    # Diese rufen nun _request auf, das die Retry-Logik beinhaltet.
    def get(self, endpoint: str, params: Optional[Dict] = None, **kwargs) -> Tuple[Optional[Union[Dict, List]], int]:
        return self._request("GET", endpoint, params=params, **kwargs)

    def post(self, endpoint: str, json_data: Optional[Dict] = None, data: Any = None, **kwargs) -> Tuple[Optional[Union[Dict, List]], int]:
        return self._request("POST", endpoint, json_data=json_data, data=data, **kwargs)

    def put(self, endpoint: str, json_data: Optional[Dict] = None, data: Any = None, **kwargs) -> Tuple[Optional[Union[Dict, List]], int]:
        return self._request("PUT", endpoint, json_data=json_data, data=data, **kwargs)

    def delete(self, endpoint: str, params: Optional[Dict] = None, **kwargs) -> Tuple[Optional[Union[Dict, List]], int]:
        return self._request("DELETE", endpoint, params=params, **kwargs)

    def patch(self, endpoint: str, json_data: Optional[Dict] = None, data: Any = None, **kwargs) -> Tuple[Optional[Union[Dict, List]], int]:
        return self._request("PATCH", endpoint, json_data=json_data, data=data, **kwargs)

    def upload_file(self, endpoint: str, file_path: str, file_form_name: str = "file",
                    additional_data: Optional[Dict] = None, method: str = "POST", **kwargs) -> Tuple[Optional[Union[Dict, List]], int]:
        if not os.path.exists(file_path):
            return {"error": f"File not found: {file_path}"}, 0
        if not os.path.isfile(file_path):
            return {"error": f"Path is not a file: {file_path}"}, 0

        try:
            with open(file_path, 'rb') as f:
                files_payload = {file_form_name: (os.path.basename(file_path), f)}
                return self._request(method.upper(), endpoint, data=additional_data, files=files_payload, **kwargs)
        except IOError as e:
            return {"error": f"Could not open or read file {file_path}: {str(e)}"}, 0
        except Exception as e:
             return {"error": f"Error during file preparation for upload: {str(e)}"}, 0

    def download_file(self, endpoint: str, local_save_path: str, params: Optional[Dict] = None,
                      chunk_size: int = 8192, **kwargs) -> Tuple[Optional[Dict], int]:
        response_or_data, status_code = self._request("GET", endpoint, params=params, stream=True, **kwargs)

        if not isinstance(response_or_data, requests.Response):
            return response_or_data, status_code

        raw_response = response_or_data
        try:
            with open(local_save_path, 'wb') as f:
                for chunk in raw_response.iter_content(chunk_size=chunk_size):
                    if chunk:
                        f.write(chunk)
            raw_response.close()
            return {"message": "File downloaded successfully", "path": local_save_path}, status_code
        except IOError as e:
            raw_response.close()
            return {"error": f"Could not write to file {local_save_path}: {str(e)}"}, 0
        except Exception as e:
            raw_response.close()
            return {"error": f"An unexpected error occurred during file download: {str(e)}"}, 0

