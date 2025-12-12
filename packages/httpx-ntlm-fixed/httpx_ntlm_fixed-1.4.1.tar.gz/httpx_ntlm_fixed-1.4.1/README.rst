httpx-ntlm
==========

This package allows for HTTP NTLM authentication using the HTTPX library. It is an
adaptation of https://github.com/requests/requests-ntlm.

Usage
-----

``HttpNtlmAuth`` extends HTTPX ``Auth`` base class, so usage is simple:

.. code:: python

    import httpx
    from httpx_ntlm import HttpNtlmAuth

    httpx.get("http://ntlm_protected_site.com",auth=HttpNtlmAuth('domain\\username','password'))

``HttpNtlmAuth`` can be used in conjunction with a ``Client`` in order to
make use of connection pooling. Since NTLM authenticates connections,
this is more efficient. Otherwise, each request will go through a new
NTLM challenge-response.

.. code:: python

    import httpx
    from httpx_ntlm import HttpNtlmAuth

    client = httpx.Client(auth=HttpNtlmAuth('domain\\username','password'))
    client.get('http://ntlm_protected_site.com')

Installation
------------

    pip install httpx-ntlm-fixed

Requirements
------------

- httpx_
- pyspnego_

.. _httpx: https://github.com/encode/httpx
.. _pyspnego: https://github.com/jborean93/pyspnego
