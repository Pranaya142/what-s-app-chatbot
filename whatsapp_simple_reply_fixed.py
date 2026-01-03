"""
WhatsApp Auto Reply Helper - Simple Version
Works WITHOUT Chrome - Just copy/paste messages
"""

import json
from datetime import datetime
import random

class SimpleWhatsAppReply:
    def __init__(self):
        self.message_history = []
        
        self.response_templates = {
            'birthday': [
                "Thank you so much! Your wishes made my day special!",
                "Thanks a lot! Really appreciate your warm wishes!",
                "Thank you! Your wishes mean a lot to me!",
                "Thanks for the birthday wishes! Hope you have a great day too!"
            ],
            'good_morning': [
                "Good morning! Have a wonderful day ahead!",
                "Morning! Wishing you a great day too!",
                "Good morning! Thanks for the wishes!",
                "Morning! Hope your day is as bright as your wishes!"
            ],
            'good_night': [
                "Good night! Sweet dreams!",
                "Night! Sleep well!",
                "Good night! Rest well!",
                "Thanks! Good night to you too!"
            ],
            'festival': [
                "Thank you! Wishing you the same!",
                "Thanks a lot! Happy {festival} to you and your family!",
                "Thank you for the wishes! Enjoy the celebrations!",
                "Thanks! May this festival bring joy and prosperity!"
            ],
            'new_year': [
                "Happy New Year! Wishing you success and happiness!",
                "Thanks! Happy New Year to you too!",
                "Thank you! May this year bring you joy!",
                "Happy New Year! Cheers to new beginnings!"
            ],
            'congratulations': [
                "Thank you so much! Your support means a lot!",
                "Thanks a lot! Really appreciate it!",
                "Thank you! Couldn't have done it without support like yours!",
                "Thanks for the kind words!"
            ],
            'default': [
                "Thank you!",
                "Thanks a lot!",
                "Appreciate your message!",
                "Thanks for reaching out!"
            ]
        }
    
    def detect_message_type(self, message):
        """Detect the type of message"""
        msg = message.lower()
        
        # Birthday
        if any(k in msg for k in ['happy birthday', 'hbd', 'birthday', 'b\'day']):
            return 'birthday'
        
        # Good morning
        if any(k in msg for k in ['good morning', 'gm', 'morning', 'gud morning']):
            return 'good_morning'
        
        # Good night
        if any(k in msg for k in ['good night', 'gn', 'night', 'gud night', 'sweet dreams']):
            return 'good_night'
        
        # Festivals
        if any(k in msg for k in ['diwali', 'christmas', 'eid', 'holi', 'navratri', 'pongal']):
            return 'festival'
        
        # New Year
        if any(k in msg for k in ['happy new year', 'new year', '2025', '2026']):
            return 'new_year'
        
        # Congratulations
        if any(k in msg for k in ['congratulations', 'congrats', 'well done', 'great job']):
            return 'congratulations'
        
        return 'default'
    
    def get_reply(self, message):
        """Generate appropriate reply"""
        msg_type = self.detect_message_type(message)
        templates = self.response_templates[msg_type]
        reply = random.choice(templates)
        
        # Personalize festival wishes
        if msg_type == 'festival':
            for festival in ['diwali', 'holi', 'christmas', 'eid', 'navratri']:
                if festival in message.lower():
                    reply = reply.replace('{festival}', festival.capitalize())
                    break
            reply = reply.replace('{festival}', 'the festival')
        
        return reply, msg_type
    
    def manual_mode(self):
        """Interactive mode for manual replies"""
        print("\n" + "="*60)
        print("  WhatsApp Reply Helper - Manual Mode")
        print("="*60)
        print("\nHow it works:")
        print("  1. You receive a message on WhatsApp")
        print("  2. Copy the message text (Ctrl+C)")
        print("  3. Come here and paste it")
        print("  4. Bot will suggest a reply")
        print("  5. Copy the suggested reply back to WhatsApp")
        print("\nType 'quit' or 'exit' to stop\n")
        
        reply_count = 0
        
        while True:
            print("-" * 60)
            message = input("\nPaste received message: ").strip()
            
            if message.lower() in ['quit', 'exit', 'q']:
                print(f"\nTotal replies generated: {reply_count}")
                print("Goodbye!")
                break
            
            if not message:
                print("  (Empty message - please paste something)")
                continue
            
            # Generate reply
            reply, msg_type = self.get_reply(message)
            
            print(f"\nDetected Type: {msg_type.replace('_', ' ').title()}")
            print(f"\nSuggested Reply:")
            print(f"\n    {reply}")
            print("\n  ^ Copy this and send on WhatsApp!")
            
            reply_count += 1
            
            # Save to history
            self.message_history.append({
                'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                'received': message,
                'type': msg_type,
                'suggested': reply
            })
    
    def save_history(self):
        """Save reply history to file"""
        if self.message_history:
            try:
                with open('reply_history.json', 'w', encoding='utf-8') as f:
                    json.dump(self.message_history, f, indent=2, ensure_ascii=False)
                print(f"\nSaved {len(self.message_history)} replies to reply_history.json")
            except Exception as e:
                print(f"Could not save history: {e}")

def main():
    """Main function"""
    print("\n")
    print("="*60)
    print("     WhatsApp Reply Helper - NO CHROME NEEDED")
    print("="*60)
    print("\nFeatures:")
    print("  * Works WITHOUT Chrome or any browser")
    print("  * Simple copy-paste interface")
    print("  * Smart reply suggestions")
    print("  * Detects: Birthday, Good Morning/Night, Festivals, etc.")
    print("  * 100% Safe - No automation, no risk")
    print("\nReady to help you reply faster!")
    print("="*60)
    
    input("\nPress ENTER to start...")
    
    bot = SimpleWhatsAppReply()
    
    try:
        bot.manual_mode()
    except KeyboardInterrupt:
        print("\n\nStopped by user (Ctrl+C)")
    except Exception as e:
        print(f"\nError: {e}")
    finally:
        bot.save_history()

if __name__ == "__main__":
    main()
