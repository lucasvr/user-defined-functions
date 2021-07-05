#include <stdio.h>
#include <unistd.h>
#include <sys/types.h>
#include <sys/shm.h>
#include <sys/ipc.h>
#include <string.h>

typedef struct { uint8_t r; uint8_t g; uint8_t b; } pal_t;

extern "C" void dynamic_dataset()
{
    // We export a single dataset that holds the game's framebuffer.
    auto fb_data  = lib.getData<uint8_t>("Framebuffer");
    auto fb_dims  = lib.getDims("Framebuffer");
    size_t size = fb_dims[0] * fb_dims[1] * fb_dims[2];

    int shmid = shmget(666, size, IPC_CREAT|0644);
    if (shmid < 0) {
        fprintf(stderr, "Failed to allocate shared memory segment: %s\n", strerror(errno));
        return;
    }
    void *mm = shmat(shmid, NULL, 0);
    if (mm == (void *) -1)
        fprintf(stderr, "Failed to attach to shared memory segment\n");
    else {
        memcpy(fb_data, ((char *) mm), size);
        shmdt(mm);
    }
}
