#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <unistd.h>
#include <arpa/inet.h>

#define MAX_DATA_SIZE 1024

int main(int argument_count, char const *argument_values[])
{
    if (argument_count != 3)
    {
        printf("Example: ./client [IP] [PORT]\n");
        return -1;
    }

    int client_socket = 0;
    struct sockaddr_in server_address;
    char data_buffer[MAX_DATA_SIZE] = {0};
    char user_input[MAX_DATA_SIZE] = {0};

    // Create socket
    if ((client_socket = socket(AF_INET, SOCK_STREAM, 0)) < 0)
    {
        printf("\n Socket creation error \n");
        return -1;
    }

    server_address.sin_family = AF_INET;
    server_address.sin_port = htons(atoi(argument_values[2]));

    // Convert IPv4 and IPv6 addresses from text to binary form
    if (inet_pton(AF_INET, argument_values[1], &server_address.sin_addr) <= 0)
    {
        printf("\nInvalid address/ Address not supported \n");
        return -1;
    }

    // Connect
    if (connect(client_socket, (struct sockaddr *)&server_address, sizeof(server_address)) < 0)
    {
        printf("\nConnection Failed \n");
        return -1;
    }

    while (1)
    {
        printf("Enter message: ");
        fgets(user_input, MAX_DATA_SIZE, stdin);
        user_input[strcspn(user_input, "\n")] = 0; // Remove newline char

        send(client_socket, user_input, strlen(user_input), 0);

        memset(data_buffer, 0, MAX_DATA_SIZE);
        read(client_socket, data_buffer, MAX_DATA_SIZE);
        printf("Server said: %s\n", data_buffer);

        if (strcmp(data_buffer, "nif") == 0)
        {
            break;
        }
    }

    close(client_socket);
    return 0;
}