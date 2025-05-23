from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import sqlite3

app = Flask(__name__)

# Connect to database
def get_response(message):
    conn = sqlite3.connect('chatbot.db')
    cursor = conn.cursor()
    cursor.execute("SELECT answer FROM chatbot WHERE keyword LIKE ?", ('%' + message + '%',))
    row = cursor.fetchone()
    conn.close()
    if row:
        return row[0]
    else:
        return "Sorry, I couldn't understand that. Please try another question."

@app.route("/", methods=["POST"])
def bot():
    incoming_msg = request.values.get('Body', '').lower()
    from_number = request.values.get('From', '')
    phone_number = from_number.replace('whatsapp:', '')

    print("From:", phone_number)
    print("Received:", incoming_msg)

    response = MessagingResponse()
    reply = get_response(incoming_msg)

    # Store conversation log
    conn = sqlite3.connect('chatbot.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO logs (phone, question, answer) VALUES (?, ?, ?)", 
                   (phone_number, incoming_msg, reply))
    conn.commit()
    conn.close()

    response.message(reply)
    return str(response)

if __name__ == "__main__":
    app.run(debug=True)
