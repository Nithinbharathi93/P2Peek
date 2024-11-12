## **P2Peek**
Peer-to-Peer (P2P) Communication Software  

## **Introduction**
P2Peek is a peer-to-peer communication software designed for secure, reliable, and efficient communication between devices. Developed using Python and TCP networking principles, P2Peek eliminates the need for centralized servers by establishing direct communication channels between peers. The software supports real-time chat, making it ideal for personal communication, collaborative work, and educational purposes.  

---

## **Features**
- **Peer-to-Peer Architecture:** Direct device-to-device communication without intermediaries.  
- **Real-Time Chat:** Instant messaging with minimal latency.  
- **Cross-Platform:** Compatible with Windows, macOS, and Linux.  
- **Secure Communication:** Ensures data integrity and optional encryption (future scope).  
- **Easy Setup:** Simple and user-friendly configuration.  

---

## **Prerequisites**  
Before running P2Peek, ensure you have the following installed:  
- Python 3.7 or higher  
- Necessary libraries (install via `pip install -r requirements.txt`)  

---

## **Installation**  
1. Clone the repository:  
   ```bash  
   git clone https://github.com/yourusername/P2Peek.git  
   cd P2Peek  
   ```  
2. Install dependencies:  
   ```bash  
   pip install -r requirements.txt  
   ```
2. Get Started:  
   Once the client has started, enter the _Username_, _Room Id_ and the _Pass Code_
   Then `Continue`

---

## **Usage**  
### **Step 1: Host Setup**  
1. Run the host script on the device that will act as the server:  
   ```bash  
   python server.py  
   ```  
2. Note the IP address and port displayed by the host.  

### **Step 2: Client Connection**  
1. Run the client script on the connecting device:  
   ```bash  
   flet run --web main.py
   ```  
2. Enter the host’s IP address and port when prompted.  

### **Step 3: Start Chatting**  
- Exchange messages in real time!  

---

## **Folder Structure**  
```plaintext  
P2Peek/  
├── server.py              # Script to initialize the host  
├── main.py            # Script for client connection  
├── requirements.txt     # List of dependencies  
└── README.md            # Documentation file  
```  


#Future Enhancements
- **End-to-End Encryption:** Implement SSL/TLS for secure data transmission.  
- **Implementing Web Sockets:** Adding the ability to communicate across the globe.   
- **File Sharing:** Introduce a reliable file-sharing feature.  
- **Multi-Peer Communication:** Enable group chats and multicast communication.  

---

#Acknowledgments
P2Peek is a project developed by the **SnykGeeks** team, with a focus on software security and networking principles.  

For queries or feedback, please contact [nithinthelordese@gmail.com](mailto:nithinthelordese@gmail.com).  

--- 

Feel free to modify this README file to suit your specific requirements!
