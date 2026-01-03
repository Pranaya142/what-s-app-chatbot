"""
WhatsApp Auto Reply Bot - FIXED VERSION
Works on Windows/Mac/Linux with proper Chrome setup
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
import time
import json
from datetime import datetime
import random

class WhatsAppAutoReply:
    def __init__(self):
        self.driver = None
        self.replied_messages = set()
        self.message_history = []
        
        # Response templates
        self.response_templates = {
            'birthday': [
                "Thank you so much! 🎂 Your wishes made my day special! 🎉",
                "Thanks a lot! Really appreciate your warm wishes! 🎈",
                "Thank you! Your wishes mean a lot to me! 🎁",
                "Thanks for the birthday wishes! Hope you have a great day too! 🥳"
            ],
            'good_morning': [
                "Good morning! Have a wonderful day ahead! ☀️",
                "Morning! Wishing you a great day too! 🌅",
                "Good morning! Thanks for the wishes! 😊",
                "Morning! Hope your day is as bright as your wishes! 🌞"
            ],
            'good_night': [
                "Good night! Sweet dreams! 🌙",
                "Night! Sleep well! ⭐",
                "Good night! Rest well! 😴",
                "Thanks! Good night to you too! 🌃"
            ],
            'festival': [
                "Thank you! Wishing you the same! 🎊",
                "Thanks a lot! Happy {festival} to you and your family! 🎉",
                "Thank you for the wishes! Enjoy the celebrations! 🪔",
                "Thanks! May this festival bring joy and prosperity! ✨"
            ],
            'new_year': [
                "Happy New Year! Wishing you success and happiness! 🎊",
                "Thanks! Happy New Year to you too! 🎆",
                "Thank you! May this year bring you joy! 🎉",
                "Happy New Year! Cheers to new beginnings! 🥂"
            ],
            'congratulations': [
                "Thank you so much! Your support means a lot! 🙏",
                "Thanks a lot! Really appreciate it! 😊",
                "Thank you! Couldn't have done it without support like yours! 💪",
                "Thanks for the kind words! 🎉"
            ],
            'get_well_soon': [
                "Thank you for your concern! Feeling better already! 💚",
                "Thanks a lot! Your wishes help me recover faster! 🙏",
                "Thank you! Appreciate your care! ❤️",
                "Thanks for checking in! Getting better! 😊"
            ],
            'default': [
                "Thank you! 😊",
                "Thanks a lot! 🙏",
                "Appreciate your message! 😊",
                "Thanks for reaching out! 👍"
            ]
        }
        
    def setup_driver(self):
        """Initialize Chrome driver with proper configuration"""
        print("🚀 Setting up Chrome WebDriver...")
        
        try:
            chrome_options = Options()
            
            # User data directory to persist session
            chrome_options.add_argument("--user-data-dir=./User_Data")
            
            # Additional options for stability
            chrome_options.add_argument("--no-sandbox")
            chrome_options.add_argument("--disable-dev-shm-usage")
            chrome_options.add_argument("--disable-blink-features=AutomationControlled")
            chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
            chrome_options.add_experimental_option('useAutomationExtension', False)
            
            # Disable notifications
            prefs = {"profile.default_content_setting_values.notifications": 2}
            chrome_options.add_experimental_option("prefs", prefs)
            
            # Use WebDriver Manager to automatically handle ChromeDriver
            service = Service(ChromeDriverManager().install())
            
            self.driver = webdriver.Chrome(service=service, options=chrome_options)
            self.driver.maximize_window()
            self.driver.get("https://web.whatsapp.com")
            
            print("📱 Please scan the QR code if this is your first time...")
            print("⏳ Waiting for WhatsApp to load (up to 60 seconds)...")
            
            # Wait for WhatsApp to load
            WebDriverWait(self.driver, 60).until(
                EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]'))
            )
            
            print("✅ WhatsApp loaded successfully!")
            time.sleep(3)
            return True
            
        except Exception as e:
            print(f"❌ Error setting up driver: {e}")
            print("\n💡 Troubleshooting tips:")
            print("   1. Make sure Google Chrome is installed")
            print("   2. Check your internet connection")
            print("   3. Try closing all Chrome windows and run again")
            print("   4. Delete 'User_Data' folder if it exists")
            return False
    
    def detect_message_type(self, message):
        """Detect the type of wishing message"""
        message_lower = message.lower()
        
        # Birthday
        if any(kw in message_lower for kw in ['happy birthday', 'hbd', 'birthday']):
            return 'birthday'
        
        # Good morning
        if any(kw in message_lower for kw in ['good morning', 'gm', 'morning']):
            return 'good_morning'
        
        # Good night
        if any(kw in message_lower for kw in ['good night', 'gn', 'night', 'sweet dreams']):
            return 'good_night'
        
        # Festivals
        if any(kw in message_lower for kw in ['happy diwali', 'eid mubarak', 'merry christmas', 
                                               'happy holi', 'happy navratri']):
            return 'festival'
        
        # New Year
        if any(kw in message_lower for kw in ['happy new year', 'new year']):
            return 'new_year'
        
        # Congratulations
        if any(kw in message_lower for kw in ['congratulations', 'congrats', 'well done']):
            return 'congratulations'
        
        # Get well soon
        if any(kw in message_lower for kw in ['get well soon', 'feel better', 'speedy recovery']):
            return 'get_well_soon'
        
        return 'default'
    
    def generate_smart_reply(self, message, message_type):
        """Generate a contextual reply"""
        templates = self.response_templates.get(message_type, self.response_templates['default'])
        response = random.choice(templates)
        
        # Personalize festival wishes
        if message_type == 'festival':
            for festival in ['diwali', 'holi', 'christmas', 'eid', 'navratri']:
                if festival in message.lower():
                    response = response.replace('{festival}', festival.capitalize())
                    break
            response = response.replace('{festival}', 'the festival')
        
        return response
    
    def get_unread_chats(self):
        """Get all chats with unread messages"""
        try:
            # Find all unread message indicators
            unread = self.driver.find_elements(By.XPATH, 
                '//div[contains(@class, "unread") or @aria-label[contains(., "unread")]]')
            return unread[:5]  # Limit to 5 at a time
        except Exception as e:
            print(f"⚠️ Error finding unread chats: {e}")
            return []
    
    def get_last_message(self):
        """Get the last message in current chat"""
        try:
            # Find incoming messages
            messages = self.driver.find_elements(By.XPATH, 
                '//div[contains(@class, "message-in")]//span[@class="_ao3e selectable-text copyable-text"]')
            
            if messages:
                return messages[-1].text
            return None
        except:
            return None
    
    def get_contact_name(self):
        """Get the name of current contact"""
        try:
            name = self.driver.find_element(By.XPATH, '//header//span[@dir="auto"]')
            return name.text
        except:
            return "Unknown"
    
    def send_message(self, message):
        """Send a message in current chat"""
        try:
            # Find message input box
            input_box = WebDriverWait(self.driver, 10).until(
                EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]'))
            )
            
            # Type message
            input_box.send_keys(message)
            time.sleep(0.5)
            
            # Send
            input_box.send_keys(Keys.ENTER)
            time.sleep(1)
            return True
            
        except Exception as e:
            print(f"❌ Error sending message: {e}")
            return False
    
    def process_unread_messages(self):
        """Process all unread messages"""
        unread_chats = self.get_unread_chats()
        
        if not unread_chats:
            return 0
        
        processed = 0
        print(f"\n📬 Found {len(unread_chats)} unread chat(s)")
        
        for chat in unread_chats:
            try:
                # Click on chat
                chat.click()
                time.sleep(2)
                
                # Get contact name
                contact = self.get_contact_name()
                
                # Get last message
                last_msg = self.get_last_message()
                
                if not last_msg:
                    continue
                
                # Check if already replied
                msg_id = f"{contact}:{last_msg}"
                if msg_id in self.replied_messages:
                    continue
                
                # Detect type and generate reply
                msg_type = self.detect_message_type(last_msg)
                
                # Only reply to wish messages
                if msg_type == 'default':
                    continue
                
                reply = self.generate_smart_reply(last_msg, msg_type)
                
                print(f"\n📩 From: {contact}")
                print(f"   Message: {last_msg[:50]}...")
                print(f"   Type: {msg_type}")
                print(f"   Reply: {reply}")
                
                # Send reply
                if self.send_message(reply):
                    self.replied_messages.add(msg_id)
                    self.message_history.append({
                        'timestamp': datetime.now().isoformat(),
                        'contact': contact,
                        'received': last_msg,
                        'type': msg_type,
                        'sent': reply
                    })
                    print(f"   ✅ Sent!")
                    processed += 1
                    
                time.sleep(2)
                
            except Exception as e:
                print(f"⚠️ Error processing chat: {e}")
                continue
        
        return processed
    
    def save_history(self):
        """Save message history"""
        try:
            with open('message_history.json', 'w', encoding='utf-8') as f:
                json.dump(self.message_history, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"⚠️ Error saving history: {e}")
    
    def load_history(self):
        """Load previous message history"""
        try:
            with open('message_history.json', 'r', encoding='utf-8') as f:
                self.message_history = json.load(f)
                for entry in self.message_history:
                    msg_id = f"{entry['contact']}:{entry['received']}"
                    self.replied_messages.add(msg_id)
                print(f"📂 Loaded {len(self.message_history)} previous replies")
        except FileNotFoundError:
            print("📂 No previous history found")
        except Exception as e:
            print(f"⚠️ Error loading history: {e}")
    
    def run(self, check_interval=15):
        """Main bot loop"""
        print("\n" + "="*60)
        print("  WhatsApp Auto Reply Bot - AI Powered")
        print("="*60)
        
        if not self.setup_driver():
            print("\n❌ Failed to start. Please check the troubleshooting tips above.")
            return
        
        self.load_history()
        
        print(f"\n🤖 Bot is now ACTIVE!")
        print(f"⏱️  Checking every {check_interval} seconds")
        print(f"🎯 Will auto-reply to: birthday, good morning/night, festivals, etc.")
        print("🛑 Press Ctrl+C to stop\n")
        
        try:
            reply_count = 0
            cycle = 0
            
            while True:
                cycle += 1
                print(f"\r🔄 Cycle {cycle} - Checking for messages...", end="", flush=True)
                
                processed = self.process_unread_messages()
                
                if processed > 0:
                    reply_count += processed
                    self.save_history()
                    print(f"\n📊 Total replies sent: {reply_count}")
                
                time.sleep(check_interval)
                
        except KeyboardInterrupt:
            print("\n\n🛑 Bot stopped by user")
            print(f"📊 Total replies sent: {reply_count}")
        except Exception as e:
            print(f"\n❌ Unexpected error: {e}")
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Cleanup resources"""
        print("\n🧹 Cleaning up...")
        self.save_history()
        if self.driver:
            self.driver.quit()
        print("✅ Goodbye!")

def main():
    print("""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║       WhatsApp Auto Reply Bot - Fixed Version                ║
║                                                              ║
║  This version uses WebDriver Manager for automatic setup    ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

📋 Requirements:
   ✓ Google Chrome installed
   ✓ Internet connection
   ✓ Python packages: selenium, webdriver-manager

💡 First time? You'll need to scan QR code with your phone.

⚙️ Press Ctrl+C anytime to stop the bot.

""")
    
    input("Press ENTER to start...")
    
    bot = WhatsAppAutoReply()
    bot.run(check_interval=15)

if __name__ == "__main__":
    main()
