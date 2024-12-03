from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from .models import User # DeviceToken  # Import any models you need
from firebase_admin import firestore, messaging  # Firebase imports
from cleaning_app.cleaning_app.local_settings import db

#---------------------------------------------------------------------------------------------------------
# Function to save a message in Firestore when a user sends one.
def send_message(request, sender_id, receiver_id):
    sender = get_object_or_404(User, id=sender_id)
    receiver = get_object_or_404(User, id=receiver_id)
    text = request.POST.get("text")
    
    # Firestore chat ID generation based on user IDs
    chat_id = f"{min(sender_id, receiver_id)}_{max(sender_id, receiver_id)}"
    
    # Save the message in Firestore
    message_data = {
        "senderId": sender_id,
        "receiverId": receiver_id,
        "text": text,
        "timestamp": firestore.SERVER_TIMESTAMP,
        "seen": False
    }
    
    db.collection("chats").document(chat_id).collection("messages").add(message_data)
    
    # Update the last message at the chat level for easy querying
    db.collection("chats").document(chat_id).set({
        "lastMessage": text,
        "timestamp": firestore.SERVER_TIMESTAMP
    }, merge=True)

    # Send a notification to the receiver
    send_fcm_notification(receiver_id, text)

    return JsonResponse({"status": "Message sent"})

#---------------------------------------------------------------------------------------------------------
# Function to send  notifications using FCM (Firebase Cloud Messaging)
def send_fcm_notification(receiver_id, message_text):
    try:
        # Retrieve the FCM token for the receiver
        token = DeviceToken.objects.get(user_id=receiver_id).token
        
        # Create a notification payload
        message = messaging.Message(
            notification=messaging.Notification(
                title="New Message",
                body=message_text
            ),
            token=token,
        )
        
        # Send the notification
        response = messaging.send(message)
        print(f"Notification sent successfully: {response}")
    except DeviceToken.DoesNotExist:
        print("No device token found for user.")
    except Exception as e:
        print(f"Error sending notification: {e}")
#------------------------------------------------------------------------------------------------------------
# Function when a user reads a message it marks it as seen in Firestore.
def mark_message_as_seen(request, chat_id, message_id):
    db.collection("chats").document(chat_id).collection("messages").document(message_id).update({
        "seen": True
    })
    return JsonResponse({"status": "Message marked as seen"})