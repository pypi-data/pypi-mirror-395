import zmq
import threading
import time
import torch
from tensordict import TensorDict
from transfer_queue.utils.zmq_utils import ZMQMessage, ZMQRequestType, ZMQServerInfo

# -------------------------- 服务端（ROUTER 套接字） --------------------------
def router_server():
    context = zmq.Context()
    router_socket = context.socket(zmq.ROUTER)
    router_socket.bind("tcp://127.0.0.1:5555")
    print("ROUTER 服务端已启动，绑定地址：tcp://127.0.0.1:5555")


    # 阶段2：使用 send_multipart/recv_multipart（多帧）通信
    print("\n=== 阶段2：多帧通信（send_multipart/recv_multipart）===")
    # 一次性接收所有帧：[identity, 空帧, 业务帧1, 业务帧2]
    messages = router_socket.recv_multipart()
    id = messages.pop(0)
    response_msg = ZMQMessage.deserialize(messages)
    print(response_msg)

    print(f"ROUTER 收到多帧请求 → identity: {id}, 数据帧1: {response_msg}")

    # 一次性回复所有帧：[identity, 空帧, 回复帧1, 回复帧2]
    router_socket.send_multipart([
        id,
        b"ack1",
        b"ack2"
    ])

    # 关闭资源
    time.sleep(1)
    router_socket.close()
    context.term()

# -------------------------- 客户端（DEALER 套接字） --------------------------
def dealer_client():
    context = zmq.Context()
    dealer_socket = context.socket(zmq.DEALER)
    # 设置客户端 identity（ROUTER 需通过此标识路由消息）
    dealer_socket.setsockopt_string(zmq.IDENTITY, "client_001")
    dealer_socket.connect("tcp://127.0.0.1:5555")
    print("DEALER 客户端已启动，连接地址：tcp://127.0.0.1:5555")
    time.sleep(0.5)  # 等待服务端就绪

    nested = torch.nested.as_nested_tensor([torch.randn(3, 5), torch.randn(4, 54)])

    jagged = torch.nested.as_nested_tensor([torch.randn(4, 5), torch.randn(4, 54)], layout=torch.jagged)

    normal_tensor = torch.randn(2, 10, 3)

    td = TensorDict({'nested_tensor': nested, 'tensor': normal_tensor, 'jagged_tensor': jagged}, batch_size=2)

    request_msg = ZMQMessage.create(
        request_type=ZMQRequestType.PUT_DATA,
        sender_id='123',
        receiver_id='456',
        body={"data":td},
    )


    # 阶段2：多帧通信（send_multipart/recv_multipart）
    # 发送：空帧 → 业务帧1 → 业务帧2（identity 自动携带）
    dealer_socket.send_multipart(request_msg.serialize())

    # 接收回复：一次性获取所有帧（空帧 + 回复帧1 + 回复帧2）
    response_frames = dealer_socket.recv_multipart()
    response_frame1 = response_frames[0]
    response_frame2 = response_frames[1]
    print(f"DEALER 收到多帧回复 → 帧1: {response_frame1}, 帧2: {response_frame2}")

    # 关闭资源
    dealer_socket.close()
    context.term()

# -------------------------- 启动线程运行 --------------------------
if __name__ == "__main__":
    # 启动服务端线程
    server_thread = threading.Thread(target=router_server)
    server_thread.start()
    time.sleep(0.5)  # 等待服务端绑定完成

    # 启动客户端线程
    client_thread = threading.Thread(target=dealer_client)
    client_thread.start()

    # 等待线程结束
    server_thread.join()
    client_thread.join()
    print("\n通信结束！")