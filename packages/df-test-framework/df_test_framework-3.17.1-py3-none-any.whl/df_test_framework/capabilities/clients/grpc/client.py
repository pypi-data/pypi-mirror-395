"""gRPC 客户端实现

注意：此实现提供了 gRPC 客户端的框架和接口，但实际使用需要：
1. 安装 grpcio: pip install grpcio grpcio-tools
2. 使用 protoc 编译 .proto 文件生成 Python 代码
3. 导入生成的 stub 类

示例：
    # 1. 编译 proto 文件
    # python -m grpc_tools.protoc -I. --python_out=. --grpc_python_out=. service.proto

    # 2. 使用客户端
    from service_pb2_grpc import GreeterStub
    from service_pb2 import HelloRequest

    client = GrpcClient("localhost:50051", GreeterStub)
    request = HelloRequest(name="World")
    response = client.unary_call("SayHello", request)
    print(response.data.message)
"""

from __future__ import annotations

from collections.abc import Iterator
from typing import Any, TypeVar

from loguru import logger

from df_test_framework.capabilities.clients.grpc.interceptors import BaseInterceptor
from df_test_framework.capabilities.clients.grpc.models import (
    ChannelOptions,
    GrpcResponse,
    GrpcStatusCode,
)

T = TypeVar("T")


class GrpcClient:
    """gRPC 客户端

    通用 gRPC 客户端，支持所有 RPC 调用模式

    注意：实际使用需要安装 grpcio 并生成 stub 代码
    """

    def __init__(
        self,
        target: str,
        stub_class: type | None = None,
        secure: bool = False,
        credentials: Any = None,
        options: ChannelOptions | None = None,
        interceptors: list[BaseInterceptor] | None = None,
    ) -> None:
        """初始化 gRPC 客户端

        Args:
            target: 服务器地址，格式为 "host:port"
            stub_class: gRPC stub 类（由 protoc 生成）
            secure: 是否使用 TLS/SSL
            credentials: gRPC 凭证对象
            options: 通道选项
            interceptors: 拦截器列表
        """
        self.target = target
        self.stub_class = stub_class
        self.secure = secure
        self.credentials = credentials
        self.options = options or ChannelOptions()
        self.interceptors = interceptors or []

        self._channel: Any = None
        self._stub: Any = None
        self._metadata: list[tuple[str, str]] = []

        logger.info(f"Initializing gRPC client for {target}")

    def _ensure_grpc_installed(self) -> None:
        """确保 grpcio 已安装"""
        try:
            import grpc  # type: ignore  # noqa: F401
        except ImportError:
            raise ImportError(
                "grpcio is not installed. Please install it with: pip install grpcio grpcio-tools"
            )

    def connect(self) -> None:
        """建立连接"""
        self._ensure_grpc_installed()
        import grpc

        # 创建通道
        if self.secure:
            if self.credentials is None:
                self.credentials = grpc.ssl_channel_credentials()
            self._channel = grpc.secure_channel(
                self.target,
                self.credentials,
                options=self.options.to_grpc_options(),
            )
        else:
            self._channel = grpc.insecure_channel(
                self.target,
                options=self.options.to_grpc_options(),
            )

        # 创建 stub
        if self.stub_class:
            self._stub = self.stub_class(self._channel)

        logger.info(f"Connected to gRPC server at {self.target}")

    def close(self) -> None:
        """关闭连接"""
        if self._channel:
            self._channel.close()
            logger.info("gRPC client closed")

    def add_metadata(self, key: str, value: str) -> None:
        """添加元数据

        Args:
            key: 元数据键
            value: 元数据值
        """
        self._metadata.append((key, value))

    def clear_metadata(self) -> None:
        """清除所有元数据"""
        self._metadata = []

    def add_interceptor(self, interceptor: BaseInterceptor) -> None:
        """添加拦截器

        Args:
            interceptor: 拦截器实例
        """
        self.interceptors.append(interceptor)

    def _apply_interceptors_request(
        self,
        method: str,
        request: Any,
        metadata: list[tuple[str, str]],
    ) -> tuple[Any, list[tuple[str, str]]]:
        """应用请求拦截器"""
        for interceptor in self.interceptors:
            request, metadata = interceptor.intercept_unary(method, request, metadata)
        return request, metadata

    def _apply_interceptors_response(
        self,
        method: str,
        response: Any,
        metadata: dict[str, str],
    ) -> Any:
        """应用响应拦截器"""
        for interceptor in self.interceptors:
            response = interceptor.intercept_response(method, response, metadata)
        return response

    def unary_call(
        self,
        method: str,
        request: Any,
        timeout: float | None = None,
        metadata: list[tuple[str, str]] | None = None,
    ) -> GrpcResponse[Any]:
        """执行一元调用（Unary RPC）

        Args:
            method: 方法名
            request: 请求对象
            timeout: 超时时间（秒）
            metadata: 请求元数据

        Returns:
            gRPC 响应对象

        Raises:
            GrpcError: gRPC 调用失败
        """
        if not self._stub:
            raise RuntimeError("Not connected. Call connect() first.")

        # 合并元数据
        combined_metadata = list(self._metadata)
        if metadata:
            combined_metadata.extend(metadata)

        # 应用拦截器
        request, combined_metadata = self._apply_interceptors_request(
            method, request, combined_metadata
        )

        try:
            # 获取方法
            rpc_method = getattr(self._stub, method)

            # 执行调用
            response = rpc_method(
                request,
                timeout=timeout,
                metadata=combined_metadata,
            )

            # 应用响应拦截器
            response = self._apply_interceptors_response(method, response, {})

            return GrpcResponse(
                data=response,
                status_code=GrpcStatusCode.OK,
            )

        except Exception as e:
            logger.error(f"gRPC call failed: {e}")
            # 解析 gRPC 错误
            status_code = self._extract_status_code(e)
            return GrpcResponse(
                data=None,
                status_code=status_code,
                message=str(e),
            )

    def server_streaming_call(
        self,
        method: str,
        request: Any,
        timeout: float | None = None,
        metadata: list[tuple[str, str]] | None = None,
    ) -> Iterator[GrpcResponse[Any]]:
        """执行服务端流式调用（Server Streaming RPC）

        Args:
            method: 方法名
            request: 请求对象
            timeout: 超时时间（秒）
            metadata: 请求元数据

        Yields:
            gRPC 响应对象

        Raises:
            GrpcError: gRPC 调用失败
        """
        if not self._stub:
            raise RuntimeError("Not connected. Call connect() first.")

        # 合并元数据
        combined_metadata = list(self._metadata)
        if metadata:
            combined_metadata.extend(metadata)

        # 应用拦截器
        request, combined_metadata = self._apply_interceptors_request(
            method, request, combined_metadata
        )

        response_stream = None
        try:
            # 获取方法
            rpc_method = getattr(self._stub, method)

            # 执行调用
            response_stream = rpc_method(
                request,
                timeout=timeout,
                metadata=combined_metadata,
            )

            # 迭代响应流
            for response in response_stream:
                response = self._apply_interceptors_response(method, response, {})
                yield GrpcResponse(
                    data=response,
                    status_code=GrpcStatusCode.OK,
                )

        except Exception as e:
            logger.error(f"gRPC streaming call failed: {e}")
            status_code = self._extract_status_code(e)
            yield GrpcResponse(
                data=None,
                status_code=status_code,
                message=str(e),
            )
        finally:
            # 确保流资源被正确释放
            if response_stream is not None and hasattr(response_stream, "cancel"):
                try:
                    response_stream.cancel()
                    logger.debug(f"Cancelled streaming call for method: {method}")
                except Exception:
                    # 忽略取消时的错误（流可能已经完成或已取消）
                    pass

    def _extract_status_code(self, error: Exception) -> GrpcStatusCode:
        """从异常中提取 gRPC 状态码"""
        # 尝试从 grpc.RpcError 中提取状态码
        if hasattr(error, "code"):
            try:
                code = error.code()  # type: ignore
                return GrpcStatusCode(code.value[0])  # type: ignore
            except (AttributeError, ValueError):
                pass

        # 默认返回 UNKNOWN
        return GrpcStatusCode.UNKNOWN

    def health_check(self, service: str = "") -> bool:
        """健康检查

        Args:
            service: 服务名称（空字符串表示检查整个服务器）

        Returns:
            服务是否健康
        """
        try:
            # 使用 gRPC Health Checking Protocol
            # https://github.com/grpc/grpc/blob/master/doc/health-checking.md
            from grpc_health.v1 import health_pb2, health_pb2_grpc

            if not self._channel:
                self.connect()

            health_stub = health_pb2_grpc.HealthStub(self._channel)
            request = health_pb2.HealthCheckRequest(service=service)
            response = health_stub.Check(request)

            return response.status == health_pb2.HealthCheckResponse.SERVING

        except Exception as e:
            logger.error(f"Health check failed: {e}")
            return False

    def __enter__(self) -> GrpcClient:
        """上下文管理器入口"""
        self.connect()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:  # type: ignore
        """上下文管理器退出"""
        self.close()
