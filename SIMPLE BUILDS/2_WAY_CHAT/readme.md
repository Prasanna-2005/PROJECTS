# Chat Application 💬

A simple terminal-based chat system built using Python, enabling real-time communication between two users via a central server.

Just like a post office routes letters, this application uses a central server (`server.py`) to receive messages from one user and deliver them to the other. It leverages key networking concepts to emulate how real-world chat services function behind the scenes.

---

## 💡 Concept

We interact with chat apps daily — WhatsApp, Telegram, Signal — and this project mirrors their basic functionality:

* One **server** handles all messaging
* Two or more **clients** connect and communicate
* The **server routes** incoming messages to the right recipient

This project demonstrates how:

* Messages are sent/received in real time
* A persistent connection is maintained
* Multiple users can interact concurrently

---

## 📁 Project Structure

```
CHAT_APPLICATION/
│
├── server.py  # Runs the chat server; handles incoming clients and routing
├── client.py  # Client-side script for users to send/receive messages
└── README.md  # Project documentation
```

---

## 🔧 Technologies Used

* Python (3.x)
* `socket` module for network communication
* `threading` module for handling multiple clients simultaneously

> This project deepened understanding of threading — each client is handled in its own thread, making concurrent communication seamless.

---

## 🚀 How to Run

### Prerequisites

* Python 3 installed on all machines
* All users should be on the same network or have IP access to the server machine

### Step 1: Run the Server (on one machine)

```bash
python server.py
```

### Step 2: Run the Client (on user machines)

```bash
python client.py
```

Each client will:

* Prompt for a username
* Connect to the server
* Send and receive messages in real-time

---

## 🔌 Features

* ✅ Real-time text communication
* ✨ Multi-threaded client handling
* 🌐 Supports multiple users (scalable design)
* ⚡ Minimal dependencies (uses only Python standard library)

---

## 📈 Future Enhancements

* 🎨 GUI using `Tkinter` or `PyQt`
* 🛡️ End-to-end message encryption
* 🛋 Persistent chat logs or database integration
* 📱 Support for mobile clients via web-based interface (Flask/React)

---

## 👤 Author

**Prasanna**
BTech CSE @ IIITDM Kancheepuram
Passionate about Networking, Python, and Real-Time Applications

---

## 🤝 Contributing

Feel free to fork this project and suggest improvements or new features!
---
