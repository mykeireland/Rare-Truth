🔍 snapshot debug – price type: <class 'float'>, value: 1.72

No error handlers are registered, logging exception.

Traceback (most recent call last):

  File "/opt/venv/lib/python3.12/site-packages/telegram/ext/_application.py", line 1234, in process_update

    await coroutine

  File "/opt/venv/lib/python3.12/site-packages/telegram/ext/_basehandler.py", line 157, in handle_update

    return await self.callback(update, context)

           ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

  File "/app/snapshot.py", line 46, in snapshot

    if lo <= price <= hi:

       ^^^^^^^^^^^^^^^^^

TypeError: '<=' not supported between instances of 'str' and 'float'
