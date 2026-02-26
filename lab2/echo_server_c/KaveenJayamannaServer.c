#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>

#define SERVER_PORT 5000
#define MAX_MESSAGE_SIZE 1024

void reverse_string(char *text)
{
    int start_index = 0, end_index = strlen(text) - 1;
    while (start_index < end_index)
    {
        char temporary = text[start_index];
        text[start_index++] = text[end_index];
        text[end_index--] = temporary;
    }
}

int main()
{
    int server_socket, client_connection;
    struct sockaddr_in server_address;
    int address_length = sizeof(server_address);
    char message_buffer[MAX_MESSAGE_SIZE] = {0};

    // Create socket
    if ((server_socket = socket(AF_INET, SOCK_STREAM, 0)) == 0)
    {
        perror("Socket failed");
        exit(EXIT_FAILURE);
    }

    // Bind to port 5000
    server_address.sin_family = AF_INET;
    server_address.sin_addr.s_addr = INADDR_ANY;
    server_address.sin_port = htons(SERVER_PORT);

    if (bind(server_socket, (struct sockaddr *)&server_address, sizeof(server_address)) < 0)
    {
        perror("Bind failed");
        exit(EXIT_FAILURE);
    }

    // Listen
    if (listen(server_socket, 3) < 0)
    {
        perror("Listen failed");
        exit(EXIT_FAILURE);
    }

    printf("Server listening on port %d...\n", SERVER_PORT);

    // Accept connection
    if ((client_connection = accept(server_socket, (struct sockaddr *)&server_address, (socklen_t *)&address_length)) < 0)
    {
        perror("Accept failed");
        exit(EXIT_FAILURE);
    }

    while (1)
    {
        memset(message_buffer, 0, MAX_MESSAGE_SIZE);
        int bytes_received = read(client_connection, message_buffer, MAX_MESSAGE_SIZE);
        if (bytes_received <= 0)
            break;

        // Process message
        reverse_string(message_buffer);
        send(client_connection, message_buffer, strlen(message_buffer), 0);

        // Check for termination
        if (strcmp(message_buffer, "nif") == 0)
        {
            printf("Termination signal received. Shutting down.\n");
            break;
        }
    }

    close(client_connection);
    close(server_socket);
    return 0;
}