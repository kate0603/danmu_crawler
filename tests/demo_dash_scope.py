# For prerequisites running the following sample, visit https://help.aliyun.com/document_detail/611472.html
"""
向【阿里云-通义千问】发起请求
"""
from http import HTTPStatus
import dashscope


def call_with_messages():
    dashscope.api_key = "xx"
    prompt_text = """问题？ """

    resp = dashscope.Generation.call(
        model="qwen-max",
        # model='qwen-max-1201',
        # model='qwen-max-longcontext',
        prompt=prompt_text,
    )
    # The response status_code is HTTPStatus.OK indicate success,
    # otherwise indicate request is failed, you can get error code
    # and message from code and message.
    if resp.status_code == HTTPStatus.OK:
        print(resp.output)  # The output text
        print(resp.usage)  # The usage information
    else:
        print(resp.code)  # The error code.
        print(resp.message)  # The error message.


if __name__ == "__main__":
    call_with_messages()
