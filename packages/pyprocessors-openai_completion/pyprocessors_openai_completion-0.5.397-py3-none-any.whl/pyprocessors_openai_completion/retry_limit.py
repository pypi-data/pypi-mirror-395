import openai
from tenacity import retry_base, Retrying, stop_after_attempt, wait_random
from tenacity.wait import wait_base


def is_throttling_related_exception(e: Exception) -> bool:
    # check is the exception is a requests one,
    # and if the status_code is a throttling related one.
    return isinstance(e, openai.error.OpenAIError)


class retry_if_throttling(retry_base):
    def __call__(self, retry_state) -> bool:
        # if the call failed (raised an exception)
        if retry_state.outcome.failed:
            exception = retry_state.outcome.exception()
            return is_throttling_related_exception(exception)


class wait_until_quota_restore(wait_base):
    def __init__(self, max_call_number: int, max_call_number_interval: int):
        self.max_call_number = max_call_number
        self.max_call_number_interval = max_call_number_interval

    def __call__(self, retry_state) -> float or int:
        if retry_state.outcome.failed:
            exception = retry_state.outcome.exception()

            if is_throttling_related_exception(exception):
                return self.max_call_number_interval / self.max_call_number

        # if this is an unknown exception, retry immediately
        return 0


def api_retry(
        max_call_number: int, max_call_number_interval: int, max_attempt_number: int = 10
):
    """
    This endpoint allows `max_call_number` per `max_call_number_interval`.
    """

    def decorator(func):
        def wrapper(*args, **kwargs):
            return Retrying(
                retry=retry_if_throttling(),
                stop=stop_after_attempt(max_attempt_number=max_attempt_number),
                wait=(
                        wait_until_quota_restore(max_call_number, max_call_number_interval)
                        + wait_random(min=1, max=3)
                ),
            )(func, *args, **kwargs)

        return wrapper

    return decorator
