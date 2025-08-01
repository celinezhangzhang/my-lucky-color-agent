import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.header import Header
import datetime
from lunarcalendar import Lunar  # 使用 lunarcalendar 中的 Lunar 类进行日期转换
import os

def generate_email_content():
    """生成邮件内容"""
    today = datetime.datetime.now()
    lunar_date = Lunar(today.year, today.month, today.day)

    day_gan_zhi = lunar_date.get_day_in_ganzhi()  # 获取干支
    today_element = lunar_date.get_wuxing()  # 获取五行

    # 定义五行颜色映射关系
    wuxing_map = {
        "金": {"我生": "黑色、蓝色、灰色 (金生水)", "同我": "白色、金色、银色 (金同)", "生我": "黄色、棕色、米色 (土生金)"},
        "木": {"我生": "红色、粉色、紫色 (木生火)", "同我": "绿色、青色、碧色 (木同)", "生我": "黑色、蓝色、灰色 (水生木)"},
        "水": {"我生": "绿色、青色、碧色 (水生木)", "同我": "黑色、蓝色、灰色 (水同)", "生我": "白色、金色、银色 (金生水)"},
        "火": {"我生": "黄色、棕色、米色 (火生土)", "同我": "红色、粉色、紫色 (火同)", "生我": "绿色、青色、碧色 (木生火)"},
        "土": {"我生": "白色、金色、银色 (土生金)", "同我": "黄色、棕色、米色 (土同)", "生我": "红色、粉色、紫色 (火生土)"}
    }

    colors = wuxing_map.get(today_element, {})
    good_hours = lunar_date.get_good_hours()  # 获取良辰吉时
    pengzu_gan = lunar_date.get_pengzu_gan()  # 彭祖百忌
    pengzu_zhi = lunar_date.get_pengzu_zhi()  # 彭祖地支
    day_yi = lunar_date.get_day_yi()  # 今日所宜
    day_ji = lunar_date.get_day_ji()  # 今日所忌

    # 构建 HTML 邮件内容
    email_content_html = f"""
    <html>
    <head>
        <style>
            body {{ font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif; line-height: 1.6; color: #333; }}
            .container {{ max-width: 600px; margin: 20px auto; padding: 20px; border: 1px solid #eee; border-radius: 10px; box-shadow: 0 2px 5px rgba(0,0,0,0.1); }}
            h2 {{ color: #2c3e50; border-bottom: 2px solid #3498db; padding-bottom: 10px;}}
            h3 {{ color: #34495e; }}
            .tip {{ background-color: #f8f9fa; border-left: 4px solid #3498db; padding: 15px; margin: 20px 0; }}
            .footer {{ font-size: 0.9em; color: #7f8c8d; text-align: center; margin-top: 20px;}}
        </style>
    </head>
    <body>
        <div class="container">
            <h2>AI为您定制的今日五行指南 🌿</h2>
            <p>早上好！新的一天，祝您顺心如意。</p>
            <h3>📅 基本信息</h3>
            <ul>
                <li><b>公历:</b> {today.strftime('%Y-%m-%d')}</li>
                <li><b>农历:</b> {lunar_date.to_full_string()}</li>
                <li><b>今日干支:</b> {day_gan_zhi} (本日五行属: <strong>{today_element}</strong>)</li>
            </ul>
            <h3>👗 今日穿衣幸运色</h3>
            <div class="tip">
                <p><b>🥇 大吉（我生，精力充沛）:</b> {colors.get('我生', '暂无')}</p>
                <p><b>🥈 次吉（同我，增强力量）:</b> {colors.get('同我', '暂无')}</p>
                <p><b>👍 平安（生我，得贵人助）:</b> {colors.get('生我', '暂无')}</p>
            </div>
            <h3>✅ 今日提醒</h3>
            <ul>
                <li><b>今日所宜:</b> {', '.join(day_yi) if day_yi else '无'}</li>
                <li><b>今日所忌:</b> {', '.join(day_ji) if day_ji else '无'}</li>
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
    return email_content_html

def send_email(email_content_html):
    """发送邮件的函数"""
    sender_email = os.environ.get('ziyoulafei@163.com')
    app_password = os.environ.get('AWfYVg24fSTDhqJh')
    receiver_email = os.environ.get('ziyoulafei@163.com')

    if not sender_email or not app_password:
        print("❌ 严重错误: 无法从Secrets中获取邮箱或授权码！请检查GitHub Secrets配置。")
        return

    try:
        msg = MIMEMultipart()
        msg['From'] = Header(f"专属AI助手 <{sender_email}>")
        msg['To'] = Header(f"亲爱的主人 <{receiver_email}>")
        msg['Subject'] = Header(f"【AI Agent】今日五行运势播报 ({datetime.date.today()})", 'utf-8')
        msg.attach(MIMEText(email_content_html, 'html', 'utf-8'))

        print("步骤1: 连接到SMTP服务器 smtp.163.com:465...")
        server = smtplib.SMTP_SSL("smtp.163.com", 465)
        print("连接成功。")

        print("步骤2: 开启调试模式...")
        server.set_debuglevel(1)

        print(f"步骤3: 使用授权码登录邮箱 {sender_email}...")
        server.login(sender_email, app_password)
        print("登录成功。")

        print("步骤4: 发送邮件...")
        server.sendmail(sender_email, [receiver_email], msg.as_string())
        print("✅ 邮件已从脚本成功发出！如果仍未收到，请检查下方服务器日志。")

        server.quit()
        print("连接已关闭。")

    except Exception as e:
        print("❌ 在邮件发送过程中发生致命错误！")
        print(f"错误类型: {type(e).__name__}")
        print(f"错误详情: {e}")

if __name__ == "__main__":
    email_content_html = generate_email_content()
    if email_content_html:
        send_email(email_content_html)
    else:
        print("邮件内容生成失败，已跳过发送步骤。")
