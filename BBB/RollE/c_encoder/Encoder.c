/* Quadrature Encoder Pulse Decoder
 *
 * This code is to be used with BBBIOlib by VigitableAvenger.
 * https://github.com/VegetableAvenger/BBBIOlib
 *
 * This code shows how to get motor's shaft position with high CPR Encoders.
 * Connect encoder channel A and B to Beaglebone Black's GPIO P8_45 and P8_46.
*/
#include <stdio.h>
#include <stdlib.h>
#include <sys/mman.h>	/* For mmap */
#include <fcntl.h>		/* For O_* constants */
#include "BBBio_lib/BBBiolib.h"
//--------------------------------------------------------------
#define DEBUG		0
#define N			3
#define SHM_FILE	"encoders.shm"
 
struct encoderStruct {
	int pinA;
	int pinB;
	int position;
	int lastState;
};

struct encoderStruct encoders[N] = {
	{BBBIO_GPIO_PIN_14, BBBIO_GPIO_PIN_12, 0, 0}, // P8_37, P8_39
	{BBBIO_GPIO_PIN_13, BBBIO_GPIO_PIN_17, 0, 0}, // P8_40, P8_34
	{BBBIO_GPIO_PIN_16, BBBIO_GPIO_PIN_15, 0, 0}  // P8_36, P8_38
};

int readPins;

int getState()
{
	int i = 0;
	int finalState = 0;
	int rawState = BBBIO_GPIO_get(BBBIO_GPIO2, readPins);

	for(i = 0; i < N; i++) {
		if(rawState & encoders[i].pinA)
			finalState |= 2 << (i*2);
		if(rawState & encoders[i].pinB)
			finalState |= 1 << (i*2);
	}
	
	return finalState;
}

int main(void)
{
	int fd = -1;
	int size = N*sizeof(int);

	fd = open(SHM_FILE, O_CREAT | O_RDWR, 0755);
	if(fd == -1) {
		printf("Error 1");
		return -1;
	}

	ftruncate(fd, size);
	int* data = (int*) mmap(NULL, size, PROT_WRITE | PROT_READ, MAP_SHARED, fd, 0);
	
	int i = 0;
	readPins = encoders[0].pinA | encoders[0].pinB | encoders[1].pinA | encoders[1].pinB | encoders[2].pinA | encoders[2].pinB;

	int res = 0;
	res = iolib_init();
	if(res == -1) {
		printf("iolib init error");
		return -1;
	}

	res = BBBIO_sys_Enable_GPIO(BBBIO_GPIO2);
	if(res == -1) {
		printf("GPIO2 Enable Error");
		return -1;
	}

	res = BBBIO_GPIO_set_dir(BBBIO_GPIO2 , readPins /* Input */, 0 /* Output */);
	if(res == -1) {
		printf("Error in setting GPIO direction");
		return -1;
	}

	int statePrev = getState();
	int stateCurr = statePrev;

	#if DEBUG
	printf("Turn motor shaft...\n\n");
	#endif

	// Reset Position to zero
	for(i = 0; i < N; i++)
		data[i] = 0;
	
	while(1)
	{
		stateCurr = getState();
		if(stateCurr != statePrev)
		for(i = 0; i < N; i++) {
			int lastposition = encoders[i].position;
			int thisStatePrev = (statePrev >> (i*2)) & 3;
			int thisStateCurr = (stateCurr >> (i*2)) & 3;

			if(thisStatePrev == thisStateCurr) continue;

			switch(thisStatePrev) {
				case 0:
					if(thisStateCurr == 1)
						encoders[i].position++;
					else if(thisStateCurr == 2)
						encoders[i].position--;
					break;
				case 1:
					if(thisStateCurr == 3)
						encoders[i].position++;
					else if(thisStateCurr == 0)
						encoders[i].position--;
					break;
				case 3:
					if(thisStateCurr == 2)
						encoders[i].position++;
					else if(thisStateCurr == 1)
						encoders[i].position--;
					break;
				case 2:
					if(thisStateCurr == 0)
						encoders[i].position++;
					else if(thisStateCurr == 3)
						encoders[i].position--;
					break;
			}

			if(encoders[i].position != lastposition) {
				data[i] = (int)encoders[i].position;
				#if DEBUG
				printf("Position %i: %i\n", i, encoders[i].position);
				#endif
			}
		}
		statePrev = stateCurr;
		
	}
	iolib_free();
	return 0;
}


