import base64
from typing import Generator

import spnego
from httpx import Auth, Request, Response


class UnknownSignatureAlgorithmOID(Warning):
    pass


class HttpNtlmAuth(Auth):
    """ HTTP NTLM Authentication Handler for HTTPX. """

    def __init__(self, username, password, send_cbt=True):
        """Create an authentication handler for NTLM over HTTP.
        :param str username: Username in 'domain\\username' format
        :param str password: Password
        :param bool send_cbt: Will send the channel bindings over a HTTPS channel (Default: True)
        """
        self.username = username
        self.password = password
        self.send_cbt = send_cbt

    def auth_flow(self, request: Request) -> Generator[Request, Response, None]:

        def auth_from_header(header):
            """
            Given a WWW-Authenticate or Proxy-Authenticate header, returns the
            authentication type to use. We prefer NTLM over Negotiate if the server
            supports it.
            """
            header = header.lower() or ""
            if "ntlm" in header:
                return "NTLM"
            elif "negotiate" in header:
                return "Negotiate"
            return None

        request.headers["Connection"] = "Keep-Alive"
        response = yield request
        if response.status_code in (401, 407):
            yield from self._retry_using_ntlm(request, response)

    def _retry_using_ntlm(self, request: Request, response):

        def auth_from_header(header):
            """
            Given a WWW-Authenticate or Proxy-Authenticate header, returns the
            authentication type to use. We prefer NTLM over Negotiate if the server
            suppports it.
            """
            header = header.lower() or ""
            if "ntlm" in header:
                return "NTLM"
            elif "negotiate" in header:
                return "Negotiate"
            return None

        if response.status_code == 401:
            resp_header = "www-authenticate"
            req_header = "Authorization"
        elif response.status_code == 407:
            resp_header = "proxy-authenticate"
            req_header = "Proxy-authorization"
        auth_type = auth_from_header(response.headers.get(resp_header))
        if not auth_type:
            return
            
        """Attempt to authenticate using HTTP NTLM challenge/response."""
        if req_header in request.headers:
            return
        # content_length = int(request.headers.get("Content-Length") or "0", base=10)
        # if hasattr(request.body, "seek"):
        #     if content_length > 0:
        #         request.body.seek(-content_length, 1)
        #     else:
        #         request.body.seek(0, 0)
        # request = request.copy()
        # ntlm returns the headers as a base64 encoded bytestring. Convert to
        # a string.
        client = spnego.client(self.username, self.password, protocol="ntlm",
                               options=spnego.NegotiateOptions.use_ntlm)
        # Perform the first step of the NTLM authentication
        negotiate_message = base64.b64encode(client.step()).decode("ascii")

        request.headers[req_header] = f"{auth_type} {negotiate_message}"
        # A streaming response breaks authentication.
        # This can be fixed by not streaming this request, which is safe
        # because the returned response3 will still have stream=True set if
        # specified in args. In addition, we expect this request to give us a
        # challenge and not the real content, so the content will be short anyway.
        response2 = yield request

        # this is important for some web applications that store
        # authentication-related info in cookies (it took a long time to figure out)
        # The original code was naively copying the Set-Cookie header from the
        # intermediate 401 response directly into the Cookie header of the next
        # request. This includes attributes like Path, HttpOnly, etc., which
        # are invalid in a Cookie header. If the server (or a load balancer in
        # front of it) relies on session affinity cookies to route the NTLM
        # handshake to the same backend node, sending a malformed cookie will
        # cause the request to be routed to a new node, which will reject the
        # final NTLM message with a 401.
        set_cookies = response2.headers.get_list("set-cookie")
        if set_cookies:
            original_cookies = request.headers.get("Cookie")
            cookie_parts = (set(original_cookies.split("; "))
                            if original_cookies else set())
            for sc in set_cookies:
                cookie_parts.add(sc.split(';', 1)[0])
            request.headers["Cookie"] = "; ".join(cookie_parts)

        # get the challenge
        auth_header_value = response2.headers[resp_header]

        auth_strip = auth_type + " "

        ntlm_header_value = next(
            s
            for s in (val.lstrip() for val in auth_header_value.split(","))
            if s.startswith(auth_strip)
        ).strip()

        # Parse the challenge in the ntlm context
        # Parse the challenge in the ntlm context and perform
        # the second step of authentication
        val = base64.b64decode(ntlm_header_value[len(auth_strip):].encode())
        authenticate_message = base64.b64encode(client.step(val)).decode("ascii")

        auth = f"{auth_type} {authenticate_message}"
        request.headers[req_header] = auth
        yield request
