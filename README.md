request file
    ↓
client 读取一行
    ↓
client 把这一行转成协议消息
    ↓
client 通过 TCP socket 发给 server
    ↓
server 收到消息
    ↓
server 解析消息
    ↓
server 操作 tuple_space
    ↓
server 构造响应消息
    ↓
server 通过 TCP socket 回给 client
    ↓
client 打印结果