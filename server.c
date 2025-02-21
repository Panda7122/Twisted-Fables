#include <arpa/inet.h>
#include <errno.h>
#include <fcntl.h>
#include <getopt.h>
#include <limits.h>
#include <math.h>
#include <netinet/in.h>
#include <regex.h>
#include <signal.h>
#include <stdbool.h>
#include <stddef.h>
#include <stdint.h>
#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <sys/mman.h>
#include <sys/socket.h>
#include <sys/stat.h>
#include <sys/types.h>
#include <time.h>
#include <unistd.h>
#define MAX_CLIENTS 1024
char hostname[256];
int serverfd;
int maxfd;
int serverPort;
int initServer(unsigned short port) {
    struct sockaddr_in server_addr;
    gethostname(hostname, sizeof(hostname));
    serverPort = port;
    serverfd = socket(AF_INET, SOCK_STREAM, 0);
    if (serverfd == -1) {
        perror("Socket creation failed");
        exit(EXIT_FAILURE);
    }

    // set server's address and port
    server_addr.sin_family = AF_INET;
    server_addr.sin_addr.s_addr = INADDR_ANY;
    server_addr.sin_port = htons(port);
    // bind socket
    if (bind(serverfd, (struct sockaddr *)&server_addr, sizeof(server_addr)) == -1) {
        perror("Binding failed");
        close(serverfd);
        exit(EXIT_FAILURE);
    }

    // listening
    if (listen(serverfd, MAX_CLIENTS) == -1) {
        perror("Listen failed");
        close(serverfd);
        exit(EXIT_FAILURE);
    }

    maxfd = getdtablesize();
    dprintf(STDOUT_FILENO, "Server listening on port %d\n", port);
    return 0;
}
int accept_conn() {
    struct sockaddr_in cliaddr;
    size_t clilen;
    int conn_fd;  // fd for a new connection with client

    clilen = sizeof(cliaddr);
    conn_fd = accept(serverfd, (struct sockaddr *)&cliaddr, (socklen_t *)&clilen);
    if (conn_fd < 0) {
        if (errno == EINTR) return -2;

        if (errno == EAGAIN) return -1;  // try again
        if (errno == ENFILE) {
            (void)fprintf(stderr, "out of file descriptor table ... (maxconn %d)\n", maxfd);
            return -1;
        }
        ERR_EXIT("accept");
    }
    return conn_fd;
}
void sig(int num) {
    dprintf(STDERR_FILENO, "close server\n");
    close(serverfd);
    exit(num);
}
int main(int argc, char **argv) {
    initServer(8080);
    signal(SIGINT, sig);
    signal(SIGTERM, SIG_IGN);
    while (1) {
        int conn_fd = accept_conn();
        if (conn_fd == -2) {
            dprintf(STDERR_FILENO, "inter\n");
            break;
        }
        if (conn_fd == -1) {
            perror("Accept failed");

            continue;
        }
        break;
    }
}