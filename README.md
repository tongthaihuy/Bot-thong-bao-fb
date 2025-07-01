# 📢 Facebook → Discord Spam Bot

Bot này giúp bạn theo dõi bài đăng mới từ một nhóm Facebook mà bạn đã tham gia, và spam link bài viết đó liên tục vào Discord cho đến khi bạn gửi lệnh `STOP`.

---

## ⚙️ Cấu hình

Tạo file `.env` theo mẫu `.env.example` và điền:

```env
FB_GROUP_URL=https://www.facebook.com/groups/1234567890
FB_COOKIE=c_user=xxxx; xs=xxxx;
BOT_TOKEN=YOUR_DISCORD_BOT_TOKEN
DISCORD_CHANNEL_ID=123456789012345678