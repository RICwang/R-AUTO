FROM python:3.10-slim

RUN apt-get update && apt-get install -y gnupg2 curl wget unzip ca-certificates

# 安装 Chrome WebDriver
RUN CHROMEDRIVER_VERSION=`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE` && \
    mkdir -p /opt/chromedriver-$CHROMEDRIVER_VERSION && \
    curl -sS -o /tmp/chromedriver_linux64.zip http://chromedriver.storage.googleapis.com/$CHROMEDRIVER_VERSION/chromedriver_linux64.zip && \
    unzip -qq /tmp/chromedriver_linux64.zip -d /opt/chromedriver-$CHROMEDRIVER_VERSION && \
    rm /tmp/chromedriver_linux64.zip && \
    chmod +x /opt/chromedriver-$CHROMEDRIVER_VERSION/chromedriver && \
    ln -fs /opt/chromedriver-$CHROMEDRIVER_VERSION/chromedriver /usr/local/bin/chromedriver

# 安装 Chrome browser
RUN curl -sS -o - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add - && \
    echo "deb http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list && \
    apt-get -y update && \
    apt-get -y install google-chrome-stable && \
    rm -rf /var/lib/apt/lists/*

# 安装 pip 包
RUN pip install --no-cache-dir DrissionPage Flask

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