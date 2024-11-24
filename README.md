# **P2Peek**  
Peer-to-Peer (P2P) Communication Software  

## **Introduction**  
P2Peek is a cutting-edge peer-to-peer communication software that prioritizes secure, reliable, and efficient device-to-device communication. Built using Python and TCP networking principles, P2Peek eliminates the need for centralized servers, offering seamless real-time chat. Ideal for personal communication, collaborative work, and educational purposes, P2Peek empowers users with robust and direct communication capabilities.  

---

## **Features**  
- **Peer-to-Peer Architecture:** Establishes direct connections between devices without intermediaries.  
- **Real-Time Chat:** Enables instant messaging with low latency.  
- **Cross-Platform Compatibility:** Works on Windows, macOS, and Linux.  
- **Secure Communication:** Designed with data integrity and optional encryption in mind (future enhancement).  
- **User-Friendly:** Simple setup and intuitive interface.  

---

## **Prerequisites**  
Ensure the following are installed before running P2Peek:  
- Python 3.7 or higher  
- Required Python libraries (installable via `pip install -r requirements.txt`)  

---

## **Installation**  

1. **Clone the Repository:**  
   ```bash  
   git clone https://github.com/yourusername/P2Peek.git  
   cd P2Peek  
   ```  

2. **Install Dependencies:**  
   ```bash  
   pip install -r requirements.txt  
   ```  

3. **Start the Application:**  
   ```bash  
   flet run main.py  
   ```  

4. **Get Started:**  
   - Enter your _Username_, _Room ID_, and _WS Link_, or select the _Run as Server_ option.  
   - Click **Join Chat** to start communicating.  

---

## **Usage**  

### **Step 1: Application Setup**  
1. Launch the application:  
   ```bash  
   flet run main.py  
   ```  
2. Note the IP address and port displayed by the server (if running as the host).  

### **Step 2: Choose Role - Server or Client**  
- **Server:** Check the "Run as Server" option to host a chat room.  
- **Client:** Provide the WS Link generated by the server to join.  

### **Step 3: Start Chatting**  
- Exchange messages with peers in real time!  

---

## **Folder Structure**  
```plaintext  
P2Peek/  
├── LICENSE                # Our MIT license for Open Source  
├── main.py                # Main application script  
├── requirements.txt       # List of Python dependencies  
└── README.md              # Project documentation  
```  

---

## **Future Enhancements**  
- **NGROK Intgration:** Using NGROK to create public links to enable global level communication
- **End-to-End Encryption:** Implement SSL/TLS for secure data transmission.  
- **Global Communication via WebSockets:** Enable worldwide communication.  
- **File Sharing:** Add functionality for reliable file transfers.  
- **Multi-Peer Communication:** Support group chats and multicast connections.  

---

## **Acknowledgments**  
P2Peek is developed by the **SnykGeeks** team, combining expertise in software security and networking.  

For queries or feedback, please contact [Me](mailto:nithinthelordese@gmail.com).  

---
