# what-s-app-chatbot

Request

{
  `path`: `C:/WhatsAppAutoReply/README.md`,
  `content`: `# WhatsApp Auto Reply Bot 🤖

An intelligent Python bot that automatically replies to WhatsApp messages with AI-powered contextual responses.

## 🌟 Features

- ✅ **Automatic Detection** - Identifies different types of wishes (birthday, festivals, good morning, etc.)
- ✅ **Smart Replies** - Generates contextual and personalized responses
- ✅ **Multiple Templates** - Various response options for each message type
- ✅ **Conversation History** - Keeps track of all auto-replies
- ✅ **No Duplicate Replies** - Ensures each message is replied to only once
- ✅ **Easy Setup** - Simple installation and configuration
- ✅ **Session Persistence** - Stays logged in across restarts

## 📋 Prerequisites

- Python 3.7 or higher
- Google Chrome browser
- ChromeDriver (will be set up automatically)
- WhatsApp account

## 🚀 Installation

### Step 1: Install Python Dependencies

```bash
cd C:/WhatsAppAutoReply
pip install -r requirements.txt
```

### Step 2: Download ChromeDriver

**Option A: Automatic (Recommended)**
```bash
pip install webdriver-manager
```

**Option B: Manual**
1. Download from: https://chromedriver.chromium.org/downloads
2. Match your Chrome version
3. Place `chromedriver.exe` in the project folder

## 📱 Usage

### First Time Setup

1. **Run the bot:**
```bash
python whatsapp_auto_reply.py
```

2. **Scan QR Code:**
   - Chrome will open WhatsApp Web
   - Scan the QR code with your phone
   - Bot will start automatically after successful login

3. **Keep Running:**
   - Keep the terminal window open
   - Bot will monitor and reply automatically
   - Press `Ctrl+C` to stop

### Subsequent Runs

The bot remembers your login session, so you won't need to scan QR code again!

```bash
python whatsapp_auto_reply.py
```

## 🎯 Supported Message Types

The bot recognizes and replies to:

### 1. **Birthday Wishes** 🎂
- Keywords: \"happy birthday\", \"HBD\", \"birthday\"
- Replies: Thank you messages with emojis

### 2. **Good Morning** ☀️
- Keywords: \"good morning\", \"GM\", \"morning\"
- Replies: Morning wishes and greetings

### 3. **Good Night** 🌙
- Keywords: \"good night\", \"GN\", \"night\"
- Replies: Night wishes and sleep well messages

### 4. **Festival Wishes** 🎊
- Keywords: \"happy diwali\", \"eid mubarak\", \"merry christmas\"
- Replies: Festival-specific responses

### 5. **New Year** 🎆
- Keywords: \"happy new year\", \"new year\"
- Replies: New year wishes

### 6. **Congratulations** 🎉
- Keywords: \"congratulations\", \"congrats\", \"well done\"
- Replies: Thank you and appreciation

### 7. **Get Well Soon** 💚
- Keywords: \"get well soon\", \"feel better\"
- Replies: Acknowledgment and thanks

## ⚙️ Configuration

### Customize Response Templates

Edit the `response_templates` dictionary in `whatsapp_auto_reply.py`:

```python
self.response_templates = {
    'birthday': [
        \"Thank you so much! 🎂\",
        \"Thanks! Your wishes made my day! 🎉\",
        # Add more custom responses here
    ],
    # ... other categories
}
```

### Adjust Check Interval

Change how often the bot checks for new messages:

```python
bot.run(check_interval=10)  # Check every 10 seconds
```

Lower values = more responsive but more CPU usage

### Add New Message Types

Add new detection patterns in `detect_message_type()`:

```python
def detect_message_type(self, message):
    message_lower = message.lower()
    
    # Add your custom type
    custom_keywords = ['your', 'keywords', 'here']
    if any(keyword in message_lower for keyword in custom_keywords):
        return 'custom_type'
    
    # ... rest of the code
```

Then add responses in `response_templates`.

## 📊 Message History

All auto-replies are saved in `message_history.json`:

```json
[
  {
    \"timestamp\": \"2025-01-03T10:30:00\",
    \"contact\": \"John Doe\",
    \"received\": \"Happy Birthday!\",
    \"type\": \"birthday\",
    \"sent\": \"Thank you so much! 🎂 Your wishes made my day special! 🎉\"
  }
]
```

## ⚠️ Important Notes

### Legal & Ethical Considerations

1. **WhatsApp Terms of Service**: Automation may violate WhatsApp ToS
2. **Account Risk**: Your account could be temporarily banned
3. **Use Responsibly**: Don't spam or abuse the bot
4. **Personal Use Only**: For personal accounts, not for business spam

### Best Practices

- ✅ Use on your personal account only
- ✅ Don't reply to every message (selective responses)
- ✅ Monitor the bot regularly
- ✅ Stop if you receive warnings from WhatsApp
- ✅ Use reasonable check intervals (10-30 seconds)
- ❌ Don't use for mass messaging
- ❌ Don't leave running 24/7 continuously
- ❌ Don't use on business accounts without proper API

## 🔧 Troubleshooting

### Problem: ChromeDriver not found
**Solution:**
```bash
pip install webdriver-manager
```
Or download manually and place in project folder.

### Problem: QR code doesn't appear
**Solution:**
- Check if Chrome opens properly
- Clear browser cache
- Delete `User_Data` folder and try again

### Problem: Bot doesn't detect messages
**Solution:**
- Increase check interval
- Check if WhatsApp Web loaded properly
- Verify XPath selectors (WhatsApp may update UI)

### Problem: Messages not sending
**Solution:**
- Check internet connection
- Verify message box XPath
- Add longer delays (`time.sleep()`)

### Problem: Account banned/warned
**Solution:**
- Stop using the bot immediately
- Wait 24-48 hours
- Reduce frequency of use
- Consider official WhatsApp Business API

## 🚀 Advanced Features (Optional)

### Integration with AI APIs

Add real AI-powered responses using Claude or GPT:

```python
# Install: pip install anthropic

from anthropic import Anthropic

def generate_ai_reply(self, message):
    client = Anthropic(api_key=\"your-api-key\")
    response = client.messages.create(
        model=\"claude-sonnet-4-20250514\",
        max_tokens=100,
        messages=[{
            \"role\": \"user\",
            \"content\": f\"Generate a friendly reply to: {message}\"
        }]
    )
    return response.content[0].text
```

### Database Integration

Store history in SQLite instead of JSON:

```python
import sqlite3

conn = sqlite3.connect('messages.db')
# ... implement database operations
```

### GUI Interface

Add a tkinter GUI for easier control:

```python
import tkinter as tk
# ... create GUI with start/stop buttons
```

## 📞 Support

For issues or questions:
1. Check this README carefully
2. Review code comments
3. Search for similar issues online
4. Modify code for your specific needs

## 📜 License

This is an educational project. Use at your own risk.

## 🎓 Learning Resources

- Selenium Documentation: https://selenium-python.readthedocs.io/
- WhatsApp Web Automation: Various tutorials online
- Python Best Practices: Official Python docs

## ⚡ Quick Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run bot
python whatsapp_auto_reply.py

# Stop bot
Ctrl + C

# View history
# Open message_history.json in text editor

# Clear history
# Delete message_history.json
```

## 🔮 Future Enhancements

Potential features to add:
- [ ] GUI interface
- [ ] Cloud AI integration (Claude, GPT)
- [ ] Scheduling (only reply during certain hours)
- [ ] Contact whitelist/blacklist
- [ ] Media message support
- [ ] Group message handling
- [ ] Reply delay randomization
- [ ] Sentiment analysis
- [ ] Multi-language support
- [ ] Voice message support

---

**Remember**: Use this bot ethically and responsibly! 🙏

**Happy Automating!** 🤖✨
`
