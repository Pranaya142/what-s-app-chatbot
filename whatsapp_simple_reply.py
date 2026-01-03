"""
WhatsApp Auto Reply - SIMPLIFIED VERSION
Works WITHOUT Chrome - Uses PyAutoGUI for automation
"""

import pyautogui
import time
import json
from datetime import datetime
import random
import keyboard

class SimpleWhatsAppReply:
    def __init__(self):
        self.replied_messages = set()
        self.message_history = []
        
        self.response_templates = {
            'birthday': [
                "Thank you so much! 🎂 Your wishes made my day special! 🎉",
                "Thanks a lot! Really appreciate your warm wishes! 🎈",
                "Thank you! Your wishes mean a lot to me! 🎁",
            ],
            'good_morning': [
                "Good morning! Have a wonderful day ahead! ☀️",
                "Morning! Wishing you a great day too! 🌅",
                "Good morning! Thanks for the wishes! 😊",
            ],
            'good_night': [
                "Good night! Sweet dreams! 🌙",
                "Night! Sleep well! ⭐",
                "Good night! Rest well! 😴",
            ],
            'festival': [
                "Thank you! Wishing you the same! 🎊",
                "Thanks a lot! Happy {festival} to you too! 🎉",
                "Thank you for the wishes! Enjoy! 🪔",
            ],
            'default': [
                "Thank you! 😊",
                "Thanks a lot! 🙏",
                "Appreciate your message! 😊",
            ]
        }
    
    def detect_message_type(self, message):
        """Detect message type"""
        msg = message.lower()
        
        if any(k in msg for k in ['birthday', 'hbd']):
            return 'birthday'
        if any(k in msg for k in ['good morning', 'gm']):
            return 'good_morning'
        if any(k in msg for k in ['good night', 'gn']):
            return 'good_night'
        if any(k in msg for k in ['diwali', 'christmas', 'eid']):
            return 'festival'
        
        return 'default'
    
    def get_reply(self, message):
        """Generate reply"""
        msg_type = self.detect_message_type(message)
        templates = self.response_templates[msg_type]
        return random.choice(templates)
    
    def manual_mode(self):
        """Manual reply mode - you copy message, bot suggests reply"""
        print("\n" + "="*60)
        print("  WhatsApp Auto Reply - MANUAL MODE")
        print("="*60)
        print("\nHow it works:")
        print("1. You receive a message on WhatsApp")
        print("2. Copy the message text (Ctrl+C)")
        print("3. Come here and paste it")
        print("4. Bot will suggest a reply")
        print("5. Copy the suggested reply back to WhatsApp\n")
        print("Type 'quit' to exit\n")
        
        while True:
            print("-" * 60)
            message = input("\n📩 Paste received message: ").strip()
            
            if message.lower() == 'quit':
                print("\n👋 Goodbye!")
                break
            
            if not message:
                continue
            
            # Detect and generate reply
            msg_type = self.detect_message_type(message)
            reply = self.get_reply(message)
            
            print(f"\n✨ Detected: {msg_type}")
            print(f"💬 Suggested reply:\n\n    {reply}\n")
            print("👆 Copy this and send on WhatsApp!")
            
            # Save to history
            self.message_history.append({
                'timestamp': datetime.now().isoformat(),
                'received': message,
                'type': msg_type,
                'suggested': reply
            })
    
    def save_history(self):
        """Save history"""
        with open('reply_history.json', 'w', encoding='utf-8') as f:
            json.dump(self.message_history, f, indent=2, ensure_ascii=False)
        print(f"\n💾 Saved {len(self.message_history)} replies to reply_history.json")

def main():
    print("""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║     WhatsApp Reply Helper - NO CHROME NEEDED                 ║
║                                                              ║
║  Simple manual mode - YOU copy/paste, BOT suggests reply    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

🎯 THIS VERSION WORKS WITHOUT:
   ✓ No Chrome needed
   ✓ No Selenium needed
   ✓ No browser automation
   ✓ Works on ANY computer

📱 HOW TO USE:
   1. Open WhatsApp on your phone/computer
   2. When you get a wish message
   3. Copy the message text
   4. Paste it here
   5. Bot suggests a perfect reply
   6. Copy and send!

Press ENTER to start...
""")
    
    input()
    
    bot = SimpleWhatsAppReply()
    
    try:
        bot.manual_mode()
    except KeyboardInterrupt:
        print("\n\n👋 Exiting...")
    finally:
        bot.save_history()

if __name__ == "__main__":
    main()
