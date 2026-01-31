import requests
import time
import hashlib
import urllib3

# 禁用 SSL 警告（如果你没有配置 HTTPS 证书的话）
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# ================= 配置区域 =================
# 1. 你的 V免签域名 (注意：不要带 /appHeart，只要域名)
# 根据你提供的信息，应该是这个：
HOST = "http://11111.com"

# 2. 你的通讯密钥 (App 设置里填的那个)
# 根据你的描述，应该是这个数字：
KEY = "123456"

# 3. 模拟 User-Agent (这是关键！)
# 默认使用 Requests 的 UA，如果被拦截，我们稍后可以换成浏览器的 UA 来测试
USER_AGENT = "Mozilla/5.0 (Linux; Android 10; Mobile) VPay/1.0"
# ===========================================

def md5(text):
    return hashlib.md5(text.encode('utf-8')).hexdigest()

def debug_heartbeat():
    print(f"[*] 目标服务器: {HOST}")
    print(f"[*] 通讯密钥: {KEY}")
    print("-" * 40)

    # 1. 模拟 App 生成时间戳 (13位)
    t = str(int(time.time() * 1000))
    
    # 2. 模拟 App 计算签名: md5(t + key)
    sign = md5(t + KEY)
    
    # 3. 构造完整的心跳 URL
    # 标准 V免签接口是 /appHeart
    target_url = f"{HOST}/appHeart?t={t}&sign={sign}"
    
    print(f"[*] 构造请求: {target_url}")
    print(f"[*] 发送请求中...")

    try:
        # 发送请求 (verify=False 忽略 SSL 证书错误)
        response = requests.get(target_url, headers={"User-Agent": USER_AGENT}, verify=False, timeout=10)
        
        # === 结果分析 ===
        print("-" * 40)
        print(f"【HTTP 状态码】: {response.status_code}")
        
        # 打印响应头，看看有没有 'Server: cloudflare'
        server_header = response.headers.get('Server', 'Unknown')
        print(f"【Server 头信息】: {server_header}")
        
        print("\n【响应内容 (前 500 字符)】:")
        print(response.text[:500])
        print("-" * 40)

        # 智能诊断
        if response.status_code == 200:
            if "success" in response.text or "ok" in response.text or response.text.strip() == "1":
                print("✅ 结果: 心跳成功！App 应该也能正常工作。")
            elif "<!DOCTYPE html>" in response.text or "<html" in response.text:
                print("❌ 结果: 状态码 200，但返回的是 HTML 页面！")
                print("💡 原因: 这就是报错 'Value <html>...' 的原因。")
                if "Just a moment" in response.text or "cloudflare" in response.text.lower():
                    print("💡 结论: 被 Cloudflare 五秒盾拦截了！请加白名单。")
                else:
                    print("💡 结论: 可能是伪静态没配置，或者访问到了默认首页。")
            else:
                print("⚠️ 结果: 返回内容格式未知，既不是 HTML 也不是标准 JSON。")
        elif response.status_code == 403:
            print("❌ 结果: 403 Forbidden - 绝对是被防火墙 (Cloudflare/宝塔) 拦截了。")
        elif response.status_code == 404:
            print("❌ 结果: 404 Not Found - 接口地址错误。请检查域名或伪静态设置。")
        elif response.status_code == 500:
            print("❌ 结果: 500 Server Error - PHP 代码报错，请查服务器日志。")
            
    except Exception as e:
        print(f"❌ 请求发生错误: {e}")

if __name__ == "__main__":
    debug_heartbeat()