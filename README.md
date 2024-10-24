# chat-app-python
This Python-based chat application uses TCP sockets secured by the TLS protocol to ensure end-to-end encryption. The TLS protocol employs a 2048-bit RSA server key and a digital certificate, both generated with OpenSSL, to authenticate client-server connections. The server key is also used to create a self-signed certificate.

> [!WARNING]
> The installation guide assume you are using a Unix/Linux system. If you're on Windows, please adjust the paths accordingly.
> Additionally, code documentation is not provided for some of the UI classes, as the code is generated by Qt Designer.
> 
> This project requires Python version 3.7+. Using a Python version lower than 3.7 may cause dependencies to become corrupted or fail to install properly.

## Snapshots
<h3 align="center">Signup/Login</h3>
<p align="center">
  <img src="https://github.com/DuckyShine004/chat-app-python/blob/main/snapshots/signup.png?raw=true" alt="signup" width="400"/>
  <img src="https://github.com/DuckyShine004/chat-app-python/blob/main/snapshots/login.png?raw=true" alt="login" width="400"/>
</p>

<h3 align="center">Chatting</h3>
<p align="center">
  <img src="https://github.com/DuckyShine004/chat-app-python/blob/main/snapshots/bob.png?raw=true" alt="bob" width="400"/>
  <img src="https://github.com/DuckyShine004/chat-app-python/blob/main/snapshots/alice.png?raw=true" alt="alice" width="400"/>
</p>

## Getting Started

To guarantee a seamless experience moving forward, please read and follow the installation instructions carefully.

### Installation
> [!NOTE]
> The `python` command may not be recognised because it wasn’t set as an alias for `python3` during installation. If your system doesn’t recognise the `python` command, use `python3` instead. Similarly, if `pip` isn’t recognised, replace it with `pip3`.

To run the project, simply follow the instructions as listed below:

1. Clone the repository
   ```sh
   git clone https://github.com/DuckyShine004/chat-app-python
   ```
2. Create a virtual environment (ensure you're using Python 3.7 or later, as specified in the assignment brief)
   ```sh
   python -m venv .venv
   ```
3. Activate the virtual environment you have just created
   ```sh
   source .venv/bin/activate # Unix/Linux
   .venv\Scripts\activate # Windows
   ```
4. Before installing dependencies, upgrade pip, setuptools, and wheel by running
   ```sh
   pip install --upgrade pip setuptools wheel
   ```
5. Install the required packages
   ```sh
   pip install -r requirements_unspecified.txt
   ```
6. To simulate a 1-1 client chat connection, start by running the server. (Note: The following assumes you are on a Unix/Linux system. Adjust the path accordingly if you're on Windows. Also run from the root directory of the project)   
   ```sh
   python -m src.server.server
   ```
7. In a new terminal with the activated virtual environment, run the client by executing
   ```sh
   python main.py
   ```
8. Repeat step 7 to connect the second client to the server

## Report and Demo
The report and demo video are located in the `report` directory, along with the corresponding Wireshark captures.

## License

Distributed under the `MIT License`. See `LICENSE.txt` for more information.



