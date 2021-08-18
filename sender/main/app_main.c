// /* SPI Slave example, sender (uses SPI master driver)

//    This example code is in the Public Domain (or CC0 licensed, at your option.)

//    Unless required by applicable law or agreed to in writing, this
//    software is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
//    CONDITIONS OF ANY KIND, either express or implied.
// */
// #include <stdio.h>
// #include <stdint.h>
// #include <stddef.h>
// #include <string.h>

// #include "freertos/FreeRTOS.h"
// #include "freertos/task.h"
// #include "freertos/semphr.h"
// #include "freertos/queue.h"

// #include "lwip/sockets.h"
// #include "lwip/dns.h"
// #include "lwip/netdb.h"
// #include "lwip/igmp.h"

// #include "esp_wifi.h"
// #include "esp_system.h"
// #include "esp_event.h"
// #include "nvs_flash.h"
// #include "soc/rtc_periph.h"
// #include "driver/spi_master.h"
// #include "esp_log.h"
// #include "esp_spi_flash.h"

// #include "driver/gpio.h"
// #include "esp_intr_alloc.h"


// /*
// SPI sender (master) example.

// This example is supposed to work together with the SPI receiver. It uses the standard SPI pins (MISO, MOSI, SCLK, CS) to
// transmit data over in a full-duplex fashion, that is, while the master puts data on the MOSI pin, the slave puts its own
// data on the MISO pin.

// This example uses one extra pin: GPIO_HANDSHAKE is used as a handshake pin. The slave makes this pin high as soon as it is
// ready to receive/send data. This code connects this line to a GPIO interrupt which gives the rdySem semaphore. The main
// task waits for this semaphore to be given before queueing a transmission.
// */


// /*
// Pins in use. The SPI Master can use the GPIO mux, so feel free to change these if needed.
// */
// #define GPIO_MOSI 12
// #define GPIO_MISO 13
// #define GPIO_SCLK 15
// #define GPIO_CS 14

// // #define GPIO_INPUT_IO_0    23
// // #define GPIO_INPUT_PIN_SEL  (1ULL<<GPIO_INPUT_IO_0)


// #ifdef CONFIG_IDF_TARGET_ESP32
// #define SENDER_HOST HSPI_HOST
// #define DMA_CHAN    2

// #elif defined CONFIG_IDF_TARGET_ESP32S2
// #define SENDER_HOST SPI2_HOST
// #define DMA_CHAN    SENDER_HOST

// #endif


// //Main application
// void app_main(void)
// {
//     esp_err_t ret;
//     spi_device_handle_t handle;
//     // gpio_config_t io_conf ={
//     //     .intr_type = GPIO_PIN_INTR_DISABLE,
//     //     .mode = GPIO_MODE_INPUT,
//     //     .pin_bit_mask = GPIO_INPUT_PIN_SEL,
//     //     .pull_up_en = 1
//     // };
//     // gpio_config(&io_conf);  



//     //Configuration for the SPI bus
//     spi_bus_config_t buscfg={
//         .mosi_io_num=GPIO_MOSI,
//         .miso_io_num=GPIO_MISO,
//         .sclk_io_num=GPIO_SCLK,
//         .quadwp_io_num=-1,
//         .quadhd_io_num=-1
//     };

//     //Configuration for the SPI device on the other side of the bus
//     spi_device_interface_config_t devcfg={
//         .command_bits=0,
//         .address_bits=0,
//         .dummy_bits=0,
//         .clock_speed_hz=500000,
//         .duty_cycle_pos=128,        //50% duty cycle
//         .mode=0,
//         .spics_io_num=GPIO_CS,
//         .cs_ena_posttrans=3,        //Keep the CS low 3 cycles after transaction, to stop slave from missing the last bit when CS has less propagation delay than CLK
//         .queue_size=3
//     };

//     uint8_t test_buffer[9];
//     uint8_t sendreq_buffer[9] = {0xFF,};
//     uint8_t sendpwm_buffer[9] = {0,};
//     uint8_t recv_buffer[9] = {0};


//     // uint8_t sendbuf[128] = {0};
//     // uint8_t recvbuf[128] = {0};
//     spi_transaction_t t;
//     uint8_t n = 0;
//     // memset(&t, 0, sizeof(t));
//     // uint16_t *test;
//     // uint16_t c = 3;
//     // test = &c;
//     // const TickType_t xDelay = 10 / portTICK_PERIOD_MS;

//     //Initialize the SPI bus and add the device we want to send stuff to.
//     ret=spi_bus_initialize(SENDER_HOST, &buscfg, DMA_CHAN);
//     assert(ret==ESP_OK);
//     ret=spi_bus_add_device(SENDER_HOST, &devcfg, &handle);
//     assert(ret==ESP_OK);

//     // while(1) {
//     //     vTaskDelay( 10000 / portTICK_PERIOD_MS );
//     //     // int res = snprintf(sendbuf, sizeof(sendbuf),
//     //     //         "heyo");
//     //     // if (res >= sizeof(sendbuf)) {
//     //     //     printf("Data truncated\n");
//     //     // }
//     //     // vTaskDelay( xDelay );
//     //     // bool pin_23 = gpio_get_level(GPIO_NUM_23);
//     //     // bool x = 0;
//     //     // if(pin_23){
//     //     //     *test = 4;
//     //     // }
//     //     // else{
//     //     //     *test = 2;
//     //     //     x = 1;
//     //     // }
//     //     if(x){
//     //         // t.length=sizeof(sendbuf)*8;
//     //         t.length = 8;
//     //         t.tx_buffer=test;
//     //         t.rx_buffer=recvbuf;

//     //         ret=spi_device_polling_transmit(handle, &t);
//     //         x = 0;
//     //     // printf("Received: %d\n", recvbuf[0]);
//     //     }
//     // }

//     while (1) {
//         vTaskDelay( 10000 / portTICK_PERIOD_MS );
//         // if(SERIALFLAG){
//             // if(REQ){
//                 memcpy(test_buffer, sendreq_buffer, sizeof(sendreq_buffer));
//             // }
//             // else{
//             //     memcpy(test_buffer, sendpwm_buffer, sizeof(sendpwm_buffer));
//             //     REQ = 1;
//             // }
//             while(n<8){ // em vez de 2 usar o len?
//                 t.length = 8;
//                 t.tx_buffer = test_buffer[n];
//                 printf("TESTING TESTING: %u%u\n", test_buffer[0], test_buffer[1]);
//                 t.rx_buffer = recv_buffer[n];
//                 printf("RECEIVE: %u\n", recv_buffer[n]);
//                 printf("NNNN = %i\n", n);

//                 ret = spi_device_polling_transmit(handle, &t);
//                 n++;
//             }
//             printf("RECEIVE: %u%u%u\n", recv_buffer[0], recv_buffer[1], recv_buffer[2]);
//             printf("RECEIVE: %u\n", test_buffer[0]);
//             // SERIALFLAG = 0;
//             n = 0;          // Use n to block/unblock bt comm?
//         // }
//     }    

//     //Never reached.
//     ret=spi_bus_remove_device(handle);
//     assert(ret==ESP_OK);
// }

/* UART Echo Example

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
#include "driver/uart.h"

/**
 * This is an example which echos any data it receives on UART1 back to the sender,
 * with hardware flow control turned off. It does not use UART driver event queue.
 *
 * - Port: UART1
 * - Receive (Rx) buffer: on
 * - Transmit (Tx) buffer: off
 * - Flow control: off
 * - Event queue: off
 * - Pin assignment: see defines below
 */

// GPIO DEFINES

#define GPIO_MOSI 12
#define GPIO_MISO 13
#define GPIO_SCLK 15
#define GPIO_CS 14

#define SENDER_HOST HSPI_HOST
#define DMA_CHAN 2

// UART DEFINES

#define ECHO_TEST_TXD  (GPIO_NUM_4)
#define ECHO_TEST_RXD  (GPIO_NUM_5)
#define ECHO_TEST_RTS  (UART_PIN_NO_CHANGE)
#define ECHO_TEST_CTS  (UART_PIN_NO_CHANGE)

#define BUF_SIZE (1024)


uint8_t *test;
bool SERIALFLAG = 0;

static void echo_task(void *arg)
{
    /* Configure parameters of an UART driver,
     * communication pins and install the driver */
    uart_config_t uart_config = {
        .baud_rate = 115200,
        .data_bits = UART_DATA_8_BITS,
        .parity    = UART_PARITY_DISABLE,
        .stop_bits = UART_STOP_BITS_1,
        .flow_ctrl = UART_HW_FLOWCTRL_DISABLE,
        .source_clk = UART_SCLK_APB,
    };
    uart_driver_install(UART_NUM_1, BUF_SIZE * 2, 0, 0, NULL, 0);
    uart_param_config(UART_NUM_1, &uart_config);
    uart_set_pin(UART_NUM_1, ECHO_TEST_TXD, ECHO_TEST_RXD, ECHO_TEST_RTS, ECHO_TEST_CTS);

    // Configure a temporary buffer for the incoming data
    uint8_t *data = (uint8_t *) malloc(BUF_SIZE);

    while (1) {
        // Read data from the UART
        int len = uart_read_bytes(UART_NUM_1, data, BUF_SIZE, 20 / portTICK_RATE_MS);
        if(len>0){
            test = data;
            SERIALFLAG = 1;
        }
        // Write data back to the UART
        // uart_write_bytes(UART_NUM_1, (const char *) data, len);
    }
}

void app_main(void)
{
    xTaskCreate(echo_task, "uart_echo_task", 1024, NULL, 10, NULL);

    esp_err_t ret;
    spi_device_handle_t handle;

    // Config for SPI bus
    spi_bus_config_t buscfg={
        .mosi_io_num = GPIO_MOSI,
        .miso_io_num = GPIO_MISO,
        .sclk_io_num = GPIO_SCLK,
        .quadwp_io_num = -1,
        .quadhd_io_num = -1
    };

    // Config for SPI device on the other side of the bus
    spi_device_interface_config_t devcfg = {
        .command_bits = 0,
        .address_bits = 0,
        .dummy_bits = 0,
        .clock_speed_hz = 500000,
        .duty_cycle_pos = 128,
        .mode = 0,
        .spics_io_num = GPIO_CS,
        .cs_ena_posttrans = 3,
        .queue_size = 3
    };

    uint8_t recvbuf[8] = {0};
    uint8_t r_buf[8] = {0};
    spi_transaction_t t;
    memset(&t, 0, sizeof(t));
    uint8_t n = 0;

    // Initialize SPI bus and add partner device
    ret = spi_bus_initialize(SENDER_HOST, &buscfg, DMA_CHAN);
    assert(ret == ESP_OK);
    ret = spi_bus_add_device(SENDER_HOST, &devcfg, &handle);
    assert(ret == ESP_OK);

    while (1) {
        vTaskDelay( 1000 / portTICK_PERIOD_MS );        
        if(SERIALFLAG){
            while(n<2){
                t.length = 8;
                t.tx_buffer = &test[n];
                printf("TESTING TESTING: %u%u\n", test[0], test[1]);
                t.rx_buffer = recvbuf;
                memcpy(&r_buf[n], recvbuf, sizeof(recvbuf));
                printf("RECEIVED: %u\n", r_buf[n]);
                ret = spi_device_polling_transmit(handle, &t);
                n++;
            }    
            // printf("RECEIVED: %i%i\n", ((uint8_t *)t.rx_buffer)[0], ((uint8_t *)t.rx_buffer)[1]);
            printf("FUCKIT: %i%i\n", r_buf[0], r_buf[1]);
            SERIALFLAG = 0;
            n = 0;
        }
    }

    // Never Reached
    ret = spi_bus_remove_device(handle);
    assert(ret == ESP_OK);
    
}
