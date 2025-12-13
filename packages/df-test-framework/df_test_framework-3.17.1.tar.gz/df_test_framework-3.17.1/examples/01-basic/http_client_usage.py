"""
HTTP客户端使用示例

演示如何使用DF Test Framework的HttpClient发送HTTP请求。
"""

from pydantic import Field

from df_test_framework import Bootstrap, FrameworkSettings


class Settings(FrameworkSettings):
    """示例配置"""

    api_base_url: str = Field(
        default="https://jsonplaceholder.typicode.com",
        description="API基础URL"
    )


def example_get_request():
    """示例1: 发送GET请求"""
    print("\n" + "="*60)
    print("示例1: 发送GET请求")
    print("="*60)

    # 初始化框架
    app = Bootstrap().with_settings(Settings).build()
    runtime = app.run()
    http = runtime.http_client()

    # 发送GET请求
    response = http.get("/users/1")

    print(f"状态码: {response.status_code}")
    print(f"响应数据: {response.json()}")


def example_post_request():
    """示例2: 发送POST请求"""
    print("\n" + "="*60)
    print("示例2: 发送POST请求")
    print("="*60)

    app = Bootstrap().with_settings(Settings).build()
    runtime = app.run()
    http = runtime.http_client()

    # 准备数据
    user_data = {
        "name": "张三",
        "email": "zhangsan@example.com",
        "username": "zhangsan"
    }

    # 发送POST请求
    response = http.post("/users", json=user_data)

    print(f"状态码: {response.status_code}")
    print(f"响应数据: {response.json()}")


def example_with_headers():
    """示例3: 带自定义请求头"""
    print("\n" + "="*60)
    print("示例3: 带自定义请求头")
    print("="*60)

    app = Bootstrap().with_settings(Settings).build()
    runtime = app.run()
    http = runtime.http_client()

    # 设置自定义请求头
    headers = {
        "X-Custom-Header": "CustomValue",
        "Authorization": "Bearer token123"
    }

    response = http.get("/users/1", headers=headers)

    print(f"状态码: {response.status_code}")
    print(f"请求头已发送: {headers}")


def example_with_params():
    """示例4: 带查询参数"""
    print("\n" + "="*60)
    print("示例4: 带查询参数")
    print("="*60)

    app = Bootstrap().with_settings(Settings).build()
    runtime = app.run()
    http = runtime.http_client()

    # 设置查询参数
    params = {
        "userId": 1
    }

    response = http.get("/posts", params=params)

    print(f"状态码: {response.status_code}")
    print(f"返回 {len(response.json())} 条记录")
    print(f"第一条: {response.json()[0]['title']}")


def example_error_handling():
    """示例5: 错误处理"""
    print("\n" + "="*60)
    print("示例5: 错误处理")
    print("="*60)

    app = Bootstrap().with_settings(Settings).build()
    runtime = app.run()
    http = runtime.http_client()

    try:
        # 请求不存在的资源
        response = http.get("/users/99999")

        if response.status_code == 404:
            print("⚠️ 资源未找到")
        else:
            print(f"响应数据: {response.json()}")

    except Exception as e:
        print(f"❌ 请求失败: {e}")


if __name__ == "__main__":
    print("\n" + "🚀 HTTP客户端使用示例")
    print("="*60)

    # 运行所有示例
    example_get_request()
    example_post_request()
    example_with_headers()
    example_with_params()
    example_error_handling()

    print("\n" + "="*60)
    print("✅ 所有示例执行完成!")
    print("="*60)
