/* SPI Slave example, sender (uses SPI master driver)

   This example code is in the Public Domain (or CC0 licensed, at your option.)

   Unless required by applicable law or agreed to in writing, this
   software is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
   CONDITIONS OF ANY KIND, either express or implied.
*/
#include <stdio.h>
#include <stdint.h>
#include <stddef.h>
#include <string.h>

#include "freertos/FreeRTOS.h"
#include "freertos/task.h"
#include "freertos/semphr.h"
#include "freertos/queue.h"

#include "lwip/sockets.h"
#include "lwip/dns.h"
#include "lwip/netdb.h"
#include "lwip/igmp.h"

#include "esp_wifi.h"
#include "esp_system.h"
#include "esp_event.h"
#include "nvs_flash.h"
#include "soc/rtc_periph.h"
#include "driver/spi_master.h"
#include "esp_log.h"
#include "esp_spi_flash.h"

#include "driver/gpio.h"
#include "esp_intr_alloc.h"


/*
SPI sender (master) example.

This example is supposed to work together with the SPI receiver. It uses the standard SPI pins (MISO, MOSI, SCLK, CS) to
transmit data over in a full-duplex fashion, that is, while the master puts data on the MOSI pin, the slave puts its own
data on the MISO pin.

This example uses one extra pin: GPIO_HANDSHAKE is used as a handshake pin. The slave makes this pin high as soon as it is
ready to receive/send data. This code connects this line to a GPIO interrupt which gives the rdySem semaphore. The main
task waits for this semaphore to be given before queueing a transmission.
*/


/*
Pins in use. The SPI Master can use the GPIO mux, so feel free to change these if needed.
*/
#define GPIO_MOSI 12
#define GPIO_MISO 13
#define GPIO_SCLK 15
#define GPIO_CS 14

// #define GPIO_INPUT_IO_0    23
// #define GPIO_INPUT_PIN_SEL  (1ULL<<GPIO_INPUT_IO_0)


#define SENDER_HOST HSPI_HOST
#define DMA_CHAN    2



//Main application
void app_main(void)
{
    esp_err_t ret;
    spi_device_handle_t handle;
    // gpio_config_t io_conf ={
    //     .intr_type = GPIO_PIN_INTR_DISABLE,
    //     .mode = GPIO_MODE_INPUT,
    //     .pin_bit_mask = GPIO_INPUT_PIN_SEL,
    //     .pull_up_en = 1
    // };
    // gpio_config(&io_conf);  



    //Configuration for the SPI bus
    spi_bus_config_t buscfg={
        .mosi_io_num=GPIO_MOSI,
        .miso_io_num=GPIO_MISO,
        .sclk_io_num=GPIO_SCLK,
        .quadwp_io_num=-1,
        .quadhd_io_num=-1
    };

    //Configuration for the SPI device on the other side of the bus
    spi_device_interface_config_t devcfg={
        .command_bits=0,
        .address_bits=0,
        .dummy_bits=0,
        .clock_speed_hz=500000,
        .duty_cycle_pos=128,        //50% duty cycle
        .mode=0,
        .spics_io_num=GPIO_CS,
        .cs_ena_posttrans=3,        //Keep the CS low 3 cycles after transaction, to stop slave from missing the last bit when CS has less propagation delay than CLK
        .queue_size=3
    };

    uint8_t test_buffer[9];
    uint8_t sendreq_buffer[9] = {0xFF,0,};
    uint8_t sendpwm_buffer[9] = {0,};
    uint8_t recv_buffer[9] = {0};
    uint8_t r_buf[9] = {0};


    // uint8_t sendbuf[128] = {0};
    // uint8_t recvbuf[128] = {0};
    spi_transaction_t t;
    uint8_t n = 0;
    // memset(&t, 0, sizeof(t));
    // uint16_t *test;
    // uint16_t c = 3;
    // test = &c;
    // const TickType_t xDelay = 10 / portTICK_PERIOD_MS;

    //Initialize the SPI bus and add the device we want to send stuff to.
    ret=spi_bus_initialize(SENDER_HOST, &buscfg, DMA_CHAN);
    assert(ret==ESP_OK);
    ret=spi_bus_add_device(SENDER_HOST, &devcfg, &handle);
    assert(ret==ESP_OK);

    // while(1) {
    //     vTaskDelay( 10000 / portTICK_PERIOD_MS );
    //     // int res = snprintf(sendbuf, sizeof(sendbuf),
    //     //         "heyo");
    //     // if (res >= sizeof(sendbuf)) {
    //     //     printf("Data truncated\n");
    //     // }
    //     // vTaskDelay( xDelay );
    //     // bool pin_23 = gpio_get_level(GPIO_NUM_23);
    //     // bool x = 0;
    //     // if(pin_23){
    //     //     *test = 4;
    //     // }
    //     // else{
    //     //     *test = 2;
    //     //     x = 1;
    //     // }
    //     if(x){
    //         // t.length=sizeof(sendbuf)*8;
    //         t.length = 8;
    //         t.tx_buffer=test;
    //         t.rx_buffer=recvbuf;

    //         ret=spi_device_polling_transmit(handle, &t);
    //         x = 0;
    //     // printf("Received: %d\n", recvbuf[0]);
    //     }
    // }

    while (1) {
        vTaskDelay( 10000 / portTICK_PERIOD_MS );
        // if(SERIALFLAG){
            // if(REQ){
                memcpy(test_buffer, sendreq_buffer, sizeof(sendreq_buffer));
            // }
            // else{
            //     memcpy(test_buffer, sendpwm_buffer, sizeof(sendpwm_buffer));
            //     REQ = 1;
            // }
            while(n<8){ // em vez de 2 usar o len?
                t.length = 8;
                t.rxlength = 8;
                t.tx_buffer = &test_buffer[n];
                printf("TESTING TESTING: %i\n", test_buffer[n]);
                t.rx_buffer = recv_buffer;
                memcpy(&r_buf[n], recv_buffer, sizeof(recv_buffer));
                printf("RECEIVED: %u\n", r_buf[n]);
                printf("NNNN = %i\n", n);

                ret = spi_device_polling_transmit(handle, &t);
                n++;
            }
            printf("FUCKIT: %i%i\n", r_buf[0], r_buf[1]);
            printf("RECEIVE: %u\n", test_buffer[0]);
            // SERIALFLAG = 0;
            n = 0;          // Use n to block/unblock bt comm?
        // }
    }    

    //Never reached.
    ret=spi_bus_remove_device(handle);
    assert(ret==ESP_OK);
}
