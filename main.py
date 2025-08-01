 # --- 这是带有超级调试模式的最终版本 ---

    import smtplib
    from email.mime.text import MIMEText
    from email.mime.multipart import MIMEMultipart
    from email.header import Header
    import datetime
    from lunar_python import Lunar
    import os

    print("AI Agent 启动，开始生成每日信息...")

    # ... [这部分和之前完全一样，是信息生成模块] ...
    # 为了简洁，这里省略，您在粘贴时请保留这部分完整代码
    today_lunar = Lunar.fromDate(datetime.datetime.now())
    day_gan_zhi = today_lunar.getDayInGanZhi()
    day_zhi = day_gan_zhi[1]
    day_wuxing_from_zhi = today_lunar.getDayZhiWuXing()
    wuxing_map = {
        "金": {"생": "黄色、棕色、米色 (土生金)", "self": "白色、金色、银色 (金同)", "克": "绿色、青色 (金克木)"},
        "木": {"생": "黑色、蓝色、灰色 (水生木)", "self": "绿色、青色、碧色 (木同)", "克": "红色、粉色、紫色 (木生火)"}, # 注意：这里修改为木生火为“所生”，而非“所克”
        "水": {"생": "白色、金色、银色 (金生水)", "self": "黑色、蓝色、灰色 (水同)", "克": "黄色、棕色、米色 (水克土)"},
        "火": {"생": "绿色、青色、碧色 (木生火)", "self": "红色、粉色、紫色 (火同)", "克": "白色、金色、银色 (火克金)"},
        "土": {"생": "红色、粉色、紫色 (火生土)", "self": "黄色、棕色、米色 (土同)", "克": "黑色、蓝色、灰色 (土克水)"},
    }
    today_element = day_wuxing_from_zhi
    colors = wuxing_map.get(today_element, {})
    good_hours = today_lunar.getJiShi()
    pengzu_gan = today_lunar.getPengZuGan()
    pengzu_zhi = today_lunar.getPengZuZhi()
    email_content_html = f"""
    <html><body>
    ... [HTML邮件内容和之前一样，这里省略] ...
    <div class="container"><h2>AI为您定制的今日五行指南 🌿</h2><p>早上好！新的一天，祝您顺心如意。</p><h3>📅 基本信息</h3><ul><li><b>公历:</b> {today_lunar.getSolar().toFullString()}</li><li><b>农历:</b> {today_lunar.toFullString()}</li><li><b>今日干支:</b> {day_gan_zhi}</li><li><b>本日五行:</b> {today_element}</li></ul><h3>👗 今日穿衣幸运色</h3><div class="tip"><p><b>🥇 大吉（我生之，食伤生财）:</b> {colors.get('克', '暂无')}</p><p><b>🥈 次吉（同我者，比劫助力）:</b> {colors.get('self', '暂无')}</p><p><b>👍 平（生我者，印绶护身）:</b> {colors.get('생', '暂无')}</p></div><h3>✅ 今日宜忌与吉时</h3><ul><li><b>今日所宜:</b> {', '.join(today_lunar.getDayYi())}</li><li><b>今日所忌:</b> {', '.join(today_lunar.getDayJi())}</li><li><b>良辰吉时:</b> {', '.join(good_hours)}</li><li><b>彭祖百忌:</b> {pengzu_gan}; {pengzu_zhi}</li></ul><div class="footer"><p>此邮件由您的专属AI Agent自动生成并发送</p></div></div>
    </body></html>
    """
    print("信息内容已生成完毕。")


    # --- 邮件发送模块 (调试版) ---
    sender_email = os.environ.get('ziyoulafei@163.com')
    app_password = os.environ.get('AWfYVg24fSTDhqJh')
    receiver_email = os.environ.get('ziyoulafei@163.com')

    print(f"准备发送邮件，发件人: {sender_email}, 收件人: {receiver_email}")
    if not sender_email or not app_password:
        print("❌ 严重错误: 无法从Secrets中获取邮箱或授权码！请检查GitHub Secrets配置。")
    else:
        try:
            msg = MIMEMultipart()
            msg['From'] = Header(f"专属AI助手 <{sender_email}>")
            msg['To'] = Header(f"亲爱的主人 <{receiver_email}>")
            msg['Subject'] = Header(f"【调试】今日五行运势播报 ({datetime.date.today()})", 'utf-8')
            msg.attach(MIMEText(email_content_html, 'html', 'utf-8'))

            print("步骤1: 连接到SMTP服务器 smtp.163.com:465...")
            server = smtplib.SMTP_SSL("smtp.163.com", 465)
            print("连接成功。")

            print("步骤2: 开启调试模式，显示所有通信日志...")
            server.set_debuglevel(1) # 开启详细调试日志
            print("调试模式已开启。")

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
