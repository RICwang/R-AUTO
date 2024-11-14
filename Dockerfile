FROM ricwang/drissionpage:latest

# 安装 pip 包
RUN pip install --no-cache-dir Flask Faker

# 设置工作目录
WORKDIR /app

# 将本地代码复制到容器中
COPY . .

# 赋予 init.sh 和 entrypoint.sh 执行权限
RUN chmod +x init.sh entrypoint.sh

# 映射
VOLUME /app/volume

# 暴露端口
EXPOSE 5000

# 设置入口点，先执行 init.sh，然后运行 main.py
ENTRYPOINT ["/bin/sh", "-c", "/app/entrypoint.sh"]