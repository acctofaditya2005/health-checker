#include <iostream>              // cout, cin - like python's print/input
#include <string>                // string type
#include <winsock2.h>            // Windows socket library- networking function
#include <ws2tcpip.h>

//Basically allows you to connect to which library we are building AKA ws2_32.lib
#pragma comment(lib, "ws2_32.lib")    

int main(){
    //step1 - initalize Windows sockets
    WSADATA wsaData;
    WSAStartup(MAKEWORD(2,2), &wsaData);

    //step2 - create socket
    SOCKET serverSocket = socket(AF_INET, SOCK_STREAM, 0);

    //step3- bind to port 8080
    sockaddr_in serverAddr;
    serverAddr.sin_family = AF_INET;
    serverAddr.sin_port = htons(8080);
    serverAddr.sin_addr.s_addr = INADDR_ANY;
    bind(serverSocket, (sockaddr*)&serverAddr, sizeof(serverAddr));

    //step4 - listen
    listen(serverSocket, 5);
    std::cout << "Server listening on port 8080..." << std::endl;

    //step5 - accept connection
    SOCKET clientSocket =accept(serverSocket, nullptr, nullptr);
    std::cout << "Client connected!" << std::endl;

    //step6 - receive message
    char buffer[1024] = {0};
    recv(clientSocket, buffer, 1024, 0);
    std::cout << "Recieved: " << buffer << std::endl;

    //Step7 - send response
    std::string response = "Message received:" + std::string(buffer);
    send(clientSocket, response.c_str(), response.size(), 0);

    //Step8 - cleanup
    closesocket(clientSocket);
    closesocket(serverSocket);
    WSACleanup();

    return 0;
}