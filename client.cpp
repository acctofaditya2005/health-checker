#include <iostream>
#include <winsock2.h>
#include <ws2tcpip.h>

#pragma comment(lib, "ws2_32.lib")


int main(){

    WSADATA wsaData;
    WSAStartup(MAKEWORD(2,2), &wsaData);

    SOCKET clientSocket = socket(AF_INET, SOCK_STREAM, 0);

    sockaddr_in serverAdder;
    serverAdder.sin_family = AF_INET;
    serverAdder.sin_port=htons(8080);
    inet_pton(AF_INET,"127.0.0.1", &serverAdder.sin_addr);
    connect(clientSocket,(sockaddr*)&serverAdder, sizeof(serverAdder));
    
    
    std::string response = "Hello from client";
    send(clientSocket, response.c_str(), response.size(), 0);

    char buffer[1024] = {0};
    recv(clientSocket, buffer, sizeof(buffer), 0);
    std::cout <<"Message recived... " << buffer << std::endl;

    closesocket(clientSocket);
    WSACleanup();
    return 0;
}
