"""
Redis缓存示例

演示如何使用DF Test Framework的RedisClient进行缓存操作。

注意：需要先启动Redis服务才能运行此示例。
"""

import json

from pydantic import Field

from df_test_framework import Bootstrap, FrameworkSettings


class Settings(FrameworkSettings):
    """示例配置"""

    redis_url: str = Field(
        default="redis://localhost:6379/0",
        description="Redis连接URL"
    )


def example_basic_operations():
    """示例1: 基础键值操作"""
    print("\n" + "="*60)
    print("示例1: 基础键值操作")
    print("="*60)

    try:
        app = Bootstrap().with_settings(Settings).build()
        runtime = app.run()
        redis = runtime.redis_client()

        # 设置键值
        redis.set("username", "张三")

        # 获取值
        username = redis.get("username")
        print(f"用户名: {username}")

        # 删除键
        redis.delete("username")

        # 检查键是否存在
        exists = redis.exists("username")
        print(f"键是否存在: {exists}")

    except Exception as e:
        print(f"❌ Redis连接失败: {e}")
        print("💡 请确保Redis服务已启动")


def example_expiration():
    """示例2: 设置过期时间"""
    print("\n" + "="*60)
    print("示例2: 设置过期时间")
    print("="*60)

    try:
        app = Bootstrap().with_settings(Settings).build()
        runtime = app.run()
        redis = runtime.redis_client()

        # 设置带过期时间的键（60秒后过期）
        redis.set("session_token", "abc123", ex=60)

        # 查看剩余时间
        ttl = redis.ttl("session_token")
        print(f"剩余时间: {ttl}秒")

        # 清理
        redis.delete("session_token")

    except Exception as e:
        print(f"❌ Redis操作失败: {e}")


def example_json_storage():
    """示例3: 存储JSON数据"""
    print("\n" + "="*60)
    print("示例3: 存储JSON数据")
    print("="*60)

    try:
        app = Bootstrap().with_settings(Settings).build()
        runtime = app.run()
        redis = runtime.redis_client()

        # 准备数据
        user_data = {
            "id": 1,
            "name": "张三",
            "age": 30,
            "email": "zhangsan@example.com"
        }

        # 存储JSON（序列化为字符串）
        redis.set("user:1", json.dumps(user_data))

        # 读取JSON
        stored_data = redis.get("user:1")
        user = json.loads(stored_data)

        print(f"用户信息: {user}")
        print(f"姓名: {user['name']}, 年龄: {user['age']}")

        # 清理
        redis.delete("user:1")

    except Exception as e:
        print(f"❌ Redis操作失败: {e}")


def example_hash_operations():
    """示例4: Hash操作"""
    print("\n" + "="*60)
    print("示例4: Hash操作")
    print("="*60)

    try:
        app = Bootstrap().with_settings(Settings).build()
        runtime = app.run()
        redis = runtime.redis_client()

        # 设置Hash字段
        redis.hset("product:1", "name", "笔记本电脑")
        redis.hset("product:1", "price", "5999.00")
        redis.hset("product:1", "stock", "100")

        # 获取Hash字段
        name = redis.hget("product:1", "name")
        price = redis.hget("product:1", "price")

        print(f"产品名称: {name}")
        print(f"产品价格: {price}")

        # 获取所有字段
        product = redis.hgetall("product:1")
        print(f"完整产品信息: {product}")

        # 清理
        redis.delete("product:1")

    except Exception as e:
        print(f"❌ Redis操作失败: {e}")


def example_list_operations():
    """示例5: List操作（队列）"""
    print("\n" + "="*60)
    print("示例5: List操作（队列）")
    print("="*60)

    try:
        app = Bootstrap().with_settings(Settings).build()
        runtime = app.run()
        redis = runtime.redis_client()

        # 从右侧推入
        redis.rpush("task_queue", "任务1")
        redis.rpush("task_queue", "任务2")
        redis.rpush("task_queue", "任务3")

        # 获取列表长度
        length = redis.llen("task_queue")
        print(f"队列长度: {length}")

        # 从左侧弹出（FIFO）
        task1 = redis.lpop("task_queue")
        task2 = redis.lpop("task_queue")

        print(f"处理任务: {task1}")
        print(f"处理任务: {task2}")

        # 查看剩余任务
        remaining = redis.lrange("task_queue", 0, -1)
        print(f"剩余任务: {remaining}")

        # 清理
        redis.delete("task_queue")

    except Exception as e:
        print(f"❌ Redis操作失败: {e}")


def example_cache_pattern():
    """示例6: 缓存模式（Cache-Aside）"""
    print("\n" + "="*60)
    print("示例6: 缓存模式")
    print("="*60)

    try:
        app = Bootstrap().with_settings(Settings).build()
        runtime = app.run()
        redis = runtime.redis_client()

        def get_user_from_db(user_id: int):
            """模拟从数据库获取用户"""
            print("  📀 从数据库查询...")
            return {
                "id": user_id,
                "name": "张三",
                "email": "zhangsan@example.com"
            }

        def get_user(user_id: int):
            """带缓存的用户查询"""
            cache_key = f"user:{user_id}"

            # 1. 先查缓存
            cached = redis.get(cache_key)
            if cached:
                print("  ⚡ 从缓存读取")
                return json.loads(cached)

            # 2. 缓存未命中，查数据库
            user = get_user_from_db(user_id)

            # 3. 写入缓存（5分钟过期）
            redis.set(cache_key, json.dumps(user), ex=300)

            return user

        # 第一次查询（缓存未命中）
        print("第一次查询用户1:")
        user1 = get_user(1)
        print(f"  结果: {user1['name']}")

        # 第二次查询（缓存命中）
        print("\n第二次查询用户1:")
        user2 = get_user(1)
        print(f"  结果: {user2['name']}")

        # 清理
        redis.delete("user:1")

    except Exception as e:
        print(f"❌ Redis操作失败: {e}")


if __name__ == "__main__":
    print("\n" + "🔴 Redis缓存示例")
    print("="*60)
    print("⚠️ 请确保Redis服务已启动")
    print("="*60)

    # 运行所有示例
    example_basic_operations()
    example_expiration()
    example_json_storage()
    example_hash_operations()
    example_list_operations()
    example_cache_pattern()

    print("\n" + "="*60)
    print("✅ 所有示例执行完成!")
    print("="*60)
