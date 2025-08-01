# 这是一个完整的、可直接运行的Python脚本

# 步骤 1: 导入必要的库
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
import datetime
from lunar_python import Lunar # 引入强大的农历计算库

print("AI Agent 正在启动...")

# 步骤 2: 核心信息生成模块 (不再抓取网页)
try:
    # 获取今天的阳历和农历信息
    today_lunar = Lunar.fromDate(datetime.datetime.now())
    
    # 获取核心的日干支和五行
    day_gan_zhi = today_lunar.getDayInGanZhi() # 例如: 壬寅
    day_zhi = day_gan_zhi[1] # 取地支 "寅"
    day_wuxing = today_lunar.getDayNaYin() # 例如：金箔金
    day_wuxing_from_zhi = today_lunar.getDayZhiWuXing() # 根据地支获取五行，例如：木
    
    # 根据五行生克原理定义颜色
    wuxing_map = {
        "金": {"self": "白色、金色、银色", "생": "黄色、棕色、米色", "克": "绿色、青色"},
        "木": {"self": "绿色、青色、碧色", "생": "黑色、蓝色、灰色", "克": "红色、粉色、紫色"},
        "水": {"self": "黑色、蓝色、灰色", "생": "白色、金色、银色", "克": "黄色、棕色、米色"},
        "火": {"self": "红色、粉色、紫色", "생": "绿色、青色、碧色", "克": "白色、金色、银色"},
        "土": {"self": "黄色、棕色、米色", "생": "红色、粉色、紫色", "克": "黑色、蓝色、灰色"},
    }
    
    today_element = day_wuxing_from_zhi
    colors = wuxing_map.get(today_element, {})
    
    # 良辰吉时 (这里用一个简化的示例，实际可以根据日干支计算更复杂的版本)
    good_hours = today_lunar.getJiShi()
    
    # 彭祖百忌
    pengzu_gan = today_lunar.getPengZuGan()
    pengzu_zhi = today_lunar.getPengZuZhi()
    
    print(f"信息生成完毕：今日五行为'{today_element}'")

    # 步骤 3: 邮件内容排版 (使用HTML以获得更美观的格式)
    email_content_html = f"""
    <html>
    <head>
        <style>
            body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif; line-height: 1.6; }}
            .container {{ max-width: 600px; margin: 20px auto; padding: 20px; border: 1px solid #eee; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }}
            h2 {{ color: #333; border-bottom: 2px solid #4CAF50; padding-bottom: 10px;}}
            h3 {{ color: #444; }}
            strong {{ color: #D32F2F; }}
            .tip {{ background-color: #f9f9f9; border-left: 4px solid #4CAF50; padding: 15px; margin: 20px 0; }}
            .footer {{ font-size: 0.9em; color: #777; text-align: center; margin-top: 20px;}}
        </style>
    </head>
    <body>
        <div class="container">
            <h2>AI为您定制的今日五行指南 🌿</h2>
            <p>早上好！新的一天，祝您顺心如意。</p>
            
            <h3>📅 基本信息</h3>
            <ul>
                <li><b>公历:</b> {today_lunar.getSolar().toFullString()}</li>
                <li><b>农历:</b> {today_lunar.toFullString()}</li>
                <li><b>今日干支:</b> {day_gan_zhi}</li>
                <li><b>本日五行:</b> {today_element}</li>
            </ul>

            <h3>👗 今日穿衣幸运色</h3>
            <div class="tip">
                <p><b>🥇 大吉（相生色，生旺自身）:</b> {colors.get('생', '暂无')}</p>
                <p><b>🥈 次吉（同元素，增强力量）:</b> {colors.get('self', '暂无')}</p>
                <p><b>⚠️ 慎用（消耗自身）:</b> {colors.get('克', '暂无')}</p>
            </div>

            <h3>✅ 今日宜忌与吉时</h3>
            <ul>
                <li><b>今日所宜:</b> {', '.join(today_lunar.getDayYi())}</li>
                <li><b>今日所忌:</b> {', '.join(today_lunar.getDayJi())}</li>
                <li><b>良辰吉时:</b> {', '.join(good_hours)}</li>
                <li><b>彭祖百忌:</b> {pengzu_gan}; {pengzu_zhi}</li>
            </ul>

            <div class="footer">
                <p>此邮件由您的专属AI Agent自动生成并发送</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    # 步骤 4: 发送邮件模块
    # --- 请在这里填入您的信息 ---
    sender_email = "ziyoulafei@163.com"  # 您的163邮箱地址
    app_password = "AWfYVg24fSTDhqJh"  # 替换成您的授权码
    receiver_email = "ziyoulafei@163.com" # 接收邮箱，也就是您自己
    # -----------------------------

    # 配置邮件服务器信息
    smtp_server = "smtp.163.com"
    smtp_port = 465  # 使用SSL加密端口

    # 创建邮件对象
    msg = MIMEMultipart()
    msg['From'] = Header(f"您的专属AI助手 <{sender_email}>")
    msg['To'] = Header(f"亲爱的主人 <{receiver_email}>")
    msg['Subject'] = Header(f"今日五行运势播报 ({datetime.date.today()})", 'utf-8')
    
    # 将HTML内容添加到邮件中
    msg.attach(MIMEText(email_content_html, 'html', 'utf-8'))

    # 连接到服务器并发送
    print(f"正在连接到 {smtp_server} 服务器...")
    with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
        print("登录中...")
        server.login(sender_email, app_password)
        print("发送邮件中...")
        server.sendmail(sender_email, [receiver_email], msg.as_string())
        print("✅ 邮件发送成功！")

except Exception as e:
    print(f"❌ 程序运行失败: {e}")
