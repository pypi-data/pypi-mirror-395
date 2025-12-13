
from uuid import uuid1
import time

#from functools import wraps

import asyncio
from asyncio import Queue

def async_to_sync(async_func):
    """Simple async to sync wrapper using asyncio.run"""
    def wrapper(*args, **kwargs):
        try:
            loop = asyncio.get_event_loop()
            if loop.is_running():
                # If event loop is running, we can't use run()
                # This is a limitation - sync methods won't work in async context
                raise RuntimeError("Cannot call sync method from within async context. Use the async version instead.")
            else:
                return loop.run_until_complete(async_func(*args, **kwargs))
        except RuntimeError:
            # No event loop, create one
            return asyncio.run(async_func(*args, **kwargs))
    return wrapper

from .magic import AetherMagic

class AetherTask():

    def __init__(self, job, task, context="x", on_perform=None, on_status=None, on_complete=None, on_cancel=None, on_timeout=None, timeout=300, channel: str = ""):

        # Request the shared AetherMagic instance for this thread and channel
        self.__instance = AetherMagic.shared(channel=channel)
        self.__job = job
        self.__workgroup = 'workgroup'
        self.__task = task
        self.__context = context
        self.__tid = str(uuid1())[:8]
        self.__channel = channel

        self.__on_perform_func = on_perform
        self.__on_status_func = on_status
        self.__on_complete_func = on_complete
        self.__on_cancel_func = on_cancel
        self.__on_timeout_func = on_timeout
        
        # Timeout settings (default 5 minutes = 300 seconds)
        self.__timeout = timeout
        self.__timeout_task = None
        self.__last_activity_time = None
        self.__is_completed = False

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        pass

    def copy(self, tid=''):
        ae_copy = AetherTask(
            job=self.__job,
            task=self.__task,
            context=self.__context,
            on_perform=self.__on_perform_func,
            on_status=self.__on_status_func,
            on_complete=self.__on_complete_func,
            on_cancel=self.__on_cancel_func,
            on_timeout=self.__on_timeout_func,
            timeout=self.__timeout,
            channel=self.__channel
        )

        # Copying tid (or setting new)
        if tid: ae_copy.tid_(tid)
        else: ae_copy.tid_(self.__tid)

        return ae_copy

#	def __call__(self, querying_func):
#		@wraps(querying_func)
#		def inner(*args, **kwargs):
#			with self:
#				return querying_func(*args, **kwargs)
#		return inner


    def tid_(self, tid=''):
        if tid: self.__tid = tid
        return self.__tid
        
    def timeout_(self):
        """Get current timeout value in seconds"""
        return self.__timeout
        
    def set_timeout_(self, timeout):
        """Set new timeout value in seconds"""
        self.__timeout = timeout

    def idle_(self):
        return async_to_sync(self.idle)()

    def perform_(self, data={}):
        return async_to_sync(self.perform)(data)

    def status_(self, progress, data={}, immediate=False):
        return async_to_sync(self.status)(progress, data, immediate)

    def complete_(self, success, data={}):
        return async_to_sync(self.complete)(success, data)

    def cancel_timeout_(self):
        return async_to_sync(self.cancel_timeout)()

    async def cancel_timeout(self):
        """Cancel the timeout timer"""
        if self.__timeout_task and not self.__timeout_task.done():
            self.__timeout_task.cancel()
            self.__timeout_task = None

    async def _timeout_handler(self):
        """Internal timeout handler that calls the user callback"""
        try:
            await asyncio.sleep(self.__timeout)
            
            # Check if task was completed while we were sleeping
            if not self.__is_completed and self.__on_timeout_func:
                await self.__on_timeout_func(self)
                
        except asyncio.CancelledError:
            # Timeout was cancelled, which is normal
            pass

    async def _start_timeout_timer(self):
        """Start the timeout timer"""
        if self.__timeout > 0 and self.__on_timeout_func:
            # Cancel existing timer if any
            await self.cancel_timeout()
            
            # Start new timer
            self.__timeout_task = asyncio.create_task(self._timeout_handler())
            self.__last_activity_time = time.time()

    async def _reset_timeout_timer(self):
        """Reset the timeout timer (called on status/complete)"""
        self.__last_activity_time = time.time()
        
        # We don't restart the timer on status, just update activity time
        # The timer continues running until complete or timeout

    async def tid(self, tid=''):
        if tid: self.__tid = tid
        return self.__tid

    async def idle(self, immediate=False):
        if not self.__on_perform_func is None:  
            if not self.__instance is None:
                await self.__instance.idle(self.__job, self.__workgroup, self.__task, self.__context, self.__tid, {}, self.on_handle, immediate=immediate)

        return self.__tid


    async def perform(self, data={}, immediate=False):
        if not self.__instance is None:
            await self.__instance.perform(self.__job, self.__workgroup, self.__task, self.__context, self.__tid, data, self.on_handle, immediate=immediate)
            
            # Start timeout timer after sending perform
            await self._start_timeout_timer()

        return self.__tid


    async def complete(self, success, data={}, immediate=False):
        if not self.__instance is None:
            await self.__instance.complete(self.__job, self.__workgroup, self.__task, self.__context, self.__tid, data, None, success, immediate=immediate)
            
            # Mark as completed and cancel timeout
            self.__is_completed = True
            await self.cancel_timeout()

        return self.__tid


    async def status(self, progress, data={}, immediate=False):

        if progress < 0: progress = 0
        elif progress > 100: progress = 100

        if not self.__instance is None:
            await self.__instance.status(self.__job, self.__workgroup, self.__task, self.__context, self.__tid, data, None, progress, immediate=immediate)
            
            # Reset timeout timer on status update
            await self._reset_timeout_timer()

        return self.__tid


    async def on_handle(self, action, tid, data, fulldata):

        # Variables to use
        status = fulldata['status']
        succeed = True if status == 'succeed' else False
        failed = True if status == 'failed' else False
        complete = True if succeed or failed else False
        progress = fulldata['progress']


        callback_perform = None
        callback_complete = None
        callback_status = None
        callback_cancel = None

        # AetherTask to send to handle functions
        ae_task = self

        if action == 'perform':

            callback_perform = self.__on_perform_func

            # if we are assigned to 'preform' action, we should reply with same tid.
            ae_task = self.copy(tid)


        elif action == 'status':			

            callback_status = self.__on_status_func
            # Reset timeout timer on incoming status
            asyncio.create_task(self._reset_timeout_timer())

        elif action == 'complete':

            callback_status = self.__on_status_func
            callback_complete = self.__on_complete_func
            # Mark as completed and cancel timeout
            self.__is_completed = True
            asyncio.create_task(self.cancel_timeout())

        elif action == 'cancel':

            callback_cancel = self.__on_cancel_func



        if callback_perform is not None:
            asyncio.create_task(callback_perform(ae_task, data))

        if callback_status is not None:
            asyncio.create_task(callback_status(ae_task, complete, succeed, progress, data))

        if callback_complete is not None:
            asyncio.create_task(callback_complete(ae_task, succeed, data))

        if callback_cancel is not None:
            asyncio.create_task(callback_cancel(ae_task, data))

