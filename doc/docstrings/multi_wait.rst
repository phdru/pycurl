wait(extra_fds, timeout_ms) -> int

Poll on all easy handles in a multi handle.

*extra_fds* is not yet implemenetd and must be ``None``. It's here for
future compatibility.

*timeout_ms* is timeout in milliseconds.

Returns the total number of file descriptors on which events occurred.

Corresponds to `curl_multi_wait`_ in libcurl.

.. _curl_multi_timeout: https://curl.haxx.se/libcurl/c/curl_multi_wait.html
