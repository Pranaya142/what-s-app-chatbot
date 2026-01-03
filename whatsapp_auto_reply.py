"""
WhatsApp Auto Reply Bot with AI-Powered Smart Responses
========================================================

This bot monitors WhatsApp Web for incoming messages and automatically
generates context-aware replies based on the message content.

Features:
- Detects wishing messages (birthday, festival, good morning, etc.)
- Generates personalized AI responses
- Auto-sends replies
- Keeps conversation history
- Customizable response templates

WARNING: Use responsibly. Excessive automation may violate WhatsApp ToS.
"""

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
import time
import json
from datetime import datetime
import re

class WhatsAppAutoReply:
    def __init__(self):
        self.driver = None
        self.replied_messages = set()
        self.message_history = []
        
        # Predefined response templates for different types of wishes
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
        """Initialize Chrome driver with WhatsApp Web"""
        print("🚀 Setting up WhatsApp Web...")
        
        chrome_options = Options()
        # Keep user data to avoid scanning QR code every time
        chrome_options.add_argument("--user-data-dir=./User_Data")
        chrome_options.add_argument("--profile-directory=Default")
        
        # Optional: Run in background (comment out to see browser)
        # chrome_options.add_argument("--headless")
        
        self.driver = webdriver.Chrome(options=chrome_options)
        self.driver.get("https://web.whatsapp.com")
        
        print("📱 Please scan the QR code if this is your first time...")
        print("⏳ Waiting for WhatsApp to load...")
        
        # Wait for WhatsApp to load
        try:
            WebDriverWait(self.driver, 60).until(
                EC.presence_of_element_located((By.XPATH, '//div[@contenteditable="true"][@data-tab="3"]'))
            )
            print("✅ WhatsApp loaded successfully!")
            time.sleep(3)
        except Exception as e:
            print(f"❌ Error loading WhatsApp: {e}")
            return False
        
        return True
    
    def detect_message_type(self, message):
        """Detect the type of wishing message"""
        message_lower = message.lower()
        
        # Birthday wishes
        birthday_keywords = ['happy birthday', 'hbd', 'birthday', 'birth day', 'many happy returns']
        if any(keyword in message_lower for keyword in birthday_keywords):
            return 'birthday'
        
        # Good morning
        morning_keywords = ['good morning', 'gm', 'morning', 'good mrng']
        if any(keyword in message_lower for keyword in morning_keywords):
            return 'good_morning'
        
        # Good night
        night_keywords = ['good night', 'gn', 'night', 'sleep well', 'sweet dreams']
        if any(keyword in message_lower for keyword in night_keywords):
            return 'good_night'
        
        # Festivals
        festival_keywords = ['happy diwali', 'happy holi', 'happy christmas', 'eid mubarak', 
                           'happy navratri', 'happy pongal', 'happy onam', 'happy durga puja',
                           'merry christmas', 'happy easter', 'ramadan mubarak']
        if any(keyword in message_lower for keyword in festival_keywords):
            return 'festival'
        
        # New Year
        new_year_keywords = ['happy new year', 'new year', 'happy 2025', 'happy 2026']
        if any(keyword in message_lower for keyword in new_year_keywords):
            return 'new_year'
        
        # Congratulations
        congrats_keywords = ['congratulations', 'congrats', 'well done', 'proud of you', 'great job']
        if any(keyword in message_lower for keyword in congrats_keywords):
            return 'congratulations'
        
        # Get well soon
        health_keywords = ['get well soon', 'feel better', 'speedy recovery', 'take care']
        if any(keyword in message_lower for keyword in health_keywords):
            return 'get_well_soon'
        
        return 'default'
    
    def generate_smart_reply(self, message, message_type):
        """Generate a contextual reply based on message type"""
        import random
        
        templates = self.response_templates.get(message_type, self.response_templates['default'])
        response = random.choice(templates)
        
        # Personalize if festival name is detected
        if message_type == 'festival':
            festival_names = {
                'diwali': 'Diwali',
                'holi': 'Holi',
                'christmas': 'Christmas',
                'eid': 'Eid',
                'navratri': 'Navratri',
                'pongal': 'Pongal',
                'onam': 'Onam'
            }
            for key, value in festival_names.items():
                if key in message.lower():
                    response = response.replace('{festival}', value)
                    break
            response = response.replace('{festival}', 'the festival')
        
        return response
    
    def get_unread_messages(self):
        """Get all unread message chats"""
        try:
            # Find chats with unread messages (green dot indicator)
            unread_chats = self.driver.find_elements(By.XPATH, '//span[@aria-label and contains(@aria-label, "unread")]')
            return unread_chats
        except Exception as e:
            print(f"⚠️ Error getting unread messages: {e}")
            return []
    
    def process_chat(self, chat):
        """Process a single chat and reply if needed"""
        try:
            # Click on the chat
            chat.click()
            time.sleep(2)
            
            # Get contact name
            try:
                contact_name = self.driver.find_element(By.XPATH, '//header//span[@dir="auto"]').text
            except:
                contact_name = "Unknown"
            
            # Get all messages in the chat
            messages = self.driver.find_elements(By.XPATH, '//div[@class="message-in"]//span[@dir="ltr"]')
            
            if not messages:
                return
            
            # Get the last message
            last_message_element = messages[-1]
            last_message = last_message_element.text
            
            # Create unique identifier for this message
            message_id = f"{contact_name}:{last_message}"
            
            # Check if we've already replied to this message
            if message_id in self.replied_messages:
                return
            
            print(f"\n📩 New message from {contact_name}:")
            print(f"   Message: {last_message}")
            
            # Detect message type
            message_type = self.detect_message_type(last_message)
            print(f"   Type: {message_type}")
            
            # Generate reply
            reply = self.generate_smart_reply(last_message, message_type)
            print(f"   Reply: {reply}")
            
            # Send the reply
            self.send_message(reply)
            
            # Mark as replied
            self.replied_messages.add(message_id)
            
            # Save to history
            self.message_history.append({
                'timestamp': datetime.now().isoformat(),
                'contact': contact_name,
                'received': last_message,
                'type': message_type,
                'sent': reply
            })
            
            print(f"✅ Reply sent to {contact_name}!")
            
            # Save history to file
            self.save_history()
            
        except Exception as e:
            print(f"⚠️ Error processing chat: {e}")
    
    def send_message(self, message):
        """Send a message in the current chat"""
        try:
            # Find the message input box
            message_box = self.driver.find_element(By.XPATH, '//div[@contenteditable="true"][@data-tab="10"]')
            
            # Clear and type message
            message_box.clear()
            message_box.send_keys(message)
            time.sleep(1)
            
            # Send message
            message_box.send_keys(Keys.ENTER)
            time.sleep(2)
            
        except Exception as e:
            print(f"❌ Error sending message: {e}")
    
    def save_history(self):
        """Save message history to JSON file"""
        try:
            with open('message_history.json', 'w', encoding='utf-8') as f:
                json.dump(self.message_history, f, indent=2, ensure_ascii=False)
        except Exception as e:
            print(f"⚠️ Error saving history: {e}")
    
    def load_history(self):
        """Load message history from JSON file"""
        try:
            with open('message_history.json', 'r', encoding='utf-8') as f:
                self.message_history = json.load(f)
                # Rebuild replied messages set
                for entry in self.message_history:
                    message_id = f"{entry['contact']}:{entry['received']}"
                    self.replied_messages.add(message_id)
                print(f"📂 Loaded {len(self.message_history)} previous conversations")
        except FileNotFoundError:
            print("📂 No previous history found, starting fresh")
        except Exception as e:
            print(f"⚠️ Error loading history: {e}")
    
    def run(self, check_interval=10):
        """Main loop to monitor and reply to messages"""
        print("\n" + "="*60)
        print("  WhatsApp Auto Reply Bot - AI Powered")
        print("="*60)
        
        if not self.setup_driver():
            return
        
        # Load previous history
        self.load_history()
        
        print(f"\n🤖 Bot is now active!")
        print(f"⏱️  Checking for new messages every {check_interval} seconds")
        print("🛑 Press Ctrl+C to stop\n")
        
        try:
            while True:
                # Get unread chats
                unread_chats = self.get_unread_messages()
                
                if unread_chats:
                    print(f"\n📬 Found {len(unread_chats)} unread chat(s)")
                    
                    for chat in unread_chats:
                        try:
                            self.process_chat(chat)
                        except Exception as e:
                            print(f"⚠️ Error processing chat: {e}")
                            continue
                
                # Wait before next check
                time.sleep(check_interval)
                
        except KeyboardInterrupt:
            print("\n\n🛑 Bot stopped by user")
        except Exception as e:
            print(f"\n❌ Unexpected error: {e}")
        finally:
            self.cleanup()
    
    def cleanup(self):
        """Clean up resources"""
        print("\n🧹 Cleaning up...")
        if self.driver:
            self.driver.quit()
        self.save_history()
        print("✅ Cleanup complete!")

def main():
    bot = WhatsAppAutoReply()
    
    # You can customize the check interval (in seconds)
    bot.run(check_interval=10)  # Check every 10 seconds

if __name__ == "__main__":
    main()
