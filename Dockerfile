# SauceDemo Behave + Selenium tests
FROM python:3.11-slim

# Install Chrome + Chromedriver
# - Chrome: google-chrome-stable (apt)
# - Chromedriver: downloaded to match Chrome major version (Chrome for Testing metadata)
RUN set -eux; \
    apt-get update; \
    apt-get install -y --no-install-recommends \
      ca-certificates \
      curl \
      gnupg \
      unzip \
      wget \
      xvfb \
      xauth \
      fonts-liberation \
      libasound2 \
      libatk-bridge2.0-0 \
      libatk1.0-0 \
      libc6 \
      libcairo2 \
      libcups2 \
      libdbus-1-3 \
      libexpat1 \
      libfontconfig1 \
      libgcc1 \
      libgbm1 \
      libglib2.0-0 \
      libgtk-3-0 \
      libnspr4 \
      libnss3 \
      libpango-1.0-0 \
      libpangocairo-1.0-0 \
      libstdc++6 \
      libx11-6 \
      libx11-xcb1 \
      libxcb1 \
      libxcomposite1 \
      libxcursor1 \
      libxdamage1 \
      libxext6 \
      libxfixes3 \
      libxi6 \
      libxrandr2 \
      libxrender1 \
      libxss1 \
      libxtst6 \
      xdg-utils; \
    wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | gpg --dearmor -o /usr/share/keyrings/google-linux-signing-key.gpg; \
    echo "deb [arch=amd64 signed-by=/usr/share/keyrings/google-linux-signing-key.gpg] http://dl.google.com/linux/chrome/deb/ stable main" > /etc/apt/sources.list.d/google-chrome.list; \
    apt-get update; \
    apt-get install -y --no-install-recommends google-chrome-stable; \
    CHROME_MAJOR="$(google-chrome --version | sed -E 's/.* ([0-9]+)\..*/\1/')"; \
    export CHROME_MAJOR; \
    CHROMEDRIVER_URL="$(python -c 'import json,os,urllib.request; milestone=os.environ["CHROME_MAJOR"]; data=json.load(urllib.request.urlopen("https://googlechromelabs.github.io/chrome-for-testing/latest-versions-per-milestone-with-downloads.json")); m=data["milestones"].get(str(milestone)); assert m, f"No chrome-for-testing entry for milestone {milestone}"; print([d["url"] for d in m["downloads"]["chromedriver"] if d["platform"]=="linux64"][0])')"; \
    curl -sSL "$CHROMEDRIVER_URL" -o /tmp/chromedriver.zip; \
    unzip -q /tmp/chromedriver.zip -d /tmp; \
    mv /tmp/chromedriver-linux64/chromedriver /usr/local/bin/chromedriver; \
    chmod +x /usr/local/bin/chromedriver; \
    rm -rf /tmp/chromedriver.zip /tmp/chromedriver-linux64; \
    rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV HEADLESS=true
ENV BROWSER=chrome
ENV EXPLICIT_WAIT_TIMEOUT=20

RUN mkdir -p /app/screenshots /app/reports

# Headless Chrome — no Xvfb needed, avoids display-related hangs
CMD ["behave", "-f", "pretty", "--no-color"]
