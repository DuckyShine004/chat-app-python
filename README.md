# chat-app-python
This Python-based chat application uses TCP sockets secured by the TLS protocol to ensure end-to-end encryption. The TLS protocol employs a 2048-bit RSA server key and a digital certificate, both generated with OpenSSL, to authenticate client-server connections. The server key is also used to create a self-signed certificate.

> [!WARNING]
> The installation guide assume you are using a Unix/Linux system. If you're on Windows, please adjust the paths accordingly.

## Getting Started

To guarantee a seamless experience moving forward, please read and follow the installation instructions carefully.

### Installation

To run the project, simply follow the instructions as listed below:

1. Clone the repository
   ```sh
   git clone https://github.com/DuckyShine004/chat-app-python
   ```
2. Install the required packages
   ```sh
   pip install -r requirements.txt
   ```
3. To simulate a 1-1 client chat connection, start by running the server. (Note: The following assumes you are on a Unix/Linux system. Adjust the path accordingly if you're on Windows.)   
   ```sh
   python src/server/server.py
   ```
4. In a new terminal, run the client by executing
    ```sh
    python main.py
    ```

## Contribution

Any contributions you make are **greatly appreciated**.

If you have a suggestion that would make this better, please fork the repo and create a pull request. Don't forget to give the project a star! (⭐)

1. Fork the Project
2. Create your Feature Branch (`git checkout -b Feat/NewFeature`)
3. Commit your Changes (`git commit -m 'Feat: Added New Feature'`)
4. Push to the Branch (`git push origin Feat/NewFeature`)
5. Open a Pull Request

## License

Distributed under the `MIT License`. See `LICENSE.txt` for more information.

## Contact

Gallon Zhou: [Linkedin](https://www.linkedin.com/in/gallon-zhou-a3739b278/)

Project Link: [https://github.com/DuckyShine004/chat-app-python](https://github.com/DuckyShine004/chat-app-python)


